"""Reader-facing appendices assembled from the verified body and original drills."""
from __future__ import annotations

import re


STYLE = r"""
.appendix{break-before:page}
.appendix h1{break-before:auto}
.appendix h2{break-before:auto;margin-top:16pt}
.appendix-formula-group{break-inside:avoid;margin:0 0 12pt}
.appendix-c-question{break-inside:avoid;margin:0 0 14pt}
.appendix-c-question h2{font-size:14pt;margin:0 0 7pt}
.appendix-c-answer{margin:7pt 0 0;padding-left:12pt;border-left:1.2pt solid #b08d57}
.appendix-checklist{columns:2;column-gap:22pt;margin:8pt 0}
.appendix-checklist li{break-inside:avoid;margin:0 0 6pt}
"""


def _chapter_formula_groups(body: str) -> str:
    groups: list[str] = []
    summaries = re.finditer(
        r'<section class="chapter-formula-summary">(.*?)</section>', body, flags=re.DOTALL
    )
    for summary in summaries:
        headings = list(re.finditer(r"<h1>(.*?)</h1>", body[: summary.start()], flags=re.DOTALL))
        if not headings:
            raise ValueError("chapter body is missing its formula summary")
        formulas = re.findall(r'<div class="formula">.*?</div>', summary.group(1), flags=re.DOTALL)
        if not formulas:
            raise ValueError("chapter formula summary is empty")
        groups.append(
            '<section class="appendix-formula-group">'
            f"<h2>{headings[-1].group(1)}</h2>{''.join(formulas)}</section>"
        )
    if len(groups) != 8:
        raise ValueError(f"expected eight chapter formula groups, found {len(groups)}")
    return "".join(groups)


def appendix_a_html(body: str) -> str:
    return (
        '<section class="appendix appendix-a"><h1>附录 A：常用公式与变换对速查</h1>'
        "<p>按正文八章汇集核心公式与变换关系；每式均保留正式数学排版，便于复习时快速检索。</p>"
        f"{_chapter_formula_groups(body)}</section>"
    )


def appendix_b_html() -> str:
    return r'''
<section class="appendix appendix-b"><h1>附录 B：考研标准答题模板</h1>
<h2>系统性质判断模板</h2>
<ol><li>先写清输入、输出及自变量；对线性系统，代入 (a x_1+b x_2) 并比较 (a y_1+b y_2)。</li><li>对时不变性，比较输入移位 (x[n-n_0]) 的输出与原输出 (y[n-n_0])。</li><li>对因果性，检查 (y[n_0]) 是否只依赖 (nle n_0) 的输入；对 BIBO 稳定性，检查有界输入是否必得有界输出。</li></ol>
<h2>z 变换与 ROC 模板</h2>
<ol><li>先写 (X(z)=sum_n x[n]z^{-n})，再写 ROC；ROC 必须单独说明，不能只给代数式。</li><li>由极点位置、因果性和稳定性共同确定 ROC；因果序列取最外极点之外，反因果序列取最内极点之内。</li><li>逆变换时先做部分分式展开，再根据 ROC 决定每项对应右边序列还是左边序列。</li></ol>
<h2>DFT 计算与循环卷积模板</h2>
<ol><li>先写长度 (N) 与定义 (X[k]=sum_{n=0}^{N-1}x[n]W_N^{nk})。</li><li>利用周期性、共轭对称性和已知变换对减少计算；索引统一使用 (x\left((n-m)\right)_N) 的周期下标格式。</li><li>循环卷积题先判定长度；只有补零到 (Nge L_x+L_h-1) 时，循环卷积才与线性卷积一致。</li></ol>
<h2>IIR／FIR 设计模板</h2>
<ol><li>IIR 题先列频率映射、预畸变和模拟原型，再给出数字系统函数与稳定性检查。</li><li>FIR 题先判定线性相位类型与长度奇偶，再写群延迟、频率采样或窗函数参数，最后说明幅相特性。</li><li>结构题由系统函数或差分方程反查每个延时、增益、加法器和反馈支路，确保可反推出原式。</li></ol>
</section>'''


