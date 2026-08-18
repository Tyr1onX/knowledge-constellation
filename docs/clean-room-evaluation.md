# Clean-room Evaluation｜隔离运行与外部审计

> Status: **Current Recognition Hardening contract**

Recognition 评测使用两条隔离路径：

```text
Frozen raw-source snapshot → Clean-room Runner → Pass A/B/C/D → Harness validation
Frozen raw-source snapshot → External Auditor → source-only notes → compare Runner output
```

目标不是让 Runner 和 Auditor生成完全相同的节点，而是持续检查：证据边界、Attribution、代表性遗漏、真实 Anchor、个人化 Galaxy、Relation 支撑，以及学习 / 依赖 / 协作 / AI-assisted 是否被错误升级成能力。

## Runner 隔离边界

Runner 只能看到：

```text
SKILL.md
skill/ORCHESTRATION.md
当前 Pass prompt
当前 Pass schema
当前 Pass 允许的 upstream output
TASK.md
frozen raw-source snapshot
```

Runner 不得读取：

- `evals/` 中其他人物 case、Auditor notes、previous verdict 或 expected；
- `tests/` 中可能暗示语义答案的 fixture / baseline；
- 之前对同一人物的人工分析；
- 任何 gold answer 或其他用户输出。

Harness 可以做 workspace isolation、schema / semantic validation、reject / repair 和持久化，但不能替 Runner 生成语义答案。

## Frozen source snapshot

每个真人 case 至少记录 target、snapshot time、source URLs / repo IDs、相关 README / profile / metadata，以及需要时的 commit / PR / issue / contribution records。Runner 与 Auditor 必须基于同一冻结范围。

## Runner 结果

`kc.cleanroom.v2` 至少保留：

```text
metadata.json
source-manifest.json
runner/pass-a.json
runner/pass-b.json
runner/pass-c.json
runner/pass-d.json
runner/validation-proof.json
audit/source-only-notes.md
audit/comparison.md
audit/verdict.json
```

不保存或要求模型隐藏思维过程。评测对象是可重放输入、结构化输出和 validator 行为。

## External Auditor

理想情况下 Auditor 来自另一进程 / 新会话 / 独立模型实例，并在看到 Runner 输出前先阅读 frozen sources。Auditor 重点寻找：

- `critical_inflation` — 无充分证据形成强 implementation / independence / mastery；
- `dependency_to_mastery` — 把依赖或生成产物写成本人能力；
- `attribution_error` — AI / collaborator / upstream / user 归因错误；
- `learning_state_error` — 学习、课程、练习被写成稳定掌握；
- `important_omission` — 代表性主题被漏掉；
- `anchor_error` — Anchor 不是实际经历；
- `taxonomy_galaxy` — Galaxy 更像课程目录；
- `unsupported_relation` — Relation 缺少个人证据；
- `over_distillation` / `under_distillation` — 首层压缩失真。

## Verdict

- `PASS` — 无关键能力膨胀，主要人物轮廓、Attribution、Anchor 与结构可靠；
- `PASS_WITH_WARNINGS` — 无致命越界，但仍有需要修复的重要结构 / 归因问题；
- `FAIL` — 出现关键膨胀、严重归因错误或主要人物轮廓失真。

## Rerun 与 blind test

修改 Recognition 规则后，优先用同一 frozen snapshot 做回归，再换新的陌生用户。可做 blind A/B：A=current Skill，B=candidate Skill，Auditor 在揭晓版本前独立审计。

如果环境不能启动真正独立的 Codex，只能使用同会话 clean-room emulation，并明确标记：

```text
isolation_level: emulated
```

真正新会话 / 新进程才记为：

```text
isolation_level: independent
```

> **We test the Skill by withholding our expectations from the Runner, then attacking its result from the outside.**
