# 第二章 2013、2015 同题零极点训练归并

## 目标

将最终第二章讲义中重复出现的零极点训练题归并为一个分章强化训练条目，标明其同时为 2013 年第八题与 2015 年第七题，并保留完整题干、图和详解。

## 已核对的结构

- `build_chapter_02_training_mathjax_component.py`：分章强化训练中的 2015 年第七题，含完整题干、零极点图与详解。
- `build_chapter_02_supplemental_training_batch_fourteen_mathjax_component.py`：同一题的重复补充入口。
- 原卷中另有相同的 2013 年第八题。

## 验收

- 最终第二章 HTML 中该题题干仅出现一次。
- 保留两个年份及对应题号，题干、图形、详解完整。
- 相关回归、候选 PDF 和视觉检查通过。

## 审计结果与待授权事项

- 最终装配中确有两个相同题干：分章强化训练入口与补充真题 batch-fourteen 入口。
- 直接从最终装配移除 batch-fourteen 会撤掉一个既有训练/详解入口；自动化保护已拒绝该删除操作。
- 需要用户明确授权以下精确变更后才能继续：从 `build_chapter_02_mathjax_handout.py` 的最终装配中移除 `supplemental_training_batch_fourteen`，保留分章强化训练中的完整题干、图形与详解，并将其年份标签改为“2013 年第八题／2015 年第七题”。
