# Conventions

> **职责**：记录仓库级的硬规则、稳定 contract、写作/编码约定和不可随意漂移的实践规则。它不只是“代码风格”，而是项目协作边界的一部分。

> **最后更新**：YYYY-MM-DD

---

## 1) Repository-Level Rules

- 主线开发优先目录：
- 哪些目录属于 legacy / reference-only：
- 哪些目录或产物默认不要手工修改：
- 哪些文件或路径只有在用户明确要求时才能改：

## 2) Naming and Structural Rules

- Python 变量、函数、文件名用 `snake_case`
- 类名用 `CamelCase`
- 配置项和常量用全大写加下划线
- 模块边界与目录组织规则：
- 测试代码放置规则：

## 3) Error Handling and Safety

- 数据缺失、schema 断裂、关键列缺失等情况如何处理：
- 是否允许 silent skip：
- 日志与错误上下文的最低要求：
- 哪些操作必须显式报错而不是“尽量继续跑”：

## 4) Data / Interface Contracts

- 稳定输入输出层是什么：
- 哪些结果属于中间产物，哪些属于最终展示产物：
- 是否要求 tidy / long-format 作为稳定接口：
- 命名、主键、schema 的约定：

## 5) Artifact and Output Rules

- 结果目录约定（例如 `data/`, `tidy/`, `table/`, `figure/`）：
- 自动生成产物是否允许手工编辑：
- 哪些大文件或二进制默认不改：
- 产物同步 / 导出规则：

## 6) Documentation Rules

- 哪些文档是主入口：
- 什么时候更新 `STATUS.md` / `REPO_STATUS.md` / `DECISIONS.md`：
- 是否使用 `MAP.md` 维护单一映射真相源：
- 是否使用 `SHORT_MEMORY/` 做会话级上下文卸载：

## 7) Project-Specific Presentation Rules (Optional)

如果项目存在论文、报告、UI、图表、API 对外展示层，可以在这里补充：

- 命名展示规则
- 图表文本规则
- UI / API 命名规则
- 与最终资产相关的 single source of truth

## 8) Dependency and Environment Rules

- Python / Node / system version expectations：
- 新增依赖需要登记到哪里：
- 环境变量管理规则：
- 是否允许把本地路径、密钥、账号信息写进仓库：

## 9) Things That Must Be Explained

以下情况必须留下说明，不能只靠代码本身推断：

- 特殊 hack
- 非直观的数据口径
- 临时兼容逻辑
- 与常规规则不一致的实现

这些说明应至少出现在代码注释、`DECISIONS.md` 或 `CONVENTIONS.md` 之一。

---

## Recommended Minimal Hard Rules

建议把最关键的 3-5 条硬规则同时写进项目级 Agent 入口文件（如 `AGENTS.md` / `CLAUDE.md`），确保每次会话都能看到。

常见例子：

- 不要改自动生成产物
- 关键缺失直接报错，不允许 silent skip
- 不要写 hardcoded local paths
- 稳定接口优先使用 tidy outputs
