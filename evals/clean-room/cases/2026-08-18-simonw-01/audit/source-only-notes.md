# External Auditor — source-only notes

Case: `2026-08-18-simonw-01`

> Notes were formulated from `source-manifest.json` before Runner comparison. During persistence, fetching the current main commit exposed the Runner summary in the commit patch before these notes were committed, so this audit is marked **emulated / imperfect separation** rather than truly blind.

## Strongly supported from the frozen sources

- A long-running **independent tool/product author-maintainer** pattern is strongly supported at project level across Datasette, sqlite-utils and LLM.
- The most representative recurring themes are not generic language/framework categories. They are durable developer/data tools, SQLite-centered data workflows, and model/LLM tooling with plugin-oriented extensibility.
- `sqlite-utils` has direct recent maintainer-history evidence in August 2026, so implementation/maintenance claims can be stronger there than a README-only artifact claim.
- Datasette is a durable open-source product ecosystem with plugins, publishing workflows and a large historical surface. This supports sustained product stewardship, not sole authorship of every contribution.
- LLM is a durable CLI/library product with multiple providers, logging, embeddings, schemas, tools, attachments and plugins. This supports model-tooling product design and maintenance, not mastery of every model provider.

## Supported but must remain bounded

- **Independent implementation:** strong at project level for owned, long-maintained projects, especially where maintainer history is present; do not convert this into sole authorship of all code.
- **SQLite expertise:** strong tooling/product practice around SQLite is supported, but database-engine internals mastery is not.
- **LLM engineering:** strong tooling/integration/product practice is supported, but model-training/research capability is not implied.
- **Plugin architecture:** recurring product-level extensibility is visible across Datasette/LLM/sqlite-utils, but should be expressed as a cross-project practice only if distinct project evidence supports it.

## Must not infer

- sole authorship of every line, merged contribution or plugin;
- mastery of every LLM provider/backend exposed by `LLM`;
- SQLite engine internals expertise from SQLite tooling alone;
- AI-generated implementation merely because one project is named `LLM`;
- generic “full-stack”, “backend”, “database”, or “AI engineer” identity when more personal project-centered structure is available.

## Expected personal structure

```text
Durable independent developer tools
    ├─ Datasette / data publishing & exploration
    ├─ sqlite-utils / SQLite manipulation & workflow tooling
    └─ LLM / model interaction, logging, tools & plugins

Cross-cutting practices:
    plugin-oriented extensibility
    CLI + Python library product design
    long-lived open-source maintenance
```

Cross-cutting practices should not automatically force an extra Galaxy if the project-centered structure already explains the person well.

## Over-conservatism test

This case counterbalances the AI-assisted devdanzin case. If attribution hardening prevents any meaningful `implementation` or independent-project author/maintainer claim here, the rules are too conservative. Correct behavior is bounded strength: strong project-level action attribution where ownership plus sustained maintainer evidence supports it, without claiming sole authorship of every subsystem.
