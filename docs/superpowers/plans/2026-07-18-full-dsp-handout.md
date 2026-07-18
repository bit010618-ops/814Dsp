# Full DSP Handout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build the complete, editable and print-ready A4 Chinese 《数字信号处理讲义》 from the 1056-page MOOC PDF, with every unique source item in its original order, chapter-end 814 training, and complete end-of-book solutions.

**Architecture:** A source-audit layer records immutable source locations, PDF bookmarks, animation-increment candidates, figures and all exam-question records. A rendering layer converts structured chapter content into a ReportLab PDF with the approved typography and natural-flow pagination. A verification layer checks source coverage, formulas, figures, page references and rendered-page appearance before every chapter-stage commit.

**Tech Stack:** Python bundled runtime; pypdf/PDFium; ReportLab; matplotlib STIX math rendering; pytest; Git/GitHub.

---

## Source audit confirmed on 2026-07-18

| Chapter | Original PDF pages | Source bookmark scope |
| --- | ---: | --- |
| 第 1 章 离散时间信号与系统 | 1–185 | MC1-1-1 through MC1-5-1 |
| 第 2 章 z 变换与 LSI 系统频域分析 | 186–387 | MC2-1-1 through MC2-7-1 |
| 第 3 章 离散傅里叶变换 | 388–559 | MC3-1-1 through MC3-7-1 |
| 第 4 章 快速傅里叶变换 | 560–655 | MC4-1-1 through MC4-6-1 |
| 第 5 章 数字滤波器结构 | 656–741 | MC5-1-1 through MC5-4-1 |
| 第 6 章 IIR 数字滤波器设计 | 742–865 | MC6-1-1 through MC6-6-1 |
| 第 7 章 FIR 数字滤波器设计 | 866–1009 | MC7-1-1 through MC7-5-1 |
| 第 8 章 多采样率数字信号处理 | 1010–1056 | MC8-1-1 through MC8-4-1 |

Course scan result: 1056 pages, 18 incremental-animation candidates. The true-paper source has 205 pages and contains 2002–2007, 2013–2017 and 2019–2025; no question may be invented for absent years.

## File map

- sample/tools/scan_pdfs.py — generic bookmark/text/animation audit.
- sample/tests/test_scan_pdfs.py — scanner regression tests.
- full/source/chapters.json — chapter page ranges and section bookmarks.
- full/source/exam_questions.json — every relevant question, source year/page, chapter, role, answer id.
- full/source/figures.json — source page, caption, original/crop/redraw choice and verification.
- full/tools/extract_course.py — content extraction and containment-only animation merges.
- full/tools/classify_exams.py — reviewable question index; low confidence is never silently assigned.
- full/tools/math_render.py — one formula renderer: display 11 pt; inline 17.5 pt with 3 pt downshift.
- full/tools/layout.py — A4 typography, header/footer, natural-flow frame and pure-white questions.
- full/tools/build_handout.py — chapter batches and final two-pass page-reference build.
- full/tests/ — coverage, typography, formula, cross-reference and PDF-render tests.
- output/pdf/数字信号处理讲义.pdf — final artifact; full/ remains editable source.

### Task 1: Make source audit reproducible

**Files:**
- Modify: sample/tools/scan_pdfs.py
- Modify: sample/tests/test_scan_pdfs.py
- Create: full/source/chapters.json
- Create: full/docs/source-audit.md
- Create: full/artifacts/course_inventory.json
- Create: full/artifacts/exam_inventory.json

- [x] **Step 1: Write a failing bookmark-tree test.**

~~~python
def test_scan_pdf_records_top_level_bookmarks(tmp_path):
    report = scan_pdf(bookmarked_fixture(tmp_path))
    assert report["outline"][0]["title"] == "Chapter 1"
    assert report["outline"][0]["children"][0]["page"] == 2
~~~

- [x] **Step 2: Run it and observe the expected missing-outline failure.**

Run: python -m pytest sample/tests/test_scan_pdfs.py::test_scan_pdf_records_top_level_bookmarks -q
Expected: KeyError: outline.

- [x] **Step 3: Implement the minimal outline reader and rerun scanner tests.**

