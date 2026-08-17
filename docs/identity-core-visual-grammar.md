# Identity Core Visual Grammar｜身份中心核视觉语法

> Status: **Current visual contract**
>
> This document narrows and extends the Identity Core rules in `model-spec-v1.md`. For Identity Core family selection and rendering constraints, this document is authoritative.

## 1. Purpose

Identity Core represents the person at the center of the knowledge universe.

It is **not**:

- a skill score;
- a personality test result;
- an avatar template library;
- a place for Codex to freely invent a logo;
- a signal of seniority, intelligence, maturity, or capability.

The goal is:

> **a small set of high-quality astronomical visual grammars that can produce personal variation without sacrificing the visual identity of Knowledge Constellation.**

The center must feel like a special object inside the same universe as the knowledge stars, not like a UI badge pasted on top of the scene.

---

## 2. Fixed visual language

Every supported Core family must obey the same product language:

- dark negative space remains dominant;
- light is restrained and low-saturation;
- no neon sci-fi HUD treatment;
- no thick outlines or obvious button shapes;
- motion is slow and quiet;
- the Core may be visually important, but must not drown out nearby knowledge structure;
- astronomical detail is simplified only when necessary for product scale;
- simplification must preserve the recognizable structural logic of the source phenomenon.

The renderer may use Canvas, WebGL, shaders, particles, textures, or precomputed assets internally. Those implementation choices are not part of the semantic model.

---

## 3. One-subject rule

The most important composition rule is:

> **One Core family has one primary visual subject.**

Auxiliary elements may explain or support that subject, but they must never compete with it.

Bad example:

```text
ring + TY + center dot + second orbit + strong halo
```

There is no clear primary subject.

Good example:

```text
minimal ring
primary subject = incomplete orbit
auxiliary = one tiny anchor on the orbit
```

A family definition must always answer:

1. What is the primary subject?
2. Which auxiliary structures are allowed?
3. Which combinations are forbidden because they create a second subject?

---

## 4. Current supported families

The current quality-gated family pool contains eight options.

### `monogram`

**Primary subject:** the monogram itself.

Typical form:

- small dark celestial body;
- restrained `TY` / user monogram as the internal identity mark;
- weak halo or a single subtle boundary.

Allowed auxiliaries:

- weak field glow;
- one subtle body boundary.

Forbidden:

- separate center light point;
- strong orbit competing with the monogram;
- duplicate identity text.

---

### `eclipse`

**Primary subject:** the occluding dark body.

Typical form:

- mostly dark body;
- partial edge light;
- very weak corona.

Allowed auxiliaries:

- local edge illumination;
- low-intensity surrounding field.

Forbidden:

- center text;
- center light point;
- full bright ring that replaces the occlusion logic.

---

### `quiet_star`

**Primary subject:** one compact point-light star.

Typical form:

- very small luminous core;
- soft long-range glow;
- optional extremely weak diffraction structure.

Allowed auxiliaries:

- soft halo;
- subtle directional diffraction.

Forbidden:

- visible solid UI sphere;
- orbit system;
- text inside the star.

---

### `minimal_ring`

**Primary subject:** one incomplete orbit / field line.

Typical form:

- thin, offset or tilted orbit;
- partial openness;
- at most one tiny anchor located on the orbit.

Allowed auxiliaries:

- one orbit anchor;
- weak field glow.

Forbidden:

- `TY` inside the ring;
- a separate center dot;
- multiple equally important rings.

---

### `black_hole`

**Primary subject:** the gravitational shadow / dark core system.

Astronomical structure to preserve:

- black-hole shadow;
- thin accretion disk;
- gravitationally lensed disk image;
- very thin photon-ring-like edge detail;
- directional brightness asymmetry where appropriate.

Allowed auxiliaries:

- thin accretion structure;
- weak lensed arcs;
- restrained disk texture.

Forbidden:

- generic black circle with a decorative neon ring;
- high-saturation cinematic fire;
- unrelated identity text in the center.

This family does not mean that the person is "mysterious", "deep", "introverted", or any other personality metaphor.

---

### `pulsar`

**Primary subject:** an extremely compact neutron-star-like luminous body.

Astronomical structure to preserve:

- very small dense stellar body;
- magnetic-pole hot regions;
- directional emission aligned to a magnetic axis that may differ from the rotation axis.

Allowed auxiliaries:

- broad, faint directional beams;
- subtle magnetospheric trace;
- restrained pulsing motion.

Forbidden:

- bright laser-beam treatment;
- large glowing sphere;
- additional orbit or text competing with the star.

This family must never imply focus, intelligence, intensity, expertise, or other personality/capability traits.

---

### `binary_star`

**Primary subject:** the relationship between two stars as one orbital system.

Astronomical structure to preserve:

