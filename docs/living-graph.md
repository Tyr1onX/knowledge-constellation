# Living Graph｜流动图谱

这一轮视觉研究引入一个新的核心方向：

> **Knowledge Constellation 不应该只是“静态星图 + Hover 动画”，而应该是一套受结构关系约束、会重新寻找平衡的活体系统。**

## 为什么参考 Obsidian Graph

Obsidian 官方 Graph View 公开提供一组力学参数：

- Center force：让图保持整体收拢；
- Repel force：节点之间互相排斥；
- Link force：链接像橡皮筋一样拉住节点；
- Link distance：控制节点间的目标距离。

参考：

- https://obsidian.md/help/plugins/graph

它的重要启发不是“节点长得像圆点”，而是：

> **结构本身会动。**

用户拖动一个节点以后，邻近结构被牵动；松手以后，系统在连接、排斥和整体约束之间重新取得平衡。这种变化会让图谱显得有机，而不是预先排好位置的 UI 元素。

---

## V3 的物理模型

当前原型先实现一个轻量级自定义 force simulation：

```text
Galaxy attraction
星系中心吸引

Node repulsion
节点排斥

Link spring
关系弹簧

Damping
阻尼

Very small tangential drift
极弱切向漂移
```

### Galaxy attraction｜星系吸引

每颗星仍然属于某个 Primary Galaxy，但不是被固定死在某个坐标。

星系中心只提供一个较弱吸引力，让同一主题保持聚集。

### Node repulsion｜节点排斥

节点之间互相推开，避免所有星体重叠在中心。

同一星系内的排斥可以略强，让局部形成自然间距。

### Link spring｜关系弹簧

真实 Relation 会产生弹性约束。

不是简单画一条线，而是：

> 两颗星的关系会影响它们最终停在哪里。

这样 Structure Model 开始真正影响空间，而不是只影响配色和标签。

### Damping｜阻尼

系统不会无限振荡。

拖动结束后，结构会逐渐重新稳定。

### Micro drift｜微漂移

完全稳定以后如果所有节点彻底静止，会重新变成普通图谱。

因此允许非常小的切向漂移，让系统保持呼吸感，但不能让用户感觉整个布局不断乱跑。

---

## 拖拽语义

V3 支持两种 Drag：

```text
拖背景
→ 平移整个宇宙

拖星体
→ 临时固定该节点到鼠标位置
→ 连接星体被弹簧牵动
→ 松手后节点重新进入物理系统
```

拖动星体不是一个编辑操作。

它更像：

> **用户短暂扰动这个宇宙，观察结构如何回应。**

因此不能永久修改 Knowledge Model。

---

## 背景减法

上一版的问题是：大量相似亮度的小灰点会产生“屏幕积灰”的视觉错觉。

V3 强制执行：

- 大幅减少背景星数量；
- 提高亮度差异，而不是均匀灰度；
- 星云只使用极低透明度的大尺度暗色结构；
- 不再用大量微尘填满空白；
- 保留真正的黑色空间。

原则：

> **深空首先是空，其次才是星。**

---

## 为什么不用 Obsidian 的布局直接复制

Knowledge Constellation 和笔记关系图不同。

Obsidian 的边来自显式链接，因此可以让全图由 link graph 自由收敛。

我们的 Relation 有更复杂语义：

- Knowledge Node 有 Primary Galaxy；
- Galaxy 来自 Anchor / Motif；
- 代表性与能力不同；
- 某些节点只是外围痕迹；
- 跨星系关系不应该把两个主题直接揉成一团。

所以我们采用：

```text
Force-directed behavior
+
Semantic galaxy constraints
```

也就是：

> **借 Obsidian 的“活”，但不借它的知识结构定义。**

---

## 后续视觉方向

### 1. Force tuning

目前最需要调的是：

- 弹簧强度；
- 阻尼；
- 排斥半径；
- 星系吸引；
- 拖拽释放后的回弹速度。

目标不是模拟真实天体物理，而是让交互有自然的“软弹性”。

### 2. Spatial hierarchy

缩放以后再逐步显示：

- 第二层星体；
- 标签；
- 局部关系；
- Evidence / explanation。

### 3. Visual cleanliness

背景细节必须始终服从可读性。

如果用户开始怀疑屏幕是不是脏了，就说明背景已经失败。

---

## 当前原则

> **关系不只是被画出来，关系应该参与决定空间。**

这会成为后续 Knowledge Constellation 视觉实现的一条核心规则。
