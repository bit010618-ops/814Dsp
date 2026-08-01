# 第二章补充真题第五批

## Objective

逐字核对并纳入 2013 年计算题第 5 小题：双边序列的 z 变换。题干保持原样；详解使用完整 MathJax 公式，明确分项 ROC、总 ROC 与最终表达式。

## Scope

- 原卷：`华理814真题.pdf` 第 25 页。
- 仅修改本批组件、对应测试、第二章候选总装配及本任务记录。
- 不暂存候选 PDF、审题截图、临时目录或任何既有未提交文件。

## Status

Completed — 已在原卷第 25 页核对题干并纳入第二章候选讲义。

## Result

- 保留 2013 年计算题第 5 小题原题干：双边序列的 z 变换。
- 详解先分解右边序列与左边序列，分别给出几何级数、ROC，再取收敛域交集；不省略左边序列的变元替换步骤。

## Verification

- RED：组件不存在时，新测试以预期的 ImportError 失败。
- GREEN：`pytest --basetemp .test-tmp-ch2-batch5-green2 full/tests/test_build_chapter_02_mathjax_handout.py full/tests/test_build_chapter_02_supplemental_training_batch_five_mathjax_component.py -q`：5 passed。
- 将候选 PDF 第 45–46 页以 160 dpi 渲染并人工复核：题干、页眉页脚、MathJax 公式和 ROC 均清晰，无重叠、裁切或裸 LaTeX。