- two stellar bodies;
- shared barycentric orbit;
- elliptical / inclined orbital geometry where useful.

Allowed auxiliaries:

- faint orbit traces;
- subtle system glow between the pair.

Forbidden:

- fake visible center object at the barycenter;
- third identity marker;
- one star visually reduced to a meaningless decoration.

This is the only current family where two bodies may jointly constitute the single primary subject: **the binary system itself**.

---

### `protostar_nebula`

**Primary subject:** one condensation center embedded in a diffuse forming structure.

Astronomical structure to preserve:

- gas / dust concentrated around a real center;
- central hot source;
- disk or dark lane where appropriate;
- bipolar cavity / outflow structure where used.

Allowed auxiliaries:

- restrained cloud filaments;
- thin disk;
- bipolar low-density structure.

Forbidden:

- random decorative smoke without a center;
- full-screen cloud texture that hides the knowledge universe;
- interpreting this family as "beginner", "young", or "still learning".

---

## 5. Codex selection contract

Codex chooses the **family**, not the drawing implementation.

At the current version, Identity Core intentionally exposes very few semantic controls:

```yaml
identity:
  family: black_hole
  label: Tyr1onX
  monogram: TY
```

That is enough.

Codex must not output:

- shader code;
- particle counts;
- ring widths;
- ray-tracing parameters;
- detailed drawing instructions;
- arbitrary decorative motifs.

### Selection may consider

- global composition compatibility;
- amount of free space around the center;
- whether the overall scene is compact, open, orbital, or diffuse;
- whether the visual composition already has a strong dual-system structure;
- readability at the expected overview scale.

### Selection must not infer

- personality;
- intelligence;
- skill level;
- seniority;
- confidence;
- learning maturity;
- emotional state;
- human value.

A `black_hole` is not a personality label. A `protostar_nebula` is not a beginner label. A `pulsar` is not an expertise label.

If multiple families fit equally well, prefer the simpler family with the clearer first-screen silhouette.

---

## 6. Personalization rule

Personalization comes primarily from the **whole universe**, not from random Core decoration.

The largest sources of personal difference should be:

- Galaxy count and mass;
- first-screen silhouette;
- spatial asymmetry;
- relation structure;
- node density and distillation;
- field and motion temperament;
- Identity Core family.

Do not manufacture individuality through dozens of tiny Core parameters.

The current system deliberately does **not** expose seed-driven Core topology changes. A deterministic scene seed may still stabilize minor background details, but it must not:

- randomly choose the Core family;
- add or remove major Core components;
- change which element is the primary subject.

Same snapshot → same Core family and same structural grammar.

---

## 7. Renderer contract

The Renderer owns the aesthetic floor.

For every supported family it must guarantee:

1. one clear primary subject;
2. compliance with the shared visual language;
3. no accidental multi-subject composition;
4. no visual implication of capability ranking;
5. acceptable appearance at overview scale;
6. acceptable appearance during zoom;
7. stable deterministic rendering for the same scene snapshot;
8. Core interaction remains separable from knowledge-node interaction.

The Renderer may contain family-specific implementations, including specialized shaders, as long as they expose one stable semantic interface to the Scene Spec.

---

## 8. Astronomy fidelity and reuse policy

For astronomy-inspired families:

1. inspect authoritative descriptions / imagery before implementation;
2. preserve the structural reason the object looks distinctive;
3. simplify for product scale only after the structure is understood;
4. prefer compatible existing rendering techniques or open-source implementations when they materially improve quality;
5. verify license compatibility and retain required attribution;
6. isolate heavyweight external rendering code behind the Renderer boundary;
7. do not let a reusable shader or particle library dictate the semantic model.

Reusing a good black-hole shader is preferable to inventing a worse one from scratch. But importing a heavy dependency is not justified when a lightweight approximation already meets the product-quality bar.

---

## 9. Quality gate

A new Core family is accepted only if all answers are yes:

- Is its primary subject obvious within one second?
- Does it still look like part of Knowledge Constellation?
- Is its astronomical inspiration structurally recognizable where applicable?
- Are auxiliary elements subordinate?
- Does it remain restrained beside knowledge stars?
- Can the Renderer implement it without changing Recognition truth?
- Does it avoid personality / capability symbolism?
- Does it add a genuinely different composition grammar rather than a cosmetic variant?

If a candidate differs only by tiny halo, seed, star position, or ring-angle changes, it is **not** a new family.

---

## 10. Current decision

Current supported pool:

```text
monogram
eclipse
quiet_star
minimal_ring
black_hole
pulsar
binary_star
protostar_nebula
```

This is a sufficient family set for the current product stage.

Do not expand the pool merely to make it look more configurable. Add a new family only when a real composition need appears and the new grammar survives the quality gate.
