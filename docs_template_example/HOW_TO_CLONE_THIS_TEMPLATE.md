# 如何复制这套模板到其他项目

> **职责**：用最少步骤把本模板迁移到新项目，并保留“核心动态文档 + 扩展层 + 归档”的分层设计。

## 步骤

1. 复制目录：`docs_template/` → `<你的项目>/docs/`

   也可以直接运行：

   ```bash
   scripts/install_to_project.sh <你的项目>
   ```

2. 先填 6 个核心动态文档：
   - `OVERVIEW.md`
   - `STATUS.md`
   - `DECISIONS.md`
   - `GLOSSARY.md`
   - `RUNBOOK.md`
   - `CONVENTIONS.md`

3. 根据项目复杂度决定是否启用扩展层：
   - `PROGRESS.md`
   - `MAP.md`
   - `SHORT_MEMORY/`

4. 把旧的日期文档、阶段记录、失败复盘迁入 `docs/archive/`

5. 在项目级 Agent 配置文件（如 `CLAUDE.md`、`AGENTS.md`）加入 docs 入口：

   ```markdown
   ## Agent 必读文档（按优先级）
   1. **docs/README.md** — 文档总入口与阅读顺序
   2. **docs/OVERVIEW.md** — 项目总览与主线
   3. **docs/STATUS.md** — 当前高层状态
   4. **docs/RUNBOOK.md** — 如何运行、产物位置
   5. **docs/CONVENTIONS.md** — 仓库硬规则与 contract
   6. **docs/DECISIONS.md** — 历史设计决策
   7. **docs/GLOSSARY.md** — 术语与变量定义
   ```

6. 如果项目使用 Agent 技能，可同步复制相关自动更新能力：
   - Skill：`.claude/skills/update-living-docs/SKILL.md`

> 如果项目不使用 Claude Code / Copilot 的 Agent 模式，可以跳过第 6 步。

## 最小维护纪律

每个文档的 update_mode 决定了"怎么改"，维护时请遵循：

| 触发场景 | 更新哪个文件 | Update Mode | 操作方式 |
|---|---|---|---|
| 项目方向或架构变化 | `OVERVIEW.md` | rewrite | 整体重写为最新全貌 |
| 里程碑完成或主线切换 | `STATUS.md` | rewrite | 用最新状态覆盖全文 |
| 某个模块实现状态变了 | `PROGRESS.md` | patch | 只改变化的那一条 |
| 新决策产生 | `DECISIONS.md` | append | 在末尾追加，不改已有条目 |
| 新术语或新口径引入 | `GLOSSARY.md` | patch | 新增或修改具体术语条目 |
| 跑法或产物位置变化 | `RUNBOOK.md` | rewrite | 整体重写为最新全貌 |
| 规则或 contract 变化 | `CONVENTIONS.md` | patch | 新增或修改具体规则 |
| 重要映射关系变化 | `MAP.md` | patch | 新增或修改具体映射 |
| 会话快结束但结论未稳定 | `SHORT_MEMORY/` | append | 新建文件追加 |
| 探索完成或碰壁后留痕 | `archive/` | append | 新建文件归档 |

关键边界提醒：
- **STATUS vs PROGRESS**：STATUS 是高层快照（rewrite，3-5 条），PROGRESS 是模块级清单（patch，20-50 条）
- **GLOSSARY vs MAP**：GLOSSARY 定义"概念是什么"，MAP 定义"概念在哪里"
