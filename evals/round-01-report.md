# Round 01｜第一轮自我迭代报告

本轮使用 `synthetic-cases-v0.yaml` 中 B～H 七个合成案例攻击当前协议。

目标不是让输出匹配预设答案，而是检查规则是否会出现系统性误判。

---

## 总结

当前协议已经比较能防住：

- Artifact → Mastery；
- Participation → Execution；
- 高级技术词自动变成中心；
- GitHub 来源自动变成 Galaxy；
- AI 存在就把人的贡献抹掉。

但第一轮暴露出 5 个需要修改的核心问题。

---

# P1｜Technology Presence 过于宽松

旧规则中：

> Repository uses X 可以支持 exposure。

Case D 证明这仍然太宽。

一个项目可以包含：

- 第三方 Rust native addon；
- Redis client；
- GraphQL library；
- 模板生成的 React UI；

但用户可能从未真正修改或理解这些部分。

因此必须拆开：

```text
Environmental Presence
技术存在于环境中

≠

Meaningful Exposure
用户真实接触、修改、调试、配置、解释过它
```

### 修正规则

只有以下信号之一出现时，技术才允许从 `environmental_presence` 升为 `meaningful_exposure`：

- 修改了该技术直接相关的代码；
- 调试过相关问题；
- 做过配置或设计选择；
- 写过相关解释；
- 学习记录明确涉及；
- 校准中确认实际接触。

单纯依赖列表、lockfile、transitive dependency 不足以生成主星图节点。

---

# P2｜Capability 不能继续是一个模糊单字段

Case C 与 Case B 暴露出相反问题。

学习型学生可以有很强的：

- 概念理解；
- 解释能力；
- 记忆稳定性；

但没有工程实现经验。

独立开发者可能有很强的：

- 实现；
- 调试；
- Review；
- 性能判断；

这两类都不能被一个 `capability: partial` 准确描述。

### 修正规则

V0 不做数字评分，但 Claim 必须标记它证明的是哪一种能力：

```text
understanding   理解 / 解释
implementation 实现
independence    独立完成
judgment        判断 / 取舍 / 验收
troubleshooting 调试 / 定位
transfer        迁移到新问题
```

不是每个节点都需要六项齐全。

这只是为了防止：

```text
考试 88 分
→ 工程能力 established
```

或者：

```text
项目做出来了
→ 底层机制理解 established
```

---

# P3｜需要 Corroboration Independence

Case B 和 H 说明“证据数量”不能简单计数。

下面这些可能本质上只有一个来源：

```text
个人 README：我精通 Rust
个人主页：我精通 Rust
简历：我精通 Rust
```

即使出现三次，仍然主要是同一个人的三次自我陈述。

而下面组合明显更强：

```text
本人 Issue 根因分析
+
实际实现 diff
+
独立 benchmark
+
维护者 Review
+
新的解释任务
```

### 修正规则

Claim 的置信度不仅看数量，还看：

- 来源是否独立；
- 证据类型是否互补；
- 是否存在第三方验证；
- 是否包含行为证据；
- 是否只是同一成果的重复描述。

V0 先不计算数学权重，只要求模型显式判断：

```text
same-origin corroboration
cross-origin corroboration
```

强 Claim 优先需要后者。

---

# P4｜Self-presented Claim 需要单独降权

Case H：

README 写：

> Expert in Rust / Kubernetes / Distributed Systems / AI Infrastructure

同时有 30 个 badge。

这些仍然是有意义的数据，因为它们可能表示：

- 自我定位；
- 兴趣；
- 想被如何看见；

但不能直接作为 Capability Claim。

### 修正规则

纯自我包装默认进入：

```text
claimed_identity
```

而不是：

```text
verified_capability
```

如果缺少其他证据：

- 可以成为校准线索；
- 可以成为 Identity 层的候选；
- 默认不进入主技能节点；
- 不能被 badge 数量提高置信度。

---

# P5｜“保守但完整”不能理解成“必须画满”

Case F 与 Case H 说明：

对于低公开痕迹用户，第一份图可能天然解析度低。