~~~python
def outline_tree(reader, entries=None):
    nodes = []
    for entry in (reader.outline if entries is None else entries):
        if isinstance(entry, list):
            nodes[-1]["children"] = outline_tree(reader, entry)
        else:
            nodes.append({"title": str(entry.get("/Title", "")),
                          "page": reader.get_destination_page_number(entry) + 1,
                          "children": []})
    return nodes
~~~

Run: python -m pytest sample/tests/test_scan_pdfs.py -q
Expected: 4 passed.

- [x] **Step 4: Store the two scan results and chapter manifest.**

Write the eight ranges above and all nested bookmarks to full/source/chapters.json and full/docs/source-audit.md. Preserve course page count 1056, all 18 candidate runs and the true-paper year availability.

- [ ] **Step 5: Commit/push only audit code, tests and compact manifests.**

~~~text
git add sample/tools/scan_pdfs.py sample/tests/test_scan_pdfs.py full/source full/docs full/artifacts
git commit -m "feat: audit DSP source and bookmarks"
git push origin main
~~~

### Task 2: Lock the global typesetting system

**Files:**
- Create: full/tools/math_render.py
- Create: full/tools/layout.py
- Create: full/source/style.json
- Create: full/tests/test_math_render.py
- Create: full/tests/test_layout.py

- [ ] **Step 1: Write a failing global-math test.**

~~~python
def test_global_math_style_matches_approved_print_spec():
    assert DISPLAY_FORMULA_SIZE == 11
    assert INLINE_MATH_DRAWN_HEIGHT == 17.5
    assert INLINE_MATH_BASELINE_OFFSET == -5.5
~~~

- [ ] **Step 2: Run the test before code exists.**

Run: python -m pytest full/tests/test_math_render.py -q
Expected: ModuleNotFoundError.

- [ ] **Step 3: Implement exactly one math style and one natural-flow frame.**

~~~python
DISPLAY_FORMULA_SIZE = 11
INLINE_MATH_DRAWN_HEIGHT = 17.5
INLINE_MATH_BASELINE_OFFSET = -5.5

def place(frame, block):
    if block.height <= frame.remaining_height:
        return frame.append(block)
    return frame.new_page().append(block)
~~~

The layout must use A4 portrait; header left 数字信号处理讲义; dynamic chapter header right; centered page number; pure-white question blocks; no page break at an original slide boundary.

- [ ] **Step 4: Write and run the natural-flow test.**

~~~python
def test_content_flow_uses_remaining_frame_before_new_page():
    frame = FlowFrame(height=420)
    assert frame.place(Block(height=200))
    assert frame.place(Block(height=190))
    assert frame.page_breaks == 0
~~~

Run: python -m pytest full/tests/test_math_render.py full/tests/test_layout.py -q
Expected: all pass.

- [ ] **Step 5: Render an A4 typography test page at 300 dpi, inspect formula glyphs and commit/push.**

Commit message: feat: add global DSP handout typography.

### Task 3: Extract ordered source content and safe figures

**Files:**
- Create: full/tools/extract_course.py
- Create: full/tools/figure_assets.py
- Create: full/tests/test_extract_course.py
- Create: full/tests/test_figure_assets.py
- Create: full/source/chapter_01.json through full/source/chapter_08.json
- Create: full/source/figures.json

- [x] **Step 1: Write containment-only tests.**

~~~python
def test_keep_only_final_slide_when_final_text_contains_prior_slide():
    pages = [{"page": 4, "text": "定义"}, {"page": 5, "text": "定义 公式 结论"}]
    assert collapse_incremental_pages(pages) == [pages[1]]

def test_keep_both_when_new_page_lacks_prior_unique_content():
    pages = [{"page": 4, "text": "定义 A"}, {"page": 5, "text": "例题 B"}]
    assert collapse_incremental_pages(pages) == pages
~~~

- [x] **Step 2: Run the tests before implementation.**

Run: python -m pytest full/tests/test_extract_course.py -q
Expected: import failure for collapse_incremental_pages.

- [x] **Step 3: Implement normalized exact containment only.**

