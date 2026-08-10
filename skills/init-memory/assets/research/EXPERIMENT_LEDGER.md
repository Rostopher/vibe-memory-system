---
layer: detail
update_mode: append
role: "科研证据账本 —— 实验协议、可比性边界、产物、结果、解释和 claim boundary"
read_when: "复核实验依据、比较结果、写论文 claim 或判断某条证据是否有效时"
not_for: "当前 TODO / 下一步（-> STATUS），模块进度（-> PROGRESS），实时服务器状态，原始日志"
---

# Experiment Ledger

> 本文件是科研项目的可选详细 owner。它记录可复核证据，不承担当前项目状态。
> 失败、无效和负结果同样保留；需要纠正历史时，追加 superseding entry。

## 使用规则

- 每个实验使用稳定 ID。
- 记录足以判断可比性的协议字段，不复制全部配置。
- artifact 使用仓库相对路径、稳定 URI 或明确的外部位置。
- 分开写 observation、interpretation 和 claim boundary。
- 当前下一步只链接到 `STATUS.md`，不在本账本维护第二份 TODO。

## Entry Template

### EXP-<ID>: <title> (<YYYY-MM-DD>)

- Status: planned | running | complete | invalid | superseded
- Question / hypothesis:
- Code revision:
- Protocol:
  - data / split:
  - model / method:
  - seed / repetitions:
  - evaluator / metric:
  - comparability constraints:
- Artifacts:
- Results:
- Interpretation:
- Uncertainty / failure modes:
- Claim boundary:
- Related / supersedes:
