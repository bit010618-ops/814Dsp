# 第五章训练恢复 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 2020 年 IIR 级联型与并联型结构简答题加入第五章训练及书末详解。

**Architecture:** 新建一个只负责第五章训练和答案 HTML 的 MathJax 组件。全书装配器以与第 1--4 章相同的入口顺序追加该组件，训练和答案引用保持 `P.____`，等待全书完成后统一回填。

**Tech Stack:** Python、pytest、HTML/CSS、MathJax、Chromium PDF 导出、Poppler 页图检查。

---

### Task 1: 第五章训练组件

**Files:**

- Create: `full/tools/build_chapter_05_training_mathjax_component.py`
- Create: `full/tests/test_build_chapter_05_training_mathjax_component.py`

- [x] **Step 1: Write the failing test**

```python
def test_2020_iir_structure_question_is_kept_with_a_book_end_answer(tmp_path):
    from full.tools import build_chapter_05_training_mathjax_component as component
    question = component.write_training_html(tmp_path / "chapter-05-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-05-answers.html").read_text(encoding="utf-8")
    assert "2020 年真题" in question
    assert "2.IIR 滤波器的级联型和并联型结构特点；" in question
    assert "详解见 P.____" in question
    assert "因式分解" in answer
    assert "部分分式展开" in answer
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest full/tests/test_build_chapter_05_training_mathjax_component.py -p no:cacheprovider`

Expected: `ModuleNotFoundError` because the component does not exist.

- [x] **Step 3: Write minimal implementation**

```python
def write_training_html(output: Path) -> Path: ...
def write_answers_html(output: Path) -> Path: ...
```

The training page uses one `exam-page`; the answer uses a single `真题整理详解` section and explains serial factor sections versus parallel partial-fraction branches.

- [x] **Step 4: Run component test to verify it passes**

Run: `python -m pytest full/tests/test_build_chapter_05_training_mathjax_component.py -p no:cacheprovider`

Expected: `1 passed`.

### Task 2: 全书接入与视觉检查

**Files:**

- Modify: `full/tools/build_full_handout.py`
- Modify: `full/tests/test_build_full_handout.py`

- [x] **Step 1: Write the failing assembly assertion**

```python
assert "第五章 分章强化训练" in html
assert "IIR 滤波器的级联型和并联型结构特点" in html
```

- [x] **Step 2: Run it to verify it fails**

Run: `python -m pytest full/tests/test_build_full_handout.py -p no:cacheprovider`

Expected: assertion failure because Chapter 5 has not been appended.

- [x] **Step 3: Add Chapter 5 writer to training and answer fragment lists**

```python
from full.tools import build_chapter_05_training_mathjax_component as chapter_five_training
```

Append `write_training_html` after Chapter 4 and `write_answers_html` after Chapter 4 answers.

- [x] **Step 4: Run regression and export**

Run: `python -m pytest full/tests/test_build_chapter_05_training_mathjax_component.py full/tests/test_build_full_handout.py -p no:cacheprovider`

Expected: all tests pass. Export the assembled HTML with local MathJax and render the Chapter 5 training/answer pages at 160 dpi.

- [x] **Step 5: Commit**

```bash
git add .codex/progress.md .codex/tasks/2026-08-21_151000-chapter-five-training-recovery.md docs/superpowers/specs/2026-08-21-chapter-five-training-design.md docs/superpowers/plans/2026-08-21-chapter-five-training.md full/tools/build_chapter_05_training_mathjax_component.py full/tests/test_build_chapter_05_training_mathjax_component.py full/tools/build_full_handout.py full/tests/test_build_full_handout.py
git commit -m "Add chapter five structure training"
```
