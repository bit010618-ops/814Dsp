"""Chapter-seven priority FIR training and consolidated answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import STYLE, _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第七章 分章强化训练</h1>
<div class="exam-head"><span>2022 年真题</span><span>详解见 P.____</span></div>
<p>九、利用窗函数法设计数字带阻滤波器，滤波器技术指标如下：</p>
<div class="formula">\[
f_{s1}=2.8\,\mathrm{kHz},\qquad f_{s2}=5.8\,\mathrm{kHz},\qquad
f_{p1}=2.2\,\mathrm{kHz},\qquad f_{p2}=6.4\,\mathrm{kHz},\qquad
f_s=20\,\mathrm{kHz}.
\]</div>
<p>采用海明窗进行设计，试求：</p>
<p>（1）滤波器的数字指标 \(\omega_{s1}\)、\(\omega_{s2}\)、\(\omega_{p1}\)、\(\omega_{p2}\)；</p>
<p>（2）求出滤波器阶数 \(N\)，写出 \(\Theta(\omega)\) 的表达式；</p>
<p>（3）写出 \(h(n)\) 的表达式。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2024 年真题</span><span>详解见 P.____</span></div>
<p>4.一个线性相位因果 FIR 数字滤波器单位脉冲响应 \(h(n)\) 均为实数，其系统函数有以下零点：</p>
<div class="formula">\[
z_1=-1,\qquad z_2=e^{-j\frac{2\pi}{3}},\qquad z_3=0.5e^{-j\frac{\pi}{3}}.
\]</div>
<p>（1）写出该系统可能的其他零点；</p>
<p>（2）试确定该滤波器的最低阶数以及最小群延迟的值。</p>
<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2025 年真题</span><span>详解见 P.____</span></div>
<p>九、用窗函数设计一个因果稳定的 FIR 线性相位高通数字滤波器，要求的理想滤波频率响应 \(H_d(e^{j\omega})\) 如下：</p>
<div class="formula">\[
H_d(e^{j\omega})=
\begin{cases}
e^{-j\tau\omega},&\omega_c\le\left|\omega\right|\le\pi,\\
0,&0\le\left|\omega\right|\le\omega_c.
\end{cases}
\]</div>
<p>（1）求理想高通数字滤波器的单位脉冲响应 \(h_d(n)\)；</p>
<p>（2）写出矩形窗函数设计法的 \(h(n)\) 表达式，确定 \(\tau\) 和 \(h(n)\) 的长度 \(N\) 的关系；</p>
<p>（3）\(N\) 值得奇偶性是否可以随意选择，为什么？</p>
<p>（4）若按照上述方法设计出的滤波器达不到阻带衰减的指标要求，你会提出什么解决方案？请简要阐述。</p>
<div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解</h1>
<h2>2022 年真题</h2>
<p>九、利用窗函数法设计数字带阻滤波器。</p>
<div class="answer-step"><strong>第 1 步：归一化频率。</strong>数字角频率由 \(\omega=2\pi f/f_s\) 得到：</div>
<div class="formula">\[
\omega_{p1}=0.22\pi,\qquad \omega_{s1}=0.28\pi,\qquad
\omega_{s2}=0.58\pi,\qquad \omega_{p2}=0.64\pi.
\]</div>
<div class="answer-step"><strong>第 2 步：确定过渡带和理想截止频率。</strong>两侧过渡带宽都为 \(0.06\pi\)，故以两侧中点作为理想带阻的边缘：</div>
<div class="formula">\[
\Delta\omega=0.06\pi,\qquad \omega_{c1}=0.25\pi,\qquad \omega_{c2}=0.61\pi.
\]</div>
<p>海明窗主瓣宽度近似为 \(8\pi/N\)。为使主瓣不宽于过渡带，长度可取满足</p>
<div class="formula">\[
N\ge\frac{8\pi}{\Delta\omega}=\frac{8\pi}{0.06\pi}=133.33.
\]</div>
<p>取不小于该值且便于中心对齐的长度；若以 \(N\) 表示滤波器阶数，则对应长度为 \(N+1\)。理想带阻幅度函数可写为：</p>
<div class="formula">\[
\Theta(\omega)=
\begin{cases}
1,&0\le\left|\omega\right|\le\omega_{c1}\ \text{或}\ \omega_{c2}\le\left|\omega\right|\le\pi,\\
0,&\omega_{c1}<\left|\omega\right|<\omega_{c2}.
\end{cases}
\]</div>
<div class="answer-step"><strong>第 3 步：写出有限长冲激响应。</strong>令 \(M=(N-1)/2\)，理想带阻冲激响应为</div>
<div class="formula">\[
h_d[n]=
\begin{cases}
1-\dfrac{\omega_{c2}-\omega_{c1}}{\pi},&n=M,\\
-\dfrac{\sin\!\left(\omega_{c2}(n-M)\right)-\sin\!\left(\omega_{c1}(n-M)\right)}{\pi(n-M)},&n\ne M.
\end{cases}
\]</div>
<p>海明窗 \(w_H[n]=0.54-0.46\cos\!\left(\frac{2\pi n}{N-1}\right)\)（\(0\le n\le N-1\)）加在理想响应上，得到最终 FIR 系数：</p>
<div class="formula">\[
h[n]=h_d[n]w_H[n],\qquad 0\le n\le N-1.
\]</div>
<h2>2024 年真题</h2>
<p>4.一个线性相位因果 FIR 数字滤波器单位脉冲响应 \(h(n)\) 均为实数，其系统函数有以下零点：\(z_1=-1\)、\(z_2=e^{-j2\pi/3}\)、\(z_3=0.5e^{-j\pi/3}\)。</p>
<div class="answer-step"><strong>第 1 步：使用实系数与线性相位的零点约束。</strong>实系数保证非实零点以共轭对出现；线性相位 FIR 还要求零点关于单位圆成倒数共轭对。因此：</div>
<div class="formula">\[
e^{-j\frac{2\pi}{3}}\ \Longrightarrow\ e^{j\frac{2\pi}{3}},
\]</div>
<p>其中单位圆上的共轭与倒数共轭重合。对于半径为 \(0.5\) 的零点，需要补全一组四元组：</p>
<div class="formula">\[
0.5e^{j\frac{\pi}{3}},\qquad 2e^{j\frac{\pi}{3}},\qquad 2e^{-j\frac{\pi}{3}}.
\]</div>
<div class="answer-step"><strong>第 2 步：数出最低阶数与群延迟。</strong>已知和补全的零点总数为 \(1+2+4=7\)，所以最小 FIR 阶数为 \(7\)。线性相位因果 FIR 的群延迟为阶数的一半，故：</div>
<div class="formula">\[
N_{\min}=7,\qquad \tau_{\min}=\frac{7}{2}.
\]</div>
<p>因此该实现的最小群延迟为 \(7/2\) 个采样周期。</p>
<h2>2025 年真题</h2>
<p>九、用窗函数设计一个因果稳定的 FIR 线性相位高通数字滤波器。</p>
<div class="answer-step"><strong>第 1 步：反变换得到理想响应。</strong>高通响应可视作单位延时冲激减去截止频率为 \(\omega_c\) 的理想低通。令 \(m=n-\tau\)，则</div>
<div class="formula">\[
h_d[n]=
\begin{cases}
1-\dfrac{\omega_c}{\pi},&m=0,\\
-\dfrac{\sin(\omega_c m)}{\pi m},&m\ne0.
\end{cases}
\]</div>
<div class="answer-step"><strong>第 2 步：矩形窗截断。</strong>长度为 \(N\) 的矩形窗为 \(w_R[n]=1\)（\(0\le n\le N-1\)），其他 \(n\) 为零。将截断中心对齐到因果序列的中点：</div>
<div class="formula">\[
\tau=\frac{N-1}{2},\qquad h[n]=h_d[n]w_R[n],\qquad 0\le n\le N-1.
\]</div>
<div class="answer-step"><strong>第 3 步：判断长度奇偶性。</strong>高通在 \(\omega=\pi\) 处必须允许非零响应。偶长度的对称 FIR（II 型）在 \(\omega=\pi\) 被强制为零，不能实现这里的理想高通。因此 \(N\) 不能任意选，需取奇数，使 \(\tau\) 为整数并得到 I 型线性相位 FIR。</div>
<div class="answer-step"><strong>第 4 步：提高阻带衰减。</strong>单纯增加矩形窗长度主要缩窄过渡带，不能显著降低矩形窗固有的旁瓣高度。应改用旁瓣更低的海明窗、布莱克曼窗或可调参数的凯泽窗；若指标同时要求更窄过渡带，则再相应增大 \(N\)。</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    print(write_training_html(root / "full" / "outputs" / "chapter_07_training_mathjax_component.html"))
    print(write_answers_html(root / "full" / "outputs" / "chapter_07_answers_mathjax_component.html"))
