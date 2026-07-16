---
layer: detail
update_mode: patch
role: "概念 → 入口文件的快速导航（只记入口，不记全量清单）"
read_when: "要找某功能 / 概念的代码在哪、追溯某产物的来源时"
not_for: "术语定义（-> GLOSSARY），当前状态（-> STATUS），全量端点 / 组件 / 字段清单（留在代码里）"
---

# Map — 概念 → 入口文件

> **本文件的边界（重要）：**
>
> MAP 只记 **概念 / 功能 → 1-2 个入口文件**，是给 Agent 的**快速导航指针**。
> Agent 拿到入口后，剩下的自己读代码。
>
> **不要**把全量 API 端点、全量前端组件、全量数据字段、全量配置都列进来。
> 那样会让 MAP 随项目线性膨胀，违背"快速导航"的初衷。
> 全量信息天然在代码里；个别需要详细展开的主题，建子文件夹并在 `DIRS.md` 登记，
> MAP 里只留一行指针。

## 示例格式

```markdown
## Translation
- 后端入口: ai/api/services/translation_service.py
- 前端入口: web-lunwen/src/components/pdf/composables/useTranslation.js

## Annotations
- 后端入口: ai/api/routers/annotations.py
- 前端入口: web-lunwen/src/components/pdf/composables/useAnnotations.js
- 详细设计: <memory-docs>/detail_mem/feature/annotations.md
```

---

## `<概念 / 功能>`

- 入口：`<path>`
- 入口：`<path>`

## 规则

- 一个概念只挂 **1-2 个入口文件**，多了就说明该建子文件夹了。
- 文件改名 / 删除时同步更新本文件。
- 保持指针和映射，不写长篇解释。