~~~python
def collapse_incremental_pages(pages):
    kept = []
    for page in pages:
        if kept and normalize(kept[-1]["text"]) in normalize(page["text"]):
            kept[-1] = page
        else:
            kept.append(page)
    return kept
~~~

Record every dropped source page with its final containing page. A non-contained page stays even if it looks similar.

- [ ] **Step 4: Write safe-figure tests, then implement conservative handling.**

~~~python
def test_keep_original_when_crop_intersects_labeled_content():
    assert choose_figure_asset(source, crop, labeled_boxes=[omega_box]).mode == "original"
~~~

Use original if crop could lose any coordinate, unit, Ω, formula, curve or label. Redraw only when the original cannot print clearly; then reproduce all knowledge-bearing labels and curves.

- [ ] **Step 5: Extract all eight chapter manifests, render boundary source pages at 300 dpi, test and commit/push.**

Run: python -m pytest full/tests/test_extract_course.py full/tests/test_figure_assets.py -q
Expected: all pass.
Commit message: feat: extract ordered DSP chapter content.

### Task 4: Index all available relevant 814 questions

**Files:**
- Create: full/tools/classify_exams.py
- Create: full/tests/test_classify_exams.py
- Create: full/source/exam_questions.json
- Create: full/docs/exam-coverage.md

- [ ] **Step 1: Write explicit-topic and ambiguous-topic tests.**

~~~python
def test_classify_dft_prompt_to_chapter_three():
    record = classify_question(2015, 29, "序列 x(n) 的 N 点 DFT")
    assert record["chapter"] == 3 and record["confidence"] == 1.0

def test_ambiguous_prompt_requires_manual_review():
    assert classify_question(2025, 56, "DSP 题")["confidence"] < 1.0
~~~

- [ ] **Step 2: Run before classifier exists.**

Run: python -m pytest full/tests/test_classify_exams.py -q
Expected: import failure.

- [ ] **Step 3: Implement keyword assignment with mandatory review.**

~~~python
TOPICS = [
    (r"DFT|DFS|频谱分析|栅栏", 3, "DFT"),
    (r"FFT", 4, "FFT"),
    (r"FIR.*结构|IIR.*结构", 5, "滤波器结构"),
    (r"巴特沃斯|双线性|脉冲响应不变", 6, "IIR 设计"),
    (r"窗函数|等波纹|线性相位", 7, "FIR 设计"),
    (r"抽取|内插|采样率转换", 8, "多采样率"),
]
~~~

Every candidate stores year, source page(s), exact transcription/image, chapter, topic, confidence, selected/supplement role, scope status and answer id.

- [ ] **Step 4: Manually resolve every low-confidence candidate.**

For each chapter, select 2–3 representative high-frequency questions as 重点精练 with natural white writing area. Put every remaining relevant question under 补充真题 grouped by year. Do not invent questions for missing years. For a cross-chapter large question, record its split mode: split independent subquestions into their own chapters; keep linked subquestions as one complete question in the latest required chapter. Never leave an earlier chapter with a subquestion that relies on unavailable later knowledge.

- [ ] **Step 5: Test completeness, generate exam-coverage.md and commit/push.**

~~~python
def test_all_candidates_are_assigned_or_explicitly_out_of_scope(index):
    assert not [q for q in index if q["scope_status"] not in {"assigned", "out_of_scope"}]
~~~

Commit message: feat: index all available 814 DSP questions.

### Task 5: Render verified chapter batches

**Files:**
- Create: full/tools/build_handout.py
- Create: full/tests/test_build_handout.py
- Modify: full/source/chapter_01.json through full/source/chapter_08.json
- Modify: full/source/exam_questions.json
- Create: output/pdf/数字信号处理讲义_第1-2章.pdf
- Create: output/pdf/数字信号处理讲义_第3-4章.pdf
- Create: output/pdf/数字信号处理讲义_第5-6章.pdf
- Create: output/pdf/数字信号处理讲义_第7-8章.pdf

- [ ] **Step 1: Write failing coverage and question-style tests.**

~~~python
def test_chapter_build_reports_every_retained_source_page(tmp_path):
    report = build_chapters([1], tmp_path / "ch1.pdf")
    assert report["retained_source_pages"] == report["rendered_source_pages"]

