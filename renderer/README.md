# Renderer Baseline｜正式渲染器基线

> Status: **Current implementation baseline**

`renderer/` 保存已经通过视觉验收、后续开发不得绕开的前端执行层基础。

它不是一次性的 Demo，也不是新的视觉实验目录。

## 为什么现在必须存在

前期视觉研究已经验证过一组重要结果：

- d3-force 的动态布局与拖拽手感；
- 小而克制的 point-light Knowledge Star；
- Universe → Galaxy → Secondary Knowledge → Node 的 Semantic Zoom；
- 小节点检查不移动镜头；
- 缩小只剥离语义层，不自动回中；
- Identity Core 单独承担“回到总览”；
- 关系线只在上下文中渐显；
- 背景与 Core 有独立视觉 grammar。

这些结果曾只存在于临时 HTML 实验中，导致后续页面容易重新实现一套静态布局并丢失已经验收的物理与星体语言。现在开始，接受过的行为必须先进入 `renderer/`，再继续迭代。

## 当前模块

- `physics.js` — d3-force 唯一节点物理基线；
- `star-renderer.js` — Knowledge Star 的正式 point-light 绘制函数；
- `semantic-zoom.js` — 语义缩放阈值与“不自动回中”交互规则；
- `index.js` — Renderer 公共入口。

这些代码来自已经验收过的 renderer-v1 视觉基线，而不是根据文档重新猜一套实现。

## 不可回退的实现约束

### 1. 不准重新写一套静态布局替代 d3-force

关系不仅被画出来，还参与决定空间。

正式页面必须基于 `createKnowledgeSimulation()`，除非新的物理引擎先通过独立对比并证明更好。

### 2. Knowledge Star 不是 UI 圆点

正式星体主体必须保持：

- 极小、过曝的 bright core；
- 非对称、非常弱的 elliptical halo；
- core star 只有极弱短芒；
- soft / veiled star 只允许不完整薄弧；
- secondary / trace star 与主星属于同一视觉家族，只是存在感更低；
- 不使用明显实心圆、描边球、徽章或节点卡片外观。

当前实现见 `drawKnowledgeStar()`。

### 3. 物理手感属于产品资产

当前基线：

```text
alpha       0.72
alphaMin    0.001
alphaDecay  0.024
velocityDecay 0.24
```

拖动时：

```text
simulation.alphaTarget(0.20).restart()
```

释放时去掉 `fx / fy`，保留少量 alpha 重新收敛。

不能因为制作一个新主页就把这些动态改成固定坐标。

### 4. Semantic Zoom 不得被页面级代码重写

- overview 首屏主要显示 primary nodes；
- 进入 Galaxy 并继续放大后 secondary nodes 渐显；
- 点击 Galaxy 内小星只检查，不自动 recenter；
- zoom-out 跨阈值时逐层隐藏 detail / Galaxy；
- zoom-out 不重置 camera transform；
- Identity Core 是显式 reset/home。

阈值集中在 `semantic-zoom.js`，页面不得散落第二套魔法数字。

## 开发规则

以后视觉开发顺序必须是：

```text
accepted renderer baseline
        ↓
在 renderer 模块上增加 / 修改能力
        ↓
用 Scene 数据生成页面
        ↓
验收
        ↓
将被接受的变化回收到 renderer
```

禁止：

```text
每次需求 → 新建一个完全独立 HTML → 重新实现星星 / physics / zoom
```

临时 Lab 可以独立存在，但它只能验证一个局部问题；当结果被接受后，必须先合并回 Renderer，后续页面才能依赖它。

## 与语义层的边界

Renderer 不判断一个人会什么。

它只消费已经接受的 Visual / Scene semantics，并负责稳定地把它们变成空间、交互和产品视觉。

> **Renderer is cumulative product infrastructure, not disposable prompt output.**
