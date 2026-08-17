# Background Field Visual Grammar｜背景场视觉语法

> Status: **Current visual contract**
>
> This document defines the atmospheric background layer behind the Knowledge Constellation universe. It complements `model-spec-v1.md` and the Identity Core contract.

## 1. Purpose

The background exists to make the universe feel spatial and alive without becoming a second subject.

The governing principle is:

> **Pure black remains the dominant visual condition. Background variation should be felt before it is consciously noticed.**

The background is atmosphere, not knowledge, identity, personality, capability, or narrative truth.

It must never compete with:

- Knowledge Nodes;
- Galaxy silhouette;
- relations;
- Identity Core;
- semantic zoom and inspection.

---

## 2. Visual hierarchy

The expected visual order is:

```text
Knowledge structure
Identity Core
Primary knowledge stars
Secondary knowledge stars / relations
Ambient background field
```

A failed background reverses this hierarchy.

Failure examples:

- the user notices the nebula before the knowledge structure;
- the scene resembles a wallpaper or screensaver;
- background stars are mistaken for interactive knowledge stars;
- a meteor repeatedly steals attention;
- bright color fields create a stronger silhouette than the Galaxies.

---

## 3. Layer model

The renderer may build the background from several restrained layers.

### Layer 0 — Negative space

The majority of the frame remains near-black.

This is the foundation of the product identity, not an empty area that must be filled.

### Layer 1 — Distant stars

Very small, low-contrast points may establish depth.

They must be visually distinct from interactive Knowledge Nodes:

- much lower brightness;
- smaller apparent size;
- no hover affordance;
- no semantic labels;
- no relation lines;
- no strong local glow.

### Layer 2 — Diffuse field structure

Optional large-scale astronomical structure may break the flatness of pure black.

Current quality-gated forms are:

- `almost_empty` — effectively pure black with distant stars;
- `cold_filament` — faint silver / cool-gray filamentary structure;
- `broken_cloud` — discontinuous low-contrast cloud fragments.

The structure should contain gaps, irregularity, and dark interruption. It must not read as a pasted gradient or obvious galaxy photograph.

### Layer 3 — Depth motion

Very small parallax or drift may make the field feel spatial.

Rules:

- motion must be slower and weaker than interactive foreground motion;
- pointer parallax should be subtle enough that the user does not perceive the background as following the cursor;
- motion must not imply semantic movement of the person's knowledge model.

### Layer 4 — Rare ambient events

Occasional events such as a distant meteor may be used to add life.

Rules:

- rare by default;
- brief;
- thin and low-contrast;
- never a repeating spectacle;
- never required for understanding the scene;
- never mapped to personal capability, activity, mood, or progress.

A meteor is an environmental event, not a data event.

---

## 4. Accepted visual directions

### `almost_empty`

Use when the scene already has enough visual structure or when maximum negative space is desirable.

Characteristics:

- dominant near-black field;
- sparse distant stars;
- no obvious large-scale cloud structure.

### `cold_filament`

Use a faint silver / cool-gray filament system.

Characteristics:

- broad, low-frequency wisps;
- a few finer inner strands;
- irregular breaks and dark lanes;
- no bright Milky-Way-like band;
- no saturated blue glow.

The user should perceive depth and texture, not "a nebula image".

### `broken_cloud`

Use several separated diffuse cloud regions with large gaps.

Characteristics:

- fragmented rather than continuous;
- low-contrast silver / cool-neutral tones;
- local dark holes and interruptions;
- large black regions remain visible between fragments.

Avoid fog-overlay aesthetics.

### Rare meteor treatment

Meteor rendering is not a `dust_family` and does not replace the field family.

Recommended behavior:

- approximately tens of seconds between possible events rather than every few seconds;
- one event at a time;
- a short fading trail;
- very low probability of appearing during a brief visit;
- no meteor shower mode in the normal product.

---

## 5. Codex / Personal Visual Model boundary

Pass D may choose semantic field parameters already exposed by `visual.schema.json`, including:

- `field.density`;
- `field.dust_family`;
- `field.temperature_bias`.

These choices should support overview readability and composition balance.

Codex must not:

- treat a background family as a personality label;
- select `broken_cloud` because a person is "creative";
- select `almost_empty` because a person is "simple";
- use field drama to imply stronger capability;
- output particle counts, blur radii, meteor timing, parallax speed, shader code, coordinates, or rendering constants.

If several field families fit equally well, prefer the quieter one.

---

## 6. Renderer responsibilities

Renderer owns the exact implementation and must guarantee hierarchy.

Renderer may decide:

- star-field density within the semantic range;
- opacity and spatial frequency of filaments / clouds;
- dark-lane placement;
- parallax depth;
- drift speed;
- meteor timing and path;
- Canvas / WebGL / shader / texture implementation;
- responsive simplification and performance fallbacks.

Renderer must preserve:

1. dominant black negative space;
2. foreground readability;
3. clear distinction between ambient stars and Knowledge Nodes;
4. low-saturation astronomical language;
5. restrained motion;
6. background visual strength below the knowledge structure.

---

## 7. Density and scale

A larger knowledge model does not require a busier background.

Background density should not scale linearly with the number of Knowledge Nodes.

When the foreground becomes dense, the renderer should generally simplify or quiet the field rather than add more visual material.

Canonical rule:

> **More knowledge may mean more foreground structure, not more background decoration.**

---

## 8. Accessibility and reduced motion

For reduced-motion environments:

- disable or greatly reduce parallax;
- disable passive drift if needed;
- disable rare meteor events;
- preserve static field morphology and contrast hierarchy.

The visual identity must remain valid without animation.

---

## 9. Current checkpoint

The accepted baseline from the visual lab is:

- pure-black-dominant field;
- restrained distant stars;
- visible-but-subordinate `cold_filament` and `broken_cloud` variants;
- very light pointer parallax;
- rare, subtle meteor as renderer-owned ambient life.

This contract intentionally stops here. Do not expand the background into a general astronomical-effects system unless a future product need demonstrates that the current vocabulary is insufficient.
