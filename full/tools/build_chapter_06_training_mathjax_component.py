"""Chapter-six IIR transformation training and consolidated answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.exam-page{break-before:page;min-height:230mm}.exam-page:first-child{break-before:auto}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.writing-space{min-height:172mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}@media(max-width:560px){body{font-size:10.5pt}.writing-space{min-height:145mm}}
</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''


def _math(x: int, y: int, width: int, text: str) -> str:
    return (
        f'<foreignObject x="{x}" y="{y}" width="{width}" height="34">'
        f'<div xmlns="http://www.w3.org/1999/xhtml" style="font:17px serif;text-align:center">\\({text}\\)</div>'
        '</foreignObject>'
    )


def _parallel_iir_diagram() -> str:
    return f'''<svg data-diagram="impulse-invariance-parallel-iir" viewBox="0 0 900 330" role="img" aria-label="脉冲响应不变法 IIR 并联型结构图" style="display:block;width:100%;max-width:158mm;height:auto;margin:10pt auto">
<defs><marker id="parallel-iir-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#174b73"/></marker></defs>
<text x="450" y="32" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">脉冲响应不变法得到的 IIR 并联型结构</text>
<path d="M55 165H150V96H245" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#parallel-iir-arrow)"/>
<path d="M150 165V234H245" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#parallel-iir-arrow)"/>
<circle cx="150" cy="165" r="4.5" fill="#174b73"/>
<rect x="245" y="60" width="220" height="72" rx="7" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<rect x="245" y="198" width="220" height="72" rx="7" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M465 96H590V145H598" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#parallel-iir-arrow)"/>
<path d="M465 234H590V185H598" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#parallel-iir-arrow)"/>
<circle cx="632" cy="165" r="34" fill="#fff" stroke="#174b73" stroke-width="2.4"/>
<text x="632" y="173" text-anchor="middle" fill="#174b73" style="font:25px serif">Σ</text>
<path d="M666 165H838" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#parallel-iir-arrow)"/>
<text x="355" y="84" text-anchor="middle" fill="#486d8b" style="font:15px Microsoft YaHei,sans-serif">并联支路 1</text>
<text x="355" y="222" text-anchor="middle" fill="#486d8b" style="font:15px Microsoft YaHei,sans-serif">并联支路 2</text>
{_math(8,129,110,'x[n]')}{_math(258,90,194,'\\frac{1}{1-e^{-1}z^{-1}}')}{_math(258,228,194,'-\\frac{1}{1-e^{-3}z^{-1}}')}{_math(790,129,78,'y[n]')}
</svg>'''


def _direct_form_ii_diagram() -> str:
    return f'''<svg data-diagram="bilinear-direct-form-ii-iir" viewBox="0 0 940 450" role="img" aria-label="双线性变换 IIR 直接 II 型结构图" style="display:block;width:100%;max-width:160mm;height:auto;margin:10pt auto">
<defs><marker id="df2-iir-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0L8,4L0,8Z" fill="#174b73"/></marker></defs>
<text x="470" y="30" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">双线性变换得到的 IIR 直接 II 型结构</text>
<path d="M55 220H132" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#df2-iir-arrow)"/>
<circle cx="166" cy="220" r="33" fill="#fff" stroke="#174b73" stroke-width="2.4"/>
<text x="166" y="228" text-anchor="middle" fill="#174b73" style="font:25px serif">Σ</text>
<path d="M199 220H274" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#df2-iir-arrow)"/>
<rect x="274" y="188" width="84" height="64" rx="6" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M358 220H438" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#df2-iir-arrow)"/>
<rect x="438" y="188" width="84" height="64" rx="6" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M522 220H570" fill="none" stroke="#174b73" stroke-width="2.4"/>
<circle cx="226" cy="220" r="4.5" fill="#174b73"/>
<circle cx="398" cy="220" r="4.5" fill="#174b73"/>
<circle cx="560" cy="220" r="4.5" fill="#174b73"/>
<path d="M226 220V310H312" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
<rect x="312" y="284" width="80" height="52" rx="5" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M392 310H704" fill="none" stroke="#174b73" stroke-width="2.2"/>
<path d="M398 220V350H474" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
<rect x="474" y="324" width="80" height="52" rx="5" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M554 350H704" fill="none" stroke="#174b73" stroke-width="2.2"/>
<path d="M560 220V390H636" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
<rect x="636" y="364" width="80" height="52" rx="5" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M716 390V310H704" fill="none" stroke="#174b73" stroke-width="2.2"/>
<circle cx="740" cy="310" r="33" fill="#fff" stroke="#174b73" stroke-width="2.4"/>
<text x="740" y="318" text-anchor="middle" fill="#174b73" style="font:25px serif">Σ</text>
<path d="M773 310H875" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#df2-iir-arrow)"/>
<path d="M398 220V126H470" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
<rect x="470" y="100" width="84" height="52" rx="5" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M470 126H166V187" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
<path d="M560 220V70H634" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
<rect x="634" y="44" width="84" height="52" rx="5" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M634 70H96V220H133" fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#df2-iir-arrow)"/>
{_math(18,184,90,'x[n]')}{_math(286,204,60,'z^{-1}')}{_math(450,204,60,'z^{-1}')}{_math(324,292,56,'b_0=\\frac{2}{15}')}{_math(486,332,56,'b_1=\\frac{4}{15}')}{_math(648,372,56,'b_2=\\frac{2}{15}')}{_math(480,108,64,'\\frac{2}{15}')}{_math(644,52,64,'\\frac{1}{15}')}{_math(838,274,72,'y[n]')}
</svg>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第六章 分章强化训练</h1>
<div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>八、证明：时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统；反之亦真。（设定双线性变换为 \(s=\frac{2}{T}\frac{z-1}{z+1}\)）</p>
<div class="writing-space"></div></section>
<section class="exam-page">
<div class="exam-head"><span>2021 年真题</span><span>详解见 P.____</span></div>
<p>八、采用双线性变换法设计一个贝特沃斯低通滤波器，技术指标为：通带下限频率为 \(f_p\,\mathrm{Hz}\)，阻带上限为 \(f_s\,\mathrm{Hz}\)，通带最大衰减为 \(\alpha_p\,\mathrm{dB}\)，阻带最小衰减为 \(\alpha_s\,\mathrm{dB}\)，取样周期为 \(T\)，试写出设计的具体步骤。</p>
<div class="writing-space"></div></section>
<section class="exam-page">
<div class="exam-head"><span>2023 年真题</span><span>详解见 P.____</span></div>
<p>九、已知某模拟滤波器传递函数 \(H(s)=\frac{2}{s^2+4s+3}\)</p>
<p>（1）用脉冲响应不变法将其转化为数字滤波器，写出系统函数 \(H(z)\) 表达式，并画出 IIR 数字滤波器的并联型结构图（采样间隔取 \(T=1\)）。</p>
<p>（2）用双线性变换法将其转化为数字滤波器，写出 \(H(z)\) 表达式，并画出 IIR 数字滤波器的直接 II 型结构图（采样间隔取 \(T=1\)）。</p>
<p>（3）简述脉冲响应不变法和双线性变换法各自的特点。</p>
<div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>真题整理详解</h1>
<h2>2007 年真题</h2>
<p>八、证明：时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统；反之亦真。（设定双线性变换为 \(s=\frac{2}{T}\frac{z-1}{z+1}\)）</p>
<div class="answer-step"><strong>第 1 步：写出实部。</strong>双线性变换把 \(z\) 平面映射到 \(s\) 平面。将分子分母同乘 \(z^*+1\)，得到：</div>
<div class="formula">\[
\begin{aligned}
\operatorname{Re}\{s\}&=\frac{2}{T}\operatorname{Re}\left\{\frac{z-1}{z+1}\right\}\\
&=\frac{2}{T}\frac{\left|z\right|^2-1}{\left|z+1\right|^2}.
\end{aligned}
\]</div>
<div class="answer-step"><strong>第 2 步：比较稳定区域。</strong>采样周期 \(T>0\)，且对有限 \(z\ne-1\)，分母 \(\left|z+1\right|^2>0\)。因此实部的符号只由 \(\left|z\right|^2-1\) 决定：</div>
<div class="formula">\[
\operatorname{Re}\{s\}<0
\quad\Longleftrightarrow\quad
\left|z\right|<1.
\]</div>
<p>也就是说，连续时间系统的左半平面一一映射到离散系统的单位圆内；虚轴 \(\operatorname{Re}\{s\}=0\) 映射到单位圆 \(\left|z\right|=1\)。</p>
<div class="answer-step"><strong>第 3 步：由极点位置得出结论。</strong>连续时间有理系统稳定当且仅当全部极点位于左半平面。经上述映射后，这些极点全部落在单位圆内，因而所得离散系统稳定。反过来，若离散系统稳定，其全部极点在单位圆内，逆双线性变换把它们映射到左半平面，所以对应连续时间系统也稳定。故双线性变换保持稳定性，反之亦真。</div>
<h2>2021 年真题</h2>
<p>八、采用双线性变换法设计一个贝特沃斯低通滤波器，技术指标为：通带下限频率为 \(f_p\,\mathrm{Hz}\)，阻带上限为 \(f_s\,\mathrm{Hz}\)，通带最大衰减为 \(\alpha_p\,\mathrm{dB}\)，阻带最小衰减为 \(\alpha_s\,\mathrm{dB}\)，取样周期为 \(T\)，试写出设计的具体步骤。</p>
<div class="answer-step"><strong>第 1 步：把数字频率指标预畸变到模拟域。</strong>先把以 Hz 给出的边缘频率写成数字角频率 \(\omega_p=2\pi f_pT\)、\(\omega_s=2\pi f_sT\)，再由双线性变换的频率关系得到模拟低通原型的边缘频率：</div>
<div class="formula">\[
\begin{aligned}
\Omega_p&=\frac{2}{T}\tan\left(\frac{\omega_p}{2}\right)
=\frac{2}{T}\tan\left(\pi f_pT\right),\\
\Omega_s&=\frac{2}{T}\tan\left(\frac{\omega_s}{2}\right)
=\frac{2}{T}\tan\left(\pi f_sT\right).
\end{aligned}
\]</div>
<div class="answer-step"><strong>第 2 步：由衰减指标确定阶数。</strong>令 \(\epsilon^2=10^{\alpha_p/10}-1\)。巴特沃斯低通原型的幅度平方为 \(\left|H_a(j\Omega)\right|^2=\frac{1}{1+\epsilon^2\left(\Omega/\Omega_c\right)^{2N}}\)，所以最小整数阶数取为：</div>
<div class="formula">\[
N=\left\lceil
\frac{
\ln\!\left[
\dfrac{10^{\alpha_s/10}-1}{10^{\alpha_p/10}-1}
\right]
}{
2\ln\!\left(\Omega_s/\Omega_p\right)
}
\right\rceil.
\]</div>
<div class="answer-step"><strong>第 3 步：选截止频率并构成模拟原型。</strong>截止频率应满足通带与阻带约束：</div>
<div class="formula">\[
\frac{\Omega_p}{\left(10^{\alpha_p/10}-1\right)^{1/(2N)}}
\leq \Omega_c \leq
\frac{\Omega_s}{\left(10^{\alpha_s/10}-1\right)^{1/(2N)}}.
\]</div>
<p>在该区间内任选 \(\Omega_c\)，按 \(N\) 阶巴特沃斯极点表或由单位圆左半平面的等角极点构成分母 \(B_N(s)\)，得到：</p>
<div class="formula">\[
H_a(s)=\frac{\Omega_c^N}{B_N(s)}.
\]</div>
<div class="answer-step"><strong>第 4 步：实施双线性变换并整理。</strong>将 \(s=\frac{2}{T}\frac{z-1}{z+1}\) 代入模拟原型，通分、归一化分母常数项后即得所需数字 IIR 低通滤波器：</div>
<div class="formula">\[
H(z)=H_a\left(\frac{2}{T}\frac{z-1}{z+1}\right).
\]</div>
<p>最后将 \(H(z)\) 写成 \(z^{-1}\) 的有理式，读出差分方程系数；实现时可按二阶节级联，以减小有限字长误差。预畸变步骤保证双线性变换后在 \(f_p\)、\(f_s\) 处满足给定的通、阻带指标。</p>
<h2>2023 年真题</h2>
<p>九、已知某模拟滤波器传递函数 \(H(s)=\frac{2}{s^2+4s+3}\)</p>
<p>（1）用脉冲响应不变法将其转化为数字滤波器，写出系统函数 \(H(z)\) 表达式，并画出 IIR 数字滤波器的并联型结构图（采样间隔取 \(T=1\)）。</p>
<p>（2）用双线性变换法将其转化为数字滤波器，写出 \(H(z)\) 表达式，并画出 IIR 数字滤波器的直接 II 型结构图（采样间隔取 \(T=1\)）。</p>
<p>（3）简述脉冲响应不变法和双线性变换法各自的特点。</p>
<div class="answer-step"><strong>（1）脉冲响应不变法。</strong>先作部分分式展开：</div>
<div class="formula">\[
H(s)=\frac{2}{(s+1)(s+3)}
=\frac{1}{s+1}-\frac{1}{s+3}.
\]</div>
<p>故模拟冲激响应为 \(h_a(t)=\left(e^{-t}-e^{-3t}\right)u(t)\)。当 \(T=1\) 时，以 \(h[n]=h_a(nT)\) 取样，得到：</p>
<div class="formula">\[
\begin{aligned}
h[n]&=\left(e^{-n}-e^{-3n}\right)u[n],\\
H_{\mathrm{ii}}(z)&=\frac{1}{1-e^{-1}z^{-1}}-\frac{1}{1-e^{-3}z^{-1}}.
\end{aligned}
\]</div>
<p>两个一阶部分分别作为并联支路，第二支路带负号，输出在标准求和器相加：</p>
    <!-- impulse-invariance-parallel-iir -->
<div class="answer-step"><strong>（2）双线性变换法。</strong>对 \(T=1\)，代入 \(s=2\frac{z-1}{z+1}\)，再同除以 \(z^2\)，有：</div>
<div class="formula">\[
\begin{aligned}
H_{\mathrm{bl}}(z)
&=\frac{2(z+1)^2}{15z^2-2z-1}\\
&=\frac{2\left(1+2z^{-1}+z^{-2}\right)}
{15-2z^{-1}-z^{-2}}.
\end{aligned}
\]</div>
<p>将分母归一化后，直接 II 型的前向系数为 \(b_0=\frac{2}{15}\)、\(b_1=\frac{4}{15}\)、\(b_2=\frac{2}{15}\)，反馈接入系数为 \(\frac{2}{15}\)、\(\frac{1}{15}\)。共享两级延时，得到：</p>
    <!-- bilinear-direct-form-ii-iir -->
<div class="answer-step"><strong>（3）两种方法的特点。</strong>脉冲响应不变法在时域保留取样时刻的冲激响应样值，极点映射为 \(z_k=e^{s_kT}\)，但连续频率响应会按采样频率周期复制，可能产生频谱混叠，因此更适用于模拟原型的高频部分可忽略的情形。双线性变换将整个 \(j\Omega\) 轴一一映射到单位圆，不产生频谱混叠，但存在频率扭曲；通过设计前的预畸变，可使关键边缘频率精确对应。</div>
</main>
"""
    content = content.replace("<!-- impulse-invariance-parallel-iir -->", _parallel_iir_diagram())
    content = content.replace("<!-- bilinear-direct-form-ii-iir -->", _direct_form_ii_diagram())
    output.write_text(_document(content), encoding="utf-8")
    return output