def test_question_blocks_are_plain_white(page):
    assert page.question_style == "plain_white"
~~~

- [ ] **Step 2: Run before builder exists.**

Run: python -m pytest full/tests/test_build_handout.py -q
Expected: import failure.

- [ ] **Step 3: Implement a natural-flow ordered builder.**

~~~python
def build_chapters(chapters, output):
    story = []
    for chapter in chapters:
        story.append(chapter_opening(chapter))
        story.extend(render_ordered_blocks(chapter))
        story.extend(render_chapter_exam_section(chapter))
    return render_pdf(story, output)
~~~

Every chapter begins on a new page. Ordinary content fills available space; only chapter-end pages and question writing regions can be intentionally spacious. Source example solutions are expanded inline where insufficient, preserving all original steps.

- [ ] **Step 4: Complete, test, render and inspect Chapters 1–2; commit/push.**

Verify every retained source id, all Ch.1/2 assigned true questions, final-page header/footer, formula visibility and 300-dpi visual pages. Commit message: feat: render DSP handout chapters 1 and 2.

- [ ] **Step 5: Complete, test, render and inspect Chapters 3–4; commit/push.**

Include full DFT/FFT coverage. The 3.6 sampling figure remains original if any crop loses labels; caption is 图 3-1 采样参数与频域离散的对应关系. The sample 2004 question must be accompanied by every other audited related question. Commit message: feat: render DSP handout chapters 3 and 4.

- [ ] **Step 6: Complete, test, render and inspect Chapters 5–6; commit/push.**

Keep filter-structure and IIR-design diagrams print-clear; render all assigned question groups. Commit message: feat: render DSP handout chapters 5 and 6.

- [ ] **Step 7: Complete, test, render and inspect Chapters 7–8; commit/push.**

Keep FIR-design and multirate content in source order, with all assigned question groups. Commit message: feat: render DSP handout chapters 7 and 8.

### Task 6: Assemble final answers and final print artifact

**Files:**
- Modify: full/tools/build_handout.py
- Modify: full/tests/test_build_handout.py
- Create: full/source/answer_records.json
- Create: output/pdf/数字信号处理讲义.pdf
- Create: full/artifacts/final_build_report.json
- Create: full/docs/final-verification.md

- [ ] **Step 1: Write failing final-reference tests.**

~~~python
def test_every_question_reference_resolves_to_a_final_answer_page(report):
    assert all(ref.page and ref.page > 0 for ref in report.answer_references)

def test_all_assigned_questions_have_detailed_answers(report):
    assert report.assigned_exam_ids == report.detailed_answer_ids
~~~

- [ ] **Step 2: Run before final pagination exists.**

Run: python -m pytest full/tests/test_build_handout.py -q
Expected: unresolved page references.

- [ ] **Step 3: Implement a two-pass final build.**

~~~python
def build_final_book(output):
    draft = build_content_with_answer_tokens()
    answer_pages = render_and_collect_answer_pages(draft)
    return render_content_with_final_page_references(draft, answer_pages, output)
~~~

The final order is TOC, Chapters 1–8 with chapter-end training, then 真题整理详解. Every answer is detailed, uses rendered math and vertical fractions, and links back to the question.

- [ ] **Step 4: Run mechanical and visual checks, then commit/push.**

Run: python -m pytest full/tests -q
Expected: all pass. Render every final PDF page at 300 dpi; inspect a representative page for each section and every flagged formula/figure/question page. Require source coverage 1.0 for all chapters, resolved answer references, full question-answer matching and no non-exempt large whitespace.

Commit message: feat: complete printable DSP handout.

## Plan self-review

- Source fidelity: Tasks 1 and 3, strict containment-only merging and retained-source reporting.
- Formula, image, print and natural-flow requirements: Tasks 2, 3, 5 and 6.
- All relevant true questions: Task 4 plus every chapter-batch acceptance check; no missing-source claim before audit.
- TDD: every production feature has a failing test before implementation.
- Persistence: every verified audit/chapter/final milestone has a task-only commit and push.
