# Knowledge Constellation｜知识星图

[English](README_EN.md)

> 把你真正做过、学过、解决过的问题，变成一片可以探索、解释并持续生长的个人知识宇宙。

Knowledge Constellation 是一个个人知识可视化项目。

它会读取项目 README、简历、学习记录、Pull Request、Review、课程与其他真实资料，从这些材料中识别知识、关系和经历来源，再把结果组织成一片可以探索的个人星图，而不是简单生成一张“技术栈列表”。

它想回答的不只是“这个人接触过哪些技术”，而是：

> **你真正做过什么、这些知识从哪里长出来、不同能力之间怎样关联，以及哪些部分仍然只是在形成中。**

## 最后会得到什么

一份知识星图主要由这些部分组成：

- **知识星（Knowledge Star）**：每一颗星代表一个知识领域，而不是一个简单的技能徽章或百分比。
- **星系（Galaxy）**：把彼此相关的知识组织成更大的主题区域。
- **身份核心（Identity Core）**：整个个人宇宙的中心，让人一眼知道“这是谁的星图”，但不会把页面做成传统个人资料卡。
- **项目锚点（Project Anchor）**：真实项目、课程、协作或长期经历，用来说明知识从哪里产生。
- **语义缩放（Semantic Zoom）**：远看时保持安静，放大后再逐渐显现更细的知识和关系，而不是一开始把所有节点堆在屏幕上。
- **依据展开（Evidence）**：默认界面只展示适合阅读的内容，需要时再继续查看这个判断来自哪些真实材料。

视觉上，它不是一张普通的节点关系图。知识会以恒星、星系、空间关系、动态核心和环境背景的形式出现，并通过缩放与探索逐层展开。

## 它适合用来做什么

你可以用 Knowledge Constellation：

- 把分散在不同项目和学习记录里的内容整理成一张长期知识地图；
- 看清哪些知识在不同真实经历中反复出现；
- 理解项目、语言、框架、工具和概念之间的关系；
- 展示自己的技术成长，而不是用“JavaScript 80% / C++ 60%”这类主观进度条；
- 随着新项目、新学习记录和新经历加入，让自己的知识宇宙继续生长。

## 怎么使用

目前版本已经具备可运行的知识生成流程和正式 Renderer 基线，但还不是一个可以点开网页后“一键生成”的完整托管产品。

### 1. 准备你的资料

可以从 [`examples/input.example.json`](examples/input.example.json) 开始：

```json
{
  "subject": {
    "id": "your-id",
    "label": "你的名字",
    "language": "zh-CN",
    "scope": "software-development"
  },
  "sources": [
    {
      "id": "S1",
      "kind": "project",
      "title": "项目 README",
      "content": "把真实的项目、简历、学习、PR 或其他资料放在这里。"
    }
  ]
}
```

比较适合提供的资料包括：

- 项目 README 与项目文档；
- 简历、自我介绍；
- 学习笔记；
- Pull Request 与 Code Review；
- Issue 讨论；
- 课程、项目总结；
- 调试、实现和技术取舍记录。

资料并不是越多越好。相比反复说“我会什么”，来自不同经历的具体记录更有价值。

### 2. 安装依赖

需要 Python 3.10+：

```bash
pip install -r requirements.txt
```

### 3. 创建自己的星图任务

```bash
cp examples/input.example.json input.json
python harness/pipeline.py init --input input.json --run runs/my-constellation
```

继续之前，把 `input.json` 里的示例内容替换成自己的真实资料。

### 4. 让 Codex 逐步认识这些资料

```bash
python harness/pipeline.py next --run runs/my-constellation
```

这一步会为当前阶段创建一个隔离 workspace。Codex 根据其中的任务读取材料，并写出要求的 `output.json`。

完成后运行：

```bash
python harness/pipeline.py validate --run runs/my-constellation
```

之后继续重复 `next` 和 `validate`，直到整个流程完成。

原始资料会逐步变成：

```text
真实材料
  ↓
Evidence
  ↓
知识模型
  ↓
关系 / 星系 / 项目锚点
  ↓
个人视觉模型
```

### 5. 生成视觉结果

最终接受的视觉模型会交给 [`renderer/`](renderer/) 中的模块使用。

目前 Renderer 已经包含知识星、力模型、语义缩放、Identity Core、Project Anchor、详情展示和环境背景等正式视觉基础。

完整的一体化产品 Runtime 仍在继续组装，因此这个仓库现阶段更适合用于 **生成个人知识模型 + 构建和验证自己的知识星图**，而不是把它理解成已经上线的 SaaS 网站。

## 为什么它不是普通“技术栈生成器”

Knowledge Constellation 会刻意避免一些很常见的错误：

- 项目用了某个依赖，不代表你就掌握了它；
- 一个技术出现在仓库里，不代表所有实现都是你完成的；
- 参与过一个任务，不代表独立完成了其中所有工作；
- 同一份自述重复出现，不会被当成多份独立证据；
- 星星更多，不代表一个人“更强”；
- 没有足够依据的地方，可以继续保持未知。

所以这个项目会先尝试理解真实材料，再把判断组织成知识结构，最后才决定它在星图里如何出现。

## 示例

仓库提供了一个最小输入：[`examples/input.example.json`](examples/input.example.json)。

[`examples/tyr1onx/`](examples/tyr1onx/) 中还保留了一组早期真实样本，可以查看一份个人资料是怎样逐渐形成 Evidence、知识节点、关系和整体结构的。

## 当前状态

目前核心 Recognition 流程和主要视觉语言已经形成。接下来主要在继续提高陌生用户上的识别可靠性，并把已经存在的 Renderer 模块进一步组合成完整的终端产品体验。

如果你想查看模型规则、评估记录、Renderer 设计和研究过程，可以继续阅读 [`docs/`](docs/) 和 [`SKILL.md`](SKILL.md)。
