# Clean-room real-user evals

这里保存当前 Recognition 回归需要的真人隔离评测。`main` 只保留**仍参与当前 gate 的 accepted / replayable case**；已经被后续 rerun 取代的中间版本留在 Git 历史中，不继续占据当前树。

每个 case 的基本结构：

```text
cases/<case-id>/
  metadata.json
  source-manifest.json
  runner/
    pass-a.json
    pass-b.json
    pass-c.json
    pass-d.json
    validation-proof.json
  audit/
    source-only-notes.md
    comparison.md
    verdict.json
```

完整方法见 [`../../docs/clean-room-evaluation.md`](../../docs/clean-room-evaluation.md)，可执行规则见 [`protocol-v2.md`](protocol-v2.md)。

## 当前 gate

[`milestone-10-user.json`](milestone-10-user.json) 是 Recognition Hardening 的 accepted 10-user baseline。CI / regression 只应把其中列出的 case 当作这一里程碑的正式集合。

验证单个 v2 case：

```bash
python harness/verify_eval_case.py evals/clean-room/cases/<case-id>
```

## 隔离纪律

- Runner 只读取当前 Skill、当前 Pass prompt/schema、允许的 upstream output 与 frozen sources；
- Runner 不得读取其他人的 case、历史 verdict、Auditor notes、tests 或 expected；
- Auditor 尽量先基于 frozen sources 形成 source-only notes，再看 Runner 输出；
- 同会话模拟必须标记 `emulated`，真正独立进程 / 新会话才标记 `independent`；
- 规则修复应产生新的 rerun，并通过回归证明没有把旧案例改坏；
- superseded / failed run 依然可由 Git 历史追溯，但不需要永久堆在 `main`。
