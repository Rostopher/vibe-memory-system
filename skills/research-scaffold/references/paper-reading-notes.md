# Paper Reading Notes

文献阅读笔记不应从强模板开始。第一目标是帮助研究者恢复当时读论文的判断、疑问、灵感和可用证据。

## 轻量结构

```markdown
# YYYY-Short-Title-Author

## 读完后的直觉

## 这篇论文在问什么

## 它怎么做

## 它发现什么

## 对本项目有什么用

## 我不完全相信哪里

## 可引用的位置

## 后续动作
```

## 拆解问题

读文献时优先回答这些问题，而不是逐段摘要：

- 这篇文章的研究问题是什么？
- 它的核心 claim 是什么？
- 它的数据、样本、benchmark 或实验对象是什么？
- 它的变量、指标、taxonomy 或评分口径如何定义？
- 关键数字是怎么计算出来的？
- 它解决的是 measurement、method、theory、data 还是 positioning 问题？
- 它对当前项目是支持、反驳、补充方法、提供数据，还是只是 related work？
- 它的主要漏洞是什么？
- 哪些段落、表格、公式、图可以进入论文？

## 写法原则

- 用自己的话解释，不把 abstract 或 introduction 改写一遍。
- 保留个人判断：哪里有启发，哪里不可信，哪里需要复核。
- 明确区分论文作者的 claim 和自己的 inference。
- 对重要结果说明计算口径：分子、分母、样本、权重、单位。
- 不把 OCR 原文或长摘录放进 note；原材料留在 `papers/`。

## 文件位置

推荐路径：

```text
notes/paper-reading/YYYY-short-title-author.md
```

如果一篇论文已经成为正式论文章节的一部分，再把相关文字迁移或改写到 `manuscripts/`，不要让 `notes/` 承担正式写作职责。

