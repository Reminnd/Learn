#!/usr/bin/env python3
"""Validate learn-agent protocol invariants beyond generic skill frontmatter."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
RUNTIME_DIRS = {".learn-agent", "learning", "work", "workspace"}
TRACKED_RUNTIME_PREFIXES = (
    ".learn-agent/",
    "learning/",
    "work/",
    "workspace/",
    "notes/",
    "progress/",
    "project/",
)
REQUIRED_RUNTIME_IGNORES = {".learn-agent/", "learning/", "work/", "workspace/"}
README_TARGETS = (
    "environment/framework-baseline.md",
    "environment/requirements-stage-01.txt",
    "scripts/preflight.py",
    "examples/stage-01/ex1_message_prompt_langchain.py",
    "curriculum/stage-01/01-llm-message-prompt-langchain.md",
    "curriculum/index.md",
    "scripts/setup_runtime.py",
)


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_section(text: str, heading: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(heading)}\s*$", text)
    if not match:
        return None
    rest = text[match.end():]
    next_heading = re.search(r"(?m)^##\s+", rest)
    return rest[:next_heading.start()] if next_heading else rest


def top_level_block(text: str, key: str, next_key: str | None = None) -> str | None:
    if next_key is None:
        pattern = rf"(?ms)^{re.escape(key)}:\s*\n(?P<body>.*)\Z"
    else:
        pattern = (
            rf"(?ms)^{re.escape(key)}:\s*\n"
            rf"(?P<body>.*?)(?=^{re.escape(next_key)}:\s*$)"
        )
    match = re.search(pattern, text)
    return match.group("body") if match else None


def inline_list(text: str, key: str, *, indent: int = 0) -> list[str] | None:
    prefix = " " * indent
    match = re.search(
        rf"(?m)^{re.escape(prefix + key)}:\s*\[(?P<body>[^\]]*)\]\s*$",
        text,
    )
    if not match:
        return None
    body = match.group("body").strip()
    if not body:
        return []
    return [
        item.strip().strip("\"'")
        for item in body.split(",")
        if item.strip()
    ]


def prerequisites_list(text: str) -> list[str] | None:
    inline = inline_list(text, "prerequisites")
    if inline is not None:
        return inline
    block = top_level_block(text, "prerequisites", "required_exercises")
    if block is None:
        return None
    return [
        item.strip().strip("\"'")
        for item in re.findall(r"(?m)^  -\s*(\S+)\s*$", block)
    ]


def scalar_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(\S+)\s*$", text)
    return match.group(1) if match else None


def list_item_ids(block: str) -> list[str]:
    return re.findall(r"(?m)^  - id:\s*(\S+)\s*$", block)


def question_critical_ids(block: str, relative: Path) -> tuple[list[str], set[str]]:
    matches = list(re.finditer(r"(?m)^  - id:\s*(\S+)\s*$", block))
    ids = [match.group(1) for match in matches]
    critical_ids: set[str] = set()
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        item = block[match.end():end]
        critical = re.search(r"(?m)^    critical:\s*(true|false)\s*$", item)
        if not critical:
            fail(f"question {match.group(1)} missing critical flag: {relative}")
        elif critical.group(1) == "true":
            critical_ids.add(match.group(1))
    return ids, critical_ids


def safe_pointer(base: Path, raw: str, label: str) -> Path | None:
    relative = Path(raw)
    if relative.is_absolute():
        fail(f"{label} must be relative: {raw}")
        return None
    root = base.resolve()
    target = (base / relative).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        fail(f"{label} escapes {base.relative_to(ROOT)}: {raw}")
        return None
    return target


def git_tracked_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        fail(f"cannot read tracked distribution files with git ls-files: {exc}")
        return []
    return [line for line in result.stdout.splitlines() if line]


skill = read(ROOT / "SKILL.md")
if len(skill.splitlines()) > 220:
    fail("SKILL.md exceeds 220 lines; move conditional detail to shared references")

stale = ROOT / "FILE_TREE.txt"
if stale.exists():
    fail(f"duplicated path catalog must not exist: {stale.name}")

readme_path = ROOT / "README.md"
if not readme_path.is_file():
    fail("root README.md is missing")
    readme_text = ""
else:
    readme_text = read(readme_path)

readme_links = set(re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", readme_text))
for target in README_TARGETS:
    if target not in readme_links:
        fail(f"README.md missing canonical link: {target}")
    if not (ROOT / target).is_file():
        fail(f"README.md canonical link target missing: {target}")

banned_paths = (
    "notes/bug-book.md",
    "progress/code-ability.md",
    "project/adr/",
    "`progress/current.md`",
)
allowed_path_examples = {ROOT / "shared" / "storage-adapters.md"}
for path in ROOT.rglob("*.md"):
    if path.relative_to(ROOT).parts[0] in RUNTIME_DIRS:
        continue
    if path in allowed_path_examples:
        continue
    text = read(path)
    for banned in banned_paths:
        if banned in text:
            fail(f"hard-coded runtime path {banned!r} in {path.relative_to(ROOT)}")

for path in ROOT.rglob("*.md"):
    relative = path.relative_to(ROOT).as_posix()
    if path.relative_to(ROOT).parts[0] in RUNTIME_DIRS:
        continue
    text = read(path)
    if "notes_status" in text and relative not in {
        "SKILL.md",
        "shared/learning-state-machine.md",
        "shared/session-persistence.md",
    }:
        fail(f"legacy notes_status outside migration documentation: {relative}")

seed_path = ROOT / "seed" / "state" / "current.md"
seed = read(seed_path)
for token in (
    "schema_version: 2",
    "lifecycle_status:",
    "learning_status:",
    "integrity:",
    "mastery:",
    "pending_writeback: null",
    "provider_route_prompted_for:",
    "last_provider_route_decision:",
):
    if token not in seed:
        fail(f"state seed missing {token!r}")
for legacy in ("deepseek_route_prompted_for", "last_deepseek_route_decision"):
    if legacy in seed:
        fail(f"state seed contains legacy provider route metadata: {legacy}")

template = read(ROOT / "seed" / "notes" / "template.md")
for token in ("schema_version", "lifecycle_status", "learning_status"):
    if token not in template:
        fail(f"note template missing {token}")

curriculum = ROOT / "curriculum"
stages = sorted(path for path in curriculum.glob("stage-*") if path.is_dir())
chapters = sorted(
    path
    for path in curriculum.glob("stage-*/*.md")
    if path.name != "README.md"
)
if not chapters:
    fail("no curriculum chapters found")

canonical_chapters = {path.relative_to(ROOT).as_posix() for path in chapters}
index_text = read(curriculum / "index.md")
index_refs = re.findall(r"`(stage-\d{2}/[^`\n]+\.md)`", index_text)
index_paths = [f"curriculum/{ref}" for ref in index_refs]
if len(index_paths) != len(set(index_paths)):
    fail("curriculum/index.md contains duplicate chapter references")
index_set = set(index_paths)
for missing in sorted(canonical_chapters - index_set):
    fail(f"canonical chapter missing from curriculum/index.md: {missing}")
for stale in sorted(index_set - canonical_chapters):
    fail(f"curriculum/index.md references missing canonical chapter: {stale}")

expected_tracks = {
    "Core Path": [f"stage-{number:02d}" for number in range(1, 10)],
    "Advanced Track": [f"stage-{number:02d}" for number in range(10, 15)],
}
track_stages: dict[str, list[str]] = {}
for track, expected in expected_tracks.items():
    section = markdown_section(index_text, f"## {track}")
    if section is None:
        fail(f"curriculum/index.md missing {track} section")
        refs: list[str] = []
    else:
        refs = re.findall(
            r"(?m)^###\s+\[Stage\s+\d{2}[^\]]*\]\((stage-\d{2})/README\.md\)\s*$",
            section,
        )
    track_stages[track] = refs
    if len(refs) != len(set(refs)):
        fail(f"curriculum/index.md contains duplicate {track} stages")
    if refs != expected:
        fail(f"curriculum/index.md {track} stages must be ordered {expected}")

core_stages = track_stages["Core Path"]
advanced_stages = track_stages["Advanced Track"]
if set(core_stages) & set(advanced_stages):
    fail("curriculum/index.md Core Path and Advanced Track overlap")

canonical_stages = [stage.name for stage in stages]
track_stage_set = set(core_stages + advanced_stages)
if track_stage_set != set(canonical_stages):
    fail("curriculum/index.md track membership is not complete for canonical stages")

core_count = sum(path.parent.name in set(core_stages) for path in chapters)
advanced_count = sum(path.parent.name in set(advanced_stages) for path in chapters)
if core_count != 29:
    fail(f"Core Path must contain 29 canonical chapters, found {core_count}")
if advanced_count != 11:
    fail(f"Advanced Track must contain 11 canonical chapters, found {advanced_count}")
if len(chapters) != 40:
    fail(f"curriculum must contain 40 canonical chapters, found {len(chapters)}")

for stage in stages:
    actual_order = [
        path.name
        for path in sorted(stage.glob("*.md"))
        if path.name != "README.md"
    ]
    actual = set(actual_order)
    readme = stage / "README.md"
    if not readme.is_file():
        fail(f"stage README missing: {readme.relative_to(ROOT)}")
        continue
    readme_content = read(readme)
    expected_track = "Core Path" if stage.name in expected_tracks["Core Path"] else "Advanced Track"
    if not re.search(
        rf"(?m)^\*\*Track:\*\*\s+{re.escape(expected_track)}\s*$",
        readme_content,
    ):
        fail(f"stage README has incorrect track label: {readme.relative_to(ROOT)}")
    if not re.search(r"\[[^\]\n]+\]\(\.\./index\.md\)", readme_content):
        fail(f"stage README missing curriculum index backlink: {readme.relative_to(ROOT)}")

    section = markdown_section(readme_content, "## 本阶段章节")
    if section is None:
        fail(f"stage README missing chapter section: {readme.relative_to(ROOT)}")
        continue
    refs = re.findall(r"\[[^\]\n]+\]\(([^)\n]+\.md)\)", section)
    if len(refs) != len(set(refs)):
        fail(f"stage README contains duplicate chapter references: {readme.relative_to(ROOT)}")
    referenced = set(refs)
    for missing in sorted(actual - referenced):
        fail(f"stage README missing chapter {missing}: {readme.relative_to(ROOT)}")
    for stale in sorted(referenced - actual):
        fail(f"stage README references missing chapter {stale}: {readme.relative_to(ROOT)}")
    if refs != actual_order:
        fail(f"stage README chapter links are not in canonical order: {readme.relative_to(ROOT)}")

learner_routing_paths = [
    ROOT / "SKILL.md",
    readme_path,
    curriculum / "index.md",
    *(stage / "README.md" for stage in stages),
]
for path in learner_routing_paths:
    if not path.is_file():
        continue
    text = read(path)
    for legacy in ("deepseek_route_prompted_for", "last_deepseek_route_decision"):
        if legacy in text:
            fail(f"learner routing uses legacy provider route metadata {legacy}: {path.relative_to(ROOT)}")

context_budget = read(ROOT / "shared" / "context-budget.md")
if "Claude Code + DeepSeek" in context_budget:
    fail("context budget contains a provider-specific Claude Code + DeepSeek route condition")
if "provider/harness route" not in context_budget:
    fail("context budget missing generic provider/harness route evaluation semantics")

chapter_ids: dict[str, Path] = {}
chapter_records: list[tuple[Path, list[str]]] = []
for path in chapters:
    text = read(path)
    relative = path.relative_to(ROOT)
    if "## 验收契约" not in text:
        fail(f"missing acceptance contract: {relative}")
        continue
    contract = text.split("## 验收契约", 1)[1]
    match = re.search(r"(?m)^chapter_id:\s*(\S+)\s*$", contract)
    if not match:
        fail(f"missing chapter_id: {relative}")
        continue
    chapter_id = match.group(1)
    if chapter_id in chapter_ids:
        fail(
            f"duplicate chapter_id {chapter_id}: "
            f"{chapter_ids[chapter_id].relative_to(ROOT)} and {relative}"
        )
    else:
        chapter_ids[chapter_id] = path

    for token in (
        "required_exercises:",
        "questions:",
        "critical: true",
        "acceptance:",
        "threshold: 80",
        "dimension_floor_ratio: 0.60",
        "critical_questions: [Q1, Q2]",
        "required_exercises: [EX1]",
    ):
        if token not in contract:
            fail(f"chapter contract missing {token!r}: {relative}")

    prerequisites = prerequisites_list(contract)
    if prerequisites is None:
        fail(f"cannot parse prerequisites: {relative}")
        prerequisites = []
    chapter_records.append((path, prerequisites))

    exercise_block = top_level_block(contract, "required_exercises", "questions")
    if exercise_block is None:
        fail(f"cannot parse required_exercises: {relative}")
        exercise_ids: list[str] = []
    else:
        exercise_ids = list_item_ids(exercise_block)
        if len(exercise_ids) != len(set(exercise_ids)):
            fail(f"duplicate required exercise id: {relative}")

    questions_block = top_level_block(contract, "questions", "mastery")
    if questions_block is None:
        fail(f"cannot parse questions: {relative}")
        question_ids: list[str] = []
        critical_ids: set[str] = set()
    else:
        question_ids, critical_ids = question_critical_ids(questions_block, relative)
        if len(question_ids) != len(set(question_ids)):
            fail(f"duplicate question id: {relative}")

    mastery_critical = inline_list(contract, "critical_questions", indent=2)
    if mastery_critical is None:
        fail(f"cannot parse mastery.critical_questions: {relative}")
        mastery_critical = []
    mastery_required = inline_list(contract, "required_exercises", indent=2)
    if mastery_required is None:
        fail(f"cannot parse mastery.required_exercises: {relative}")
        mastery_required = []

    unknown_critical = set(mastery_critical) - set(question_ids)
    if unknown_critical:
        fail(
            f"mastery critical_questions reference undeclared questions "
            f"{sorted(unknown_critical)}: {relative}"
        )
    if set(mastery_critical) != critical_ids:
        fail(
            f"mastery critical_questions do not match critical questions: {relative}"
        )

    unknown_required = set(mastery_required) - set(exercise_ids)
    if unknown_required:
        fail(
            f"mastery required_exercises reference undeclared exercises "
            f"{sorted(unknown_required)}: {relative}"
        )
    if set(mastery_required) != set(exercise_ids):
        fail(
            f"mastery required_exercises do not match declared required exercises: {relative}"
        )

known_chapter_ids = set(chapter_ids)
for path, prerequisites in chapter_records:
    missing = set(prerequisites) - known_chapter_ids
    if missing:
        fail(
            f"prerequisites reference missing chapter_id {sorted(missing)}: "
            f"{path.relative_to(ROOT)}"
        )

for key in ("chapter_file", "next_chapter"):
    value = scalar_value(seed, key)
    if value is None:
        fail(f"state seed missing {key}")
        continue
    if value not in canonical_chapters:
        fail(f"state seed {key} is not a canonical chapter: {value}")
    elif value not in index_set:
        fail(f"state seed {key} is missing from curriculum/index.md: {value}")

chapter_file = scalar_value(seed, "chapter_file")
note_pointer = scalar_value(seed, "note_pointer")
if note_pointer is None:
    fail("state seed missing note_pointer")
else:
    note_path = safe_pointer(ROOT / "seed" / "notes", note_pointer, "note_pointer")
    if note_path is not None:
        if not note_path.is_file():
            fail(f"note_pointer target missing: {note_pointer}")
        elif chapter_file is not None:
            note_text = read(note_path)
            note_chapter = re.search(
                r"(?m)^- chapter_file:\s*`([^`]+)`\s*$",
                note_text,
            )
            if not note_chapter:
                fail(f"seed note missing chapter_file metadata: {note_path.relative_to(ROOT)}")
            elif note_chapter.group(1) != chapter_file:
                fail(
                    f"seed note chapter_file does not match state chapter_file: "
                    f"{note_path.relative_to(ROOT)}"
                )

qa_pointer = scalar_value(seed, "qa_pointer")
if qa_pointer is None:
    fail("state seed missing qa_pointer")
else:
    qa_path = safe_pointer(ROOT / "seed" / "notes" / "qa", qa_pointer, "qa_pointer")
    if qa_path is not None and not qa_path.is_file():
        fail(f"qa_pointer target missing: {qa_pointer}")

tracked = git_tracked_files()
for path in tracked:
    if path.startswith(TRACKED_RUNTIME_PREFIXES):
        fail(f"runtime or legacy state path must not be tracked in Skill distribution: {path}")

ignore_lines = {
    line.strip()
    for line in read(ROOT / ".gitignore").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
}
for required in sorted(REQUIRED_RUNTIME_IGNORES - ignore_lines):
    fail(f".gitignore missing runtime boundary entry: {required}")

if ERRORS:
    for error in ERRORS:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"OK: protocol invariants validated for {len(chapters)} chapters")
