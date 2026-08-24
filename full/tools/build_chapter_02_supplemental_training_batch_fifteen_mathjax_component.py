"""Fifteenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r'''<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
figure{break-inside:avoid;margin:10pt auto;text-align:center}svg{width:min(100%,470pt);height:auto}figcaption{color:#315d7c;font-size:9.5pt;margin-top:3pt}
</style>'''


def _system_svg() -> str:
    return r'''<figure><svg data-source-candidate-id="2025-q七-01" viewBox="0 0 790 190" role="img" aria-label="连续时间信号经采样、频移、数字滤波和数模转换的系统框图">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#164e78"/></marker></defs>
<g fill="none" stroke="#164e78" stroke-width="2.4" marker-end="url(#arrow)"><path d="M24 78H115"/><path d="M270 78H336"/><path d="M391 78H454"/><path d="M580 78H650"/><path d="M758 78H786"/></g>
<g fill="#fff" stroke="#164e78" stroke-width="2.2"><rect x="115" y="43" width="155" height="70" rx="2"/><rect x="454" y="43" width="126" height="70" rx="2"/><rect x="650" y="43" width="108" height="70" rx="2"/><circle cx="364" cy="78" r="27"/></g>
<g stroke="#164e78" stroke-width="2" marker-end="url(#arrow)"><path d="M192 151V115"/><path d="M364 151V108"/><path d="M704 151V115"/></g>
<g fill="#1f2933" font-family="Microsoft YaHei, sans-serif" font-size="18" text-anchor="middle"><text x="192" y="73">理想 A/D</text><text x="192" y="98">转化器</text><text x="517" y="87">数字滤波器</text><text x="704" y="73">理想 D/A</text><text x="704" y="98">转化器</text></g>
<g fill="#1f2933" font-family="Cambria Math, serif" font-size="21" text-anchor="middle"><text x="70" y="67">x(t)</text><text x="302" y="67">x[n]</text><text x="420" y="67">w[n]</text><text x="615" y="67">y[n]</text><text x="776" y="67">y(t)</text><text x="517" y="88">H(eʲω)</text><text x="192" y="177">T</text><text x="364" y="177">(−1)ⁿ</text><text x="704" y="177">T</text></g>
<g stroke="#b56b2e" stroke-width="2.5"><path d="M351 65L377 91M377 65L351 91"/></g>
</svg><figcaption>2025 年第七题第 4 小题的处理结构：采样后先乘以 −1 的离散幂实现频移，再经数字滤波和理想 D/A 转换。</figcaption></figure>'''


def _source_response_svg() -> str:
    return r'''<figure><svg data-source-candidate-id="2025-q七-01" viewBox="0 0 760 230" role="img" aria-label="输入连续频谱与数字滤波器频率响应">
<defs><marker id="axis" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#164e78"/></marker></defs>
<g transform="translate(25 20)"><text x="155" y="18" text-anchor="middle" fill="#315d7c" font-family="Microsoft YaHei" font-size="17">输入连续频谱</text><g stroke="#164e78" stroke-width="2" fill="none" marker-end="url(#axis)"><path d="M10 135H300"/><path d="M155 152V35"/></g><path d="M67 135V69H243V135" fill="none" stroke="#008f92" stroke-width="3"/><g fill="#1f2933" font-family="Cambria Math" font-size="17"><text x="148" y="31">X(jΩ)</text><text x="302" y="151">Ω</text><text x="57" y="157">−600π</text><text x="145" y="157">0</text><text x="219" y="157">600π</text><text x="163" y="66">1</text></g></g>
<g transform="translate(410 20)"><text x="155" y="18" text-anchor="middle" fill="#315d7c" font-family="Microsoft YaHei" font-size="17">数字滤波器频率响应</text><g stroke="#164e78" stroke-width="2" fill="none" marker-end="url(#axis)"><path d="M10 135H300"/><path d="M155 152V35"/></g><path d="M68 135V82H112V135M198 135V82H242V135" fill="none" stroke="#008f92" stroke-width="3"/><g fill="#1f2933" font-family="Cambria Math" font-size="17"><text x="148" y="31">H(eʲω)</text><text x="302" y="151">ω</text><text x="55" y="157">−π</text><text x="93" y="157">−0.5π</text><text x="145" y="157">0</text><text x="196" y="157">0.5π</text><text x="239" y="157">π</text><text x="163" y="79">1</text></g></g>
</svg><figcaption>题图中的输入连续频谱及数字滤波器的幅频响应。</figcaption></figure>'''


def _answer_spectra_svg() -> str:
    return r'''<figure><svg data-source-candidate-id="2025-q七-01" viewBox="0 0 760 420" role="img" aria-label="采样、乘以负一的 n 次幂、滤波和数模转换后的频谱">
<defs><marker id="axis2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#164e78"/></marker></defs>
<g font-family="Microsoft YaHei" fill="#315d7c" font-size="17"><text x="190" y="22" text-anchor="middle">x[n] 的频谱</text><text x="570" y="22" text-anchor="middle">w[n] 的频谱</text><text x="190" y="222" text-anchor="middle">y[n] 的频谱</text><text x="570" y="222" text-anchor="middle">y(t) 的频谱</text></g>
<g stroke="#164e78" stroke-width="2" fill="none" marker-end="url(#axis2)"><path d="M35 145H335"/><path d="M185 162V50"/><path d="M425 145H725"/><path d="M575 162V50"/><path d="M35 345H335"/><path d="M185 362V250"/><path d="M425 345H725"/><path d="M575 362V250"/></g>
<g fill="none" stroke="#008f92" stroke-width="3"><path d="M95 145V85H275V145"/><path d="M425 145V85H485V145M665 145V85H725"/><path d="M425 345V285H485V345M665 345V285H725"/><path d="M470 345V285H505V345M645 345V285H680V345"/></g>
<g fill="#1f2933" font-family="Cambria Math" font-size="16"><text x="338" y="160">ω</text><text x="728" y="160">ω</text><text x="338" y="360">ω</text><text x="728" y="360">Ω</text><text x="88" y="164">−0.6π</text><text x="178" y="164">0</text><text x="260" y="164">0.6π</text><text x="422" y="164">−π</text><text x="470" y="164">−0.4π</text><text x="650" y="164">0.4π</text><text x="708" y="164">π</text><text x="422" y="364">−π</text><text x="470" y="364">−0.5π</text><text x="650" y="364">0.5π</text><text x="708" y="364">π</text><text x="448" y="364">−1000π</text><text x="505" y="364">−500π</text><text x="645" y="364">500π</text><text x="686" y="364">1000π</text></g>
</svg><figcaption>四个频谱均按同一幅度比例绘制；在各频带的内部幅度为 1。</figcaption></figure>'''


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2025 年真题</span><span>详解见 P.____</span></div>
<p>四、利用如下框图处理连续时间信号，已知采样周期为 \(T=1\,\mathrm{ms}\)，\(x(t)\) 的频谱 \(X(j\Omega)\) 和系统频谱如图，试画出：</p>''' + _system_svg() + _source_response_svg() + r'''<p>（1）\(x[n]\) 的频谱 \(X(e^{j\omega})\)；</p><p>（2）\(w[n]\) 的频谱 \(W(e^{j\omega})\)；</p><p>（3）\(y[n]\) 的频谱 \(Y(e^{j\omega})\)；</p><p>（4）\(y(t)\) 的频谱 \(X(j\Omega)\)。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2025 年真题：采样、频移、数字滤波与恢复</h2>
<p>采样周期为 \(T=10^{-3}\,\mathrm{s}\)，所以 \(\Omega_s=\frac{2\pi}{T}=2000\pi\,\mathrm{rad/s}\)。原谱带宽为 \(600\pi\,\mathrm{rad/s}\)，低于奈奎斯特角频率 \(\Omega_s/2=1000\pi\,\mathrm{rad/s}\)，因此采样后在一个主值区间内没有混叠。</p>
<div class="formula">\[X(e^{j\omega})=\frac{1}{T}\sum_{k=-\infty}^{\infty}X\!\left(j\frac{\omega-2\pi k}{T}\right),\qquad \left|\omega\right|\leq0.6\pi.\]</div>
<p>其中 \(X(e^{j\omega})\) 在 \(\left|\omega\right|\leq0.6\pi\) 内为常数 \(1/T\)。题图按归一化幅度绘制时可取该矩形高度为 1。</p>
<p>乘以 \((-1)^n=e^{j\pi n}\) 相当于将离散时间频谱平移 \(\pi\)：</p>
<div class="formula">\[W(e^{j\omega})=X\!\left(e^{j(\omega-\pi)}\right).\]</div>
<p>考虑 \(2\pi\) 周期延拓后，\(W(e^{j\omega})\) 的两个频带为 \(0.4\pi\leq\left|\omega\right|\leq\pi\)。滤波器仅通过 \(0.5\pi\leq\left|\omega\right|\leq\pi\)，故</p>
<div class="formula">\[Y(e^{j\omega})=\begin{cases}\frac{1}{T},&0.5\pi\leq\left|\omega\right|\leq\pi,\\0,&\text{其他}。\end{cases}\]</div>
<p>理想 D/A 在主值频带内满足 \(Y_c(j\Omega)=T\,Y(e^{j\Omega T})\)。于是输出连续频谱恢复为单位高度的双边带通矩形：</p>
<div class="formula">\[Y_c(j\Omega)=\begin{cases}1,&500\pi\leq\left|\Omega\right|\leq1000\pi,\\0,&\text{其他}。\end{cases}\]</div>''' + _answer_spectra_svg() + r'''</section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
