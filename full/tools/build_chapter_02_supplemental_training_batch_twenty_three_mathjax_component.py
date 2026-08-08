"""2014 DTFT magnitude/phase property question for chapter-two supplemental training."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.plot-pair{break-inside:avoid;display:block;margin:10pt 0}.plot{display:block;break-inside:avoid;margin:6pt auto;text-align:center}.plot svg{width:min(100%,400pt);height:auto}.plot figcaption{color:#315d7c;font-size:9.5pt;margin-top:2pt}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def amplitude_phase_svg() -> str:
    """Draw separate source-faithful magnitude and phase plots from exact axes."""
    defs = r'''<defs><marker id="arrow-2014-dtft" markerWidth="8" markerHeight="8" refX="6.5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#174b73"/></marker></defs>'''
    magnitude = r'''<svg viewBox="0 0 520 295" role="img" aria-label="2014 年真题的 DTFT 幅频图">''' + defs + r'''
<path d="M48 220H482" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-2014-dtft)"/><path d="M265 245V37" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-2014-dtft)"/>
<path d="M70 220V210M168 220V210M265 220V210M362 220V210M460 220V210M255 150H265M255 80H265" fill="none" stroke="#52616b" stroke-width="1.2"/>
<path d="M70 220V80H168L265 150L362 80H460V220" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linejoin="round"/>
<text x="272" y="35" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">幅度</text><text x="486" y="228" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">ω</text><text x="245" y="239" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">0</text><text x="238" y="155" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">1</text><text x="238" y="85" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">2</text>
<foreignObject x="48" y="226" width="44" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(-\pi\)</div></foreignObject><foreignObject x="140" y="226" width="56" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(-\pi/2\)</div></foreignObject><foreignObject x="335" y="226" width="56" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(\pi/2\)</div></foreignObject><foreignObject x="438" y="226" width="44" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(\pi\)</div></foreignObject>
</svg>'''
    phase = r'''<svg viewBox="0 0 520 295" role="img" aria-label="2014 年真题的 DTFT 相频图">''' + defs + r'''
<path d="M48 150H482" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-2014-dtft)"/><path d="M265 245V37" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-2014-dtft)"/>
<path d="M70 150V140M265 150V140M460 150V140M255 220H265M255 80H265" fill="none" stroke="#52616b" stroke-width="1.2"/><path d="M70 220L460 80" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linecap="round"/>
<text x="272" y="35" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">相位</text><text x="486" y="158" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">ω</text><text x="245" y="169" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">0</text>
<foreignObject x="218" y="202" width="40" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(-\pi\)</div></foreignObject><foreignObject x="268" y="63" width="34" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:left">\(\pi\)</div></foreignObject><foreignObject x="48" y="156" width="44" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(-\pi\)</div></foreignObject><foreignObject x="438" y="156" width="44" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px;text-align:center">\(\pi\)</div></foreignObject>
</svg>'''
    return f'<div class="plot-pair"><figure class="plot">{magnitude}<figcaption>幅频图</figcaption></figure><figure class="plot">{phase}<figcaption>相频图</figcaption></figure></div>'


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2014 年真题</span><span>详解见 P.____</span></div><p>二、</p><p>已知系统 \(x[n]\) 的傅里叶变换 \(X(e^{j\omega})\) 在 \(-\pi\leq\omega\leq\pi\) 的区间上幅频和相频图如图，试确定 \(x[n]\) 是否是周期的，实信号，偶信号及有限能量的？</p>''' + amplitude_phase_svg() + r'''</section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2014 年真题：由 DTFT 的幅相特性判定序列性质</h2><p>先从图中读出：幅度 \(\left|X(e^{j\omega})\right|\) 关于 \(\omega=0\) 为偶函数；相位为 \(\phi(\omega)=\omega\)，关于原点为奇函数。下面分别判定。</p><h3>1．周期性</h3><p>若 \(x[n]\) 是周期序列，其 DTFT 应由若干谐波频率处的冲激谱线构成。题图给出的是在一个周期内连续变化、且有界的幅相曲线，因此 \(x[n]\) <strong>不是周期序列</strong>。</p><h3>2．实序列性</h3><p>实序列的频谱必须满足共轭对称性：</p><div class="formula">\[X^*(e^{j\omega})=X(e^{-j\omega}).\]</div><p>等价地，幅度为偶函数、相位为奇函数。题图恰好满足这两个条件，所以 \(x[n]\) <strong>是实序列</strong>。</p><h3>3．偶序列性</h3><p>若 \(x[n]\) 为偶序列，则 \(X(e^{j\omega})=X(e^{-j\omega})\)，其相位只能在 \(0\) 或 \(\pi\)（模 \(2\pi\)）附近取值。题图的相位 \(\phi(\omega)=\omega\) 并不满足该条件，所以 \(x[n]\) <strong>不是偶序列</strong>。</p><h3>4．能量性</h3><p>该幅度曲线在 \([-\pi,\pi]\) 上有界、分段连续，故平方可积。由 Parseval 关系：</p><div class="formula">\[E_x=\frac{1}{2\pi}\int_{-\pi}^{\pi}\left|X(e^{j\omega})\right|^2\,\mathrm{d}\omega&lt;\infty.\]</div><p>因此 \(x[n]\) <strong>是有限能量序列</strong>。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>''', encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    return subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
