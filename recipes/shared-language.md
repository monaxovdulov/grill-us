# Recipe: Shared Language

Use this recipe when participants use the same term differently or need a small, agreed project glossary. Grill Us controls the multi-human discussion; Matt Pocock's `domain-modeling` controls term sharpening and glossary format.

Minimum Grill Us version: `0.6.0`.

## Instructions for the agent

### 1. Install or verify the skills

For Agent Skills clients, install missing dependencies with:

```bash
npx skills add monaxovdulov/grill-us --skill grill-us
npx skills add mattpocock/skills --skill domain-modeling
```

Read both installed `SKILL.md` files. Verify `name: grill-us`, Grill Us protocol version `0.6.0` or later, and `name: domain-modeling`. Do not load Matt Pocock's `grilling`: Grill Us owns pacing, participant routing, intervention permission, and proposal behavior.

### 2. Apply precedence

- Grill Us owns participant identity, speaker provenance, firsthand knowledge, decision authority, disagreement, and Record/Grill/Advise behavior.
- `domain-modeling` detects overloaded terms, proposes precise project language, and formats `CONTEXT.md` when a writable repository was explicitly selected.
- Do not create an ADR unless the user asks for repository documentation and the decision meets the `domain-modeling` gates.
- Without a selected writable target, keep glossary updates in the conversation. Do not claim they were saved.

### 3. Resolve terms with several humans

Give each term one state:

- `proposed` — a definition has been suggested;
- `agreed` — every affected participant confirmed it, or a named language authority accepted it;
- `contested` — attributed meanings still differ.

Keep competing meanings attached to their speakers. Translation, silence, and non-objection do not establish a shared definition. In Grill, ask one short clarification at a time. In Record, capture the conflict without proposing a canonical term. In Advise, label a canonical term suggested by the agent as an agent proposal until accepted.

### 4. Start the session

```text
Use Grill Us with the Shared Language recipe. Use Grill Us for participant routing and decision state, and domain-modeling only for terminology and glossary formatting. Do not load Matt Pocock's grilling skill. Preserve competing definitions by speaker. A term becomes agreed only after confirmation by the affected participants or a named language authority. Write files only when I explicitly select a writable repository target.
```
