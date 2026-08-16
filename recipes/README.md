# Grill Us recipes

A recipe is an agent-facing instruction for composing Grill Us with another skill or host capability. Give the agent the recipe URL or local path and ask it to read and apply the whole file. The agent checks available capabilities, installs missing skills when its environment permits, and follows the stated precedence rules.

## Available recipes

- [Quiet Record](quiet-record.md) — observe a host-supplied discussion, avoid unsolicited replies, and show an attributed record on request.
- [Shared Language](shared-language.md) — combine Grill Us with Matt Pocock's `domain-modeling` discipline to resolve and record project terms.
- [Grill Us + pohuy](grill-us-pohuy.ru.md) — Russian-only composition with idiomatic profanity in the agent's questions and connective text.

Recipes extend the core protocol. They do not grant a host sender identity, ambient-message delivery, writable files, or durable memory that it does not already provide.
