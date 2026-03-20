# Vibe Memory System

> 一个面向 Agent 的项目级精细 memory 文档系统，用来把项目中的稳定知识、细粒度映射、会话上下文和历史记录分层沉淀下来，减少遗忘，提升跨会话一致性。

> 这不是单纯的“文档模板合集”，而是一套给 Agent 用的 project memory operating system。目标是让 Agent 在进入项目时，不必每次都重新扫完整个仓库，也不必在长对话后反复丢上下文。

---

## 先让 Agent 给你解释它在干什么

如果你不想先自己读完整套文档，最好的入口不是继续往下翻，而是直接让 Agent 先读，再用人话解释这套系统。

如果你还想顺手问它“这套系统怎么维护、怎么自动更新”，也可以直接一起问。这个仓库已经附带了一组 skills，尤其是 `$update-living-docs`，就是用来让 Agent 在完成工作后自动把该写回 docs 的内容写回去，而不是靠你手动维护。

可以直接把下面这段话发给 Agent：

```text
请先阅读这个仓库里的 README 和 docs_template_example/ASK_YOUR_AGENT.md。

然后不要按“文件说明书”的方式介绍，而是直接回答：
1. 这套 Vibe Memory System 到底是在干什么
2. 它实际解决的是哪些项目协作问题
3. 为什么它对 Agent 的 consistency 特别重要
4. 哪些文档层分别负责什么
5. 如果我要维护这套系统，哪些事情可以直接通过 skills 自动完成

要求：
- 用中文解释
- 先讲核心作用，再讲结构
- 多举具体问题，不要写抽象大话
- 把它当成“项目级记忆系统”来解释，不要当成普通 README 模板
- 顺带告诉我怎么用 `$update-living-docs` 之类的 skills 来减少手动维护
```

如果你想让 Agent 用更口语、更像协作讨论的方式解释，也可以直接说：

```text
你先读一下这个仓库，然后像在跟项目作者解释思路一样，告诉我这套系统到底是干什么的。重点讲它为什么能帮助 Agent 保持 consistency，避免每次换 session 都像失忆一样重新来过。
```

一个理想的对话效果大概像这样：

```text
用户：这个仓库到底是干什么的？我不想看一堆模板文件。

Agent：它本质上不是模板合集，而是一套给项目加“记忆层”的系统。目的不是多写文档，而是把项目里那些会慢慢长出来、但又特别容易在新 session 里丢掉的东西沉淀下来，比如规范、决策、术语、实现链路、历史坑点。

用户：为什么非要搞这个？

Agent：因为 Agent 最大的问题往往不是写不出来，而是每次都像一个聪明但失忆的新同事。你之前跟它花了很多轮对话磨出来的规范和结论，一换 session 就很容易丢。这个系统就是把这些项目记忆分层存下来，让后续 Agent 能继承，而不是重新摸索。

用户：那这些文档以后还得我自己手动维护吗？

Agent：不一定。这个仓库已经带了 `update-living-docs` 这类 skills。你可以直接让我用 `$update-living-docs` 去判断这次工作该更新 `STATUS`、`DECISIONS`、`CONVENTIONS`、`MAP` 还是 `SHORT_MEMORY`。也就是说，很多情况下你不用自己手动整理，我可以按文档层级自动写回。
```

更完整的解释入口见 [docs_template_example/ASK_YOUR_AGENT.md](/Volumes/ssd4t/code4t/llm_projects/vibe-memory-system/docs_template_example/ASK_YOUR_AGENT.md)。

如果你想直接让 Agent 动手，而不是只解释，可以这样说：

```text
请用 $update-living-docs，根据这次工作的实际结果更新这套 memory system。不要泛泛地改 README，要判断应该更新哪一层文档。
```

如果你做完一轮开发，准备整理提交，也可以这样说：

```text
请先用 $commit-planner 看看当前修改应该怎么分 commit，再用 $commit-pipeline 帮我完成本轮提交。
```

## 这是什么？

这个仓库提供一套可复用的文档记忆系统，适合放进 AI-assisted coding / research / engineering 项目里作为长期项目记忆层。

它要解决的核心问题不是“文档不够多”，而是：

- 项目知识散落在代码、聊天记录和临时笔记里，Agent 很难稳定继承
- 新会话像“失忆”的新同事，容易重复理解背景、重复踩坑
- 只按日期写文档，最后人和 Agent 都不看
- 项目一复杂，单个 `README` 或单个 `STATUS` 很快失去入口价值

这套系统的目标是把不同粒度的信息放到不同层里，让 Agent 始终有一个低成本、可维护、可复用的项目记忆入口。

## 它解决的不是抽象问题，而是真实协作问题

下面这些例子，不是为了“举例而举例”，而是这类系统最典型、也最真实的使用场景。

