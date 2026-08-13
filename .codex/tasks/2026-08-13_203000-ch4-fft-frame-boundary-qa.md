# Chapter 4 FFT figure frame-boundary QA

## Objective

Remove remaining course-slide borders from the retained DIT and DIF FFT flow diagrams while preserving every technical path, node, label, and I/O marker.

## Completed

- Replaced the two coarse crop boxes with tighter image-specific boundaries.
- Removed green outer slide frames and residual slide-only space.
- Retained all eight input/output labels, butterfly paths, node dots, and twiddle-factor labels.

## Verification

- `pytest -q full/tests/test_build_all_main_body.py full/tests/test_build_chapter_05_filter_structures_mathjax_component.py full/tests/test_crop_source_figures.py` → `4 passed`.
- Direct image visual inspection confirms complete technical drawings with no remaining slide title strip, school mark, footer, or colored outer frame.

## Next action

Continue the main-body page-by-page visual audit and replace any remaining unsafe source crop with a complete vector diagram.
