# 整书第八章 SVG 样式装配修复

## Objective

修复第八章多采样率 SVG 在独立组件正常、装配进整本讲义 PDF 后却出现黑色填充块的问题；将整书装配样式纳入回归检查，并以实际 A4 导出验证。

## Completed

- 定位为整书 `STYLE` 未包含组件局部 `.multirate-svg` 样式，而非图形数据或公式渲染问题。
- 在整书样式中加入频谱、结构框、连线、坐标轴、中文标签及数学标签的完整规则。
- 新增总装配回归断言，要求两条频谱路径都以明确的 `fill:none` 与统一描边进入最终 HTML。
- 重新导出整书正文，并逐页检查第八章的装配后页面。

## Verification

- `python -m pytest -q full/tests/test_build_all_main_body.py full/tests/test_build_chapter_08_multirate_mathjax_component.py`: `2 passed`。
- A4 PDF 导出：MathJax `unrendered=[]`、`pageErrors=[]`。
- 已检查整书第 86--90 页：频谱不再黑填充；四幅图均无课件框、水印、裁切、重叠或端口悬空连线。

## Next

继续正文页级密度审计，优先重排非章节末尾的大面积空白页；冻结真题训练、详解与附录的重新编排，直至正文完成。
