---
name: grill-us
description: Facilitate or record a rigorous decision discussion for two or more named humans while preserving speaker provenance, decision authority, and open disagreement. Use when a pair, team, cofounders, or mixed-expertise group asks to decide together, capture who said what, challenge assumptions, or receive recommendations in a shared conversation.
metadata: {"openclaw":{"emoji":"🔥","homepage":"https://github.com/monaxovdulov/grill-us"}}
---

# Grill Us

Protocol version: **0.6.0**.

Build an attributed decision tree with the participants. Treat each unresolved decision as a branch. Attach every load-bearing claim to a speaker or external source.

## Select the identity mode

- When each message has stable sender identity and all participants share one session, read `{baseDir}/references/room-mode.md`.
- When participants share an account, terminal, device, or microphone, read `{baseDir}/references/turn-mode.md`.
- When identity or shared state is uncertain, verify it before substantive questioning. Fall back to turn mode if necessary.

## Set the intervention level

Treat the level as shared-session permission. The levels are cumulative:

- **Record** — capture and classify contributions; ask only attribution or meaning clarifications.
- **Grill** — Record plus evidence-seeking and decision-seeking questions; no agent proposals. This is the default.
- **Advise** — Grill plus clearly labelled agent proposals.

Infer an explicit request: “only record this” means Record, “challenge our assumptions” means Grill, and “give us recommendations” means Advise. State the inferred level and continue without a separate setup question. When no request is present, use Grill without asking the group to choose.

If participants request different levels, honor a named facilitator with explicit authority over the meeting process. Otherwise use the lowest requested level and ask who owns the session format. Do not offer proposals while Advise remains contested. Let the group switch levels at any time.

In the first direct reply after identity mode is known, show one compact line:

```text
Grill Us v0.6.0 · <Record|Grill|Advise> · <Room|Turn> · <language>
```

## Establish the room incrementally

Start with available participant identity and the outcome wanted from the session. Build a short roster as the discussion proceeds:

- collect relevant firsthand knowledge before routing an evidence question;
- collect decision authority before requesting a decision or approval;
- ask for a role only when it changes routing;
- ask for language only when the working language is mixed or unclear.

Let participants correct the roster. Do not infer authority from confidence, technical fluency, job title alone, writing style, or message volume.

Treat firsthand knowledge as claim-scoped: a participant may have direct access to one event and none to another. Treat authority as decision-scoped: owning one decision domain does not grant authority over another.

Use the group's working language. When participants use different working languages, offer the record in the requested language and preserve decision-critical original terms with their speakers. Treat translation and agreement as separate events.

When the working language is Russian, or a Russian utterance could change consent, authority, or disagreement, read `{baseDir}/references/russian-pragmatics.md` before classifying it or writing participant-facing labels.

## Preserve provenance

Classify material contributions when doing so affects the decision:

- **Observation** — something the speaker directly saw or measured;
- **Interpretation** — what the speaker thinks the observation means;
- **Assumption** — an unverified belief;
- **Preference** — what the speaker wants;
- **Proposal** — a candidate choice that has not yet been accepted by its owner;
- **Decision** — a choice made by someone with authority;
- **Disagreement** — incompatible claims, goals, or choices that remain open.

Track proposal and decision state as proposed, accepted, rejected, or superseded. Only explicit acceptance by the named owner turns a proposal into a decision. Keep a superseded decision attributed in the record while marking that it is no longer current. Treat disagreement as a relationship between attributed positions, not as proof that either position is wrong.

Maintain the attribution ledger internally. Surface attribution when claims conflict, ownership matters, state changes, or the session ends. Mark secondhand statements as relayed rather than attributing them directly to the absent person.

Do not promote a speaker-attributed claim to group consensus unless every participant whose agreement is asserted explicitly confirms the same proposition. Silence, non-objection, a related observation, translation, or a relayed statement is not confirmation.

For decision-critical public claims, verify external facts when tools are available. Ask participants for firsthand experience, private context, judgment, and decisions.

## Compose with other skills

Other skills may change language, tone, verbosity, and formatting. Preserve speaker identity, contribution type, decision authority, decision status, proposal status, and open disagreement. Treat emoji and other display conventions as optional presentation.

## Build the decision tree

Start from the outcome the group wants from the session. Expand only branches that could change the product direction. Common branches include:

- evidence of the problem;
- users and use context;
- current alternatives and workarounds;
- desired outcome and product behavior;
- scope, exclusions, and constraints;
- value, risks, and reversibility;
- smallest useful test and required evidence.

Use these branches as options rather than a fixed questionnaire. Recompute the unresolved frontier after every answer.

## Run the interview loop

1. Identify the highest-impact unresolved branches.
2. Classify the next question as evidence-seeking or decision-seeking. Route evidence questions to the participant with the strongest relevant firsthand knowledge. Route decisions or approvals only to the named owner for that decision domain. Do not transfer authority between domains.
3. Ask at most one substantial question at a time. Use round pace only when the group requests it; then ask at most one question per participant and one shared question.
4. Use one numbered format for directed and shared questions:

```text
Q<n> → <name|everyone> — <question title>: <question>
```

In Advise, add proposals separately:

```text
Agent proposal — <proposal>
Basis: <attributed inputs or external evidence>
Status: awaiting owner decision
```

Only a named decision owner's explicit acceptance can turn an agent proposal into a decision. Wait for each addressed participant to answer or pass. Allow anyone to challenge an answer. Ask a follow-up only when it changes the frontier.

Before sending in Record or Grill, remove product recommendations and proposed solutions. In sequential pace, keep at most one substantial question.

## Expose compact state changes

When a decision, disagreement, unknown, or proposal status changes, show a short **State change** block containing only changed entries, their sources, and owners. Provide the full current ledger only on request or when finishing the session.

Recognize natural requests to show the compact state, the full record, or only open items. When explicitly asked to save the record, use a storage capability exposed by the host or return the record for the host to store. Use only conversation context supplied by the host. Do not configure, emulate, or claim durable memory.

## Handle disagreement

Keep conflicting branches visible. Resolve each disagreement through one of these paths:

- a decision by the named owner;
- a shared decision criterion;
- an experiment with a success threshold;
- a parked disagreement with an owner and revisit condition.

Resolve authority conflicts before resolving the product question.

## Finish the session

Finish only when all of the following hold:

- the decision frontier is empty or explicitly parked;
- load-bearing claims have named sources;
- each decision has an owner and rationale;
- each disagreement is resolved or parked;
- each unknown has a research action, experiment, owner, or accepted-risk label;
- each present participant explicitly confirms the record or passes; an unavailable participant is marked unconfirmed with the reason only after confirmation was requested.

If any condition remains unmet, return an **Interim record**. Do not label an unresolved or parked branch as a decision.

Return a concise record. Include Outcome, Participants and authority, Problem evidence, and Attributed decision tree when they contain useful information. Always include Decisions and owners, Open or parked disagreements, Unknowns and experiments, and Participant confirmations; write `None` when a required section is empty.

Stop before writing specifications, tickets, or implementation plans unless the group asks for them.
