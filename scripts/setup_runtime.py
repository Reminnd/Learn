#!/usr/bin/env python3
"""Initialize or migrate a Learn runtime outside the Skill checkout."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_DISTRIBUTION_REF = "d08b8005538157e3fda3274cd75033c4cb486f21"
ORPHAN_CHAPTER = "curriculum/stage-01/06-production-hardening.md"
NEXT_CANONICAL_CHAPTER = "curriculum/stage-02/01-state.md"


SEED_MAPPINGS = (
    ("seed/state/current.md", ".learn-agent/progress/current.md"),
    ("seed/notes/index.md", "learning/notes/index.md"),
    ("seed/notes/template.md", "learning/notes/template.md"),
    ("seed/notes/stage-01", "learning/notes/stage-01"),
    ("seed/notes/qa", "learning/qa"),
    ("seed/notes/bug-book.md", "learning/bug-book/bug-book.md"),
    ("seed/progress", "learning/progress"),
    ("seed/project/adr", "learning/adr"),
    ("seed/project/milestones.md", "learning/project/milestones.md"),
    ("seed/project/project-track.md", "learning/project/project-track.md"),
    ("seed/project/target-architecture.md", "learning/project/target-architecture.md"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Learn runtime outside the Skill repository."
    )
    parser.add_argument(
        "--runtime-root",
        required=True,
        type=Path,
        help="Backend root outside the Learn Skill checkout.",
    )
    parser.add_argument(
        "--migrate-legacy",
        action="store_true",
        help="Migrate the legacy learning/ and work/ state before seeding missing files.",
    )
    parser.add_argument(
        "--legacy-ref",
        default=LEGACY_DISTRIBUTION_REF,
        help="Git ref containing the legacy tracked runtime state.",
    )
    return parser.parse_args()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_runtime_root(runtime_root: Path) -> Path:
    resolved_repo = REPO_ROOT.resolve()
    resolved_runtime = runtime_root.expanduser().resolve()
    if is_within(resolved_runtime, resolved_repo):
        raise SystemExit(
            "runtime root must be outside the Learn Skill checkout: "
            f"{resolved_runtime}"
        )
    resolved_runtime.mkdir(parents=True, exist_ok=True)
    return resolved_runtime


def copy_missing(source: Path, target: Path) -> int:
    if not source.exists():
        return 0
    if source.is_file():
        if target.exists():
            return 0
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return 1

    copied = 0
    for child in sorted(source.rglob("*")):
        if not child.is_file():
            continue
        copied += copy_missing(child, target / child.relative_to(source))
    return copied


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line]


def git_blob(ref: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f"{ref}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def extract_legacy_tree(ref: str, source_root: str, target_root: Path) -> int:
    try:
        paths = git_lines("ls-tree", "-r", "--name-only", ref, "--", source_root)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"cannot read legacy ref {ref!r}: {exc}") from exc

    copied = 0
    prefix = f"{source_root}/"
    for path in paths:
        if not path.startswith(prefix):
            continue
        target = target_root / path[len(prefix) :]
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git_blob(ref, path))
        copied += 1
    return copied


def migrate_legacy(runtime_root: Path, legacy_ref: str) -> int:
    copied = 0

    local_control = REPO_ROOT / ".learn-agent"
    if local_control.exists():
        copied += copy_missing(local_control, runtime_root / ".learn-agent")

    local_learning = REPO_ROOT / "learning"
    if local_learning.exists():
        copied += copy_missing(local_learning, runtime_root / "learning")
    copied += extract_legacy_tree(legacy_ref, "learning", runtime_root / "learning")

    local_work = REPO_ROOT / "work"
    if local_work.exists():
        copied += copy_missing(local_work, runtime_root / "workspace")
    copied += extract_legacy_tree(legacy_ref, "work", runtime_root / "workspace")

    return copied


def seed_missing(runtime_root: Path) -> int:
    copied = 0
    for source_rel, target_rel in SEED_MAPPINGS:
        copied += copy_missing(REPO_ROOT / source_rel, runtime_root / target_rel)
    return copied


def rollback_orphan_note_route(runtime_root: Path) -> bool:
    path = runtime_root / "learning" / "notes" / "index.md"
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")
    start_marker = "<!-- learn-agent:evidence:stage-01-ch06-production-hardening-added:start -->"
    end_marker = "<!-- learn-agent:evidence:stage-01-ch06-production-hardening-added:end -->"
    if start_marker not in text or end_marker not in text:
        return False

    start = text.index(start_marker)
    end = text.index(end_marker, start) + len(end_marker)
    block = text[start:end]
    if ORPHAN_CHAPTER not in block and "Chapter 05 mastered → Chapter 06 → Stage 02" not in block:
        return False

    replacement = """<!-- learn-agent:evidence:stage-01-ch06-production-hardening-added:start -->
