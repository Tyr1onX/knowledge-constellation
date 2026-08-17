# Knowledge Constellation｜知识星图

> 用证据认识一个人，再把这种认识变成一片可解释、可探索的个人知识宇宙。

Knowledge Constellation 是一个 **Skill-first** 项目。它不把 GitHub 技术栈、简历关键词或项目依赖直接翻译成“技能等级”，而是让 Codex 在明确的 Recognition Contract 下完成语义判断，再由 Harness 负责隔离、验证和 repair。

## 当前状态

当前稳定主线是 **Codex-in-the-loop semantic harness**：

- 根 `SKILL.md` 是 Codex 的统一语义契约；
- Pass A/B/C/D 依次产生 Evidence → Model → Structure → Visual Model；
- Harness 只负责 orchestration / schema / semantic validation / repair；
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
accepted semantic artifacts
```

职责必须保持清晰：

- **Codex**：理解、归因、Claim、Knowledge Node、Anchor、Relation、Galaxy、Distillation、Visual Model；
- **Harness**：输入组织、Schema、状态机、隔离、验证、repair、持久化；
- **Renderer**：Scene / Canvas / d3-force / Semantic Zoom / Identity Core / 产品表面。完整视觉执行层会作为独立 checkpoint 迁入，不让半套原型污染 main。

如果 Python 开始通过关键词表自动创建 Rust / React / Database 节点，架构就退化了。

## 核心原则

- Evidence before inference；
- Artifact ≠ mastery；
- Participation ≠ execution；
- Assistance ≠ erasure；
- Dependency is provenance, not personal knowledge；
- Unknown is valid；
- stronger claims require stronger and more independent evidence；
- representativeness ≠ capability；
- Galaxy 描述个人真实主题，而不是默认课程目录。

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

## 视觉层状态

旧的 `prototype/index.html` 已从当前树中移除，因为它不再代表产品。历史版本仍可从 Git 历史恢复。

Scene / Renderer 的正式接口已经在：

- `docs/model-spec-v1.md`
- `docs/presentation-contract.md`
- `docs/physics-engine.md`

中定义。完整多文件 Renderer 将作为后续独立 checkpoint 迁入 main。

## 仓库结构

```text
SKILL.md                 Codex 语义入口
contracts/               A/B/C/D JSON contracts
prompts/                 各阶段任务提示
skill/ORCHESTRATION.md   host state machine 约定
harness/                 orchestration / validation
tests/                   当前可运行的 Harness 回归
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
- 不让 Harness 偷偷成为第二个语义模型。

> **Same person, different resolution.**

> **远看是作品，近看是工具。**
