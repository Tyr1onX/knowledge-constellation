# Clean-room real-user evals

这里保存 Recognition Hardening 阶段的真实陌生用户隔离评测。

每个案例使用独立目录：

```text
cases/<case-id>/
  metadata.json
  source-manifest.json
  runner/
    pass-a.json
    pass-b.json
    pass-c.json
    pass-d.json
    validation-log.md
    runner-summary.md
  audit/
    source-only-notes.md
    comparison.md
    verdict.json
```

完整协议见 [`../../docs/clean-room-evaluation.md`](../../docs/clean-room-evaluation.md)。

## 纪律

- Runner 不得读取本目录的 Audit / expected / previous verdict；
- Auditor 理想上在看到 Runner 输出前先完成 source-only notes；
- Runner 与 Auditor 使用同一 frozen source snapshot；
- 不要求两边生成相同节点，只比较证据边界、代表性、归因、Anchor、Galaxy 与 Distillation；
- 同一会话模拟必须在 metadata 中写 `isolation_level: emulated`；
- 真正独立进程 / 新会话写 `isolation_level: independent`；
- 失败案例不删除，规则更新后追加 rerun。

第一轮目标不是追求漂亮分数，而是积累稳定失败模式。
