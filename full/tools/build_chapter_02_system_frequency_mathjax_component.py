"""System function, frequency response and geometric reading in one MathJax flow."""
from __future__ import annotations

import base64
from io import BytesIO
import subprocess
import sys
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:20mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}figure{margin:12pt auto;text-align:center}.diagram-plot{width:min(100%,470pt);height:auto}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def z_plane_plot() -> str:
    """Render the z-plane from coordinates at print resolution, avoiding SVG/WeasyPrint corruption."""
    fig = Figure(figsize=(7.1, 3.8), dpi=240, facecolor="#fbfcfd")
    FigureCanvasAgg(fig)
    ax = fig.add_axes((0.06, 0.14, 0.88, 0.77), facecolor="#fbfcfd")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.30, 1.38)
    ax.set_ylim(-1.20, 1.20)
    ax.axis("off")

    axis_colour = "#234b6e"
    unit_colour = "#8aa5b5"
    zero_colour = "#008e96"
    pole_colour = "#b83a31"
    ax.annotate("", xy=(1.30, 0), xytext=(-1.22, 0), arrowprops={"arrowstyle": "-|>", "color": axis_colour, "lw": 1.4})
    ax.annotate("", xy=(0, 1.13), xytext=(0, -1.10), arrowprops={"arrowstyle": "-|>", "color": axis_colour, "lw": 1.4})
    ax.add_patch(__import__("matplotlib").patches.Circle((0, 0), 1, fill=False, ec=unit_colour, lw=1.3, ls=(0, (4, 3))))
    ax.plot(0, 0, "o", color=axis_colour, ms=4)

    b = (0.70, 0.70)
    c = (1.03, 0.0)
    d = (0.70, 0.0)
    ax.plot((0, b[0]), (0, b[1]), color=zero_colour, lw=1.2, ls=(0, (4, 3)))
    ax.plot((b[0], d[0]), (b[1], d[1]), color=pole_colour, lw=1.5)
    ax.plot(*b, "o", color=zero_colour, ms=6)
    ax.plot(*c, marker="o", mfc="#fbfcfd", mec=zero_colour, mew=2.0, ms=10)
    ax.plot(*d, marker="x", color=pole_colour, mew=2.5, ms=11)

    font = {"fontname": "Microsoft YaHei"}
    ax.text(1.33, -0.10, "实轴", color=axis_colour, fontsize=11, ha="left", va="top", **font)
    ax.text(0.06, 1.10, "虚轴", color=axis_colour, fontsize=11, ha="left", va="bottom", **font)
    ax.text(0.06, -0.10, "0", color=axis_colour, fontsize=10, ha="left", va="top", **font)
    ax.text(-0.68, 0.90, "单位圆", color="#54758a", fontsize=10, **font)
    ax.text(b[0] + 0.08, b[1] + 0.02, "频率点 B", color="#006d73", fontsize=10.5, **font)
    ax.text(c[0] - 0.02, -0.18, "零点 C", color="#006d73", fontsize=10.5, ha="center", **font)
    ax.text(d[0] + 0.10, 0.12, "极点 D", color="#9d302a", fontsize=10.5, **font)
    ax.text(0.78, 0.33, "距离 |B−D|", color=pole_colour, fontsize=10, **font)
    ax.text(0, -1.10, "单位圆上的位置随频率转动", color="#54758a", fontsize=10, ha="center", **font)

    payload = BytesIO()
    fig.savefig(payload, format="png", dpi=240, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.04)
    encoded = base64.b64encode(payload.getvalue()).decode("ascii")
    return f'<figure><img class="diagram-plot" src="data:image/png;base64,{encoded}" alt="单位圆上的频率点与零、极点的距离决定幅度的峰谷"><figcaption>单位圆上的频率点与零、极点的距离决定幅度的峰谷</figcaption></figure>'


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r'''
<main>
<h1>系统函数及其与系统性质的关系</h1>
<p>对零状态 LSI 系统，输出是输入与单位脉冲响应的卷积；在 z 域中卷积化为乘法。系统函数定义（用于由输入输出关系刻画系统）为：</p>
<div class="formula">\[H(z)=\frac{Y(z)}{X(z)}=\mathcal{Z}\{h(n)\}\]</div>
<p>系统函数的收敛域与 [[h(n)]] 的收敛域相同。LSI 系统的因果性与 BIBO 稳定性可直接由单位脉冲响应判定：</p>
<p>因果系统的单位脉冲响应条件（用于判断当前输出是否只依赖当前及过去输入）为：</p>
<div class="formula">\[h(n)=0,\qquad n<0\]</div>
<p>BIBO 稳定性定义（用于判断有界输入是否只产生有界输出）为：</p>
<div class="formula">\[\left|x(n)\right|\le M<\infty\ \Longrightarrow\ \left|y(n)\right|\le P<\infty\]</div>
<p>LSI 系统的绝对可和判据（用于把稳定性转化为对单位脉冲响应的检验）为：</p>
<div class="formula">\[\sum_{n=-\infty}^{\infty}\left|h(n)\right|<\infty\]</div>
<p>因果系统的收敛域在最外极点之外；稳定系统要求单位圆落在收敛域中。因而，因果有理系统稳定的充要条件是全部极点严格位于单位圆内。</p>
<h2>例题：由单位脉冲响应判定因果与稳定</h2>
<p><strong>例题</strong>：判断系统的因果稳定性： [[h(n)=\frac{1}{3}\left[\delta(n+1)+\delta(n)+\delta(n-1)\right] ]]</p>
<h3>解</h3>
<p>因果性检查（用于排除含有未来输入项的系统）：</p>
<div class="formula">\[h(-1)=\frac{1}{3}\ne 0\]</div>
<p>因此该冲激响应在负时刻非零，系统<strong>非因果</strong>。稳定性检查（用于按绝对可和判据作结论）为：</p>
<div class="formula">\[\sum_{n=-\infty}^{\infty}\left|h(n)\right|=\frac{1}{3}+\frac{1}{3}+\frac{1}{3}=1<\infty\]</div>
<p>所以系统稳定。对应的系统函数（用于从极点和收敛域再核对该结论）为：</p>
<div class="formula">\[H(z)=\frac{1}{3}\left(z+1+z^{-1}\right)=\frac{z^2+z+1}{3z}\]</div>
<p>该序列是有限长双边序列，故其收敛域为：</p>
<div class="formula">\[\operatorname{ROC}:\quad 0<\left|z\right|<\infty\]</div>
<p>单位圆在此收敛域中，与“系统稳定”的时域结论一致；同时收敛域不是最外极点之外的右边区域，与“系统非因果”的结论一致。</p>
<h3>将上例改造成因果稳定系统</h3>
<p>将原冲激响应延时一个样本，得到因果版本：</p>
<div class="formula">\[h'(n)=\frac{1}{3}\left[\delta(n)+\delta(n-1)+\delta(n-2)\right]\]</div>
<p>时移对应的系统函数关系（用于由原系统函数直接得到延时后的系统函数）为：</p>
<div class="formula">\[H'(z)=H(z)z^{-1}=\frac{1}{3}\left(1+z^{-1}+z^{-2}\right)=\frac{z^2+z+1}{3z^2}\]</div>
<p>因 [[h'(n)]] 在 [[n<0]] 时为零且仍绝对可和，改造后的系统因果且稳定；它的收敛域为：</p>
<div class="formula">\[\operatorname{ROC}:\quad \left|z\right|>0\]</div>
<h2>例题：由差分方程求系统函数</h2>
<p><strong>例题</strong>：已知线性移不变因果系统的差分方程为：</p>
<div class="formula">\[y(n)+0.2y(n-1)-0.24y(n-2)=x(n)+x(n-1)\]</div>
<p>（1）求系统函数 [[H(z)]] 和系统收敛域。<br>（2）判别系统的稳定性。<br>（3）求系统的单位取样响应 [[h(n)]]。</p>
<h3>解</h3>
<p>零状态 z 变换得到的系统函数（用于读取零极点并确定收敛域）为：</p>
<div class="formula">\[H(z)=\frac{1+z^{-1}}{1+0.2z^{-1}-0.24z^{-2}}=\frac{z(z+1)}{(z+0.6)(z-0.4)}\]</div>
<p>因系统因果，收敛域为 [[|z|&gt;0.6]]；单位圆在该区域内，因此系统稳定。部分分式展开与反变换（用于求单位取样响应）后：</p>
<div class="formula">\[h(n)=\left(\frac{7}{5}\,0.4^n-\frac{2}{5}(-0.6)^n\right)u(n)\]</div>
<h1>系统频率响应的意义</h1>
<p>频率响应是单位脉冲响应的 DTFT，也是系统函数在单位圆上的取值：</p>
<div class="formula">\[H(e^{j\omega})=\sum_{n=-\infty}^{\infty}h(n)e^{-j\omega n}=H(z)\big|_{z=e^{j\omega}}\]</div>
<p>它由幅频响应与相频响应共同构成：</p>
<div class="formula">\[H(e^{j\omega})=\left|H(e^{j\omega})\right|e^{j\angle H(e^{j\omega})}\]</div>
<p>幅度响应常用分贝表示，以便直接比较增益和衰减：</p>
<div class="formula">\[G_{\mathrm{dB}}(\omega)=20\log_{10}\left|H(e^{j\omega})\right|\]</div>
<p>因此 \(0\,\mathrm{dB}\) 对应单位增益；\(20\,\mathrm{dB}\) 对应十倍幅度增益；\(-20\,\mathrm{dB}\) 对应十分之一幅度。</p>
<h2>归一化角频率的换算</h2>
<p>连续时间正弦在一个周期内包含 \(N_0=T_0/T\) 个采样点时，其连续角频率与离散时间归一化角频率的换算（用于在 \(\Omega\) 与 \(\omega\) 两个频率标度间转换）为：</p>
<div class="formula">\[\omega=\Omega T=\frac{2\pi}{T_0}T=\frac{2\pi}{N_0}\]</div>
<p>若输入为复指数 [[x(n)=e^{j\omega_0n}]]，输出仍为同频率复指数：</p>
<div class="formula">\[y(n)=H(e^{j\omega_0})e^{j\omega_0n}\]</div>
<p>对实正弦输入 [[x(n)=A\cos(\omega_0n+\varphi)]]，频率不变；输出幅度乘以 [[|H(e^{j\omega_0})|]]，相位增加 [[\angle H(e^{j\omega_0})]]。纯延时 [[n_d]] 个样本只改变相位：</p>
<div class="formula">\[H(e^{j\omega})=e^{-j\omega n_d},\qquad \left|H(e^{j\omega})\right|=1,\quad \angle H(e^{j\omega})=-\omega n_d\]</div>
<p>相频响应随频率的斜率对应群延迟；对理想延时系统，所有频率分量具有相同的群延迟：</p>
<div class="formula">\[\tau_g(\omega)=-\frac{\mathrm{d}}{\mathrm{d}\omega}\angle H(e^{j\omega}),\qquad \tau_g(\omega)=n_d\quad\text{（理想延时）}\]</div>
<h2>例题：固定频率正弦通过一阶 LSI 系统</h2>
<p><strong>例题</strong>：某 LSI 系统的系统函数如下：</p>
<div class="formula">\[H(z)=0.05\frac{1+z^{-1}}{1-0.9z^{-1}}\]</div>
<p>若系统的输入信号为：</p>
<div class="formula">\[x(n)=\sin(0.01\pi n)\]</div>
<p>试编程并分析系统的输出。</p>
<h3>解</h3>
<p>本讲义只保留该例的解析频域结论。将单位圆上的频率点代入系统函数，得到频率响应公式（用于计算该频率分量的幅度变化与相位变化）：</p>
<div class="formula">\[H(e^{j\omega})=0.05\frac{1+e^{-j\omega}}{1-0.9e^{-j\omega}}\]</div>
<p>该系统的等价差分方程（用于说明输出由当前输入、前一输入和前一输出共同决定）为：</p>
<div class="formula">\[y(n)=0.9y(n-1)+0.05x(n)+0.05x(n-1)\]</div>
<p>在 \(\omega_0=0.01\pi\) 处，有 \(\left|H(e^{j\omega_0})\right|\approx0.958\)、\(\angle H(e^{j\omega_0})\approx-0.290\,\mathrm{rad}\)。因此输出仍为同频率正弦，幅度仅略微减小且向后移相；在低频附近群延迟约为 9--10 个样本，符合该系统低通且带明显低频延时的特征。</p>
<h2>例题：分析 3 点均值滤波系统的频率响应</h2>
<p><strong>例题</strong>：分析 3 点均值滤波系统的频率响应。</p>
<p>该系统的单位脉冲响应和等价时域表达式（用于说明它对相邻三个样本作算术平均）分别为：</p>
<div class="formula">\[h(n)=\frac{1}{3}\left[\delta(n)+\delta(n-1)+\delta(n-2)\right]\]</div>
<div class="formula">\[y(n)=\frac{1}{3}\left[x(n)+x(n-1)+x(n-2)\right]\]</div>
<p>频率响应的化简式（用于读取幅度、相位和被完全抑制的频率）为：</p>
<div class="formula">\[H(e^{j\omega})=\frac{1+e^{-j\omega}+e^{-j2\omega}}{3}=\frac{1}{3}e^{-j\omega}\frac{\sin\left(\frac{3\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}\]</div>
<p>因此在 \(\omega=\frac{2\pi}{3}\) 处幅度为零，低频附近幅度较大，说明它具有平滑、抑制较高频分量的低通特性。主值相位（用于判断相位移位方向）为：</p>
<div class="formula">\[\angle H(e^{j\omega})=
\begin{cases}
-\omega, & 0\le\omega<\frac{2\pi}{3},\\
\pi-\omega, & \frac{2\pi}{3}\le\omega\le\pi.
\end{cases}\]</div>
<p>若输入同时含有 \(0.25\pi\)、\(0.5\pi\) 与 \(0.85\pi\) 三个频率分量，则输出中靠近 \(0.85\pi\) 的分量会被显著抑制；这正是根据幅频响应判断“哪些频率通过、哪些频率衰减”的方法。</p>
<h1>几何法画频率响应</h1>
<p>设系统函数的零点为 [[c_r]]、极点为 [[d_r]]，增益为 [[A]]。令单位圆上的频率点 [[B=e^{j\omega}]] 随 [[\omega]] 转动，则零极点分解给出：</p>
<div class="formula">\[H(z)=A\frac{\prod_r(z-c_r)}{\prod_r(z-d_r)}\]</div>
<div class="formula">\[\left|H(e^{j\omega})\right|=\left|A\right|\frac{\prod_r\left|B-C_r\right|}{\prod_r\left|B-D_r\right|},\qquad B=e^{j\omega}\]</div>
<p>若分子、分母以 \(z\) 表示时的次数分别为 \(N\)、\(M\)，把单位圆上的频率点代入后，额外幂次只影响相位：</p>
<div class="formula">\[H(e^{j\omega})=Ae^{j(N-M)\omega}\frac{\prod_r\left(e^{j\omega}-c_r\right)}{\prod_r\left(e^{j\omega}-d_r\right)}\]</div>
<p>因此，频率点靠近极点时分母变小，幅度形成峰；靠近零点时分子变小，幅度形成谷。单位圆上的零点对应完全抑制的频率；单位圆上的极点会导致不稳定，故稳定系统的极点不能在单位圆上。</p>
__Z_PLANE__
<h2>一阶系统与梳状零点</h2>
<p>对 [[y(n)=by(n-1)+x(n)]]（[[0&lt;b&lt;1]]），有：</p>
<div class="formula">\[H(z)=\frac{1}{1-bz^{-1}},\qquad \left|H(e^{j\omega})\right|=\frac{1}{\left|e^{j\omega}-b\right|}\]</div>
<p>极点位于正实轴且在单位圆内；当 [[\omega=0]] 时频率点最接近极点，幅度最大；当 [[\omega=\pi]] 时距离最大，幅度最小，故为低通特性。</p>
<p>对 [[H(z)=1-z^{-N}]]，单位圆上有 [[N]] 个等角度零点，频响为：</p>
<div class="formula">\[\left|H(e^{j\omega})\right|=\left|1-e^{-jN\omega}\right|=2\left|\sin\frac{N\omega}{2}\right|\]</div>
<p>零点出现在 [[\omega=2\pi k/N]]，因而形成等间隔衰减槽。读图时先让频率点沿单位圆转动：靠极点找峰、靠零点找谷，再检查极点是否全在单位圆内。</p>
</main>'''.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")").replace("__Z_PLANE__", z_plane_plot())
    document = f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_system_frequency_mathjax_component.pdf"))
