# Knowledge Constellation｜知识星图

> 基于证据建立个人知识画像，并把不确定性保留下来。

Knowledge Constellation 想回答一个简单但很难的问题：

> **根据目前能够观察到的痕迹，我们有理由相信这个人知道什么、接触过什么、实践过什么？这些东西又是如何组成“这个人”的？**

项目希望从 GitHub、简历、学习记录、项目、作品集等已经存在的资料出发，生成一份**保守但完整、可解释、可以逐渐校准**的个人知识画像，而不是看到某个技术出现在项目里，就直接把它当成“已掌握技能”。

## 当前状态

仓库目前处于 **V0 研究阶段**。

现在还不是在急着发布一个完整 Skill，而是在验证它下面最重要的“认识协议（Recognition Protocol）”和“结构协议（Structure Protocol）”：

```text
Source / 来源
    ↓
Evidence / 证据
    ↓
Attribution / 归因
    ↓
Claim / 可支持的判断
    ↓
Knowledge Node / 知识节点
    ↓
Anchor / 真实经历锚点
    ↓
Relation / 个人关系
    ↓
Motif / 反复出现的个人主题
    ↓
Galaxy / 星系
    ↓
Distillation / 蒸馏
    ↓
Constellation / 知识星图
```

第一阶段默认使用 **Passive Evidence（被动证据）**：不要求用户先做长问卷、不要求深度自述，也不因为信息不足就乐观补全。

## 核心原则

- **证据先于推断（Evidence before inference）**：结论必须能够追溯到实际证据。
- **成果不等于掌握（Artifact ≠ mastery）**：项目用了 Rust，不等于用户能独立使用 Rust 开发。
- **参与不等于执行（Participation ≠ execution）**：参与一个 PR，不等于其中的分析、实现、测试都由本人完成。
- **归因很重要（Attribution matters）**：AI、协作者、模板与自动化都可能参与成果生产，需要区分人在其中真正承担的角色。
- **未知是合法状态（Unknown is valid）**：不知道就保留不知道，而不是自动补全。
- **接触不等于能力（Exposure ≠ capability）**：经常遇到一项技术，与能够独立使用它，是两种不同信号。
- **结构来自个人经历，而不是课程目录**：星系优先围绕真实项目、活动和学习轨迹形成，而不是预设“前端 / 后端 / 数据库”。
- **代表性不等于能力强弱（Representativeness ≠ proficiency）**：一个节点可以非常代表这个人，同时能力深度仍然没有解析清楚。
- **被动证据优先（Passive first）**：用户应该只提供已有资料，就能先得到一份有意义的结果。
- **渐进式解析（Progressive resolution）**：之后再通过少量选择题、自适应问题或长期证据，让画像逐渐变清晰。
- **人是主体（The person is the subject）**：不是拿一套标准知识树计算“完成度”，而是描绘哪些知识、实践和经历构成了现在的这个人。

## 仓库结构

```text
knowledge-constellation/
├─ README.md
├─ SKILL.md
├─ docs/
│  ├─ principles.md
│  ├─ v0-knowledge-model.md
│  ├─ attribution-model.md
│  ├─ structure-model.md
│  ├─ distillation.md
│  ├─ micro-calibration.md
│  └─ research-notes.md
└─ examples/
   └─ tyr1onx/
      ├─ evidence.md
      ├─ model.yaml
      └─ structure.md
```

## 第一个真实案例

第一份 V0 样本使用 `Tyr1onX` 的公开 GitHub 痕迹。

当前公开案例故意保持 **Passive-only**：只看公开 GitHub，测试零询问情况下最多能安全知道什么。

目前已经形成三个层次：

1. `evidence.md`：系统看到了什么；
2. `model.yaml`：这些证据最多允许系统相信什么；
3. `structure.md`：这些节点如何被压缩成更像个人的主题结构。

当前 Passive-only 的结构草案形成三个主题：

- **开源参与与工程流转**；
- **课刻与桌面产品**；
- **Web 基础补全**。

并发、SQLite、CAS 等真实但低代表性的概念被主动降到第二层，而不是因为技术复杂就成为主星。

聊天中的个人校准信息不会自动写入这个公开仓库。后续如果要公开“校准前 / 校准后”对照样本，应单独确认再加入。

## 路线

### V0 — Passive Constellation｜被动画像

已有资料 → 保守建模 → 个人结构 → 蒸馏 → 第一张知识星图。

### V0.1 — Explainability｜可解释

每个节点都能回答：为什么它存在？为什么它这么显眼？证据在哪里停止？

### V0.2 — Micro Calibration｜微校准

用少量、低成本、尽量高信息量的选择题改善归因、解析度，必要时允许星系结构本身发生变化。

### V0.3 — Adaptive Calibration｜自适应校准

只针对真正重要且不确定的区域，追加少量问题或小任务。

### Later — Longitudinal Constellation｜长期变化

让多次快照体现成长、遗忘、新方向和知识结构的变化。

## 当前两个成功标准

### 认识层

> **在证据不完整时，依然形成一幅有意义的画像，但绝不假装知道得比证据更多。**

### 展示层

> **用尽可能少的可见结构，保留尽可能多的个人解释力。**

最终希望做到：

> **远看是作品，近看是工具。**
