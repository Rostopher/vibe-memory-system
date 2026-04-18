# Project Status

> **职责**：记录"项目当前主线推进到哪了"。它是高层状态入口，应该保持精简，只写当前阶段最值得频繁查看的信息。
>
> **update_mode: rewrite** — 每次更新时用最新全貌覆盖旧内容。这是一份"快照"，不是追加日志。

> **最后更新**：YYYY-MM-DD

> **边界说明 — STATUS vs PROGRESS**：
>
> `STATUS.md` 是**高层快照**（rewrite）：用 3-5 条 bullet 概括项目整体推进到哪了，每次更新直接用最新状态覆盖全文。
>
> `PROGRESS.md` 是**模块级清单**（patch）：可能有 20-50 条逐项 checklist，某个模块状态变了就改那一条。
>
> 判断边界：如果你要写的内容是"项目整体做到哪了"，写在 STATUS；如果是"某个具体模块做了没有"，写在 PROGRESS。
>
> 其他相邻文件边界：
> - 稳定决策的理由 → `DECISIONS.md`（append）
> - 术语定义 → `GLOSSARY.md`（patch）
> - 实现映射 → `MAP.md`（patch）

---

## 1) Scope（当前主线范围）

- 当前项目目标：
- 当前主线目录 / 仓库：
- 当前主线版本 / 阶段：
- 如果有 legacy / historical implementation，当前是否仍需维护：

## 2) Done（高层）

- [x] 里程碑 / 模块 A：
- [x] 里程碑 / 模块 B：
- [x] 已经稳定的关键规则或能力：

## 3) In Progress

- [ ] 当前事项 A：
  - 阻塞点：
  - 下一步：

- [ ] 当前事项 B：
  - 阻塞点：
  - 下一步：

## 4) Backlog（按优先级）

- P0：
- P1：
- P2：

## 5) Key Reminders / Current Contracts

- 当前最重要的口径或约束 1：
- 当前最重要的口径或约束 2：
- 当前最重要的口径或约束 3：

## 6) Related Pointers

- 详细状态：`docs/PROGRESS.md`
- 决策记录：`docs/DECISIONS.md`
- 运行方式：`docs/RUNBOOK.md`
- 仓库规则：`docs/CONVENTIONS.md`
- 关键映射：`docs/MAP.md`

---

> 维护原则：
>
> - 写"当前最重要的项目状态"，不是所有历史细节
> - 每次更新是 **rewrite**：用最新全貌覆盖，不保留旧版本痕迹
> - 一旦某部分开始过长，就把细节迁到 `PROGRESS.md`（patch 模式逐条更新）
> - 稳定结论应写在这里；中间讨论不应直接堆进这里
> - 不要在这里逐条追踪模块实现状态，那是 `PROGRESS.md` 的职责
