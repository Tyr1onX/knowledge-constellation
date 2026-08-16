# Knowledge Constellation Model Spec v1

> This document defines the contract between **recognizing a person** and **rendering that recognition as a personal universe**.

Knowledge Constellation has two independent success criteria:

1. **Recognition truthfulness** — form a useful model from incomplete evidence without claiming more than the evidence supports.
2. **Visual externalization** — turn that model into a distinctive, beautiful, explorable universe without letting visual drama overstate capability.

The renderer must never invent personal truth.  
The recognition pipeline must never dictate a single fixed visual composition.

---

## 1. System boundary

```text
RAW INPUT
  ↓
Source
  ↓
Evidence
  ↓
Attribution
  ↓
Claim
  ↓
Knowledge Node
  ↓
Anchor
  ↓
Relation
  ↓
Galaxy
  ↓
Distillation
  ↓
Personal Visual Model
  ↓
Scene Spec
  ↓
Renderer
  ↓
Knowledge Constellation
```

This creates a hard boundary:

- **Recognition side** answers: what are we justified in believing?
- **Visualization side** answers: how should that belief become space?
- **Renderer** owns interaction and visual quality.
- A coding agent must not rebuild the renderer from scratch for every user.

---

# Part A — Recognition Model

## 2. Source

A Source is an original input container.

Examples:

- GitHub profile / repository / PR / issue
- resume
- learning log
- project documentation
- portfolio
- user self-report
- calibration answer
- external review or test result

```yaml
source:
  id: S1
  kind: github_repository
  title: desktop-course-widget
  uri: github:Tyr1onX/desktop-course-widget
  visibility: public
  observed_at: 2026-08-16
```

A Source does **not** directly create a skill claim.

---

## 3. Evidence

Evidence is a normalized observation extracted from a Source.

```yaml
evidence:
  id: E4
  source_id: S2
  kind: artifact
  observation: >
    A continuously maintained Windows desktop timetable product exists and
    contains Tauri, Rust, TypeScript, import, local data, tests and release work.
  confidence: high
  attribution: uncertain
  supports:
    - project_exposure
    - product_iteration
  does_not_support:
    - independent_rust_mastery
    - independent_tauri_mastery
```

### Required fields

- `id`
- `source_id`
- `kind`
- `observation`
- `confidence`
- `attribution`

### Optional fields

- `observed_at`
- `supports`
- `does_not_support`
- `correlation_group`
- `freshness`

### Rule

**Evidence describes what was observed, not what the person “is”.**

---

## 4. Attribution

Attribution answers who actually carried the activity.

A result can be real while personal execution remains unresolved.

### Human contribution roles

- `initiated`
- `selected`
- `specified`
- `implemented`
- `reviewed`
- `validated`
- `operated`
- `authorized`
- `debugged`
- `explained`

### Agent / collaborator roles

The same vocabulary may be recorded separately for:

- AI agent
- collaborator
- maintainer
- automation
- template / generator

```yaml
attribution:
  human:
    selected: supported
    implemented: unknown
    validated: partial
  agent:
    implemented: unknown
  resolution: low
```

### Core rule

> Participation is not execution evidence.

---

## 5. Claim

A Claim is the smallest statement the current evidence is allowed to support.

```yaml
claim:
  id: C-rust-exposure
  subject: rust
  dimension: exposure
  value: high
  confidence: high
  evidence: [E4]
  boundary: >
    Project use of Rust does not prove independent Rust implementation ability.
```

Claims should be dimension-specific.

Do not compress these into one “skill score”:

- exposure
- understanding
- implementation
- independence
- judgment
- debugging
- transfer
- recency
- representativeness

---

## 6. Knowledge Node

A Knowledge Node is a stable concept worth representing in the model.

```yaml
node:
  id: rust
  label: Rust
  state: observed
  confidence: low
  resolution: low

  signals:
    exposure: high
    capability: unresolved
    representativeness: medium_high

  claims:
    - C-rust-exposure

  evidence:
    - E4

  known:
    - Rust is strongly associated with current project experience.

  unknown:
    - Independent implementation ability.
    - Independent debugging depth.
    - Transfer to unfamiliar Rust projects.

  boundary:
    - Artifact presence is not mastery.

  display:
    priority: primary
```

