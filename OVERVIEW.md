---
layer: framework
update_mode: rewrite
role: "项目是什么 —— 一页纸的整体认知（做什么、怎么组织、技术栈）"
read_when: "进入项目、问架构 / 范围 / 技术栈时"
not_for: "当前进度（-> STATUS），项目演变（-> HISTORY），术语（-> GLOSSARY），代码位置（-> MAP）"
---

# Project Overview

> 复制到项目后，把本文件填成你项目的真实概览。**保持精简**：这里是"框架认知"，
> 不要塞全量目录树或全量 API 列表（那些留给代码或 `detail_mem/MAP.md` 的入口指针）。

## 一句话定位

`<项目名>` 是 `<做什么、解决什么问题>`。

## 目标

- `<目标>`
- `<目标>`

## 主要业务流 / 工作流

用几句话 + 一个简单的流程图说明核心链路即可。复杂细节留给子文件夹。

```text
<输入>
  -> <处理 / 转换>
  -> <核心逻辑>
  -> <输出 / 交付>
```

## 核心服务 / 模块

只列**顶层**的几个服务或模块，每个一句话。不要把每个子组件都写进来。

| 服务 / 模块 | 角色 | 入口（指针，详见 detail_mem/MAP.md） |
|---|---|---|
| `<模块>` | `<职责>` | `<入口文件>` |

## 技术栈

- 运行时 / 语言：
- 框架：
- 数据 / 存储：
- 外部依赖：

## 相关文档

- 当前状态：`<memory-docs>/STATUS.md`
- 项目演变：`<memory-docs>/HISTORY.md`
- 术语：`<memory-docs>/GLOSSARY.md`
- 约定：`<memory-docs>/CONVENTIONS.md`
- 代码导航：`<memory-docs>/detail_mem/MAP.md`
