# Vibe Memory System

给 AI Agent 用的项目级记忆系统。把项目中的决策、规范、术语、运行方式、实现映射和历史记录分层沉淀下来，让 Agent 在每次进入项目时都能继承之前的上下文，而不是从零开始。

## 不想自己读？

可以先让 Agent 按模板入口读一遍，再让它用自己的话解释。你可以这样说：

```text
请先读 README.md 和 docs_template/ASK_YOUR_AGENT.md，再按 docs_template/ 里各个文档的职责说明，理解这套 memory system 的分层、用途和更新方式。最后读 docs_template/MEMORY_MANIFEST.yml，校准读取顺序和 update_mode。

读完后，请用中文直接告诉我：这套系统是干什么的、解决哪些真实问题、各层文档分别负责什么、实际项目里应该怎么用。
```

## 设计理念

### 问题

Agent 的能力再强，也会被记忆拖住。每次新会话就像换了一个聪明但失忆的同事：

- 你花了很多轮对话磨出来的绘图规范、命名约定、数据口径，一换 session 就丢了
- 项目变大后，一张图由哪个脚本生成、一个 feature 落在哪些文件里，Agent 要重新搜一遍
- 你明明踩过一个坑，但说不清具体是什么了，Agent 只能重新踩一次

### 思路

把项目知识按**稳定程度**和**粒度**分层存放，每一层有明确的职责和更新方式。Agent 进入项目时按需读取，而不是每次扫完整个仓库。

### 核心机制：三种更新模式

每个文件都标注了一个 `update_mode`，告诉 Agent "这个文件该怎么改"：

| 模式 | 含义 | 例子 |
|---|---|---|
| **rewrite** | 整体重写，文件是"当前快照" | OVERVIEW、STATUS、RUNBOOK |
| **append** | 只追加，旧内容不动 | DECISIONS、SHORT_MEMORY、archive |
| **patch** | 逐条修改 | CONVENTIONS、GLOSSARY、MAP、PROGRESS |

这解决了一个常见问题：没有明确指引时，Agent 要么不敢动文件，要么整体重写把旧内容覆盖掉。

## 四层结构

### 1. Base Memory — 稳定事实层

项目最常被读取的核心文档。

| 文件 | 职责 | 更新模式 |
|---|---|---|
| `OVERVIEW.md` | 项目的一页纸概括：做什么、怎么组织 | `rewrite` |
| `STATUS.md` | 高层快照：Done / In Progress / Backlog | `rewrite` |
| `DECISIONS.md` | 决策档案：为什么选 A 不选 B，以及 trade-off | `append` |
| `GLOSSARY.md` | 项目词典：当我说 X 时，我指的是什么 | `patch` |
| `RUNBOOK.md` | 操作手册：环境、命令、产物位置、编译顺序 | `rewrite` |
| `CONVENTIONS.md` | 硬规则：绘图风格、命名约定、数据 contract | `patch` |

### 2. Scaling Memory — 细粒度扩展层

项目变复杂后才需要启用。

| 文件 | 职责 | 更新模式 |
|---|---|---|
| `PROGRESS.md` | 模块级实现清单：每个模块做了没有 | `patch` |
| `MAP.md` | 导航图：概念/产物 → 文件/脚本/链路 | `patch` |

**STATUS vs PROGRESS**：STATUS 是高层快照（3-5 条），PROGRESS 是细粒度清单（可能 20-50 条）。

**GLOSSARY vs MAP**：GLOSSARY 定义"概念是什么"，MAP 定义"概念在哪里"。

### 3. Session Memory — 会话交接层

- `SHORT_MEMORY/`（`append`）— 当前会话中有用但还没稳定的上下文，留给下一轮 Agent。

### 4. Historical Memory — 历史归档层

- `archive/`（`append`）— 复盘、失败探索、日期型记录。主要用于回溯，不参与日常工作路由。

## 使用方式

### 安装

```bash
scripts/install_to_project.sh TARGET_PROJECT_PATH
```

这会把 `AGENTS.md`、`docs_template/`（作为 `docs/`）和 `.claude/skills/` 安装到目标项目。

也可以手动复制 `docs_template/` 并改名为 `docs/`。

### 自动维护

安装后不需要手动维护文档。做完工作后让 Agent 执行：

```text
请用 $update-living-docs 把这次工作的结果同步回 docs。
```

Agent 会读取每个文件的 `update_mode`，判断该 rewrite、append 还是 patch，然后写入正确的层。

### 推荐工作流

1. 安装后 → `$init-memory` 扫描仓库，一次性填充所有 docs 模板
2. 新会话 → `$git-understand` 建立上下文
3. 做完工作 → `$update-living-docs` 回写记忆
4. 准备提交 → `$commit-pipeline` 整理 commit

## 仓库结构

```text
vibe-memory-system/
├── AGENTS.md                    # 可复制到目标项目的 Agent 入口模板
├── docs_template/               # 干净安装源（默认安装到目标项目）
├── docs_template_example/       # 带详细中文解释的教学版
├── docs/                        # 本仓库自身的记忆
├── .claude/skills/              # Agent skills
│   ├── init-memory/             #   首次接入时扫描仓库填充 docs 模板
│   ├── update-living-docs/      #   做完工作后自动回写 docs
│   ├── commit-pipeline/         #   plan → stage → message → commit
│   ├── commit-planner/          #   分析修改，规划 commit 批次
│   ├── commit-messages/         #   根据 staged changes 生成 commit message
│   ├── git-understand/          #   新会话快速建立仓库上下文
│   └── research-engineering/    #   研究型 Python 项目规范
└── scripts/
    ├── install_to_project.sh    #   安装模板到目标项目
    ├── sync_to_claude.sh        #   同步 skills 到 ~/.claude/
    └── sync_to_codex.sh         #   同步 skills 到 ~/.codex/
```

## 设计原则

- 职责清晰比格式统一重要
- 先从 Base Memory 开始，按真实痛点再加扩展层
- 稳定事实不应该沉没在聊天记录里
- 一个文件只做一件事
