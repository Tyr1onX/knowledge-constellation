# Evals｜Recognition 回归

这里保留当前仍有效的 **clean-room real-user evaluation**。早期 synthetic case 和 round report 已完成方法探索，不再作为当前主评测入口；需要时可从 Git 历史恢复。

## 当前协议

```text
Frozen raw sources
    ↓
Clean-room Runner
    ↓
Pass A / B / C / D
    ↓ Harness validation

同一份 frozen sources
    ↓
External Auditor
    ↓
source-only judgment
    ↓
与 Runner 输出比较
```

正式规则见 [`../docs/clean-room-evaluation.md`](../docs/clean-room-evaluation.md) 和 [`clean-room/protocol-v2.md`](clean-room/protocol-v2.md)。

`kc.cleanroom.v2` case 必须拥有真实的 Pass A/B/C/D 文件，并能通过：

```bash
python harness/verify_eval_case.py evals/clean-room/cases/<case>
```

## 当前基线

- [`clean-room/milestone-10-user.json`](clean-room/milestone-10-user.json) — 10 个不同真人样本的 accepted gate。
- [`clean-room/cases/`](clean-room/cases/) — 当前保留的 accepted real-user cases。
- [`../docs/milestones/v0.4-recognition-hardening-10-user.md`](../docs/milestones/v0.4-recognition-hardening-10-user.md) — 这一阶段发现并修复的问题总结。

评测关注的是：是否越界、是否错误归因、是否把依赖/学习/协作升级成掌握、是否遗漏代表性主题，以及 Anchor / Galaxy / Distillation 是否仍然像这个具体的人。

> Evals 是研发输入和回归资产，不是普通 Skill 运行时的语义输入。clean-room Runner 不得读取其他用户 case、Auditor verdict 或历史 expected 来生成当前人物模型。
