# External Auditor — source-only notes

Case: `2026-08-18-devdanzin-01`
Runner freeze: `6f3252a438399c9c7048c62d5e3e8147d6a500a2`
Isolation level: **emulated**

> Limitation: this is not a truly blind independent-process audit. The Runner was frozen before this comparison stage, but the same model/session is acting as Auditor. These notes therefore test the workflow and adversarial criteria, not independence itself.

## Strongly supported from the frozen sources

- A sustained **CPython/Python reliability and bug-finding** theme is real and highly representative.
- `lafleur` and `labeille` form a concrete fuzzing/testing toolchain; `fusil` is explicitly a revival/maintenance lineage rather than original authorship.
- Reproduction, re-running, source checking, triage and upstream issue reporting recur across multiple independent public artifacts.
- CPython JIT, free-threaded CPython/TSan, and OOM/error-path testing are real recurring contexts.
- Upstream collaboration is behavior-proximal: the snapshot contains subject-authored `python/cpython` issues rather than only self-description.
- AI assistance is extensive and explicitly disclosed.

## Supported, but must stay bounded

- **CPython C-internals understanding:** source-level investigation is repeatedly visible, but this snapshot does not establish broad independent C implementation capability.
- **Fuzzing-tool implementation:** author/maintainer evidence is meaningful, but individual subsystem authorship and the role of coding agents are not separated.
- **Root-cause judgment:** human source checking and re-verification are explicitly documented; independent first-pass derivation is not consistently separable from Claude Code.
- **Python ecosystem breadth:** profile/campaign data suggests breadth, but non-CPython projects were not independently sampled in this frozen snapshot.

## Must not infer

- original authorship of fusil;
- Rust mastery from RustPython/review repositories;
- broad C mastery from CPython bug investigation;
- independent authorship of every reducer, report, root-cause writeup or catalog tool;
- authorship of linked CPython fixes merely because an issue links PRs;
- “464 bugs independently found by the human” from the catalog headline;
- broad security or compiler expertise beyond the evidenced contexts.

## Personal structure

The strongest personal structure is not a standard `Python / C / Testing / GitHub` taxonomy. It is:

```text
CPython reliability
    ↓
fuzzing → reproducing → verifying → reporting upstream
    ↘
     tool-building (lafleur / labeille / fusil)
```

AI-assisted review is a **cross-cutting working mode** inside this structure. It is important provenance, but it does not obviously deserve a separate Galaxy by itself.

The broader goal “Python ecosystem reliability” is also cross-cutting. It may be a high-level motif or distillation statement rather than a standalone cluster unless more independently sampled non-CPython evidence is collected.