## Stage 01 / Chapter 06 课程迁移回滚

- attempted_chapter: `06-production-hardening`
- route: `Chapter 05 mastered → Stage 02 / Chapter 01`
- next_chapter: `curriculum/stage-02/01-state.md`
- status: `rolled_back`
- reason: `canonical Stage 01 Chapter 06 was never created`
<!-- learn-agent:evidence:stage-01-ch06-production-hardening-added:end -->"""
    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    return True


def rollback_orphan_state_route(runtime_root: Path) -> bool:
    path = runtime_root / ".learn-agent" / "progress" / "current.md"
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")
    old = f"next_chapter: {ORPHAN_CHAPTER}"
    new = f"next_chapter: {NEXT_CANONICAL_CHAPTER}"
    if old not in text:
        return False
    path.write_text(text.replace(old, new), encoding="utf-8")
    return True


def rollback_orphan_transaction(runtime_root: Path) -> bool:
    path = runtime_root / "workspace" / "stage01-ch06-curriculum-migration.json"
    if not path.exists():
        return False

    data = json.loads(path.read_text(encoding="utf-8"))
    state_updates = data.get("state_updates")
    if not isinstance(state_updates, dict):
        return False
    if state_updates.get("next_chapter") != ORPHAN_CHAPTER:
        return False

    state_updates["next_chapter"] = NEXT_CANONICAL_CHAPTER
    state_updates["last_checkpoint_reason"] = "curriculum_migration_rollback"
    if "last_note_update" in state_updates:
        state_updates["last_note_update"] = (
            "Stage 01 Chapter 06 未完成迁移已回滚；Chapter 05 后继路由恢复为 Stage 02 / Chapter 01"
        )

    rollback_content = (
        "## Stage 01 / Chapter 06 课程迁移回滚\n\n"
        "- attempted_chapter: `06-production-hardening`\n"
        "- route: `Chapter 05 mastered → Stage 02 / Chapter 01`\n"
        "- next_chapter: `curriculum/stage-02/01-state.md`\n"
        "- status: `rolled_back`\n"
        "- reason: `canonical Stage 01 Chapter 06 was never created`"
    )
    for target in data.get("targets", []):
        if not isinstance(target, dict):
            continue
        content = target.get("content")
        if isinstance(content, str) and (
            ORPHAN_CHAPTER in content
            or "Chapter 05 mastered → Chapter 06 → Stage 02" in content
        ):
            target["expected_change"] = "记录未完成的 Stage 01 Chapter 06 迁移已回滚"
            target["content"] = rollback_content

    data["status"] = "rolled_back"
    data["rollback_reason"] = "canonical Stage 01 Chapter 06 was never created"
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return True


def write_manifest(runtime_root: Path, *, replace: bool) -> None:
    manifest = runtime_root / ".learn-agent" / "storage-manifest.yaml"
    if manifest.exists() and not replace:
        return
    manifest.parent.mkdir(parents=True, exist_ok=True)
    backend_root = json.dumps(str(runtime_root), ensure_ascii=False)
    manifest.write_text(
        f"""version: 2
backend: local_workspace
backend_root: {backend_root}
capabilities:
  persistent_read: true
  persistent_write: true
  local_path_exposed: true
  user_browsable: true
  versioned: false
paths:
  state.current: .learn-agent/progress/current.md
  notes.root: learning/notes
  notes.index: learning/notes/index.md
  qa.stage: learning/qa/stage-XX.md
  bugs.book: learning/bug-book/bug-book.md
  progress.code_ability: learning/progress/code-ability.md
  project.root: learning/project
  adr.root: learning/adr
sync_targets: []
""",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    runtime_root = validate_runtime_root(args.runtime_root)

    migrated = 0
    if args.migrate_legacy:
        migrated = migrate_legacy(runtime_root, args.legacy_ref)

    seeded = seed_missing(runtime_root)
    rollback_count = sum(
        (
            rollback_orphan_note_route(runtime_root),
            rollback_orphan_state_route(runtime_root),
            rollback_orphan_transaction(runtime_root),
        )
    )
    write_manifest(runtime_root, replace=args.migrate_legacy)

    print(f"runtime_root={runtime_root}")
    print(f"legacy_files_copied={migrated}")
    print(f"seed_files_copied={seeded}")
    print(f"orphan_routes_rolled_back={rollback_count}")
    print("manifest=.learn-agent/storage-manifest.yaml")


if __name__ == "__main__":
    main()
