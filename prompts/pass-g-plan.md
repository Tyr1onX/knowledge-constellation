# Pass G — Next Best Steps

Read `SKILL.md`, accepted `goal_input.json`, accepted `target.json`, accepted `gap.json`, and `current_model.json`. Produce only `plan.json` matching `contracts/plan.schema.json`.

Choose **1–3 priorities only**. The plan is not a complete curriculum. Prefer the smallest set of steps that most naturally bridges the person's existing evidence-backed footholds toward important unresolved/partial target requirements.

A priority must explain:
- which target requirement(s) it advances;
- which current accepted nodes, if any, make it a sensible next move;
- why it deserves attention now rather than merely being generally useful;
- one concrete action;
- what new observable artifact or behavior would count as evidence of progress.

Do not claim a step is objectively optimal when the goal sources or user constraints do not establish that. Do not recommend work merely to make the constellation denser. Do not upgrade current capability while planning future learning.

Requirements already `supported` should not be the sole reason for a priority. `eligibility` requirements are not learning priorities; surface them under `non_learning_constraints`. Put lower-priority actionable requirements in `deferred_requirement_ids` rather than producing a long checklist.

The intended user-facing answer is simple: **where am I now, what matters for this goal, and what are the next 1–3 things worth doing?**
