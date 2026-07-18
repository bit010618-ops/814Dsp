# MOOC DSP A4 讲义代表性样稿 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成并通过视觉验收的 5–10 页 MOOC 数字信号处理 A4 讲义代表性样稿。

**Architecture:** `scan_pdfs.py` 只读扫描两份 PDF，输出页数、书签、文本密度、连续动画候选组与代表页清单；`build_sample.py` 从经确认的内容映射生成可修改的 ReportLab PDF；`verify_sample.py` 检查页数、页面尺寸和页眉页脚，再通过 300 dpi 渲染进行人工视觉验收。

**Tech Stack:** Python 3、pypdf、pdfplumber、ReportLab、Poppler（pdfinfo/pdftoppm）、pytest。

---

### Task 1: 扫描两份源 PDF 并选出候选样稿段

**Files:**
- Create: `tools/scan_pdfs.py`
- Create: `artifacts/source_inventory.json`
- Create: `artifacts/sample_candidates.md`
- Test: `tests/test_scan_pdfs.py`

- [ ] **Step 1: 写入读取页数、页面尺寸和前 20 页文本摘要的失败测试**

```python
def test_scan_pdf_reports_page_count_and_text(tmp_path):
    report = scan_pdf(Path("fixture.pdf"), max_pages=2)
    assert report["page_count"] == 2
    assert report["pages"][0]["text_chars"] > 0
```

- [ ] **Step 2: 运行测试，确认扫描器在实现前失败**

Run: `pytest tests/test_scan_pdfs.py::test_scan_pdf_reports_page_count_and_text -v`

Expected: FAIL，因为尚未定义 `scan_pdf`。

- [ ] **Step 3: 实现只读 PDF 扫描器**

```python
def scan_pdf(path: Path, max_pages: int | None = None) -> dict:
    reader = PdfReader(str(path))
    limit = len(reader.pages) if max_pages is None else min(max_pages, len(reader.pages))
    pages = []
    for index in range(limit):
        text = reader.pages[index].extract_text() or ""
        pages.append({"index": index + 1, "text_chars": len(text), "text": text[:1200]})
    return {"path": str(path), "page_count": len(reader.pages), "pages": pages}
```

- [ ] **Step 4: 运行测试并生成真实材料清单**

Run: `pytest tests/test_scan_pdfs.py -v; python tools/scan_pdfs.py --course "C:\\Users\\HP\\Desktop\\MOOC课件-合并版.pdf" --exams "C:\\Users\\HP\\Desktop\\讲义、做题本\\华理814真题.pdf" --output artifacts/source_inventory.json`

Expected: PASS；生成包含课件和真题页数、书签、页文本摘要和候选连续页组的 JSON。

- [ ] **Step 5: 写出候选样稿段理由**

Run: `python tools/scan_pdfs.py --write-candidates artifacts/sample_candidates.md`

Expected: 输出 2–3 个候选段，各自说明公式、图形、例题和动画递进证据页。

### Task 2: 固化样稿视觉规范和来源映射

**Files:**
- Create: `artifacts/sample_spec.json`
- Create: `artifacts/source_mapping.md`
- Test: `tests/test_sample_spec.py`

- [ ] **Step 1: 写入验证 A4 页面、固定层级字号和页眉页脚字段的失败测试**

```python
def test_sample_spec_has_printable_a4_and_fixed_type_scale():
    spec = json.loads(Path("artifacts/sample_spec.json").read_text(encoding="utf-8"))
    assert spec["page_size"] == "A4"
    assert spec["orientation"] == "portrait"
    assert spec["type_scale"]["body"] == spec["type_scale"]["body"]
    assert spec["header_left"] == "数字信号处理讲义"
```

- [ ] **Step 2: 运行测试，确认视觉规范尚未创建**

Run: `pytest tests/test_sample_spec.py::test_sample_spec_has_printable_a4_and_fixed_type_scale -v`

Expected: FAIL，因为 `sample_spec.json` 不存在。

- [ ] **Step 3: 创建视觉规范和逐页来源映射**

```json
{
  "page_size": "A4",
  "orientation": "portrait",
  "header_left": "数字信号处理讲义",
  "type_scale": {"chapter": 18, "section": 14, "body": 10.5, "formula": 11, "caption": 9},
  "palette": {"ink": "#1F2933", "chapter": "#123B5D", "accent": "#9D2B2B"}
}
```

- [ ] **Step 4: 运行规范测试并人工复核候选段**

