# External Auditor — source-only notes

Case: `2026-08-18-devdanzin-02`
Runner freeze: `2e45297e362d7cc7b370a64ea3e455d2b40a2ae0`
Isolation level: **emulated**

> Regression audit reuses the same frozen source-only interpretation as case 01. The source scope did not change; only the Recognition contracts changed.

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

The strongest personal structure remains:

```text
CPython reliability
    ↓
fuzzing → reproducing → verifying → reporting upstream
    ↘
     tool-building (lafleur / labeille / fusil)
```

AI assistance is a cross-cutting working mode. The broader goal “Python ecosystem reliability” is a cross-cutting motif unless more independently sampled ecosystem evidence is collected.
