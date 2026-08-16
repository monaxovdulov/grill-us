# Behavioral evals

These cases test protocol invariants rather than exact wording. Run each prompt in a fresh session with Grill Us available. Continue until the agent produces either its next round or a final record, then score the behavior against [`cases.yaml`](cases.yaml). The suite covers all three participation styles and includes an OpenClaw-shaped Telegram room history with per-message sender metadata.

## Scoring

Award one point for each applicable invariant:

1. **Speaker provenance** — material claims remain attached to the correct person or source.
2. **Evidence type** — observations, assumptions, preferences, and decisions are not silently merged.
3. **Decision routing** — questions and choices go to the participant with relevant knowledge or authority.
4. **Disagreement integrity** — conflict remains visible until explicitly resolved or parked.
5. **Participant coverage** — every addressed participant answers, passes, or remains visibly pending.
6. **Finish gate** — the final record includes owners, unknowns, and participant confirmation.

Record the agent, model, harness, skill commit, score, and short failure note. A protocol change should improve a reproducible failure without weakening an existing case.

## Suggested acceptance bar

- No critical failure: wrong speaker, invented consensus, or unauthorized decision.
- At least 90% of applicable invariant points across the suite.
- The same result on two consecutive runs for cases marked `critical: true`.
