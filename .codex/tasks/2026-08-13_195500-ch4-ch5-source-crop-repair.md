# Chapter 4–5 source-figure crop repair

## Objective

Audit course-slide figure crops in chapters four and five. A crop must retain the complete technical drawing while excluding slide-only decorations; if that cannot be done safely, replace the figure with a clean programmatic diagram.

## Completed

- Replaced the unsafe IIR second-order cascade slide crop with a complete formal SVG: aligned second-order sections, left-to-right flow, explicit input/output, and unambiguous arrows.
- Tightened the DIT FFT butterfly crop to remove the residual bottom slide banner without cutting its nodes, paths, twiddle factors, inputs, or outputs.
- Confirmed that the affected chapter-five page has no source header, watermark, cut technical drawing, or overlap.

## Verification

- `pytest -q full/tests/test_build_chapter_05_filter_structures_mathjax_component.py full/tests/test_crop_source_figures.py` → `6 passed`.
- Rebuilt `tmp/dsp-main-body-crop-qa-v2.pdf`; MathJax reported `unrendered=[]` and `pageErrors=[]`.
- Rendered the affected A4 pages and visually checked the repaired IIR cascade page.

## Rule carried forward

Never keep iterating a risky crop. If removing slide chrome would cut formulas, arrows, labels, or structure, use a clean vector redraw instead.

## Next action

Continue page-by-page audit of remaining source-derived figures in the main body before returning to the frozen training and appendix sections.
