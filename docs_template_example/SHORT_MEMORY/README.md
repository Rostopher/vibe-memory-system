# Short Memory

> **职责**：存放会话级的上下文卸载材料，避免在长对话 compact 后丢失对后续 Agent 工作仍有价值的中间理解。

---

## 什么时候写进这里？

适合写入 `SHORT_MEMORY/` 的情况：

- 本轮 session 快接近上下文上限
- 当前讨论还没有形成稳定结论
- 内容不足以进入核心动态文档
- 内容又比“直接丢掉”更有价值，后续 Agent 可能需要接着做

## 不该写进这里的内容

以下内容应上提到其他层：

- 稳定项目状态：`STATUS.md` / `PROGRESS.md`
- 正式决策：`DECISIONS.md`
- 长期规则：`CONVENTIONS.md`
- 稳定术语：`GLOSSARY.md`
- 已完成的阶段性记录：`archive/`

## 建议命名

可以按日期，也可以按 session id：

- `20260315_repeat_stability_reason_audit.md`
- `session_017_api_refactor_context.md`

一天出现多个 short memory 文件是正常的。

## 使用原则

- 写“这轮讨论对下一轮最有用的最小摘要”
- 不要求完美成文，但要尽量结构清晰
- 如果其中某些结论后来稳定了，要把它们提炼回上层动态文档
