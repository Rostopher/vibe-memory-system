---
layer: detail
update_mode: append
role: "会话级临时上下文 —— 有用但还不够稳定、需要交接给下轮 Agent 的内容"
read_when: "长会话恢复、Agent 间交接时"
not_for: "稳定状态（-> STATUS/PROGRESS），稳定决策（-> DECISIONS），稳定规则（-> CONVENTIONS），已完成复盘（-> archive/）"
---

# Short Memory

> 放**对下个会话有用、但还没稳定到能进框架层**的上下文。
>
> 这是 memory-docs 详细层的一个**已有协议的子文件夹实例**。
> 新建别的子文件夹时，参考这里的协议风格，并在 `DIRS.md` 登记。

## 什么时候用

遵循入口中的工作收尾协议：用户确认写入或明确要求交接时集中整理。
不把本目录当作每个小改动的自动日志，不绕过用户暂缓或自行整理的决定。
“Short”表示上下文的暂时性，不是篇幅上限；困难排障与接续证据可以完整记录。

- 长会话需要交接笔记。
- 当前理解有用，但还属于试探性结论。
- 下一轮 Agent 需要继承、但还不构成"决策"的上下文。

## 不要放

- 稳定状态 → `STATUS.md` / `detail_mem/PROGRESS.md`
- 稳定决策 → `detail_mem/DECISIONS.md`
- 长期规则 → `CONVENTIONS.md`
- 已完成复盘 → `archive/`

## 命名

- `YYYYMMDD_topic.md`
- `session_<id>_topic.md`

并行工作可以保留多份主题明确的 handoff。若项目需要一个默认恢复入口，可维护
`CURRENT.md`：它只保留相对稳定 owner 的**会话增量**和链接，不复制整份 STATUS。

## 生命周期

1. 新会话先读仍活跃的 handoff，并验证其中假设。
2. 在确认的记忆更新批次中，将稳定结论蒸馏到相应 owner。
3. 经确认维护后清理纯临时恢复提示，或将仍有复盘价值的记录移入 archive。
4. 已失效 handoff 不得继续声称自己是“当前”入口。
