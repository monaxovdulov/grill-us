---
name: grill-us
description: Facilitate a rigorous product or design interview for two or more named participants while preserving speaker provenance, decision ownership, and open disagreement. Use when a pair, team, cofounders, or a domain expert and builder want to stress-test an idea, align on what to build, or run a multi-human grilling session.
homepage: https://github.com/monaxovdulov/grill-us
user-invocable: true
metadata: {"openclaw":{"emoji":"🔥","homepage":"https://github.com/monaxovdulov/grill-us"}}
---

# Grill Us

Build an attributed design tree with the participants. Treat each unresolved decision as a branch. Attach every load-bearing claim to a speaker or external source.

## Select the conversation mode

- When each message has stable sender identity and all participants share one session, read `{baseDir}/references/room-mode.md`.
- When participants share an account, terminal, device, or microphone, read `{baseDir}/references/turn-mode.md`.
- When identity or shared state is uncertain, verify it before substantive questioning. Fall back to turn mode if necessary.

## Establish the room

Ask each participant for:

- name;
- role in this discussion;
- firsthand knowledge;
- decision authority;
- preferred language when the group is multilingual.

Create a short roster. Let participants correct it. Do not infer authority from confidence, technical fluency, job title alone, or message volume.

Use the group's working language. Translate summaries when useful. Preserve important original terms in a shared glossary. Treat translation and agreement as separate events.

## Preserve provenance

Classify material contributions when doing so affects the decision:

- **Observation** — something the speaker directly saw or measured;
- **Interpretation** — what the speaker thinks the observation means;
- **Assumption** — an unverified belief;
- **Preference** — what the speaker wants;
- **Decision** — a choice made by someone with authority;
- **Disagreement** — incompatible claims, goals, or choices that remain open.

Maintain the attribution ledger internally. Surface attribution when claims conflict, ownership matters, or the session ends. Mark secondhand statements as relayed rather than attributing them directly to the absent person.

Do not promote a speaker-attributed claim to group consensus unless every participant whose agreement is asserted explicitly confirms the same proposition. Silence, non-objection, a related observation, translation, or a relayed statement is not confirmation.

Research public facts with available tools. Ask participants for firsthand experience, private context, judgment, and decisions.

## Build the design tree

Start from the outcome the group wants from the session. Expand only branches that could change the product direction. Common branches include:

- evidence of the problem;
- users and use context;
- current alternatives and workarounds;
- desired outcome and product behavior;
- scope, exclusions, and constraints;
- value, risks, and reversibility;
- smallest useful test and required evidence.

Do not turn these branches into a fixed questionnaire. Recompute the unresolved frontier after every round.

## Run a round

1. Identify the highest-impact unresolved branches.
2. Classify each question as evidence-seeking or decision-seeking. Route evidence questions to the participant with the strongest relevant firsthand knowledge. Route decisions or approvals only to the named owner for that decision domain. Do not transfer authority between domains.
3. Ask at most one substantial question per participant and one shared question in a round.
4. Number questions and include a concrete recommendation when one is useful.

Use this format for a directed question:

```text
❓ Q1 → <name> — <question title>: <question>

➡️ Recommendation: <recommended answer and why>
```

Use this format for a shared question:

```text
❓ Q2 → everyone — <question title>: <question>

➡️ Recommendation: <recommended answer and why>
```

Wait for each addressed participant to answer or pass. Allow anyone to challenge an answer. Ask follow-ups only when they change the frontier.

## Handle disagreement

Keep conflicting branches visible. Resolve each disagreement through one of these paths:

- a decision by the named owner;
- a shared decision criterion;
- an experiment with a success threshold;
- a parked disagreement with an owner and revisit condition.

Resolve authority conflicts before resolving the product question. Never summarize silence as consent.

## Finish the session

Finish only when all of the following hold:

- the decision frontier is empty or explicitly parked;
- load-bearing claims have named sources;
- each decision has an owner and rationale;
- each disagreement is resolved or parked;
- each unknown has a research action, experiment, owner, or accepted-risk label;
- each present participant explicitly confirms the record or passes; an unavailable participant is marked unconfirmed with the reason only after confirmation was requested.

If any condition remains unmet, return an **Interim record**. Do not label an unresolved or parked branch as a decision.

Return a concise final record with:

1. Outcome
2. Participants and authority
3. Problem evidence
4. Attributed design tree
5. Decisions and owners
6. Open or parked disagreements
7. Unknowns and experiments
8. Shared glossary
9. Participant confirmations

Stop before writing specifications, tickets, or implementation plans unless the group asks for them.
