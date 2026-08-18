# External Audit comparison — regression 02

Case: `2026-08-18-devdanzin-02`
Runner freeze: `2e45297e362d7cc7b370a64ea3e455d2b40a2ae0`

## Overall

The first-round warnings were substantially reduced without changing the frozen source scope. The rerun preserves the same dominant personal silhouette while improving attribution and structure.

No `critical_inflation`, `dependency_to_mastery`, `taxonomy_galaxy`, unsupported trajectory, or Anchor handoff gap was found.

The remaining issue is narrower: one implementation claim does not cite the available authorship/role evidence that would justify using the stronger `implementation` dimension.

## Findings

| Category | Finding | Severity |
| --- | --- | --- |
| `critical_inflation` | None found. | none |
| `dependency_to_mastery` | None found. Rust/RustPython remains unresolved. | none |
| `attribution_error` | The former `崩溃复现与最小化` issue is fixed: the human-facing node is now `崩溃复现与验证`, while AI-assisted reduction/drafting is preserved as a Motif/boundary. | none |
| `learning_state_error` | None found. | none |
| `important_omission` | No major omission inside the frozen scope. Older/non-CPython history remains intentionally under-resolved rather than guessed. | none |
| `anchor_error` | The two Anchors are coherent experiential sources and their node membership matches their scope. | none |
| `taxonomy_galaxy` | Fixed. AI assistance and ecosystem reliability are Motifs; only two experiential Galaxies remain. | none |
| `unsupported_relation` | Fixed. No trajectory relation is emitted without time evidence. | none |
| `over_distillation` | None. Specialized free-threading/OOM/C-internals nodes remain secondary. | none |
| `under_distillation` | None material. First layer is dominated by behavior streams rather than provenance labels. | none |
| `claim_provenance_gap` | `C8 / N8 Python 包测试与兼容性编排` uses the `implementation` dimension but cites only `E4`, the project-behavior README observation. The frozen evidence also contains `E2`, which is the actual author/maintainer-role evidence for labeille. Stronger action dimensions should cite both behavior evidence and the attribution/role evidence when those are separate observations. | medium |

## Cross-layer check

The previous Pass C → Pass D gap is fixed in the contract and in this rerun:

- both Structure Anchors appear exactly once in `visual.anchors`;
- their Galaxy membership follows accepted node ownership;
- Identity Presence is now a formal Visual Model field;
- `identity.label` is sourced from the frozen input identity rather than reconstructed downstream.

## General rule suggested by the remaining warning

When a Claim uses an action-bearing dimension such as `implementation`, `debugging/troubleshooting`, `review`, or `validation`, distinguish two questions:

1. **Did this behavior/artifact exist?**
2. **What evidence attributes that behavior to the person?**

If those answers live in separate Evidence objects, the Claim should cite both. A rich project README can describe a system, but the stronger action Claim should not silently borrow authorship from elsewhere without listing the attribution evidence.

This is a general provenance rule, not a devdanzin-specific exception.
