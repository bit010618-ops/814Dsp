"""Chapter-seven supplemental FIR training and consolidated answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import STYLE, _document


QUESTION_IDS = (
    "2007-q十-p1",
    "2007-q十二-whole",
    "2015-qintro-p8",
    "2016-q九-whole",
    "2017-q八-whole",
    "2019-q五-whole",
    "2021-q九-whole",
    "2024-fir-second",
)


def _math(x: int, y: int, width: int, text: str, height: int = 34) -> str:
    return (
        f'<foreignObject x="{x}" y="{y}" width="{width}" height="{height}">'
        f'<div xmlns="http://www.w3.org/1999/xhtml" '
        f'style="font:16px serif;text-align:center">\\({text}\\)</div>'
        '</foreignObject>'
    )


def _frequency_sampling_diagram() -> str:
    """Textbook-layout comb-plus-resonator-cabinet realization."""
    return f'''<svg class="structure-svg frequency-sampling-diagram" data-diagram="frequency-sampling-fir" viewBox="0 0 920 300" role="img" aria-label="频率采样型 FIR 的梳状滤波器与谐振器柜结构图">
<defs><marker id="fs-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#174b73"/></marker></defs>
<text x="460" y="32" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">频率采样型 FIR：梳状滤波器与谐振器柜</text>
<path d="M58 150H184" fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#fs-arrow)"/>
<rect x="184" y="105" width="176" height="90" rx="7" fill="#f4f7f8" stroke="#0d8794" stroke-width="2"/>
<path d="M360 150H455" fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#fs-arrow)"/>
<rect x="455" y="78" width="245" height="144" rx="7" fill="#f4f7f8" stroke="#0d8794" stroke-width="2"/>
<path d="M700 150H857" fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#fs-arrow)"/>
<text x="272" y="135" text-anchor="middle" fill="#315d7c" style="font:16px Microsoft YaHei,sans-serif">梳状滤波器</text>
<text x="578" y="122" text-anchor="middle" fill="#315d7c" style="font:16px Microsoft YaHei,sans-serif">N 个一阶谐振器并联</text>
<text x="578" y="157" text-anchor="middle" fill="#315d7c" style="font:16px Microsoft YaHei,sans-serif">组成谐振器柜</text>
{_math(14,105,90,'x(n)')}{_math(202,149,142,'H_1(z)=1-z^{-N}')}{_math(475,170,202,r'\frac{1}{N}\sum_{k=0}^{N-1}H_k(z)')}{_math(830,105,80,'y(n)')}
<text x="460" y="271" text-anchor="middle" fill="#52616b" style="font:14px Microsoft YaHei,sans-serif">梳状滤波器的单位圆零点与各谐振支路的极点逐一相消</text>
</svg>'''


def _frequency_sampling_target_plot() -> str:
    """Redraw the exact low-pass target plot from the source question."""
    return f'''<svg class="structure-svg frequency-sampling-diagram" data-diagram="frequency-sampling-target" viewBox="0 0 880 330" role="img" aria-label="频率采样设计题的理想幅度响应">
<defs><marker id="target-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#174b73"/></marker></defs>
<text x="440" y="28" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">理想幅度响应</text>
<line x1="125" y1="238" x2="790" y2="238" stroke="#174b73" stroke-width="2.4" marker-end="url(#target-arrow)"/>
<line x1="184" y1="270" x2="184" y2="62" stroke="#174b73" stroke-width="2.4" marker-end="url(#target-arrow)"/>
<path d="M184 102H398L505 238H738" fill="none" stroke="#0d8794" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="398" y1="102" x2="398" y2="238" stroke="#8294a0" stroke-width="1.5" stroke-dasharray="6 5"/>
<line x1="184" y1="238" x2="184" y2="251" stroke="#174b73" stroke-width="1.5"/>
<line x1="398" y1="238" x2="398" y2="251" stroke="#174b73" stroke-width="1.5"/>
<line x1="505" y1="238" x2="505" y2="251" stroke="#174b73" stroke-width="1.5"/>
<line x1="738" y1="238" x2="738" y2="251" stroke="#174b73" stroke-width="1.5"/>
{_math(140,240,78,'0')}{_math(365,248,84,'\\frac{\\pi}{5}')}{_math(461,248,92,'\\frac{3\\pi}{10}')}{_math(720,248,58,'\\pi')}{_math(128,76,48,'1')}{_math(153,46,70,'H_d(\\omega)')}{_math(796,215,44,'\\omega')}
<text x="440" y="306" text-anchor="middle" fill="#52616b" style="font:14px Microsoft YaHei,sans-serif">低频平坦区后接线性过渡带</text>
</svg>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第七章 补充真题</h1>
<div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>十、简答题</p>
<p>（1）用窗函数法设计 FIR 滤波器时，窗函数的长短和形状对滤波器性能产生什么样的影响？</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>十二、用频率采样法设计一类线性相位 FIR 滤波器 \(H(z)\)，采样点数 \(N=20\)，滤波器理想频率响应表示为：</p>
<div class="formula">\[
H_d(e^{j\omega})=H_d(\omega)e^{j\theta(\omega)},
\]
</div>
<p>其幅度特性如图所示：</p>
__FREQUENCY_SAMPLING_TARGET__
<p>（1）若频率采样值为 \(H(k)=H_g(k)e^{j\theta(k)}\)，求 \(H_g(k)\) 和 \(\theta(k)\)；</p>
<p>（2）根据频域内插公式写出 \(H(z)\) 的表达式，并用频域采样结构实现。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div>
<p>8. FIR 滤波器的单位采样响应 \(h(n)\) 是偶对称的 \(N=6\)，\(h(0)=h(5)=1.5\)，\(h(1)=h(4)=2\)，\(h(2)=h(3)=3\)，其幅度特性有什么特性？________；相位有什么特性？________。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2016 年真题</span><span>详解见 P.____</span></div>
<p>九、已知</p>
<div class="formula">\[
\left|H_d(e^{j\omega})\right|=
\begin{cases}
1,&\dfrac{\pi}{2}<\left|\omega\right|<\dfrac{3\pi}{2},\\
0,&\text{其他}.
\end{cases}
\]
</div>
<p>用 \(N=15\) 设计一类 FIR：</p>
<p>1. 求 \(H(k)\)；</p><p>2. 利用 \(N\) 点 \(H(k)\)，求 \(H(z)\)；</p><p>3. 画出频域采样型结构。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2017 年真题</span><span>详解见 P.____</span></div>
<p>八、用矩形窗设计一个低通滤波器，已知</p>
<div class="formula">\[
H_d(e^{j\omega})=
\begin{cases}
e^{-j\omega a},&0\le\left|\omega\right|\le\omega_c,\\
0,&\omega_c<\left|\omega\right|\le\pi.
\end{cases}
\]
</div>
<p>1. 求 \(h(n)\) 的表达式，确定 \(a\) 与 \(N\) 的关系；</p>
<p>2. 有几种类型？分别属于哪一种线性相位滤波器？</p>
<p>3. 若改用余弦窗设计，求出 \(h(n)\) 的表达式。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2019 年真题</span><span>详解见 P.____</span></div>
<p>五、设计 FIR 滤波器，</p>
<div class="formula">\[
H(z)=1-2a\cos\theta\,z^{-1}+a^2z^{-2}.
\]
</div>
<p>1. 求零极点；</p><p>2. 画出直接型；</p><p>3. \(a\) 为何值时，满足线性相位。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2021 年真题</span><span>详解见 P.____</span></div>
<p>九、FIR 滤波器。给出</p>
<div class="formula">\[
H(z)=1-2a\cos\theta\,z^{-1}+a^2z^{-2}.
\]
</div>
<p>1. 求零极点；</p><p>2. 画出直接型；</p><p>3. \(a\) 何值时，满足线性相位；</p><p>4. 若有一窄带干扰，主频率分量等于 \(\dfrac{\pi}{3}\) 弧度，要滤去这个干扰，滤波器的频率特性该如何设计？</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2024 年真题</span><span>详解见 P.____</span></div>
<p>八、已知某 2 阶 FIR 数字滤波器的系统函数为</p>
<div class="formula">\[
H(z)=1+az^{-1}+z^{-2}.
\]
</div>
<p>（1）设滤波器的幅度响应在 \(\omega=\dfrac{3\pi}{4}\) 处为 0，试求 \(H(z)\) 中的系数 \(a\)；</p>
<p>（2）若该滤波器的频率响应表示为 \(H(e^{j\omega})=H(\omega)e^{j\theta(\omega)}\)，试求系统的振幅响应 \(H(\omega)\) 及相位响应 \(\theta(\omega)\) 的表达式；</p>
<p>（3）该滤波器是否具有线性相位，如果是，请问该滤波器的延迟是多少？如果不是，请解释原因。</p>
<div class="writing-space"></div></section>
</main>
"""
    output.write_text(
        _document(content.replace("__FREQUENCY_SAMPLING_TARGET__", _frequency_sampling_target_plot())),
        encoding="utf-8",
    )
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解</h1>
<h2>2007 年真题：窗函数的长度与形状</h2>
<p>十、简答题（1）用窗函数法设计 FIR 滤波器时，窗函数的长短和形状对滤波器性能产生什么样的影响？</p>
<div class="answer-step"><strong>长度决定过渡带的主要尺度。</strong>把理想无限长响应截为有限长，相当于在频域用窗函数的主瓣作平滑。长度 \(N\) 增大时主瓣变窄，因此过渡带通常变窄、截止位置更接近理想指标；长度变短则主瓣变宽，过渡带变宽。</div>
<div class="answer-step"><strong>形状决定主瓣与旁瓣的权衡。</strong>矩形窗主瓣最窄但旁瓣最高，阻带纹波较大；海明、布莱克曼、凯泽等窗可降低旁瓣和阻带泄漏，但通常以更宽的主瓣、即更宽的过渡带为代价。故先用长度满足过渡带宽度，再按阻带衰减选窗形；两类指标不能只靠单独调一个参数同时任意改善。</div>
<h2>2007 年真题：频率采样法</h2>
<p>十二、用频率采样法设计一类线性相位 FIR 滤波器 \(H(z)\)，采样点数 \(N=20\)。</p>
<div class="answer-step"><strong>第 1 步：确定采样频率和幅度样值。</strong>频率样点为 \(\omega_k=2\pi k/N=k\pi/10\)。图中的线性过渡区恰在 \(\pi/5\) 与 \(3\pi/10\) 两个样点之间，因此没有非零的过渡采样值：</div>
<div class="formula">\[
H_g(k)=
\begin{cases}
1,&k=0,1,2,18,19,\\
0,&k=3,4,\ldots,17.
\end{cases}
\]
</div>
<div class="answer-step"><strong>第 2 步：写出线性相位样值。</strong>长度为 \(N=20\) 的对称因果 FIR 的中心位于 \((N-1)/2=19/2\)，所以可取</div>
<div class="formula">\[
\theta(k)=-\frac{N-1}{N}\pi k=-\frac{19\pi}{20}k,
\qquad H(k)=H_g(k)e^{j\theta(k)}.
\]
</div>
<div class="answer-step"><strong>第 3 步：由频域内插恢复系统函数。</strong>令 \(W_N=e^{-j2\pi/N}\)，频域采样内插式为</div>
<div class="formula">\[
H(z)=\frac{1-z^{-N}}{N}\sum_{k=0}^{N-1}\frac{H(k)}{1-W_N^{-k}z^{-1}},\qquad N=20.
\]
</div>
<p>因为只有 \(k=0,1,2,18,19\) 的样值非零，实际相加时只保留这五个谐振支路，其余支路系数为零。</p>
""" + _frequency_sampling_diagram() + r"""
<h2>2015 年真题：偶对称 FIR 的幅相特性</h2>
<p>8. FIR 滤波器的单位采样响应 \(h(n)\) 是偶对称的 \(N=6\)，\(h(0)=h(5)=1.5\)，\(h(1)=h(4)=2\)，\(h(2)=h(3)=3\)，其幅度特性有什么特性？________；相位有什么特性？________。</p>
<div class="answer-step"><strong>第 1 步：围绕对称中心配对。</strong>对称中心为 \(5/2\)，因此</div>
<div class="formula">\[
H(e^{j\omega})=e^{-j\frac{5}{2}\omega}
\left[3\cos\!\left(\frac{5\omega}{2}\right)+4\cos\!\left(\frac{3\omega}{2}\right)+6\cos\!\left(\frac{\omega}{2}\right)\right].
\]
</div>
<p>方括号内为实偶函数，故幅度响应 \(\left|H(e^{j\omega})\right|\) 是实偶函数，并以 \(2\pi\) 为周期；由于长度为偶数的偶对称 FIR 属于 II 型，它还满足 \(H(e^{j\pi})=0\)。</p>
<div class="answer-step"><strong>第 2 步：读出相位。</strong>在幅度不为零的频段，线性相位主项为 \(-5\omega/2\)；当实幅度因子变号时相位额外相差 \(\pi\)。群延迟恒为 \(5/2\) 个采样周期。</div>
<h2>2016 年真题：15 点频率采样设计</h2>
<p>九、已知 \(\left|H_d(e^{j\omega})\right|=1\)（\(\pi/2<|\omega|<3\pi/2\)），其他频率为 0，用 \(N=15\) 设计一类 FIR。</p>
<div class="answer-step"><strong>第 1 步：标出有效频率样点。</strong>样点为 \(\omega_k=2\pi k/15\)，线性相位延迟为 \((N-1)/2=7\)。在 \(0\le k\le14\) 的一个周期中，通带样点为 \(k=4,5,\ldots,11\)，因此</div>
<div class="formula">\[
H(k)=
\begin{cases}
e^{-j\frac{14\pi}{15}k},&k=4,5,\ldots,11,\\
0,&k=0,1,2,3,12,13,14.
\end{cases}
\]
</div>
<div class="answer-step"><strong>第 2 步：写出 \(H(z)\)。</strong>代入频域内插公式：</div>
<div class="formula">\[
H(z)=\frac{1-z^{-15}}{15}\sum_{k=4}^{11}\frac{e^{-j\frac{14\pi}{15}k}}{1-W_{15}^{-k}z^{-1}},
\qquad W_{15}=e^{-j\frac{2\pi}{15}}.
\]
</div>
<div class="answer-step"><strong>第 3 步：结构实现。</strong>仍采用梳状滤波器 \(1-z^{-15}\) 与并联谐振器柜的级联；本题只激活 \(k=4\) 至 \(11\) 的八个支路。</div>
""" + _frequency_sampling_diagram() + r"""
<h2>2017 年真题：矩形窗与余弦窗低通设计</h2>
<p>八、用矩形窗设计一个低通滤波器。</p>
<div class="answer-step"><strong>第 1 步：理想响应。</strong>令 \(m=n-a\)。对理想低通作反 DTFT：</div>
<div class="formula">\[
h_d(n)=
\begin{cases}
\dfrac{\omega_c}{\pi},&m=0,\\
\dfrac{\sin(\omega_c m)}{\pi m},&m\ne0.
\end{cases}
\]
</div>
<p>为得到因果线性相位 FIR，截断中心应与有限长窗中心重合，故</p>
<div class="formula">\[
a=\frac{N-1}{2},\qquad h(n)=h_d(n)w_R(n),\qquad
w_R(n)=\begin{cases}1,&0\le n\le N-1,\\0,&\text{其他}.
\end{cases}
\]
</div>
<div class="answer-step"><strong>第 2 步：长度类型。</strong>\(N\) 为奇数时，\(a\) 为整数，得到偶对称的 I 型线性相位 FIR；\(N\) 为偶数时，\(a\) 为半整数，得到偶对称的 II 型线性相位 FIR。两种均可由同一中心对齐关系写出。</div>
<div class="answer-step"><strong>第 3 步：改用余弦窗。</strong>若采用标准余弦（Hann）窗，取</div>
<div class="formula">\[
w_C(n)=\begin{cases}
\dfrac{1}{2}\left[1-\cos\!\left(\dfrac{2\pi n}{N-1}\right)\right],&0\le n\le N-1,\\
0,&\text{其他},
\end{cases}
\qquad h(n)=h_d(n)w_C(n).
\]
</div>
<p>余弦窗旁瓣低于矩形窗，但主瓣更宽；因此阻带纹波改善而过渡带相应变宽。</p>
<h2>2019 年真题：二阶 FIR 的零点与线性相位</h2>
<p>五、设计 FIR 滤波器，\(H(z)=1-2a\cos\theta\,z^{-1}+a^2z^{-2}\)。</p>
<div class="answer-step"><strong>第 1 步：因式分解。</strong></div>
<div class="formula">\[
H(z)=\left(1-ae^{j\theta}z^{-1}\right)\left(1-ae^{-j\theta}z^{-1}\right).
\]
</div>
<p>故有两个零点 \(z_{1,2}=ae^{\pm j\theta}\)，没有有限极点；若以 \(z^{-1}\) 的实现形式计，FIR 的极点均在原点。</p>
<div class="answer-step"><strong>第 2 步：直接型。</strong>系数为 \(b_0=1\)、\(b_1=-2a\cos\theta\)、\(b_2=a^2\)，所以直接型为两个串联延时器的抽头延迟线，三个抽头加权后在求和器相加：</div>
<div class="formula">\[
y(n)=x(n)-2a\cos\theta\,x(n-1)+a^2x(n-2).
\]
</div>
<div class="answer-step"><strong>第 3 步：线性相位条件。</strong>实 FIR 的长度为 3；要偶对称，须 \(b_0=b_2\)，即 \(a^2=1\)。因此 \(a=1\) 或 \(a=-1\) 时满足线性相位，群延迟为 1 个采样周期。</div>
<h2>2021 年真题：窄带干扰抑制</h2>
<p>九、FIR 滤波器。给出 \(H(z)=1-2a\cos\theta\,z^{-1}+a^2z^{-2}\)。</p>
<div class="answer-step"><strong>零极点、直接型与线性相位。</strong>前三问与上题相同：零点为 \(ae^{\pm j\theta}\)，直接型差分方程为</div>
<div class="formula">\[
y(n)=x(n)-2a\cos\theta\,x(n-1)+a^2x(n-2),
\qquad a=\pm1\ \text{时为线性相位}.
\]
</div>
<div class="answer-step"><strong>第 4 步：将零点放到干扰频率。</strong>窄带干扰主频率为 \(\pi/3\) 时，实系数滤波器必须同时在 \(\pm\pi/3\) 设置共轭零点。令</div>
<div class="formula">\[
a=1,\qquad\theta=\frac{\pi}{3},
\]
</div>
<p>则</p>
<div class="formula">\[
H(z)=1-z^{-1}+z^{-2},\qquad
H\!\left(e^{j\frac{\pi}{3}}\right)=H\!\left(e^{-j\frac{\pi}{3}}\right)=0.
\]
</div>
<p>这给出以 \(\pm\pi/3\) 为中心的二阶陷波；若实际干扰频带有宽度，应增加零点对或采用更高阶带阻 FIR，以同时控制陷波带宽和通带失真。</p>
<h2>2024 年真题：二阶 FIR 的幅相响应</h2>
<p>八、已知 \(H(z)=1+az^{-1}+z^{-2}\)。</p>
<div class="answer-step"><strong>第 1 步：由零响应求 \(a\)。</strong>代入单位圆并将延时因子提出：</div>
<div class="formula">\[
H(e^{j\omega})=e^{-j\omega}\left(a+2\cos\omega\right).
\]
</div>
<p>在 \(\omega=3\pi/4\) 处为零，故</p>
<div class="formula">\[
a=-2\cos\!\left(\frac{3\pi}{4}\right)=\sqrt{2}.
\]
</div>
<div class="answer-step"><strong>第 2 步：幅度和相位。</strong>代入该系数：</div>
<div class="formula">\[
\left|H(e^{j\omega})\right|=\left|\sqrt{2}+2\cos\omega\right|,
\]
\[
\theta(\omega)=
\begin{cases}
-\omega,&\sqrt{2}+2\cos\omega\ge0,\\
\pi-\omega,&\sqrt{2}+2\cos\omega<0,
\end{cases}
\quad (\text{按 }2\pi\text{ 主值折返}).
\]
</div>
<div class="answer-step"><strong>第 3 步：线性相位。</strong>系数 \(h(0)=1\)、\(h(1)=\sqrt2\)、\(h(2)=1\) 满足偶对称，因此是 I 型线性相位 FIR。相位直线的斜率为 \(-1\)，延迟为 1 个采样周期。</div>
</main>
"""
    document = _document(content).replace(
        "</style>",
        """.frequency-sampling-diagram{display:block;width:100%;max-width:166mm;height:auto;margin:10pt auto;border:1px solid #d8e0e5;border-radius:5pt;background:#fbfcfd;break-inside:avoid}\n</style>""",
    )
    output.write_text(document, encoding="utf-8")
    return output


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    print(write_training_html(root / "full" / "outputs" / "chapter_07_supplemental_training.html"))
    print(write_answers_html(root / "full" / "outputs" / "chapter_07_supplemental_answers.html"))
