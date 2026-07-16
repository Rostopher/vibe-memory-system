# Vibe Memory System

给 AI Agent 用的**项目级记忆模板**。

它的目标只有一个：**让 Agent 快速建立项目框架认知，并知道去哪里找细节**，
而不是把项目的每个 API、每个组件、每张表都塞进记忆。

---

## 这是什么

一套可直接复制进任何项目的 `memory-docs/` 文件夹模板。
Agent 每次进入项目，读其中几个精简文件，就能继承之前的上下文，而不是从零开始。

核心是**三层结构**：

| 层 | 内容 | 性质 |
|---|---|---|
| **框架层** | OVERVIEW / STATUS / HISTORY / CONVENTIONS / GLOSSARY | 增长极慢，进项目必读 |
| **路由层** | DIRS | 查"详细层里有什么、去哪找" |
| **详细层** | detail_mem/（MAP / PROGRESS / DECISIONS）+ 子文件夹 | 随项目自由生长，按需读 |

关键设计：**框架层不放任何会随项目线性膨胀的东西**。
全量 API 列表、全量组件清单留在代码里；memory-docs 只记"框架 + 导航指针"。

---

## 怎么用（30 秒）

1. **复制**：把这个仓库里下面这些文件 / 文件夹，整体复制进你的项目，改名为 `memory-docs/`：

   ```
   INDEX.md  OVERVIEW.md  STATUS.md  HISTORY.md  CONVENTIONS.md  GLOSSARY.md
   detail_mem/MAP.md  detail_mem/PROGRESS.md  detail_mem/DECISIONS.md  DIRS.md
   SHORT_MEMORY/  archive/
   ```

2. **改名占位**：手动复制时，把文件里的 `<memory-docs>/` 全部替换成 `memory-docs/`；安装器会自动替换。

3. **让 Agent 接手**：让 Agent 读 `memory-docs/INDEX.md`，建立认知；再用
   `init-memory` skill（或手动）把模板填成你项目的真实内容。

推荐使用跨平台 Python 安装器：

```bash
python scripts/install_to_project.py <目标项目路径>
```

Bash 用户也可以运行等价包装器：

```bash
scripts/install_to_project.sh <目标项目路径>
```

安装器默认安装 `memory-docs/`、项目本地 `.claude/skills/` 和
`.memory-docs-tools/validate_memory_docs.py`。已有 `AGENTS.md` 会保留并提示手动合并；
只有显式传入 `--replace-agents` 才会替换。可用 `--component memory-docs|skills|tools`
单独安装某一部分。

刷新标准模板时可用 `--force`。它不会删除 `SHORT_MEMORY/` 或 `archive/` 中的额外记录；
如果检测到自建 memory 子目录，则拒绝自动刷新，避免覆盖 `DIRS.md` 注册信息。

安装或修改后运行校验：

```bash
python scripts/validate_memory_docs.py <目标项目路径>
```

---

## 为什么是这个结构

这套结构是从真实项目（一个包含前端 / 后端 / 数据库的大型网站工程）长期使用中
反复打磨出来的。踩过的坑包括：

- **MAP 膨胀**：最初 MAP 想做"概念→文件"快速索引，结果 agent 出于好意把全量端点、
  全量组件都列进去，慢慢长成几百行的代码目录册，违背了"快速导航"的初衷。
  → 解法：MAP 只记**概念→入口文件**（1-2 个），全量信息留给代码。

- **STATUS 流水账**：STATUS 的 Done 区不断追加，变成无叙事弧度的长流水账。
  → 解法：STATUS 只留最近 3-5 条，沉淀下来的里程碑进 HISTORY。

- **模板污染**：早期模板自带示例文字，复制进新项目后，agent 觉得"这不是我的项目"，
  惰性不更新。
  → 解法：模板保持干净占位，三层职责清晰，每个文件有明确边界。

- **docs 命名冲突**：很多项目本身就有 `docs/`，再用 `docs/` 会混淆。
  → 解法：统一叫 `memory-docs/`，语义自解释，不与项目自有 `docs/` 冲突。

完整设计推演见 `project-memory-docs/HISTORY.md`（项目自用记录，已 gitignore）。

---

## 仓库结构

```
vibe-memory-system/
├── README.md                ← 本文件（仓库说明）
├── AGENTS.md                ← Agent 使用 memory-docs 的指引（可合并进目标项目）
├── .gitignore               ← 含 project-memory-docs/（项目自用，不上传）
│
├── 【模板文件 - 复制进你的项目，改名为 memory-docs/】
│   ├── INDEX.md             ← memory-docs 入口（三层说明 + 更新协议）
│   ├── OVERVIEW.md          ← 项目是什么
│   ├── STATUS.md            ← 当前在做什么（精简）
│   ├── HISTORY.md           ← 项目怎么走到今天（时间线）
│   ├── CONVENTIONS.md       ← 工作约定 / 硬规则
│   ├── GLOSSARY.md          ← 项目术语
│   ├── detail_mem/           ← 详细层主目录
│   │   ├── MAP.md           ← 概念→入口文件（导航，非全量清单）
│   │   ├── PROGRESS.md      ← 模块实现清单
│   │   └── DECISIONS.md     ← 决策档案
│   ├── DIRS.md              ← 路由层：子文件夹注册表
│   ├── SHORT_MEMORY/        ← 会话级临时上下文
│   └── archive/             ← 历史归档
│
├── project-memory-docs/     ← vibe-memory-system 自己的演进记录（gitignore）
├── .claude/skills/          ← 配套 Agent skills
└── scripts/
    ├── install_to_project.py     ← 跨平台安装器
    ├── install_to_project.sh     ← Bash 包装器
    ├── validate_memory_docs.py   ← 结构 / frontmatter / DIRS 校验
    └── _test_memory_docs_tools.py ← 安装与校验回归测试
```

> 注意：框架层模板文件**平铺在根目录**，详细层文件收入 `detail_mem/` 子文件夹。
> `project-memory-docs/` 是**本项目自用**的，已加入 `.gitignore`，两者不混淆。

---

## 配套 Skills

| Skill | 用途 |
|---|---|
| `init-memory` | 首次接入时扫描仓库，把 memory-docs 模板一次性填成真实内容 |
| `update-living-docs` | 做完工作后，按更新协议把结果回写 memory-docs |
| `commit-pipeline` | plan → stage → message → commit |
| `git-understand` | 新会话快速建立仓库上下文 |

---

## 设计原则

- **职责清晰比格式统一重要**：每个文件只做一件事，边界用 `not_for` 写明。
- **框架层保持精简**：任何会随项目膨胀的内容都不该进框架层。
- **导航优先于细节**：memory-docs 是地图，不是百科全书。
- **以代码为准**：文档与代码冲突时，信代码，修文档。
