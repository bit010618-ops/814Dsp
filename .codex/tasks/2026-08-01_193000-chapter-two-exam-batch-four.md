# 第二章补充真题第四批

## Objective

核对并纳入题库归属第二章、尚未收录的 2013 年第五题与第八题；题干逐字保留，详解使用统一 MathJax 公式，必要结构图或零极点图按教材规范矢量重绘。

## Scope

- 原卷：`华理814真题.pdf` 第 26–27 页。
- 仅修改本批组件、对应测试、第二章候选总装配和本任务记录。
- 不暂存候选 PDF、预览图片、临时目录或既有未提交文件。

## Status

Completed — 原卷第 26–27 页已核对；2013 年第五题与第八题已纳入第二章候选讲义。第五题的两条反馈支路分别由求和器下方与左下侧独立进入，禁止与 `x[n]` 主输入共线或在求和器下方形成方向不明的折返箭头。

## Result

- 2013 年第五题题干逐字保留；重绘为无水印的两延时反馈结构图，并给出因果解与稳定、非因果解。
- 2013 年第八题题干逐字保留；重绘为标准零极点图，并给出 ROC、稳定性、单位脉冲响应和差分方程。
- 将正文与页眉页脚封装为相互隔离的 PDF Form 图层，修复部分页面正文图形状态遮挡页眉的问题。

## Verification

- `pytest --basetemp .test-tmp-ch2-form-group-green full/tests/test_build_chapter_02_mathjax_handout.py full/tests/test_build_chapter_02_supplemental_training_batch_four_mathjax_component.py -q`：4 passed。
- 以 160 dpi 渲染候选 PDF 第 41–44 页并逐页复核：加法器反馈箭头、零极点图、MathJax 公式、页眉页脚均清晰，无重叠或裁切。
