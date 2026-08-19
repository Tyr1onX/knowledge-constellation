# Pass E — Target Model

Read only `SKILL.md`, accepted `goal_input.json`, and `contracts/target.schema.json`. Produce only `target.json` matching the schema.

Model what the stated goal actually requires from the target sources. Do **not** read the person's current Recognition Model in this pass: the target must not be weakened, strengthened, or reworded to fit the current person.

Each requirement must be source-grounded. Separate knowledge/practice/experience requirements from non-learning eligibility constraints. Use `required`, `preferred`, and `contextual` conservatively; job descriptions often mix hard requirements, preferences, and broad context. Preserve ambiguity instead of inventing a universal competency rubric.

Prefer target sources in this order when available: the exact user-provided role → current official internship/campus roles matching the goal → closely adjacent official roles used only as contextual evidence. Do not silently raise an internship target using full-time or social-recruitment requirements; if an adjacent role contributes context, say so in `ambiguity` and keep its requirement strength conservative.

A requirement should describe an externally justified capability or constraint, not a syllabus-shaped list of every technology commonly associated with the role. If target sources disagree, retain the requirement only at the strength the sources justify and explain the disagreement in `ambiguity`.
