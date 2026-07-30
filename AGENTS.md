Always respond in Chinese-simplified.

# AGENTS.md Template

这个文件是项目级 Agent 入口。复制到目标仓库后，可在保留基础规则的前提下，
追加该仓库特有的任务说明、目录约定、运行方式和禁止事项。

---

## 基础原则

- 优先遵守当前仓库的代码、脚本、测试和最新结果；文档与实现不一致时，**以实现为准**，并明确指出不一致。
- 不提交本机绝对路径、私有虚拟环境路径、账号、密钥、token 或机器特定配置。
- 用可移植路径示例：`.venv`、`$HOME`、`<project-root>`。
- 不回滚或覆盖用户已有改动，除非用户明确要求。
- 改之前先理解现有结构和本地约定，优先沿用仓库已有模式。

---

## memory-docs 使用指引

本项目用 `memory-docs/` 文件夹作为 Agent 的项目记忆层。
**核心哲学**：让 Agent 快速建立**框架认知**并知道**去哪找细节**，
而不是把项目的每个 API、组件、字段都塞进记忆。

### 三层结构

| 层 | 文件 | 性质 |
|---|---|---|
| **框架层**（进项目必读，永远精简） | `OVERVIEW` `STATUS` `HISTORY` `CONVENTIONS` `GLOSSARY` | 增长极慢 |
| **路由层** | `DIRS` | 查"详细层里有什么" |
| **详细层**（按需读，随项目生长） | `detail_mem/MAP` `detail_mem/PROGRESS` `detail_mem/DECISIONS` `SHORT_MEMORY/` `archive/` `<自建>/` | 保留详细 owner 与证据 |

入口与完整说明见 `memory-docs/INDEX.md`。

### 阅读顺序

**进入项目（最小集）**：

1. `memory-docs/OVERVIEW.md` —— 项目是什么
2. `memory-docs/STATUS.md` —— 现在做什么
3. `memory-docs/CONVENTIONS.md` —— 有什么硬规则

**按需查阅**：

- 不懂术语 → `GLOSSARY.md`
- 想知道项目演变 → `HISTORY.md`
- 找代码入口 → `detail_mem/MAP.md`
- 看模块完成度 → `detail_mem/PROGRESS.md`
- 了解决策来由 → `detail_mem/DECISIONS.md`
- 不认识某子文件夹 → `DIRS.md`
- 接手未完成会话 → `SHORT_MEMORY/`
- 查实验协议、结果和证据边界 → `research/EXPERIMENT_LEDGER.md`（若启用）
- 翻旧账 → `archive/`

若某文件不存在，跳过即可；不要为满足模板而虚构内容。

### 条件式历史检索

普通任务不要预载全部历史。只有在准备断言"以前没做过"、避免重复实现、重开旧路线、
推翻稳定决策、诊断回归或解释"为什么"时，才先用 2-4 个主题词及别名检索
`DECISIONS`、`STATUS/HISTORY`、实验账本、计划 / 研究记录、archive 文件名 /
manifest 和相关 Git。若 manifest 没有路由到主题，再检索匹配的 flat archive note。
只读有用命中，但不要停在第一个结果；要确认
proposal → pilot → confirmation → closure / superseded 的最终阶段。
当前 owner 优先，重要结论再用代码、测试或产物核验。完整流程见 `update-living-docs`。

### 更新协议（关键）

每类信息都有明确归属，Agent 不必猜"这条记哪"。

**通用规则**：
- 每类可重复查询的事实只维护一个详细 owner；非 owner 只写本地影响和链接。
- `STATUS.md` 拥有项目级当前快照；`detail_mem/PROGRESS.md` 拥有模块级状态、卡点和下一步。
- 框架层文件**不能无限增长**；某段内容开始膨胀就移到详细层 / 子文件夹。
- 先把稳定结论蒸馏进 owner，再归档完成、替代、拒绝或被压缩的来源细节。
- 不要把活跃 blocker、当前 TODO 或机器实时状态藏进 archive / 实验账本。
- 代码与文档冲突，**以代码为准**，并修文档或标记。
- 不把未稳定讨论直接写成事实。
- 计划默认只是 proposal，不代表当前状态；完成、放弃或被替代后必须留下
  closure / superseded 指针，指向当前 owner、决策或 archive manifest。

