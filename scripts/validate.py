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
    "VERSION",
    "README.md",
    "README.ru.md",
    "LICENSE.md",
    "plugin.json",
    "THIRD_PARTY_NOTICES.md",
    "skills/grill-us/SKILL.md",
    "skills/grill-us/agents/openai.yaml",
    "skills/grill-us/references/room-mode.md",
    "skills/grill-us/references/russian-pragmatics.md",
    "skills/grill-us/references/turn-mode.md",
    "docs/skill.ru.md",
    "docs/hermes-telegram.md",
    "docs/hermes-telegram.ru.md",
    "docs/openclaw-telegram.md",
    "docs/openclaw-telegram.ru.md",
    "examples/mixed-expertise-pair.md",
    "examples/mixed-expertise-pair.ru.md",
    "evals/README.md",
    "evals/README.ru.md",
    "evals/cases.yaml",
    "recipes/README.md",
    "recipes/README.ru.md",
    "recipes/grill-us-pohuy.ru.md",
    "recipes/quiet-record.md",
    "recipes/quiet-record.ru.md",
    "recipes/shared-language.md",
    "recipes/shared-language.ru.md",
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

    version_file = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version_file):
        fail("VERSION must contain one semantic version")
    if version_file != manifest.get("version"):
        fail("VERSION must match plugin.json")

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

    manifest = json.loads(PLUGIN.read_text(encoding="utf-8"))
    protocol_version = re.search(r"^Protocol version: \*\*(\d+\.\d+\.\d+)\*\*\.$", text, re.MULTILINE)
    if not protocol_version:
        fail("SKILL.md must expose its protocol version")
    if protocol_version.group(1) != manifest.get("version"):
        fail("SKILL.md protocol version must match plugin.json")
    if f"Grill Us v{protocol_version.group(1)}" not in text:
        fail("SKILL.md must show the loaded protocol version in its first-reply template")
    if "claim-scoped" not in text or "decision-scoped" not in text:
        fail("SKILL.md must scope knowledge to claims and authority to decisions")
    if "Do not configure, emulate, or claim durable memory" not in text:
        fail("SKILL.md must preserve the host-owned memory boundary")

    if len(text.splitlines()) > 190:
        fail("SKILL.md exceeded the 190-line progressive-disclosure budget")

    for reference in (
        "references/room-mode.md",
        "references/turn-mode.md",
        "references/russian-pragmatics.md",
    ):
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
    manifest = json.loads(PLUGIN.read_text(encoding="utf-8"))
    version = manifest["version"]
    if "README.ru.md" not in english or "README.md" not in russian:
        fail("README language switch is incomplete")
    reader_translation = (ROOT / "docs/skill.ru.md").read_text(encoding="utf-8")
    if "канонической версией" not in reader_translation:
        fail("Russian reader translation must identify the canonical executable skill")
    if f"версии {version}" not in reader_translation:
        fail("Russian reader translation must identify the current protocol version")
    if "russian-pragmatics.md" not in english or "russian-pragmatics.md" not in russian:
        fail("both READMEs must link the executable Russian pragmatics reference")
    if "recipes/README.md" not in english or "recipes/README.ru.md" not in russian:
        fail("both READMEs must expose the recipe mechanism")

    russian_labels = (ROOT / "skills/grill-us/references/russian-pragmatics.md").read_text(
        encoding="utf-8"
    )
    for fragment in (
        "только записывать",
        "уточнять вопросами",
        "Предложение от агента",
        "ждёт решения",
        "Какая часть разговора учтена",
    ):
        if fragment not in russian_labels:
            fail(f"Russian labels reference is missing: {fragment}")


def check_recipes() -> None:
    required_by_recipe = {
        "recipes/grill-us-pohuy.ru.md": (
            "npx skills add monaxovdulov/grill-us --skill grill-us",
            "npx skills add smixs/pohuy",
            "name: grill-us",
            "name: pohuy",
            "явное согласие каждого присутствующего участника",
            "В Record и Grill удаляйте оценки и рекомендации агента",
            "Статус: ждёт решения",
        ),
        "recipes/quiet-record.md": (
            "Minimum Grill Us version: `0.6.0`",
            "npx skills add monaxovdulov/grill-us --skill grill-us",
            "The host owns storage, retention, retrieval, and access control",
            "Unknown whether the beginning is available",
        ),
        "recipes/quiet-record.ru.md": (
            "Минимальная версия Grill Us: `0.6.0`",
            "какая часть разговора учтена",
            "неизвестно, доступно ли начало разговора",
        ),
        "recipes/shared-language.md": (
            "npx skills add mattpocock/skills --skill domain-modeling",
            "Do not load Matt Pocock's `grilling`",
            "proposed",
            "agreed",
            "contested",
        ),
        "recipes/shared-language.ru.md": (
            "npx skills add mattpocock/skills --skill domain-modeling",
            "Не загружайте `grilling` Мэта Покока",
            "значение не согласовано",
        ),
    }
    for recipe_path, fragments in required_by_recipe.items():
        recipe = (ROOT / recipe_path).read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in recipe:
                fail(f"{recipe_path} is missing required instruction: {fragment}")

    recipe_links = {
        "README.md": (
            "recipes/quiet-record.md",
            "recipes/shared-language.md",
            "recipes/grill-us-pohuy.ru.md",
        ),
        "README.ru.md": (
            "recipes/quiet-record.ru.md",
            "recipes/shared-language.ru.md",
            "recipes/grill-us-pohuy.ru.md",
        ),
        "recipes/README.md": (
            "quiet-record.md",
            "shared-language.md",
            "grill-us-pohuy.ru.md",
        ),
        "recipes/README.ru.md": (
            "quiet-record.ru.md",
            "shared-language.ru.md",
            "grill-us-pohuy.ru.md",
        ),
    }
    for source_path, links in recipe_links.items():
        source = (ROOT / source_path).read_text(encoding="utf-8")
        for link in links:
            if link not in source:
                fail(f"{source_path} must link recipe: {link}")


def check_evals() -> None:
    text = (ROOT / "evals/cases.yaml").read_text(encoding="utf-8")
    case_ids = re.findall(r"^\s{2}- id: ([a-z0-9-]+)$", text, flags=re.MULTILINE)
    if not text.startswith("version: 2\n"):
        fail("eval suite must use schema version 2")
    if len(case_ids) < 20:
        fail("eval suite must contain at least twenty cases")
    if len(case_ids) != len(set(case_ids)):
        fail("eval case IDs must be unique")
    if text.count("critical: true") < 15:
        fail("eval suite must retain at least fifteen critical cases")
    if text.count("pressure:") < 2:
        fail("eval suite must retain at least two pressure cases")
    required_cases = {
        "openclaw-room-provenance",
        "default-grill-no-setup",
        "record-mode-no-steering",
        "infer-record-natural-language",
        "grill-mode-neutral-sequential",
        "advise-proposal-is-not-decision",
        "infer-advise-natural-language",
        "intervention-conflict-lowest",
        "progressive-roster-no-batch",
        "russian-non-objection",
        "russian-we-decided",
        "composition-preserves-semantics",
        "compact-state-delta",
        "pressure-authority-false-consensus",
        "pressure-product-owner-cannot-raise-intervention",
        "claim-scoped-firsthand",
        "decision-scoped-authority",
        "human-proposal-awaits-owner",
        "russian-clear-status-labels",
        "quiet-record-host-boundary",
        "shared-language-contested",
        "save-record-without-storage",
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
    check_recipes()
    check_evals()
    check_license()
    check_placeholders()
    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    print(f"OK: grill-us repository is valid ({markdown_count} Markdown files checked)")


if __name__ == "__main__":
    main()
