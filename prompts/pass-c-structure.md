# Pass C — Anchors, Relations, Motifs, Galaxies, Distillation

Read `SKILL.md`, accepted `evidence.json`, accepted `model.json`, and `contracts/structure.schema.json`. Produce only `structure.json` matching the schema.

Anchors are real experiences: projects, recurring activity streams, learning trajectories, long-running knowledge bases, goals, or repeated task contexts. Relations require actual personal Evidence; world knowledge may explain but not invent them. Galaxies are recurring personal themes, not default syllabus categories. Prefer names grounded in the person's own project identity, contribution stream, or learning trajectory.

Not every recurring idea deserves a Galaxy. Use `motifs` for cross-cutting goals, provenance patterns, working modes, or themes that connect existing nodes without owning them. A Motif is not a Knowledge Star and must not be used to rescue leftover nodes into a synthetic Galaxy. AI-assisted/collaborative work is commonly a Motif/provenance fact rather than a Galaxy.

Use `trajectory` only when the sources establish chronology. Every trajectory relation must include `temporal_basis.earlier_evidence`, `temporal_basis.later_evidence`, and a short source-grounded rationale. The earlier/later sets must represent genuinely ordered observations, not merely two related pieces of evidence. If chronology is unavailable, use `repeated_context`, `practice`, `co_occurrence`, or omit the relation.

Apply the removal test aggressively: if removing a node barely changes who this looks like, it likely belongs deeper. Every accepted Knowledge Node must appear in exactly one Galaxy and one display layer. Motifs may reference nodes across Galaxies but do not change node ownership. Do not read test baselines or prior expected answers.
