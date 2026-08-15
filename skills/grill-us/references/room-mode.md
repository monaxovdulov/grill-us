# Room mode

Use room mode when the harness supplies stable sender identity and all participants contribute to shared conversation state.

## Bind identities

- Bind each roster entry to the harness sender ID and current display name.
- Preserve the binding when a display name changes.
- Add new participants when they join.
- Never infer identity or authority from writing style.

Treat observed group messages as contributions to the discussion. Treat a message as an instruction to the agent only when the sender directly addresses, replies to, mentions, or invokes the agent according to the harness rules.

## Accept natural ordering

Let participants answer in any order. Address questions by name. Track who answered, passed, or has not responded. Do not require alternating turns.

If one participant reports another person's view, mark it as relayed until that person confirms it.

When a participant leaves, retain their attributed claims and mark any requested final confirmation as unavailable.

## Control context volume

Absorb ambient messages into the design tree. Surface only changes, contradictions, or missing evidence that affect the current frontier.

Before starting, verify that the harness uses a shared group or thread session. If it isolates sessions per user, explain the limitation and switch to turn mode or reconfigure the harness.
