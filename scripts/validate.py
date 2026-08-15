#!/usr/bin/env python3
"""Validate the portable Grill Us skill and repository links using stdlib only."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "grill-us" / "SKILL.md"

REQUIRED = (
    "README.md",
    "README.ru.md",
    "LICENSE.md",
    "THIRD_PARTY_NOTICES.md",
    "skills/grill-us/SKILL.md",
    "skills/grill-us/agents/openai.yaml",
    "skills/grill-us/references/room-mode.md",
    "skills/grill-us/references/turn-mode.md",
    "docs/skill.ru.md",
    "docs/hermes-telegram.md",
    "docs/hermes-telegram.ru.md",
    "examples/mixed-expertise-pair.md",
    "examples/mixed-expertise-pair.ru.md",
    "evals/cases.yaml",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def check_skill() -> None:
    text = SKILL.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        fail("SKILL.md must begin with YAML frontmatter")

    keys = []
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            fail(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        keys.append(key.strip())
        values[key.strip()] = value.strip()

    if keys != ["name", "description"]:
        fail("portable skill frontmatter must contain only name and description")
    if values["name"] != "grill-us":
        fail("skill name must be grill-us")
    if len(values["description"]) < 80:
        fail("skill description must include useful trigger context")
    if len(text.splitlines()) > 190:
        fail("SKILL.md exceeded the 190-line progressive-disclosure budget")

    for reference in ("references/room-mode.md", "references/turn-mode.md"):
        if f"]({reference})" not in text:
            fail(f"SKILL.md does not link to {reference}")

    agent_yaml = (ROOT / "skills/grill-us/agents/openai.yaml").read_text(encoding="utf-8")
    if "$grill-us" not in agent_yaml:
        fail("agents/openai.yaml default prompt must mention $grill-us")


def check_markdown_links() -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for source in ROOT.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split(" ", 1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            path_part = unquote(target.split("#", 1)[0])
            destination = (source.parent / path_part).resolve()
            try:
                destination.relative_to(ROOT)
            except ValueError:
                fail(f"link escapes repository: {source.relative_to(ROOT)} -> {target}")
            if not destination.exists():
                fail(f"broken link: {source.relative_to(ROOT)} -> {target}")


def check_bilingual_contract() -> None:
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    russian = (ROOT / "README.ru.md").read_text(encoding="utf-8")
    if "README.ru.md" not in english or "README.md" not in russian:
        fail("README language switch is incomplete")
    if "канонической версией" not in (ROOT / "docs/skill.ru.md").read_text(encoding="utf-8"):
        fail("Russian reader translation must identify the canonical executable skill")


def check_evals() -> None:
    text = (ROOT / "evals/cases.yaml").read_text(encoding="utf-8")
    case_ids = re.findall(r"^\s{2}- id: ([a-z0-9-]+)$", text, flags=re.MULTILINE)
    if len(case_ids) < 5:
        fail("eval suite must contain at least five cases")
    if len(case_ids) != len(set(case_ids)):
        fail("eval case IDs must be unique")
    if text.count("critical: true") < 3:
        fail("eval suite must retain at least three critical cases")


def check_placeholders() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path == Path(__file__):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if re.search(r"\b(?:TODO|FIXME)\b", text):
            fail(f"placeholder found in {path.relative_to(ROOT)}")


def main() -> None:
    check_required_files()
    check_skill()
    check_markdown_links()
    check_bilingual_contract()
    check_evals()
    check_placeholders()
    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    print(f"OK: grill-us repository is valid ({markdown_count} Markdown files checked)")


if __name__ == "__main__":
    main()
