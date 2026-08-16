# Structure Model｜结构模型

> V0.5 research note — 从“有哪些节点”走向“这些节点为什么会组成这个人”。

Knowledge Model 解决的是：**哪些判断能够被证据支持？**

Structure Model 解决的是另一件事：

> **这些被支持的知识、实践和经历，是围绕什么真实上下文组织起来的？**

如果缺少这一层，Knowledge Constellation 很容易退化成“前端 / 后端 / 数据库 / 算法”这样的课程目录，只是换了一层星图皮肤。

---

## 1. 星系不是学科分类

星系（Galaxy）不应该默认来自预设 taxonomy。

不推荐：

```text
前端开发
├─ HTML
├─ CSS
└─ JavaScript
```

更希望得到：

```text
课刻与桌面产品
├─ 产品迭代
├─ Tauri
├─ Rust
└─ TypeScript
```

后者描述的是**这个人的真实经历如何把知识组织在一起**，而不是世界知识如何给技术分类。

原则：

> **Galaxy should describe the person, not the syllabus.**
>
> 星系应当描述这个人，而不是描述课程目录。

---

## 2. Anchor｜锚点

在 Knowledge Node 与 Galaxy 之间增加一个内部对象：**Anchor（锚点）**。

锚点不是知识点，而是真实存在的上下文，例如：

- 一个长期项目；
- 一组持续的开源贡献；
- 一段明确的学习轨迹；
- 一份长期维护的知识库；
- 一个反复出现的工作目标；
- 一类稳定出现的实际任务。

示例：

```yaml
id: anchor_desktop_course_widget
type: project
label: 课刻
sources:
  - desktop-course-widget
```

```yaml
id: anchor_external_prs
type: activity_stream
label: 持续的外部 PR
```

锚点回答的是：

> **为什么这些节点会在这个人的世界里靠近？**

而不是：

> 这些技术在百科全书里是否相关？

---

## 3. Relation｜关系

V0 先限制为四类关系，避免模型过度创造语义网络。

### 3.1 `co_occurrence`｜共同经历

两个节点在同一个真实锚点中出现。

```text
课刻
├─ Tauri
├─ Rust
└─ TypeScript
```

它允许建立：

```text
Tauri ↔ Rust
Tauri ↔ TypeScript
```

但关系来源是共同项目，而不是语言模型知道它们“理论上相关”。

### 3.2 `repeated_context`｜重复共现

两个节点在多个独立锚点或多次活动中反复一起出现。

重复共现比单次共同经历更强，因为它说明这种组合对**这个人**具有稳定性。

### 3.3 `trajectory`｜学习或发展轨迹

存在明确顺序或阶段关系，例如：

```text
Web / 网络基础
→ 浏览器渲染
→ JavaScript / DOM
→ 后续异步机制
```

必须有学习记录、时间序列或其他实际证据支持，不能仅靠“正常学习顺序”推断。

### 3.4 `practice`｜实践关系

节点共同组成一种持续出现的做事方式，例如：

```text
开源参与
→ GitHub / PR 工作流
→ 测试与验证
```

它不是知识依赖关系，而是实践过程中的结构关系。

---

## 4. 世界知识只能辅助，不能创建个人事实

LLM 当然知道：

- React 与 JavaScript 有关系；
- HTTP 通常建立在 TCP 等传输机制之上；
- Rust 与 ownership 等概念有关。

这些背景知识可以帮助：

- 理解节点；
- 解释布局；
- 生成更自然的名称；
- 提出后续校准假设。

但它**不能单独创建**：

- 新的 Knowledge Node；
- 新的个人关系；
- 新的 Galaxy；
- 新的能力 Claim。

否则会发生：

```text
用户学过 HTTP
→ TCP
→ Socket
→ Linux Network Stack
→ epoll
```

最后模型绘制的是“计算机知识图谱”，而不是这个人。

规则：

> **Know by evidence, not by implication.**
>
> 根据证据认识，而不是根据理论关联补全。

---

