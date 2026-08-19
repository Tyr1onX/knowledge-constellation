# Calibration Loop｜自然语言校准

> Status: **Current product contract**

Knowledge Constellation 的第一版应该在**不提问**的情况下直接给出一个有用结果；校准发生在用户看到结果之后。

用户不需要编辑 JSON，也不需要理解 Evidence、Claim 或 Scene。正常交互应该只是：

```text
“这个其实主要是 AI 做的，我负责 review 和验证。”
“Rust 没有你画得那么强，我目前主要是在课刻里接触。”
“7BYTE 对我更重要一些。”
```

## 1. 校准不是手工改图

任何用户反馈都不能直接 patch `model.json`、`structure.json`、`visual.json` 或 `scene.json`。

正确链路：

```text
已有 accepted input
+ 用户自然语言反馈
↓
追加一个 kind = user_calibration 的第一方 Source
↓
重新执行 Pass A / B / C / D
↓
validator / repair
↓
Scene Composer
↓
canonical Renderer
```

这样可以让归因、边界、结构和最终视觉保持一致，而不是只把表面画面“改得像用户说的”。

仓库实现入口：`harness/recalibrate.py`。

## 2. 两类校准

### Truth Calibration

纠正“事实和归因”：

- 谁真正实现了什么；
- 哪部分由 AI / 协作者完成；
- 用户负责的是选择、review、验证还是实现；
- 当前处于学习、接触、实践还是更稳定的理解状态；
- 原结果是否把依赖、参与或系统描述错误归到了本人。

来自主体本人的负向 / 边界性纠正，是非常重要的直接 Evidence，应优先阻止过度归因。

但一句“我很精通 X”不能单独绕过 Stronger claims need stronger evidence：自我声明可以成为 Source，但强能力 Claim 仍需要与其强度匹配的行为证据。

### Identity Calibration

纠正“什么更像我”：

- 某个项目更重要；
- 某条学习主线更能代表当前状态；
- 某个主题只是偶然出现，不应占据首屏中心。

这类反馈可以改变 `representativeness`、primary / secondary 层和有限的视觉权重，但**不能升级 capability truth**。

“对我重要”不等于“我更擅长”。

## 3. 累积而不是覆盖

每次校准都作为新的 `user_calibration` Source 加入 accepted input。后续校准从上一版 accepted input 出发，因此历史反馈会累积保留。

相同反馈使用稳定哈希 ID，重复提交不会无限复制相同 Source。

新 revision 仍然从 Pass A 开始重新 Recognition；旧的 accepted semantic artifacts 只作为历史产物存在，不作为新一轮语义输入。

## 4. 产品表面

普通用户不需要看到“Truth Calibration / Identity Calibration”这些术语。

产品语言只需要是：

> 哪里不对，直接告诉 Codex。

Codex 负责把自然语言反馈转换成新的第一方 Source，再完整重跑生成流程。

## 5. 不可回退边界

- 不把反馈转成关键词规则；
- 不让 Harness 判断用户掌握了什么；
- 不直接移动星体来“满足反馈”；
- 不用用户偏好提高 competence；
- 不因 AI 参与就抹掉已被证据支持的人类 review / judgment / validation；
- 不因用户自称精通就跳过强主张的证据要求。

> **Calibration changes the evidence context, then Recognition changes the universe. It does not edit the universe around Recognition.**