### Node state vocabulary

Current recommended states:

- `established`
- `developing`
- `observed`
- `unresolved`

These describe **evidence support**, not traditional proficiency levels.

---

## 7. Anchor

An Anchor is a real experience that explains why several nodes belong near each other.

Anchor types:

- project
- activity stream
- learning trajectory
- long-maintained knowledge base
- recurring goal
- repeated task context

```yaml
anchor:
  id: course-widget
  kind: project
  label: 课刻
  nodes:
    - product-iteration
    - tauri
    - rust
    - typescript
```

Anchor answers:

> Why are these nodes close in this person's world?

---

## 8. Relation

Relations require actual personal evidence.

Current relation vocabulary:

- `co_occurrence`
- `repeated_context`
- `trajectory`
- `practice`

```yaml
relation:
  source: product-iteration
  target: tauri
  kind: co_occurrence
  strength: medium
  evidence: [E4]
```

External taxonomy knowledge may help explain or lay out a relation, but it must not create a personal relation that has no evidence.

---

## 9. Galaxy

A Galaxy is a recurring **personal theme**, not a syllabus category.

A Galaxy should normally have:

- at least one Anchor
- multiple supported nodes
- actual relations
- sustained personal relevance
- a silhouette distinguishable from another Galaxy

Good:

- 课刻与桌面产品
- 开源参与与工程流转
- Web 基础补全

Usually bad as a default:

- Frontend
- Backend
- Database
- Programming Languages

```yaml
galaxy:
  id: desktop-product
  label: 课刻与桌面产品
  anchor: course-widget
  primary_nodes:
    - product-iteration
    - tauri
    - rust
    - typescript
  secondary_nodes:
    - ocr
    - windows-desktop
    - excel-import
```

One node should have one `primary_galaxy`, while cross-galaxy relations remain possible.

---

## 10. Distillation

The internal model can be much richer than the first screen.

Distillation is explainable lossy compression.

### Primary test

> If removing this node barely changes who this looks like, it probably belongs in a deeper layer.

### Important distinction

`representativeness != capability`

A node may be visually important because it strongly represents the person's current life while still having unresolved capability.

### Suggested internal dimensions

- representativeness
- confidence
- resolution
- structural role
- recency
- activity

Do not collapse them into one fake score.

---

# Part B — Personal Visual Model

## 11. Identity Core

The universe has a center representing the person.

```yaml
identity:
  mode: monogram
  label: Tyr1onX
  monogram: TY
  avatar: null
  reset_view_on_activate: true
```

Supported center families may include:

- `avatar`
- `monogram`
- `name`
- `quiet_star`
- `eclipse`
- `minimal_ring`

The **existence of a center** is a design rule.  
The **appearance of the center** is a personalization choice.

Activating the Identity Core may later act as an explicit “return to overview” action.

---

## 12. Visual DNA

Visual DNA provides diversity without asking a coding agent to redesign the application.

```yaml
visual_dna:
  seed: kc:v1:Tyr1onX:2026-08-16

  composition:
    archetype: three_islands
    dominant_axis: diagonal
    asymmetry: 0.63
    openness: 0.58

  identity_core:
    family: monogram

  field:
    density: sparse
    dust_family: cold_filament
    temperature_bias: cool_neutral

  stars:
    family: subtle_point
    temperature_variation: low

  motion:
    temperament: quiet
```

### Deterministic rule

Visual variation must use a deterministic seed derived from stable inputs such as:

```text
subject id
+ knowledge-model fingerprint
+ visual-system version
```

The same snapshot should reproduce the same universe.

A changing knowledge model should **evolve** the universe, not randomly reshuffle it.

---

## 13. Composition Model

Different users should be able to produce different first-screen silhouettes.

Possible composition archetypes include:

- dominant core + satellites
- dual core
- three islands
- stream / trajectory
- sparse archipelago
- compact cluster
- asymmetric chain

Composition should be driven by:

