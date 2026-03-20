# Project Overview

> **职责**：用一份文档让人和 Agent 快速理解这个项目是什么、要解决什么问题、当前主线是什么、整体架构和主要目录如何组织。

> **边界说明**：`OVERVIEW.md` 负责“项目级摘要”，不是实现细节汇总。
>
> - 当前做到哪一步，优先看 `STATUS.md`
> - 更细的实现追踪，优先看 `REPO_STATUS.md`
> - 运行方法、命令和产物位置，优先看 `RUNBOOK.md`
> - 术语定义，优先看 `GLOSSARY.md`
> - 细粒度映射关系，优先看 `MAP.md`

---

## One-Sentence Description

This project is for ________.

## Project Goals / Core Questions

- Goal 1:
- Goal 2:
- Goal 3:

## Main Workstreams

如果项目存在多条主线，建议先用高层语言概括，而不是直接堆目录名。

例如：

1. Data generation / collection
2. Core analysis / product logic
3. Final outputs / reporting / UI delivery

## System Architecture

用 ASCII 图或简单列表即可，重点是帮助读者快速形成整体心智模型。

```text
Input / Source
  -> Processing / Transformation
  -> Core Logic / Analysis
  -> Final Outputs / Delivery
```

## Important Directories

| Directory | Role |
|---|---|
| `src/` / `analysis/` / `app/` | Main implementation |
| `data/` | Raw and intermediate inputs |
| `results/` / `artifacts/` | Generated outputs |
| `docs/` | Project documentation |
| `tests/` | Validation and regression checks |

根据项目实际情况替换路径，不需要拘泥于这些目录名。

## Tech Stack

- Main language / runtime:
- Key tools:
- External systems or dependencies:

## Related Pointers

- Current status: `docs/STATUS.md`
- Detailed status: `docs/REPO_STATUS.md`
- Run instructions: `docs/RUNBOOK.md`
- Decisions: `docs/DECISIONS.md`
- Conventions: `docs/CONVENTIONS.md`
- Mapping index: `docs/MAP.md`

---

> 维护原则：
>
> - 保持高层、稳定、可快速扫描
> - 项目方向或主线架构发生明显变化时优先更新这里
> - 不要把实现细节、每日进展和临时讨论堆进这里
