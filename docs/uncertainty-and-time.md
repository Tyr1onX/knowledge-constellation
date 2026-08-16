# Uncertainty & Time｜冲突、不确定性与时间

Round 02 发现：即使每条证据本身都正确，不同证据也可能描述**不同维度、不同时间点、不同角色**。

如果模型粗暴地把它们“平均”成一个技能等级，仍然会把人画错。

---

# 1. 先判断是不是“真的矛盾”

例如：

```text
有两个 React 项目
+
JavaScript closure 仍在学习
```

这并不必然矛盾。

它可能同时说明：

```text
React / 项目 exposure         高
产品实践                      存在
JavaScript implementation     部分存在
JavaScript understanding      有明显边界
independence                  未解析
```

因此遇到表面冲突时，第一步不是选一个“更可信的”，而是检查：

> **它们是不是其实在描述不同 Claim Type？**

只有当两条证据对**同一维度、同一时间范围、同一对象**给出不兼容判断时，才进入真正的 Conflict。

---

# 2. Conflict Ledger｜冲突记录

真正冲突的证据不要静默平均，也不要强行挑一个。

内部保留：

```yaml
conflict:
  target: javascript.independence
  evidence_for:
    - resume_claim
  evidence_against:
    - fresh_behavioral_task
  resolution: unresolved
  suggested_calibration: true
```

在没有足够信息时，更合理的输出是：

> 当前资料对这一点存在冲突，解析度较低。

而不是：

> 综合来看，你是中级。

---

# 3. Evidence Precedence 不是固定排行榜

不能简单规定：

```text
behavioral > external > self_report > artifact
```

因为证据支持的内容不同。

例如：

- 一次 behavioral task 只能证明那个任务与当时状态；
- 三年真实实现记录对长期实践很强；
- 证书对考试覆盖知识很强，但对生产实践很弱；
- 用户自述对“谁实际做了什么”有时是唯一直接来源。

所以选择证据时看：

1. 是否直接对应当前 Claim；
2. 时间是否匹配；
3. Attribution 是否清楚；
4. 是否有跨源佐证；
5. 证据覆盖范围有多大。

---

# 4. Time 不能偷偷变成“技能衰减分数”

历史深度和当前活跃度是两件事。

例如：

```text
2020：Java / Spring 深度实践
2026：四年几乎未使用
```

不能变成：

```text
Java skill = 30%
```

也不能删除历史事实。

至少拆成：

```text
historical_evidence_strength: high
current_activity: low
current_resolution: medium
```

如果有新的行为证据，可以进一步描述当前保留程度。

---

# 5. Activity State｜活动状态

V0.7 增加与 Knowledge State 分离的时间字段：

```text
active       当前持续出现
recent       最近阶段出现，但不是持续主线
historical   过去有明确证据，目前较久未出现
unknown      无法判断当前性
```

它回答：

> 这部分现在还在这个人的生活 / 学习 / 工作中活跃吗？

而不是：

> 这个人会不会？

因此一个节点完全可以是：

```yaml
label: Java / Spring
state: established
activity_state: historical
```

表示：

> 历史能力证据很强，但当前不是活跃方向。

---

# 6. Recency 在视觉上只表达“现在性”

未来视觉层可以让：

- active 节点有更明显的动态或更靠近当前中心；
- historical 节点稍远、运动更慢或进入时间层；

但不能通过“变暗到像不会了”表达历史状态。

否则用户会把视觉上的时间变化误读成能力下降。

---

# 7. Certification｜证书证据必须限定范围

一个可验证证书可以支持：

- 用户在某个时间点通过了对应测评；
- 对考试覆盖范围存在结构化学习与外部验证。

它不能自动支持：

- 生产环境经验；
- 独立系统设计；
- 故障处理；
- 长期记忆稳定性。

因此证书 Evidence 应带：

```text
assessment_scope
issued_at
```

必要时还有：

```text
expires_at / validity
```

如果证书本身没有过期规则，也不能由系统擅自创造。

---

# 8. Collaboration｜代码量不是贡献量

团队项目中：

```text
commit 占比 8%
```

不能直接得到：

```text
贡献度 8%
```

因为用户可能主要承担：

- 需求定义；
- Review；
- 验收；
- 发布判断；
- 用户测试；
- 风险控制。

同样，代码很多也不自动证明：

- 架构决策；
- 产品判断；
- 独立设计。

Commit / LOC 只能作为 Activity Trace，不是通用价值权重。

---

# 9. Calibration 的优先级

如果出现真正冲突，Micro Calibration 的价值会明显升高。

优先询问那些：

- 同时影响多个 Claim；
- 当前证据真的互相冲突；
- 用户只需一个低成本选择即可澄清；
- 会明显改变星系结构或视觉表达。

例如：

> 你现在做 React 项目时，更接近哪一种？
>
> A. 主要依赖 AI / 模板，我负责需求和验收  
> B. 我能阅读并修改主要代码，但底层 JS 仍在补  
> C. 大部分实现可独立完成，AI 只是辅助  
> D. 不同项目差异很大 / 不好判断

这种问题比问“你是不是中级前端”信息量更高。

---

# 10. 视觉层必须同时容纳“强历史 + 低近期”

最终星图需要能够表达这种状态：

```text
这个东西曾经非常构成我
但现在不是我的主要活动
```

而不是只允许：

```text
会 / 不会
亮 / 暗
```

这也是 Knowledge Constellation 与传统 Skills Matrix 的一个重要区别：

> **它画的是一个有时间的人，而不是一个静态能力表。**
