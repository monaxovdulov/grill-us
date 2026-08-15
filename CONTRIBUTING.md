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

1. Describe the observed failure.
2. Add or update an eval case that reproduces it.
3. Keep the main skill concise; put mode-specific detail in `references/`.
4. Update the Russian reader translation when behavior changes.
5. Run `python scripts/validate.py`.

Avoid generic additions that do not change a demonstrated failure mode. Preserve speaker provenance and decision ownership as protocol invariants.

## Pull requests

Keep pull requests focused. Explain the scenario, expected behavior, and evidence that the change helps. By contributing, you agree that your contribution is licensed under the repository's license.
