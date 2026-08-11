"""Chapter-three conceptual bridge from FS and FT to DTFT and DFS."""
from __future__ import annotations

from pathlib import Path

from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.mapping{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.mapping th,.mapping td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left}.mapping th{color:#315d7c;font-weight:500;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.mapping{font-size:9.5pt}.formula{padding:7pt 8pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第三章 离散傅里叶变换</h1>
<p>傅里叶分析的核心是把信号放在适合观察或计算的频域中描述。本章把前面已经见过的傅里叶级数、傅里叶变换和序列傅里叶变换连接起来，再建立离散傅里叶级数与离散傅里叶变换的计算框架。</p>

<h2>四类傅里叶描述的坐标关系</h2>
<table class="mapping"><thead><tr><th>时域</th><th>频域</th><th>对应工具</th></tr></thead><tbody>
<tr><td>连续时间</td><td>连续频率</td><td>傅里叶变换 FT</td></tr>
<tr><td>连续时间</td><td>离散频率</td><td>傅里叶级数 FS</td></tr>
<tr><td>离散时间</td><td>连续频率</td><td>序列傅里叶变换 DTFT</td></tr>
<tr><td>离散时间</td><td>离散频率</td><td>离散傅里叶级数 DFS</td></tr>
</tbody></table>
<p>时域周期性会导致频域离散性；频域周期性会导致时域离散性。DFS 恰好位于“离散时间、离散频率”的一格，因此它在两个域内都带有周期结构。</p>

<h2>从傅里叶级数到傅里叶变换</h2>
<p>对周期为 [[T_0]] 的连续时间信号，基本角频率为 [[\Omega_0=2\pi/T_0]]。其频谱只出现在谐波频点 [[k\Omega_0]] 上，频点间隔由 [[T_0]] 决定：</p>
<div class="formula">\[
T_0\uparrow\quad\Longrightarrow\quad\Omega_0=\frac{2\pi}{T_0}\downarrow.
\]</div>
<p>当 (T_0) 无限增大时，频谱取样间隔趋于零，离散的傅里叶级数频谱过渡为连续的傅里叶变换频谱。虽然相邻频点的数值可能相同，频率位置不同仍对应不同的物理谐波分量，不能只比较系数数值而忽略频率坐标。</p>

<h2>从连续时间频谱到 DTFT</h2>
<p>连续信号以采样间隔 [[T]] 变为序列后，模拟角频率 [[\Omega]] 与数字角频率 [[\omega]] 的关系为：</p>
<div class="formula">\[
\omega=\Omega T,\qquad \Omega=\frac{\omega}{T}.
\]</div>
<p>采样会使离散时间序列的频谱以 [[2\pi]] 为周期重复。若原模拟频谱在折叠频率以内，[[X(e^{j\omega})]] 可理解为 [[X(j\Omega)]] 在数字频率轴上的周期延拓，并带有与采样间隔相关的幅度缩放。减小 [[T]] 会提高采样频率、扩大可无混叠观察的频率范围。</p>

<h2>本章的计算视角</h2>
<p>频域把时域卷积化为乘积，因此常将复杂的时域计算转换到频域完成，再经反变换回到时域。离散形式允许使用有限个样本和快速算法完成计算；但使用任何有限点变换前，必须区分清楚线性卷积、循环卷积、记录长度与频率取样间隔。</p>
</main>
"""
    content = normalize_legacy_inline_math(
        content.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    )
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
