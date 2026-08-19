# Pass F — Current-to-Target Gap

Read `SKILL.md`, accepted `goal_input.json`, accepted `target.json`, and the completed current Recognition artifacts copied into the workspace (`current_input.json`, `current_evidence.json`, `current_model.json`). Produce only `gap.json` matching `contracts/gap.schema.json`.

Account for every target requirement exactly once. Compare the externally grounded target against what current evidence can actually support about the person.

Status semantics:
- `supported`: current evidence and claims already support the target requirement at a materially relevant level.
- `partial`: there is a relevant foothold, but the target asks for a stronger/different dimension or broader transfer than current evidence supports.
- `unresolved`: current material is too ambiguous to decide; say what evidence would resolve it.
- `not_observed`: no direct current evidence supports the target requirement. This means **not observed in the available material**, never “the person cannot do it”.
- `not_applicable`: the requirement does not meaningfully apply to this subject/goal instance after source-grounded interpretation.

Do not create new current Knowledge Nodes or capability Claims in this pass. Cite only accepted current node/claim/evidence ids. Put adjacent existing strengths in `bridge_from_node_ids`; adjacency is a possible learning foothold, not proof that the missing requirement is already known.

Eligibility constraints are gaps/constraints, not learning topics. Preserve them for the planning pass without turning them into fake study recommendations.
