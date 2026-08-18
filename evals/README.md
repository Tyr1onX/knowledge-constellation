# Evals｜自我迭代测试

这个目录用于测试 Knowledge Constellation 的 Recognition、Attribution、Structure、Distillation 与后续 Visual Model。

目标不是得到一个“准确率 92%”之类的数字，而是持续攻击模型最容易犯错的地方。

## 当前主评测：Clean-room real-user audit

Recognition Hardening 阶段优先使用：

```text
Frozen raw sources
    ↓
Clean-room Runner（只运行当前 Skill）
    ↓
结构化结果

Frozen raw sources
    ↓
Independent External Auditor
    ↓
独立 source-only judgment
    ↓
与 Runner 输出比较
```

完整协议见 [`../docs/clean-room-evaluation.md`](../docs/clean-room-evaluation.md)，真实案例存放在 [`clean-room/`](clean-room/)。

重点不是 Runner 和 Auditor 是否生成完全一样的节点，而是：是否越界、是否漏掉代表性主题、归因是否可靠、Anchor 是否真实、Galaxy 是否具有个人结构。

### Protocol v2：Runner 结果必须可执行验证

从 `kc.cleanroom.v2` 开始，只有真正通过当前 schema + semantic validator 的 `pass-a/b/c/d` 才能计入 Recognition Hardening 用户数。Runner 的文字总结不能替代 Harness 验证。

每个 v2 case 在进入 External Audit 前必须通过：

```bash
python harness/verify_eval_case.py evals/clean-room/cases/<case>
```

规则见 [`clean-room/protocol-v2.md`](clean-room/protocol-v2.md)。CI 会回归所有已经提交的 v2 case，避免规则更新后旧样本静默失效。

## 历史测试循环

```text
构造极端案例
    ↓
只读取案例提供的证据
    ↓
按当前协议生成保守画像
    ↓
Critic 主动寻找误判
    ↓
定位错误层
Recognition / Attribution / Structure / Distillation / Visual
    ↓
修改规则
    ↓
重新跑案例
```

同一个案例在规则修改前后都应该保留结果，避免只留下“最终正确答案”。

## 当前案例类型

- `B-independent-developer`：真实独立开发者，测试模型会不会保守过头；
- `C-learning-heavy-student`：学习证据很多但项目少，测试会不会生成空图；
- `D-one-project-specialist`：一个项目很深，测试会不会把依赖树当本人知识树；
- `E-broad-generalist`：方向很多，测试结构和首屏预算；
- `F-low-public-trace`：公开痕迹少，测试非 GitHub 证据能否工作；
- `G-ai-heavy-high-judgment`：AI 深度实现，但用户真实承担需求、判断与验收，测试会不会把人类贡献抹掉；
- `H-impressive-readme`：README 很厉害但缺少行为证据，测试自我包装膨胀。

`Tyr1onX` 的公开 GitHub Passive-only 案例继续作为真实 Case A。

## 每个案例至少检查

1. 是否凭空生成能力；
2. 是否把工具/依赖出现当成能力；
3. 是否把一次活动当成长期结构；
4. 是否把辅助存在误解成“用户没有贡献”；
5. 是否低估有充分独立证据的真实能力；
6. 星系是否围绕个人真实 Anchor，而不是课程 taxonomy；
7. 第一层是否仍能一眼读出人物轮廓；
8. 任何强 Claim 是否有至少一条真正支持“能力”的证据，而不只是成果存在。

## 重要约束

合成案例的 `expected` 不是让模型机械匹配答案，而是定义不可违反的边界。

例如：

```yaml
must_not:
  - infer Rust mastery from a transitive dependency
```

它测试的是原则，而不是固定文案。

真实 clean-room 案例不把 Auditor 输出暴露给 Runner；失败案例也必须保留并在规则变化后 rerun。
