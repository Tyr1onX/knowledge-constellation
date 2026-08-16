# Round 02｜第二轮自我迭代报告

本轮使用 I～L 四个对抗案例，重点测试：证据冲突、时间、团队角色、证书。

## I — Contradictory Evidence

初始风险：把“React 项目做得出来”和“JS 基础仍在补”平均成一个模糊等级。

修复：引入 Claim Type 与 Conflict Ledger。

结果：

```text
React project exposure        supported
product practice              supported
JavaScript understanding      bounded / developing
independence                  unresolved
```

不再生成“中级前端”这种无法解释的折中标签。

**通过。**

---

## J — Stale Expertise

初始风险：旧能力要么被保留得过强，要么因为多年未使用直接消失。

修复：把 Knowledge State 与 `activity_state` 分开。

结果：

```text
Java / Spring
state: established
activity_state: historical
```

历史事实不被抹掉，当前中心也不会被旧证据占据。

**通过。**

---

## K — Collaboration-heavy

现有 Role Attribution 已能较好处理。

结果允许：

```text
Requirement Framing          strong evidence
Product Judgment             strong evidence
Acceptance & Validation      strong evidence
Core Implementation          limited evidence
Architecture Ownership       unsupported
```

并正式写死：Commit / LOC 不是贡献度。

**通过。**

---

## L — Certification-only

初始风险：把证书直接当成生产能力。

修复：证书必须带 `assessment_scope` 和时间，只验证测评覆盖范围。

结果：

```text
AWS structured understanding    supported
exam validation                 supported
production architecture         unresolved
troubleshooting                 unresolved
```

**通过。**

---

# 两轮测试后的状态

目前合成案例已经覆盖：

- AI-heavy builder；
- independent developer；
- learning-heavy student；
- one-project specialist；
- broad generalist；
- low-public-trace user；
- AI-heavy + high human judgment；
- impressive README / badge inflation；
- contradictory evidence；
- stale expertise；
- collaboration-heavy role；
- certification-only evidence。

当前没有发现必须阻塞第一版视觉原型的 Recognition / Attribution 级漏洞。

仍然存在的未知主要属于：

1. 真实第二个人案例是否符合合成测试预期；
2. Distillation 在真实复杂资料中是否稳定；
3. 视觉语义是否会在用户直觉中产生新的误读。

第三点已经不能只靠文档继续推演。

> **下一阶段应该进入可视化原型，用最终用户真正看到的东西继续测试。**

这不是宣布 Knowledge Model 已经完成，而是说明：

> 再继续只在文字协议里迭代，边际收益已经下降；最重要的新反馈将来自视觉层。
