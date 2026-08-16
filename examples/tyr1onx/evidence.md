# Tyr1onX 被动证据样本｜Passive Evidence Sample

这是 Knowledge Constellation 的第一份真实 V0 案例。

## 实验约束

这份样本故意只使用 **公开 GitHub 痕迹**。

不使用：

- 私有聊天历史；
- 私下自述；
- 额外校准答案；
- 对本人技术能力的乐观猜测。

目的只有一个：

> **测试 Passive-first 系统在完全不询问用户时，最多能安全地认识到什么程度。**

快照日期：2026-08-16。

---

# Sources｜来源

## S1 — GitHub Profile README

`Tyr1onX/Tyr1onX`

观察到：

- 主页重点展示 `desktop-course-widget`、`Tyr1onX.github.io`、`accounting-excel-tool`；
- 公开说明参与 EGC 协作；
- 展示多项外部已合并 Pull Request。

证据边界：

这是用户主动整理的公开自我展示，适合发现重要项目与活动，但其中的能力判断最好继续由仓库、PR、Review 或外部结果验证。

---

## S2 — Desktop Course Widget｜课刻

`Tyr1onX/desktop-course-widget`

从公开 README 观察到：

- 存在一个持续维护的 Windows 桌面课表产品；
- 技术环境包括 Tauri 2、Rust、Vite、Vanilla TypeScript、HTML/CSS、Calamine；
- 产品包含 Excel 导入、截图/OCR 开发路径、多课表、桌面集成、本地存储等功能；
- 仓库明确记录测试命令、隐私说明、版本限制与开发规范。

归因边界：

仓库所有权和持续维护能强力证明：

- 项目与用户高度相关；
- 用户真实接触过这些技术环境和产品问题。

但不能单独证明：

- 每项实现由用户独立完成；
- 用户已经掌握 Rust / TypeScript / Tauri 等技术。

---

## S3 — Learning Repository｜学习仓库

`Tyr1onX/Learning`

观察到：

- 仓库专门记录当前学习状态，而不只是最终成果；
- 状态包括 `not-started`、`learning`、`understood`、`review-needed`、`interview-ready`；
- Web / Network / Browser 等主题存在结构化学习记录；
- JavaScript / DOM 明确记录为当前学习中；
- Framework、Backend、Database、OS/Linux 和部分算法仍被明确标记为未系统学习或需要复习。

证据边界：

这是高质量的结构化学习证据，但不是第三方独立考试。

可以支持：

- 这些内容确实被系统学习过；
- 当前学习边界相对明确。

不能直接支持：

- 长期记忆稳定；
- 新场景下能够独立迁移；
- 专业级能力。

---

## S4 — EGC PR #1271

`Fmarzochi/EGC#1271`

观察到：

- PR 处理 overlapping readers 下的 exactly-once session event delivery；
- 最终方案涉及 cursor compare-and-swap；
- 增加了使用 SQLite WAL 的多进程 chaos harness；
- 维护者明确确认修复正确，并以 full credit 合并；
- 维护者称这是该贡献者的第 11 次贡献。

归因边界：

这可以强力证明：

- 用户真实参与了一项外部开源贡献；
- 该交付结果通过了外部维护者接受；
- 存在持续贡献历史。

公开 GitHub 不能回答：

- 分析是否由本人完成；
- 实现是否由本人完成；
- 测试是否由本人设计；
- 用户能否在新场景下独立解释 CAS、SQLite WAL 或并发原理。

因此这类技术默认只应增加 **Exposure（接触）**，不能直接增加独立 Capability。

---

## S5 — 其他外部 Pull Requests

公开贡献中还出现过：

- EGC 安装、集成和 Dashboard 问题；
- polling / reconnect / regression；
- QQ Chat Exporter 的 Windows/Linux 兼容、ESM 启动、scheduler 校验、分页、认证文档与测试；
- Avenx 的自定义 HTTP headers 支持。

证据边界：

反复出现的外部 PR 能比单个 PR 更强地支持“持续开源参与”和“真实工程环境暴露”。

但其中出现的每项技术仍然不能直接升级为个人掌握。

---

# Normalized Evidence｜归一化证据

## E1 — 持续外部贡献活动

```yaml
kind: activity
observation: 存在跨多个外部项目的 Pull Request 活动，其中包含多项已合并贡献。
attribution: direct
confidence: high
```

可以支持：

- 持续开源参与；
- GitHub / PR 工作流暴露；
- 反复进入真实项目约束。

不能证明：

- 每项贡献由本人独立实现；
- 贡献涉及的技术均已掌握。

---

## E2 — EGC #1271 外部验证

```yaml
kind: external_validation
observation: 维护者确认 exactly-once 修复正确，以 full credit 合并，并称其为第 11 次贡献。
attribution: external
confidence: high
```

可以支持：

- 真实贡献结果获得外部接受；
- 持续贡献历史不是只有本地成果。

不能证明：

- 本人独立掌握 CAS、Concurrency 或 SQLite WAL。

---

## E3 — 测试 / 回归语言反复出现

```yaml
kind: activity
observation: 多项公开 PR 描述中反复出现 regression test、CI、edge case、真实环境验证等内容。
attribution: direct
confidence: high
```

可以谨慎支持：

- Testing / Validation 确实长期存在于工程活动中；
- 用户反复接触测试、回归和 CI 流程。

仍然未知：

- 测试是谁设计和实现的；
- 用户本人能否判断覆盖是否充分；
- 独立测试能力深度。

因此这一证据首先支持 **Exposure / Participation**，而不是直接支持 Testing Capability。

---

## E4 — 持续维护的复杂桌面产品

```yaml
kind: artifact
observation: 存在一个持续维护的 Windows 桌面课表产品，包含多技术栈、导入流程、桌面行为、本地数据、测试、隐私和发布规范。
attribution: uncertain
confidence: high
```

可以支持：

- Product / Project exposure；
- 与 Tauri、Rust、TypeScript、Windows desktop、Excel parsing、OCR 等问题存在真实接触。

不能证明：

- 这些能力由本人独立实现；
- 对任一底层技术具备独立掌握。

---

## E5 — Web / Network / Browser 结构化学习记录

```yaml
kind: learning_record
observation: 学习仓库记录多个 Web、Network、Browser 主题为 understood，同时明确保留薄弱项与未开始项。
attribution: direct
confidence: high
```

可以谨慎支持：

- 存在主动、持续、结构化学习；
- Web / Network / Browser 已形成一定知识结构。

不能证明：

- 长期无提示回忆稳定；
- 专业深度；
- 在真实新问题中的迁移能力。

---

## E6 — JavaScript / DOM 当前学习中

```yaml
kind: learning_record
observation: JavaScript 基础和 DOM 明确被记录为 learning，而不是 established。
attribution: direct
confidence: high
```

可以支持：

- JavaScript / DOM 应该进入当前星图；
- 它们属于正在形成的知识，而不是成熟能力。

---

# Passive Evidence 当前无法回答什么

仅靠公开 GitHub，当前无法可靠回答：

- 个人项目或外部 PR 中有多少代码由本人独立完成；
- AI Agent 的真实参与程度；
- 分析、实现、测试、Review 分别由谁承担；
- 用户脱离 AI 后能够复现多少项目级推理；
- Rust、TypeScript、Tauri、Concurrency、SQLite 等内容的真实理解深度；
- Learning 仓库中的历史状态在间隔一段时间后是否仍然稳定。

这些 Unknown 不是模型失败。

它们是 V0 输出的一部分，也是未来 Micro Calibration 最有价值的目标。
