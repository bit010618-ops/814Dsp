# 全书训练与书末详解装配基础 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在八章正文之后接入现有第 1--3 章强化训练，全部详解集中到书末，并为最终页码回填提供单一入口。

**Architecture:** 新建 `build_full_handout.py`，复用正文装配器的八章正文，同时从已有训练组件中提取训练段和答案段。它统一替换旧组件的固定答案页码为占位符；以后第 4--8 章只需追加组件注册，不触碰正文装配器。

**Tech Stack:** Python、MathJax、pytest、Chromium PDF 导出器、ReportLab/PyPDF。

---

### Task 1: 建立全书装配入口

**Files:**

- Create: `full/tools/build_full_handout.py`
- Create: `full/tests/test_build_full_handout.py`

- [ ] Step 1 — 在测试文件中先写 `test_full_handout_orders_body_training_then_answers`：调用 `write_html`，断言“第八章 多速率数字信号处理”在“第一章 分章强化训练”之前，且“第三章 分章强化训练”在第一次“真题整理详解”之前。
- [ ] Step 2 — 运行 `& $py -m pytest -p no:cacheprovider full/tests/test_build_full_handout.py`，预期因不存在 `build_full_handout` 而失败。
- [ ] Step 3 — 实现最小的 `write_html(output: Path) -> Path`：用 `build_all_main_body.write_html` 生成正文，再在临时目录调用第 1、2、3 章已有组件，提取其 `<main>` 内容，按“正文、训练、答案”顺序写入一个新的 MathJax HTML 文档。
- [ ] Step 4 — 重新运行同一测试，预期 `1 passed`。
- [ ] Step 5 — 仅提交 `full/tools/build_full_handout.py` 与 `full/tests/test_build_full_handout.py`，提交信息为 `Add full handout assembly foundation`。

### Task 2: 清除旧的固定页码

**Files:**

- Modify: `full/tools/build_full_handout.py`
- Modify: `full/tests/test_build_full_handout.py`

- [ ] Step 1 — 先写 `test_full_handout_uses_only_pending_page_references`：断言输出包含“详解见 P.____”，且不包含“详解见 P.59”或“详解见 P.18”。
- [ ] Step 2 — 运行该测试，预期因旧组件写死页码而失败。
- [ ] Step 3 — 只在总装配器实现 `_normalize_answer_refs(fragment: str) -> str`，用正则把 `详解见 P.` 后的数字或下划线替换为 `详解见 P.____`；不得改动题干文字或逐个编辑旧组件。
- [ ] Step 4 — 运行全文件测试，预期 `2 passed`。
- [ ] Step 5 — 仅提交本任务两文件，提交信息为 `Prepare training references for final pagination`。

### Task 3: 导出候选稿并视觉验收

**Files:**

- Modify: `full/tools/build_full_handout.py`
- Modify: `full/tests/test_build_full_handout.py`

- [ ] Step 1 — 先写测试，断言全书输出至少包含三个 `exam-page`，且最后一个训练标题在书末详解之前。
- [ ] Step 2 — 运行测试并确认因共享训练样式缺失或答案没有独立书末区段而失败。
- [ ] Step 3 — 在总装配器的全局 CSS 中增加 `.exam-page{break-before:page;min-height:230mm}` 与 `.answer-section{break-before:page}`；不得向普通正文插入空白占位块。
- [ ] Step 4 — 运行全文件测试，并运行 `build_full_handout.py` 与本地 MathJax PDF 导出器；要求 `unrendered=[]` 且 `pageErrors=[]`。
- [ ] Step 5 — 用 180 dpi 渲染最终正文页、第一张训练页、第一张和最后一张详解页；检查训练只在第八章之后、详解连续位于书末、无公式源码、裁切、重叠或正文大留白。仅提交相关装配器与测试。

## Review

- 计划不改变原题题干、八章正文顺序或普通正文分页。
- 准确的印刷页码明确延后到最终全书分页，不允许旧固定页码进入成品。
- 第 4--8 章训练在其题干与详解逐题迁移前不伪造为已完成。
