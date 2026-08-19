# Goal / Gap Orchestration Contract

This pipeline starts only after a completed Current Capability Recognition run exists.

```text
COMPLETED CURRENT RECOGNITION
        +
USER GOAL + TARGET SOURCES
        ↓
PASS_E_TARGET
        ↓ validate / repair
PASS_F_GAP
        ↓ validate / repair
PASS_G_PLAN
        ↓ validate / repair
NEXT 1–3 STEPS
```

## Hard boundary: target independence

Pass E must not read the person's current Model. The target is modeled only from the user's stated goal and target-side sources. Otherwise the system can silently move the goalposts toward whatever the person already knows.

## Hard boundary: absence is not inability

Pass F compares the accepted target against accepted current Recognition artifacts. If a requirement is not represented in current evidence, use `not_observed`; do not convert missing evidence into a claim that the person lacks the capability.

## Hard boundary: planning does not rewrite Recognition

Pass G may recommend future actions. It must never upgrade current Claims, create current Knowledge Nodes, or patch the current Scene. Progress only enters the personal universe later through new real Source material and a fresh Recognition/calibration run.

## Eligibility is not a study topic

Degree, location, work authorization, availability, or similar constraints may matter to a goal, but they do not become learning priorities. Surface unresolved eligibility requirements separately.

## Goal planning is intentionally narrow

Return 1–3 next priorities, not a complete curriculum. Lower-priority target requirements can remain deferred. The point is to answer what is most worth doing next from the person's actual footholds, not to reproduce a generic roadmap.
