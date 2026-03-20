# Archive

> **职责**：存放历史文档快照、阶段记录、失败复盘和一次性分析材料，用于回溯，不作为日常工作入口。

---

## 归档规则

- 归档内容应尽量保持原始时间点真实性，迁入后一般不再重写
- 仍然有效的结论应提取到上层动态文档或 `MAP.md`
- 与动态文档冲突时，以当前动态文档为准
- `archive/` 适合保存“完整记录”，不适合保存“尚未稳定的上下文卸载”

## 和 `SHORT_MEMORY/` 的区别

- `SHORT_MEMORY/`：会话级卸载，目的是让后续 Agent 能接续当前讨论
- `archive/`：阶段性留痕，目的是保留可回溯的历史记录

如果你只是担心这轮对话 compact 后丢失上下文，优先写进 `SHORT_MEMORY/`。  
如果一轮探索已经结束，或一次碰壁/诊断值得长期保留，放进 `archive/`。

## 建议命名

- `YYYYMMDD_topic.md`
- `YYYYMMDD_milestone_retrospective.md`
- `YYYYMMDD_failed_experiment.md`

## 示例

- `20260228_method_review.md`
- `20260303_experiment_failure_retrospective.md`
- `20260315_reason_audit_notes.md`
