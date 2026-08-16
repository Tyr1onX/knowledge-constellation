# Evidence & Claim Semantics｜证据准入与判断语义

> Round 01 之后补充：不仅要问“有没有证据”，还要问“这条证据到底能证明哪一种事情”。

这个文档解决四个在合成测试中暴露出来的问题：

1. 技术出现在环境中，不等于用户真的接触过；
2. “能力”不是一个单一维度；
3. 多条同源描述不能假装成多份独立佐证；
4. 自我包装不能直接升级成能力事实。

---

# 1. Environmental Presence ≠ Meaningful Exposure

旧的简单规则：

```text
项目使用 X
→ 用户对 X 有 exposure
```

仍然太宽松。

现代项目包含大量：

- 间接依赖；
- 模板代码；
- 生成代码；
- untouched library；
- 平台自动带入的组件。

所以 V0.6 开始把“存在”拆成两个层级。

## `environmental_presence`｜环境存在

只能说明：

> 这项技术存在于与用户相关的项目或工作环境中。

例如：

```text
package.json 出现 Redis client
Cargo.toml 出现某 Rust crate
项目模板带 React
```

它默认**不足以形成可见 Knowledge Node**。

## `meaningful_exposure`｜有意义接触

至少需要一条能把技术与用户实际行为连接起来的证据，例如：

- 修改过相关代码；
- 调试过相关问题；
- 配置过相关行为；
- 做过采用 / 放弃该技术的取舍；
- 写过相关解释；
- 学习记录明确涉及；
- 校准明确确认本人实际接触。

只有到这里，才允许安全地说：

> 这项技术真实进入过这个人的知识或实践世界。

规则：

> **Dependency is provenance, not personal knowledge.**
>
> 依赖关系说明项目组成，不自动说明人的知识组成。

---

# 2. Claim Type｜判断必须说明“证明的是哪种能力”

V0 不建立一个万能 `skill_score`。

一条 Claim 至少要标记它主要描述哪一种能力。

## `understanding`｜理解

能解释概念、机制、因果和边界。

典型证据：

- 新问题下的解释；
- 纠错记录；
- 技术说明；
- 口头 / 书面推理。

## `implementation`｜实现

能够把要求变成可运行的实现。

典型证据：

- 明确归因的代码修改；
- 功能实现；
- 重构；
- 修复。

## `independence`｜独立程度

在没有大量外部代做的情况下，能独立推进任务。

它不能仅由“代码作者名”推断。

需要更强的：

- 过程证据；
- 明确角色说明；
- 多次独立行为；
- 校准 / behavioral evidence。

## `judgment`｜判断与取舍

能够判断：

- 哪个方案更符合目标；
- 什么结果不可接受；
- 什么边界需要处理；
- 什么时候可以发布 / 合并。

AI-heavy 工作流中，这一项尤其重要。

## `troubleshooting`｜诊断与调试

能够：

- 复现问题；
- 缩小范围；
- 判断根因；
- 验证修复。

## `transfer`｜迁移

能够把已有知识用于新的、没有直接见过的问题。

V0 很少直接宣称 Transfer，除非存在新情境下的行为证据。

---

# 3. 同一个节点可以有不对称能力状态

例如：

```yaml
node: TCP
claims:
  understanding: established
  implementation: unresolved
  troubleshooting: low-evidence
```

或者：

```yaml
node: Rust
claims:
  implementation: established
  troubleshooting: developing
  understanding: medium-evidence
  independence: established
```

这比：

```text
Rust：4/5
```

更诚实。

注意：这些细项主要服务内部判断和详情页，不要求全部出现在首屏。

---

# 4. Corroboration Independence｜佐证独立性

证据数量不等于证据强度。

## Same-origin Corroboration｜同源重复

例如：

```text
个人 README：熟悉 Rust
个人主页：熟悉 Rust
个人简历：熟悉 Rust
```

它们可以说明这个人反复这样自我描述，但主要仍属于同一主体的自我陈述。

不能当成三份独立能力验证。

## Cross-origin Corroboration｜跨源佐证

例如：

```text
本人 Issue 根因分析
+
明确归因的实现记录
+
维护者 Review
+
独立 benchmark
+
新的解释任务
```

这些证据类型互补，并且部分来自独立第三方或新的行为情境。

更适合支撑强 Claim。

## V0 判断方式

暂不计算数学权重。

每个强 Claim 至少回答：

1. 证据是不是都来自同一个自我描述？
2. 有没有行为证据？
3. 有没有第三方结果？
4. 有没有多个不同情境下的重复？
5. 这些证据是不是其实只是同一成果的不同表述？

---

# 5. Self-presented Identity｜自我呈现单独保存

README、个人主页、简历中的：

```text
Expert in X
Passionate about Y
Full-stack developer
AI engineer
```

不是无价值信息。

它可以表示：

- 用户希望如何定义自己；
- 当前兴趣；
- 职业定位；
- Identity Calibration 的线索。

但默认进入：

```text
claimed_identity
```

而不是：

```text
verified_capability
```

只有出现额外能力证据后，才能形成对应 Capability Claim。

## 技术 Badge

Badge 数量本身没有能力证明力。

```text
30 个技术 badge
≠
30 个 Knowledge Node
```

---

# 6. Absence of Evidence ≠ Negative Evidence

没有找到证据只能说明：

> 当前资料无法支持这个判断。

不能自动说明：

> 用户不会。

例如 Case H 没有 Kubernetes 行为痕迹：

```text
Kubernetes capability: unresolved / unsupported
```

而不是：

```text
Kubernetes capability: low
```

真正的 Negative Evidence 应该是：

- 用户明确说从未接触；
- 当前学习记录明确标记 not-started；
- 行为任务直接暴露明显边界；
- 其他可靠证据明确与某 Claim 冲突。

即使存在 Negative Evidence，也要限定它能否代表当前状态和完整能力。

---

# 7. Claim Admission｜强判断准入

V0.6 建议：

## 可以仅凭一条证据成立的低强度判断

例如：

```text
这个项目真实存在。
这个技术明确出现在环境中。
用户公开自述对这个方向感兴趣。
```

## 需要多种证据才能成立的高强度判断

例如：

```text
可以独立使用 Rust 开发。
能够稳定诊断并发问题。
能够把网络知识迁移到新系统。
```

强度越高，越需要：

- 行为证据；
- 跨源佐证；
- 重复情境；
- 清晰 Attribution。

原则：

> **The stronger the claim, the stronger and more independent the evidence must be.**
>
> 判断越强，证据不仅要更多，还要更独立、更接近真实行为。

---

# 8. “保守但完整”的新定义

完整不是节点数量。

> **Complete means the currently supportable personal shape is represented without deliberate omission.**

因此：

```text
低证据用户
→ 2 个清晰主题 + 大片未解析
```

完全可以比：

```text
20 个靠猜出来的技能节点
```

更完整。

V0 宁愿让宇宙存在暗区，也不使用世界知识把暗区补亮。
