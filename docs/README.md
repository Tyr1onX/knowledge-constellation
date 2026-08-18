# Documentation Map｜文档状态导航

仓库同时保留“当前执行规范”和“历史研究过程”。阅读时优先按下面的状态区分。

## Current contracts｜当前有效

- `../SKILL.md` — Codex 语义总契约，当前最高优先级。
- `model-spec-v1.md` — Recognition Model → Visual Model → Renderer 的正式边界。
- `identity-core-visual-grammar.md` — Identity Core 当前视觉语法、支持 family、Codex / Renderer 边界。
- `background-field-visual-grammar.md` — 背景场当前视觉语法、负空间、环境形态与动态边界。
- `knowledge-growth.md` — 无固定节点数、adaptive overview density 与自然 Semantic Zoom 揭示规则。
- `presentation-contract.md` — 面向产品表面的表达边界。
- `../renderer/README.md` — 当前 Renderer 实现基线与“禁止从零重写”连续性规则。
- `repository-checkpoint-cadence.md` — 仓库 checkpoint 规则。
- `skill-harness-v0.3.md` — Skill-first Harness 当前设计。
- `milestones/v0.3-skill-first-harness.md` — v0.3 里程碑。
- `unseen-eval-v0.3.md` — 当前 unseen-user gate。

当这些文档与更早 V0 文档产生语义冲突时，以 `SKILL.md`、`model-spec-v1.md`、`knowledge-growth.md`、`renderer/README.md` 和对应的当前专项 contract 为准。

## Current implementation assets｜当前实现资产

- `../renderer/physics.js` — d3-force 物理基线；
- `../renderer/star-renderer.js` — Knowledge Star point-light 基线；
- `../renderer/overview-visibility.js` — 首屏自适应星体密度；
- `../renderer/semantic-zoom.js` — Semantic Zoom / camera invariant / global reveal 基线。

这些文件不是实验快照。后续主页和 Renderer Runtime 必须复用 / 扩展它们。

## Research foundations｜仍然有效的研究基础

这些文档包含当前系统仍在使用的重要原则，但写作时间早于可执行 Harness：

- `principles.md`
- `attribution-model.md`
- `evidence-and-claims.md`
- `structure-model.md`
- `distillation.md`
- `visual-semantics.md`
- `uncertainty-and-time.md`
- `living-graph.md`
- `physics-engine.md`
- `star-system.md`
- `micro-calibration.md`

## Historical V0 research｜历史阶段

- `v0-knowledge-model.md`
- `evaluation.md`
- `research-notes.md`
- `../evals/round-01-report.md`
- `../evals/round-02-report.md`

这些文件记录“在正式视觉原型之前”“V0 应先验证什么”等当时正确的研究决策。它们保留作为设计 provenance，不应被理解为当前项目仍停留在那个阶段。

## Examples

- `../examples/tyr1onx/` — 早期 Passive-only 人工研究样本。
