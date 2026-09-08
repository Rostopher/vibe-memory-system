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
| **框架层** | OVERVIEW / STATUS / HISTORY / CONVENTIONS / GLOSSARY | 当前入口聚焦；规则按任务、历史按需读取 |
| **路由层** | DIRS | 查"详细层里有什么、去哪找" |
| **详细层** | detail_mem/（MAP / PROGRESS / DECISIONS）+ 可选子文件夹 + archive | 按需读，保留证据与细节 |

关键设计：**默认读取面保持可控，详细证据与历史允许增长**。
全量 API 列表、全量组件清单留在代码里；memory-docs 维护"框架 + 导航指针 +
可追溯的细节"。每类事实只有一个详细 owner，非 owner 只保留当前读者需要的结论和链接。

---

## 开发与记忆的节奏

按不确定性选择隔离 Explore、局部 `probe_` 或直接实现。探索验证可行后可以暂不接入；
Integrate 完成模块归属、必要整理和受影响行为验证。日常整理服务当前修改，
版本节点与累计改动触发结构检查，Consolidate 由 Agent 提出证据和范围、用户决定。

memory 以完整工作单元收尾：到达约定交付节点，询问是否收束、是否更新，确认后集中整理。
不随每个小改动或试错反复写 docs；commit 和部署均不是前提。已经明确授权的初始化、
迁移和维护直接执行，不重复确认。用户暂缓或自行整理时尊重决定。
复杂排障、失败探索、SHORT_MEMORY 和历史允许长文，按用途保真并提供检索入口。

新探针命名 `probe_`，正式测试沿框架约定；既有 `_test_` 分类迁移与关键测试补齐另行安排。
核心规则见 [AGENTS.md](AGENTS.md)，完整流程见
[evolutionary-development](skills/evolutionary-development/SKILL.md)。

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
python3 scripts/install_to_project.py <目标项目路径> --skill-target codex
```

Bash 用户也可以运行等价包装器：

```bash
scripts/install_to_project.sh <目标项目路径> --skill-target codex
```

默认 component 会安装 `memory-docs/`、所选平台的项目级 skills 和
`.memory-docs-tools/validate_memory_docs.py`。只要 component 包含 skills，就必须显式
选择 `--skill-target claude|codex|both`，避免只使用一个 CLI 的项目无意生成两套副本。
仓库顶层 `skills/` 是平台中立的唯一源码和分发目录，本身不是独立项目的自动发现
目录；安装器会生成 Claude 使用的 `.claude/skills/` 或 Codex/Agent 使用的
`.agents/skills/`，这些平台目录只是可校验、可重建的安装产物。

常用选项：

```bash
# 只装某个平台的项目级 skills
python3 scripts/install_to_project.py <目标项目> --component skills --skill-target codex

# 安全刷新 skills / validator，同时保留已有项目记忆
python3 scripts/install_to_project.py <目标项目> --skill-target codex --force

# 明确重置标准 memory 模板；这是破坏性选择，必须单独指定
python3 scripts/install_to_project.py <目标项目> \
  --component memory-docs --replace-memory-docs
```

- `--skill-target claude|codex|both` 没有隐式默认值；`both` 必须明确选择。
- 已有 `AGENTS.md` 默认保留；只有 `--replace-agents` 才替换。
- 单独同步已管理且没有被手改的 skills 时不需要 `--force`；旧项目首次接管无
  manifest 的同名目录，或用默认 component 同时刷新 validator 时需要显式 `--force`。
- 对 memory-docs，`--force` 不覆盖已有 `STATUS`、`DECISIONS` 等真实记忆，只补缺失模板文件。
- `--replace-memory-docs` 也会保留额外 archive / SHORT_MEMORY 记录；检测到自建
  memory 子目录时会拒绝自动重置，避免破坏 `DIRS.md` 路由。
- 可用 `--component memory-docs|skills|tools` 单独安装某一部分。

升级已经有真实内容的旧项目时，不要用 `--replace-memory-docs` 或
`--replace-agents` 做协议迁移。先用一条命令非破坏地刷新生成内容、validator，并
补齐缺失模板：

```bash
python3 scripts/install_to_project.py <目标项目> --skill-target codex --force
```

然后明确要求 `init-memory` 执行 protocol migration：保留现有 owner、frontmatter、
自建目录和项目规则，把工作单元收尾、历史检索、当前决策视图与 archive 契约合并进
现有 `AGENTS.md` / `memory-docs`；registry 从现有稳定 ID 渐进建立，不批量重写历史。
最后运行 validator。`--force` 不会暗中改写已有的真实项目记忆或 `AGENTS.md`。

需要安装到用户级 skill 目录时，分别运行：

```bash
scripts/sync_to_claude.sh   # ~/.claude/skills/
scripts/sync_to_codex.sh    # ~/.agents/skills/

