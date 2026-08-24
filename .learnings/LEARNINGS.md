# Learnings

## [LRN-20260824-001] correction

**Logged**: 2026-08-24T00:00:00+08:00
**Priority**: high
**Status**: promoted
**Area**: docs

### Summary
真题必须按章节紧接正文排入，书末仅保留附录 F 的完整详解，分区标题和页眉页脚必须一致。

### Details
不能把题面集中到全书末尾，也不能残留“真题整理讲解序”等未确认的总真题区标题。章节真题区须为“第 X 章真题整理”，书末答案区须为“附录 F：真题整理详解”，页脚仅显示连续页码。

### Resolution
- 已提升为 `.codex/CONTEXT.md` 的永久产品约束。

### Metadata
- Source: user_feedback
- Related Files: .codex/CONTEXT.md
- Tags: true-exams, sectioning, headers, footers

---

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
