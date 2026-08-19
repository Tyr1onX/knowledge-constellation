# Goal / Gap Loop｜从“我会什么”到“下一步做什么”

> Status: **Current product contract**

Knowledge Constellation 的 Current Universe 回答：

> 从现有证据看，我现在会什么、做过什么、哪些还在学习或无法确定？

Goal / Gap Loop 在此基础上回答第二个问题：

> 如果我有一个明确目标，我和它之间真正的距离是什么？下一步最值得做什么？

## 1. 目标不是拿来重写当前能力的

目标侧和当前人物侧必须分开建模：

```text
Current side                         Target side
-----------                          -----------
Input → Evidence → Claims/Nodes      Goal + target-side sources
                                     ↓
                                     Target Requirements
              \                     /
               \                   /
                Current-to-Target Gap
                         ↓
                  Next 1–3 Steps
```

Pass E（Target）**不能读取当前人物 Model**。否则系统很容易根据“这个人已经会什么”偷偷降低或修改目标要求，形成移动球门。

## 2. “没看到”不等于“不会”

Gap 只比较：

- 目标要求什么；
- 当前资料能证明什么。

当当前资料没有出现某项要求时，状态是 `not_observed`：

> 在现有资料里没有观察到足够证据。

它不是：

> 这个人不会。

因此 Gap 状态使用：

- `supported` — 现有证据已能实质支持；
- `partial` — 有真实基础，但目标要求更强的维度、深度或迁移；
- `unresolved` — 信息不足，无法判断；
- `not_observed` — 当前资料没有直接证据；
- `not_applicable` — 经目标语境判断后不适用。

## 3. Target 必须有外部依据

用户的一句目标，例如：

> “我想找 Linux / C++ 后端实习。”

只定义方向，不自动定义这个目标究竟要求什么。

如果用户给了具体 JD，优先使用它。否则 Codex 应收集少量高质量、当前有效的目标侧资料（例如真实岗位要求、官方技术要求、可靠招聘页面），再规范化为 `goal_input.json`。

Target Model 不应变成通用学习路线，也不应因为“后端通常会 X”就无限补全技术栈。

## 4. Gap 不是分数

我们不输出：

```text
C++ 72%
Linux 63%
网络 81%
```

这种数字无法由当前证据可靠推出，也会把不同维度压扁成一个伪精确分数。

Gap 必须保留维度差异：一个人可能有真实 implementation 证据，但 independence 仍未解决；也可能理解概念，却缺少 transfer / troubleshooting 的证据。

## 5. 下一步只给 1–3 个

Goal / Gap 的价值不是再生成一张 30 项 roadmap。

Pass G 只挑 1–3 个当前优先项，并说明：

- 它连接哪个目标要求；
- 当前已有哪个真实 foothold；
- 为什么现在值得先做它；
- 一个具体动作；
- 完成后什么可观察结果可以成为新的 Evidence。

低优先级要求可以明确 deferred。

## 6. Eligibility 不是学习内容

学历、地点、签证 / 工作许可、到岗时间等目标约束可能很重要，但不能伪装成“知识缺口”。

它们作为 `eligibility` requirement 单独保留；如果尚未满足或未知，在 `non_learning_constraints` 中展示，而不是产生“去学习学历”之类荒谬建议。

## 7. Growth 闭环

真正的产品闭环是：

```text
Current Universe
↓
告诉 Codex 一个目标
↓
Target / Gap / Next Steps
↓
学习、项目、贡献、工作实践
↓
产生新的真实资料
↓
重新进入 Recognition / Calibration
↓
Current Universe 发生真实变化
```

Plan 本身永远不能直接让星星变亮。

只有新的 Source / Evidence 可以改变对“当前的我”的 Recognition。

## 8. 当前实现

- `contracts/goal-input.schema.json`
- `contracts/target.schema.json`
- `contracts/gap.schema.json`
- `contracts/plan.schema.json`
- `harness/goal_pipeline.py`
- `harness/validate_goal.py`
- `harness/goal_e2e.py`
- `skill/GOAL_ORCHESTRATION.md`

当前阶段先验证**目标建模、Gap 判断和下一步选择是否可信**。在这层语义通过真人测试之前，不把 Target / Gap 强行塞进已经验收的 canonical Renderer。

> **先保证“下一步为什么是它”说得通，再决定目标宇宙应该怎么长在画面里。**
