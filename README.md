# Knowledge Constellation｜知识星图

> 用证据认识一个人，再把这种认识变成一片可解释、可探索、会持续生长的个人知识宇宙。

Knowledge Constellation 是一个 **Skill-first** 项目。它不把 GitHub 技术栈、简历关键词或项目依赖直接翻译成“技能等级”，而是让 Codex 在明确的 Recognition Contract 下完成语义判断，再由 Harness 负责隔离、验证和 repair。

## 当前状态

当前稳定主线是 **Codex-in-the-loop semantic harness + cumulative Renderer baseline**。

视觉与交互已经形成可用产品基线：

- Detail Polish — point-light Knowledge Star、恒星色温、动态 Identity Core、Ambient Space；
- Growing Universe — 无固定节点数、adaptive overview density、滚轮自然显现 secondary / trace；
- Personal Universe — Identity Presence、Project Anchor、去审计化默认详情、Evidence 二级展开。

因此当前主要研发阶段正式转向：

> **Recognition Hardening — 更准确地认识一个人。**

重点不再是继续增加视觉特效，而是减少错误归因、区分依赖 / 参与 / 实现 / 判断、识别真实 Anchor、加强跨项目重复与时间轨迹，并用更多陌生用户做 unseen evaluation。

当前系统边界：

- 根 `SKILL.md` 是 Codex 的统一语义契约；
- Pass A/B/C/D 依次产生 Evidence → Model → Structure → Visual Model；
- Harness 只负责 orchestration / schema / semantic validation / repair；
- `renderer/` 保存所有已经验收的视觉与交互执行基线；
- 每个 Pass 使用隔离 workspace，避免读取 tests、历史 examples 或其他人的 fixture；
- 强 implementation / independence / troubleshooting / transfer Claim 需要多组独立证据，并要求多来源 provenance 或 external validation；
- 早期研究文档、Tyr1onX Passive-only 样本和 unseen-evaluation 结论继续保留，作为设计 provenance。

项目仍处于研究型产品阶段，不宣称存在一个可泛化到所有人的“准确率”。当前评估更关注可审计的错误：有没有吹高能力、把依赖当掌握、把学习中写成 established、把单份自述伪装成多份独立验证等。

## 架构边界

```text
Raw Sources
    ↓
Codex + SKILL.md
    ↓
Pass A — Evidence
    ↓ validate / repair
Pass B — Claims + Knowledge Nodes
    ↓ validate / repair
Pass C — Anchors + Relations + Galaxies + Distillation
    ↓ validate / repair
Pass D — Personal Visual Model
    ↓ validate / repair
Scene semantics
    ↓
Renderer baseline
    ↓
Knowledge Constellation
```

职责必须保持清晰：

- **Codex**：理解、归因、Claim、Knowledge Node、Anchor、Relation、Galaxy、Distillation、Visual Model；
- **Harness**：输入组织、Schema、状态机、隔离、验证、repair、持久化；
- **Renderer**：Scene / Canvas / d3-force / Knowledge Star / Semantic Zoom / Identity Core / Project Anchor / 背景环境 / 产品表面。已验收的执行层必须累积在 `renderer/`，页面不得重新实现一套平行版本。

如果 Python 开始通过关键词表自动创建 Rust / React / Database 节点，架构就退化了；如果每个新页面重新实现 stars / physics / zoom / anchors，视觉层同样退化了。

## 核心原则

- Evidence before inference；
- Artifact ≠ mastery；
- Participation ≠ execution；
- Assistance ≠ erasure；
- Dependency is provenance, not personal knowledge；
- Unknown is valid；
- stronger claims require stronger and more independent evidence；
- representativeness ≠ capability；
- more stars ≠ stronger person；
- Galaxy 描述个人真实主题，而不是默认课程目录；
- Project Anchor 描述真实经历来源，而不是另一种 skill badge。

完整规则见 [`SKILL.md`](SKILL.md) 和 [`docs/model-spec-v1.md`](docs/model-spec-v1.md)。

## 快速验证

