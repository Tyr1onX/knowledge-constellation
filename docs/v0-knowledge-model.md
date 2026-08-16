# V0 知识模型｜V0 Knowledge Model

V0 故意保持小而保守。

它不试图一次描述所有形式的人类知识，而是先验证：

> **仅依赖已有资料，能不能生成一份保守、完整、可解释的第一版个人知识画像？**

## 基础管线

```text
Source / 来源
    ↓
Evidence / 证据
    ↓
Claim / 可支持的判断
    ↓
Knowledge Node / 知识节点
```

`Attribution（归因）`、`Confidence（置信度）` 和 `State（状态）` 在 V0 中先作为字段，而不是独立对象。

---

# 1. Source｜来源

Source 只回答：**这条信息从哪里来？**

```yaml
id: source_egc_pr_1271
type: github_pr
locator: https://github.com/Fmarzochi/EGC/pull/1271
observed_at: 2026-08-16
```

V0 初始支持：

```text
github_profile
github_repository
github_pr
github_issue
github_review
resume
portfolio
learning_record
document
self_report
```

来源类型本身不等于真实性等级。

例如学习记录和外部维护者 Review 都有价值，但它们能支持的结论不同。

---

# 2. Evidence｜证据

Evidence 记录**实际观察到了什么**，先不急着评价能力。

```yaml
id: evidence_egc_1271_merged
source: source_egc_pr_1271
kind: external_validation
observation: >-
  一个包含并发修复和多进程 chaos harness 的 PR 经维护者 Review 后被合并。
attribution:
  level: external
confidence: high
```

## V0 证据类型

- `artifact`：仓库、文件、功能、PR、文档等成果真实存在；
- `activity`：某人反复出现在可观察的活动流程中；
- `learning_record`：结构化记录显示某主题被学习、解释或复习；
- `external_validation`：维护者、Reviewer、考试或其他外部结果提供验证；
- `self_report`：用户明确描述自己的经历或参与方式；
- `behavioral`：观察到用户直接解释、回答、完成任务等行为。

## 证据写法

错误：

```text
用户擅长并发。
```

更好：

```text
用户账号提交并完成过一个涉及 cursor CAS 和多进程并发测试的已合并 PR。
```

Evidence 描述事实，能力判断留给 Claim。

---

# 3. Attribution｜归因

Attribution 回答：

> **这些观察中，哪些部分可以安全地归因给这个人？**

V0 保留四个总级别：

### `direct`｜直接

观察到的行为本身明确和用户绑定，例如：提交 PR、公开解释、回答校准问题。

`direct` **不代表**整个成果由本人独立完成。

### `assisted`｜有辅助

有明确证据表明 AI、协作者、模板或工具深度参与，而用户也真实参与其中。

### `uncertain`｜不确定

成果与用户有关，但无法从已有资料判断具体贡献深度。

### `external`｜外部

证据来自第三方评价或结果，例如维护者接受 PR。

## 角色归因

仅有这四类还不足以描述 AI Agent 场景，因此 V0 同时允许记录角色：

```text
initiated   发起
selected    选择目标
specified   定义需求
implemented 实现
reviewed    审阅
validated   验证
operated    操作
authorized  授权
debugged    调试 / 定位
explained   解释
```

角色状态只使用：

```text
supported
partial
low
unknown
```

详细规则见 [`attribution-model.md`](attribution-model.md)。

## 关键规则

```text
Participation ≠ Execution
参与 ≠ 执行
```

如果只知道一个仓库属于某人，具体实现归因默认必须是 `uncertain`，而不是 `direct`。

---

# 4. Claim｜可支持的判断

Claim 才是真正关于“这个人”的陈述。

```yaml
id: claim_open_source_participation
statement: 持续参与过真实开源贡献流程。
supported_by:
  - evidence_egc_1271_merged
  - evidence_other_merged_prs
confidence: high
limits:
  - 不代表这些贡献中的全部技术工作由本人独立完成。
```

每条 Claim 都必须回答：

1. 我们相信什么？
2. 为什么相信？
3. 哪些 Evidence 支持它？
4. 其中哪些部分能归因给用户？
5. **证据在哪里停止？**

回答不了，就应该弱化、标记未解析或删除，而不是继续补全。

---

# 5. Knowledge Node｜知识节点

Knowledge Node 是最终可能进入星图的概念。

一颗星**不等于“已经掌握的技能”**。

它表示：

> 这个概念在当前这个人的知识、学习或实践世界里，占据了一个有意义的位置。

例如：

```yaml
id: rust
label: Rust
state: observed
confidence: low
signals:
  exposure: high
  capability: unresolved
```

这样 Rust 可以真实存在于星图中，同时不虚构“Rust 熟练度”。

---

# 节点状态｜Node State

V0 只使用四种状态。

## `established`｜较明确

多条较强证据支持一个相对稳定的知识或实践判断。

## `developing`｜正在形成

存在明确学习或实践证据，但能力仍在形成，或者只有部分被确认。

## `observed`｜已观察

这个概念明确出现在经历中，但理解深度、独立程度或能力尚未解析。

## `unresolved`｜未解析

存在值得保留的迹象，但证据还不足以形成稳定可见节点。

`unresolved` 默认不进入主星图，或者只在外围以不确定状态出现。

---

# Confidence｜置信度

V0 不制造假精确。

只允许：

```text
high
medium
low
```

没有可靠评估方法之前，不使用 `0.783` 这种数字。

---

# Exposure 与 Capability 必须分开

Passive Evidence 最容易观察的是：

> “这个技术反复出现。”

最难知道的是：

> “这个人能不能独立完成。”

因此：

```yaml
id: typescript
label: TypeScript
state: observed
confidence: low
signals:
  exposure: high
  capability: unresolved
```

比“TypeScript 3/5”更可靠。

---

# 常见证据边界

## 仓库使用 X

可以支持：

- X 存在于项目环境；
- 用户与 X 有真实接触。

不能自动支持：

- 能独立使用 X 实现；
- 深入理解 X。

## 已合并 PR 涉及 X

可以支持：

- 真实参与了一次被接受的贡献；
- 接触过相应问题域；
- 存在开源流程经验；
- 交付结果受到外部接受。

不能自动支持：

- 每一行都是本人写的；
- 每个技术概念都由本人理解；
- 测试、分析、实现都由本人完成。

## 学习记录写着 `understood`

可以支持：

- 该主题被认真学习过；
- 存在结构化理解记录；
- 节点至少可以进入 developing 候选。

不能自动支持：

- 长期记忆稳定；
- 新场景下独立迁移；
- 面试级或专家级能力。

---

# Micro Calibration 如何进入模型

第一版生成以后，如果 Attribution 中存在高价值不确定项，可以询问极少量选择题。

例如：

> “你在这些开源 PR 中通常承担什么角色？”

回答首先更新的是：

```text
Attribution
```

随后重新计算：

```text
Claim
↓
Knowledge Node
```

而不是修改“这些活动曾经发生过”的历史 Evidence。

详细见 [`micro-calibration.md`](micro-calibration.md)。

---

# V0 停止条件

V0 不需要知道完整的人。

它只需要能够稳定说出两类话：

> **“这确实属于你的知识星图。”**

以及：

> **“它确实出现在你的经历里，但现有证据还不足以让我说得更深。”**

如果系统能形成一份有意义的第一版画像，同时诚实保留这种边界，V0 就已经成功。
