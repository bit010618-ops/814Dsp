# Active task

- 完成《数字信号处理讲义》全文的可编辑 A4 教材式重制，并纳入经审计的华理 814 训练与书末详解。

# Current stage

- 八章讲义正文已完成源页覆盖与 A4 视觉核验，现转入全书真题训练、书末详解、最终页码回填与附录阶段。训练题面保持单题页、纯白题面和可书写空间；书末集中输出完整详解。

# Next action

- 按 `full/source/exam_training_manifest.json` 补齐尚缺的 21 道真题训练与详解，继续优先第 3 章余下 6 道；所有题干按原卷保留，跨章节题按依赖规则放置，最终统一回填“详解见 P.××”。

# Allowed paths

- 八章讲义正文转写、公式、图形、自然续排及 A4 视觉验收，以及真题训练、详解、页码回填和附录所必需的 `full/source/`、`full/tools/`、`full/tests/`、`full/outputs/` 中的精确相关文件。
- 当前任务记录、需求变更记录及阶段验收文档；先确认文件相关性再修改。

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

- 尚缺 21 道训练/详解、真题图重绘、全书分页、答案索引回填和附录尚未完成；当前机器的 Edge/Chromium headless GPU 缓存故障暂时阻断新的 PDF 视觉验收。
- 工作区有既有未提交组件与诊断文件，提交前必须逐项隔离。

# Detailed task source

- `.codex/tasks/2026-07-18_184000-full-dsp-handout.md`

# Status

- In progress — 继续补齐分章训练与书末详解。