### 例子 1：规范没有被记住，输出就会持续漂移

比如你在写论文，整个项目的绘图规范是很明确的学术风格：

- 黑白灰，不是花花绿绿
- 不同对象要有稳定的纹理、底色或填充方式
- legend 命名有固定写法
- x 轴、y 轴、title、外轴标题都有固定约定
- 一些展示口径和命名方式，之前你已经跟 AI 讲过很多次

但当你前面和 AI 合作很顺，一次上下文用满，被迫开启新 session 后，你再说一句“帮我画一下这个图”，Agent 很可能立刻开始风格漂移：

- 配色变成彩色
- legend 名字改掉了
- 轴标题风格不对
- 标签命名不统一
- 之前交代过的显示规则没有继承

这类问题本来不应该靠你每次重新提醒。它们本质上属于项目规范，应该沉淀到文档里，再由 Agent 读取并遵守。

### 例子 2：项目变大之后，回溯一条产物链会非常贵

当项目规模上来之后，你经常会碰到这样的问题：

- 这张图到底是由哪条链路生成的
- 这个表格背后对应哪个脚本、哪个输入、哪个中间产物
- 这个 feature 具体落在哪几个文件里
- 这个 API 背后到底串了哪些模块

如果之前没有把这些关系记录下来，Agent 就只能重新在代码库里一步一步搜索、追溯、猜测。这不仅耗 token，更重要的是很慢，而且容易在复杂仓库里走偏。

`MAP.md` 这一层的价值，就是把“概念 / 产物 / feature”和“文件 / runner / 输入 / 输出链路”明确对上，减少重复回溯。

### 例子 3：你明明记得踩过一个坑，但已经说不清了

还有一种很常见的情况是：

- 你知道这个问题以前遇到过
- 你脑子里有模糊印象，知道当时踩过坑
- 你甚至记得最后好像已经解决了
- 但你讲不清那个坑具体是什么，也讲不清为什么后来不那样做了

这时候如果没有项目记忆，Agent 只能重新扫代码、重新搜历史、重新猜故事线。

而这些东西其实恰恰是最值得被保存的项目知识：

- 某个坑到底是什么
- 当时的 accepted fix 是什么
- 某条技术路线为什么被放弃
- 某个 decision 是怎么收敛出来的

这些规则很多不是你一开始就能 predefined 的，而是在项目推进过程中慢慢长出来的。文档系统的价值，不只是存放“预先定义好的规则”，而是承接这些 project-grown memory。

## 设计目标

- 提升 Agent 在多轮会话、多次交接下的 consistency
- 降低每次进入项目时的上下文扫描成本
- 避免稳定事实、临时讨论、历史记录混在一起
- 让“该写进哪里”的边界足够清晰，减少文档维护负担

## Memory System 分层

这个仓库当前采用的是四层 memory 结构：

### 1. Base Memory

项目的稳定主干文档，负责承载最常被重复读取的事实：

- `OVERVIEW.md`
- `STATUS.md`
- `DECISIONS.md`
- `GLOSSARY.md`
- `RUNBOOK.md`
- `CONVENTIONS.md`

### 2. Scaling Memory

当项目复杂度上升后，用来承接更细的实现状态和映射关系：

- `REPO_STATUS.md`
- `MAP.md`

### 3. Session Memory

用于卸载单次长会话中的中间上下文，避免 compact 或切会话后丢失：

- `SHORT_MEMORY/`

### 4. Historical Memory

用于保留日期型记录、复盘、探索过程和历史快照：

- `archive/`

核心原则很简单：

- 稳定事实放在动态文档
- 细粒度活动信息放在扩展层
- 暂时有用但未稳定的内容放在 session memory
- 已经结束、主要用于回溯的内容放进 archive

## 为什么这套系统对 Agent 特别重要？

- Agent 的问题通常不是“不会写”，而是“记不住项目历史”
- 好的项目记忆可以减少无谓搜索，节省上下文和时间
- 规范、术语、实现映射一旦稳定下来，Agent 才能持续写出一致的东西
- 多个 Agent 或多轮对话之间，只有文档能稳定交接项目状态
- 很多真正重要的约束并不是预设出来的，而是在项目中慢慢生长出来的

## 仓库结构

```text
vibe-memory-system/
├── README.md
├── .claude/
│   └── skills/
│       ├── commit-messages/
│       ├── commit-pipeline/
│       ├── commit-planner/
│       ├── git-understand/
│       └── update-living-docs/
└── docs_template_example/
    ├── README.md
    ├── OVERVIEW.md
    ├── STATUS.md
    ├── DECISIONS.md
    ├── GLOSSARY.md
    ├── RUNBOOK.md
    ├── CONVENTIONS.md
    ├── REPO_STATUS.md
    ├── MAP.md
    ├── SHORT_MEMORY/
    └── archive/
```