## 5. Motif｜个人主题

Anchor 与 Relation 形成稳定模式后，可以抽取 **Motif（个人主题）**。

Motif 是比单个节点更高一级的解释：

> 一组知识和实践为什么反复围绕同一种真实活动出现？

例如：

```text
Anchor: 多次外部 PR
        ↓
开源参与 ─ GitHub / PR ─ 测试与验证
        ↓
Motif: 开源参与与工程流转
```

```text
Anchor: 课刻
        ↓
产品迭代 ─ Tauri ─ Rust ─ TypeScript
        ↓
Motif: 课刻与桌面产品
```

Motif 不一定最终成为视觉上的实体，但它是 Galaxy 命名和形成的重要中间层。

---

## 6. Galaxy Candidate｜星系候选

一个 Galaxy Candidate 通常需要同时满足：

1. 至少存在一个真实 Anchor；
2. 有多个证据支持的节点；
3. 节点之间存在实际关系，而不是仅仅语义相似；
4. 这个主题可以解释一部分持续的个人经历；
5. 与其他候选主题存在足够区别。

不要求每个 Galaxy 都是“技能领域”。

它可以是：

- 一个项目；
- 一条学习路线；
- 一种实践方式；
- 一个长期兴趣方向；
- 一种反复出现的问题类型。

---

## 7. 一个节点只有一个 Primary Galaxy

为了避免视觉重复，V0 规定：

> **一个 Knowledge Node 最多只有一个 Primary Galaxy（主星系），但可以存在多个跨星系关系。**

例如“测试与验证”同时出现在开源贡献和个人项目中。

不推荐复制两个 Testing 节点。

更推荐：

```text
开源参与与工程流转
        │
   测试与验证
        │
        └────────→ 课刻与桌面产品
```

Primary Galaxy 可以根据以下信号决定：

- 出现频率；
- 与哪个 Anchor 关联最强；
- 在哪个主题里解释力更高；
- 是否承担桥接作用。

---

## 8. Galaxy 名称必须个人化

默认避免仅使用：

- 前端；
- 后端；
- 数据库；
- 软件工程；
- 编程语言。

只有当这些标签确实最能描述这个人的结构时才使用。

更好的命名往往来自：

```text
真实 Anchor + Motif
```

例如：

- 课刻与桌面产品；
- 开源参与与工程流转；
- Web 基础补全；
- 浏览器自动化实践；
- 数据分析与研究工作流。

同样学习 JavaScript 的两个人，不应该自动得到同样的星系。

---

## 9. 复杂技术不应因为“看起来厉害”而成为中心

一次 PR 中出现 CAS、SQLite WAL、并发读取等高级概念，只能说明这些概念真实进入过经历。

如果它们：

- 只在单一事件中出现；
- 个人理解仍未解析；
- 对其他经历解释力有限；

那么它们通常应该成为外围节点或第二层细节，而不是中心星。

复杂度不是代表性。

---

## 10. Calibration 可以改变结构，而不只是改变等级

校准之后，系统可能发现新的反复模式。

例如 Passive Evidence 只能看到：

```text
开源 PR
课刻
多个软件项目
```

但一次用户校准可能揭示：

```text
这些活动都大量依赖 AI Agent 推进
```

那么可能出现一个新的 Motif：

```text
AI-assisted Workflow
```

并重新连接原有星系。

因此：

> **Galaxy 是当前证据下的结构快照，不是永久 taxonomy。**

---

## 11. V0 结构管线

```text
Knowledge Nodes
      ↓
Anchors
真实项目 / 活动 / 学习轨迹
      ↓
Relations
共同经历 / 重复共现 / 轨迹 / 实践
      ↓
Motifs
反复出现的个人主题
      ↓
Galaxy Candidates
      ↓
Distillation
决定第一眼应该看到什么
      ↓
Visual Model
```

Structure Model 的成功标准不是“分类得很完整”，而是：

> **把节点重新组织后，比平铺节点更能解释“为什么这个人的知识世界是现在这个样子”。**
