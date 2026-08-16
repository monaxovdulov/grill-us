# Example: mixed-expertise pair

This shortened transcript shows turn mode. Lena knows the operating problem; Max knows the implementation constraints. They share one terminal and prefix every answer with a name.

## Opening

```text
Use $grill-us.

Lena — runs a home-care agency. I know the shift-handoff workflow and own the
definition of a useful outcome.

Max — builds the software. I know the integration and privacy constraints and
own technical feasibility decisions.

Goal — decide what to test before building a handoff product.
Style — Grill.
Pace — one question at a time.
```

The agent records the roster and starts with one routed question.

```text
❓ Q1 → Lena — Problem evidence: What did you personally observe during a failed handoff?
```

## Answers

```text
Lena: Last Thursday the evening carer missed a medication note. I have seen
four similar misses in six weeks. One required a supervisor call.
```

The agent continues after the addressed participant answers:

```text
❓ Q2 → Max — Reversible test: What is the smallest test that avoids storing patient data?
```

```text
Max: We can test a structured handoff template with synthetic cases. No login,
database, or patient identifiers are needed.
```

```text
❓ Q3 → everyone — Success threshold: What result would justify another week of work?
```

```text
Lena: I want carers to finish the handoff in under two minutes.

Max: I agree on the time limit. I also need zero real patient data in the test.
```

The agent keeps the claims separate:

- Lena's incident count is a firsthand observation.
- Max's proposed test is a technical recommendation and feasibility decision.
- The two-minute threshold is Lena's preference until both participants adopt it as the test criterion.
- The privacy constraint is Max's technical decision.

## Disagreement

```text
Lena: Voice notes would be fastest for carers.
Max: Voice introduces sensitive audio and transcription risk. I prefer a form.
```

The agent preserves both branches and routes the next decision:

```text
❓ Q4 → Lena — User evidence: Do you have direct evidence that typing is the main handoff failure?

❓ Q5 → Max — Safe comparison: Can the test compare a form and disposable voice capture without retaining audio?
```

Lena has no evidence about typing. Max can support a supervised, non-retained voice prototype. The pair chooses an experiment rather than reporting consensus.

## Final record excerpt

```text
Outcome
Run five supervised handoffs with synthetic cases: three structured forms and
two disposable voice captures.

Decisions and owners
- Test outcome: completion under two minutes with every required field present.
  Owner: Lena. Confirmed by Max.
- Privacy: no patient identifiers and no retained audio. Owner: Max.

Problem evidence
- Lena observed four missed notes in six weeks; one caused a supervisor call.

Parked disagreement
- Preferred long-term input method. Revisit after the five-session comparison.

Confirmations
- Lena: confirmed.
- Max: confirmed.
```