Run: `pytest tests/test_sample_spec.py -v`

Expected: PASS；`source_mapping.md` 为每页写明课件页范围、是否为动画合并和真题来源。

### Task 3: 生成可修改的 A4 样稿 PDF

**Files:**
- Create: `tools/build_sample.py`
- Create: `artifacts/sample_content.json`
- Create: `outputs/mooc-dsp-handout-sample/数字信号处理讲义_样稿.pdf`
- Test: `tests/test_build_sample.py`

- [ ] **Step 1: 写入验证 PDF 页数、A4 页面尺寸和页码文本的失败测试**

```python
def test_generated_sample_is_a4_and_has_pages(tmp_path):
    output = build_sample(Path("artifacts/sample_content.json"), tmp_path / "sample.pdf")
    reader = PdfReader(str(output))
    assert 5 <= len(reader.pages) <= 10
    assert round(float(reader.pages[0].mediabox.width)) == 595
    assert "1" in (reader.pages[0].extract_text() or "")
```

- [ ] **Step 2: 运行测试，确认构建器尚未实现**

Run: `pytest tests/test_build_sample.py::test_generated_sample_is_a4_and_has_pages -v`

Expected: FAIL，因为 `build_sample` 不存在。

- [ ] **Step 3: 以 ReportLab 实现样稿构建器**

```python
canvas.setPageSize(A4)
canvas.setFont("NotoSerifCJKsc-Regular", 10.5)
draw_header(canvas, "数字信号处理讲义", chapter_name)
draw_footer(canvas, str(page_number))
```

构建器必须接受正文、显示公式、图片/重绘图、例题和训练页数据；同类元素复用固定样式，不得按页随意缩小字号。

- [ ] **Step 4: 运行构建测试并生成候选 PDF**

Run: `pytest tests/test_build_sample.py -v; python tools/build_sample.py --content artifacts/sample_content.json --output outputs/mooc-dsp-handout-sample/数字信号处理讲义_样稿.pdf`

Expected: PASS；生成 5–10 页 A4 PDF 和可再次构建的源数据。

### Task 4: 300 dpi 渲染、自动检查和视觉复验

**Files:**
- Create: `tools/verify_sample.py`
- Create: `artifacts/verification_report.md`
- Create: `renders/sample-01.png` through `renders/sample-10.png`
- Test: `tests/test_verify_sample.py`

- [ ] **Step 1: 写入检查样稿页数、A4 尺寸和页眉文本的失败测试**

```python
def test_verify_sample_reports_page_count_and_header(tmp_path):
    report = verify_pdf(Path("sample.pdf"))
    assert report["a4_portrait"] is True
    assert report["header_missing_pages"] == []
```

- [ ] **Step 2: 运行测试，确认验证器尚未实现**

Run: `pytest tests/test_verify_sample.py::test_verify_sample_reports_page_count_and_header -v`

Expected: FAIL，因为 `verify_pdf` 不存在。

- [ ] **Step 3: 实现 PDF 验证器并在 300 dpi 渲染样稿**

```python
assert 590 <= width <= 600 and 840 <= height <= 850
assert "数字信号处理讲义" in page_text
subprocess.run([pdftoppm, "-r", "300", "-png", str(pdf), str(render_prefix)], check=True)
```

- [ ] **Step 4: 运行自动验证、逐页查看 PNG，并写入验收报告**

Run: `pytest tests/test_verify_sample.py -v; python tools/verify_sample.py --pdf outputs/mooc-dsp-handout-sample/数字信号处理讲义_样稿.pdf --render-dir renders --report artifacts/verification_report.md`

Expected: PASS；报告记录页数、尺寸、页眉页脚、来源映射和人工视觉检查结论。

### Task 5: 记录、提交和样稿评审

**Files:**
- Modify: `task_plan.md`
- Modify: `findings.md`
- Modify: `progress.md`
- Create: `artifacts/sample_review_notes.md`

- [ ] **Step 1: 更新三份恢复文件，记录真实样稿文件、测试结果、视觉缺陷和下一步**

- [ ] **Step 2: 只暂存样稿相关的源文件、映射、测试与恢复记录**

Run: `git add work/mooc-dsp-handout-sample outputs/mooc-dsp-handout-sample`

Expected: 暂存区不包含任何用户无关文件。

- [ ] **Step 3: 提交并推送样稿里程碑**

Run: `git commit -m "Create MOOC DSP handout sample"; git push origin main`

Expected: 本地和远端均包含可恢复的样稿版本。

