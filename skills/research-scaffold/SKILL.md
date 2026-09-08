---
name: research-scaffold
description: 初始化或调整研究项目的目录职责、研究材料与项目记忆的边界。用于建立研究脚手架、整理已有研究目录，或连接当前 vibe-memory-system；日常分析、单次实验和普通 memory 更新不单独触发。
---

# Research Scaffold

为研究工作建立可生长的目录边界，让原材料、研究判断、可执行代码、正式写作和项目记忆各有归属。
适用于单个研究项目，也可在已有多项目仓库中作用于明确的一项研究；沿用现有组织方式。

## 先确定已有边界

- 先看项目 `AGENTS.md`、README、目录和实际使用的 memory 入口，确认本次新增或调整的范围。
  用户已给出范围时直接执行，不重复要求确认。
- 下表是职责示例，不是必须一次建齐的目录清单。已有 `src/`、`tests/`、数据存储或手稿布局
  可以继续使用；不要为了套模板移动已工作的代码、数据和引用。
- 新项目默认安装当前 `vibe-memory-system` 的 `memory-docs/INDEX.md` 系统；已有项目沿用
  经确认的记忆根与入口，例如 `docs/README.md`。不另建平行 memory，也不生成旧式 docs 占位系统。

| 职责示例 | 详细内容的归属 |
|---|---|
| `memory-docs/` 或已有记忆根 | 当前项目事实、状态、规则、重要决策及检索入口 |
| `notes/` | 消化后的文献、方法、数据理解与研究判断 |
| `ideas/` | 待验证的研究问题、claim、方案，以及失败或暂缓方向 |
| `papers/` | PDF、OCR、元数据、解析图片等来源材料与生成内容 |
| `repos/` | 外部参考仓库；默认只读，需要修改时遵循本次授权 |
| `data/` | 数据、字典、来源与版本信息；按实际存储策略组织 |
| `modules/` 或已有实现目录 | 可执行流程、局部探针、正式测试、产物和运行记录 |
| `manuscripts/` | 面向读者的正式写作与可追溯的论文资产 |

判断具体内容的 owner 时读 [scaffold-contract.md](references/scaffold-contract.md)。
每项详细事实保留一个 owner，其他层用链接或定位信息连接，不复制整套研究记录。

## 初始化与增量调整

全新项目可使用随 skill 分发的 `scripts/init_research_scaffold.py`。
`<skill-dir>` 是当前这份 skill 的实际安装路径；不要假定 `.codex/skills/` 等固定目录。
传入目标项目与 memory 源仓库的绝对路径：

```text
python "<skill-dir>/scripts/init_research_scaffold.py" "<project>" --memory-system "<vibe-memory-system>"
```

- 默认创建七个研究职责目录、对应 README 和缺失的忽略文件；子目录按工作需要再建。
  只补部分职责时使用 `--directories notes ideas modules`。
- 默认保留已有 README、忽略文件、AGENTS 和 memory。`--force` 只用于明确要重置本次所选
  目录的模板说明及根 README / 忽略文件；会替换这些文件全文，不能拿来合并项目约定。
- 脚本识别 `memory-docs/` 和有项目记忆特征的 `docs/`。其他已有记忆根通过
  `--memory-root "<existing-memory-root>"` 明确声明；此参数用于沿用，不能创建自定义 memory 系统。
  自动识别只是辅助，Agent 应先核对项目入口。
- 没有可用的 `--memory-system` 时，脚本只建研究目录并报告 memory 未安装。
  不造占位 memory 冒充安装完成。安装模板后仍需根据项目事实初始化内容。
- 已有项目先提出与目标有关的目录变更，再实施已授权部分。目录职责整理不自动扩大为
  全库搬迁、旧 `_test_` 改名、历史决策迁移或整套测试体系建设。

首次填充或明确要求的协议迁移可使用同仓库的 `init-memory`；它不可用时按当前 memory
入口契约填充真实事实。初始化已在用户请求范围内时，无需另问一次是否允许写 memory。

## 研究模块如何生长

未知技术路线可在隔离 demo / side project 探索；局部未知可用 `probe_<用途>`；路径明确的
修改直接实现。Explore 可以完成为“在已测条件下可行，暂未接入”，不把 demo 跑通当作接入完成。
Integrate 应明确模块归属、完成正式运行路径并验证受影响行为；有边界的局部技术债可以保留。

模块仅按实际需要增加 README、probe、测试、输出或日志目录。新 Python 正式测试通常为
`test_*.py`；探针不承担长期回归保障。既有 `_test_` 按实际用途理解，迁移另行安排。
模块组织、关键契约、数据与验证证据见 [module-conventions.md](references/module-conventions.md)。
可用时，复杂演进用 `evolutionary-development`，具体研究执行用 `research-engineering`。

日常整理完成当前接入所需的去重、边界修正和废弃临时代码处理。版本或累计改动触发结构检查；
发现跨模块问题时说明证据、范围和收益，由用户决定 Consolidate 的时机。已有授权直接实施。

## 研究记录与 memory 的节奏

用户要求的阅读笔记、研究方案、实验报告属于本次交付；运行时的日志、参数、数据版本与产物
按执行需要保留。项目记忆的提炼在一次工作收束时集中进行，不跟随每个 probe 或小改动。
到交付节点主动询问本轮是否收束、是否更新 memory，并结合用户确认的范围一次写入。
明确要求初始化、更新、迁移或交接已构成对应授权；用户自行整理、暂缓或不写时尊重其决定。

成功、失败和暂缓的探索都值得成为候选记忆：保留问题、尝试条件、证据、局限、停止原因、
重试条件、所属仓库与 Git 版本，以及必要数据 / 配置 / 产物位置。允许完整长文；当前入口只需
让 Agent 能找到适用结论和历史证据。不要借 `SHORT_MEMORY/` 绕过批次更新约定。

持续维护可使用 `update-living-docs`。仅在初始化或实际改动 memory 目录、索引、链接等结构时
按需做一次结构检查；安装器已有验证则复用结果，不为每次正文编辑机械运行校验器。
研究型证据账本是可选 owner，持续积累可比实验时再建立；不要无条件给每个项目增加一套账本。

文献阅读需要写作辅助时读 [paper-reading-notes.md](references/paper-reading-notes.md)；
其结构可自由调整，不把阅读笔记变成必填表格。
