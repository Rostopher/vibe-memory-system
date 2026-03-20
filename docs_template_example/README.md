# Docs Template README

> **职责先说清**：这个 README 是给“复制进你的项目后的 `docs/` 目录”用的入口说明，不是用来介绍本仓库 `vibe-memory-system` 自己在干什么。

> 如果你想知道这个仓库本身的定位、为什么要做这套系统、它解决了哪些真实问题，先看仓库根目录 [README.md](/Volumes/ssd4t/code4t/llm_projects/vibe-memory-system/README.md)。

> 如果你已经把这套模板复制进某个具体项目，并改名为 `docs/`，那么当前这个文件回答的是：这些文档在项目里各自负责什么、先用哪些、怎么逐步启用。

---

## 这份 README 和仓库 README 的分工

为了避免两份 README 说同一件事，这里先明确边界：

### 仓库根目录 `README.md`

它负责解释：

- Vibe Memory System 是什么
- 为什么这套系统有必要
- 它解决了哪些 Agent 协作问题
- 这整个仓库里包含哪些模板和 skills

### 当前这个 `docs/README.md`

它负责解释：

- 当这套模板被放进一个具体项目后，`docs/` 目录怎么用
- 哪些文档是基础层，哪些是扩展层
- 什么时候该更新哪一份文档
- 应该从最小版本开始，还是启用增强层

一句话说：

- 根 README 解释“这套系统是什么”
- 模板 README 解释“这套系统进到项目里以后怎么落地”

## 这是什么？

这是一个可复制到其他项目里的 `docs/` 模板，用来给项目提供分层的 memory system。

它不是让你机械照抄一组文件名，而是给你一套清晰的职责拆分方式，让项目里的知识知道自己该落在哪一层。

如果你准备把它复制到一个新项目，建议先把它当成一套“最小可运行的项目记忆结构”，而不是一次性铺满所有文档。

## 先怎么用：最小版还是增强版？

### 方案 A：先只启用 Base Memory

先只使用这 6 个核心动态文档：

- `OVERVIEW.md`
- `STATUS.md`
- `DECISIONS.md`
- `GLOSSARY.md`
- `RUNBOOK.md`
- `CONVENTIONS.md`

适合：

- 新项目刚开始
- 代码库还不复杂
- 当前只有一条主线工作流
- 你想先把最小维护成本跑通

### 方案 B：再逐步加上扩展层

当项目复杂度上来后，再启用：

- `REPO_STATUS.md`
- `MAP.md`
- `SHORT_MEMORY/`

适合：

- 项目已经持续了一段时间
- 存在多条工作流或复杂实现链路
- Agent 很难只靠搜索快速定位 feature / artifact / API
- 长对话很多，session 一切换就容易丢上下文

推荐默认策略：

1. 先从 Base Memory 开始
2. 当 `STATUS.md` 明显太挤时，加 `REPO_STATUS.md`
3. 当实现链路很难回溯时，加 `MAP.md`
4. 当 session 上下文经常丢时，加 `SHORT_MEMORY/`

也就是说：

**先把最小系统跑起来，再按真实痛点长出扩展层。**

## 四层结构分别负责什么

### 1. Base Memory

项目最常被重复读取的稳定事实。

| 文件 | 回答的核心问题 | 什么时候更新 |
|---|---|---|
| `OVERVIEW.md` | 这个项目是什么，主线和架构是什么 | 项目方向或架构明显变化时 |
| `STATUS.md` | 当前项目高层进展到哪了 | 里程碑完成或主线变化时 |
| `DECISIONS.md` | 为什么要这样做 | 做出稳定决策后 |
| `GLOSSARY.md` | 术语、变量、命名分别是什么意思 | 引入新概念时 |
| `RUNBOOK.md` | 怎么运行、怎么排错、产物在哪 | 运行方式变化时 |
| `CONVENTIONS.md` | 代码和输出有哪些硬规则 | 规范新增或变更时 |

原则：

- 保持精简
- 只放稳定事实
- 不要把中间讨论和实现细节全塞进去

### 2. Scaling Memory

当项目变复杂后，用来承接 Base Memory 放不下、但又很活跃的重要细节。

#### `REPO_STATUS.md`

用来承接更细的实现追踪，例如：

- 哪些模块做完了
- 哪些差异还存在
- 哪些工作流已经落地到什么程度

#### `MAP.md`

用来做概念到实现的映射，例如：

- 一个 feature 对应哪些文件
- 一个 API 背后由哪些模块共同完成
- 一张图、一个表、一个 artifact 对应哪个脚本、哪个输入、哪个导出链路

原则：

- `REPO_STATUS.md` 负责更细的“状态”
- `MAP.md` 负责更细的“对照和指针”

### 3. Session Memory

`SHORT_MEMORY/` 用来保存单次会话里有价值、但还没稳定到能进正式文档的上下文。

适合放：

- 调试过程中的中间判断
- 某轮 session 的工作摘要
- 暂时性方向判断
- 下一轮 Agent 很可能需要继承的背景

不适合放：

- 已经稳定的项目状态
- 已经明确的规范
- 已经形成正式结论的决策

### 4. Historical Memory

`archive/` 用来保留历史记录和回溯材料，例如：

- 日期型记录
- 阶段性复盘
- 失败探索
- 一次性分析
- 历史快照

一个简单判断：

- 如果内容主要是为了让下一轮 session 接着干，优先放 `SHORT_MEMORY/`
- 如果内容主要是为了以后回看，优先放 `archive/`

## 推荐目录结构

```text
docs/
├── README.md
├── OVERVIEW.md
├── STATUS.md
├── REPO_STATUS.md
├── DECISIONS.md
├── GLOSSARY.md
├── RUNBOOK.md
├── CONVENTIONS.md
├── MAP.md
├── SHORT_MEMORY/
│   └── README.md
├── archive/
│   └── README.md
├── ASK_YOUR_AGENT.md
└── HOW_TO_CLONE_THIS_TEMPLATE.md
```

不是每个项目都需要一开始就启用全部层。

这份模板的重点不是“文件越全越好”，而是“职责拆分尽量清楚”。

## 30 秒落地

如果你只想快速装到新项目里：

1. 把 `docs_template_example/` 复制到目标项目并改名为 `docs/`
2. 先填 6 个基础动态文档
3. 在项目级 Agent 入口里加入 `docs/README.md`
4. 如果用户不想自己读 docs，直接让 Agent 先看 `docs/ASK_YOUR_AGENT.md`
5. 如果你也想减少手动维护，把仓库里的 `.claude/skills/` 一起复制过去
6. 做完有意义的工作后，直接让 Agent 用 `$update-living-docs` 回写 docs
7. 只有在出现明确痛点时，再启用 `REPO_STATUS.md`、`MAP.md`、`SHORT_MEMORY/`

详细迁移步骤见 [HOW_TO_CLONE_THIS_TEMPLATE.md](./HOW_TO_CLONE_THIS_TEMPLATE.md)。

## 如果你不想手动维护 docs

这套模板本身可以手动维护，但更推荐配合仓库附带的 skills 一起使用。

最关键的是：

- `$update-living-docs`：让 Agent 根据这次工作结果自动判断应该更新哪一层 docs
- `$commit-planner`：让 Agent 先想清楚当前修改该怎么拆 commit
- `$commit-pipeline`：让 Agent 把 commit 的计划、暂存、写 message、提交串起来

一个最常用的说法就是：

```text
请用 $update-living-docs，把这次工作的结果同步回 docs。不要泛泛更新，要判断应该写进 Base Memory、Scaling Memory、Session Memory 还是 archive。
```

## Agent 应该先读什么

如果这是一个已经落地到具体项目里的 `docs/` 目录，推荐 Agent 按这个顺序阅读：

1. `docs/README.md`
2. `docs/OVERVIEW.md`
3. `docs/STATUS.md`
4. `docs/GLOSSARY.md`
5. `docs/RUNBOOK.md`
6. `docs/CONVENTIONS.md`
7. `docs/DECISIONS.md`

如果项目明显更复杂，再继续看：

- `docs/REPO_STATUS.md`
- `docs/MAP.md`
- `docs/SHORT_MEMORY/`

## 使用原则

- 不要把所有事情都写进一个文档
- 不要让稳定事实沉没在日期文件里
- 不要让 `SHORT_MEMORY/` 变成第二个 archive
- 不要让 `STATUS.md` 承载所有实现细节
- 不要为了“完整”而牺牲入口可读性

## 最后提醒

这套模板是一个职责拆分示例，不是 rigid format。

你完全可以：

- 改名字
- 调整目录
- 删除不需要的层
- 增加项目专属文档

只要你还能保持两件事，这套系统就仍然有效：

1. 稳定事实有清晰入口
2. 不同粒度的信息不要混在一起
