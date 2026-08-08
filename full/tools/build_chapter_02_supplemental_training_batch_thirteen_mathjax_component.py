"""Thirteenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r'''<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>'''


def _training_html_raw() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2025 年真题</span><span>详解见 P.____</span></div><p>八、已知某因果稳定的 LSI 系统 (S_1) 的差分方程如下</p><div class="formula">\[y(n)=\frac{1}{4}\left[x(n)-x(n-1)+x(n+2)-x(n-3)\right]\]</div><p>假设系统函数为 (H_1(z))，求系统的频谱响应为 (H_1(e^{j\omega}))，单位脉冲响应为 (h(n))。</p><p>（1）设系统 (S_1) 的频率响应表达式为 (H_1(e^{j\omega})=\left|H_1(e^{j\omega})\right|e^{j\theta_1(\omega)})，其中 \(\left|H_1(e^{j\omega})\right|\) 为振幅响应，\(\theta_1(\omega)\) 为相位响应，请写出 \(\left|H_1(e^{j\omega})\right|\) 和 \(\theta_1(\omega)\) 的表达式。</p><p>（2）假设有一个系统 (S_2)，该系统的频率响应为 (H_2(e^{j\omega}))，且有 (H_2(e^{j\omega})=H_1(-e^{j\omega}))，设系统 (S_2) 的频率响应同样可以表示为 (H_2(e^{j\omega})=\left|H_2(e^{j\omega})\right|e^{j\theta_2(\omega)})，试写出单位脉冲响应 (h_2(n))，以及 \(\left|H_2(e^{j\omega})\right|\) 和 \(\theta_2(\omega)\) 的表达式。</p><p>（3）试分析系统 (S_1) 和系统 (S_2) 的滤波特性。</p></section>'''


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2025 年真题</span><span>详解见 P.____</span></div><p>八、已知某因果稳定的 LSI 系统 \(S_1\) 的差分方程如下</p><div class="formula">\[y(n)=\frac{1}{4}\left[x(n)-x(n-1)+x(n+2)-x(n-3)\right]\]</div><p>假设系统函数为 \(H_1(z)\)，求系统的频谱响应为 \(H_1(e^{j\omega})\)，单位脉冲响应为 \(h(n)\)。</p><p>（1）设系统 \(S_1\) 的频率响应表达式为 \(H_1(e^{j\omega})=\left|H_1(e^{j\omega})\right|e^{j\theta_1(\omega)}\)，其中 \(\left|H_1(e^{j\omega})\right|\) 为振幅响应，\(\theta_1(\omega)\) 为相位响应，请写出 \(\left|H_1(e^{j\omega})\right|\) 和 \(\theta_1(\omega)\) 的表达式。</p><p>（2）假设有一个系统 \(S_2\)，该系统的频率响应为 \(H_2(e^{j\omega})\)，且有 \(H_2(e^{j\omega})=H_1(-e^{j\omega})\)，设系统 \(S_2\) 的频率响应同样可以表示为 \(H_2(e^{j\omega})=\left|H_2(e^{j\omega})\right|e^{j\theta_2(\omega)}\)，试写出单位脉冲响应 \(h_2(n)\)，以及 \(\left|H_2(e^{j\omega})\right|\) 和 \(\theta_2(\omega)\) 的表达式。</p><p>（3）试分析系统 \(S_1\) 和系统 \(S_2\) 的滤波特性。</p></section>'''


def _answers_html_raw() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2025 年真题：频移系统的幅相响应</h2><p>由差分方程直接得到冲激响应与频率响应：</p><div class="formula">\[\begin{aligned}h_1[n]&=\frac{1}{4}\left[\delta[n]-\delta[n-1]+\delta[n+2]-\delta[n-3]\right],\\H_1(e^{j\omega})&=\frac{1}{4}\left(1-e^{-j\omega}+e^{j2\omega}-e^{-j3\omega}\right).\end{aligned}\]</div><p>将指数项按共轭对配对，可把幅度和相位因子明确分离：</p><div class="formula">\[H_1(e^{j\omega})=j e^{-j\frac{\omega}{2}}\cos\omega\sin\left(\frac{3\omega}{2}\right).\]</div><p>因此</p><div class="formula">\[\left|H_1(e^{j\omega})\right|=\left|\cos\omega\sin\left(\frac{3\omega}{2}\right)\right|,\qquad \theta_1(\omega)=\frac{\pi}{2}-\frac{\omega}{2}+\begin{cases}0,&\cos\omega\sin\left(\frac{3\omega}{2}\right)\ge0,\\\pi,&\cos\omega\sin\left(\frac{3\omega}{2}\right)<0.\end{cases}\pmod {2\pi}.\]</div><p>对系统 (S_2)，有 \(-e^{j\omega}=e^{j(\omega-\pi)}\)，所以这是把 (S_1) 的频率响应平移 \(\pi\) 的结果：</p><div class="formula">\[\begin{aligned}H_2(e^{j\omega})&=H_1\left(e^{j(\omega-\pi)}\right),\\h_2[n]&=(-1)^nh_1[n],\\\left|H_2(e^{j\omega})\right|&=\left|H_1\left(e^{j(\omega-\pi)}\right)\right|,\qquad\theta_2(\omega)=\theta_1(\omega-\pi).\end{aligned}\]</div><p>由 \(\left|H_1(e^{j\omega})\right|\) 可见，(S_1) 在直流处为零、在 \(\omega=\pm\frac{\pi}{2}\) 与 \(\omega=\pm\frac{2\pi}{3}\) 也有陷波，而 \(\omega=\pi\) 附近响应较强，属于高频通过为主且带多个阻带零点的频率选择系统。(S_2) 是其频谱平移 \(\pi\) 后的版本：高低频选择关系对调，低频附近响应较强，同时保留相应移位后的陷波位置。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2025 年真题：频移系统的幅相响应</h2><p>由差分方程直接得到冲激响应与频率响应：</p><div class="formula">\[\begin{aligned}h_1[n]&=\frac{1}{4}\left[\delta[n]-\delta[n-1]+\delta[n+2]-\delta[n-3]\right],\\H_1(e^{j\omega})&=\frac{1}{4}\left(1-e^{-j\omega}+e^{j2\omega}-e^{-j3\omega}\right).\end{aligned}\]</div><p>将指数项按共轭对配对，可把幅度和相位因子分离：</p><div class="formula">\[H_1(e^{j\omega})=j e^{-j\frac{\omega}{2}}\cos\omega\sin\left(\frac{3\omega}{2}\right).\]</div><p>幅度为</p><div class="formula">\[\left|H_1(e^{j\omega})\right|=\left|\cos\omega\sin\left(\frac{3\omega}{2}\right)\right|.\]</div><p>令 \(q(\omega)=\cos\omega\sin\left(\frac{3\omega}{2}\right)\)，则相位写为</p><div class="formula">\[\theta_1(\omega)=\frac{\pi}{2}-\frac{\omega}{2}+\begin{cases}0,&q(\omega)\ge0,\\\pi,&q(\omega)<0.\end{cases}\pmod{2\pi}\]</div><p>对系统 \(S_2\)，有 \(-e^{j\omega}=e^{j(\omega-\pi)}\)，所以这是把 \(S_1\) 的频率响应平移 \(\pi\) 的结果：</p><div class="formula">\[H_2(e^{j\omega})=H_1\left(e^{j(\omega-\pi)}\right),\qquad h_2[n]=(-1)^nh_1[n].\]</div><div class="formula">\[\left|H_2(e^{j\omega})\right|=\left|H_1\left(e^{j(\omega-\pi)}\right)\right|,\qquad\theta_2(\omega)=\theta_1(\omega-\pi).\]</div><p>由 \(\left|H_1(e^{j\omega})\right|\) 可见，\(S_1\) 在直流处为零、在 \(\omega=\pm\frac{\pi}{2}\) 与 \(\omega=\pm\frac{2\pi}{3}\) 也有陷波，而 \(\omega=\pi\) 附近响应较强，属于高频通过为主且带多个阻带零点的频率选择系统。\(S_2\) 是其频谱平移 \(\pi\) 后的版本：高低频选择关系对调，低频附近响应较强，同时保留相应移位后的陷波位置。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