# 只检查，不写入；同步时也可直接使用 --target both
scripts/sync_to_codex.sh --check
python3 scripts/sync_skills.py --target both --check
```

首次同步会在目标根写入 `.vibe-memory-system-skills.json`，记录本系统拥有的
skill 名称和确定性 SHA-256 tree 摘要，但不记录本机绝对源码路径。摘要使用有长度
边界的记录编码，覆盖相对路径、类型、内容以及文件/目录的 executable bits，避免
分隔歧义和“内容没变但脚本已不可执行”的假同步。以后同步据此区分：

- 已管理且未手改的旧版本：安全升级；
- 已管理但被手改的副本：拒绝覆盖，`--check` 报 drift；
- 同名但未管理的目录：拒绝接管；
- 已从源码删除、此前由本系统管理的 skill：安全清理；
- 与本系统无关的其他 skill：始终保留。

确认目标副本可以被重新生成时才加 `--force`。从旧版无 manifest 安装首次迁移到
新协议时，同名目录会被视为未管理，也需要一次显式 `--force`。

---

## 为什么是这个结构

这套结构是从真实项目（一个包含前端 / 后端 / 数据库的大型网站工程）长期使用中
反复打磨出来的。踩过的坑包括：

- **MAP 膨胀**：最初 MAP 想做"概念→文件"快速索引，结果 agent 出于好意把全量端点、
  全量组件都列进去，慢慢长成几百行的代码目录册，违背了"快速导航"的初衷。
  → 解法：MAP 只记**概念→入口文件**（1-2 个），全量信息留给代码。

- **STATUS 流水账**：STATUS 的 Done 区不断追加，变成无叙事弧度的长流水账。
  → 解法：STATUS 只留最近 3-5 条，沉淀下来的里程碑进 HISTORY。

- **状态重复**：STATUS 和 PROGRESS 都维护模块卡点、下一步，时间久了互相矛盾。
  → 解法：STATUS 拥有项目级快照；PROGRESS 拥有模块级状态，其他位置只写影响和链接。

- **细节黑洞**：为了保持活跃文档精简，旧方案和实验细节被随手移走，之后无法追溯。
  → 解法：先把稳定结论蒸馏进 owner，再用带 manifest 的 archive bundle 保留来源。

- **DECISIONS 线性膨胀**：每条 rationale 永久堆在活跃文件里，真正有效的决策被淹没。
  → 解法：当前视图突出仍适用的选择，完整 ID 与理由放到可检索的主题索引 / 详情。
  保留 lifecycle、自然关键词、旧引用和替代关系，不让默认读取表随历史无限追加。

- **历史首个命中误导**：搜索先命中 proposal 或 promising pilot，就误以为它是最终结论。
  → 解法：只在相关任务中做有界历史检索，并继续追到 confirmation、closure 或
  superseded；当前 owner 定义现状，archive 只提供出处。

- **模板污染**：早期模板自带示例文字，复制进新项目后，agent 觉得"这不是我的项目"，
  惰性不更新。
  → 解法：模板保持干净占位，三层职责清晰，每个文件有明确边界。

- **docs 命名冲突**：很多项目本身就有 `docs/`，再用 `docs/` 会混淆。
  → 解法：统一叫 `memory-docs/`，语义自解释，不与项目自有 `docs/` 冲突。

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
│   │   └── DECISIONS.md     ← 当前决定 + 完整历史的按需检索路由
│   ├── DIRS.md              ← 路由层：子文件夹注册表
│   ├── SHORT_MEMORY/        ← 会话级临时上下文
│   └── archive/             ← 历史归档
│
├── project-memory-docs/     ← vibe-memory-system 自己的演进记录（gitignore）
├── skills/                  ← 配套 Agent skills 的唯一源码
│   ├── init-memory/         ← 首次初始化 / 迁移
│   └── update-living-docs/  ← 增量维护 + 轻量健康检查
└── scripts/
    ├── install_to_project.py     ← 跨平台安装器
    ├── install_to_project.sh     ← Bash 包装器
    ├── sync_skills.py            ← 单一同步引擎 + manifest / check / rollback
    ├── sync_to_claude.sh         ← Claude 用户级薄包装
    ├── sync_to_codex.sh          ← Codex 用户级薄包装
    ├── validate_memory_docs.py   ← 结构 + 轻量健康检查
    ├── test_memory_docs_tools.py ← 安装器回归测试
    ├── test_sync_skills.py       ← 同步故障与漂移测试
    └── test_validate_memory_docs.py ← 健康检查回归测试
```