**工程事件 → 更新哪个文件**：

| 发生了什么 | 主要更新 | 附带 |
|---|---|---|
| 新增 / 改 API 端点 | `detail_mem/MAP.md` 加**一行**（概念→入口文件） | `STATUS.md` 一句话 |
| 新增 / 改前端功能 | `detail_mem/MAP.md` 加一行 | `STATUS.md` 一句话 |
| 修 bug | `STATUS.md` 一句话 | 复杂根因写进自建子文件夹 |
| 加数据表 / 字段 | `detail_mem/MAP.md` 加一行 | 重大变更记 `detail_mem/DECISIONS.md` |
| 重要架构选择 | `detail_mem/DECISIONS.md` 加一条 | — |
| 完成可复用实验 | `research/EXPERIMENT_LEDGER.md`（若启用） | `STATUS.md` 只留当前影响 |
| 会话要交接 | `SHORT_MEMORY/` 写一篇 | — |
| 方案定稿沉淀 | `HISTORY.md` 加时间线条目 | 旧 STATUS 条目可清掉 |
| 多份来源完成 / 被替代 | `archive/YYYYMMDD_topic/` + manifest | 先更新对应 live owner |
| 建新子文件夹 | `DIRS.md` 登记一行 | — |

> **`detail_mem/MAP.md` 只记"概念 → 入口文件"（1-2 个），不要记全量清单。**
> 全量信息留在代码里。

### 结构与健康检查

如果项目安装了本地校验器，在 memory-docs 初始化或结构变更后运行：

```bash
python3 .memory-docs-tools/validate_memory_docs.py .
```

结构问题是 error；断链、文档膨胀、显式状态陈旧、异常超长普通 prose 单行、
长段重复和 archive manifest 问题是 warning。warning 默认不阻断，需要严格模式时
使用 `--strict`。检查器不会自动删除、归档或重写内容。

当前标准不包含 `MEMORY_MANIFEST.yml`、`RUNBOOK.md` 或 `memory-docs/README.md`；
除非目标项目另有独立用途，不要恢复旧体系文件。

---

## Skills 使用

- Skill 的完整流程由各自 `SKILL.md` 定义，本文件只说明何时用。
- **首次接入**：刚把 memory-docs 安装到已有仓库时，用 `init-memory` 扫描仓库，把模板一次性填成真实内容。
- 做完有意义的代码 / 文档 / 决策 / 映射 / 实验工作后，优先用 `update-living-docs`
  把验证过的事实写进 owner，并运行轻量健康检查。
- 准备提交时用 `commit-planner` 拆批；要完整流程用 `commit-pipeline`。
- 涉及 Python 数据处理、回归、诊断、测试、绘图时，用 `research-engineering`。
- 某个 skill 当前环境不可用时，按下面的 fallback 执行，并说明降级原因。
- 若 `.claude/skills/` 或 `.agents/skills/` 中存在
  `.vibe-memory-system-skills.json`，manifest 列出的 skill 是安装生成物：
  不要直接修改；从 canonical `skills/` 更新并重新同步。未列出的其他 skill
  仍归项目或用户所有，不得顺带删除。

## Python / 数据处理 fallback

没有 `research-engineering` 但任务涉及 Python / 数据 / 回归 / 测试 / 绘图时：

- 路径定位基于 `pathlib.Path` 与 `__file__`，不依赖 `cwd` 或裸相对路径。
- 默认先写可被标准测试发现的 `test_*.py`，或先做最小诊断脚本，再决定是否动核心代码。
- 巨型文本 / JSON / JSONL / CSV 先做头部预览、抽样或流式读取，别整文件加载进上下文。
- 结果文件、日志、图表、缓存沿脚本所在目录或父目录输出。
- 暴露真实错误；不预埋静默 fallback、空值替代或 `except: continue`。
- 若 fallback 影响研究口径、样本定义、统计含义或下游解释，先停下来向用户确认。

---

## 仓库特定补充

复制到目标仓库后，在此追加该项目自己的规则。例如：

- 主线开发目录：
- legacy / 只读目录：
- 默认运行环境：
- 关键命令：
- 禁止手改的自动生成产物：
- 必须一致的展示命名 / 图表规范 / API 契约：
