# 如何复制这套模板到其他项目

> **职责**：用最少步骤把本模板迁移到新项目，并保留“核心动态文档 + 扩展层 + 归档”的分层设计。

## 步骤

1. 复制目录：`docs_template_example/` → `<你的项目>/docs/`

2. 先填 6 个核心动态文档：
   - `OVERVIEW.md`
   - `STATUS.md`
   - `DECISIONS.md`
   - `GLOSSARY.md`
   - `RUNBOOK.md`
   - `CONVENTIONS.md`

3. 根据项目复杂度决定是否启用扩展层：
   - `REPO_STATUS.md`
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
   - Slash Command：`.claude/commands/update-docs.md`
   - Skill：`.claude/skills/update-living-docs/SKILL.md`

> 如果项目不使用 Claude Code / Copilot 的 Agent 模式，可以跳过第 6 步。

## 最小维护纪律

- 项目方向或架构变化：更新 `OVERVIEW.md`
- 里程碑完成或主线切换：更新 `STATUS.md`
- 复杂实现状态需要更细追踪：更新 `REPO_STATUS.md`
- 新决策产生：追加 `DECISIONS.md`
- 新术语或新口径引入：更新 `GLOSSARY.md`
- 跑法或产物位置变化：更新 `RUNBOOK.md`
- 规则或 contract 变化：更新 `CONVENTIONS.md`
- 重要映射关系变化：更新 `MAP.md`
- 会话快结束但结论未稳定：写入 `SHORT_MEMORY/`
- 一次探索完成或碰壁后需要留痕：归档到 `archive/`
