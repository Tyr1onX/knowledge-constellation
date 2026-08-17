# Knowledge Constellation Skill Harness v0.3

Knowledge Constellation is a **Skill-first** system.

The semantic engine is Codex executing the repository-root `SKILL.md`.
The Python harness is deliberately incapable of deciding what a person knows.

## Responsibility boundary

```text
Codex owns
  Source interpretation
  Evidence extraction
  Attribution reasoning
  Claims
  Knowledge Nodes
  Anchors / Relations / Galaxies
  Distillation
  Personal Visual Model

Harness owns
  input packaging
  stage orchestration
  JSON contracts
  semantic invariant validation
  repair-loop bookkeeping
  persistence
  regression tests
  deterministic renderer handoff

Renderer owns
  exact coordinates
  palette mechanics
  d3-force / Canvas behavior
  semantic zoom
  star rendering
  identity core rendering
  product surface
```

If Python starts creating nodes through keyword matching, the architecture has regressed.

## Runtime state machine

```text
input.json
   ↓
Pass A — Codex → evidence.json
   ↓ validator
   ├─ reject → Codex repair
   └─ accept
   ↓
Pass B — Codex → model.json
   ↓ validator
   ├─ reject → Codex repair
   └─ accept
   ↓
Pass C — Codex → structure.json
   ↓ validator
   ├─ reject → Codex repair
   └─ accept
   ↓
Pass D — Codex → visual.json
   ↓ validator
   ├─ reject → Codex repair
   └─ accept
   ↓
deterministic Scene Composer
   ↓
Renderer
```

The default repair budget is two attempts per semantic pass. After that, the run fails explicitly instead of manufacturing an answer.

## How Codex drives the harness

Initialize a run:

```bash
python harness/pipeline.py init \
  --input fixtures/tyr1onx-public.json \
  --run runs/tyr1onx
```

Ask the harness for the next Codex packet:

```bash
python harness/pipeline.py next --run runs/tyr1onx
```

The packet contains only the current Skill contract, pass prompt, schema, accepted upstream artifacts, an isolated workspace, and repair errors when relevant. The runtime contract excludes `tests/`, `examples/`, and other `fixtures/` from semantic input.

Codex writes `output.json` inside the isolated workspace. The harness ingests and validates that file; it never synthesizes a semantic replacement.

After all four passes are accepted, `pipeline.py render` creates the renderer handoff through a deterministic Scene Composer.

## Safety invariants

The validator checks source provenance, evidence boundaries, Claim and Node references, explicit unknowns and boundaries, strong-claim evidence independence, relation evidence, exclusive Galaxy/display membership, anti-syllabus Galaxy names, Recognition/Visual separation, and renderer semantic preservation.

## v0.3 unseen evaluation

Four public unseen-style cases were evaluated with expectations applied only after semantic generation: a Tauri/Java proof-of-concept, a current React learner, an Android tooling learning journey, and a detailed professional engineering resume. Current guards pass across all four cases and produce multiple distinct global composition archetypes.

This is not a universal accuracy score for people; human calibration remains important for subjective representativeness and facts unavailable in public evidence.
