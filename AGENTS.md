Always respond in Chinese-simplified.

# AGENTS.md Template

这个文件是项目级 Agent 入口模板。复制到目标仓库后，可以在保留基础规则的前提下，继续追加该仓库特有的任务说明、目录约定、运行方式和禁止事项。

## 基础原则

- 优先遵守当前仓库的代码、脚本、测试和最新结果；当文档与实现不一致时，以当前实现为准，并明确指出不一致。
- 不要提交个人本机绝对路径、私有虚拟环境路径、账号、密钥、token 或机器特定配置。
- 使用可移植路径示例，例如 `.venv`、`$HOME`、`<project-root>`。
- 不要回滚或覆盖用户已有改动，除非用户明确要求。
- 修改前先理解现有结构和本地约定，优先沿用仓库已有模式。

## 项目上下文获取

需要项目背景、研究口径、目录映射、近期状态、历史决策时，优先查看 `docs/` 下面的动态文档系统，而不是依赖聊天上下文。

建议阅读顺序：

1. `docs/MEMORY_MANIFEST.yml`：结构化阅读顺序与更新规则
2. `docs/README.md`：文档系统入口
3. `docs/OVERVIEW.md`：项目整体概览
4. `docs/STATUS.md`：当前高层状态
5. `docs/RUNBOOK.md`：运行方式、验证方式和产物位置
6. `docs/CONVENTIONS.md`：仓库硬规则与 contract
7. `docs/DECISIONS.md`：关键决策与理由
8. `docs/GLOSSARY.md`：术语、变量、命名口径

按需继续查看：

- `docs/PROGRESS.md`：模块/feature 级实现清单
- `docs/MAP.md`：概念、feature、产物与文件映射
- `docs/SHORT_MEMORY/`：会话级上下文卸载
- `docs/archive/`：历史记录、复盘、旧方案

如果某些文档不存在，跳过即可；不要为了满足模板而虚构内容。

## Skills 使用

- Skills 的完整流程由各自的 `SKILL.md` 定义，`AGENTS.md` 只说明何时优先使用。
- 完成有意义的代码、文档、决策、映射或运行方式变更后，优先使用 `update-living-docs` 判断是否需要回写 `docs/`。
- 准备提交时，优先使用 `commit-planner` 拆分提交；需要完整提交流程时使用 `commit-pipeline`。
- 涉及 Python 数据处理、回归、诊断脚本、测试或绘图时，优先使用 `research-engineering`。
- 如果某个 skill 在当前 Agent 环境不可用，按本文件的 fallback 规则执行，并说明降级原因。

## Python / 数据处理 fallback 规则

当没有可用的 `research-engineering` skill，但任务涉及 Python、数据处理、回归、测试或绘图时：

- 路径定位必须基于 `pathlib.Path` 与 `__file__`，不要依赖 `cwd` 或裸相对路径。
- 默认先写 `_test_*.py` 或最小诊断脚本，再决定是否修改核心代码。
- 遇到巨型文本文件、JSON/JSONL/CSV 等大数据文件时，先做头部预览、抽样读取或流式读取；不要无必要整文件加载到内存或上下文。
- 结果文件、日志、图表、缓存应沿脚本所在目录或其父目录拼接输出。
- 默认暴露真实错误；不要为了“稳妥”预埋静默 fallback、空值替代或 `except: continue`。
- 若 fallback 会影响研究口径、样本定义、统计含义或下游解释，先停下来向用户确认。

## 文档维护规则

- 稳定事实写入 Base Memory：`OVERVIEW.md`、`STATUS.md`、`DECISIONS.md`、`GLOSSARY.md`、`RUNBOOK.md`、`CONVENTIONS.md`。
- 细粒度实现状态和映射写入 Scaling Memory：`PROGRESS.md`、`MAP.md`。
- 尚未稳定但下一轮会话需要继承的内容写入 `SHORT_MEMORY/`。
- 完成的探索、复盘、旧方案和历史快照写入 `archive/`。
- 不要把原始会话讨论直接写成稳定事实；先判断信息属于哪一层。

## 仓库特定补充

复制到目标仓库后，在这里追加该项目自己的规则。例如：

- 主线开发目录：
- legacy / reference-only 目录：
- 默认运行环境：
- 关键命令：
- 不能手工修改的自动生成产物：
- 必须保持一致的展示命名、图表规范或 API contract：
