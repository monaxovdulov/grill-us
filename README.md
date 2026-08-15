<p align="center">
  <img src="assets/hero.webp" alt="Grill Us — an attributed product interview for several humans" width="100%" />
</p>

<p align="center">
  <strong>English</strong> · <a href="README.ru.md">Русский</a>
</p>

An attributed product interview for pairs and small groups.

Grill Us helps several people work out what to build and why. The agent keeps track of who observed what, who can decide what, where the group disagrees, and which evidence would settle the next decision.

[![Install with skills.sh](https://img.shields.io/badge/skills.sh-install-111111?style=flat-square)](#install)
[![Agent Plugins 1.0.0](https://img.shields.io/badge/Agent_Plugins-1.0.0-6f42c1?style=flat-square)](https://agent-plugins.org/)
[![Validate](https://img.shields.io/github/actions/workflow/status/monaxovdulov/grill-us/validate.yml?branch=main&style=flat-square&label=validate)](https://github.com/monaxovdulov/grill-us/actions/workflows/validate.yml)
[![MIT-style + Beer Clause](https://img.shields.io/badge/license-MIT--style%20%2B%20Beer%20Clause-2f6feb?style=flat-square)](LICENSE.md)

## How it works

In a product conversation, the domain expert may know the problem, the builder may know the constraints, and both may use “we” before they have actually agreed.

Grill Us treats each participant as a separate source. It maintains speaker provenance and decision ownership throughout the interview, whether two people share one terminal or a messaging harness supplies stable sender identity.

## Install

```bash
npx skills add monaxovdulov/grill-us --skill grill-us
```

Or copy [`skills/grill-us`](skills/grill-us) into your agent's skills directory.

The repository root is also an [Agent Plugins 1.0.0](https://agent-plugins.org/specification) package. A skills-capable client can read [`plugin.json`](plugin.json) and discover the same skill under `skills/`. Grill Us does not bundle an MCP server, so `mcp.json` is intentionally absent. The package has one workflow, defined by `skills/grill-us/SKILL.md`.

## Start a session

```text
Use $grill-us.

Mira — runs a language school and knows the current workflow.
Dima — can build the product and owns technical constraints.
Goal — decide whether a parent progress digest is worth testing.
Mode — we share this terminal and will prefix every answer with our name.
```

The agent will establish the roster, route questions by knowledge and authority, preserve disagreements, and return an attributed decision record.

## Two conversation modes

| Mode | Identity source | Best fit |
| --- | --- | --- |
| Turn mode | `Name:` prefixes or announced handoff | One account, terminal, device, or microphone |
| Room mode | Stable sender IDs from the harness | Telegram groups, forum topics, Slack or Discord rooms |

Room mode accepts replies in any order. It requires shared conversation state; per-user session isolation prevents the agent from seeing the whole discussion.

## The protocol

1. Register participants, firsthand knowledge, and decision authority.
2. Build an attributed design tree from the desired outcome.
3. Ask each unresolved question to the person best placed to answer it.
4. Keep disagreement visible until an owner decides, a criterion resolves it, or an experiment is defined.
5. Finish with decisions, owners, evidence, unknowns, and confirmation from each participant.

The executable protocol lives in [`skills/grill-us/SKILL.md`](skills/grill-us/SKILL.md). A reader-friendly Russian translation is available in [`docs/skill.ru.md`](docs/skill.ru.md).

## Hermes + Telegram

Hermes can expose stable Telegram sender identity and maintain a shared room session. The integration guide covers privacy mode, allowlists, shared-session settings, ambient messages, and a per-channel prompt:

- [Hermes + Telegram setup](docs/hermes-telegram.md)
- [Настройка Hermes + Telegram](docs/hermes-telegram.ru.md)

## Test cases

The repository includes small behavioral evals for speaker mixing, false consensus, decision routing, turn-mode attribution, and bilingual terminology. See [`evals/README.md`](evals/README.md).

## Prior art

The design-tree and frontier mechanics are adapted from Matt Pocock's [`grilling`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) skill. The name and broader pair-grilling idea have appeared independently in a [Jira refinement workflow](https://zenn.dev/kimuchan/articles/bc8e98682f8594) and in Jo Van Eyck's essay [“Pair grilling is the new pair programming”](https://jvaneyck.wordpress.com/2026/07/27/pair-grilling-is-the-new-pair-programming/).

This repository develops the protocol around mixed-expertise groups, stable speaker provenance, decision ownership, multilingual discussion, and messaging-harness room mode. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for attribution.

## Contributing

Field notes are especially useful: who was in the room, which mode you used, where attribution failed, and whether the final record matched the group's actual decisions. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request.

## License

[MIT-style + Beer Clause](LICENSE.md)
