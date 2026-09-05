#!/usr/bin/env python3
"""Validate learn-agent protocol invariants beyond generic skill frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
RUNTIME_DIRS = {".learn-agent", "learning", "work", "workspace"}


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


skill = read(ROOT / "SKILL.md")
if len(skill.splitlines()) > 220:
    fail("SKILL.md exceeds 220 lines; move conditional detail to shared references")

for stale in (ROOT / "README.md", ROOT / "FILE_TREE.txt"):
    if stale.exists():
        fail(f"duplicated path catalog must not exist: {stale.name}")

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

seed = read(ROOT / "seed" / "state" / "current.md")
for token in (
    "schema_version: 2",
    "lifecycle_status:",
    "learning_status:",
    "integrity:",
    "mastery:",
    "pending_writeback: null",
):
    if token not in seed:
        fail(f"state seed missing {token!r}")

template = read(ROOT / "seed" / "notes" / "template.md")
for token in ("schema_version", "lifecycle_status", "learning_status"):
    if token not in template:
        fail(f"note template missing {token}")

chapters = sorted(
    path
    for path in (ROOT / "curriculum").glob("stage-*/*.md")
    if path.name != "README.md"
)
if not chapters:
    fail("no curriculum chapters found")

chapter_ids: set[str] = set()
for path in chapters:
    text = read(path)
    relative = path.relative_to(ROOT)
    if "## 验收契约" not in text:
        fail(f"missing acceptance contract: {relative}")
        continue
    match = re.search(r"(?m)^chapter_id:\s*(\S+)\s*$", text)
    if not match:
        fail(f"missing chapter_id: {relative}")
    elif match.group(1) in chapter_ids:
        fail(f"duplicate chapter_id {match.group(1)}: {relative}")
    else:
        chapter_ids.add(match.group(1))
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
        if token not in text:
            fail(f"chapter contract missing {token!r}: {relative}")

if ERRORS:
    for error in ERRORS:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"OK: protocol invariants validated for {len(chapters)} chapters")
