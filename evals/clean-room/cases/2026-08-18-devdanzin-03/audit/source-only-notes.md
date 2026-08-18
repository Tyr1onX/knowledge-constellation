# External Auditor — source-only notes

Case: `2026-08-18-devdanzin-03`
Runner freeze: `0fe392acd55007668e2e587295d4c1d9a63e1ef7`
Isolation level: **emulated**

The frozen source interpretation is unchanged from cases 01/02. The audit therefore attacks only whether the v3 Runner still respects that source-only boundary after introducing explicit action attribution.

## Source-grounded silhouette

- Sustained CPython robustness / bug-finding / upstream-reporting activity is highly representative.
- `lafleur` / `labeille` are author-maintainer tool contexts; `fusil` is maintenance/revival with explicit upstream lineage.
- Human re-reproduction, re-verification and source checking are explicitly preserved in multiple AI-assisted campaigns.
- AI assistance is substantial in reduction, drafting, candidate generation and parts of tooling.
- CPython JIT, free-threaded/TSan and OOM paths are recurring testing contexts.

## Boundaries that must remain

- no original fusil authorship;
- no Rust mastery from RustPython targets/repositories;
- no broad C mastery from CPython source investigation;
- no automatic authorship of linked upstream fixes;
- no assumption that every reducer, root-cause draft or analysis agent output was independently produced by the human;
- no requirement to turn AI assistance itself into a Knowledge Star or Galaxy.
