# Runbook

> **职责**：说明“怎么运行、产物在哪、常见问题如何排查”。它是执行类信息的主入口，负责把项目从“看懂”推进到“跑起来”。

> **最后更新**：YYYY-MM-DD

> **边界说明**：`RUNBOOK.md` 负责运行方法、路径、命令和排障。它不负责解释项目为什么这么设计；设计理由应放在 `OVERVIEW.md` 或 `DECISIONS.md`。

---

## 1) Environment Setup

- 语言 / 运行时版本：
- 依赖安装方式：
- 关键环境变量：
- 外部依赖（例如数据库、Stata、Docker、服务账号等）：

## 2) Main Entry Points

列出最重要的运行入口，而不是所有脚本：

- 全流程入口：
- 分阶段入口：
- 调试 / dry-run 入口：
- 仅导出 / 仅同步 / 仅编译入口（如适用）：

示例：

```bash
# full run
python run.py

# selected stages
python run.py --stages stage_a stage_b

# dry run
python run.py --dry-run
```

## 3) Output Layout

说明项目产物的层级结构，以及哪些是稳定接口。

```text
results/
├── data/      # 中间产物，会被后续脚本读取
├── tidy/      # 稳定接口层，适合画图/导表/跨版本比较
├── table/     # 最终展示表，主要给人看
└── figure/    # 最终图像产物
```

补充说明：

- 哪一层是后续代码应优先读取的稳定接口：
- 哪些目录是自动生成的，不应手工编辑：
- 哪些产物是 paper-facing / UI-facing / API-facing：

## 4) Common Workflows

按项目实际情况列出最常见的几类工作：

- 生成主线结果：
- 重跑某个 stage：
- 导出最终表格 / 图像：
- 同步最终资产：
- 编译论文 / 文档 / 前端（如适用）：

## 5) Common Failures and Debugging

记录那些“高频、值得重复参考”的问题。

- 问题 A：
  - 现象：
  - 可能原因：
  - 排查：
  - 修复：

- 问题 B：
  - 现象：
  - 可能原因：
  - 排查：
  - 修复：

## 6) Related Pointers

- 项目总览：`docs/OVERVIEW.md`
- 当前状态：`docs/STATUS.md`
- 详细状态：`docs/REPO_STATUS.md`
- 决策记录：`docs/DECISIONS.md`
- 仓库规则：`docs/CONVENTIONS.md`
- 映射关系：`docs/MAP.md`

---

> 维护原则：
>
> - 只保留最常用、最可靠的运行方式
> - 把“怎么跑”和“为什么这样设计”分开
> - 一旦运行入口或产物路径变了，优先更新这里