_COMPREHENSIVE_DRILLS = (
    ("第一章", r"已知 (x[n]=u[n]-u[n-4])，(h[n]=(\tfrac12)^n u[n])。求 (y[n]=x[n]*h[n])，并说明卷积和的有效范围。", r"由 (x[m]) 仅在 (0le mle3) 非零，故 (y[n]=sum_{m=0}^{min(n,3)}(\tfrac12)^{n-m})，且 (n<0) 时为零。分别化简得 (0le nle3) 时 (y[n]=2(1-2^{-(n+1)}))，(nge4) 时 (y[n]=15\cdot2^{-(n+1)})。"),
    ("第二章", r"给定 (H(z)=\frac{1-2z^{-1}}{1-\tfrac12z^{-1}})。分别给出因果实现的 ROC，并判断稳定性。", r"唯一极点为 (z=\tfrac12)。因果实现的 ROC 为 (left|z\right|>\tfrac12)，包含单位圆，因此系统 BIBO 稳定。零点 (z=2) 不决定 ROC。"),
    ("第三章", r"对 (x[n]=\{1,0,-1,0\}) 作 4 点 DFT，求 (X[k])。", r"直接代入 (W_4=e^{-j\pi/2})：(X[0]=0)，(X[1]=2)，(X[2]=0)，(X[3]=2)。结果为实偶序列的离散频谱，两个非零谱线位于 (k=1,3)。"),
    ("第四章", r"8 点基 2 DIT-FFT 的旋转因子 (W_8^2) 等于多少？说明其在蝶形单元中的作用。", r"(W_8^2=e^{-j2\pi\cdot2/8}=e^{-j\pi/2}=-j)。它乘在规定的下支路上，再与上支路做加、减组合；旋转因子的位置由 DIT 的分解顺序确定，不能随意交换。"),
    ("第五章", r"系统满足 (y[n]=x[n]+x[n-1]-\tfrac12y[n-1])。写出 (H(z))，并说明实现所需的基本元件。", r"零初始条件下 (H(z)=\frac{1+z^{-1}}{1+\tfrac12z^{-1}})。结构至少含一个 (z^{-1}) 延时器、前向系数 (1,1)、反馈系数 (-\tfrac12) 与标准求和节点；反馈支路应回到求和器输入端。"),
    ("第六章", r"双线性变换把模拟域的稳定区域映射到数字域的什么区域？为何需要预畸变？", r"左半 (s) 平面映射到单位圆内。映射 (omega=2\tan^{-1}(\Omega T/2)) 是非线性的，会产生频率扭曲；预畸变先把关键数字频率映回模拟频率，以保证关键频点准确。"),
    ("第七章", r"设计长度 (N=33) 的线性相位低通 FIR，选择哪一类线性相位类型？群延迟是多少？", r"(N) 为奇数且低通在直流处需允许非零增益，应选 I 型偶对称 FIR。群延迟为 ((N-1)/2=16)。奇对称类型会在直流处受零值约束，不适合作一般低通。"),
    ("第八章", r"信号先上采样 (L=2)，再下采样 (M=3)。若输入采样率为 (f_s)，输出采样率是多少？说明中间滤波的任务。", r"输出采样率为 \(\frac{2}{3}f_s\)。上采样后先用插值低通滤波器去除镜像；下采样前用抗混叠低通滤波器限制带宽，防止频谱折叠。"),
)


def appendix_c_html() -> str:
    drills: list[str] = []
    for chapter, prompt, answer in _COMPREHENSIVE_DRILLS:
        drills.append(
            '<section class="appendix-c-question"><h2>'
            f"{chapter}综合训练</h2><p>{prompt}</p>"
            f'<div class="appendix-c-answer"><strong>解：</strong>{answer}</div></section>'
        )
    return (
        '<section class="appendix appendix-c"><h1>附录 C：分章综合训练与详细解答</h1>'
        "<p>以下题目为与正文例题、章末真题去重的综合训练；每章一题，用于串联核心概念。</p>"
        f"{''.join(drills)}</section>"
    )


def appendix_d_html() -> str:
    return r'''
<section class="appendix appendix-d"><h1>附录 D：考前高频公式与检查表</h1>
<div class="formula">\[f_s=\frac{1}{T},\qquad \Omega_s=\frac{2\pi}{T}\]</div>
<div class="formula">\[X[k]=\sum_{n=0}^{N-1}x[n]W_N^{nk},\qquad x[n]=\frac1N\sum_{k=0}^{N-1}X[k]W_N^{-nk}\]</div>
<div class="formula">\[Y(z)=H(z)X(z),\qquad H\left(e^{j\omega}\right)=H(z)\big|_{z=e^{j\omega}}\]</div>
<div class="formula">\[\omega=2\tan^{-1}\!\left(\frac{\Omega T}{2}\right),\qquad \tau_g=\frac{N-1}{2}\]</div>
<h2>计算题检查</h2><ul class="appendix-checklist"><li>变换式、ROC 和因果／稳定条件是否同时写出？</li><li>DFT 长度、补零长度和循环下标是否明确？</li><li>幅度、相位、频率单位及主值范围是否一致？</li><li>FIR 类型、群延迟和端点约束是否匹配？</li><li>IIR 的预畸变、频率映射和稳定区域是否核对？</li><li>结构图能否反向写回原差分方程？</li></ul>
</section>'''


def appendix_i_html() -> str:
    return '''
<section class="appendix appendix-i"><h1>附录 I：全书自测与考场检查</h1>
<h2>八章闭环自测</h2><ol><li>能否由序列定义判断周期性、偶奇性与支集？</li><li>能否由 ROC 判断 z 变换对应的序列方向、因果性和稳定性？</li><li>能否写出 DFT、IDFT、循环卷积与线性卷积的边界条件？</li><li>能否区分 DIT、DIF 的输入／输出顺序与旋转因子位置？</li><li>能否由差分方程画出正确的直接型或转置型结构？</li><li>能否说明脉冲响应不变法与双线性变换的关键差别？</li><li>能否由对称性和长度判断四类线性相位 FIR？</li><li>能否说明抽取、内插中的镜像与混叠抑制位置？</li></ol>
<h2>最后两分钟检查表</h2><ul class="appendix-checklist"><li>每个小问均有结论，且单位、索引范围、ROC 未遗漏。</li><li>公式中的分式、上下标、共轭、负号和括号均已核对。</li><li>图形的横纵轴、原点、箭头、关键频点和样值标注清楚。</li><li>若使用性质，已写出适用条件，不把线性卷积与循环卷积混用。</li><li>计算结果已用对称性、长度或极限情况交叉检查。</li><li>答题区域内无相互矛盾的中间结论。</li></ul>
</section>'''


def pre_answer_appendices_html(body: str) -> str:
    return "".join((appendix_a_html(body), appendix_b_html(), appendix_c_html(), appendix_d_html()))
