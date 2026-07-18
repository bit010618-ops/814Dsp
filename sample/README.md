# 代表性样稿（制作中）

## 可修改源文件

- `tools/build_sample.py`：A4 PDF 生成器。
- `artifacts/sample_content.json`：8 页样稿内容与逐页结构。
- `artifacts/sample_spec.json`：字体、字号、页边距、配色与公式规则。
- `source-assets/source-spectrum-0528.png`：本样稿保留的原课件图。
- `tests/`：扫描、规范和 PDF 生成自动测试。

## 当前约束

- 所有公式使用统一数学字体及 11 pt 基准字号；分式使用竖式，分式高度不得使字变大或越出公式框。
- 该原课件图完整保留，避免裁切图内的 Ω、单位、坐标与参数标注。

## 验证

在此目录下运行：

```powershell
python -m pytest -q
python tools/build_sample.py --content artifacts/sample_content.json --output outputs/数字信号处理讲义_样稿.pdf
```
