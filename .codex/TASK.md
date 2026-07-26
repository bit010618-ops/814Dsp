# Active task

- 完成《数字信号处理讲义》全文的可编辑 A4 教材式重制，并纳入经审计的华理 814 训练与书末详解。

# Current stage

- 第一章正文、自然续排和三道重点真题训练已生成并验收：`full/outputs/chapter_01_handout.pdf` 为 62 页 A4 成品；`chapter_01_answers_component.pdf` 为对应书末详解组件。补充真题、全书书末详解汇编和最终页码回填尚未完成，因此第一章仍不能被误报为最终全章交付。

# Next action

- 从已审核题库逐题补入第一章“补充真题”，同时保持重点训练、详解组件和最终全书页码回填机制可重建；每一批题目均先完成题干、图形及详解的可读性验收，再接入章节自然续排。

# Allowed paths

- 第一章训练、补充真题、详解及自然续排所必需的 `full/source/`、`full/tools/`、`full/tests/`、`full/outputs/` 中的精确相关文件。
- 当前任务记录、需求变更记录及本章验收文档；先确认文件相关性再修改。

# Read only when needed

- 主课件、真题 PDF、参考稿、`sample/`、`legacy_full/`、全书其余章节模型和历史 HANDOFF 归档。

# Forbidden changes

- 不得改动原课件或真题源文件，不得用历史 119 页基线替代当前 8 章／1056 页交付。
- 不得删除未提交内容、把诊断产物混入提交，或机械合并动画／截去图内有效信息。

# Acceptance criteria

- 原顺序和唯一信息完整；公式、图形、训练与真题规则均满足详细需求。
- 实际 PDF 以适当分辨率渲染复核，无缺字、公式代码、裁切、重叠、水印或非题目页大面积留白。
- 每个已验证阶段仅提交相关文件并推送当前分支。

# Current risks

- 真题图重绘、全书分页、答案索引回填和第一章整体覆盖验收尚未完成。
- 工作区有既有未提交组件与诊断文件，提交前必须逐项隔离。

# Detailed task source

- `.codex/tasks/2026-07-18_184000-full-dsp-handout.md`

# Status

- In progress — 文档上下文迁移完成后继续第一章正文整合。
