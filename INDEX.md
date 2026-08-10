---
layer: framework
update_mode: rewrite
role: "memory-docs 入口 —— 三层结构说明、阅读顺序、更新协议"
read_when: "第一次进入 memory-docs，或不确定某条信息该写进哪个文件时"
not_for: "项目本身的内容（-> OVERVIEW 等其他文件）"
---

# Memory Docs 入口

这个文件夹是**给 Agent 看的项目记忆层**。它的唯一目标是：

> 让 Agent 快速建立项目的**框架认知**，并知道**去哪里找细节**，
> 而不是把所有细节都塞进这里。

---

## 核心哲学

memory-docs **不是**项目的完整 API 手册或代码目录册。

它是**框架 + 导航**：
- **框架**：项目是什么、现在在做什么、怎么来的、有什么约定 —— 这些几乎不随项目增长。
- **导航**：当 Agent 需要某个功能的细节时，知道去哪个文件 / 哪个入口钻。
- **证据保真**：活跃层只保留可行动结论；仍有复查价值的来源和细节进入可检索 archive。

凡是要随项目**线性膨胀**的东西（全部 API 端点、全部组件、全部数据表……），
都不应堆进框架层；优先留在代码或原始产物中，确需长期解释时放进按需自建的
详细 owner，完成或被替代后再归档。

---

## 三层结构

### 框架层 —— 进项目必读，永远精简

这些文件**增长极慢**，是 Agent 建立认知的基底。

| 文件 | 回答什么 | 更新模式 |
|---|---|---|
| `<memory-docs>/OVERVIEW.md` | 项目**是什么**、怎么组织 | rewrite |
| `<memory-docs>/STATUS.md` | **现在**在做什么（当前焦点 + 最近 3-5 条） | rewrite |
| `<memory-docs>/HISTORY.md` | 项目是**怎么走到今天**的（时间线叙事） | append |
| `<memory-docs>/CONVENTIONS.md` | 有哪些**硬规则 / 约定** | patch |
| `<memory-docs>/GLOSSARY.md` | 项目**术语**是什么意思 | patch |

### 路由层 —— 查"去哪找"

| 文件 | 回答什么 | 更新模式 |
|---|---|---|
| `<memory-docs>/DIRS.md` | 详细层里**有哪些子文件夹**、各是干什么的 | patch |

### 详细层 —— 按需读，随项目自由生长

这些文件**会随项目变大**，Agent 不进项目时不必读，需要细节时再查。

| 文件 / 目录 | 回答什么 | 更新模式 |
|---|---|---|
| `<memory-docs>/detail_mem/MAP.md` | 某个**概念 / 功能**对应代码的**入口文件**在哪 | patch |
| `<memory-docs>/detail_mem/PROGRESS.md` | 各模块**实现到什么程度**（清单，非流水账） | patch |
| `<memory-docs>/detail_mem/DECISIONS.md` | 当前决策生命周期、结论与详细理由 | append（registry 可 patch） |
| `<memory-docs>/SHORT_MEMORY/` | 会话级**临时上下文**交接 | append |
| `<memory-docs>/archive/` | 已完成 / 旧的**历史记录** | append |
| `<memory-docs>/research/EXPERIMENT_LEDGER.md` | 可选：实验协议、结果、证据边界 | append |
| `<memory-docs>/<自建>/` | Agent 按需新建的详细页（见 DIRS.md） | append |

---

## 阅读顺序

**进入项目时（最小集，必读）**：

1. `<memory-docs>/OVERVIEW.md`
2. `<memory-docs>/STATUS.md`
3. `<memory-docs>/CONVENTIONS.md`

**按需查阅**：

- 不懂某个词 → `GLOSSARY.md`
- 想知道项目演变 → `HISTORY.md`
- 要找个功能 / 代码入口 → `detail_mem/MAP.md`
- 要看模块完成度 → `detail_mem/PROGRESS.md`
- 想了解某个决策的来龙去脉 → `detail_mem/DECISIONS.md`
- 不知道某个子文件夹是干嘛的 → `DIRS.md`
- 接手未完成的会话 → `SHORT_MEMORY/`
- 查实验协议、结果或 claim boundary → `research/EXPERIMENT_LEDGER.md`（若存在）
- 翻旧账 / 复盘 → `archive/`

