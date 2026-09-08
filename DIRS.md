---
layer: routing
update_mode: patch
role: "路由层 —— memory-docs 里有哪些子文件夹、各是干什么的（子目录注册表）"
read_when: "看到一个不认识的子文件夹、或要新建子文件夹时"
not_for: "代码位置（-> MAP），术语（-> GLOSSARY）"
---

# DIRS — 子目录注册表

> memory-docs 的详细层支持**任意子文件夹**。不规定名字，只规定**模式**：
>
> 当主题有独立职责或需要按需路由时，在确认的记忆更新中创建语义清晰的 owner，
> 必要时放入子文件夹，并在本文件登记。篇幅长可以保留，不为几行文字机械新建目录。
>
> Agent 任何时候读这张表，就能知道 memory-docs 里有哪些子文件夹、各是什么。

## 预置目录

| 目录 | 用途 | 什么时候用 | 更新模式 |
|---|---|---|---|
| `detail_mem/` | 详细层主目录：MAP / PROGRESS / DECISIONS 等按需查阅的文件 | 需要代码导航、模块进度、决策记录时 | patch / append |
| `SHORT_MEMORY/` | 会话级临时上下文交接 | 长会话中断、Agent 间交接 | append |
| `archive/` | 已完成 / 旧的归档记录 | 方案定稿、复盘、旧快照 | append |

## 可选目录

| 目录 | 用途 | 什么时候用 | 更新模式 |
|---|---|---|---|
| `research/` | 实验协议、artifact、结果、解释与 claim boundary | 项目持续产生需要比较和追溯的实验时 | append |

只有真正需要时才创建可选目录。若启用 `research/`，可从 `init-memory` skill 的
asset 创建 `EXPERIMENT_LEDGER.md`；当前 TODO、下一步和机器实时状态仍不写进账本。

## 自建目录（按需追加）

> 命名建议用语义清晰的英文 / 拼音目录名，如 `feature/`、`handover/`、`ops/`、
> `design/`、`migration/`。每新建一个，就在下面登记一行。

| 目录 | 用途 | 什么时候用 | 登记日期 |
|---|---|---|---|
| `<示例: feature/>` | `<某功能的详细设计页>` | `<新功能开始设计时>` | `<YYYY-MM-DD>` |

## 规则

- 新建子文件夹后**必须**回这里登记，否则别的 Agent 不知道它存在。
- 目录废弃时，在此标注（不要直接删，以免历史断链），或在 `archive/` 留个说明。
- 子文件夹内部仍遵循 one-owner：详细信息可以充分，但不要和另一个活跃 owner 重复。
