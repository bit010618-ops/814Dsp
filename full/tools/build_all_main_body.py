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
.table{break-inside:auto}
.table tr{break-inside:avoid}
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
    if "g(0)=1" in compact and "g(kT)=0" in compact and "k\\in\\mathbb{Z}" in compact:
        return "插值函数的抽样性质（用于保证每个重构样点只保留对应的插值项）"
    if "y_a(mT)=x_a(mT)" in compact:
        return "重构信号的插值一致性（用于验证恢复信号准确通过全部采样值）"
    if "x(n)=A\\cos\\left(\\frac{3\\pi}{7}n\\right)" in compact and "N=14" in compact:
        return "离散正弦序列的周期求解（用于由角频率的有理比确定基本周期）"
    if "T[x(n-k)]=y(n-k)" in compact and "y(n)=T[x(n)]" not in compact:
        return "时不变系统的时移检验式（用于比较输入时移前后的输出是否同步平移）"
    if "y(n)=3\\delta(n)+8\\delta(n-1)+5\\delta(n-2)+2\\delta(n-3)" in compact:
        return "离散卷积的输出序列（用于列出各输出时刻的卷积结果）"
    if "x(n)*[\\delta(n)+\\alpha\\delta(n-R)]" in compact and "x(n)+\\alphax(n-R)" in compact:
        return "双抽头回声系统的输入输出关系（用于表示原信号与延迟衰减副本的叠加）"
    if "y(n)\\longrightarrowy_0(t)\\longrightarrowy_a(t)" in compact:
        return "数模转换与零阶保持流程（用于说明离散输出经保持和重构得到连续信号）"
    if "\\sin(2100\\pit)" in compact and "\\sin(2.1\\pin)=\\sin(0.1\\pin)" in compact:
        return "采样混叠的等效离散正弦关系（用于说明高频连续信号可产生相同离散样值）"
    if "f_h\\le\\frac{f_s}{2}" in compact and "\\Omega_h\\le\\frac{\\Omega_s}{2}" in compact:
        return "带限信号的无混叠采样条件（用于由最高频率确定最低采样率）"
    if "f_0=f_h-\\frac{\\Deltaf_0}{2}" in compact:
        return "带通信号的中心频率（用于由最高频率和带宽确定频带位置）"
    if "T\\downarrow" in compact and "f_s=\\frac{1}{T}\\uparrow" in compact:
        return "采样间隔与采样率的倒数关系（用于说明缩短采样间隔会提高采样率）"
    if "T_0=NT" in compact and "F_0=\\frac{1}{T_0}" in compact and "f_s=NF_0" in compact:
        return "记录长度与频率分辨率关系（用于由样本数和采样周期确定频率间隔）"
    if "X(k)=X\\left(e^{j\\omega}\\right)" in compact and "\\omega=\\frac{2\\pik}{N}" in compact:
        return "DFT 的等间隔频率取样关系（用于确定每个 DFT 样值在 DTFT 上的频率位置）"
    if "\\widetilde{x}(n)=x(n)" in compact and "N\\geM" in compact:
        return "零填充的无时域混叠条件（用于保证周期延拓副本不重叠）"
    if "F_s'=\\frac{L}{M}F_s" in compact:
        return "有理数倍采样率变换关系（用于计算变换后的采样率）"
    if "H\\!\\left(e^{j\\omega}\\right)=\\begin{cases}L" in compact and "\\omega_c=\\min" in compact:
        return "有理数倍变换的抗影像抗混叠滤波器（用于同时限制上采样影像和下采样混叠）"
    if "\\frac{147}{160}=\\frac{7}{8}\\cdot\\frac{7}{5}\\cdot\\frac{3}{4}" in compact:
        return "多级有理数倍分解（用于把总采样率变换拆为低复杂度级联）"
    if "44100=294\\cdot50\\cdot3" in compact and "44056=245\\cdot59.94\\cdot3" in compact:
        return "44.1 kHz 的制式分解（用于说明采样率与 PAL、NTSC 扫描体制的匹配）"
    if "\\frac{2\\pi}{\\omega}=\\frac{N}{k}" in compact and "\\gcd(N,k)=1" in compact:
        return "离散正弦序列的周期判定条件（用于求最小整数周期）"
    if "T[x_1(n)+x_2(n)]=T[x_1(n)]+T[x_2(n)]" in compact:
        return "系统线性的可加性条件（用于检验两个输入之和的输出）"
    if "T[ax_1(n)]=aT[x_1(n)]" in compact:
        return "系统线性的齐次性条件（用于检验输入缩放后的输出）"
    if "T[ax_1(n)+bx_2(n)]=ay_1(n)+by_2(n)" in compact:
        return "系统线性的叠加原理（用于同时检验可加性和齐次性）"
    if "y(n)=T[x(n)]" in compact and "T[x(n-k)]=y(n-k)" in compact and "\\forallk" in compact:
        return "时不变系统的时移关系（用于检验输入时移是否引起同样的输出时移）"
    if "x(n)*\\delta(n-n_0)=x(n-n_0)" in compact:
        return "单位脉冲卷积的时移性质（用于快速得到序列与移位冲激的卷积结果）"
    if "x(n)*h(n)=h(n)*x(n)" in compact:
        return "卷积的交换律（用于交换两个卷积序列的计算次序）"
    if "x(n)*h_1(n)" in compact and "*h_2(n)=x(n)*" in compact and "h_1(n)*h_2(n)" in compact:
        return "卷积的结合律（用于改变多级系统的级联分组）"
    if "x(n)*[h_1(n)+h_2(n)]=x(n)*h_1(n)+x(n)*h_2(n)" in compact:
        return "卷积的分配律（用于展开并联支路的总输出）"
    if "r_{xy}(n)=x(n)*y(-n)" in compact and "r_{yx}(n)=y(n)*x(-n)" in compact:
        return "互相关的卷积表示（用于计算两个序列不同移位下的相似度）"
    if "r_{xx}(n)=x(n)*x(-n)" in compact:
        return "自相关的卷积表示（用于衡量序列与其时移副本的相似度）"
    if "\\omega=\\OmegaT=2\\pi\\frac{f}{f_s}" in compact:
        return "模拟频率与数字频率的换算关系（用于把赫兹或模拟角频率换算为数字角频率）"
    if "x_a(t)\\longrightarrowx(n)\\longrightarrowy(n)\\longrightarrowy_a(t)" in compact:
        return "模拟信号的数字处理链（用于表示采样、数字处理和重构的先后顺序）"
    if "\\Omega_s\\ge2\\Omega_c" in compact and "f_s=\\frac{1}{T}" in compact:
        return "抗混叠采样条件与采样率定义（用于设置模数转换前的滤波和采样参数）"
    if "DFT" in heading and "IDFT" in heading and "x(n)=" in compact and "X(k)" in compact and "\\sum" in compact:
        return "离散傅里叶反变换定义（用于由离散频谱重建周期序列）"
    if "DFS" in heading and "变换对" in heading and "x(n)=" in compact and "a_k" in compact:
        return "离散傅里叶级数综合式（用于由周期序列的频域系数恢复时域波形）"
    if "DFS" in heading and "基本性质" in heading and "a_k=" in compact and "\\sum" in compact:
        return "离散傅里叶级数分析式（用于计算周期序列的频域系数）"
    if "重叠保留法" in heading and "\\operatorname{IDFT}" in compact:
        return "重叠保留法的块卷积输出（用于用 DFT 分块实现长序列线性卷积）"
    if "DTMF" in heading and "\\cos" in compact:
        return "双音多频信号的合成表达式（用于由两个标准音频分量构造按键音）"
    if "f_s\\ge2f_h" in compact:
        return "奈奎斯特采样条件（用于确定避免频谱混叠的最低采样频率）"
    if "X_s(j\\Omega)" in compact and "\\sum" in compact:
        return "周期冲激采样的频谱复制关系（用于判断采样后频谱副本的位置和间隔）"
    if "F_s(j\\Omega)" in compact and "\\sum" in compact:
        return "周期冲激采样的频谱复制关系（用于确定采样后频谱副本的位置和间隔）"
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
    if "H(\\Omega)" in compact and "\\begin{cases}" in compact:
        return "理想低通滤波器的频率响应（用于保留目标频带并抑制其余频谱副本）"
    if "h_r(t)=" in compact and "\\sin" in compact:
        return "理想低通重构滤波器的冲激响应（用于在时域实现理想低通重构）"
    if "44100" in compact and "f_s" in compact:
        return "不同采样率下的可保留频率（用于比较采样率降低对信号细节的影响）"
    if "E_x=" in compact and "\\int" in compact:
        return "能量信号的频域能量关系（用于由频谱判定信号能量是否有限）"
    if "w_C(n)=\\begin{cases}" in compact and "\\cos" in compact and "h(n)=h_d(n)w_C(n)" in compact:
        return "余弦（Hann）窗系数（用于对理想冲激响应加窗以抑制频谱泄漏）"
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
    if "H(z)=\\pmz^{-(N-1)}H\\!\\left(z^{-1}\\right)" in compact:
        return "FIR 系统函数的倒数对称关系（用于由零点镜像结构判断线性相位特性）"
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
    if "H(k)=" in compact and "\\begin{cases}" in compact:
        return "频率采样设计的目标样值（用于指定各离散频率点的幅度和相位）"
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
    if "y(n)=x^2(n)" in compact:
        return "非线性系统示例（用于说明平方运算不满足叠加原理）"
    if "T[ax_1+bx_2]" in compact and "x_1x_2" in compact:
        return "非线性系统的叠加检验（用于展开平方运算中的交叉项）"
    if "T[ax_1+bx_2]\\ne" in compact:
        return "非线性系统的判定结论（用于说明输出不等于各输入响应的线性组合）"
    if "T[x_1]=1" in compact and "T[x_2]=1" in compact and "T[x_1]+T[x_2]=2" in compact:
        return "非线性反例的输出和（用于比较两个输入响应相加的结果）"
    if "T[x_1+x_2]\\neT[x_1]+T[x_2]" in compact:
        return "非线性系统的叠加判定（用于通过输出和的不一致证明系统不满足线性）"
    if "T[ax_1(n)+bx_2(n)]" in compact and "x_1(-n)" in compact:
        return "时反系统的线性检验（用于验证时反运算满足叠加原理）"
    if "\\operatorname{Mid}" in compact:
        return "中值滤波系统表达式（用于说明中值运算通常不满足线性叠加）"
    if "\\mathcal{Z}\\{x(n-m)\\}" in compact:
        return "z 变换的时移性质（用于由原序列的 z 变换求时移序列的 z 变换）"
    if "\\mathcal{Z}\\{\\delta(n)\\}" in compact:
        return "单位脉冲序列的 z 变换（用于建立冲激及其移位的 z 域基本对）"
    if ("x(n)=\\cos(\\omega_0n)u(n)" in compact or "x(n)&=\\cos(\\omega_0n)u(n)" in compact) and "X(z)" in compact:
        return "因果余弦序列的 z 变换（用于求含单位阶跃余弦序列的系统函数）"
    if "X(z)=1+z^{-1}+z^{-2}" in compact:
        return "有限长序列的 z 变换（用于给出有限序列及其收敛域）"
    if "ax_1(n)+bx_2(n)" in compact and "aX_1(k)+bX_2(k)" in compact:
        return "DFT 的线性性质（用于将时域线性组合直接映射到频域）"
    if "x\\left((n-n_0)\\right)_N" in compact and "W_N^{kn_0}" in compact:
        return "DFT 的循环时移性质（用于由循环移位后的序列快速得到频谱相位因子）"
    if "W_N^{-nk_0}x(n)" in compact and "X\\left((k-k_0)\\right)_N" in compact:
        return "DFT 的调制性质（用于由时域复指数调制得到频域循环移位）"
    if "N\\geN_1+N_2-1" in compact:
        return "线性卷积的零填充长度条件（用于避免 DFT 计算时产生时域混叠）"
    if "\\operatorname{IDFT}_N\\{X(k)H(k)\\}" in compact:
        return "循环卷积定理（用于由频域相乘和 IDFT 得到 N 点循环卷积）"
    if "z_k=A_0W_0^{-k}" in compact and "e^{jk\\varphi_0}" in compact:
        return "Chirp-Z 变换的取样点参数式（用于在 z 平面指定螺旋或圆弧取样路径）"
    if "H(z)=\\left(1-ae^{j\\theta}z^{-1}\\right)\\left(1-ae^{-j\\theta}z^{-1}\\right)" in compact:
        return "二阶 FIR 的零点因式分解（用于由因子直接确定共轭零点位置）"
    if "y(n)=x(n)-2a\\cos\\theta\\,x(n-1)+a^2x(n-2)" in compact:
        return "二阶 FIR 的差分方程（用于按当前与延迟输入计算滤波器输出）"
    if "h(n)=h(N-1-n)" in compact and "h(n)=-h(N-1-n)" in compact:
        return "线性相位 FIR 的对称类型（用于区分偶对称和奇对称的冲激响应）"
    if ("h(n)=\\delta(n-\\tau)" in compact or "h(n)&=\\delta(n-\\tau)" in compact) and "\\tau_g" in compact:
        return "理想延时系统的线性相位关系（用于说明群延迟等于固定延时时间）"
    if "H\\!\\left(e^{j\\omega}\\right)&=\\pm" in compact and "\\theta(\\omega)" in compact:
        return "线性相位频率响应形式（用于区分两类线性相位的相位函数）"
    if "\\tau=\\frac{N-1}{2}" in compact and "h(n)=h(N-1-n)" in compact:
        return "偶对称 FIR 的群延迟关系（用于确定线性相位滤波器的固定延时）"
    if "h(n)=\\pmh(N-1-n)" in compact:
        return "线性相位 FIR 的对称条件（用于判定有限长滤波器能否具有线性相位）"
    if "h(n)=3\\delta(n)+2\\delta(n-1)+\\delta(n-2)" in compact:
        return "有限长单位脉冲响应（用于列出 FIR 系统各延时抽头的权重）"
    if "x(n)=\\delta(n)+2\\delta(n-1)" in compact:
        return "冲激输入序列（用于给出由若干移位冲激组成的输入信号）"
    if "h_e(n)=\\delta(n)+\\frac{1}{2}\\delta(n-1)+\\frac{1}{2}\\delta(n+1)" in compact:
        return "单位脉冲响应的偶分量（用于分解并检查冲激响应的对称性）"
    if "h(n)=h_e(n)+h_o(n)=\\delta(n)+\\delta(n-1)" in compact:
        return "偶奇分量重构关系（用于由偶分量和奇分量恢复原序列）"
    if "h(-1)=\\frac{1}{3}\\ne0" in compact:
        return "因果性反例判据（用于由负时刻冲激响应非零判定系统非因果）"
    if "H(z)=\\frac{1}{3}\\left(z+1+z^{-1}\\right)" in compact:
        return "对称 FIR 的系统函数（用于由抽头系数求 z 域表达式）"
    if "\\operatorname{ROC}:" in compact and "0<\\left|z\\right|<\\infty" in compact:
        return "有限长序列的收敛域（用于说明 z 变换在非零有限 z 平面内收敛）"
    if "H(z)=\\frac{1+z^{-1}}{1+0.2z^{-1}-0.24z^{-2}}" in compact:
        return "有理系统函数的零极点分解（用于直接读出系统零点和极点位置）"
    if "h(n)=\\left(\\frac{7}{5}\\,0.4^n-\\frac{2}{5}(-0.6)^n\\right)u(n)" in compact:
        return "部分分式反变换结果（用于由极点展开得到因果单位脉冲响应）"
    if "x(t)=\\sin(2\\pi\\cdot10t)+\\sin(2\\pi\\cdot250t)" in compact:
        return "双频连续时间输入信号（用于确定采样前各正弦分量的频率）"
    if "\\omega_1=2\\pi\\frac{10}{1000}" in compact and "\\omega_2=2\\pi\\frac{250}{1000}" in compact:
        return "模拟频率的数字归一化（用于把赫兹频率换算为离散角频率）"
    if "0.0628" in compact and "\\omega_c" in compact and "0.5\\pi" in compact:
        return "低通截止频率选取范围（用于在保留低频分量时抑制高频分量）"
    if "H(z)=G\\frac{z^2-1}{z^2+r^2}" in compact:
        return "二阶零极点滤波器结构（用于按零点和极点位置构造频率选择性滤波器）"
    if "H(z)=0.15\\frac{z^2-1}{z^2+0.7}" in compact:
        return "二阶滤波器的归一化系统函数（用于给出满足幅度约束后的实际增益）"
    if "\\omega_0=2\\pi\\frac{50}{1000}" in compact:
        return "干扰频率的数字归一化（用于把干扰的赫兹频率换算为数字角频率）"
    if "H(z)=\\frac{1}{3.9}\\frac{(z-e^{j\\omega_0})(z-e^{-j\\omega_0})}{z^2}" in compact:
        return "单位圆共轭零点的陷波器（用于在指定干扰频率及其共轭频率处置零）"
    if "H(z)=\\frac{(z-e^{j\\omega_0})(z-e^{-j\\omega_0})}{(z-re^{j\\omega_0})(z-re^{-j\\omega_0})}" in compact:
        return "二阶陷波器的零极点表达式（用于由极点半径控制陷波带宽）"
    if "\\frac{k}{N}=\\frac{\\omega}{2\\pi}=\\frac{f}{f_s}=\\frac{\\Omega}{\\Omega_s}" in compact:
        return "频率坐标换算关系（用于在 DFT 索引、数字频率和模拟频率之间换算）"
    if "H(z)=\\frac{1-3z^{-1}}{1-\\frac{3}{4}z^{-1}}" in compact:
        return "非最小相位系统函数（用于识别单位圆外零点并开始最小相位分解）"
    if "H_{\\min}(z)=3\\frac{z-\\frac{1}{3}}{z-\\frac{3}{4}}" in compact:
        return "最小相位因子（用于把单位圆外零点反射到单位圆内）"
    if "H_{\\mathrm{ap}}(z)=\\frac{z-3}{3z-1}" in compact and "H(z)=H_{\\min}(z)H_{\\mathrm{ap}}(z)" in compact:
        return "最小相位与全通分解（用于把系统分解为最小相位部分和全通部分）"
    if "\\widetilde{X}_8(0)=4" in compact and "\\widetilde{X}_8(7)" in compact:
        return "8 点 DFT 频谱样值（用于列出补零后各离散频率点的复幅度）"
    if "X_8(k)=X\\left(e^{j\\omega}\\right)" in compact and "X_{16}(k)=X\\left(e^{j\\omega}\\right)" in compact:
        return "补零后的频率采样关系（用于说明不同 DFT 长度在 DTFT 上的取样位置）"
    if "-0.3090\\pmj0.9511" in compact and "-0.8090\\pmj0.5878" in compact:
        return "单位圆频率采样点（用于标出 DFT 对应的复平面根点坐标）"
    if "p=\\frac{s^2+\\Omega_0^2}{Bs}" in compact:
        return "低通到带通的频率变换（用于由模拟低通原型构造带通滤波器）"
    if "h(n)=Te^{-nT}u(n)" in compact and "H(z)=\\frac{T}{1-e^{-T}z^{-1}}" in compact:
        return "冲激响应不变法的离散化结果（用于由模拟冲激响应构造数字 IIR 系统）"
    if "N-1=7" in compact and "\\tau=\\frac{N-1}{2}=3.5" in compact:
        return "线性相位 FIR 的长度与群延迟（用于由滤波器长度确定固定延时）"
    if ("\\omega_p=2\\pi\\frac{f_p}{f_s}" in compact or "\\omega_p&=2\\pi\\frac{f_p}{f_s}" in compact) and "\\Delta\\omega" in compact:
        return "FIR 设计的归一化频率指标（用于确定通带、阻带与过渡带宽度）"
    if "N=\\frac{6.6\\pi}{\\Delta\\omega}" in compact and "\\tau=\\frac{N-1}{2}" in compact:
        return "凯泽窗法的长度估计（用于由过渡带宽度确定 FIR 阶数）"
    if "h_d(n)=\\begin{cases}" in compact and "w_{\\mathrm{Ham}}(n)" in compact:
        return "窗函数法 FIR 系数（用于用哈明窗截断理想低通冲激响应）"
    if "\\sin\\!\\left[0.3\\pi(n-16)\\right]" in compact and "R_{33}(n)" in compact:
        return "33 阶哈明窗 FIR 系数（用于写出指定截止频率的实际滤波器抽头）"
    if "\\omega_c=\\frac{\\pi}{8}" in compact and "\\left|H_d\\!\\left(e^{j\\omega}\\right)\\right|=\\begin{cases}" in compact:
        return "理想低通目标响应（用于指定频率采样法设计的通带和阻带）"
    topic = re.sub(r"^第[一二三四五六七八九十0-9]+章\s*", "", heading)
    topic = re.sub(r"^第[一二三四五六七八九十0-9]+章\s*", "", heading)
    topic = re.sub(r"^\d+(?:\.\d+)*\s*", "", topic)
    topic = re.sub(r"^\d{4}\s*年真题\s*[：:]\s*", "", topic)
    topic = topic.replace("（续）", "").replace("(续)", "").strip(" ：:")
    semantic_topics = (
        (("数字谐振器",), "二阶数字谐振器的系统函数（用于在指定频率附近形成窄带共振）"),
        (("巴特沃斯低通原型",), "巴特沃斯低通原型的幅度平方响应（用于由截止频率和阶数确定平坦通带特性）"),
        (("脉冲响应不变法",), "脉冲响应不变法的离散化关系（用于由模拟冲激响应构造数字 IIR 滤波器）"),
        (("递归分解与运算量",), "IIR 滤波器的级联分解（用于把高阶递归滤波器实现为多个低阶节）"),
        (("频率采样法",), "频率采样设计的目标样值（用于指定各离散频率点的滤波器响应）"),
        (("DFT 与 IDFT",), "离散傅里叶反变换定义（用于由离散频谱重建周期序列）"),
        (("DFS 的变换对",), "离散傅里叶级数综合式（用于由周期序列的频域系数恢复时域波形）"),
        (("DFS 的基本性质",), "离散傅里叶级数分析式（用于计算周期序列的频域系数）"),
        (("重叠保留法",), "重叠保留法的块卷积输出（用于用 DFT 分块实现长序列线性卷积）"),
        (("系统函数及其与系统性质的关系",), "离散系统函数定义（用于在 z 域表示输入与输出的传递关系）"),
        (("折叠频率与三种频率",), "模拟、数字与归一化频率换算（用于统一采样系统中的频率坐标）"),
        (("有理函数的标准反变换对",), "有理 z 函数的部分分式展开（用于按 ROC 选择相应的时域反变换）"),
        (("DTMF 双音多频信号",), "双音多频信号的合成表达式（用于由两个标准音频分量构造按键音）"),
        (("z 反变换",), "z 反变换的围线积分定义（用于由 z 域函数恢复时域序列）"),
        (("部分分式展开法",), "部分分式展开的留数系数（用于把有理 z 函数拆成可直接反变换的简单项）"),
        (("共轭对称与分解",), "共轭对称分量分解（用于把任意序列拆为共轭对称与共轭反对称部分）"),
        (("实序列的频谱对称性",), "实序列频谱的共轭对称关系（用于由正频率谱确定负频率谱）"),
        (("四抽头平均", "零点分布"), "四抽头平均滤波器的零点位置（用于在 z 平面定位频率响应的零点）"),
        (("收敛域与典型序列",), "单极点 z 变换与收敛域关系（用于说明同一代数式在不同 ROC 下对应不同序列）"),
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
        (("双线性变换",), "双线性变换的频率映射关系（用于在模拟和数字频率之间建立非线性对应）"),
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
