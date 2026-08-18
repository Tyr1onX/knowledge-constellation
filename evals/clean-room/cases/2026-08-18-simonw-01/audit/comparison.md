# External Audit comparison — simonw 01

Case: `2026-08-18-simonw-01`

## Overall

The semantic direction is reasonable, but this run cannot count as an accepted clean-room result because the stored Pass outputs do not match the active contracts and were not proven by the Harness validator.

Observed contract mismatches include: Pass B omits canonical top-level Claims and unresolved output and uses a non-contract node state; Pass C emits non-contract relation and Motif kinds; one node is assigned to two Galaxies; and the validation log is prose rather than machine validator output.

The source-only audit still supports the intended silhouette: durable independent developer tools, SQLite/data publishing workflows, LLM developer tooling, plugin-oriented extensibility, and long-lived maintenance. Attribution hardening is therefore not obviously over-conservative. The issue here is eval integrity, not capability inflation.

## Verdict

`FAIL` — protocol / validation integrity failure.

## Generalized fix

A clean-room case only counts when every stored Pass artifact validates against the recorded active schemas and semantic validator. Prose validation notes are supplemental only. Canonical Pass shapes are required, and a failed historical run must be rerun as a new case rather than edited into compliance after audit.
