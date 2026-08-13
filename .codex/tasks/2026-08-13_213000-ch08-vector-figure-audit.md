# 第八章原课件图净化与矢量重绘

## Objective

审计第八章正文中保留的原课件技术图；去除课件框、底纹、讲解标记与其他投影片元素，同时保留正确的多采样率技术关系。

## Completed

- 逐张核查了四张原图及其原始课件页，确认它们都含有不应进入讲义的投影片框线、底纹或强调标记。
- 以四张独立 SVG 图替换原有 PNG 引用：二倍抽取频谱过程、抗混叠抽取级联、插值级联、有理数倍采样率转换。
- 所有框图连线均以箭头明确终止于模块边界；无水印、页眉、页脚、来源文字或投影片配色残留。
- 修复频谱流程图中降幅子图越出面板的初版布局问题，并增加回归断言。

## Verification

- `python -m pytest -q full/tests/test_build_all_main_body.py full/tests/test_build_chapter_08_multirate_mathjax_component.py full/tests/test_crop_source_figures_ch8.py`：3 passed。
- `git diff --check`：通过。
- 已输出并逐页检查 `tmp/ch08-diagram-qa-v2.pdf`：MathJax `unrendered=[]`、`pageErrors=[]`；三张含图页无裁切、重叠或原课件外框。

## Next

提交并推送本次第八章图形修复；随后继续对全书正文中的公式、图形与分页进行审计。
