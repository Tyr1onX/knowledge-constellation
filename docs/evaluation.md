# Evaluation｜V0 评估与反例设计

> 只在一个人身上看起来合理，不足以证明模型成立。

当前第一份真实案例来自 Tyr1onX。它非常适合发现 AI 时代的 Attribution 问题，但也带来一个风险：

> **我们可能把规则调成“刚好适合这一个人”。**

因此在进入正式视觉实现之前，需要用不同类型的案例测试 Recognition、Structure 与 Distillation 是否仍然成立。

---

## 1. V0 不追求一个总准确率

目前没有可信方法声称：

```text
Knowledge Constellation accuracy = 87.3%
```

所以 V0 采用一组可审计问题，而不是伪精确总分。

每个案例至少检查：

1. 有没有把没有证据的能力说出来？
2. 有没有把 Activity 当成 Capability？
3. 有没有因为 AI / 协作存在就把用户所有贡献都抹掉？
4. 有没有漏掉最能解释这个人的重要主题？
5. Galaxy 是否像个人结构，而不是标准课程目录？
6. 第一眼是否被一次性高级技术或高频工具污染？
7. 隐藏细节后，人物轮廓是否仍然成立？
8. 每个可见判断能否追溯到 Evidence？

---

# 2. 主要失败模式

## F1 — Artifact Inflation｜成果膨胀

```text
项目用了 Rust
→ Rust 熟练
```

失败原因：把项目属性直接变成个人能力。

期望行为：

```text
Rust exposure: supported
independent capability: unresolved
```

---

## F2 — Participation Inflation｜参与膨胀

```text
PR 被合并
→ 用户独立完成分析、实现、测试
```

失败原因：Participation ≠ Execution。

期望行为：先确认活动事实，再解析角色。

---

## F3 — Assistance Erasure｜辅助抹除

与 F2 相反的另一个极端：

```text
使用了 AI
→ 这个成果与用户无关
```

也不成立。

AI 辅助可能仍然留下真实的人类角色，例如：

- 发起；
- 需求定义；
- 判断；
- 验收；
- 调试；
- 选择；
- 操作；
- 产品方向。

期望行为：降低错误的 Implementation Claim，但保留有证据的人类角色。

---

## F4 — Sophistication Bias｜高级词偏差

```text
CAS / WAL / 并发
看起来高级
→ 成为大星
```

失败原因：技术复杂度不等于个人代表性。

期望行为：如果只在少量事件中出现，优先进入第二层。

---

## F5 — Evidence Density Bias｜证据密度偏差

```text
GitHub 留下很多记录
→ GitHub 相关内容一定最重要
```

失败原因：可观察程度不等于个人主观重要性。

期望行为：

- Passive-only 只声称 Observable Representativeness；
- Identity Calibration 可以调整展示重心；
- 不反向修改能力 Claim。

---

## F6 — Source-as-Galaxy Bias｜把来源误当星系

例如用户提供：

```text
GitHub
简历
学习笔记
```

系统不能自动生成：

```text
GitHub 星系
简历星系
笔记星系
```

Source 是 provenance，不是个人结构。

一个 Source 可以包含多个 Anchor；多个 Source 也可以共同描述同一个 Anchor。

Galaxy 必须由真实主题形成，而不是由文件来源形成。

---

## F7 — Syllabus Completion｜课程目录补全

```text
JavaScript
→ 自动补 React
→ 自动补 Node
→ 自动补数据库
```

或：

```text
前端 / 后端 / 算法 / 数据库
```

作为所有人的默认 Galaxy。

失败原因：世界知识覆盖了个人证据。

期望行为：taxonomy 只能帮助解释，不能自动创造个人事实。

---

## F8 — Score Collapse｜维度坍缩

把：

- 代表性；
- 能力；
- 置信度；
- 解析度；
- 活跃度；

压成一个星星大小或一个分数。

失败原因：语义不可解释，并制造错误排名。

---

## F9 — Preference Contamination｜偏好污染事实

```text
用户说“Rust 很代表我”
→ Rust capability 自动升级
```

失败原因：Identity Calibration 污染 Truth Model。

期望行为：只调整 representativeness / display priority。

---

