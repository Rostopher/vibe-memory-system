---
layer: detail
update_mode: append
role: "历史归档 —— 已完成的记录、复盘、旧快照、失败探索"
read_when: "问历史问题、重建旧上下文、回顾旧方案时"
not_for: "当前状态（-> STATUS/PROGRESS），活跃会话上下文（-> SHORT_MEMORY/）"
---

# Archive

> 放**历史的、已完成的**内容：复盘、旧快照、失败探索、定稿前的方案记录。
>
> 这是 memory-docs 详细层的一个**已有协议的子文件夹实例**。
> 新建别的子文件夹时，参考这里的协议风格，并在 `DIRS.md` 登记。

## 规则

- 归档记录**忠于当时**，不事后改写。
- **先蒸馏，再归档**：仍有价值的结论先写进对应活跃 owner。
- 归档内容与活跃文档冲突时，**以活跃文档为准**。
- 不要把归档当作"当前状态"来用。
- 活跃 owner 应在历史细节仍有用时链接到 archive，archive manifest 也应指回 owner。

## 命名

- `YYYYMMDD_topic.md`
- `YYYYMMDD_retrospective.md`
- `YYYYMMDD_failed_experiment.md`

单篇记录可以继续平铺。若一次迁移保留多个来源文件，使用 topic bundle：

```text
archive/YYYYMMDD_topic/
├── README.md
└── <preserved-source-files>
```

bundle 的 `README.md` 或 `MANIFEST.md` 至少写明：

- `Archived`：归档日期；
- `Reason`：为什么离开活跃层；
- `Preserves`：保留了哪些来源；
- `Distilled into`：用有效的本地 Markdown 链接指向承接稳定结论的活跃 owner；
- `Retrieval keywords`：未来读者会自然搜索的主题词、旧称和别名，并写明什么情况下
  应重新阅读。

这些字段都必须有非空值；只写标签不算完成。标签可以使用等价中文。
`Distilled into` 不能只写文件名或路径文本，至少包含一个可解析且存在的本地
Markdown 链接。若稳定结论尚无活跃 owner，先建立 owner，再归档。

示例：

```markdown
- Archived: 2026-07-31
- Reason: confirmation closed the route
- Preserves: proposal.md, pilot-results.md
- Distilled into: [DEC-017](../../detail_mem/DECISIONS.md#dec-017)
- Retrieval keywords: adapter bank, router, oracle gap；重开路由方案时阅读
```
