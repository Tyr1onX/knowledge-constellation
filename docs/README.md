# Documentation｜当前文档

这里只保留**当前仍参与设计、实现或验收**的文档。已经被新契约取代的早期研究稿不再留在 `main`，需要时可直接从 Git 历史恢复。

## 先看这些

- [`../SKILL.md`](../SKILL.md) — Codex 的最高优先级语义契约。
- [`model-spec-v1.md`](model-spec-v1.md) — Source → Evidence → Model → Structure → Visual Model → Scene → Renderer 的系统边界。
- [`../renderer/README.md`](../renderer/README.md) — 当前正式 Renderer 与不可回退的交互/视觉基线。

## Recognition

- [`clean-room-evaluation.md`](clean-room-evaluation.md) — clean-room Runner + External Auditor 评测协议。
- [`knowledge-growth.md`](knowledge-growth.md) — 节点数量、overview density 与自然 Semantic Zoom 规则。
- [`calibration-loop.md`](calibration-loop.md) — 用户自然语言反馈如何作为新的第一方 Source 进入完整重跑，而不是直接改 Scene。

## Goal / Growth

- [`goal-gap-loop.md`](goal-gap-loop.md) — 从 Current Capability 到目标要求、Gap 与下一步 1–3 个行动的产品闭环。

## Product / Visual

- [`personal-universe.md`](personal-universe.md) — Identity Presence、Project Anchor 与个人宇宙产品规则。
- [`presentation-contract.md`](presentation-contract.md) — Product Surface / Evidence / Developer Inspector 的表达边界。
- [`identity-core-visual-grammar.md`](identity-core-visual-grammar.md) — Identity Core 视觉语法。
- [`background-field-visual-grammar.md`](background-field-visual-grammar.md) — 背景场与负空间视觉语法。

## Milestones

- [`milestones/v0.4-recognition-hardening-10-user.md`](milestones/v0.4-recognition-hardening-10-user.md) — 10-user Recognition Hardening gate。
- [`milestones/v0.5-e2e-runtime-foundation.md`](milestones/v0.5-e2e-runtime-foundation.md) — E2E Runner / Scene / Runtime 基础。
- [`milestones/v0.6-blind-codex-visual-validation.md`](milestones/v0.6-blind-codex-visual-validation.md) — 一句话 blind Codex 生成与人工视觉验收 checkpoint。
- [`milestones/v0.7-goal-gap-foundation.md`](milestones/v0.7-goal-gap-foundation.md) — Goal → Target → Gap → Next 1–3 Steps 的实现 checkpoint，等待真人语义验收。

> 当文档与代码或契约发生冲突时，优先级为：`SKILL.md` → `contracts/` / `prompts/` → 当前 Harness / Renderer → 本目录说明文档。
