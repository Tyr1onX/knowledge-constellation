# Repository Checkpoint Cadence

Knowledge Constellation is being developed through fast visual and modeling iteration.  
The repository should preserve **decisions and usable checkpoints**, not every experiment.

## 1. Default workflow

```text
explore locally / in temporary artifacts
        ↓
compare several iterations
        ↓
a direction is accepted
        ↓
consolidate related changes
        ↓
one meaningful repository checkpoint
```

The repository is not a frame-by-frame recording of the conversation.

---

## 2. When a checkpoint is worth pushing

Push when at least one of these is true:

### Accepted product baseline

A visual / interaction direction has survived several iterations and is now the new baseline.

Examples:

- d3-force replacing custom physics
- universe-first presentation
- Semantic Zoom becoming the navigation model
- Identity Core becoming part of the product language

### Interface contract changes

A stable boundary between subsystems has been defined.

Examples:

- Knowledge Model → Scene Spec → Renderer
- Evidence / Claim / Node schemas
- Visual DNA contract

### Research conclusion changes future work

A finding is general enough that future contributors should not have to rediscover it.

Examples:

- participation is not execution evidence
- generated raster star sprites are not the preferred renderer path
- small-node inspection should not recenter the camera

### Handoff / branch milestone

The branch is about to change focus, be reviewed, or be handed to another agent/contributor.

---

## 3. What should usually stay out of Git history

Do not push merely because:

- a halo alpha changed
- one star became 2 px smaller
- a temporary V-number was generated
- a rejected visual experiment exists
- a short-lived instruction string changed
- an experiment is likely to be replaced within the same session

Rejected experiments may still be summarized in `docs/research-notes.md` if the lesson is reusable.

---

## 4. Bundling rule

Prefer one checkpoint that groups a coherent idea.

Good:

```text
model: define model-to-renderer contract and sync accepted prototype
```

Less useful:

```text
tweak star
tweak star again
remove hint
change zoom
fix zoom
change label
```

A checkpoint may include:

- the stable prototype
- the spec it implements
- documentation of the general design decision

when those files represent the same milestone.

---

## 5. Prototype policy

`prototype/index.html` should represent the **current accepted interaction baseline**, not the newest experiment.

Temporary experimental versions may remain outside the repository until accepted.

When a later prototype clearly supersedes the current baseline, replace `prototype/index.html` in the next meaningful checkpoint.

---

## 6. Branch / PR policy for current research

Current research work stays on:

`research/v0-knowledge-model`

Do not create a PR for every checkpoint.

A PR becomes appropriate when:

- the research branch has a coherent reviewable milestone
- the recognition and rendering contracts are internally consistent
- the prototype demonstrates the intended contract
- the user explicitly wants to move the work toward `main`

---

## 7. Practical rule

Before publishing a checkpoint, ask:

> If we stop working for a week and return later, is this state worth recovering exactly?

If yes, it probably belongs in Git.

If no, keep iterating first.