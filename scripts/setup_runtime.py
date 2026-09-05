#!/usr/bin/env python3
"""Initialize or migrate a Learn runtime outside the Skill checkout."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_DISTRIBUTION_REF = "d08b8005538157e3fda3274cd75033c4cb486f21"
ORPHAN_CHAPTER = "curriculum/stage-01/06-production-hardening.md"
NEXT_CANONICAL_CHAPTER = "curriculum/stage-02/01-state.md"
MANIFEST_REL = Path(".learn-agent/storage-manifest.yaml")
DEFAULT_PATHS = {
    "state.current": ".learn-agent/progress/current.md",
    "notes.root": "learning/notes",
    "notes.index": "learning/notes/index.md",
    "qa.stage": "learning/qa/stage-XX.md",
    "bugs.book": "learning/bug-book/bug-book.md",
    "progress.code_ability": "learning/progress/code-ability.md",
    "project.root": "learning/project",
    "adr.root": "learning/adr",
}
LEGACY_LEARNING_ROOTS = {"adr", "bug-book", "notes", "progress", "project", "qa"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Learn runtime outside the Skill repository."
    )
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--migrate-legacy", action="store_true")
    parser.add_argument("--legacy-ref", default=LEGACY_DISTRIBUTION_REF)
    return parser.parse_args()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_runtime_root(runtime_root: Path) -> Path:
    root = runtime_root.expanduser().resolve()
    if is_within(root, REPO_ROOT.resolve()):
        raise SystemExit(f"runtime root must be outside the Learn Skill checkout: {root}")
    return root


def scalar(raw: str) -> str:
    value = raw.strip()
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise SystemExit("unsupported storage manifest scalar") from exc
        if not isinstance(parsed, str):
            raise SystemExit("unsupported storage manifest scalar")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if not value or value.startswith("[") or value.startswith("{"):
        raise SystemExit("unsupported storage manifest scalar")
    return value


def manifest_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        raise SystemExit(f"unsupported storage manifest: missing {key}")
    return scalar(match.group(1))


def manifest_paths(text: str) -> dict[str, str]:
    match = re.search(r"(?m)^paths:\s*\n(?P<body>(?:^  [^\n]+\n?)+)", text)
    if not match:
        raise SystemExit("unsupported storage manifest: missing paths")
    result: dict[str, str] = {}
    for line in match.group("body").splitlines():
        key, sep, value = line.strip().partition(":")
        if not sep:
            raise SystemExit("unsupported storage manifest paths")
        result[key.strip()] = scalar(value)
    return result


def runtime_path(root: Path, key: str, raw: str) -> Path:
    relative = Path(raw)
    if relative.is_absolute():
        raise SystemExit(f"unsupported storage manifest: {key} must be relative")
    target = (root / relative).resolve()
    if not is_within(target, root):
        raise SystemExit(f"unsupported storage manifest: {key} escapes backend_root")
    return target


def load_layout(root: Path) -> tuple[dict[str, Path], bool]:
    manifest = root / MANIFEST_REL
    if not manifest.exists():
        return {key: runtime_path(root, key, value) for key, value in DEFAULT_PATHS.items()}, False
    if not manifest.is_file():
        raise SystemExit("unsupported storage manifest: manifest path is not a file")

    text = manifest.read_text(encoding="utf-8")
    if manifest_value(text, "version") != "2":
        raise SystemExit("unsupported storage manifest: version must be 2")
    if manifest_value(text, "backend") != "local_workspace":
        raise SystemExit("unsupported storage manifest: backend must be local_workspace")
    if Path(manifest_value(text, "backend_root")).expanduser().resolve() != root:
        raise SystemExit("unsupported storage manifest: backend_root mismatch")

    raw_paths = manifest_paths(text)
    missing = [key for key in DEFAULT_PATHS if key not in raw_paths]
    if missing:
        raise SystemExit("unsupported storage manifest: missing paths: " + ", ".join(missing))
    if "stage-XX.md" not in raw_paths["qa.stage"]:
        raise SystemExit("unsupported storage manifest: qa.stage must contain stage-XX.md")
    return {key: runtime_path(root, key, raw_paths[key]) for key in DEFAULT_PATHS}, True


def child(root: Path, parent: Path, relative: Path) -> Path:
    target = (parent / relative).resolve()
    if not is_within(target, root):
        raise SystemExit(f"runtime target escapes backend_root: {target}")
    return target


def qa_root(layout: dict[str, Path]) -> Path:
    return layout["qa.stage"].parent


def copy_missing(source: Path, target: Path, *, skip: set[str] | None = None) -> int:
    if not source.exists():
        return 0
    if source.is_file():
        if target.exists():
            return 0
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return 1

    skipped = skip or set()
    copied = 0
    for file in sorted(source.rglob("*")):
        if file.is_file() and file.relative_to(source).as_posix() not in skipped:
            copied += copy_missing(file, target / file.relative_to(source))
    return copied


def git_lines(*args: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"cannot read legacy ref: {exc}") from exc
    return [line for line in result.stdout.splitlines() if line]


def git_blob(ref: str, path: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-C", str(REPO_ROOT), "show", f"{ref}:{path}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"cannot read legacy asset {path!r}: {exc}") from exc


def git_copy_missing(ref: str, source_prefix: str, target: Path, *, skip: set[str] | None = None) -> int:
    skipped = skip or set()
    copied = 0
    prefix = source_prefix.rstrip("/") + "/"
    for path in git_lines("ls-tree", "-r", "--name-only", ref, "--", source_prefix):
        if not path.startswith(prefix):
            continue
        relative = path[len(prefix):]
        if relative in skipped:
            continue
        destination = target / relative
        if destination.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(git_blob(ref, path))
        copied += 1
    return copied


def validate_legacy_shape(ref: str) -> None:
    local_learning = REPO_ROOT / "learning"
    if local_learning.exists():
        unknown = {p.name for p in local_learning.iterdir()} - LEGACY_LEARNING_ROOTS
        if unknown:
            raise SystemExit("unsupported local legacy learning assets: " + ", ".join(sorted(unknown)))
    tracked = git_lines("ls-tree", "-d", "--name-only", f"{ref}:learning")
    unknown = {Path(path).name for path in tracked} - LEGACY_LEARNING_ROOTS
    if unknown:
        raise SystemExit("unsupported tracked legacy learning assets: " + ", ".join(sorted(unknown)))


def migrate_legacy(root: Path, layout: dict[str, Path], ref: str) -> int:
    copied = 0
    local_state = REPO_ROOT / ".learn-agent/progress/current.md"
    copied += copy_missing(local_state, layout["state.current"])

    local = REPO_ROOT / "learning"
    copied += copy_missing(local / "notes/index.md", layout["notes.index"])
    copied += copy_missing(local / "notes", layout["notes.root"], skip={"index.md"})
    copied += copy_missing(local / "qa", qa_root(layout))
    copied += copy_missing(local / "bug-book/bug-book.md", layout["bugs.book"])
    copied += copy_missing(local / "progress/code-ability.md", layout["progress.code_ability"])
    copied += copy_missing(local / "progress/history.md", layout["progress.code_ability"].parent / "history.md")
    copied += copy_missing(local / "project", layout["project.root"])
    copied += copy_missing(local / "adr", layout["adr.root"])

    copied += git_copy_missing(ref, "learning/notes", layout["notes.root"], skip={"index.md"})
    for source, target in (
        ("learning/notes/index.md", layout["notes.index"]),
        ("learning/bug-book/bug-book.md", layout["bugs.book"]),
        ("learning/progress/code-ability.md", layout["progress.code_ability"]),
        ("learning/progress/history.md", layout["progress.code_ability"].parent / "history.md"),
    ):
        if not target.exists():
            paths = git_lines("ls-tree", "-r", "--name-only", ref, "--", source)
            if paths:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(git_blob(ref, source))
                copied += 1
    copied += git_copy_missing(ref, "learning/qa", qa_root(layout))
    copied += git_copy_missing(ref, "learning/project", layout["project.root"])
    copied += git_copy_missing(ref, "learning/adr", layout["adr.root"])

    workspace = child(root, root, Path("workspace"))
    copied += copy_missing(REPO_ROOT / "work", workspace)
    copied += git_copy_missing(ref, "work", workspace)
    return copied


def seed_missing(root: Path, layout: dict[str, Path]) -> int:
    copied = 0
    copied += copy_missing(REPO_ROOT / "seed/state/current.md", layout["state.current"])
    copied += copy_missing(REPO_ROOT / "seed/notes/index.md", layout["notes.index"])
    copied += copy_missing(REPO_ROOT / "seed/notes/template.md", layout["notes.root"] / "template.md")
    copied += copy_missing(REPO_ROOT / "seed/notes/stage-01", layout["notes.root"] / "stage-01")
    copied += copy_missing(REPO_ROOT / "seed/notes/qa", qa_root(layout))
    copied += copy_missing(REPO_ROOT / "seed/notes/bug-book.md", layout["bugs.book"])
    copied += copy_missing(REPO_ROOT / "seed/progress/code-ability.md", layout["progress.code_ability"])
    copied += copy_missing(REPO_ROOT / "seed/progress/history.md", layout["progress.code_ability"].parent / "history.md")
    copied += copy_missing(REPO_ROOT / "seed/project/adr", layout["adr.root"])
    for name in ("milestones.md", "project-track.md", "target-architecture.md"):
        copied += copy_missing(REPO_ROOT / "seed/project" / name, layout["project.root"] / name)
    return copied


def rollback_orphan_note_route(layout: dict[str, Path]) -> bool:
    path = layout["notes.index"]
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


def rollback_orphan_state_route(layout: dict[str, Path]) -> bool:
    path = layout["state.current"]
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    old = f"next_chapter: {ORPHAN_CHAPTER}"
    if old not in text:
        return False
    path.write_text(text.replace(old, f"next_chapter: {NEXT_CANONICAL_CHAPTER}"), encoding="utf-8")
    return True


def rollback_orphan_transaction(root: Path) -> bool:
    path = root / "workspace/stage01-ch06-curriculum-migration.json"
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    state_updates = data.get("state_updates")
    if not isinstance(state_updates, dict) or state_updates.get("next_chapter") != ORPHAN_CHAPTER:
        return False
    state_updates["next_chapter"] = NEXT_CANONICAL_CHAPTER
    state_updates["last_checkpoint_reason"] = "curriculum_migration_rollback"
    if "last_note_update" in state_updates:
        state_updates["last_note_update"] = "Stage 01 Chapter 06 未完成迁移已回滚；Chapter 05 后继路由恢复为 Stage 02 / Chapter 01"
    data["status"] = "rolled_back"
    data["rollback_reason"] = "canonical Stage 01 Chapter 06 was never created"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def write_manifest(root: Path) -> None:
    manifest = root / MANIFEST_REL
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        f"""version: 2
backend: local_workspace
backend_root: {json.dumps(str(root), ensure_ascii=False)}
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
    root = validate_runtime_root(args.runtime_root)
    layout, manifest_existed = load_layout(root)  # validate existing manifest before writes

    if args.migrate_legacy:
        validate_legacy_shape(args.legacy_ref)  # validate legacy shape before writes
        migrated = migrate_legacy(root, layout, args.legacy_ref)
    else:
        migrated = 0

    seeded = seed_missing(root, layout)
    rollback_count = sum((
        rollback_orphan_note_route(layout),
        rollback_orphan_state_route(layout),
        rollback_orphan_transaction(root),
    ))
    if not manifest_existed:
        write_manifest(root)

    print(f"runtime_root={root}")
    print(f"legacy_files_copied={migrated}")
    print(f"seed_files_copied={seeded}")
    print(f"orphan_routes_rolled_back={rollback_count}")
    print("manifest=.learn-agent/storage-manifest.yaml")


if __name__ == "__main__":
    main()
