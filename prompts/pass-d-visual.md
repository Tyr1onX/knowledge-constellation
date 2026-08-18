# Pass D — Personal Visual Model

Read `SKILL.md`, accepted `input.json`, accepted `model.json`, accepted `structure.json`, and `contracts/visual.schema.json`. Produce only `visual.json` matching the schema.

Decide semantic visual parameters: deterministic scene seed, Identity Core family, identity presence, composition archetype, asymmetry, openness, dominant axis, field density/dust/temperature, motion temperament, every accepted Anchor's visual provenance role, and each Galaxy's relative mass/morphology/dominance. The person's structure should influence the first-screen silhouette. Do not output coordinates, raw CSS, Canvas/WebGL code, or HTML. Do not include Evidence, Claims, confidence text, known/unknown/boundary or other Recognition truth fields. Visual drama must never upgrade capability truth. Do not read test baselines or prior expected answers.

`identity.label` must come from `input.json.subject.label`; do not recover identity from node labels or invent a persona. `identity.presence` controls only the brief product-level identity introduction described by the schema.

Every Structure Anchor must appear exactly once in `visual.anchors` using the same id. Do not rename or reinterpret Anchor semantics here. The visual Anchor only selects low/medium provenance presence and lists the Galaxies that its accepted nodes actually belong to. Project Anchor is not a Knowledge Star, skill badge, competence signal, or new claim.

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

## Background Field rules

Treat the background as **ambient space**, never as a second semantic subject. Pure black / near-black negative space must remain dominant.

Choose `field.dust_family` only from the quality-gated options allowed by the schema. The current supported families are:

- `almost_empty`
- `cold_filament`
- `broken_cloud`

Choose the field family for overview readability and composition balance, not as a personality metaphor. Do not map `broken_cloud` to creativity, `almost_empty` to simplicity, or any background morphology to capability, mood, learning state, or life stage.

If several field families fit equally well, prefer the quieter one. A denser knowledge model does not require a denser background.

Do not output meteor timing, particle counts, parallax speed, blur radii, shader parameters, dust coordinates, or other rendering constants. Very subtle parallax, drift, and rare meteor events are Renderer-owned ambient behavior. A meteor is an environmental event, not a data event and not a signal that the user's knowledge changed.

Detailed renderer-side constraints live in `docs/background-field-visual-grammar.md`; this prompt contains the semantic rules required for Pass D and must remain usable in an isolated workspace.