如果为了“完整”硬补节点，就会破坏真实性。

因此重新定义：

> **完整（complete）不是节点多，而是当前可支持的人物轮廓没有被故意截断。**

可以出现：

```text
2 个稳定主题
+ 3 个 unresolved 区域
```

而不是强行填满 20 颗星。

---

# 各案例结果

## B — Independent Developer

### 初始协议结果

能够识别：

- Rust；
- 网络服务；
- 调试；
- Review；
- 性能工作。

### 初始问题

协议可能因为“PR 不等于独立实现”而保守过头，让 Rust 长期停留在 `observed`。

### 修复后期望

多种独立证据同时支持：

```text
Rust implementation
Rust independence
troubleshooting
code review judgment
```

因此 Rust 可以进入更稳定状态。

**结果：初始部分失败，修规则后应通过。**

---

## C — Learning-heavy Student

### 初始协议结果

不会生成空图，学习记录可以形成轨迹。

### 初始问题

`capability` 太粗，容易混淆：

```text
conceptual understanding
engineering implementation
```

### 修复后期望

二分、进程线程、TCP 等可以拥有较强 `understanding`，但工程实践保持未知或较弱。

**结果：结构通过，能力语义部分失败。**

---

## D — One-project Specialist

### 初始协议结果

能形成浏览器自动化主题。

### 初始问题

旧规则“项目用了 X → exposure”会让 Rust / Redis / GraphQL 等依赖得到过多存在感。

### 修复后期望

只有 TypeScript、DOM、Browser Automation、Debugging 等真正被修改/解释的内容进入主结构。

**结果：发现明确漏洞。**

---

## E — Broad Generalist

### 初始协议结果

能够形成多个 Anchor / Galaxy。

### 风险

如果不限制预算，会出现：

```text
React / Python / ESP32 / Go / JS / CSS / Pandas / UART / ...
```

全部同权。

### 修复方向

第一层继续使用 Distillation Budget：

- 3～5 个 Galaxy；
- 每个 Galaxy 只保留少量核心节点；
- 跨项目稳定出现的 Practice Motif 可以作为桥梁，而不是再复制成一个技术星系。

**结果：基本通过，依赖蒸馏预算。**

---

## F — Low-public-trace

### 初始协议结果

多源证据模型能够工作，不依赖 GitHub。

### 风险

简历、自述、作品视频、导师推荐信的证据属性必须分开。

### 修复后期望

例如：

```text
Qt / C++ project presence    supported
串口协议实现                third-party corroborated
独立整体项目能力            partial / unresolved
```

**结果：基本通过，需要 Corroboration Independence。**

---

## G — AI-heavy High Judgment

### 初始协议结果

现有 Role Attribution 能够避免把 AI 生成代码全部算给用户，也不会把用户贡献归零。

### 重要结果

这类案例应该允许形成：

- Requirement Framing；
- Acceptance / Validation；
- Product Iteration；
- AI-assisted Workflow；

同时保持具体语言的独立实现为 unresolved。

**结果：通过，是当前归因模型的优势案例。**

---

## H — Impressive README

### 初始协议风险

如果模型把 `self_report` 当成普通正证据，仍可能形成大量虚高节点。

### 修复后期望

README 技术徽章只作为：

```text
claimed identity / interest signal
```

不建立 established capability。

同时：缺少公开证据也不能反向断言“用户不会”。

**结果：发现明确漏洞。**

---

# Round 01 后的新 Gate

进入视觉原型前，协议至少需要做到：

- [x] Participation ≠ Execution
- [x] AI assistance ≠ zero human contribution
- [x] Sophisticated term ≠ representativeness
- [x] Source ≠ Galaxy
- [ ] Environmental presence ≠ meaningful exposure
- [ ] Understanding ≠ implementation
- [ ] 同源重复 ≠ 独立佐证
- [ ] Self-presented identity ≠ capability
- [x] Sparse evidence 可以生成低解析度但诚实的图

先修复上述 4 个未完成项，再进行 Round 02。