## F10 — Under-crediting Quiet Expertise｜低估低痕迹能力

有些用户能力很深，但几乎没有公开数字痕迹。

Passive-only 可能只能得到很保守的结果。

这不是通过“大胆猜测”解决，而应该：

- 明确保留 unknown；
- 允许简历、自述、作品和行为证据补充；
- 必要时使用低成本校准。

---

## F11 — Staleness｜历史痕迹冒充当前状态

五年前大量使用某技术，不等于现在仍然活跃。

需要保留时间信息，并在必要时询问 Recency。

---

## F12 — Visual Overclaim｜视觉越权

文字模型写：

> Rust 独立能力未知。

但视觉却把 Rust 画成最亮、最中心、最稳定的大星。

即使数据文件是“保守的”，用户最终仍会被误导。

因此视觉层也必须接受诚实测试。

---

# 3. 测试案例矩阵

V0 至少应该覆盖以下类型，而不是只测试 AI-heavy builder。

## Case A — AI-heavy Builder

特征：

- 有真实项目和外部成果；
- AI 深度参与分析和实现；
- 用户可能主要负责目标、授权、判断或操作。

主要测试：

- 是否过度归因实现能力；
- 是否又走向“有 AI = 什么都不算”的反方向。

Tyr1onX 当前属于这一类的重要样本。

## Case B — Independent Developer

特征：

- 有长期独立编码和调试记录；
- 有代码 Review / 解释 / Issue 分析等可验证痕迹；
- AI 使用较少或只是辅助。

主要测试：

> 模型会不会因为过度保守而不敢承认真实能力？

## Case C — Learning-heavy Student

特征：

- 项目少；
- 学习记录丰富；
- 有练习、笔记、考试或解释记录。

主要测试：

- 会不会因为缺少大项目就生成空图；
- 能不能区分“正在形成的知识”与“成熟能力”。

## Case D — One-project Specialist

特征：

- 公开痕迹高度集中于一个深项目；
- 技术栈可能很复杂。

主要测试：

- 会不会把一个项目的整个依赖树都算到本人头上；
- Galaxy 是否能保持聚焦而不虚构广度。

## Case E — Broad Generalist

特征：

- 多类项目；
- 多种独立实践；
- 主题跨度大。

主要测试：

- Structure 是否真的能形成多个有意义 Galaxy；
- 是否会变成几十颗同权重星星。

## Case F — Low-public-trace User

特征：

- GitHub 很少；
- 简历、作品集、自述或本地项目较多。

主要测试：

- 输入源是否真正多样；
- 是否把 GitHub 错误地当成产品前提。

---

# 4. 每个案例需要保存三份结果

建议未来测试统一保留：

```text
raw-evidence.md
model.yaml
structure.md
```

如果有校准，再增加：

```text
calibration.md
model-after-calibration.yaml
structure-after-calibration.md
```

这样可以观察：

> 一次校准到底修复了什么，而不是只看最终图好不好看。

---

# 5. Human Review｜真人复核问题

测试对象看完第一版后，不需要填写长评价表。

可以只问：

### Truth

> 有哪些地方明显把你说高了？

> 有哪些地方明显把你说错了？

### Missing

> 有什么很能代表你，但完全没被看出来？

### Structure

> 这些 Galaxy 像不像你的实际结构？

### Distillation

> 有没有某些很显眼的东西，其实只是偶然经历？

### Effort

> 如果只允许再回答 1～3 个选择题，哪些模糊点最值得修？

这比问“你给这个产品打几分”更能帮助模型进化。

---

# 6. 进入正式视觉原型前的 Gate

至少完成以下条件后，再认真进入视觉实现：

1. AI-heavy case 不明显吹高；
2. independent developer case 不明显压低；
3. learning-heavy case 不会因为缺少项目而变空；
4. one-project case 不会变成依赖树；
5. broad case 能形成可读结构；
6. 至少两类案例经过真人复核；
7. Distillation 在多数案例中能把首层压到可读规模；
8. 主要失败都能解释是 Recognition、Attribution、Structure 还是 Visual 层造成。

通过这个 Gate 后，视觉原型才有意义。

否则我们可能只是在给一个尚未稳定的判断系统做漂亮皮肤。
