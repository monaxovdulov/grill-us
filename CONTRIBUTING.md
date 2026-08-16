# Contributing

Grill Us is a small behavioral protocol. Contributions should make its behavior easier to understand, test, or run across agent harnesses.

## Field notes

Field notes are the most useful contribution during the early releases. Open a field-note issue and include:

- participant count and roles, without private details;
- turn mode or room mode;
- agent and harness;
- the point where provenance, routing, or disagreement handling worked or failed;
- a redacted excerpt when possible;
- the smallest protocol change you think would help.

## Protocol changes

For a change to `SKILL.md`:

1. Describe the observed failure and run the same prompt without the skill.
2. Add or update an atomic eval case that reproduces the behavior.
3. Micro-test one wording change at a time in at least five fresh runs.
4. Keep the main skill concise; put branch-specific detail in `references/`.
5. Update the Russian reader translation when behavior changes.
6. Run `python scripts/validate.py`.

Avoid generic additions that do not change a demonstrated failure mode. Preserve speaker provenance and decision ownership as protocol invariants.

## Pull requests

Keep pull requests focused. Explain the scenario, expected behavior, and evidence that the change helps. By contributing, you agree that your contribution is licensed under the repository's license.
