# Knowledge Constellation Skill｜知识星图 Skill

> 状态：研究占位（research placeholder），目前还不是稳定可执行的正式 Skill。

最终目标是：把用户提供的已有资料，转换成一份**基于证据、保留不确定性、可以逐渐校准**的个人知识星图。

当前阶段故意先验证“如何认识一个人”，而不是急着把所有规则塞进一个巨大 Prompt。

## 默认语言

- 默认输出语言：`zh-CN`；
- 用户明确要求时支持英文 `en`；
- 专有概念可以保留中文 + 英文，例如“归因（Attribution）”；
- 内部结构字段可以使用英文，面向用户的解释默认中文。

## 计划中的高层行为

```text
用户已有资料
↓
提取可观察证据
↓
保留归因不确定性
↓
形成有边界的 Claim
↓
压缩成 Knowledge Node
↓
生成保守但完整的第一张星图
↓
可选：低成本 Micro Calibration
```

## V0 暂时不做什么

V0 不应该：

- 根据仓库技术栈直接生成漂亮的熟练度分数；
- 因为项目或 PR 很复杂，就自动判断用户掌握其中技术；
- 在第一份结果之前强迫用户完成长问卷；
- 把“参与活动”静默升级成“本人执行”；
- 把未知作者归因默认为本人能力；
- 尝试一次画出一个人的全部知识；
- 在 Knowledge Model 尚未验证前锁死最终视觉形式。

## 正式 Skill 之前必须验证

至少需要多个真实案例确认：

1. Evidence 提取是否稳定；
2. Attribution 边界是否足够保守；
3. Participation 与 Execution 是否能被正确区分；
4. Claim 是否始终能倒查到 Evidence；
5. 节点粒度是否像“这个人”，而不是标准课程目录；
6. Passive-only 结果即使有大量未知，是否仍然有价值；
7. Micro Calibration 是否真的能用少量操作明显改善模型；
8. 中文默认输出是否足够自然、易读。

当前协议见：

- `docs/principles.md`
- `docs/v0-knowledge-model.md`
- `docs/attribution-model.md`
- `docs/micro-calibration.md`
