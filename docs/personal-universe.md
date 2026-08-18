# Personal Universe｜让星图明确属于一个人

> Status: **Current product contract**
>
> Accepted checkpoint: **Personal Knowledge Constellation v3 — 2026-08-18**

Knowledge Constellation 不应该只是“某个 GitHub 账号里出现过的技术集合”。最终成品必须让陌生人也能感知：

> 这是一个具体的人留下的作品、学习、实践和判断，在空间里形成的宇宙。

## 1. Identity Core 是“这个宇宙属于谁”

Identity Core 除了作为 home / reset 与中心物理体，还承担最低限度的身份存在感。

推荐表现：

- 初次进入时，在 Core 附近短暂出现名字 / handle；
- 可以附带一句极短的说明，例如“由作品、学习与工程实践生长出的知识星图”；
- 几秒后自然淡出；
- 用户再次靠近 / hover Core 时重新出现；
- 不常驻大头像、个人资料卡、简历摘要或操作教程。

目标是让陌生人理解“这是 Erokin 的宇宙”，而不是把宇宙退化成“Profile Card + 星空背景”。

## 2. Project Anchor 是真实经历的空间来源

Structure 中的 Anchor 应允许进入正式视觉层。

Project Anchor 表达：

- 一个真实项目；
- 一段课程 / 实验经历；
- 一次长期协作；
- 一类有明确证据边界的实践上下文。

例如：

```text
NyaMikan Runtime
Repotra
Moka AI Code Mother
算法与课程实践
```

它们不是 Knowledge Star，也不是 skill badge。

Knowledge Star 回答：

> 从证据看，这个人在哪些知识 / 工程主题上留下了痕迹？

Project Anchor 回答：

> 这些痕迹是从哪些真实经历里长出来的？

因此 Project Anchor：

- 可以拥有很轻的空间标记；
- 靠近时显示项目名；
- 可以弱连接到由它支撑的 Knowledge Star；
- 点击可以作为进入相关 Galaxy 的导航动作；
- 不映射 competence / seniority / personality；
- 不应比 Galaxy 或 Identity Core 成为更强的首屏主体。

## 3. 详情卡不是 Recognition 审计报告

默认节点详情只应该回答：

```text
这是什么
来自哪里
和什么有关
```

推荐结构：

```text
多架构 CI

来自 NyaMikan Runtime

NyaMikan 的 CI 覆盖 lint、类型检查、测试、shell checks
以及 amd64 / arm64 镜像构建，并发布 SBOM / provenance。

相关
Docker · TypeScript · Agent Runtime

查看依据  >
```

以下 Recognition 内部字段不得默认堆在产品详情中：

- 已观察；
- 可靠度较高；
- confidence；
- resolution；
- “现在能看到”；
- “仍然模糊”；
- “下一步”；
- 模型版本；
- Evidence 编号。

这些信息仍然可以存在于 deeper evidence inspection，但默认收起。

## 4. 证据仍然必须可追溯

隐藏审计语言不等于删除证据。

节点详情应保留一个低存在感的“查看依据”入口，展开后可看到：

- supporting observations；
- Source / README / commit / PR；
- attribution boundary；
- 必要的不确定性说明。

产品表面负责“像一个人的宇宙”；Evidence 层负责“为什么有资格这样画”。两者都不能牺牲。

## 5. 避免无意义的双语重复

如果：

```text
多架构 CI
Multi-arch CI
```

第二行没有提供额外信息，则默认不显示。

英文只在以下情况保留：

- 中文名称可能造成歧义；
- 英文是原始项目 / 协议 / 技术正式名称；
- 双语确实帮助理解，而不是机械翻译。

## 6. “个人化”不能滑向人格推断

让页面更像“这个人的东西”，不等于从 GitHub 猜：

- 性格；
- 审美人格；
- 职业气质；
- 心理特征。

Personalization 优先来自：

```text
真实 Anchor
+ Knowledge topology
+ 时间轨迹
+ Identity label
+ stable visual seed
```

而不是“这个人看起来很神秘，所以用黑洞”。

## 7. 下一层：Trajectory

Project Anchor 解决“知识从哪里长出来”。后续 Living Graph 再解决：

> 这个人是怎么一路走到这里的？

未来可以表达：

- 首次出现 / 最近出现；
- 从课程实践迁移到个人项目；
- 同一能力跨项目重复；
- 新 Galaxy 正在形成；
- 长期稳定主线；
- 旧节点逐渐退远。

但时间结构仍然应该融入宇宙，不做成覆盖其上的传统时间轴。

> **A personal universe is not a decorated skill graph. Its identity comes from real experiences, provenance, and growth.**
