# Clean-room Evaluation｜隔离运行与外部审计

> Status: **Current Recognition Hardening contract**

Knowledge Constellation 的 Recognition 评测采用两条彼此隔离的路径：

```text
Frozen raw-source snapshot
        ↓
Clean-room Runner
        ↓
Pass A / B / C / D outputs
        ↓
final structured result

Frozen raw-source snapshot
        ↓
Independent External Auditor
        ↓
source-only audit notes
        ↓
compare against Runner output
```

目标不是让 Runner 和 Auditor 得到完全相同的节点列表，而是验证：

- 是否越过证据边界；
- 是否遗漏最具代表性的主题；
- Attribution 是否可靠；
- Anchor 是否来自真实经历；
- Galaxy 是否像这个人，而不是默认技术 taxonomy；
- 学习 / 依赖 / 协作 / AI-assisted 是否被错误升级成独立能力。

## 1. Clean-room Runner 的隔离边界

Runner 只能看到当前任务真正允许的输入：

```text
SKILL.md
skill/ORCHESTRATION.md
当前 Pass prompt
当前 Pass schema
当前 Pass 允许的 upstream output
TASK.md
frozen raw-source snapshot
```

Runner **禁止读取**：

- `examples/` 中任何历史人物结果；
- `evals/` 中 expected / auditor notes / previous verdict；
- tests 中可能暗示人物答案的 fixture；
- 之前对同一人物的人工分析；
- 其他用户的输出；
- Auditor 的任何中间判断。

Harness 可以做 schema validation、reject / repair 和 workspace isolation，但不能替 Runner 生成语义答案。

## 2. Frozen source snapshot

每个真实人物案例必须冻结输入快照，至少记录：

- target handle / profile URL；
- snapshot timestamp；
- source URLs / repository IDs；
- README / profile text；
- repository metadata；
- 需要时的 commit / PR / issue / contribution records；
- source collection note；
- Knowledge Constellation commit SHA；
- Runner model / configuration。

Runner 与 Auditor 必须基于同一个 snapshot 范围，避免一方读到之后新增的资料。

## 3. Runner 输出必须保存

每次运行至少保留：

```text
metadata.json
source-manifest.json
pass-a.json
pass-b.json
pass-c.json
pass-d.json
validation-log.md
runner-summary.md
```

如果某 Pass 触发 repair，应保留失败版本、validator error 和修复版本，而不是只留下最终成功答案。

不要求保存或审计模型隐藏思维过程。评测对象是可重放输入、结构化输出与 validator 行为。

## 4. External Auditor 必须独立

理想条件下 Auditor 是另一进程 / 另一会话 / 另一模型实例，在看到 Runner 输出前先独立阅读 frozen raw sources。

Auditor 先形成 source-only notes，再打开 Runner 输出进行比较。

Auditor 不要求复现同一棵知识树，而是回答：

1. Runner 说了什么不该说的？
2. Runner 漏掉了什么真正重要的？
3. 哪些 Attribution 被夸大或抹除了？
4. 哪些 Node 只是依赖、成果存在或课程暴露？
5. 哪些跨项目重复、debugging、review、trade-off、validation traces 值得更高权重？
6. Anchor 是否真实？
7. Galaxy 是否具有个人结构？
8. Distillation 是否把真正代表这个人的内容留在首层？

## 5. 审计错误分类

每个案例至少记录以下错误：

- `critical_inflation` — 无足够证据却形成强 implementation / independence / mastery 等结论；
- `dependency_to_mastery` — 把依赖、框架、生成产物直接写成本人掌握；
- `attribution_error` — AI / collaborator / upstream / user contribution 归因错误；
- `learning_state_error` — 课程、练习、正在学习被写成稳定能力；
- `important_omission` — 具有明显代表性的长期或跨上下文主题被漏掉；
- `anchor_error` — Anchor 是技术分类而不是真实经历；
- `taxonomy_galaxy` — Galaxy 更像课程目录而不是个人主题；
- `unsupported_relation` — 关系没有个人证据；
- `over_distillation` — 为保持固定节点数而压掉有意义结构；
- `under_distillation` — 低价值细节挤占首层。

## 6. Verdict

每个案例给出：

- `PASS` — 无 critical inflation；主要人物轮廓、Anchor 与边界可靠；
- `PASS_WITH_WARNINGS` — 无致命越界，但存在重要遗漏、结构或归因问题；
- `FAIL` — 出现关键能力膨胀、严重归因错误、主要人物轮廓失真或其他产品级错误。

不使用单一“准确率”替代错误说明。

## 7. Blind A/B

当修改 Recognition Skill 时，推荐使用同一 frozen source snapshot 分别运行：

```text
A = current Skill
B = candidate Skill
```

Auditor 在不知道 A/B 版本身份的情况下分别审计，再揭晓版本。

目标是避免“刚改了 prompt，所以主观认为新版更好”的确认偏差。

## 8. 同一会话内的临时模拟

如果环境暂时无法启动真正独立的 Codex 实例，可以做 **single-session clean-room emulation**：严格限制 Runner 只使用允许文件，并把其输出先冻结，再进入 Audit。

这种结果必须标记：

```text
isolation_level: emulated
```

不能冒充真正的独立 blind run。正式 v0.1 gate 优先使用另一进程 / 新会话的 `isolation_level: independent`。

> **We test the Skill by withholding our expectations from the Runner, then attacking its result from the outside.**
