#!/usr/bin/env python3
"""Validate the portable Grill Us skill and repository links using stdlib only."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "grill-us" / "SKILL.md"
PLUGIN = ROOT / "plugin.json"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"

REQUIRED = (
    "README.md",
    "README.ru.md",
    "LICENSE.md",
    "plugin.json",
    "THIRD_PARTY_NOTICES.md",
    "skills/grill-us/SKILL.md",
    "skills/grill-us/agents/openai.yaml",
    "skills/grill-us/references/room-mode.md",
    "skills/grill-us/references/turn-mode.md",
    "docs/skill.ru.md",
    "docs/hermes-telegram.md",
    "docs/hermes-telegram.ru.md",
    "docs/openclaw-telegram.md",
    "docs/openclaw-telegram.ru.md",
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


def check_plugin_manifest() -> None:
    try:
        manifest = json.loads(PLUGIN.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"plugin.json is not valid JSON: {error}")

    if not isinstance(manifest, dict):
        fail("plugin.json must contain a top-level object")

    allowed = {
        "$schema",
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "extensions",
    }
    unknown = sorted(set(manifest) - allowed)
    if unknown:
        fail("plugin.json contains unknown fields: " + ", ".join(unknown))

    if manifest.get("$schema") != PLUGIN_SCHEMA:
        fail("plugin.json must target Agent Plugins 1.0.0")

    name = manifest.get("name")
    if not isinstance(name, str) or not re.fullmatch(
        r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?", name
    ):
        fail("plugin name violates Agent Plugins 1.0.0 naming constraints")
    if name != "grill-us":
        fail("plugin name must be grill-us")

    string_fields = ("version", "description", "homepage", "repository", "license")
    for field in string_fields:
        if field in manifest and not isinstance(manifest[field], str):
            fail(f"plugin.json field {field!r} must be a string")

    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            fail("plugin.json author must be an object")
        author_unknown = sorted(set(author) - {"name", "email", "url"})
        if author_unknown:
            fail("plugin.json author contains unknown fields: " + ", ".join(author_unknown))
        if not all(isinstance(value, str) for value in author.values()):
            fail("plugin.json author values must be strings")

    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list)
        or not all(isinstance(keyword, str) for keyword in keywords)
    ):
        fail("plugin.json keywords must be an array of strings")

    extensions = manifest.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict)
        or not all(isinstance(value, dict) for value in extensions.values())
    ):
        fail("plugin.json extensions must map namespaces to objects")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    release = re.search(r"^## (\d+\.\d+\.\d+)\b", changelog, flags=re.MULTILINE)
    if not release or manifest.get("version") != release.group(1):
        fail("plugin version must match the current changelog release")

    skills_root = ROOT / "skills"
    discovered = [
        child
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    ]
    if SKILL.parent not in discovered:
        fail("Agent Plugins discovery cannot find skills/grill-us/SKILL.md")

    mcp_path = ROOT / "mcp.json"
    if mcp_path.exists():
        try:
            mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            fail(f"mcp.json is not valid JSON: {error}")
        if not isinstance(mcp, dict) or set(mcp) != {"$schema", "mcpServers"}:
            fail("mcp.json must contain only $schema and mcpServers")
        if mcp["$schema"] != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
            fail("mcp.json must target the same Agent Plugins version as plugin.json")
        if not isinstance(mcp["mcpServers"], dict):
            fail("mcp.json mcpServers must be an object")


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

    expected_keys = ["name", "description", "metadata"]
    if keys != expected_keys:
        fail("skill frontmatter must contain portable metadata in canonical order")
    if values["name"] != "grill-us":
        fail("skill name must be grill-us")
    if len(values["description"]) < 80:
        fail("skill description must include useful trigger context")
    try:
        metadata = json.loads(values["metadata"])
    except json.JSONDecodeError as error:
        fail(f"OpenClaw metadata must be single-line JSON: {error}")
    if metadata.get("openclaw", {}).get("homepage") != "https://github.com/monaxovdulov/grill-us":
        fail("OpenClaw metadata must point to the public repository")
    if len(text.splitlines()) > 190:
        fail("SKILL.md exceeded the 190-line progressive-disclosure budget")

    for reference in ("references/room-mode.md", "references/turn-mode.md"):
        if f"`{{baseDir}}/{reference}`" not in text:
            fail(f"SKILL.md does not use a portable baseDir reference for {reference}")

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
    if len(case_ids) < 10:
        fail("eval suite must contain at least ten cases")
    if len(case_ids) != len(set(case_ids)):
        fail("eval case IDs must be unique")
    if text.count("critical: true") < 7:
        fail("eval suite must retain at least seven critical cases")
    required_cases = {
        "openclaw-room-provenance",
        "setup-style-choice",
        "record-mode-no-steering",
        "grill-mode-neutral-sequential",
        "advise-proposal-is-not-decision",
    }
    missing = sorted(required_cases - set(case_ids))
    if missing:
        fail("eval suite is missing required cases: " + ", ".join(missing))


def check_license() -> None:
    manifest = json.loads(PLUGIN.read_text(encoding="utf-8"))
    license_text = (ROOT / "LICENSE.md").read_text(encoding="utf-8")
    if manifest.get("license") != "MIT-0":
        fail("plugin manifest must use the MIT-0 SPDX identifier")
    if not license_text.startswith("MIT No Attribution\n"):
        fail("LICENSE.md must contain the MIT-0 license")
    if "beer" in license_text.lower():
        fail("legacy Beer Clause remains in LICENSE.md")


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
    check_plugin_manifest()
    check_skill()
    check_markdown_links()
    check_bilingual_contract()
    check_evals()
    check_license()
    check_placeholders()
    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    print(f"OK: grill-us repository is valid ({markdown_count} Markdown files checked)")


if __name__ == "__main__":
    main()
