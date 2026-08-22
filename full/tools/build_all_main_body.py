"""Build the eight-chapter handout body before any training is attached."""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_01_body_only as chapter_one,
    build_chapter_02_body_only as chapter_two,
    build_chapter_03_dfs_mathjax_component as chapter_three_dfs,
    build_chapter_03_dft_mathjax_component as chapter_three_dft,
    build_chapter_03_frequency_sampling_mathjax_component as chapter_three_frequency_sampling,
    build_chapter_03_lsi_output_mathjax_component as chapter_three_lsi_output,
    build_chapter_03_overview_mathjax_component as chapter_three_overview,
    build_chapter_03_spectrum_analysis_mathjax_component as chapter_three_spectrum,
    build_chapter_04_dft_efficiency_mathjax_component as chapter_four_efficiency,
    build_chapter_04_dif_ifft_optimization_mathjax_component as chapter_four_dif_ifft,
    build_chapter_04_dit_fft_mathjax_component as chapter_four_dit,
    build_chapter_05_filter_structures_mathjax_component as chapter_five,
    build_chapter_06_iir_design_mathjax_component as chapter_six,
    build_chapter_07_fir_design_mathjax_component as chapter_seven,
    build_chapter_08_multirate_mathjax_component as chapter_eight,
)
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""
<style>
@page{size:A4;margin:24mm 18mm 20mm;@top-left{content:"数字信号处理讲义";color:#486d8b;font:9pt "Microsoft YaHei",serif;border-bottom:.45pt solid #c59d6e;padding-bottom:3pt}@top-right{content:string(running-title,first);color:#52616b;font:9pt "Microsoft YaHei",serif;border-bottom:.45pt solid #c59d6e;padding-bottom:3pt}@bottom-center{content:counter(page);color:#52616b;font:9pt "Times New Roman",serif}}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
.chapter-start+.chapter-start{break-before:page}
h1{string-set:running-title content(text);break-after:avoid;color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
h4{break-after:avoid;color:#315d7c;font-size:11.5pt;font-weight:400;margin:10pt 0 3pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.formula-wide{padding:8pt 10pt;font-size:9.5pt}
.formula mjx-container[display="true"]{max-width:100%;margin:0 auto!important}
.chapter-formula-summary{break-before:auto}
.chapter-formula-summary>p{color:#486d8b;margin:0 0 10pt}
.chapter-formula-summary .formula-name{break-after:avoid;color:#52616b;font-size:10.5pt;margin:9pt 0 3pt}
.chapter-formula-summary .formula{break-inside:avoid}
.mapping,.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt;break-inside:avoid}
.mapping th,.mapping td,.table th,.table td{border:.45pt solid #b9c6cf;padding:6pt 7pt;text-align:left;vertical-align:top}
.mapping th,.table th{color:#315d7c;font-weight:600;background:#f4f7f8}
figure{break-inside:avoid;margin:12pt auto;text-align:center}
.zero-order-hold-flow{break-inside:avoid;max-width:145mm}
.source-figure{max-width:100%;padding:0;background:#fff;border:1px solid #d8e0e5;border-radius:5pt;overflow:hidden}
.source-figure.compact{max-width:156mm}
.source-figure-flow{break-inside:auto;max-width:156mm;margin:8pt auto}
.source-figure img{display:block;width:100%;height:auto}
.source-figure figcaption{padding:5pt 8pt 6pt;color:#486d8b;font-size:9.5pt;text-align:center;background:#fbfcfd}
.chart-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9pt;align-items:start}
.chart-grid figure{width:100%;margin:6pt auto 10pt}
.typical-sequence-continuation .chart{break-inside:auto;margin:6pt auto 8pt}
.typical-sequence-continuation .chart svg{max-width:500px!important}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9pt;align-items:start}
.grid svg{width:100%;height:auto}
svg{max-width:100%;height:auto}
.diagram{background:#f8fafb;border:1px solid #d8e0e5;border-radius:5pt;padding:8pt;margin:10pt 0}
.structure-svg{display:block;width:100%;height:auto}
.structure-svg .wire{fill:none;stroke:#174b73;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.structure-svg .block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}
.structure-svg .sum{fill:#fff;stroke:#174b73;stroke-width:2.4}
.structure-svg .branch{fill:#174b73}
.structure-svg .sum-sign{font:24px "Times New Roman",serif;fill:#174b73}
.structure-svg .math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:20px}
.multirate-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.multirate-svg .wire{fill:none;stroke:#174b73;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.multirate-svg .block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.multirate-svg .label{fill:#315d7c;font:17px "Microsoft YaHei",sans-serif}.multirate-svg .annotation{fill:#587083;font:14px "Microsoft YaHei",sans-serif}.multirate-svg .axis{fill:none;stroke:#315d7c;stroke-width:1.7;stroke-linecap:round}.multirate-svg .spectrum-a{fill:none;stroke:#0d8794;stroke-width:2.4;stroke-linejoin:round}.multirate-svg .spectrum-b{fill:none;stroke:#b56b2e;stroke-width:2.4;stroke-linejoin:round}.multirate-svg .panel{fill:#fff;stroke:#d8e0e5;stroke-width:1.2}.multirate-svg .math-label div{height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:17px;white-space:nowrap;overflow:visible}
.chain-svg,.spectrum-svg,.wheel-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.chain-svg .chain-box{fill:#f4f7f8;stroke:#b08d57;stroke-width:1.6}.chain-svg .chain-label{fill:#1e4f79;font:18px "Microsoft YaHei",sans-serif}.chain-svg .chain-arrow{fill:none;stroke:#174b73;stroke-width:2.1;stroke-linecap:round}
.spectrum-svg .axis,.spectrum-svg .guide{fill:none;stroke:#174b73;stroke-linecap:round}.spectrum-svg .axis{stroke-width:2.1}.spectrum-svg .guide{stroke-width:1.5}.spectrum-svg .replica{fill:none;stroke-width:3;stroke-linejoin:round}
.wheel-svg .wheel-rim{fill:none;stroke:#b6342d;stroke-width:4}.wheel-svg .spoke{fill:none;stroke:#0f8b8d;stroke-width:2.5}.wheel-svg .hub{fill:#f4f7f8;stroke:#b6342d;stroke-width:3}.wheel-svg .marker{fill:#174b73}.wheel-svg .wheel-label{fill:#1e4f79;font:17px "Microsoft YaHei",sans-serif}.wheel-svg .wheel-note{fill:#51697b;font:15px "Microsoft YaHei",sans-serif}
.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.signal-svg .axis{fill:none;stroke:#174b73;stroke-width:2}
.signal-svg .guide{fill:none;stroke:#174b73;stroke-width:1.45}.signal-svg .overlap{fill:none;stroke:#b13a3a;stroke-width:3}.signal-svg .separated,.signal-svg .replica{fill:none;stroke:#0f8b8d;stroke-width:3;stroke-linejoin:round}.signal-svg .passband{fill:none;stroke:#b08d57;stroke-width:2.2}.signal-svg .band-fill{fill:#dceff0;stroke:#0f8b8d;stroke-width:2}.signal-svg .dimension{fill:none;stroke:#b08d57;stroke-width:1.7}.signal-svg .plain-label,.signal-svg .figure-note{fill:#486d8b;font:16px "Microsoft YaHei",sans-serif}.signal-svg .bad-note{fill:#b13a3a;font:16px "Microsoft YaHei",sans-serif}.signal-svg .good-note{fill:#0f8b8d;font:16px "Microsoft YaHei",sans-serif}.signal-svg .sinc-primary{fill:none;stroke:#0f8b8d;stroke-width:3}.signal-svg .sinc-secondary{fill:none;stroke:#78babc;stroke-width:2}.signal-svg .sample-dot{fill:#b56b2e}
.signal-svg .stem{stroke:#b45309;stroke-width:2}
.signal-svg .hold{fill:none;stroke:#0f8b8d;stroke-width:3;stroke-linejoin:round}
.signal-svg .dot{fill:#b45309}.signal-svg .tick{stroke:#174b73;stroke-width:1.3}
.signal-svg .label{fill:#374c5b;font:16px "Microsoft YaHei",sans-serif}
.signal-svg .conv-line{fill:none;stroke:#008f95;stroke-width:3}
.fir-flow-svg,.fir-symmetry-svg,.fir-pz-svg,.fir-sampling-svg,.fir-spectrum-selection-svg,.iir-route-svg,.iir-plane-map-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.fir-flow-svg .box{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.fir-flow-svg .freq-box{fill:#fff8df;stroke:#b08d57;stroke-width:2}.fir-flow-svg .wire{fill:none;stroke:#174b73;stroke-width:2.4}.fir-flow-svg .arrow{fill:none;stroke:#174b73;stroke-width:2.4;marker-end:url(#fir-flow-arrow)}.fir-flow-svg .label,.fir-symmetry-svg .label,.fir-pz-svg .label,.fir-sampling-svg .label{fill:#243746;font:16px "Microsoft YaHei",sans-serif}.fir-flow-svg .math,.fir-symmetry-svg .math,.fir-pz-svg .math,.fir-sampling-svg .math{fill:#172b3a;font:italic 19px "Times New Roman",serif}.fir-flow-svg .caption,.fir-symmetry-svg .caption,.fir-pz-svg .caption,.fir-sampling-svg .caption{fill:#486d8b;font:15px "Microsoft YaHei",sans-serif}
.math-foreign>div{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:16px;line-height:1;overflow:visible}.math-foreign mjx-container{margin:0!important}
.fir-symmetry-svg .axis,.fir-pz-svg .axis,.fir-sampling-svg .axis{fill:none;stroke:#174b73;stroke-width:2}.fir-symmetry-svg .guide{stroke:#8ba1b0;stroke-width:1.5;stroke-dasharray:5 4}.fir-symmetry-svg .stem{stroke:#b45309;stroke-width:2.2}.fir-symmetry-svg .dot{fill:#b45309}.fir-symmetry-svg .mirror{stroke:#0d8794;stroke-width:1.8;stroke-dasharray:5 4}.fir-pz-svg .unit{fill:none;stroke:#8ba1b0;stroke-width:1.7}.fir-pz-svg .zero{fill:#fff;stroke:#0d8794;stroke-width:3}.fir-pz-svg .pole{stroke:#b6342d;stroke-width:3}.fir-sampling-svg .ideal{fill:none;stroke:#0d8794;stroke-width:2.5;stroke-dasharray:7 4}.fir-sampling-svg .response{fill:none;stroke:#174b73;stroke-width:3}.fir-sampling-svg .stem{stroke:#b45309;stroke-width:2}.fir-sampling-svg .dot{fill:#b45309}.fir-sampling-svg .transition{fill:#fbf0e7;stroke:none}
.fir-spectrum-selection-svg .axis{fill:none;stroke:#174b73;stroke-width:2}.fir-spectrum-selection-svg .input-spectrum{fill:none;stroke:#0d8794;stroke-width:3;stroke-linejoin:round}.fir-spectrum-selection-svg .filter-response{fill:none;stroke:#b56b2e;stroke-width:3;stroke-linejoin:round}.fir-spectrum-selection-svg .output-spectrum{fill:none;stroke:#174b73;stroke-width:3;stroke-linejoin:round}.fir-spectrum-selection-svg .cutoff{fill:none;stroke:#8ba1b0;stroke-width:1.5;stroke-dasharray:5 4}.fir-spectrum-selection-svg .label{fill:#243746;font:16px "Microsoft YaHei",sans-serif}.fir-spectrum-selection-svg .caption{fill:#486d8b;font:15px "Microsoft YaHei",sans-serif}.fir-spectrum-selection-svg .passband{fill:#fff8df;stroke:none}
.iir-route-svg .box{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.iir-route-svg .method{fill:#fff8df;stroke:#b08d57;stroke-width:2}.iir-route-svg .wire,.iir-plane-map-svg .axis,.iir-plane-map-svg .map-arrow{fill:none;stroke:#174b73;stroke-width:2.3}.iir-route-svg .wire,.iir-plane-map-svg .map-arrow{marker-end:url(#iir-arrow)}.iir-route-svg .label,.iir-plane-map-svg .label{fill:#243746;font:16px "Microsoft YaHei",sans-serif}.iir-route-svg .caption,.iir-plane-map-svg .caption{fill:#486d8b;font:14px "Microsoft YaHei",sans-serif}.iir-plane-map-svg .stable{fill:#e6f4f3;stroke:none}.iir-plane-map-svg .unit{fill:none;stroke:#8ba1b0;stroke-width:2}.iir-plane-map-svg .boundary{fill:none;stroke:#0d8794;stroke-width:2;stroke-dasharray:5 4}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.formula-wide{font-size:9pt}.mapping,.table{font-size:9.5pt}.chart-grid,.grid{grid-template-columns:1fr}}
</style>
"""


def _main_body(html: str) -> str:
    match = re.search(r"<main(?:\s[^>]*)?>(.*)</main>", html, flags=re.DOTALL)
    if not match:
        raise ValueError("main-body component is missing its main container")
    return match.group(1)


def _render_component_bodies(components: tuple, directory: Path) -> str:
    bodies = []
    for component in components:
        path = component.write_html(directory / f"{component.__name__.split('.')[-1]}.html")
        bodies.append(_main_body(path.read_text(encoding="utf-8")))
    return "\n".join(bodies)


def _demote_headings(body: str) -> str:
    def replace(match: re.Match[str]) -> str:
        closing, level = match.group(1), int(match.group(2))
        return f"<{closing}h{level + 1}>"

    return re.sub(r"<(/?)h([1-3])>", replace, body)


def _keep_first_heading_as_chapter_title(body: str) -> str:
    match = re.search(r"<h1>.*?</h1>", body, flags=re.DOTALL)
    if not match:
        raise ValueError("chapter body is missing its chapter title")
    return f"{match.group(0)}{_demote_headings(body[match.end():])}"


def _with_chapter_title(title: str, body: str) -> str:
    return f"<h1>{title}</h1>{_demote_headings(body)}"


def _formula_name(formula: str, heading: str) -> str:
    """Return a reader-facing name that says what a core formula is used for."""
    compact = re.sub(r"\s+", "", formula).replace(r"\geq", r"\ge").replace(r"\leq", r"\le")
    if "x(n)=x_a(nT)" in compact:
        return "连续信号的离散采样关系（用于把连续时间信号转为离散序列）"
    if "f_s\\ge2f_h" in compact:
        return "奈奎斯特采样条件（用于确定避免频谱混叠的最低采样频率）"
    if "X_s(j\\Omega)" in compact and "\\sum" in compact:
        return "周期冲激采样的频谱复制关系（用于判断采样后频谱副本的位置和间隔）"
    if "X(e^{j\\omega})" in compact and "\\frac{1}{T}" in compact and "\\sum" in compact:
        return "连续时间频谱到离散时间频谱的映射关系（用于把模拟频谱换算到数字频域）"
    if "W(e^{j\\omega})=X(e^{j(\\omega-\\pi)})" in compact:
        return "离散时间频移关系（用于说明时域交替变号会使频谱平移 π）"
    if "Y(e^{j\\omega})" in compact and "\\begin{cases}" in compact:
        return "滤波后的输出频谱（用于给出通带内外的频谱幅度）"
    if "\\Deltaf_0" in compact and "f_s=2\\Deltaf_0" in compact:
        return "采样频率的可行性条件（用于判断哪些采样频率不会产生频谱混叠）"
    if "H_r(j\\Omega)" in compact and "\\begin{cases}" in compact:
        return "理想低通重构滤波器的频率响应（用于保留中心频谱副本并抑制其他副本）"
    if "h_r(t)=" in compact and "\\sin" in compact:
        return "理想低通重构滤波器的冲激响应（用于在时域实现理想低通重构）"
    if "44100" in compact and "f_s" in compact:
        return "不同采样率下的可保留频率（用于比较采样率降低对信号细节的影响）"
    if "E_x=" in compact and "\\int" in compact:
        return "能量信号的频域能量关系（用于由频谱判定信号能量是否有限）"
    if "X^*(e^{j\\omega})=X(e^{-j\\omega})" in compact:
        return "实序列频谱的共轭对称关系（用于由正频率部分判断负频率部分）"
    if "\\left|z\\right|=1" in compact and "ROC" in compact:
        return "BIBO 稳定性的 ROC 条件（用于判断收敛域是否包含单位圆）"
    if "\\left|a\\right|\\ne1" in compact and "\\left|b\\right|\\ne1" in compact:
        return "极点避开单位圆的条件（用于排除单位圆上的极点）"
    if "H(e^{j\\omega})" in compact:
        return "系统的频率响应表达式（用于求系统对各频率分量的幅度和相位作用）"
    if "H(z)=\\frac{Y(z)}{X(z)}" in compact or "H(z)=\\mathcal{Z}" in compact:
        return "系统函数的定义（用于在 z 域描述输入与输出的关系）"
    if "h(n)=0" in compact and "n<0" in compact:
        return "因果系统的单位脉冲响应条件（用于判断系统是否只依赖当前和过去输入）"
    if "\\sum" in compact and "|h(n)|" in compact and "\\infty" in compact:
        return "BIBO 稳定性判据（用于判断有界输入是否产生有界输出）"
    if "y(n)" in compact and ("y(n-1)" in compact or "y(n-2)" in compact):
        return "线性常系数差分方程（用于由输入和历史输出递推计算当前输出）"
    if "X[k]=" in compact and "W_N" in compact and "\\sum" in compact:
        return "离散傅里叶变换定义（用于把有限长序列分解为离散频率分量）"
    if "x[n]=" in compact and "X[k]" in compact and "\\sum" in compact:
        return "离散傅里叶反变换定义（用于由离散频谱重建时域序列）"
    if "W_N" in compact and "=" in compact:
        return "DFT 旋转因子关系（用于统一表示 DFT 中的复指数基函数）"
    if "\\{" in compact and ("x_" in compact or "x(n)" in compact):
        return "离散序列的数列表达（用于列出各离散时刻的样值）"
    if "\\delta" in compact and "\\begin{cases}" in compact:
        return "单位脉冲序列的定义（用于表示仅在指定时刻取非零值的离散序列）"
    if "\\omega=2\\tan^{-1}" in compact:
        return "双线性变换的频率映射关系（用于把模拟角频率映射到数字角频率）"
    if "\\int" in compact and "e^{-j\\omega" in compact:
        return "连续时间傅里叶变换定义（用于把时域连续信号变换到频域）"
    if "\\sum" in compact and "e^{-j\\omega" in compact:
        return "离散时间傅里叶变换定义（用于把离散序列变换到连续频率域）"
    if "\\sum" in compact and "z^{-" in compact:
        return "z 变换定义（用于把离散序列表示为 z 域函数）"
    if "\\mathcal{L}" in compact or ("\\int" in compact and "e^{-st}" in compact):
        return "拉普拉斯变换定义（用于把连续时间信号表示为 s 域函数）"
    if "\\int" in compact:
        return "连续时间积分关系（用于按连续变量累计各部分贡献）"
    if "y(n)" in compact and "\\sum" in compact:
        return "离散卷积和（用于由输入和单位脉冲响应计算输出序列）"
    if "\\sum" in compact:
        return "离散时间求和关系（用于把各离散分量累加为所需结果）"
    topic = re.sub(r"^第[一二三四五六七八九十0-9]+章\s*", "", heading)
    topic = re.sub(r"^\d+(?:\.\d+)*\s*", "", topic)
    topic = re.sub(r"^\d{4}\s*年真题\s*[：:]\s*", "", topic)
    topic = topic.replace("（续）", "").replace("(续)", "").strip(" ：:")
    semantic_topics = (
        (("DFT", "基本性质"), "DFT 基本性质关系（用于根据时域运算快速推导对应的频域结果）"),
        (("表示",), "离散序列表示式（用于明确各离散时刻的样值或函数表达）"),
        (("和与积",), "序列逐项运算关系（用于计算两序列相加或相乘后的结果）"),
        (("回声",), "延时叠加系统表达式（用于表示各次回声的延迟和衰减）"),
        (("反褶",), "序列反褶关系（用于把序列按指定原点镜像翻转）"),
        (("差分",), "序列差分关系（用于由相邻样值求序列的变化量）"),
        (("阶跃",), "单位阶跃序列定义（用于表示从指定时刻开始的序列）"),
        (("矩形",), "矩形序列定义（用于表示有限时长的离散脉冲）"),
        (("实指数",), "实指数序列定义（用于描述按等比规律变化的序列）"),
        (("正弦",), "离散正弦序列定义（用于描述离散周期振荡分量）"),
        (("复指数",), "离散复指数序列定义（用于表示幅度变化和相位旋转）"),
        (("周期",), "离散序列周期条件（用于判定序列是否按固定间隔重复）"),
        (("调幅",), "调幅序列频率关系（用于确定调制后产生的频率分量）"),
        (("线性",), "系统线性条件（用于检验系统是否满足叠加原理）"),
        (("移不变",), "系统时移不变条件（用于检验输入时移是否等效为输出同样时移）"),
        (("卷积",), "离散卷积计算式（用于由两个序列求其卷积结果）"),
        (("因果",), "系统因果性条件（用于判断输出是否只依赖当前和过去输入）"),
        (("稳定",), "系统稳定性条件（用于判断有界输入能否产生有界输出）"),
        (("混叠",), "频谱混叠判别关系（用于判断采样后频谱副本是否发生重叠）"),
        (("采样",), "采样参数关系（用于确定采样条件或由样值恢复信号）"),
        (("重构",), "信号重构关系（用于由离散样值恢复连续时间信号）"),
        (("傅里叶",), "傅里叶变换关系（用于建立时域与频域之间的对应）"),
        (("DTFT",), "离散时间傅里叶变换关系（用于建立离散序列与连续频率谱的对应）"),
        (("z 变换",), "z 变换关系（用于在 z 域分析离散序列或离散系统）"),
        (("拉普拉斯",), "拉普拉斯变换关系（用于在 s 域分析连续时间信号或系统）"),
        (("频率响应",), "系统频率响应关系（用于求系统对各频率分量的幅度和相位作用）"),
        (("零极点",), "零极点与系统特性关系（用于由零极点位置判断系统性质）"),
        (("滤波器",), "滤波器设计关系（用于由设计指标求滤波器参数或响应）"),
        (("FIR",), "FIR 滤波器关系（用于分析或设计有限长单位脉冲响应滤波器）"),
        (("IIR",), "IIR 滤波器关系（用于分析或设计递归数字滤波器）"),
        (("抽取",), "抽取处理关系（用于降低采样率并控制频谱混叠）"),
        (("内插",), "内插处理关系（用于提高采样率并补入新的样值）"),
        (("FFT",), "快速傅里叶变换关系（用于降低 DFT 的计算量）"),
        (("蝶形",), "FFT 蝶形运算关系（用于按级完成 DFT 的分解计算）"),
    )
    for keywords, label in semantic_topics:
        if all(keyword in topic for keyword in keywords):
            return label
    if topic and topic not in {"真题整理详解", "本章公式总表", "例题", "解", "反例"}:
        return f"{topic}的计算表达式（用于根据本节已知条件求出所需结果）"
    return "已知条件的计算表达式（用于代入题设数据并求得目标量）"


def _formula_summary(body: str) -> str:
    """Collect each chapter's reader-visible formulas for its closing reference."""
    # SVG labels are figure annotations, not standalone chapter formulas.  The
    # surrounding text and formula blocks remain part of the summary source.
    text = re.sub(r"<svg\b.*?</svg>", "", body, flags=re.DOTALL)
    tokens = re.compile(
        r"<h[1-4](?:\s[^>]*)?>(?P<heading>.*?)</h[1-4]>|"
        r"\\\[(?P<display>.*?)\\\]",
        flags=re.DOTALL,
    )
    formulas: list[tuple[str, str]] = []
    seen: set[str] = set()
    heading = "本章核心"
    for token in tokens.finditer(text):
        if token.group("heading") is not None:
            heading = re.sub(r"<[^>]+>", "", token.group("heading")).strip() or heading
            continue
        formula = token.group("display")
        normalized = re.sub(r"\s+", " ", formula).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        formulas.append((normalized, _formula_name(normalized, heading)))
    if not formulas:
        raise ValueError("chapter body contains no extractable formulas")
    formula_blocks = "\n".join(
        f'<p class="formula-name">{label}：</p>'
        f'<div class="formula">\\[\n{formula}\n\\]</div>'
        for formula, label in formulas
    )
    return (
        '<section class="chapter-formula-summary"><h2>本章公式总表</h2>'
        '<p>以下汇总本章正文中出现的公式；重复公式仅列一次。</p>'
        f"{formula_blocks}</section>"
    )


def _chapters() -> list[str]:
    with tempfile.TemporaryDirectory(prefix="dsp-all-main-body-") as directory:
        temporary = Path(directory)
        chapter_one_path = chapter_one.write_html(temporary / "chapter-one.html")
        chapter_two_path = chapter_two.write_html(temporary / "chapter-two.html")
        raw = [
            _main_body(chapter_one_path.read_text(encoding="utf-8")),
            _main_body(chapter_two_path.read_text(encoding="utf-8")),
            _render_component_bodies(
                (
                    chapter_three_overview,
                    chapter_three_dfs,
                    chapter_three_dft,
                    chapter_three_lsi_output,
                    chapter_three_frequency_sampling,
                    chapter_three_spectrum,
                ),
                temporary,
            ),
            _render_component_bodies(
                (chapter_four_efficiency, chapter_four_dit, chapter_four_dif_ifft),
                temporary,
            ),
            _render_component_bodies((chapter_five,), temporary),
            _render_component_bodies((chapter_six,), temporary),
            _render_component_bodies((chapter_seven,), temporary),
            _render_component_bodies((chapter_eight,), temporary),
        ]
    raw[0] = _keep_first_heading_as_chapter_title(raw[0])
    raw[2] = _keep_first_heading_as_chapter_title(raw[2])
    raw[3] = _with_chapter_title("第四章 快速傅里叶变换", raw[3])
    return [f"{body}{_formula_summary(body)}" for body in raw]


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    chapters = "\n".join(
        f'<section class="chapter-start">{body}</section>' for body in _chapters()
    )
    document = (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}<body><main>{chapters}</main></body></html>'
    )
    output.write_text(document, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "dsp_main_body.html"))
