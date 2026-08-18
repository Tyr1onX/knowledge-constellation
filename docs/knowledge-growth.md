# Knowledge Growth｜知识宇宙的增长规则

> Status: **Current product contract**

Knowledge Constellation 没有固定的 Knowledge Node 数量，也没有固定的首屏星数。曾经使用的 28-node、80/160/320 stress-test 都只是验证样本，不是产品上限或默认答案。

## 1. 三个数量必须分开

```text
Knowledge Model 中有多少节点
        ≠
首屏第一眼能感知多少颗知识星
        ≠
继续缩放后最终能看到多少细节
```

Recognition 决定“证据允许我们建模多少东西”；Distillation 决定代表性；Renderer 决定在当前屏幕和缩放尺度下如何分层呈现。

## 2. 首屏密度随知识结构增长

当用户的证据和模型持续丰富时，overview 可以自然出现更多 Knowledge Star。不能因为早期基线较稀疏，就永久把首屏锁成十几颗主星。

Renderer 应综合：

- modeled node count；
- primary / secondary / trace 的比例；
- Galaxy 数量；
- 节点视觉代表性；
- 当前 viewport 容量。

得到一个 adaptive overview visibility plan。

它不是固定 `overview_node_count = 28`，也不是把所有节点一次性等亮显示。

## 3. 更多星不等于更强

视觉密度表达的是：

> 当前有多少被证据支持、值得进入个人模型的信息。

它绝不直接表达：

- competence；
- seniority；
- mastery；
- intelligence；
- employability。

一个学习轨迹丰富的学生可能拥有更多节点；一个长期专注少数领域的资深开发者可能拥有更少但更稳定的节点。

## 4. Semantic Zoom 是自然揭示，不是点击门锁

secondary / trace 的可见性由三个信号共同决定：

```text
overview presence
+ global spatial zoom reveal
+ focused Galaxy boost
```

因此：

- 有代表性的 secondary star 可以在 overview 以较弱存在感出现；
- 用户仅通过滚轮放大，就可以逐渐看到更多细星；
- 点击 Galaxy 仍可让当地细节更早、更清楚地出现；
- 但点击 Galaxy 不再是 secondary star 出现的必要条件；
- zoom-out 仍按原规则逐层剥离 detail / Galaxy，并且不自动 recenter。

这让交互保持空间连续性：用户是在“靠近一个宇宙”，而不是在切换隐藏菜单。

## 5. 宇宙增长不只意味着节点变多

如果结构证据足够，未来 Renderer 可以让增长表现为：

- 更多首屏可感知 Knowledge Star；
- 局部更密的 star cluster；
- 更复杂的 Galaxy silhouette；
- 更丰富但仍克制的 relation texture；
- 由结构触发的弱星云 / 物质感。

这些视觉变化必须来自知识结构，不得简单使用 `node_count -> cloud opacity` 的线性映射。

## 6. 长期身份保持

同一个人的星图重新生成时，应优先保留稳定 Visual Seed 和已有空间身份，让新证据表现为“宇宙继续生长”，而不是每次随机得到一个全新的宇宙。

后续 living graph 可以表达：

- new node；
- emerging Galaxy；
- trace → developing / established；
- relation strengthening；
- 长期未继续得到支持的节点逐渐退远。

> **The universe may grow. Growth is evidence richness, not a score.**