### 条件式历史检索

普通进入项目时不要预载全部历史。只有在判断 prior work、避免重复实现、重开旧路线、
反转稳定决策、诊断回归或解释原因时，才用 2-4 个主题词及别名检索
`DECISIONS`、`STATUS/HISTORY`、实验账本、计划 / 研究记录、archive 文件名 /
manifest 和相关 Git。manifest 没有路由时，再检索匹配的 flat archive note。
只打开有用命中，不停在第一个结果；确认 proposal、pilot、confirmation、closure /
superseded 的完整生命周期。当前 owner 优先，并用代码或产物核验关键结论。

---

## 更新协议（关键）

这套系统最大的价值在于：**每一类信息都有明确的归属**。Agent 不必猜"这条记哪"。

### 通用规则

- 写入前先判断：这条信息**稳定**了吗？属于哪一层？
- 每类可重复查询的事实只选一个**详细 owner**；其他文件只写本地需要的结论和链接。
- `STATUS.md` 拥有项目级当前快照；`detail_mem/PROGRESS.md` 拥有模块级实现状态。
- 框架层文件**不能无限增长**。若某段内容开始膨胀，把它移到详细层或子文件夹。
- 压缩或归档前，先把仍然有效的结论蒸馏进 owner；不要把活跃 blocker 藏进 archive。
- 代码与文档冲突时，**以代码为准**，并同步修正或标记文档。
- 不把未稳定的讨论直接写成事实。
- 计划是 proposal，不是当前事实；完成、放弃或替代后要留下
  closure / superseded 指针，指向当前 owner、决策或 archive manifest。

### 常见工程事件 → 更新哪个文件

| 发生了什么 | 主要更新 | 可能附带 |
|---|---|---|
| 新增 / 改了一个 API 端点 | `detail_mem/MAP.md`（概念→入口文件，**一行**） | `STATUS.md` Done（**一句话**） |
| 新增 / 改了一个前端功能 | `detail_mem/MAP.md`（功能→入口文件） | `STATUS.md` 一句话 |
| 修了一个 bug | `STATUS.md` 一句话 | 复杂根因可写进自建子文件夹 |
| 加了一张数据库表 / 字段 | `detail_mem/MAP.md`（表→入口文件） | 重大变更记 `detail_mem/DECISIONS.md` |
| 做了一个重要架构选择 | `detail_mem/DECISIONS.md`（一条） | — |
| 完成一次可复用实验 | `research/EXPERIMENT_LEDGER.md`（若已启用） | `STATUS.md` 只留当前影响 |
| 完成一段会话、要交接 | `SHORT_MEMORY/`（一篇） | — |
| 某方案定稿、沉淀下来 | `HISTORY.md`（时间线条目） | 旧 STATUS 条目可清掉 |
| 一组来源完成 / 被替代 | `archive/YYYYMMDD_topic/` + manifest | 先更新对应 live owner |
| 建了一个新的子文件夹 | `DIRS.md`（登记一行） | — |

> `detail_mem/MAP.md` 只记**概念 → 入口文件**（1-2 个文件），
> **不要**记全量端点 / 全量组件 / 全量字段清单。
> 全量信息留给代码本身。

### 轻量健康检查

安装了本仓库的工具后运行：

```bash
python3 .memory-docs-tools/validate_memory_docs.py .
```

结构错误会阻断；断链、膨胀、陈旧、异常超长普通 prose 单行、长段重复和 archive
可检索性属于 warning。warning 是人工判断入口，不会自动删除、归档或重写内容；
需要在自动化中阻断时使用 `--strict`。

---

## 复制到你的项目后

把整个文件夹复制进你的项目，改名为 `memory-docs/`，然后：

1. 把文件里所有 `<memory-docs>/` 占位换成 `memory-docs/`。
2. 让 Agent 读 `INDEX.md`（本文件）建立认知。
3. 让 Agent 用 `init-memory` 之类的能力扫描仓库，把模板填成真实内容。

如果你的项目根目录已有 `AGENTS.md`，把本项目 `AGENTS.md` 中的
"memory-docs 使用指引"部分合并进去。