## 这个仓库里有什么？

### `docs_template_example/`

一个可直接复制到别的项目里的示例 docs 结构。

它不是强制规范，而是一个已经按职责拆好的参考实现。你可以自由改名、删减、重组，但建议保留每个文档的核心职责边界。

### `.claude/skills/update-living-docs/`

这个 skill 的职责是：当 Agent 做完有意义的工作后，主动判断哪些信息应该被写回项目记忆系统，而不是依赖用户手动维护文档。

它强调的不是“多写文档”，而是“把信息放进正确的层”：

- 稳定事实进 Base Memory
- 活跃但细的实现信息进 Scaling Memory
- 尚未稳定但对下一轮会话有帮助的信息进 Session Memory
- 适合回溯的内容进 Historical Memory

这也是整个仓库最核心的实践理念之一。

## 附带的 Skills

除了 docs template，这个仓库还附带了一组可以直接配合 Agent 使用的 skills。它们的目标不是“展示技巧”，而是把这套 memory system 真正融进日常工作流里。

### `$update-living-docs`

用途：

- 当一轮有意义的工作结束后，自动判断应该更新哪些 docs
- 避免用户手动维护 `STATUS.md`、`DECISIONS.md`、`CONVENTIONS.md`、`MAP.md`、`SHORT_MEMORY/` 等文件
- 保证写回的是“正确层级”，而不是把所有内容都塞进一个 README

适合直接这样用：

```text
请用 $update-living-docs，把这轮工作的结果同步回 docs。只更新真正该更新的层，不要把 session 讨论直接写成稳定事实。
```

### `$commit-planner`

用途：

- 分析当前工作区修改
- 判断哪些文件应该属于同一个 commit
- 给出更合理的 commit batch 划分

适合在修改比较多、内容比较杂时先用它做拆分。

### `$commit-messages`

用途：

- 根据 staged changes 生成结构化 commit message
- 使用 Conventional Commits 标题
- 在提交信息里保留 `Why`、`What`、`Risk`、`Tests`、`Live Docs` 这些部分

适合在你已经决定好当前这一批要提交什么之后使用。

### `$commit-pipeline`

用途：

- 串起完整的 `plan -> stage -> message -> commit` 流程
- 先调用 `$commit-planner`
- 再调用 `$commit-messages`
- 最后安全地完成 commit

适合直接这样用：

```text
请用 $commit-pipeline 帮我把当前修改整理并提交。先合理分 batch，不要把不相关改动混在一个 commit 里。
```

### `$git-understand`

用途：

- 在新会话开始时快速建立仓库上下文
- 做 change review、branch 对比、历史追踪
- 在动手之前先理解当前仓库状态

适合直接这样用：

```text
请先用 $git-understand 看一下这个仓库最近的改动和当前工作区状态，再告诉我你准备怎么接手。
```

### 一个实用工作流

如果你把这套系统带进一个项目里，比较自然的工作流通常是：

1. 新会话开始时，用 `$git-understand` 建立上下文
2. 做完有意义的工作后，用 `$update-living-docs` 回写 docs
3. 准备提交时，用 `$commit-planner` 或 `$commit-pipeline` 整理 commit

这样文档更新和提交整理都会更自动化，不需要用户每次手动兜底。

## 适合什么项目？

- 用 Agent 辅助开发的软件项目
- 需要跨多轮会话持续推进的研究型项目
- 会积累大量决策、术语、映射关系的工程项目
- 已经开始感到“项目有记忆，但不好找”的仓库

## 快速使用

1. 把 `docs_template_example/` 复制到目标项目并改名为 `docs/`
2. 先填好最基础的动态文档
3. 在项目级 Agent 入口里要求优先阅读 `docs/README.md` 和核心 docs
4. 按项目复杂度逐步启用 `REPO_STATUS.md`、`MAP.md`、`SHORT_MEMORY/`
5. 如果你也在用 Claude Code，可把 `.claude/skills/update-living-docs/` 一起带过去

## 使用原则

- 不追求格式统一，追求职责清晰
- 不追求文档越多越好，追求项目记忆能被稳定复用
- 不让稳定事实沉没在聊天记录和日期文件里
- 不让一个文档同时承担总览、状态、决策、映射、会话记录等多种职责

## 当前状态

这个仓库目前是一个 memory system 模板仓库，重点在于：

- 提供可复用的 docs template
- 提供配套的 Agent skills
- 形成一套适合项目级长期维护的文档分层方法

后续如果继续演进，比较自然的方向会是：

- 补更多面向不同 Agent / IDE / workflow 的集成方式
- 增加更具体的落地示例
- 继续打磨文档边界和维护流程