- Galaxy mass
- relation density
- dominant Anchor
- number of primary vs secondary nodes
- cross-galaxy bridges
- representativeness distribution
- activity / recency

Do not select an archetype merely for decoration.

---

## 14. Scene Spec

Scene Spec is the direct input contract for the renderer.

```yaml
scene:
  identity:
    mode: monogram
    label: Tyr1onX

  galaxies:
    - id: desktop-product
      mass: 0.92
      center: [0.68, 0.36]
      morphology: elongated
      dominant: true

  nodes:
    - id: rust
      galaxy: desktop-product
      layer: primary
      presence: 0.74
      resolution: 0.28
      activity: 0.41

  relations:
    - source: product-iteration
      target: rust
      visibility: contextual

  visual_dna:
    seed: kc:v1:Tyr1onX:2026-08-16
```

The Scene Spec contains **visual semantics**, not raw CSS or HTML.

---

# Part C — Renderer Contract

## 15. Renderer owns presentation quality

The renderer is a reusable product asset.

It owns:

- Canvas / WebGL implementation
- d3-force physics
- star rendering
- background field rendering
- Semantic Zoom
- progressive node reveal
- camera easing
- pointer-centered zoom
- drag behavior
- focus / relation reveal
- Identity Core rendering
- detail inspector
- responsive behavior
- accessibility
- performance

A model-generating agent should not regenerate these implementation details for each user.

---

## 16. Semantic Zoom contract

Current spatial levels:

```text
Universe overview
  ↓ zoom / enter
Galaxy
  ↓ zoom
Secondary knowledge
  ↓ inspect
Single-node explanation
```

Rules:

- large-scale action may move the camera
- small-scale inspection should not recenter the camera
- zooming out peels semantic layers away
- zoom-out should not automatically recenter the universe
- explicit recentering belongs to a separate action, potentially the Identity Core
- product surface should not require permanent instructional chrome

---

## 17. Explainability contract

A node detail view should be able to answer:

1. What can currently be seen?
2. What is still unresolved?
3. Why does this node have its current state?
4. Where does the evidence stop?
5. What evidence supports it?
6. What new evidence would improve resolution?

Explainability may live in a deeper inspector layer.  
It should not dominate the initial universe view.

---

# Part D — Generation Responsibilities

## 18. What the model-generating agent should do

The agent may:

- inspect sources
- normalize evidence
- model attribution
- create bounded claims
- create / merge / remove nodes
- infer Anchors
- infer evidence-backed relations
- form Galaxies
- perform distillation
- generate Visual DNA
- output Scene Spec

The agent must not:

- invent personal capability to complete a taxonomy
- use visual importance as proof of skill
- create personal relations only because two technologies are generally related
- rewrite the renderer from scratch to make a single output “creative”

---

## 19. What the renderer should do

Given valid Scene Spec:

- produce a visually coherent constellation
- preserve the global design language
- introduce deterministic diversity
- make uncertainty visually quieter / less resolved
- reveal detail progressively
- keep first impression universe-first
- preserve spatial context during inspection

---

# Part E — Minimal v1 Validation

A v1 implementation is acceptable only if:

### Recognition

- every visible primary node can trace back to evidence
- unknowns remain unknown
- artifact / participation inflation tests pass
- passive-only output remains useful without calibration

### Structure

- Galaxy names describe the person, not a syllabus
- low-representativeness technical details can be pushed to deeper layers
- deleting secondary nodes does not materially change the person's first-screen silhouette

### Visual

- first screen reads as a universe before it reads as a dashboard
- different model structures can produce different global silhouettes
- the same model snapshot is deterministic
- entering a Galaxy reveals more structure
- inspecting a small node does not steal the camera
- zooming out restores semantic context without forced recentering
- evidence / confidence language does not leak into the first screen

---

# 20. Canonical principle

The whole system should preserve this invariant:

> **Same person, different resolution.**

At every scale, it is still the same model:

- far away: personal silhouette
- closer: recurring themes
- inside a Galaxy: concrete knowledge and practice
- close up: evidence, uncertainty and boundaries

The product succeeds when:

> **远看是作品，近看是工具。**