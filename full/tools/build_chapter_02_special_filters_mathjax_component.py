"""Core special-filter design theory, rendered only by MathJax."""
from __future__ import annotations

import subprocess
import sys
from base64 import b64encode
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:20mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.figure{margin:11pt auto 13pt;text-align:center;break-inside:avoid}.figure img{display:block;width:100%;max-width:148mm;margin:auto;border:0}.figure figcaption{color:#536b7d;font-size:9.5pt;line-height:1.55;margin-top:4pt}table{border-collapse:collapse;width:100%;margin:9pt 0 12pt;font-size:10pt;break-inside:avoid}th,td{border:.55pt solid #8299aa;padding:4pt 6pt;text-align:center}th{background:#eaf1f4;color:#1e4f79;font-weight:600}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def _png_uri(figure) -> str:
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=240, bbox_inches="tight", facecolor="white")
    buffer.seek(0)
    return "data:image/png;base64," + b64encode(buffer.read()).decode("ascii")


def _render_first_order_lowpass_figures() -> dict[str, str]:
    """Render the source example with data-driven, print-ready textbook plots."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams.update({
        "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "mathtext.fontset": "stix",
    })
    axis_color = "#244f72"
    stem_color = "#008e98"
    marker_color = "#bd6d0a"

    def discrete_axis(ax, xlim, ylim, xlabel, title, ticks):
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(0, color=axis_color, lw=1.05, zorder=0)
        ax.axvline(0, color=axis_color, lw=1.05, zorder=0)
        dx = (xlim[1] - xlim[0]) * 0.035
        dy = (ylim[1] - ylim[0]) * 0.07
        ax.annotate("", xy=(xlim[1], 0), xytext=(xlim[1] - dx, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
        ax.annotate("", xy=(0, ylim[1]), xytext=(0, ylim[1] - dy), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
        ax.set_xticks(ticks)
        ax.set_yticks([])
        ax.tick_params(axis="x", length=3, colors="#596b78", labelsize=8)
        ax.text(0.98, 0.04, xlabel, transform=ax.transAxes, ha="right", va="bottom", color=axis_color, fontsize=9)
        ax.text(0.04, 0.94, "幅值", transform=ax.transAxes, ha="left", va="top", color=axis_color, fontsize=9)
        ax.set_title(title, color="#1e4f79", fontsize=10, pad=7)

    figures: dict[str, str] = {}
    figure, ax = plt.subplots(figsize=(4.5, 3.65), constrained_layout=True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    theta = np.linspace(0, 2 * np.pi, 600)
    ax.plot(np.cos(theta), np.sin(theta), color="#8094a4", lw=1.2, ls="--", label="单位圆")
    ax.axhline(0, color=axis_color, lw=1.1)
    ax.axvline(0, color=axis_color, lw=1.1)
    ax.annotate("", xy=(1.34, 0), xytext=(1.2, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.1})
    ax.annotate("", xy=(0, 1.34), xytext=(0, 1.2), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.1})
    ax.scatter([-1], [0], s=60, marker="o", facecolors="white", edgecolors=stem_color, linewidths=1.8, zorder=3)
    ax.scatter([0.9], [0], s=82, marker="x", color=marker_color, linewidths=2.0, zorder=3)
    ax.text(-1, -0.16, r"$-1$（零点）", ha="center", va="top", fontsize=9, color=stem_color)
    ax.text(0.9, 0.14, r"$0.9$（极点）", ha="center", va="bottom", fontsize=9, color=marker_color)
    ax.text(0.06, -0.14, "0", ha="left", va="top", fontsize=9, color="#596b78")
    ax.text(1.3, 0.08, r"$\mathrm{Re}(z)$", ha="right", va="bottom", fontsize=10)
    ax.text(0.08, 1.3, r"$\mathrm{Im}(z)$", ha="left", va="top", fontsize=10)
    ax.set(xlim=(-1.38, 1.38), ylim=(-1.38, 1.38), aspect="equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("一阶低通滤波器的零极点配置", color="#1e4f79", fontsize=11, pad=8)
    figures["pole_zero"] = _png_uri(figure)
    plt.close(figure)

    fs = 1000.0
    n = np.arange(100)
    x = np.sin(2 * np.pi * 10 * n / fs) + np.sin(2 * np.pi * 250 * n / fs)
    y = np.zeros_like(x)
    for index in range(len(n)):
        y[index] = 0.9 * (y[index - 1] if index else 0.0) + 0.05 * x[index] + 0.05 * (x[index - 1] if index else 0.0)

    figure, axes = plt.subplots(2, 1, figsize=(6.8, 4.4), sharex=True, constrained_layout=True)
    for ax, sequence, title, limits in (
        (axes[0], x, "输入序列：10 Hz 与 250 Hz 叠加", (-2.2, 2.2)),
        (axes[1], y, "输出序列：保留低频、抑制高频", (-1.15, 1.15)),
    ):
        markerline, stemlines, baseline = ax.stem(n, sequence, linefmt=stem_color, markerfmt="o", basefmt=" ")
        markerline.set_markerfacecolor(marker_color)
        markerline.set_markeredgecolor(marker_color)
        markerline.set_markersize(2.9)
        stemlines.set_linewidth(0.75)
        discrete_axis(ax, (-4, 104), limits, r"$n$", title, [0, 20, 40, 60, 80, 100])
    axes[0].tick_params(axis="x", labelbottom=False)
    figures["time"] = _png_uri(figure)
    plt.close(figure)

    frequencies = np.fft.rfftfreq(len(n), d=1 / fs)
    input_spectrum = np.abs(np.fft.rfft(x))
    output_spectrum = np.abs(np.fft.rfft(y))
    input_spectrum /= input_spectrum.max()
    output_spectrum /= input_spectrum.max()
    omega = 2 * np.pi * frequencies / fs
    filter_amplitude = np.abs(0.05 * (1 + np.exp(-1j * omega)) / (1 - 0.9 * np.exp(-1j * omega)))
    figure, axes = plt.subplots(3, 1, figsize=(6.8, 3.5), constrained_layout=True)
    for ax, values, title, ylabel in (
        (axes[0], input_spectrum, "输入序列的离散幅度谱", "归一化幅度"),
        (axes[1], filter_amplitude, "一阶低通滤波器的幅频响应", "幅度"),
        (axes[2], output_spectrum, "输出序列的离散幅度谱", "归一化幅度"),
    ):
        markerline, stemlines, baseline = ax.stem(frequencies, values, linefmt=stem_color, markerfmt="o", basefmt=" ")
        markerline.set_markerfacecolor(marker_color)
        markerline.set_markeredgecolor(marker_color)
        markerline.set_markersize(3.2)
        stemlines.set_linewidth(0.8)
        discrete_axis(ax, (0, 520), (-0.05, 1.16 if title != "一阶低通滤波器的幅频响应" else 1.05), r"$f / \mathrm{Hz}$", title, [0, 100, 200, 300, 400, 500])
        ax.text(0.04, 0.80, ylabel, transform=ax.transAxes, ha="left", va="top", color=axis_color, fontsize=8.5)
    axes[0].axvline(10, color="#b56b2e", lw=0.8, ls=":")
    axes[0].axvline(250, color="#b56b2e", lw=0.8, ls=":")
    axes[2].axvline(10, color="#b56b2e", lw=0.8, ls=":")
    figures["spectrum"] = _png_uri(figure)
    plt.close(figure)
    return figures


def _render_resonator_figures() -> dict[str, str]:
    """Render the resonator examples from their poles and transfer functions."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.font_manager import FontProperties

    chinese_font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc")
    plt.rcParams.update({"axes.unicode_minus": False, "mathtext.fontset": "stix"})
    axis_color = "#244f72"
    pole_color = "#bd6d0a"
    curve_colors = ("#008e98", "#b56b2e")
    figures: dict[str, str] = {}

    figure, axes = plt.subplots(1, 2, figsize=(7.1, 3.15), constrained_layout=True)
    geometry, response = axes
    for spine in geometry.spines.values():
        spine.set_visible(False)
    theta = np.linspace(0, 2 * np.pi, 720)
    radius = 0.9
    centre = np.pi / 2
    geometry.plot(np.cos(theta), np.sin(theta), color="#8094a4", lw=1.1, ls="--")
    geometry.axhline(0, color=axis_color, lw=1.05)
    geometry.axvline(0, color=axis_color, lw=1.05)
    geometry.annotate("", xy=(1.30, 0), xytext=(1.15, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    geometry.annotate("", xy=(0, 1.30), xytext=(0, 1.15), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    poles = radius * np.exp(1j * np.array((centre, -centre)))
    geometry.scatter(poles.real, poles.imag, marker="x", s=68, lw=2.0, color=pole_color, zorder=4)
    geometry.plot([0, poles[0].real], [0, poles[0].imag], color="#aab8c2", lw=0.9, ls=":")
    geometry.text(0.08, 0.92, "共轭极点", transform=geometry.transAxes, fontproperties=chinese_font, color=pole_color, fontsize=9, va="top")
    geometry.text(0.95, 0.46, r"$\mathrm{Re}(z)$", transform=geometry.transAxes, fontsize=9, ha="right")
    geometry.text(0.53, 0.96, r"$\mathrm{Im}(z)$", transform=geometry.transAxes, fontsize=9, va="top")
    geometry.text(0.53, 0.75, r"$r=0.9$", fontsize=9, color=pole_color)
    geometry.set(xlim=(-1.34, 1.34), ylim=(-1.34, 1.34), aspect="equal")
    geometry.set_xticks([])
    geometry.set_yticks([])
    geometry.set_title("谐振器的极点位置", fontproperties=chinese_font, color="#1e4f79", fontsize=10.5, pad=6)

    omega = np.linspace(0, np.pi, 1600)
    for radius, color, label in ((0.70, curve_colors[0], r"$r=0.70$"), (0.93, curve_colors[1], r"$r=0.93$")):
        response_value = 1 / ((1 - radius * np.exp(1j * centre) * np.exp(-1j * omega)) * (1 - radius * np.exp(-1j * centre) * np.exp(-1j * omega)))
        magnitude = np.abs(response_value)
        response.plot(omega / np.pi, magnitude / magnitude.max(), color=color, lw=1.65, label=label)
    response.axvline(0.5, color="#8094a4", ls=":", lw=0.9)
    for spine in response.spines.values():
        spine.set_visible(False)
    response.axhline(0, color=axis_color, lw=1.05, zorder=0)
    response.axvline(0, color=axis_color, lw=1.05, zorder=0)
    response.annotate("", xy=(1.10, 0), xytext=(1.02, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    response.annotate("", xy=(0, 1.12), xytext=(0, 1.03), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    response.set(xlim=(0, 1.10), ylim=(0, 1.12), xticks=(0, 0.5, 1), xticklabels=("0", r"$1/2$", "1"), yticks=(0, 0.5, 1))
    response.grid(axis="y", color="#d9e1e6", lw=0.6)
    response.set_xlabel(r"$\omega/\pi$", fontsize=9)
    response.text(0.035, 0.92, "归一化幅度", transform=response.transAxes, fontproperties=chinese_font, fontsize=8.5, color=axis_color, va="top")
    response.set_title("极点半径控制谐振峰宽度", fontproperties=chinese_font, color="#1e4f79", fontsize=10.5, pad=6)
    response.legend(prop=chinese_font, frameon=False, fontsize=8, loc="upper left")
    figures["pole_zero_response"] = _png_uri(figure)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(6.8, 3.0), constrained_layout=True)
    radius_squared = 0.7
    gain = 0.15
    omega = np.linspace(0, np.pi, 1600)
    response_value = gain * (1 - np.exp(-2j * omega)) / (1 + radius_squared * np.exp(-2j * omega))
    axis.plot(omega / np.pi, np.abs(response_value), color="#008e98", lw=1.85)
    axis.axvline(0.5, color="#b56b2e", ls=":", lw=1.0)
    axis.scatter((0, 0.5, 1), (0, np.abs(response_value[len(omega)//2]), 0), color="#bd6d0a", zorder=3, s=22)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.axhline(0, color=axis_color, lw=1.05, zorder=0)
    axis.axvline(0, color=axis_color, lw=1.05, zorder=0)
    axis.annotate("", xy=(1.10, 0), xytext=(1.02, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    axis.annotate("", xy=(0, 1.12), xytext=(0, 1.03), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    axis.set(xlim=(0, 1.10), ylim=(-0.02, 1.12), xticks=(0, 0.5, 1), xticklabels=("0", r"$1/2$", "1"), yticks=(0, 0.5, 1))
    axis.grid(axis="y", color="#d9e1e6", lw=0.6)
    axis.set_xlabel(r"$\omega/\pi$", fontsize=9)
    axis.text(0.035, 0.92, "幅度", transform=axis.transAxes, fontproperties=chinese_font, fontsize=8.5, color=axis_color, va="top")
    axis.set_title("二阶带通谐振器的实际幅频响应", fontproperties=chinese_font, color="#1e4f79", fontsize=10.8, pad=7)
    axis.annotate("中心频率", xy=(0.5, np.abs(response_value[len(omega)//2])), xytext=(0.61, 0.84), fontproperties=chinese_font, fontsize=8.5, color="#7c4a16", arrowprops={"arrowstyle": "->", "color": "#7c4a16", "lw": 0.8})
    axis.text(0.02, 0.08, "直流零点", fontproperties=chinese_font, fontsize=8.5, color="#596b78")
    axis.text(0.82, 0.08, "最高频零点", fontproperties=chinese_font, fontsize=8.5, color="#596b78")
    figures["bandpass_response"] = _png_uri(figure)
    plt.close(figure)

    figure, axes = plt.subplots(1, 2, figsize=(7.1, 3.15), constrained_layout=True)
    geometry, response = axes
    notch_frequency = 0.1 * np.pi
    notch_radius = 0.95
    for spine in geometry.spines.values():
        spine.set_visible(False)
    geometry.plot(np.cos(theta), np.sin(theta), color="#8094a4", lw=1.1, ls="--")
    geometry.axhline(0, color=axis_color, lw=1.05)
    geometry.axvline(0, color=axis_color, lw=1.05)
    geometry.annotate("", xy=(1.30, 0), xytext=(1.15, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    geometry.annotate("", xy=(0, 1.30), xytext=(0, 1.15), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    zeros = np.exp(1j * np.array((notch_frequency, -notch_frequency)))
    poles = notch_radius * np.exp(1j * np.array((notch_frequency, -notch_frequency)))
    geometry.scatter(zeros.real, zeros.imag, marker="o", s=52, lw=1.8, facecolors="white", edgecolors="#008e98", zorder=4)
    geometry.scatter(poles.real, poles.imag, marker="x", s=62, lw=1.9, color=pole_color, zorder=4)
    geometry.plot([0, zeros[0].real], [0, zeros[0].imag], color="#aab8c2", lw=0.9, ls=":")
    geometry.text(0.58, 0.74, "单位圆零点", transform=geometry.transAxes, fontproperties=chinese_font, color="#008e98", fontsize=8.6)
    geometry.text(0.56, 0.60, "内侧极点", transform=geometry.transAxes, fontproperties=chinese_font, color=pole_color, fontsize=8.6)
    geometry.text(0.95, 0.46, r"$\mathrm{Re}(z)$", transform=geometry.transAxes, fontsize=9, ha="right")
    geometry.text(0.53, 0.96, r"$\mathrm{Im}(z)$", transform=geometry.transAxes, fontsize=9, va="top")
    geometry.set(xlim=(-1.34, 1.34), ylim=(-1.34, 1.34), aspect="equal")
    geometry.set_xticks([])
    geometry.set_yticks([])
    geometry.set_title("50 Hz 陷波器的零极点配置", fontproperties=chinese_font, color="#1e4f79", fontsize=10.5, pad=6)

    omega = np.linspace(0, np.pi, 1600)
    response_value = (1 - 2 * np.cos(notch_frequency) * np.exp(-1j * omega) + np.exp(-2j * omega)) / (1 - 2 * notch_radius * np.cos(notch_frequency) * np.exp(-1j * omega) + notch_radius ** 2 * np.exp(-2j * omega))
    response.plot(omega / np.pi, np.abs(response_value), color="#008e98", lw=1.7)
    response.axvline(0.1, color="#b56b2e", ls=":", lw=1.0)
    response.scatter((0.1,), (0,), color=pole_color, zorder=3, s=22)
    for spine in response.spines.values():
        spine.set_visible(False)
    response.axhline(0, color=axis_color, lw=1.05, zorder=0)
    response.axvline(0, color=axis_color, lw=1.05, zorder=0)
    response.annotate("", xy=(1.10, 0), xytext=(1.02, 0), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    response.annotate("", xy=(0, 1.12), xytext=(0, 1.03), arrowprops={"arrowstyle": "-|>", "color": axis_color, "lw": 1.05})
    response.set(xlim=(0, 1.10), ylim=(0, 1.12), xticks=(0, 0.1, 0.5, 1), xticklabels=("0", r"$0.1$", r"$1/2$", "1"), yticks=(0, 0.5, 1))
    response.grid(axis="y", color="#d9e1e6", lw=0.6)
    response.set_xlabel(r"$\omega/\pi$", fontsize=9)
    response.text(0.035, 0.92, "幅度", transform=response.transAxes, fontproperties=chinese_font, fontsize=8.5, color=axis_color, va="top")
    response.set_title("50 Hz 对应的陷波频率", fontproperties=chinese_font, color="#1e4f79", fontsize=10.5, pad=6)
    response.annotate("50 Hz", xy=(0.1, 0), xytext=(0.20, 0.30), fontproperties=chinese_font, fontsize=8.5, color="#7c4a16", arrowprops={"arrowstyle": "->", "color": "#7c4a16", "lw": 0.8})
    figures["notch_response"] = _png_uri(figure)
    plt.close(figure)
    return figures


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    figures = _render_first_order_lowpass_figures()
    figures.update(_render_resonator_figures())
    content = r'''
<main>
<h1>特殊滤波器的设计</h1>
<p>本节只保留数字信号处理与考研复习所需的设计思想、数学结构和判读原则。所有设计都从同一规则出发：要抑制某个频率，就在单位圆对应位置布置零点；要增强某个频率，就在同方向、单位圆内靠近该位置布置极点。</p>
<h2>简单一阶低通与高通</h2>
<p>在 [[\omega=\pi]] 处放零点可抑制最高离散频率，得到最简单的低通平滑器：</p>
<div class="formula">\[H(z)=\frac{z+1}{2z}=\frac{1}{2}(1+z^{-1}),\qquad y(n)=\frac{1}{2}[x(n)+x(n-1)]\]</div>
<p>在 [[\omega=0]] 处放零点可抑制直流和缓慢变化部分，得到最简单的高通器：</p>
<div class="formula">\[H(z)=\frac{z-1}{2z}=\frac{1}{2}(1-z^{-1}),\qquad y(n)=\frac{1}{2}[x(n)-x(n-1)]\]</div>
<p>另一类低通设计是在 [[z=a]]、[[0&lt;a&lt;1]] 处放一个靠近 [[z=1]] 的极点；极点越接近单位圆，低频增强越明显，但必须严格留在单位圆内以保证稳定。单极点低通的系统函数为：</p>
<div class="formula">\[H(z)=\frac{1-a}{z-a},\qquad 0&lt;a&lt;1\]</div>
<p>若同时在 [[z=-1]] 布置零点，就能在保留低频增强能力的同时压低最高频率处的幅度。一阶低通的实用形式为：</p>
<div class="formula">\[H(z)=\frac{1-a}{2}\frac{z+1}{z-a},\qquad 0&lt;a&lt;1\]</div>
<figure class="figure"><img src="{{LOWPASS_POLE_ZERO}}" alt="一阶低通滤波器的零极点图"><figcaption>一阶低通滤波器的零极点图：零点位于 [[z=-1]]，极点位于 [[z=a]]；极点越接近单位圆，低频选择性越强。</figcaption></figure>
<p>把通带截止频率定义为幅度下降到 \(-3\,\mathrm{dB}\) 的频率 \(\omega_c\)，则：</p>
<div class="formula">\[\cos\omega_c=\frac{4a-a^2-1}{2a}\]</div>
<p>等价地，截止频率可直接按下式确定：</p>
<div class="formula">\[\omega_c=\arccos\left(\frac{2a}{1+a^2}\right)\]</div>
<p>当 \(a\) 靠近 1 时，截止频率的近似关系为 \(\omega_c\approx1-a\)。因此极点越靠近单位圆，通带越窄、低频选择性越强。下表保留原课件给出的典型数值，带宽单位均为 rad：</p>
<table><thead><tr><th>\(a\)</th><th>精确带宽 \(\omega_c\)</th><th>近似带宽 \(1-a\)</th></tr></thead><tbody><tr><td>0.60</td><td>0.49</td><td>0.40</td></tr><tr><td>0.70</td><td>0.35</td><td>0.30</td></tr><tr><td>0.80</td><td>0.22</td><td>0.20</td></tr><tr><td>0.85</td><td>0.16</td><td>0.15</td></tr><tr><td>0.90</td><td>0.10</td><td>0.10</td></tr><tr><td>0.95</td><td>0.05</td><td>0.05</td></tr></tbody></table>
<h3>例题</h3>
<p>假设模拟信号如下，设计一个一阶低通数字滤波器，将信号中的高频分量滤除。</p>
<div class="formula">\[x(t)=\sin(2\pi\cdot10t)+\sin(2\pi\cdot250t)\]</div>
<p>取采样频率 \(f_s=1000\,\mathrm{Hz}\)，则需保留的低频和需要滤除的高频对应数字频率分别为：</p>
<div class="formula">\[\omega_1=2\pi\frac{10}{1000}=0.02\pi\approx0.0628\,\mathrm{rad},\qquad \omega_2=2\pi\frac{250}{1000}=0.5\pi\,\mathrm{rad}\]</div>
<p>为了让低频成分通过而使高频成分衰减，截止频率应满足：</p>
<div class="formula">\[0.0628&lt;\omega_c&lt;0.5\pi\]</div>
<p>按近似带宽取 \(\omega_c\approx0.1\)，于是 \(a=0.9\)。所得系统函数和对应差分方程为：</p>
<div class="formula">\[H(z)=0.05\frac{1+z^{-1}}{1-0.9z^{-1}}\]</div>
<div class="formula">\[y(n)=0.9y(n-1)+0.05x(n)+0.05x(n-1)\]</div>
<figure class="figure"><img src="{{LOWPASS_TIME}}" alt="10 Hz 与 250 Hz 输入、输出的离散序列对比"><figcaption>10 Hz 与 250 Hz 输入、输出的离散序列对比：离散样值使用标准 stem 图表示，输出中高频交替变化被明显压低。</figcaption></figure>
<figure class="figure"><img src="{{LOWPASS_SPECTRUM}}" alt="一阶低通滤波前后的离散频谱"><figcaption>一阶低通滤波前后的离散频谱：10 Hz 分量通过，250 Hz 分量仅被一阶滤波器部分衰减；提高选择性需进一步缩小带宽或提高阶数。</figcaption></figure>
<h2>数字谐振器</h2>
<p>数字谐振器把输入频谱中靠近某一固有频率的成分显著增强。二阶实系数谐振器通常在单位圆内、角度为 [[\pm\omega_0]] 的位置配置一对共轭极点：</p>
<div class="formula">\[p_{1,2}=re^{\pm j\omega_0},\qquad 0&lt;r&lt;1\]</div>
<p>二阶谐振器的系统函数用于给出“中心频率由极点角度决定、选择性由极点半径决定”的标准结构：</p>
<div class="formula">\[H(z)=\frac{A}{(1-re^{j\omega_0}z^{-1})(1-re^{-j\omega_0}z^{-1})}\]</div>
<p>极点角度决定通带中心频率 [[\omega_0]]；半径 [[r]] 决定选择性。[[r]] 越接近 1，极点越接近单位圆，谐振峰越尖、带宽越窄。若同时要求在直流与最高频率处完全抑制，可在 [[z=1]]、[[z=-1]] 处配置零点，得到一类二阶带通结构：</p>
<figure class="figure" data-plot="resonator-pole-zero-response"><img src="{{RESONATOR_POLE_ZERO_RESPONSE}}" alt="谐振器极点半径与频率选择性"><figcaption>谐振器的极点—频率选择性关系：极点角度设定中心频率；极点半径越接近单位圆，谐振峰越尖、带宽越窄。</figcaption></figure>
<div class="formula">\[H(z)=G\frac{1-z^{-2}}{1-2r\cos\omega_0\,z^{-1}+r^2z^{-2}}\]</div>
<p>其中 [[G]] 用中心频率处的目标幅度确定；[[r]] 则由给定带宽或指定频率处的幅度条件确定。设计后必须检查极点半径小于 1，才能保证因果稳定。</p>
<h3>例题</h3>
<p>设计一个二阶带通滤波器，[[\omega_0=\frac{\pi}{2}]] 是通带中心，在 [[\omega=0,\pi]] 两点频率响应为零，在 [[\omega=\frac{4\pi}{9}]] 处幅度为 [[\frac{1}{\sqrt2}]]。</p>
<p>由通带中心和两端零响应条件，零点取在 [[z=\pm1]]，极点取在 [[z=\pm jr]]，因此带通滤波器的设计式为：</p>
<div class="formula">\[H(z)=G\frac{z^2-1}{z^2+r^2}\]</div>
<p>把指定频率的幅度条件代入后，得到 [[r^2=0.7]]、[[G=0.15]]。故本题的设计结果为：</p>
<div class="formula">\[H(z)=0.15\frac{z^2-1}{z^2+0.7}\]</div>
<figure class="figure" data-plot="bandpass-resonator-response"><img src="{{BANDPASS_RESPONSE}}" alt="二阶带通谐振器的幅频响应"><figcaption>二阶带通谐振器的幅频响应：由本例的实际系统函数计算，直流与最高频率处为零，中心频率处形成通带峰值。</figcaption></figure>
<h2>DTMF 双音多频信号</h2>
<p>电话按键的 DTMF 信号由一个低频组频率与一个高频组频率叠加而成。低频组为 697、770、852、941 Hz，高频组为 1209、1336、1477、1633 Hz。每个按键对应唯一的一对频率；例如按键 8 对应 852 Hz 和 1336 Hz。</p>
<table data-table="dtmf-keypad"><thead><tr><th>低频组／高频组</th><th>1209 Hz</th><th>1336 Hz</th><th>1477 Hz</th><th>1633 Hz</th></tr></thead><tbody><tr><th>697 Hz</th><td>1</td><td>2</td><td>3</td><td>A</td></tr><tr><th>770 Hz</th><td>4</td><td>5</td><td>6</td><td>B</td></tr><tr><th>852 Hz</th><td>7</td><td>8</td><td>9</td><td>C</td></tr><tr><th>941 Hz</th><td>*</td><td>0</td><td>#</td><td>D</td></tr></tbody></table>
<p>这张按键—双频对应表用于由按键位置直接确定需要叠加或检测的两条目标频率；普通电话键盘通常只使用前三列。</p>
<div class="formula">\[x(n)=A_1\cos(\omega_1n+\varphi_1)+A_2\cos(\omega_2n+\varphi_2),\qquad \omega_i=2\pi\frac{f_i}{f_s}\]</div>
<p>以按键 8 为例，取 [[f_s=8000\,\mathrm{Hz}]] 时，两个谐振器中心的数字频率为：</p>
<div class="formula">\[\omega_1=2\pi\frac{852}{8000}=0.213\pi,\qquad \omega_2=2\pi\frac{1336}{8000}=0.334\pi\]</div>
<p>生成某个按键信号时，可分别用两个中心频率对应的数字谐振器选择所需频率，再将两路输出相加。判读题目时先由采样频率换算数字频率，再确认两个通带中心分别落在对应低频组和高频组频率上。</p>
<h2>数字陷波器</h2>
<p>陷波器用于消除特定窄带干扰。若要抑制数字频率 [[\omega_0]]，必须在单位圆上成对放置共轭零点，才能保证实系数：</p>
<div class="formula">\[z=e^{\pm j\omega_0},\qquad \omega_0=2\pi\frac{f_0}{f_s}\]</div>
<p>一个二阶陷波器可写为：</p>
<div class="formula">\[H(z)=K\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{z^2}\]</div>
<figure class="figure" data-plot="notch-zero-pole-response"><img src="{{NOTCH_RESPONSE}}" alt="50 Hz 陷波器的零极点与幅频响应"><figcaption>50 Hz 陷波器的零极点与幅频响应：单位圆上一对零点给出精确阻零，内侧同角度极点控制陷波宽度并保持因果稳定。</figcaption></figure>
<h3>例题</h3>
<p>若采样频率 [[f_s=1000\,\mathrm{Hz}]]，需抑制 50 Hz 工频干扰，则陷波中心的数字频率为：</p>
<div class="formula">\[\omega_0=2\pi\frac{50}{1000}=0.1\pi\]</div>
<p>本式用于在 [[\omega_0]] 处设置一对单位圆零点；按原例的幅度归一化系数，系统函数为：</p>
<div class="formula">\[H(z)=\frac{1}{3.9}\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{z^2}\]</div>
<p>实际实现中，有限字长会使陷波中心偏移。若还要保持较窄的陷波宽度，可把极点置于相同角度、半径 [[r&lt;1]] 的位置：</p>
<div class="formula">\[H(z)=\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{(z-re^{j\omega_0})(z-re^{-j\omega_0})}\]</div>
<p>[[r]] 越接近 1，陷波越窄；同时也越要求系数量化足够精确，避免 50 Hz 的抑制中心产生明显偏移。</p>
<p>频率、采样率与 DFT 索引的换算必须统一使用：</p>
<div class="formula">\[\frac{k}{N}=\frac{\omega}{2\pi}=\frac{f}{f_s}=\frac{\Omega}{\Omega_s}\]</div>
<h2>全通滤波器</h2>
<p>全通滤波器的幅度在整个频带内恒为一；它不改变幅度，只校正相位或群延迟：</p>
<div class="formula">\[\left|H_{\mathrm{ap}}(e^{j\omega})\right|=1,\qquad 0\leq\omega&lt;2\pi\]</div>
<p>若 [[D(z)]] 的极点都在单位圆内，则实系数稳定全通滤波器可表示为：</p>
<div class="formula">\[H_{\mathrm{ap}}(z)=A\frac{z^{-N}D(z^{-1})}{D(z)}=A\prod_{i=1}^{N}\frac{z^{-1}-p_i^*}{1-p_i z^{-1}}\]</div>
<p>其零极点具有共轭倒易关系：每个极点 [[p_i]] 对应零点 [[1/p_i^*]]。稳定实系数全通滤波器在 [[0,\pi]] 内相位单调减小，群延迟为正。</p>
<h2>最小相位滤波器</h2>
<h3>逆系统与最小相位条件</h3>
<p>逆系统用于抵消已知系统的传递作用：原系统与其逆系统级联后，整体输出应恢复为输入。其系统函数关系为：</p>
<div class="formula">\[H_i(z)=\frac{1}{H(z)},\qquad H(z)H_i(z)=1\]</div>
<p>若一个因果稳定系统及其逆系统都要求因果稳定，则原系统的全部零点和极点都必须位于单位圆内。这类系统称为最小相位系统。</p>
<p>任何适当的因果稳定系统可分解为最小相位部分和全通部分：</p>
<div class="formula">\[H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)\]</div>
<p>相位与群延迟满足可加关系：</p>
<div class="formula">\[\arg H(e^{j\omega})=\arg H_{\min}(e^{j\omega})+\arg H_{\mathrm{ap}}(e^{j\omega})\]</div>
<div class="formula">\[\operatorname{grd}\{H(e^{j\omega})\}=\operatorname{grd}\{H_{\min}(e^{j\omega})\}+\operatorname{grd}\{H_{\mathrm{ap}}(e^{j\omega})\}\]</div>
<p>全通部分只额外引入相位滞后和正群延迟，因此最小相位部分具有最小相位滞后、最小群延迟和最小能量延迟。分解时，将单位圆内的零极点归入 [[H_{\min}(z)]]，单位圆外的零点通过共轭倒易配对组成 [[H_{\mathrm{ap}}(z)]]。</p>
<h3>例题</h3>
<p>将单位圆外的零点折回单位圆内，可把一个因果稳定系统分解为最小相位部分和全通部分。对下式，零点 [[z=3]] 位于单位圆外，极点 [[z=3/4]] 位于单位圆内：</p>
<div class="formula">\[H(z)=\frac{1-3z^{-1}}{1-\frac{3}{4}z^{-1}}\]</div>
<p>下列最小相位因子把零点映射为 [[z=1/3]]，因此它的零极点均位于单位圆内：</p>
<div class="formula">\[H_{\min}(z)=3\frac{z-\frac{1}{3}}{z-\frac{3}{4}}\]</div>
<p>与之配对的全通因子不改变幅频响应，只补偿相位；二者相乘恰好恢复原系统：</p>
<div class="formula">\[H_{\mathrm{ap}}(z)=\frac{z-3}{3z-1},\qquad H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)\]</div>
<h2>工程中常用的滤波方法</h2>
<p>下列方法用于离散采样数据的预处理，重点在于理解适用的干扰类型与参数选择，而非程序实现。</p>
<h3>限幅滤波</h3>
<p>设 [[E]] 为两次采样允许的最大偏差。若新样值与上一次有效输出相差过大，则以旧输出代替新样值，因而可抑制偶发脉冲干扰：</p>
<div class="formula">\[y(n)=\begin{cases}x(n),&\left|x(n)-y(n-1)\right|\le E,\\y(n-1),&\left|x(n)-y(n-1)\right|&gt;E.\end{cases}\]</div>
<p>阈值过小会误删信号的真实突变；阈值过大则难以去除干扰。</p>
<h3>中值滤波与滑动平均</h3>
<p>中值滤波把连续 [[N]] 个采样值排序后取中间值，对孤立异常点有效；滑动平均则取一个局部窗口内的算术平均，能平滑高频波动，但对脉冲干扰的抑制较弱：</p>
<div class="formula">\[y(n)=\operatorname{med}\left\{x(n-M),\ldots,x(n),\ldots,x(n+M)\right\}\]</div>
<div class="formula">\[y(n)=\frac{1}{M_1+M_2+1}\sum_{k=-M_1}^{M_2}x(n-k)\]</div>
<p>中值平均可先删除一个最大值和一个最小值，再对其余样值取均值；限幅平均可先作限幅，再作滑动平均。加权平均中离当前时刻越近的样值通常赋予更大的权重，灵敏度提高的同时平滑能力会下降。</p>
<h2>本节检查顺序</h2>
<p>先把目标频率换成数字频率，再按“零点抑制、极点增强”的规则确定位置；随后检查共轭对称以保证实系数、检查全部极点位于单位圆内以保证稳定；最后根据是否保幅判断是否属于全通，并根据零极点位置判断是否最小相位。</p>
</main>'''.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    content = (content
               .replace("{{LOWPASS_POLE_ZERO}}", figures["pole_zero"])
               .replace("{{LOWPASS_TIME}}", figures["time"])
               .replace("{{LOWPASS_SPECTRUM}}", figures["spectrum"])
               .replace("{{RESONATOR_POLE_ZERO_RESPONSE}}", figures["pole_zero_response"])
               .replace("{{BANDPASS_RESPONSE}}", figures["bandpass_response"])
               .replace("{{NOTCH_RESPONSE}}", figures["notch_response"]))
    document = f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_special_filters_mathjax_component.pdf"))
