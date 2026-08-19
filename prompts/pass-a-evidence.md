# Pass A — Evidence

Read:
- `SKILL.md`
- accepted `input.json`
- `contracts/evidence.schema.json`

Produce only `evidence.json` matching the schema. Normalize sources into observations; do not create Knowledge Nodes, Galaxies, visual concepts, or proficiency ratings. Every Evidence item must preserve provenance, confidence, attribution uncertainty, supported implications, explicit non-support boundaries, and correlation groups when several descriptions are the same underlying event. Prefer behavior-proximal evidence over branding language. Do not turn dependencies into personal knowledge unless the source connects them to meaningful user activity. Do not read test baselines or prior expected answers.

A Source with `kind = user_calibration` is first-party feedback from the subject after seeing an earlier result. Treat explicit corrections about authorship, AI/collaborator assistance, learning state, ownership, or prior overstatement as direct evidence that can narrow or invalidate weaker inferences. Treat statements such as “this is more important to me” as evidence of representativeness only, not capability. A self-asserted strong capability statement is still only one source and does not by itself satisfy the evidence standard for mastery, independence, troubleshooting, or transfer.
