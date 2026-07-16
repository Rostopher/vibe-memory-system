---
layer: detail
update_mode: append
role: "历史归档 —— 已完成的记录、复盘、旧快照、失败探索"
read_when: "问历史问题、重建旧上下文、回顾旧方案时"
not_for: "当前状态（-> STATUS/PROGRESS），活跃会话上下文（-> SHORT_MEMORY/）"
---

# Archive

> 放**历史的、已完成的**内容：复盘、旧快照、失败探索、定稿前的方案记录。
>
> 这是 memory-docs 详细层的一个**已有协议的子文件夹实例**。
> 新建别的子文件夹时，参考这里的协议风格，并在 `DIRS.md` 登记。

## 规则

- 归档记录**忠于当时**，不事后改写。
- 仍有价值的结论，提炼进活跃文档（`STATUS` / `DECISIONS` / `HISTORY`）。
- 归档内容与活跃文档冲突时，**以活跃文档为准**。
- 不要把归档当作"当前状态"来用。

## 命名

- `YYYYMMDD_topic.md`
- `YYYYMMDD_retrospective.md`
- `YYYYMMDD_failed_experiment.md`
