# Renderer Baseline｜正式渲染器基线

> Status: **Current implementation baseline**
>
> Accepted visual checkpoint: **Detail Polish v1 — 2026-08-17**

`renderer/` 保存已经通过视觉验收、后续开发不得绕开的前端执行层基础。它不是一次性的 Demo，也不是新的视觉实验目录。

## 当前已正式沉淀的视觉资产

- `physics.js` — d3-force 唯一节点物理基线；
- `star-renderer.js` — Knowledge Star 的 point-light 形态 + Detail Polish 微观动态；
- `stellar-color.js` — 受控、物理启发的恒星色温；
- `identity-core-physics.js` — 有中心势阱、非线性阻力、回中与邻近星体扰动的 Core 物理；
- `identity-core-renderer.js` — 8 个已验收 Identity Core family 的动态绘制；
- `background-field.js` — Pure Black + Ambient Space 背景实现；
- `semantic-zoom.js` — 语义缩放阈值与“不自动回中”交互规则；
- `index.js` — Renderer 公共入口。

## 不可回退的实现约束

### 1. d3-force 是正式物理层

关系不仅被画出来，还参与决定空间。正式页面必须继续基于 `createKnowledgeSimulation()`，除非新物理方案先通过独立对比并证明更好。

当前节点物理基线：

```text
alpha          0.72
alphaMin       0.001
alphaDecay     0.024
velocityDecay  0.24
```

拖动知识星时 reheat，松手后重新收敛。

### 2. Knowledge Star 不是 UI 圆点

正式星体保持：

- 极小、过曝的 bright core；
- 非对称、很弱的 elliptical halo；
- 极轻的 corona filament / 微观漂移；
- core star 只有弱短芒；
- soft / veiled star 使用不完整、缓慢进动的薄弧；
- secondary / trace 与主星属于同一视觉家族，只降低存在感；
- 不使用明显实心圆、描边球、徽章或节点卡片外观。

### 3. 恒星色温只属于视觉物理

`stellar-color.js` 根据稳定 node id 产生 deterministic `temperatureK`，再近似转换为恒星色。

它**绝不映射**：

- 能力强弱；
- 熟练度；
- seniority；
- 技术类别；
- personality。

大多数 Knowledge Star 必须留在暖白 / 白 / 冷白区域，只有少部分明显偏暖或蓝白。中心始终接近过曝白色，不能退化成彩色 UI 点。

### 4. Identity Core 是有质量的中心体

Core 不是可以任意拖到世界角落的 draggable element。

当前正式行为：

- 有固定 equilibrium point；
- 近距离基本跟手；
- 距离越远阻力越大；
- 位移渐近接近最大活动半径；
- 松手后高阻尼回中，不反复弹跳；
- 位移通过 `identity-core-field` 注入现有 d3 simulation；
- 周围知识星会被带动，再在 link / charge / collide / Galaxy anchor 下重新收敛。

当前关键参数：

```text
freeRadius       18
maxRadius        82
resistanceScale  95
homeSpring       0.032
homeDamping      0.79
maxReturnSpeed   2.6
```

### 5. Identity Core family 是视觉语法，不是头像模板

当前 family：

```text
monogram
 eclipse
quiet_star
minimal_ring
black_hole
pulsar
binary_star
protostar_nebula
```

共同原则：一个 family 只有一个明确主视觉主体；motion 来自天体形态本身，不用 personality / competence stereotype 选型。

当前动态包括：

- monogram：身份文字稳定，内部材料、双层场环、边缘 glint 缓慢运动；
- eclipse：亮边沿遮挡体轮廓绕行；
- quiet star：轻微光变与衍射旋转；
- minimal ring：完整弱轨道 + 沿轨运行的亮弧和锚点；
- black hole：吸积盘物质持续运行并保留前后层次；
- pulsar：双向束流 + 周期发射 + 沿轴向外传播的 pulse packets；
- binary star：两颗星围绕共同中心相位相反公转；
- protostar nebula：云气和吸积结构缓慢漂移。

### 6. 背景是 atmosphere，不是第二个主题

当前 quality-gated family 只有：

- `almost_empty`；
- `cold_filament`；
- `broken_cloud`。

Rare meteor 是 Renderer-owned ambient event，不是 `dust_family`。

纯黑始终占主导，背景不能比知识结构形成更强的第一屏轮廓。云气允许非常慢的局部漂移，但不得变成动态壁纸。

### 7. Semantic Zoom 不得被页面级代码重写

- overview 首屏主要显示 primary nodes；
- 进入 Galaxy 并继续放大后 secondary nodes 渐显；
- 点击 Galaxy 内小星只检查，不自动 recenter；
- zoom-out 跨阈值时逐层隐藏 detail / Galaxy；
- zoom-out 不重置 camera transform；
- Identity Core 是显式 reset/home。

## 开发规则

以后视觉开发必须是：

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
每次需求 → 新建一个完全独立 HTML → 重新实现 stars / physics / Core / background / zoom
```

Lab 可以独立存在，但只用于验证一个局部问题；一旦通过验收，结果必须先回收到 Renderer，下一版页面再继续。

## 与语义层的边界

Renderer 不判断一个人会什么。它只消费已经接受的 Visual / Scene semantics，并稳定地把它们变成空间、交互和产品视觉。

> **Renderer is cumulative product infrastructure, not disposable prompt output.**
