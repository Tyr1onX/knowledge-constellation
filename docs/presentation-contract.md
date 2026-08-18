# Presentation Contract｜成品界面契约

> 最终产品首先是一幅“属于这个人的知识宇宙”，其次才是一份可解释的数据报告。
>
> Current checkpoint: **Personal Universe v3 — 2026-08-18**

本文件约束 **Knowledge Model 如何进入最终用户界面**。它的目的，是防止研究阶段、调试阶段和模型内部使用的语言直接泄漏到成品体验中。

## 1. 第一眼必须先是宇宙

打开最终产物时，用户首先应该感受到：

- 空间；
- 星体；
- 星系；
- 密度与疏密；
- 某些区域更清晰、某些区域仍在雾中；
- 这是“某个具体人的”结构，而不是一张报告。

第一屏默认不出现：

- V0 / Prototype / Passive-only 等开发阶段标签；
- “当前暗区”“Evidence E1/E2”之类模型术语；
- 解释图例；
- 大面积侧边栏；
- 调试按钮；
- 长段产品原则说明；
- 传统简历式 Profile Card。

## 2. 信息按交互逐层出现

当前推荐层级：

```text
默认
宇宙本体 + 短暂 Identity Presence
    ↓ hover
星名 / Project Anchor 名 / 极短来源提示
    ↓ click
产品化节点详情：这是什么 / 来自哪里 / 和什么有关
    ↓ 查看依据
evidence / source / attribution boundary / uncertainty
    ↓ developer inspector
model version / debug / raw intermediate state
```

即：

> **远看是作品，近看是工具。**

## 3. Product Surface、Evidence 与 Developer Inspector 分层

### Product Surface｜用户表面

只放用户真正需要感受到或操作的内容。

默认节点详情不直接显示：

- “已观察”；
- 可靠度 / confidence；
- resolution；
- “现在能看到”；
- “仍然模糊”；
- “下一步”；
- Evidence 编号；
- 模型版本。

### Evidence｜解释层

用户主动打开“查看依据”后，允许查看：

- Source；
- supporting observations；
- attribution boundary；
- 必要的不确定性说明。

Evidence 必须存在，但默认收起。

### Developer Inspector｜研发层

用于：

- raw Evidence；
- intermediate outputs；
- validator decisions；
- model / schema version；
- debug information。

这一层不属于普通成品界面。

## 4. 默认节点详情保持简洁

默认详情回答三个问题：

```text
这是什么
来自哪里
和什么有关
```

例如：

```text
多架构 CI

来自 NyaMikan Runtime

NyaMikan 的 CI 覆盖 lint、类型检查、测试、shell checks，
以及 amd64 / arm64 镜像构建与 SBOM / provenance。

相关
Docker · TypeScript · Agent Runtime

查看依据  >
```

如果中文标题与英文只是机械翻译，例如：

```text
多架构 CI
Multi-arch CI
```

英文默认去重。只有英文提供额外、必要信息时才保留。

## 5. Identity Core 同时承担最低限度的身份存在感

陌生人打开页面后，应能理解：

> 这是某个人的知识宇宙。

但不能用大面积头像 / bio / 简历卡破坏 Universe-first。

推荐：

- 初次进入时，在 Identity Core 附近短暂显示名字 / handle；
- 可以带一句极短说明；
- 几秒后淡出；
- hover Core 时重新出现；
- 用户开始探索后不常驻。

详细规则见 `personal-universe.md`。

## 6. Project Anchor 进入正式视觉层

Project Anchor 是真实项目 / 经历 / 课程 / 长期实践的空间来源。

它不是 Knowledge Star，也不是技术标签。

它用于让陌生人理解：

> 这些知识从哪些真实经历里长出来？

表现应当：

- 低存在感；
- 靠近时显示项目名；
- 可弱连接到相关 Knowledge Star；
- 点击可作为进入相关 Galaxy 的空间导航；
- 不映射能力强弱或 personality。

## 7. 星体必须有自己的视觉语言

星星不能只是相同圆点换大小。

当前正式语言包括：

- tiny overexposed core；
- asymmetric elliptical halo；
- corona filament；
- restrained stellar temperature；
- soft / veiled incomplete arc；
- progressive secondary / trace presence。

这些视觉差异必须有稳定语义或纯视觉物理来源，不能为了“更炫”随意映射能力等级。

## 8. 首屏视觉语义

当前：

- **视觉存在感** → 代表性（Representativeness）与 overview plan；
- **边缘清晰度 / 核心稳定度** → 解析度（Resolution）的弱视觉表达；
- **空间距离** → 结构关联强弱；
- **局部密度 / 物质感** → Galaxy / Motif；
- **轻微动态** → 视觉生命感，可在有语义时辅助表达活跃 / forming，但不能单独升级真值；
- **Project Anchor** → 真实经历的 provenance。

能力深度不要在总览里被压成“星体大小”或“星越多越强”。

## 9. 星系边界不要像图表分组框

避免：

- 虚线椭圆；
- 卡片框；
- 明确矩形分区；
- 类似流程图的容器。

更倾向：

- 星云浓度；
- 局部背景差异；
- 星尘密度；
- 空间聚类；
- 弱标签；
- Project Anchor 与知识星形成的自然局部结构。

目标是“感知到星系”，不是“看到几个被圈起来的组”。

## 10. 最终成品禁止开发语句泄漏

以下语言只属于研发文档、Evidence 或 Developer Inspector：

- Passive-only；
- V0 / V0.1；
- 当前模型；
- Evidence E1；
- 这是一个 Prototype；
- 本图不代表……；
- 这一层用于测试……；
- 当前暗区；
- validator / repair / schema debug。

成品不应让用户感到自己正在看模型的调试页面。

## 11. 当前产品方向

Universe-first 视觉已经达到可用基线。接下来默认优先级不再是继续增加视觉效果，而是：

1. Recognition / Attribution hardening；
2. Anchor 与跨项目重复证据；
3. 时间 / trajectory；
4. 陌生用户 unseen evaluation；
5. 移动端、reduced-motion、触控、导出等产品化收尾。

> **The surface should feel personal. The evidence layer should remain accountable. Neither should impersonate the other.**
