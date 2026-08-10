---
layer: framework
update_mode: rewrite
role: "现在在做什么 —— 当前焦点 + 最近 3-5 条里程碑（快照，非流水账）"
read_when: "进入项目、规划工作、问当前状态时"
not_for: "模块级细节（-> PROGRESS），历史演变（-> HISTORY），决策来由（-> DECISIONS）"
line_budget: 160
stale_after_days: 14
---

# Project Status

> **本文件只保留"当前快照"。** Done 区只放最近 3-5 条里程碑，每条**一句话**。
> 再往前的内容定期**沉淀进 `HISTORY.md`**，不要在这里无限堆积。
> 本文件拥有项目级焦点、优先级和阻塞摘要；模块级状态、卡点和下一步由
> `detail_mem/PROGRESS.md` 拥有，这里只写其对项目主线的影响并链接过去。
>
> 更新时间：`<YYYY-MM-DD>`

## Current Focus

- `<当前在做什么、当前阶段>`
- `<当前阶段>`
- `<活跃的工作流 / 负责人>`

## Done（最近 3-5 条）

> 每条一句话即可。详细背景如需保留，写进 `HISTORY.md` 或相关子文件夹。

- [x] `<里程碑>` (`<日期>`) — `<一句话说明>`
- [x] `<里程碑>` (`<日期>`) — `<一句话说明>`

## In Progress

- `<跨模块工作流或项目级事项>` → 细节见 `detail_mem/PROGRESS.md`

## Backlog

- P0：`<高优先>`
- P1：`<中优先>`
- P2：`<低优先>`

## 当前必须遵守的约束（快照）

> 这里只放"当前有效、影响决策"的少数硬约束。完整规则在 `CONVENTIONS.md`。

- `<约束>`
- `<约束>`

## 相关文档

- 模块实现清单：`<memory-docs>/detail_mem/PROGRESS.md`
- 项目演变：`<memory-docs>/HISTORY.md`
- 决策：`<memory-docs>/detail_mem/DECISIONS.md`
- 约定：`<memory-docs>/CONVENTIONS.md`