> 注意：框架层模板文件**平铺在根目录**，详细层文件收入 `detail_mem/` 子文件夹。
> `project-memory-docs/` 是**本项目自用**的，已加入 `.gitignore`，两者不混淆。

---

## 配套 Skills

| Skill | 用途 |
|---|---|
| `init-memory` | 首次接入时扫描仓库，把 memory-docs 模板一次性填成真实内容 |
| `update-living-docs` | 工作收尾时审议记忆，按已确认范围集中更新并验证 |
| `evolutionary-development` | Explore / probe / 直接实现、Integrate、验证与 Consolidate 边界 |
| `research-scaffold` | 初始化或调整研究目录职责，连接现有 memory，区分材料、判断、代码与写作 |
| `research-engineering` | 数据与研究语义、可复现执行、探针和正式测试 |
| `commit-pipeline` | plan → stage → message → commit |
| `git-understand` | 新会话快速建立仓库上下文 |

---

## 科研项目（可选）

新建或调整研究项目目录时使用 `research-scaffold`。它提供可选择的研究目录和初始化脚本，
新项目接入当前 memory 模板，已有项目沿用实际记忆入口；不要求统一搬迁为固定目录树。
该 skill 随现有 skills 安装与同步流程分发。

持续产生实验协议、artifact、结果和 claim boundary 的项目，可以让 `init-memory`
从 skill asset 创建：

```text
memory-docs/research/EXPERIMENT_LEDGER.md
```

启用后要在 `DIRS.md` 注册 `research/`。账本记录实验问题、协议、可比性条件、结果、
解释、不确定性和结论边界；当前 TODO、下一步实验、服务器实时状态和原始日志仍分别
留给 `STATUS`、`PROGRESS`、session memory 或外部 artifact。普通项目无需创建它。

---

## 设计原则

- **职责清晰比格式统一重要**：每个文件只做一件事，边界用 `not_for` 写明。
- **一个事实一个 owner**：非 owner 只保留局部结论和链接，避免多个“最新状态”。
- **默认读取聚焦**：当前答案可见；历史和长证据按需读取，必要时按主题 / 阶段拆分。
- **按工作单元更新**：先确认收尾与记忆范围，再集中沉淀，允许充分记录复杂过程。
- **导航优先于细节**：memory-docs 是地图，不是百科全书。
- **先蒸馏再归档**：当前结论必须直接可见，最细来源仍可检索。
- **按需追完整生命周期**：历史相关任务用少量关键词查命中，不预载全部历史，
  也不停在第一个 proposal / pilot。
- **健康检查辅助判断**：启发式 warning 不自动删改内容。
- **证据核验**：文档与实现冲突时核验并说明；记忆修正在已确认批次中进行。
