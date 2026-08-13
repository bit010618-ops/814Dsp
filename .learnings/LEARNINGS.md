# Learnings

## [LRN-20260813-001] correction

**Logged**: 2026-08-13T20:10:00+08:00
**Priority**: high
**Status**: resolved
**Area**: frontend

### Summary
Structural-diagram arrows must terminate on an explicit component port, not merely near the target.

### Details
Visual QA found two DTMF branch arrows ending in empty space just before the summing node. Geometry checks now require their endpoints to land on the two intended left-side input positions of the summer.

### Resolution
- Updated the DTMF branch paths to end at the summer boundary.
- Added targeted regression assertions in `full/tests/test_build_chapter_05_filter_structures_mathjax_component.py`.

### Metadata
- Source: user_feedback
- Related Files: full/tools/build_chapter_05_filter_structures_mathjax_component.py
- Tags: svg, structure-diagram, arrows, visual-qa

