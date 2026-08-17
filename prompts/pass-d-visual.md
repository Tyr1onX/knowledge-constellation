# Pass D — Personal Visual Model

Read `SKILL.md`, accepted `model.json`, accepted `structure.json`, and `contracts/visual.schema.json`. Produce only `visual.json` matching the schema.

Decide semantic visual parameters: deterministic scene seed, Identity Core family, composition archetype, asymmetry, openness, dominant axis, field density/dust/temperature, motion temperament, and each Galaxy's relative mass/morphology/dominance. The person's structure should influence the first-screen silhouette. Do not output coordinates, raw CSS, Canvas/WebGL code, or HTML. Do not include Evidence, Claims, confidence text, known/unknown/boundary or other Recognition truth fields. Visual drama must never upgrade capability truth. Do not read test baselines or prior expected answers.

## Identity Core rules

Choose exactly one `identity.family` allowed by the schema. The current supported pool is:

- `monogram`
- `eclipse`
- `quiet_star`
- `minimal_ring`
- `black_hole`
- `pulsar`
- `binary_star`
- `protostar_nebula`

The family is a **visual composition grammar**, not a personality or capability label. Never choose a family because a person seems mysterious, focused, intelligent, senior, young, beginner, mature, intense, creative, introverted, or similar. A black hole is not a personality metaphor; a protostar is not a learning-state metaphor.

Prefer the family that best fits the global scene geometry and overview readability. Consider composition compatibility, center clearance, openness/compactness, and whether the scene already has a strong dual-system structure. If several families fit equally well, prefer the simpler family with the clearer silhouette.

Do not use the deterministic seed to choose the Identity Core family. Do not invent family-specific decorations or rendering instructions. Renderer owns the astronomical detail and must enforce the one-subject rule: one Core family has one primary visual subject, with auxiliary elements strictly subordinate.

Detailed renderer-side constraints live in `docs/identity-core-visual-grammar.md`; this prompt contains the semantic rules required for Pass D and must remain usable in an isolated workspace.