需要 Python 3.10+：

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m py_compile harness/pipeline.py harness/validate.py
```

准备一份符合 `contracts/input.schema.json` 的输入。仓库提供最小例子：

```bash
cp examples/input.example.json input.json
python harness/pipeline.py init --input input.json --run runs/demo
python harness/pipeline.py next --run runs/demo
```

`next` 会生成一个隔离 workspace，只包含：

- `SKILL.md`
- `ORCHESTRATION.md`
- 当前 Pass Prompt
- 当前 Schema
- 已验收上游结果
- `TASK.md`

Codex 在 workspace 中写 `output.json`，然后执行：

```bash
python harness/pipeline.py validate --run runs/demo
```

Validator 只能接受或拒绝，不能替 Codex 生成语义答案。失败后再次 `next` 会进入 repair 模式；默认每个 Pass 最多两次 repair。

## 当前评估

早期 Tyr1onX 样本保留在 `examples/tyr1onx/`，用于说明 Evidence / Model / Structure 是如何形成的。

`docs/unseen-eval-v0.3.md` 记录了当前公开 unseen-user gate：单项目型、学习型学生、Android 工具链学习轨迹、职业型开发者等案例。它们用“不能错误推断什么”作为主要 guard，而不是假装存在唯一主观标准答案。

接下来的 Recognition Hardening 会扩大陌生用户样本，并重点审计：

- 依赖 ≠ 掌握；
- 课程 / 模板 / 复刻 / 协作 / AI-assisted 的归因差异；
- 跨独立项目的重复证据；
- 调试、取舍、review、验证等 judgment traces；
- Anchor 是否真的是个人经历，而不是技术分类；
- 时间持续性与迁移。

## 视觉层状态

旧的 `prototype/index.html` 已从当前树中移除，因为它不再代表产品。历史版本仍可从 Git 历史恢复。

当前正式 Renderer 已包含：

- `renderer/physics.js` — d3-force 力模型与 drag/reheat；
- `renderer/star-renderer.js` — point-light Knowledge Star；
- `renderer/stellar-color.js` — 受控恒星色温；
- `renderer/overview-visibility.js` — adaptive overview density；
- `renderer/semantic-zoom.js` — global natural reveal 与 camera invariants；
- `renderer/identity-core-physics.js` — Core 中心势阱与节点耦合；
- `renderer/identity-core-renderer.js` — 8 种 Identity Core；
- `renderer/identity-presence.js` — 短暂身份存在感；
- `renderer/project-anchor.js` — 真实项目 / 经历 provenance；
- `renderer/presentation.js` — 默认详情去审计化与 Evidence disclosure；
- `renderer/background-field.js` — Pure Black + Ambient Space。

视觉 contract 继续由：

- `docs/model-spec-v1.md`
- `docs/presentation-contract.md`
- `docs/knowledge-growth.md`
- `docs/personal-universe.md`
- `docs/physics-engine.md`
- `docs/star-system.md`
- `docs/identity-core-visual-grammar.md`
- `docs/background-field-visual-grammar.md`

共同约束。

新的主页、Scene Composer 或完整 Runtime 必须建立在 `renderer/` 上，而不是重新从空白 HTML 开始。

## 仓库结构

```text
SKILL.md                 Codex 语义入口
contracts/               A/B/C/D JSON contracts
prompts/                 各阶段任务提示
skill/ORCHESTRATION.md   host state machine 约定
harness/                 orchestration / validation
renderer/                累积式前端 Renderer 基线
tests/                   Harness + Renderer contract 回归
docs/                    当前规范 + 历史研究
evals/                   早期 synthetic / round reports
examples/                研究样本与最小输入示例
prototype/README.md      旧 prototype 的迁移说明
```

## 文档状态

早期 V0 文档不会删除，因为它们记录 Attribution、Evidence、Distillation 和失败模式的形成过程；但它们不一定代表当前执行入口。先看 [`docs/README.md`](docs/README.md) 区分“当前规范”和“历史研究”。

## 项目不做什么

- 不生成假的统一 skill score；
- 不把依赖树当知识树；
- 不因为 PR 被合并就默认分析、实现和测试全部由本人独立完成；
- 不为了视觉震撼把低解析节点画成成熟能力；
- 不让 Harness 偷偷成为第二个语义模型；
- 不把 Project Anchor 当能力徽章；
- 不把已验收的 Renderer 当一次性对话产物，在下一次页面开发里重新造一套。

> **Same person, different resolution.**

> **远看是作品，近看是工具。**
