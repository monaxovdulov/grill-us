# Third-party notices and prior art

## Matt Pocock — `grilling`

Grill Us adapts the design-tree, frontier, round, recommendation, and completion ideas from [`mattpocock/skills`](https://github.com/mattpocock/skills), particularly [`skills/productivity/grilling`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling).

The upstream repository is distributed under the MIT License:

> Copyright (c) 2026 Matt Pocock

Its license text is available at [`mattpocock/skills/LICENSE`](https://github.com/mattpocock/skills/blob/main/LICENSE).

The Grill Us protocol adds an incremental participant roster, stable speaker provenance, knowledge- and authority-based question routing, explicit disagreement handling, multilingual terminology, turn mode, room mode, and group confirmation.

## Skill authoring references

The 0.5.0 authoring and eval pass consulted these public projects:

- Matt Pocock's [`writing-for-agents`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) for context pointers, completion criteria, and instruction pruning.
- smixs' [`skill-conductor`](https://github.com/smixs/skill-conductor) for no-guidance controls, atomic eval assertions, and pressure testing.
- smixs' [`pohuy`](https://github.com/smixs/pohuy) and [`humanizer-ru`](https://github.com/smixs/humanizer-ru) as examples of native Russian semantic calibration and preservation rules.
- smixs' [`awesome-claude-output-styles`](https://github.com/smixs/awesome-claude-output-styles) for separating presentation from task invariants.

Grill Us does not bundle their style corpora, scripts, or output-style definitions.

## Matt Pocock — `domain-modeling`

The optional Shared Language recipe composes Grill Us with Matt Pocock's [`domain-modeling`](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) skill. The recipe keeps Grill Us in control of multi-participant pacing, provenance, authority, and intervention while `domain-modeling` supplies terminology checks and `CONTEXT.md` formatting. It explicitly does not load Matt Pocock's single-user `grilling` skill.

## Other public uses of pair grilling

- Kimura Kei described a local `/grill-us` skill for Jira refinement with two or three developers in [「要件定義の手戻りをAIで防ぐ」](https://zenn.dev/kimuchan/articles/bc8e98682f8594).
- Jo Van Eyck described collaborative human-agent interrogation in [“Pair grilling is the new pair programming”](https://jvaneyck.wordpress.com/2026/07/27/pair-grilling-is-the-new-pair-programming/).

These references are listed to make the lineage and adjacent ideas clear. This project makes no priority claim over the phrase “grill us” or the general practice of pair grilling.
