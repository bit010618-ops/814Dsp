# 正文整书页眉页码

## Objective

为八章连续 A4 正文增加独立的 PDF 页眉页码层：左上固定“数字信号处理讲义”，右上为当前章节名，页脚仅保留真实页码；页眉页码不得压住正文，并须随重排后的实际章节分页自动变化。

## Evidence

- `tmp/dsp-main-body-arrow-port-v13.pdf` 的正文无统一页眉和页码，未满足既定打印规范。
- 仓库已有 Chapter 2 的安全叠加实现：先完成 Chromium 正文分页，再用 ReportLab / PyPDF 在页边距处叠加页眉和页码，避免浏览器固定定位压住正文。

## Next

已完成并进入后续正文审计：通用叠加器以浏览器实际分页后的页面文本识别当前章节，逐页叠加页眉、章节名与页码；不依赖固定页码表。

## Result

- 新增 `full/tools/stamp_main_body_pdf.py`，在正文排版完成后写入页眉页码层。
- 新增 `full/tests/test_stamp_main_body_pdf.py`，锁定跨章节页的章节延续规则。
- `tmp/dsp-main-body-arrow-port-v13-stamped.pdf` 共 90 页；抽查第 1、31、44、76、90 页，页眉、章节名、页码清晰且不与正文重叠。
