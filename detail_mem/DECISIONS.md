---
layer: detail
update_mode: append
line_budget: 200
role: "决策注册表与档案 —— 当前结论、生命周期，以及为什么选 A 不选 B"
read_when: "做设计选择、回看旧决策、想理解某东西为什么是这样时"
not_for: "操作规则（-> CONVENTIONS），未定论的讨论（-> SHORT_MEMORY/），演变叙事（-> HISTORY）"
---

# Decisions

> 用紧凑 registry 快速找到当前结论，再按需读取详细理由或 archive。
>
> - `DECISIONS.md` 是**决策查找表**：registry 回答当前结论和生命周期，
>   detail 保留来由和取舍。
> - `HISTORY.md` 是**叙事线**：把多条决策串成项目演变的故事。两者互补。

## Registry

| ID | Status | Topic | Current conclusion | Keywords | Detail |
|---|---|---|---|---|---|
| `DEC-001` | `governing` | `<主题>` | `<一句话当前结论>` | `<自然检索词、旧称、别名>` | [details](#dec-001) |

Status 使用：

- `active`：稳定选择正在执行或验证，尚未形成长期默认；
- `governing`：当前规则、默认或设计边界；
- `closed`：路线已明确停止；
- `superseded`：已由另一 ID 替代；
- `historical`：只为解释历史保留，不再约束当前工作。

`Current conclusion` 必须能脱离详细记录独立理解，`Keywords` 使用未来读者会自然搜索的词。

## 更新契约

为兼容既有工具，frontmatter 仍为 `update_mode: append`。文件内部采用以下混合契约：

- **Registry 可 patch**：状态、当前结论、关键词和 detail 指针应随生命周期更新；
  不删除旧 ID，也不把旧 ID 分配给新含义。
- **Detail 正常 append**：新增决策追加独立记录；已有 rationale 不静默改写。
  被替代时追加新决策或带日期的 closure note，并从 registry 互相链接。
- **受控 rollover**：接近 `line_budget` 时，可在先更新 registry 后，把
  `closed` / `superseded` 的完整 rationale 移入 archive；registry 行和可用 detail
  指针必须保留。

ID 一经发布永不复用。迁入旧账若与本项目 ID 冲突，使用稳定 namespace，例如
`legacy-2024-06/DEC-001`，不要让同一个裸 ID 指向两个决定。

计划默认只是 proposal，不能据此断言当前状态。计划完成、停止或被替代时，必须留下
明确的 `closure` / `superseded` 指针，连接计划、registry 当前行以及确认它的
代码、产物、实验记录或 archive manifest。

## Details

### DEC-001

- 标题：`<标题>`
- 日期：`<YYYY-MM-DD>`
- 状态：`governing`
- 背景：
- 决策：
- 理由：
- 影响：
- 证据 / 验证：
- 生命周期：`<proposal / pilot / confirmation / closure / superseded 链接>`
- 演变关联：见 `<memory-docs>/HISTORY.md`

不要把仍在讨论、只有 proposal 或只有未确认 pilot 的内容写成 governing 决策。
