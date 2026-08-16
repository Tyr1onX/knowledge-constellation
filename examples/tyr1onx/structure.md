# Tyr1onX Structure Draft｜结构草案

> 模式：Passive-only
>
> 只使用公开 GitHub 证据；不使用私有聊天校准。

这份文件不是最终视觉稿，而是测试：

> 从现有 Knowledge Nodes 出发，是否能够形成比“平铺技能列表”更像个人的结构。

---

## 第一眼轮廓

当前 Passive Evidence 更自然地形成三个主题，而不是“前端 / 后端 / 数据库”这样的标准分类。

```text
        开源参与与工程流转
                 ✦
        ┌────────┼────────┐
        │        │        │
     开源参与   GitHub/PR  测试与验证


          课刻与桌面产品
                 ✦
        ┌────────┼────────┐
        │        │        │
      产品迭代   Tauri    Rust / TypeScript


            Web 基础补全
                 ✦
        ┌────────┼────────┐
        │        │        │
     Web/网络   浏览器渲染  JavaScript/DOM
```

这里的 `✦` 代表主题中心，不代表能力等级。

---

# Galaxy A — 开源参与与工程流转

## Anchor

持续出现的外部 Pull Request、CI、Review、修改和合并活动。

## Primary nodes

### 开源参与 / Open-source Participation

- 代表性：高
- 证据置信度：高
- 解析度：中
- 状态：Established

为什么首层显示：

- 多次、跨项目重复出现；
- 具有外部合并和维护者反馈；
- 删除后会明显损失当前 GitHub 画像的重要部分。

边界：

- 证明持续参与，不证明具体技术实现由本人独立完成。

### GitHub / PR 工作流

- 代表性：高
- 证据置信度：高
- 解析度：中
- 状态：Established

为什么首层显示：

- 是多次贡献共同存在的结构；
- 可以解释大量活动痕迹。

边界：

- 流程暴露和参与明确；独立 Git 操作能力仍未解析。

### 测试与验证

- 代表性：中
- 证据置信度：中
- 解析度：低
- 状态：Observed

为什么仍可进入首层：

- 测试、回归、CI 在多次工程活动中重复出现；
- 它是连接外部 PR 与个人项目的一座潜在桥梁。

为什么不能显得太“亮”：

- 当前不知道测试设计、实现和判断有多少由本人完成。

## 第二层节点

- 并发 / Concurrency
- SQLite
- CAS
- WAL
- 具体平台兼容问题

这些概念虽然真实出现过，但当前主要来自具体 PR，删除它们不会显著改变第一眼人物轮廓。

---

# Galaxy B — 课刻与桌面产品

## Anchor

长期维护的 `desktop-course-widget / 课刻` 项目。

## Primary nodes

### 产品迭代 / Product Iteration

- 代表性：高
- 证据置信度：中
- 解析度：中低
- 状态：Developing

为什么首层显示：

- 项目不是一次性 Demo，而是存在持续功能、限制、测试、隐私和发布记录；
- 可以解释多个技术节点为什么会共同出现。

边界：

- 项目持续推进明确，但人在需求、设计、实现、测试各阶段的角色尚未完全解析。

### Tauri

- 代表性：中高
- 证据置信度：高（存在性）
- 能力解析度：低
- 状态：Observed

为什么可见：

- 它是长期项目的重要技术环境，对该项目的辨识度较高。

为什么不等于熟练：

- 项目使用 Tauri 不能证明本人独立掌握 Tauri。

### Rust / TypeScript

当前都具有：

- 较高 Exposure；
- 较低 Capability Resolution。

V0 需要进一步研究：

> 首层是否应该同时展示两者，还是只选择更能解释项目结构的一个，再把另一个放到第二层？

这正是 Distillation 需要解决的“信息预算”问题。

## 第二层候选

- OCR
- Windows 桌面行为
- Excel 导入 / 解析
- 本地数据
- DPI / 多显示器
- 更具体的实现技术

它们对理解项目很有价值，但首屏全部展示会把人物画像重新变成 README 词云。

---

# Galaxy C — Web 基础补全

## Anchor

公开 Learning 仓库中的持续学习记录。

## Primary nodes

### Web / 网络基础

- 代表性：中高
- 证据置信度：中
- 解析度：中
- 状态：Developing

### 浏览器渲染 / Browser Rendering

- 代表性：中
- 证据置信度：中
- 解析度：中
- 状态：Developing

### JavaScript / DOM

- 代表性：中
- 证据置信度：高（当前学习状态）
- 解析度：中
- 状态：Developing

这个 Galaxy 的特点不是“已经掌握 Web 开发”，而是：

> 当前存在一条比较明确的 Web 基础补全轨迹。

因此 Galaxy 名称使用“Web 基础补全”，而不是“Web Development”。

## 第二层候选

- HTTP 方法 / 状态码
- Cookie / Session / JWT
- XSS / CSRF / CORS
- Cache / CDN
- HTTP/2 / HTTP/3 / QUIC
- DOM / CSSOM / Layout / Paint / Composite
- script / defer / async

这些内容共同支持主干，但没必要在第一眼逐个出现。

---

# 当前被主动隐藏的节点

## 并发

隐藏原因：

- 技术复杂度高，但代表性不足；
- 主要来自少量贡献；
- 能力深度未解析。

如果把它画成一颗大星，很容易产生“本人并发能力很强”的错误暗示。

## SQLite

隐藏原因类似。

它是真实经历的一部分，但暂时不是人物轮廓的一部分。

---

# 当前不能出现的核心主题

## AI-assisted Development

Passive GitHub 证据不足以判断 AI 的实际参与程度，所以当前不能把它自动建立为 Galaxy。

这不是说它不存在，而是说：

> **Passive-only 系统目前没有资格知道。**

这类主题可能通过一次高信息量 Micro Calibration 被揭示出来，并使整张结构重新组织。

---

# 对这一版结构的三个检查

## 1. Removal Test｜删除测试

如果删除：

- CAS；
- SQLite；
- WAL；

人物轮廓基本不变。

如果删除：

- 开源参与；
- 课刻与桌面产品；
- Web 基础补全；

人物轮廓会发生明显变化。

说明后一组更适合第一眼。

## 2. Syllabus Test｜课程目录测试

当前结构没有使用：

```text
前端 / 后端 / 数据库 / 编程语言
```

作为默认 Galaxy，因此仍然是在描述个人轨迹，而不是套统一技能树。

## 3. Honesty Test｜诚实测试

当前最危险的节点是：

- Rust；
- TypeScript；
- Tauri；
- 测试与验证。

它们具有真实 Exposure 和人物相关性，但能力解析不足。

最终视觉必须能够让它们“明显存在”，同时避免产生“已经熟练掌握”的视觉暗示。

---

# 暂时结论

Passive-only 下，这三个 Galaxy 已经比完整节点列表更接近一个人的轮廓：

1. **开源参与与工程流转**
2. **课刻与桌面产品**
3. **Web 基础补全**

但它仍然只是“公开痕迹里的这个人”。

一次高价值校准有可能揭示一个跨越多个 Galaxy 的新主题，并使结构重新排列。
