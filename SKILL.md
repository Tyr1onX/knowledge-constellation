# Knowledge Constellation Skill

## Purpose

Turn incomplete user-provided or public materials into an evidence-grounded, explainable, visually externalizable personal knowledge universe.

The system has two goals:
1. Recognize the person truthfully.
2. Externalize that recognition beautifully.

The first goal must never be weakened for visual drama.

## Architecture boundary

You are the semantic engine.

The harness around you may:
- gather and normalize input containers;
- provide schemas;
- validate structured outputs;
- reject unsupported or malformed outputs;
- ask you to repair them;
- run regression tests;
- pass the accepted result to a renderer.

The harness must NOT decide what the person knows by keyword matching.

You must perform the semantic work:

```text
Raw Input
→ Source
→ Evidence
→ Attribution
→ Claim
→ Knowledge Node
→ Anchor
→ Relation
→ Motif / Galaxy
→ Distillation
→ Personal Visual Model
→ deterministic Scene Composer
→ Scene Spec
```

Never regenerate the renderer from scratch for each user.

## Canonical principles

### Evidence before inference
Do not create a personal fact because two technologies are generally related.

### Artifact is not mastery
A repository using Rust does not prove independent Rust ability.

### Participation is not execution
A merged PR does not by itself prove independent analysis, implementation, testing, or debugging.

### Assistance is not erasure
AI or collaborator assistance does not erase supported human roles such as selecting, specifying, judging, validating, authorizing, operating, reviewing, or explaining.

### Attribution must survive compression
Do not merge two activities into one public-facing node label when their attribution differs enough to change what the label implies about the human. If evidence strongly supports human reproduction/verification but reduction or drafting is explicitly AI-assisted, prefer a label such as `reproduction and verification`; keep reduction/drafting as mixed-attribution evidence, a bounded claim, or a cross-cutting motif unless separately supported.

For action-bearing Claims (`implementation`, `independence`, `judgment`, `troubleshooting`, `participation`, `transfer`), explicitly identify which cited Evidence attributes the action to the person. Evidence that merely describes an artifact may support that the behavior/system exists, but must not silently borrow authorship from another observation.

### Working mode is not automatically knowledge
AI-assisted, collaborative, generated, templated, or automated are provenance/work-mode facts. They may shape attribution or become a cross-cutting Motif, but should not become a Knowledge Node or Galaxy merely because the mode recurs.

### Dependency is provenance, not personal knowledge
A dependency, generated file, or template may exist without meaningful human exposure.

### Unknown is valid output
Absence of evidence is not negative evidence.

### Stronger claims need stronger evidence
Implementation, independence, troubleshooting, and transfer need stronger, more behavior-proximal, and more independent evidence than exposure claims.

### Representativeness is not capability
A technology can strongly represent the person's current work while independent capability remains unresolved.

### Galaxy is a personal theme, not a syllabus category
Prefer a real project, recurring contribution stream, learning trajectory, long-running goal, or repeated context. Avoid default Frontend / Backend / Database buckets unless the person's evidence genuinely forms them.

A Galaxy does **not** need multiple Knowledge Nodes merely to look substantial. Multi-node Galaxies are preferred when the evidence really forms a cluster, but a one-node Galaxy is valid for an isolated, representative experience/theme. Never fabricate a companion node, merge unrelated Anchors, or invent an umbrella theme to satisfy layout or schema shape.

### Cross-cutting Motif is allowed
Not every important idea should own a Galaxy. A repeated goal, provenance pattern, working mode, or cross-cutting theme may be represented as a Motif that references existing nodes without becoming a Knowledge Star or forcing unrelated nodes into a synthetic cluster.

### Trajectory requires time evidence
Use a `trajectory` Relation only when the allowed sources establish an ordered change: dated earlier/later evidence, an explicit migration, first/last occurrence, or another source-grounded temporal basis. Semantic plausibility is not chronology. Without temporal evidence, use another supported relation kind or omit the relation.

## Pass A — Evidence
Read only the Source inputs. Produce normalized Evidence objects. Each must state what was observed, source provenance, confidence, attribution resolution, what it supports, what it does not support, and correlation group when needed. Do not create Knowledge Nodes in this pass.

## Pass B — Claims and Nodes
Read accepted Evidence. Create bounded, dimension-specific Claims, then Knowledge Nodes. Possible dimensions: exposure, understanding, implementation, independence, judgment, troubleshooting, transfer, participation, learning-state, recency, representativeness. Preserve known, unknown, boundary, evidence, confidence, resolution, and representativeness. Do not complete a taxonomy. Node labels themselves are claims about what belongs to the person: do not hide a mixed human/agent attribution problem inside an over-broad label. For action-bearing Claims, `attribution_evidence` must name the cited Evidence that justifies assigning the action to the person.

## Pass C — Structure and Distillation
Create Anchors, evidence-backed Relations, optional cross-cutting Motifs, Galaxies, and primary / secondary layers. Use the removal test: if removing a node barely changes who this looks like, it probably belongs deeper. One primary Galaxy per accepted Knowledge Node; Motifs do not own nodes and may cross Galaxies. A truthful one-node Galaxy is allowed when no second node is justified. A `trajectory` Relation must carry explicit temporal evidence.

## Pass D — Personal Visual Model
Translate the accepted input identity, Recognition Model, and Structure into visual semantics such as composition archetype, identity core family, identity presence, Galaxy mass, Anchor presence, asymmetry, openness, field density, dust morphology, motion temperament, presence, resolution, and activity. Preserve every accepted Structure Anchor as visual provenance; do not recreate or rename Anchor semantics in this pass. Do not output raw CSS or rewrite renderer implementation. Visual importance must not upgrade capability truth.

## Scene composition and rendering
After Pass D is accepted, the deterministic Scene Composer maps the accepted Recognition Model, Structure, and Personal Visual Model into the renderer contract.

The Scene Composer may choose exact coordinates, palette values, force parameters, and other rendering mechanics. It must not invent new personal claims, nodes, evidence, Anchor semantics, or Galaxy semantics.

Codex owns semantic visual choices. The renderer stack owns exact presentation mechanics.

## Calibration
The first passive result must be useful without asking questions. Optional later calibration is split into:
1. Truth Calibration — who did what, independence, understanding.
2. Identity Calibration — what feels most representative.
Identity Calibration may alter representativeness and display priority, but must not upgrade capability Claims.

## Product language
Internal ids such as S2, E4, or C-rust-exposure are valid for audit files but should not appear on the ordinary product surface.

## Repair behavior
When the harness rejects an output, read the validation errors and repair only invalid or unsupported parts. Preserve valid upstream artifacts when possible. Never weaken truth constraints merely to satisfy shape or size expectations.

The harness is a guardrail, not a second semantic model.

## Final invariant
Same person, different resolution.

```text
far away       → personal silhouette
closer         → recurring themes
inside Galaxy  → concrete knowledge and practice
close up       → evidence, uncertainty and boundaries
```

远看是作品，近看是工具。
