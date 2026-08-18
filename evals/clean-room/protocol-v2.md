# Clean-room Protocol v2 — executable eval integrity

A real-user clean-room case counts toward Recognition Hardening only when its persisted Runner artifacts are executable-contract valid.

## Counted case requirements

A counted case must declare in `metadata.json`:

```json
{
  "protocol_version": "kc.cleanroom.v2",
  "validation_mode": "harness"
}
```

and persist canonical:

```text
source-manifest.json
runner/pass-a.json
runner/pass-b.json
runner/pass-c.json
runner/pass-d.json
runner/validation-proof.json
```

`validation-proof.json` is machine evidence that the same persisted files passed the active schema + semantic validator. A prose validation summary may still exist for humans, but it never replaces machine validation.

## Integrity rule

Before External Audit, run:

```bash
python harness/verify_eval_case.py evals/clean-room/cases/<case>
```

The case is Runner-frozen only if this returns success. If contract verification fails, record a protocol failure and rerun as a new case after fixing the generalized evaluation process. Do not edit a failed Runner into compliance after seeing the Auditor result.

## Why this exists

The eval loop tests the Skill, but the eval loop itself can fail. A plausible semantic summary is not a valid Pass output. Without executable verification, the project can accidentally reward an output that no real Harness run would accept.

## Historical cases

Older `kc.cleanroom.v1` / unversioned cases remain evidence of development history. They may be useful for qualitative regression, but they do not satisfy the v2 ten-user milestone unless rerun under v2.

## Anti-overfitting rule

A fix triggered by one person must be stated as a general evidence, attribution, structure, distillation, visual-contract, or eval-integrity rule. The same change must be regression-checked against previously saturated cases before the target is considered resolved.
