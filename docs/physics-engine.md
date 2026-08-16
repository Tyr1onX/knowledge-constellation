# Physics Engine｜物理层

Knowledge Constellation 的视觉渲染与物理布局必须分离。

当前原型使用 **d3-force 3.x（通过 D3 7.9.0 bundle）** 作为唯一的节点物理引擎；Canvas 只负责星体、光、星云、标签和交互渲染。

## 当前力模型

```text
forceLink
  真实关系像弹簧一样约束相对距离

forceManyBody
  节点之间保持自然排斥，避免拥挤

forceCollide
  防止星体视觉范围互相穿透

forceX / forceY
  将节点柔和地吸引回所属 Galaxy 的空间区域
```

不再维护一套平行的自定义 spring / repel / damping 模拟。

## Drag / Reheat

拖动星体时：

```text
simulation.alphaTarget(0.20).restart()
```

让已经趋于稳定的系统重新获得能量，邻近节点可以真实响应拖拽。

松手后：

```text
node.fx = null
node.fy = null
simulation.alphaTarget(0)
```

并保留少量 alpha，让系统柔和地重新寻找平衡，而不是立即弹回原位置。

## 手感参数

当前原型：

```text
alphaDecay: 0.024
velocityDecay: 0.24
```

较低的 `velocityDecay` 用于保留一定惯性，但必须避免长期振荡。

连接距离与强度按关系设置；跨 Galaxy 的弱关系强度远低于 Galaxy 内部关系。

## 原则

> **关系不只是被画出来，关系应该参与决定空间。**

但物理层不决定视觉语义：

- 星体大小仍来自 representativeness；
- 星体形态仍来自 resolution / structural role；
- d3-force 只负责在约束下寻找自然空间布局。

未来如果替换物理引擎，应先证明新方案在拖拽响应、重新收敛、稳定性和大规模节点性能上明显更好，而不是重新手写简化 physics。
