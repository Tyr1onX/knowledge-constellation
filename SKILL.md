# Knowledge Constellation Skill

> Status: research placeholder — not yet a stable executable Skill.

The final Skill will eventually transform user-provided evidence into an evidence-driven personal knowledge constellation.

For now, the repository is deliberately validating the recognition model before encoding it into a large prompt or agent workflow.

## Planned high-level behavior

```text
Existing user materials
↓
Extract observable evidence
↓
Preserve attribution uncertainty
↓
Generate bounded claims
↓
Distill knowledge nodes
↓
Produce a conservative first constellation
↓
Optionally offer low-friction calibration
```

## Current non-goals

V0 should not:

- assign impressive proficiency scores from repository technology lists;
- infer mastery because a project or pull request is sophisticated;
- require a long questionnaire before producing a result;
- silently convert uncertain authorship into personal capability;
- attempt to map every piece of knowledge a person has;
- commit to a final visualization format before the knowledge model is validated.

## Before this becomes a real Skill

The following must be tested with multiple real cases:

1. evidence extraction is consistent;
2. attribution boundaries are conservative enough;
3. claims remain traceable to evidence;
4. visible node granularity is useful rather than syllabus-like;
5. passive-only output is valuable even with unresolved areas;
6. micro-calibration materially improves the model without becoming burdensome.

See `docs/v0-knowledge-model.md` for the current protocol.
