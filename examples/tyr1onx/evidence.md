# Tyr1onX Passive Evidence Sample

This is the first real V0 case study.

## Experiment constraint

This sample intentionally uses **public GitHub traces only**.

It does not use private conversation history, private self-report, or additional calibration answers. The purpose is to test how far a passive-first system can go without over-attributing capability.

Snapshot date: 2026-08-16.

---

## Sources

### S1 — GitHub profile repository README

https://github.com/Tyr1onX/Tyr1onX

Observed:

- highlights `desktop-course-widget`, `Tyr1onX.github.io`, and `accounting-excel-tool` as personal projects;
- states participation as an EGC collaborator;
- lists multiple merged pull requests in external repositories.

Interpretation boundary:

This is a curated public self-presentation. It is useful for discovering relevant artifacts, but claims should be corroborated by the linked repositories or external outcomes where possible.

---

### S2 — Desktop Course Widget

https://github.com/Tyr1onX/desktop-course-widget

Observed from the public README:

- a real Windows desktop course-schedule product exists;
- the documented stack includes Tauri 2, Rust, Vite, Vanilla TypeScript, HTML/CSS, and Calamine;
- the product includes Excel import, a screenshot/OCR development path, multi-schedule management, desktop integration, local persistence, testing commands, and release practices;
- the repository documents product limitations, privacy, testing, and development policy.

Attribution boundary:

Repository ownership and maintenance establish strong project association and technology exposure. They do not by themselves establish how much implementation was independently authored by the owner or how deeply each technology is understood.

---

### S3 — Learning repository

https://github.com/Tyr1onX/Learning

Observed:

- the repository explicitly tracks learning state instead of only completed artifacts;
- its status model distinguishes `not-started`, `learning`, `understood`, `review-needed`, and `interview-ready`;
- the public learning status records structured study of Web/network/browser topics;
- JavaScript/DOM is recorded as currently learning;
- several areas such as frameworks, backend, database, OS/Linux, and parts of algorithms are explicitly recorded as not yet systematically learned or needing review.

Attribution boundary:

This is structured learning evidence, not an independent examination. It supports deliberate study and self-tracked understanding, but stronger capability claims require corroboration or calibration.

---

### S4 — EGC PR #1271

https://github.com/Fmarzochi/EGC/pull/1271

Observed:

- the PR addressed exactly-once session event delivery across overlapping readers;
- the accepted change involved cursor compare-and-swap logic and a multi-process chaos harness using SQLite WAL;
- the maintainer explicitly confirmed the fix as correct and merged it with full credit;
- the maintainer described it as the contributor's 11th contribution.

Attribution boundary:

The PR is direct evidence of participation in a real accepted contribution and external validation of the delivered change. Public GitHub data alone does not establish whether the implementation was independently produced, heavily assisted, or how deeply the author can reproduce the underlying concurrency reasoning in a fresh setting.

---

### S5 — Other external pull requests

Examples visible from the public contribution history include work involving:

- EGC installation/integration behavior;
- dashboard regressions and polling/reconnect behavior;
- QQ Chat Exporter Windows/Linux compatibility, ESM startup behavior, scheduler validation, UI pagination, authentication documentation, and regression tests;
- Avenx custom HTTP headers support.

Interpretation boundary:

Repeated contribution activity supports an open-source workflow claim more strongly than any single PR. The technologies touched by those PRs should still default to exposure unless capability is independently supported.

---

# Normalized evidence records

## E1 — Sustained external contribution activity

```yaml
kind: activity
observation: Multiple external pull requests exist across more than one project, including merged contributions.
attribution: direct
confidence: high
```

Supports:

- open-source participation;
- GitHub / pull-request workflow exposure;
- repeated interaction with real project constraints.

Does not prove:

- independent implementation of every accepted change;
- mastery of every technology involved.

---

## E2 — Maintainer validation of EGC #1271

```yaml
kind: external_validation
observation: The maintainer confirmed the exactly-once fix as correct, merged it with full credit, and identified it as the contributor's 11th contribution.
attribution: external
confidence: high
```

Supports:

- a real contribution reached external acceptance;
- sustained contribution history is not merely a local/private artifact.

Does not prove:

- independent mastery of concurrency, CAS, or SQLite WAL.

---

## E3 — Repeated test and regression language in contributions

```yaml
kind: activity
observation: Multiple public PR descriptions include regression tests, CI validation, edge cases, or real-environment verification.
attribution: direct
confidence: high
```

Supports cautiously:

- repeated exposure to testing/validation workflows;
- testing and regression are structurally present in the person's engineering activity.

Unresolved:

- how independently tests are designed and implemented;
- depth of testing theory.

---

## E4 — Complex desktop product exists and is actively specified

```yaml
kind: artifact
observation: A maintained Windows desktop course-schedule product documents a multi-language stack, import flows, desktop behavior, local data handling, testing, privacy, releases, and current limitations.
attribution: uncertain
confidence: high
```

Supports:

- product/project exposure;
- repeated contact with Tauri, Rust, TypeScript, Windows desktop concerns, Excel parsing, and OCR-related work.

Does not prove:

- independent implementation capability in any of those technologies.

---

## E5 — Structured Web/network/browser learning record

```yaml
kind: learning_record
observation: The public learning repository records multiple Web/network/browser topics as understood while retaining explicit weak and not-started areas.
attribution: direct
confidence: high
```

Supports cautiously:

- deliberate learning in Web/network/browser fundamentals;
- a developing knowledge structure with explicit boundaries.

Does not prove:

- durable recall under fresh testing;
- professional-level depth.

---

## E6 — JavaScript/DOM currently learning

```yaml
kind: learning_record
observation: JavaScript language basics and DOM concepts are explicitly recorded as learning rather than established.
attribution: direct
confidence: high
```

Supports:

- JavaScript and DOM belong in the current constellation;
- they should not be represented as established capability.

---

# What passive evidence cannot currently answer

The public evidence does not reliably answer:

- how much code in personal or external projects was produced independently;
- the degree of AI assistance;
- whether the user can reproduce project-level reasoning without tools;
- how deeply Rust, TypeScript, Tauri, concurrency, SQLite, or platform internals are understood;
- whether public learning-state labels remain stable after time has passed.

These unknowns are not model failures. They are part of the V0 output and potential targets for later micro-calibration.
