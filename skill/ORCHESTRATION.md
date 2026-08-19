# Orchestration Contract

```text
INGEST
  ↓
PASS_A_EVIDENCE
  ↓ validate
  ├─ invalid → REPAIR_A → validate
  └─ valid
  ↓
PASS_B_MODEL
  ↓ validate
  ├─ invalid → REPAIR_B → validate
  └─ valid
  ↓
PASS_C_STRUCTURE
  ↓ validate
  ├─ invalid → REPAIR_C → validate
  └─ valid
  ↓
PASS_D_VISUAL
  ↓ validate
  ├─ invalid → REPAIR_D → validate
  └─ valid
  ↓
DETERMINISTIC_SCENE_COMPOSER
  ↓
RENDER
```

The harness MUST NOT fill rejected semantic fields itself.

Bad:
```text
Codex omitted a Rust node
→ harness sees Rust in README
→ harness creates Rust node
```

Correct:
```text
Codex output fails validation
→ harness reports exact failure
→ Codex rereads accepted upstream artifacts and repairs its output
```

Recommended retry budget: at most 2 repair attempts per pass. If still invalid, preserve the last valid upstream artifact and return a structured failure instead of manufacturing content.

## Calibration loop

After a user has seen an accepted result, natural-language corrections or representativeness feedback must enter as new Source evidence rather than as direct edits to semantic or visual artifacts.

```text
COMPLETED_RUN
  + user feedback
  ↓
APPEND kind=user_calibration SOURCE
  ↓
NEW PASS_A_EVIDENCE
  ↓
PASS_B_MODEL → PASS_C_STRUCTURE → PASS_D_VISUAL
  ↓
DETERMINISTIC_SCENE_COMPOSER
  ↓
RENDER NEW REVISION
```

Use `harness/recalibrate.py` to create this revision when the repository runtime is available. It starts from the prior run's accepted `input.json`, appends the subject's feedback as a first-party Source, then launches a fresh E2E run. It must never patch the previous accepted Model, Structure, Visual Model, or Scene in place.

Truth corrections and identity/representativeness corrections are semantically different: feedback such as “AI did this part” may constrain attribution and capability Claims; feedback such as “this project matters more to me” may change representativeness and display priority but cannot upgrade capability truth.

## Gold isolation

Test-only baselines may exist under `tests/baselines/`, but they are forbidden runtime inputs. The Codex execution packet must never include or reference them. They are used only after a completed run for external acceptance comparison.

## Isolated pass workspace

For each semantic pass, the harness materializes a new workspace that contains only the files that pass may read. A normal generation workspace contains the root `SKILL.md`, this orchestration contract, the current prompt, the current schema, and the accepted upstream JSON required by that pass. Repair workspaces may additionally contain the rejected previous candidate and validation errors.

Codex writes `output.json` in that workspace. The harness copies that output into the candidate slot and validates it. Historical examples, test expectations, gold baselines, and other-subject fixtures are not semantic inputs.
