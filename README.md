# Knowledge Constellation

> An evidence-driven personal knowledge constellation.

Knowledge Constellation explores a simple but difficult question:

> Given the traces currently available, what are we justified in believing about a person's knowledge and practice?

The project aims to turn resumes, GitHub activity, learning records, projects, and other existing artifacts into a conservative but meaningful personal knowledge map — without pretending that an artifact automatically proves mastery.

## Current status

This repository is in the **V0 research stage**.

The current goal is not to ship a polished Skill yet. It is to validate the recognition protocol underneath it:

```text
Source
  ↓
Evidence
  ↓
Claim
  ↓
Knowledge Node
  ↓
Constellation
```

The first experiment uses passive evidence only: no mandatory interview, no long questionnaire, and no attempt to fill missing information with optimistic guesses.

## Core ideas

- **Evidence before inference** — conclusions must be traceable to observable evidence.
- **Artifact ≠ mastery** — a repository using a technology does not prove independent capability in that technology.
- **Attribution matters** — AI-assisted and collaborative work makes authorship and contribution depth a first-class problem.
- **Unknown is valid** — uncertainty should be represented instead of silently completed.
- **Exposure ≠ capability** — repeated contact with a technology and demonstrated independent ability are different signals.
- **Passive first** — the user should be able to get a useful first result from existing materials with minimal effort.
- **Progressive resolution** — optional micro-calibration and adaptive questions can later make the constellation more precise.
- **The person is the subject** — this is not a completion percentage against a universal curriculum.

## Repository structure

```text
knowledge-constellation/
├─ README.md
├─ SKILL.md
├─ docs/
│  ├─ principles.md
│  ├─ v0-knowledge-model.md
│  └─ research-notes.md
└─ examples/
   └─ tyr1onx/
      ├─ evidence.md
      └─ model.yaml
```

## First case study

The first V0 case uses public GitHub traces from `Tyr1onX` only.

The experiment deliberately avoids private conversation history and additional self-report so that we can test the limits of passive evidence.

A key expected outcome is that some technologies may appear as **observed** because they clearly exist in the person's project history, while independent capability remains unresolved.

See:

- [`examples/tyr1onx/evidence.md`](examples/tyr1onx/evidence.md)
- [`examples/tyr1onx/model.yaml`](examples/tyr1onx/model.yaml)

## Roadmap

### V0 — Passive constellation

Existing evidence → conservative model → first constellation.

### V0.1 — Explainability

Every visible node can explain why it exists and where the evidence stops.

### V0.2 — Micro calibration

A few low-cost multiple-choice questions improve attribution and resolution after the first result already exists.

### V0.3 — Adaptive calibration

A small number of high-information questions or tasks verify important uncertain areas.

### Later — Longitudinal constellation

Repeated evidence allows the constellation to change over time and reflect growth, fading knowledge, and new directions.

## Design principle

The first version does not need to know the whole person.

It needs to do something narrower and more defensible:

> Build a useful picture from incomplete evidence without pretending to know more than the evidence supports.
