from pathlib import Path
import re


def test_formula_names_state_the_formula_name_and_its_reader_facing_use():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(r"\[f_s\geq2f_h\]", "离散时间信号的由来") == (
        "奈奎斯特采样条件（用于确定避免频谱混叠的最低采样频率）"
    )
    assert _formula_name(r"\[W(e^{j\omega})=X(e^{j(\omega-\pi)})\]", "真题详解") == (
        "离散时间频移关系（用于说明时域交替变号会使频谱平移 π）"
    )
    assert _formula_name(r"\[Y(e^{j\omega})=\begin{cases}\frac{1}{T},&0.5\pi\leq|\omega|\leq\pi\\0,&\text{其他}\end{cases}\]", "真题详解") == (
        "滤波后的输出频谱（用于给出通带内外的频谱幅度）"
    )
    assert _formula_name(r"\[\Delta f_0'=\frac{f_h}{r}\geq\Delta f_0,\quad r\in\mathbb{Z},\quad f_s=2\Delta f_0'\]", "采样") == (
        "采样频率的可行性条件（用于判断哪些采样频率不会产生频谱混叠）"
    )
    assert _formula_name(r"\[H_r(j\Omega)=\begin{cases}T,&|\Omega|\leq\frac{\Omega_s}{2}\\0,&|\Omega|>\frac{\Omega_s}{2}\end{cases}\]", "重构") == (
        "理想低通重构滤波器的频率响应（用于保留中心频谱副本并抑制其他副本）"
    )
    assert _formula_name(r"\[E_x=\frac{1}{2\pi}\int_{-\pi}^{\pi}|X(e^{j\omega})|^2\,\mathrm{d}\omega<\infty\]", "能量") == (
        "能量信号的频域能量关系（用于由频谱判定信号能量是否有限）"
    )
    assert _formula_name(r"\[X^*(e^{j\omega})=X(e^{-j\omega})\]", "实序列性") == (
        "实序列频谱的共轭对称关系（用于由正频率部分判断负频率部分）"
    )


def test_full_main_body_assembly_contains_eight_chapters_without_training(tmp_path: Path):
    from full.tools.build_all_main_body import write_html

    html = write_html(tmp_path / "dsp-main-body.html").read_text(encoding="utf-8")

    for heading in (
        "第一章 离散时间信号与系统",
        "z 变换的基本概念",
        "第三章 离散傅里叶变换",
        "4.1 直接计算 DFT 的问题及改进途径",
        "第五章 数字滤波器结构",
        "第六章 IIR 数字滤波器设计",
        "第七章 FIR 数字滤波器设计",
        "第八章 多采样率数字信号处理",
    ):
        assert heading in html
    assert html.count("<main>") == 1
    assert html.count('class="chapter-start"') == 8
    assert html.count("<h1>") == 8
    assert "<h1>第四章 快速傅里叶变换</h1>" in html
    assert "<h2>4.1 直接计算 DFT 的问题及改进途径</h2>" in html
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "page-break-after:always" not in html
    assert ".chart-grid{display:grid" in html
    assert "grid-template-columns:repeat(2,minmax(0,1fr))" in html
    assert ".grid{display:grid" in html
    assert ".mapping th,.mapping td,.table th,.table td{border:.45pt solid" in html
    assert ".table{break-inside:auto}" in html
    assert ".table tr{break-inside:avoid}" in html
    assert ".source-figure.compact{max-width:156mm}" in html
    assert ".source-figure-flow{break-inside:auto;max-width:156mm;margin:8pt auto}" in html
    assert ".formula mjx-container[display=\"true\"]" in html
    assert ".structure-svg .wire{fill:none;stroke:#174b73" in html
    assert ".structure-svg .block{fill:#f4f7f8;stroke:#0d8794" in html
    assert ".spectrum-svg .replica{fill:none;stroke-width:3" in html
    assert ".chain-svg .chain-box{fill:#f4f7f8;stroke:#b08d57" in html
    assert ".wheel-svg .wheel-rim{fill:none;stroke:#b6342d" in html
    assert ".multirate-svg .spectrum-a{fill:none;stroke:#0d8794" in html
    assert ".multirate-svg .spectrum-b{fill:none;stroke:#b56b2e" in html
    assert ".signal-svg .hold{fill:none;stroke:#0f8b8d;stroke-width:3" in html
    assert ".zero-order-hold-flow{break-inside:avoid;max-width:145mm}" in html
    assert "typical-sequence-continuation" in html
    assert ".typical-sequence-continuation .chart{break-inside:auto" in html
    assert ".typical-sequence-continuation .chart svg{max-width:500px!important}" in html
    assert 'data-first-sample-clearance=' not in html
    assert 'data-origin-at-zero="true"' in html
    assert 'data-origin-label="true"' in html
    assert '@top-left{content:"数字信号处理讲义"' in html
    assert '@top-right{content:string(running-title,first)' in html
    assert '@bottom-center{content:counter(page)' in html
    assert 'string-set:running-title content(text)' in html


def test_full_main_body_places_a_deduplicated_formula_summary_at_each_chapter_end(tmp_path: Path):
    from full.tools.build_all_main_body import write_html

    html = write_html(tmp_path / "dsp-main-body.html").read_text(encoding="utf-8")

    summaries = re.findall(
        r'<section class="chapter-formula-summary">(.*?)</section>', html, flags=re.DOTALL
    )
    assert len(summaries) == 8
    assert html.count("本章公式总表") == 8
    assert 'class="formula-name">连续信号的离散采样关系（用于把连续时间信号转为离散序列）：' in html
    assert all(r"\[" in summary and r"\]" in summary for summary in summaries)
    assert "x(n)=x_a(nT)" in summaries[0]
    assert "H(z)" in summaries[1]
    assert r"L\geq N+M-1" in summaries[3]


def test_formula_summary_flows_into_preceding_page_when_space_remains(tmp_path: Path):
    from full.tools.build_all_main_body import write_html

    html = write_html(tmp_path / "dsp-main-body.html").read_text(encoding="utf-8")

    assert ".chapter-formula-summary{break-before:page}" not in html
    assert ".chapter-formula-summary{break-before:auto}" in html


def test_formula_names_describe_the_formula_instead_of_its_chapter():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(r"X(\omega)=\int_{-\infty}^{\infty}x(t)e^{-j\omega t}\,\mathrm{d}t", "第三章 傅里叶变换")

    assert label == "连续时间傅里叶变换定义（用于把时域连续信号变换到频域）"
    assert "第三章" not in label
    assert "核心关系" not in label


def test_formula_name_identifies_a_listed_discrete_sequence():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"x_1(n)=\{1,2,3,4,5\},\qquad x_2(n)=\{1,2,3,4,5\}",
        "用数列与函数表示",
    )

    assert label == "离散序列的数列表达（用于列出各离散时刻的样值）"


def test_formula_name_explains_the_reader_use_for_a_section_specific_formula():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(r"A=B", "第三章 3.2 DFT 的基本性质")

    assert label == "DFT 基本性质关系（用于根据时域运算快速推导对应的频域结果）"
    assert "第三章" not in label
    assert "用于说明该性质中各变量的对应关系" not in label


def test_formula_name_does_not_mislabel_bilinear_transform_as_linearity():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\Omega=\frac{2}{T}\tan\frac{\omega}{2}",
        "6.4 双线性变换法",
    )

    assert label == "双线性变换的频率映射关系（用于在模拟和数字频率之间建立非线性对应）"


def test_formula_name_uses_formula_specific_labels_before_a_linear_heading():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (
            r"\mathcal{Z}\{x(n-m)\}=z^{-m}X(z)",
            "线性与时移性质",
            "z 变换的时移性质（用于由原序列的 z 变换求时移序列的 z 变换）",
        ),
        (
            r"x\left((n-n_0)\right)_N\longleftrightarrow W_N^{kn_0}X(k)",
            "DFT 的线性与循环移位",
            "DFT 的循环时移性质（用于由循环移位后的序列快速得到频谱相位因子）",
        ),
        (
            r"h(n)=\pm h(N-1-n),\qquad 0\leq n\leq N-1",
            "线性相位 FIR 数字滤波器的条件和特点",
            "线性相位 FIR 的对称条件（用于判定有限长滤波器能否具有线性相位）",
        ),
    )

    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_alignment_and_spacing_in_linear_topic_formulae():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"T[a x_1+b x_2]=(a x_1+b x_2)^2=a^2x_1^2+b^2x_2^2+2abx_1x_2",
        "系统线性",
    ) == "非线性系统的叠加检验（用于展开平方运算中的交叉项）"
    assert _formula_name(
        r"\begin{aligned}x(n)&=\cos(\omega_0n)u(n),\\X(z)&=\frac{1-\cos(\omega_0)z^{-1}}{1-2\cos(\omega_0)z^{-1}+z^{-2}}\end{aligned}",
        "线性系统的 z 变换",
    ) == "因果余弦序列的 z 变换（用于求含单位阶跃余弦序列的系统函数）"
    assert _formula_name(
        r"\begin{aligned}h(n)&=\delta(n-\tau),&y(n)&=x(n-\tau),\\H\!\left(e^{j\omega}\right)&=e^{-j\tau\omega},&\tau_g(\omega)=\tau.\end{aligned}",
        "线性相位",
    ) == "理想延时系统的线性相位关系（用于说明群延迟等于固定延时时间）"


def test_formula_name_does_not_mislabel_fir_factorization_or_difference_equation():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"H(z)=\left(1-ae^{j\theta}z^{-1}\right)\left(1-ae^{-j\theta}z^{-1}\right)",
        "2019 年真题：二阶 FIR 的零点与线性相位",
    ) == "二阶 FIR 的零点因式分解（用于由因子直接确定共轭零点位置）"
    assert _formula_name(
        r"y(n)=x(n)-2a\cos\theta\,x(n-1)+a^2x(n-2)",
        "2019 年真题：二阶 FIR 的零点与线性相位",
    ) == "二阶 FIR 的差分方程（用于按当前与延迟输入计算滤波器输出）"


def test_formula_name_identifies_specific_design_and_decomposition_formulae():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"h(n)=3\delta(n)+2\delta(n-1)+\delta(n-2)",
        "真题整理详解",
    ) == "有限长单位脉冲响应（用于列出 FIR 系统各延时抽头的权重）"
    assert _formula_name(
        r"\operatorname{ROC}:\quad 0<\left|z\right|<\infty",
        "真题整理详解",
    ) == "有限长序列的收敛域（用于说明 z 变换在非零有限 z 平面内收敛）"
    assert _formula_name(
        r"H_{\mathrm{ap}}(z)=\frac{z-3}{3z-1},\qquad H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)",
        "真题整理详解",
    ) == "最小相位与全通分解（用于把系统分解为最小相位部分和全通部分）"
    assert _formula_name(
        r"p=\frac{s^2+\Omega_0^2}{Bs}",
        "真题整理详解",
    ) == "低通到带通的频率变换（用于由模拟低通原型构造带通滤波器）"
    assert _formula_name(
        r"h_d(n)=\begin{cases}\dfrac{\sin[\omega_c(n-\tau)]}{\pi(n-\tau)},&n\ne\tau\\\dfrac{\omega_c}{\pi},&n=\tau\end{cases}\qquad h(n)=h_d(n)w_{\mathrm{Ham}}(n)",
        "窗函数法设计 FIR 滤波器",
    ) == "窗函数法 FIR 系数（用于用哈明窗截断理想低通冲激响应）"
    assert _formula_name(
        r"w_C(n)=\begin{cases}\dfrac{1}{2}\left[1-\cos\!\left(\dfrac{2\pi n}{N-1}\right)\right],&0\le n\le N-1,\\0,&\text{其他},\end{cases}\qquad h(n)=h_d(n)w_C(n)",
        "余弦窗",
    ) == "余弦（Hann）窗系数（用于对理想冲激响应加窗以抑制频谱泄漏）"
    assert _formula_name(
        r"g(0)=1,\qquad g(kT)=0\quad\left(k\in\mathbb{Z},\ k\ne 0\right)",
        "采样点处的严格插值",
    ) == "插值函数的抽样性质（用于保证每个重构样点只保留对应的插值项）"
    assert _formula_name(
        r"y_a(mT)=x_a(mT)",
        "采样点处的严格插值",
    ) == "重构信号的插值一致性（用于验证恢复信号准确通过全部采样值）"


def test_formula_name_handles_html_escaped_inequalities_and_alignment_markers():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"T[x_1+x_2]\ne T[x_1]+T[x_2]",
        "反例",
    ) == "非线性系统的叠加判定（用于通过输出和的不一致证明系统不满足线性）"
    assert _formula_name(
        r"0.0628&lt;\omega_c&lt;0.5\pi",
        "采样与恢复",
    ) == "低通截止频率选取范围（用于在保留低频分量时抑制高频分量）"
    assert _formula_name(
        r"\begin{aligned}\omega_p&=2\pi\frac{f_p}{f_s},&\Delta\omega&=\left|\omega_{st}-\omega_p\right|\end{aligned}",
        "FIR 设计",
    ) == "FIR 设计的归一化频率指标（用于确定通带、阻带与过渡带宽度）"


def test_formula_name_replaces_generic_sampling_parameter_labels():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (
            r"f_h\leq\frac{f_s}{2}\qquad\Longleftrightarrow\qquad\Omega_h\leq\frac{\Omega_s}{2}",
            "采样定理的工程应用",
            "带限信号的无混叠采样条件（用于由最高频率确定最低采样率）",
        ),
        (
            r"f_0=f_h-\frac{\Delta f_0}{2}",
            "带通信号采样",
            "带通信号的中心频率（用于由最高频率和带宽确定频带位置）",
        ),
        (
            r"T\downarrow\quad\Longrightarrow\quad f_s=\frac{1}{T}\uparrow",
            "采样与保持",
            "采样间隔与采样率的倒数关系（用于说明缩短采样间隔会提高采样率）",
        ),
        (
            r"T_0=NT,\qquad f_s=\frac{1}{T},\qquad F_0=\frac{1}{T_0},\qquad f_s=NF_0",
            "采样参数与频率分辨率",
            "记录长度与频率分辨率关系（用于由样本数和采样周期确定频率间隔）",
        ),
        (
            r"X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}},\qquad k=0,1,\ldots,N-1",
            "频域采样",
            "DFT 的等间隔频率取样关系（用于确定每个 DFT 样值在 DTFT 上的频率位置）",
        ),
        (
            r"\widetilde{x}(n)=x(n),\quad0\leq n\leq M-1,\qquad N\geq M",
            "DFT 的周期延拓",
            "零填充的无时域混叠条件（用于保证周期延拓副本不重叠）",
        ),
        (
            r"F_s'=\frac{L}{M}F_s",
            "有理数倍采样率变换",
            "有理数倍采样率变换关系（用于计算变换后的采样率）",
        ),
        (
            r"H\!\left(e^{j\omega}\right)=\begin{cases}L,&0\leq\left|\omega\right|<\omega_c\\0,&\omega_c\leq\left|\omega\right|\leq\pi\end{cases}\qquad\omega_c=\min\!\left(\frac{\pi}{L},\frac{\pi}{M}\right)",
            "有理数倍采样率变换",
            "有理数倍变换的抗影像抗混叠滤波器（用于同时限制上采样影像和下采样混叠）",
        ),
        (
            r"\frac{147}{160}=\frac{7}{8}\cdot\frac{7}{5}\cdot\frac{3}{4}",
            "多级采样率变换",
            "多级有理数倍分解（用于把总采样率变换拆为低复杂度级联）",
        ),
        (
            r"44100=294\cdot50\cdot3,\qquad44056=245\cdot59.94\cdot3",
            "44.1 kHz 的由来",
            "44.1 kHz 的制式分解（用于说明采样率与 PAL、NTSC 扫描体制的匹配）",
        ),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_replaces_generic_foundation_formula_labels():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (
            r"\frac{2\pi}{\omega}=\frac{N}{k},\qquad N,k\in\mathbb{Z}_{+},\qquad\gcd(N,k)=1",
            "离散序列的周期性",
            "离散正弦序列的周期判定条件（用于求最小整数周期）",
        ),
        (
            r"T[x_1(n)+x_2(n)]=T[x_1(n)]+T[x_2(n)]",
            "系统的线性",
            "系统线性的可加性条件（用于检验两个输入之和的输出）",
        ),
        (
            r"T[a x_1(n)]=aT[x_1(n)]",
            "系统的线性",
            "系统线性的齐次性条件（用于检验输入缩放后的输出）",
        ),
        (
            r"T[a x_1(n)+b x_2(n)]=a y_1(n)+b y_2(n)",
            "叠加原理",
            "系统线性的叠加原理（用于同时检验可加性和齐次性）",
        ),
        (
            r"y(n)=T[x(n)]\quad\Longrightarrow\quad T[x(n-k)]=y(n-k),\qquad\forall k\in\mathbb{Z}",
            "时不变系统",
            "时不变系统的时移关系（用于检验输入时移是否引起同样的输出时移）",
        ),
        (
            r"x(n)*\delta(n-n_0)=x(n-n_0)",
            "图解卷积步骤",
            "单位脉冲卷积的时移性质（用于快速得到序列与移位冲激的卷积结果）",
        ),
        (
            r"x(n)*h(n)=h(n)*x(n)",
            "卷积的运算规律",
            "卷积的交换律（用于交换两个卷积序列的计算次序）",
        ),
        (
            r"\bigl[x(n)*h_1(n)\bigr]*h_2(n)=x(n)*\bigl[h_1(n)*h_2(n)\bigr)",
            "卷积的运算规律",
            "卷积的结合律（用于改变多级系统的级联分组）",
        ),
        (
            r"x(n)*[h_1(n)+h_2(n)]=x(n)*h_1(n)+x(n)*h_2(n)",
            "卷积的运算规律",
            "卷积的分配律（用于展开并联支路的总输出）",
        ),
        (
            r"r_{xy}(n)=x(n)*y(-n),\qquad r_{yx}(n)=y(n)*x(-n)",
            "相关",
            "互相关的卷积表示（用于计算两个序列不同移位下的相似度）",
        ),
        (
            r"r_{xx}(n)=x(n)*x(-n)",
            "相关",
            "自相关的卷积表示（用于衡量序列与其时移副本的相似度）",
        ),
        (
            r"\omega=\Omega T=2\pi\frac{f}{f_s}",
            "频率换算",
            "模拟频率与数字频率的换算关系（用于把赫兹或模拟角频率换算为数字角频率）",
        ),
        (
            r"x_a(t)\longrightarrow x(n)\longrightarrow y(n)\longrightarrow y_a(t)",
            "模拟信号的数字处理方法",
            "模拟信号的数字处理链（用于表示采样、数字处理和重构的先后顺序）",
        ),
        (
            r"\Omega_s\geq2\Omega_c,\qquad f_s=\frac{1}{T}",
            "模拟到数字",
            "抗混叠采样条件与采样率定义（用于设置模数转换前的滤波和采样参数）",
        ),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_replaces_actual_first_chapter_generic_fallbacks():
    """Real formulas from the generated first chapter must not hit the generic fallback."""
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (
            r"x(n)=A\cos\left(\frac{3\pi}{7}n\right),\qquad \frac{2\pi}{\omega}=\frac{2\pi}{3\pi/7}=\frac{14}{3},\qquad N=14",
            "有理性判据",
            "离散正弦序列的周期求解（用于由角频率的有理比确定基本周期）",
        ),
        (
            r"T[x(n-k)]=y(n-k)",
            "判别步骤",
            "时不变系统的时移检验式（用于比较输入时移前后的输出是否同步平移）",
        ),
        (
            r"y(n)=3\delta(n)+8\delta(n-1)+5\delta(n-2)+2\delta(n-3)",
            "例题详解",
            "离散卷积的输出序列（用于列出各输出时刻的卷积结果）",
        ),
        (
            r"\begin{aligned}y(n)&=x(n)*[\delta(n)+\alpha\delta(n-R)]\\&=x(n)+\alpha x(n-R).\end{aligned}",
            "应用例：延时叠加系统",
            "双抽头回声系统的输入输出关系（用于表示原信号与延迟衰减副本的叠加）",
        ),
        (
            r"y(n)\longrightarrow y_0(t)\longrightarrow y_a(t)",
            "数模转换与零阶保持",
            "数模转换与零阶保持流程（用于说明离散输出经保持和重构得到连续信号）",
        ),
        (
            r"\left.\sin(2100\pi t)\right|_{t=nT}=\sin(2.1\pi n)=\sin(0.1\pi n)",
            "两个给出相同样值的连续信号",
            "采样混叠的等效离散正弦关系（用于说明高频连续信号可产生相同离散样值）",
        ),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_uses_specific_named_topic_before_generic_fallback():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"x(n)=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,\mathrm{d}z", "z 反变换", "z 反变换的围线积分定义（用于由 z 域函数恢复时域序列）"),
        (r"A_k=\left.(1-p_kz^{-1})X(z)\right|_{z=p_k}", "部分分式展开法", "部分分式展开的留数系数（用于把有理 z 函数拆成可直接反变换的简单项）"),
        (r"x_e(n)=\frac12[x(n)+x^*(-n)]", "共轭对称与分解", "共轭对称分量分解（用于把任意序列拆为共轭对称与共轭反对称部分）"),
        (r"X(e^{j\omega})=X^*(e^{-j\omega})", "实序列的频谱对称性", "实序列频谱的共轭对称关系（用于由正频率谱确定负频率谱）"),
        (r"z_k=e^{j(2\pi k/4+\pi/4)}", "例题：四抽头平均的零点分布", "四抽头平均滤波器的零点位置（用于在 z 平面定位频率响应的零点）"),
        (r"H(z)=\frac{1}{1-az^{-1}}", "收敛域与典型序列", "单极点 z 变换与收敛域关系（用于说明同一代数式在不同 ROC 下对应不同序列）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_transform_and_block_processing_topics():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"x(n)=\frac1N\sum_{k=0}^{N-1}X(k)e^{j2\pi kn/N}", "DFT 与 IDFT", "离散傅里叶反变换定义（用于由离散频谱重建周期序列）"),
        (r"x(n)=\sum_{k=0}^{N-1}a_ke^{jk\omega_0n}", "DFS 的变换对", "离散傅里叶级数综合式（用于由周期序列的频域系数恢复时域波形）"),
        (r"a_k=\frac1N\sum_{n=0}^{N-1}x(n)e^{-jk\omega_0n}", "DFS 的基本性质", "离散傅里叶级数分析式（用于计算周期序列的频域系数）"),
        (r"y_i(n)=\operatorname{IDFT}\{X_i(k)H(k)\}", "重叠保留法", "重叠保留法的块卷积输出（用于用 DFT 分块实现长序列线性卷积）"),
        (r"H(z)=\frac{Y(z)}{X(z)}", "系统函数及其与系统性质的关系", "系统函数的定义（用于在 z 域描述输入与输出的关系）"),
        (r"\omega=\Omega T=2\pi\frac{f}{f_s}", "折叠频率与三种频率", "模拟频率与数字频率的换算关系（用于把赫兹或模拟角频率换算为数字角频率）"),
        (r"X(z)=\frac{4}{3}\frac{z}{z-2}-\frac{1}{3}\frac{z}{z-0.5}", "有理函数的标准反变换对", "有理 z 函数的部分分式展开（用于按 ROC 选择相应的时域反变换）"),
        (r"x(n)=\cos(\omega_1n)+\cos(\omega_2n)", "DTMF 双音多频信号", "双音多频信号的合成表达式（用于由两个标准音频分量构造按键音）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_filter_design_named_topics():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"H(z)=\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{(z-re^{j\omega_0})(z-re^{-j\omega_0})}", "数字陷波器", "二阶陷波器的零极点表达式（用于由极点半径控制陷波带宽）"),
        (r"H(z)=\frac{1}{1-2r\cos\omega_0z^{-1}+r^2z^{-2}}", "数字谐振器", "二阶数字谐振器的系统函数（用于在指定频率附近形成窄带共振）"),
        (r"|H_a(j\Omega)|^2=\frac{1}{1+(\Omega/\Omega_c)^{2N}}", "巴特沃斯低通原型", "巴特沃斯低通原型的幅度平方响应（用于由截止频率和阶数确定平坦通带特性）"),
        (r"h(n)=Th_a(nT)", "脉冲响应不变法", "脉冲响应不变法的离散化关系（用于由模拟冲激响应构造数字 IIR 滤波器）"),
        (r"H(z)=\prod_{i=1}^L H_i(z)", "递归分解与运算量", "IIR 滤波器的级联分解（用于把高阶递归滤波器实现为多个低阶节）"),
        (r"H(k)=H(e^{j2\pi k/N})", "频率采样法", "频率采样设计的目标样值（用于指定各离散频率点的滤波器响应）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_remaining_design_and_efficiency_topics():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)", "逆系统与最小相位条件", "最小相位与全通因子的分解（用于把系统分离为可逆最小相位部分和全通部分）"),
        (r"X_N(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk}", "零填充的作用", "DFT 旋转因子关系（用于统一表示 DFT 中的复指数基函数）"),
        (r"h_{\mathrm{HP}}(n)=\delta(n)-h_{\mathrm{LP}}(n)", "高通、带通与带阻的理想单位抽样响应", "理想高通 FIR 的单位抽样响应（用于由低通原型构造高通滤波器）"),
        (r"C_{\mathrm{DFT}}=N^2", "规模为何会成为问题", "直接 DFT 的计算量（用于说明长序列频谱计算的复杂度增长）"),
        (r"x(n)=\sum_{m=1}^{M}x_m(n)", "频分复用", "频分复用信号的叠加表达式（用于表示多个频带信号在同一通道中的合成）"),
        (r"W_N=e^{-j2\pi/N}", "例题：512 点 DFT 的计算时间", "DFT 旋转因子关系（用于统一表示 DFT 中的复指数基函数）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_remaining_named_body_topics():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"|z|<|p_1|,\quad |p_1|<|z|<|p_2|", "给定极点时 ROC 的可能性", "有理 z 函数的候选收敛域（用于由极点模值判断左边、双边或右边序列）"),
        (r"W(e^{j\omega})=\sum_{n=0}^{N-1}w(n)e^{-j\omega n}", "观察实例：窗口长度与泄漏", "离散时间傅里叶变换定义（用于把离散序列变换到连续频率域）"),
        (r"H(z)=\frac{1-a}{1-az^{-1}}", "简单一阶低通与高通", "一阶低通滤波器的系统函数（用于通过极点位置控制低通平滑程度）"),
        (r"y(n)=\sum_i y_i(n-iM)", "例题：重叠相加法验证", "重叠相加法的输出合成式（用于把分块卷积的重叠样本相加为连续输出）"),
        (r"x(n)\longleftrightarrow X(k),\qquad X(n)\longleftrightarrow Nx((-k)_N)", "对偶性", "DFT 的对偶性质（用于交换时域序列和频域序列的角色）"),
        (r"X(z)=\sum_nx(n)z^{-n}", "其他常用性质", "z 变换定义（用于把离散序列表示为 z 域函数）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_remaining_actual_z_and_frequency_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"x(n)=\sin(0.1\pi n),\qquad T=\frac{1}{f_s}=1\,\mathrm{ms}", "同一组样值未必对应唯一连续信号", "离散样值与采样周期关系（用于说明仅凭样值不能唯一确定连续信号）"),
        (r"\text{右边序列：}\;|z|>|p_{\max}|", "四种典型序列的 ROC 形状", "典型序列的收敛域分类（用于按时间支持范围选择正确 ROC）"),
        (r"\frac{3z^{-1}}{(1-3z^{-1})^2}=3z^{-1}+18z^{-2}+\cdots", "幂级数展开法", "z 反变换的幂级数展开（用于由 z 的级数系数读取时域序列）"),
        (r"\omega=\Omega T=\frac{2\pi}{T_0}T=\frac{2\pi}{N_0}", "归一化角频率的换算", "归一化角频率换算关系（用于由连续周期和采样周期确定离散角频率）"),
        (r"z=e^{\pm j\omega_0},\qquad \omega_0=2\pi\frac{f_0}{f_s}", "数字陷波器", "陷波器零点的单位圆位置（用于将指定赫兹干扰频率映射为共轭零点）"),
        (r"Y(k)=W_4^{3k}X(k)", "例题：由频域相位因子恢复圆周移位序列", "DFT 循环时移的相位因子（用于由频域相位直接恢复时域循环移位）"),
        (r"y(n)=x(n)+\alpha x(n-R)+\alpha^2x(n-2R)", "离散时间信号与系统", "多回声延时叠加模型（用于表示多次衰减回声的输出序列）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_first_chapter_signal_properties():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"x(n)=A\sin(n\omega+\varphi),\qquad N\omega=2k\pi", "离散时间信号与系统", "离散正弦序列的周期条件（用于由角频率求整数基本周期）"),
        (r"x(n)=e^{j(\frac{n}{6}-\pi)},\qquad \frac{2\pi}{\omega}=12\pi\notin\mathbb{Q}", "离散时间信号与系统", "无周期复指数序列的判据（用于说明角频率无理比时不存在整数周期）"),
        (r"x(n)=A[1+m\cos(\omega_Ln)]\cos(\omega_Hn)", "离散时间信号与系统", "离散调幅信号模型（用于表示低频包络调制高频载波）"),
        (r"y(n)=x(2n)", "离散时间信号与系统", "离散时间尺度变换（用于表示按两倍索引抽取的序列）"),
        (r"L_y=L_x+L_h-1", "离散时间信号与系统", "有限长序列卷积的长度关系（用于由输入和冲激响应长度确定输出长度）"),
        (r"h(n)=0\quad(n<0)", "离散时间信号与系统", "因果系统的单位冲激响应条件（用于判断输出是否只依赖当前和过去输入）"),
        (r"|x(n)|\leq M<\infty\Longrightarrow |y(n)|\leq P<\infty", "离散时间信号与系统", "BIBO 稳定性定义（用于检验任意有界输入是否始终产生有界输出）"),
        (r"\Omega_h\leq\frac{\Omega_s}{2}", "离散时间信号与系统", "奈奎斯特无混叠采样条件（用于由信号最高角频率限制采样频率）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_first_chapter_signal_operations():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"\left.\sin(100\pi t)\right|_{t=nT}=\sin(0.1\pi n)", "两个给出相同样值的连续信号", "连续正弦信号的采样等效关系（用于说明不同连续频率可给出相同离散样值）"),
        (r"x(n)=\delta(n)\quad\Longrightarrow\quad X(z)=1,\qquad \text{ROC：全 z 平面}", "例题：同一代数式与不同收敛域", "单位冲激序列的 z 变换与收敛域（用于说明有限长冲激在全 z 平面收敛）"),
        (r"y(n)=H(e^{j\omega_0})e^{j\omega_0n}", "归一化角频率的换算", "复指数输入的频率响应特性（用于由系统频响直接得到稳态输出）"),
        (r"H(z)=K\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{z^2}", "数字陷波器", "单位圆共轭零点的陷波器结构（用于在指定频率处抑制窄带干扰）"),
        (r"y(n)=x\left((n-3)\right)_4R_4(n)", "例题：由频域相位因子恢复圆周移位序列", "四点循环时移序列（用于写出频域相位因子对应的时域输出）"),
        (r"\begin{aligned}y(n)&=x\left((n-3)\right)_4R_4(n)\\&=x\left((n+1)\right)_4R_4(n)\end{aligned}", "例题：由频域相位因子恢复圆周移位序列", "四点循环时移序列（用于写出频域相位因子对应的时域输出）"),
        (r"x_4(n)=A\sin(\omega n+\varphi),\quad n\in(-\infty,\infty)", "离散时间信号与系统", "离散正弦序列的通式（用于表示幅度、角频率和初相位可调的振荡信号）"),
        (r"y(n)=x_1(n)+x_2(n),\qquad y(n)=x_1(n)x_2(n)", "离散时间信号与系统", "离散序列的相加与相乘运算（用于逐时刻构造组合序列）"),
        (r"y(n)=x(n)+\alpha x(n-R),\qquad 0<\alpha<1", "离散时间信号与系统", "单回声延时叠加模型（用于表示原信号与延迟衰减副本的叠加）"),
        (r"y(n)=x(-n)", "离散时间信号与系统", "离散序列的时反变换（用于按原点镜像翻转序列）"),
        (r"\nabla x(n)=x(n+1)-x(n),\qquad \Delta x(n)=x(n)-x(n-1)", "离散时间信号与系统", "离散序列的前向与后向差分（用于描述相邻样值的变化）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_first_chapter_signal_operations_batch_two():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"x(-n+1),\qquad x(-n-1)", "离散时间信号与系统", "离散序列的时反与时移结果（用于确定不同反褶原点对应的样值位置）"),
        (r"\Delta R_{10}(n)=R_{10}(n)-R_{10}(n-1)=\{1,0,0,0,0,0,0,0,0,0,-1\}", "离散时间信号与系统", "矩形序列的后向差分（用于由相邻样值之差标出起止边缘）"),
        (r"u(n)=\begin{cases}1,&n\geq0,\\0,&n<0.\end{cases}", "离散时间信号与系统", "单位阶跃序列的定义（用于表示从零时刻开始的离散信号）"),
        (r"R_N(n)=\begin{cases}1,&0\leq n\leq N-1,\\0,&n\notin[0,N-1].\end{cases}", "离散时间信号与系统", "长度 N 的矩形序列定义（用于表示有限个连续非零样值）"),
        (r"x(n)=a^n u(n)", "离散时间信号与系统", "右边实指数序列（用于表示从零时刻开始按等比变化的信号）"),
        (r"x(n)=A\sin(n\omega+\varphi),\qquad x(n)=A\cos(n\omega+\varphi)", "离散时间信号与系统", "离散正弦与余弦序列通式（用于表示可调幅度、频率和初相位的振荡信号）"),
        (r"\omega=\Omega T=2\pi\frac{f_0}{f_s}", "离散时间信号与系统", "模拟频率到数字角频率的换算（用于由赫兹频率和采样率确定离散频率）"),
        (r"x(n)=e^{(\sigma+j\omega)n}=e^{\sigma n}\left[\cos(\omega n)+j\sin(\omega n)\right]", "离散时间信号与系统", "离散复指数序列的欧拉展开（用于分离指数包络和正余弦振荡分量）"),
        (r"e^{\pm jx}=\cos x\pm j\sin x", "离散时间信号与系统", "欧拉公式（用于在复指数与正余弦形式之间换算）"),
        (r"x(n+N)=x(n),\quad n\in\mathbb{Z},\quad N\in\mathbb{Z}_{+}", "离散时间信号与系统", "离散序列的周期定义（用于判定序列是否每隔 N 个样值重复）"),
        (r"N=\frac{2\pi k}{\omega},\qquad k\in\mathbb{Z}_{+}", "离散时间信号与系统", "离散正弦序列的周期求解式（用于由角频率搜索整数周期）"),
        (r"x(n)=A\cos(0.01\pi n),\qquad \frac{2\pi}{\omega}=\frac{2\pi}{0.01\pi}=200,\qquad N=200", "离散时间信号与系统", "离散余弦序列的周期计算（用于求角频率为 0.01π 时的基本周期）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_first_chapter_system_analysis_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"x(n)=A\cos\left(\frac{13\pi}{4}n\right),\qquad \frac{2\pi}{\omega}=\frac{8}{13},\qquad N=8", "离散时间信号与系统", "离散余弦序列的最小周期计算（用于由整数倍相位条件求 N=8）"),
        (r"\omega_L=0.01\pi,\quad\omega_H=0.2\pi,\quad N_1=10,\quad N_2=N_3=200", "离散时间信号与系统", "离散调幅信号的频率与周期参数（用于确定包络、载波及各分量的周期）"),
        (r"x(2n-2k)\ne x(2n-k)", "离散时间信号与系统", "尺度变换系统的时变性反例（用于证明索引缩放不保持时移不变性）"),
        (r"y(n-1)=x\bigl(2(n-1)\bigr)=x(2\cdot3-2)=x(4)=4,\qquad T[x(n-1)]=x(2n-1)=x(2\cdot3-1)=x(5)=5", "离散时间信号与系统", "尺度变换系统的时移比较（用于由不同输出值判定系统时变）"),
        (r"x(m)\ne0:\ N_1\leq m\leq N_2,\qquad h(n-m)\ne0:\ n-N_4\leq m\leq n-N_3", "离散时间信号与系统", "有限长卷积的非零支撑条件（用于确定求和变量的有效重叠区间）"),
        (r"N_1+N_3\leq n\leq N_2+N_4", "离散时间信号与系统", "有限长卷积的输出支撑范围（用于确定卷积结果的起止索引）"),
        (r"y(n_0)\Longleftarrow x(n),\qquad n\leq n_0", "离散时间信号与系统", "因果系统的输入依赖范围（用于说明当前输出只能使用当前和过去输入）"),
        (r"\begin{aligned}h(0)&=1,\qquad h(1)=a,\qquad h(2)=a^2,\\h(n)&=a h(n-1)=a^n u(n).\end{aligned}", "离散时间信号与系统", "一阶因果系统的单位冲激响应（用于由递推关系写出几何衰减序列）"),
        (r"\Omega_h>\frac{\Omega_s}{2}", "离散时间信号与系统", "采样频率不足的混叠条件（用于判定频谱副本将发生重叠）"),
        (r"\frac{\Omega}{\Omega_s}=\frac{f}{f_s}=\frac{\omega}{2\pi}", "离散时间信号与系统", "频率坐标的归一化换算关系（用于统一模拟角频率、赫兹和数字角频率）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_appendix_and_past_paper_formula_purposes():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"f_s=\frac{1}{T},\qquad \Omega_s=\frac{2\pi}{T}", "附录 D：考前高频公式与检查表", "采样率与采样角频率定义（用于由采样周期换算频率参数）"),
        (r"Y(z)=H(z)X(z),\qquad H\left(e^{j\omega}\right)=H(z)\big|_{z=e^{j\omega}", "附录 D：考前高频公式与检查表", "LSI 系统的 z 域输入输出关系（用于由系统函数求输出及单位圆频率响应）"),
        (r"\begin{aligned}a[n]&=0.25x[n]+0.4b[n],\\c[n]&=a[n-1]+0.5x[n],\\b[n]&=c[n-1],\\y[n]&=0.2x[n]+0.3c[n]+0.2b[n].\end{aligned}", "2019 年真题：离散系统结构分析", "离散系统的状态递推方程（用于由输入逐样本计算内部状态和输出）"),
        (r"y[n]-0.4y[n-2]=0.35x[n]+0.175x[n-1]-0.03x[n-2]", "2019 年真题：离散系统结构分析", "离散系统的等效差分方程（用于由结构消去状态变量后计算输出）"),
        (r"s[n]=\left[\frac{33}{40}-\frac{19+6\sqrt{10}}{80}\left(\frac{\sqrt{10}}{5}\right)^n", "2019 年真题：离散系统结构分析", "离散系统的单位冲激响应（用于写出由极点展开得到的因果响应）"),
        (r"f_{s,\min}=2f_2", "2020 年真题：组合带限信号的抽样频率", "组合带限信号的最低采样率（用于按最高频率确定无混叠采样下限）"),
        (r"X(j\Omega)=\frac{1}{2}\left[G\bigl(j(\Omega-1000\pi)\bigr)+G\bigl(j(\Omega+1000\pi)\bigr)\right]", "2021 年真题：带通信号的时域抽样", "余弦调制后的频谱平移关系（用于确定带通信号的正负频带位置）"),
        (r"\Omega_s\geq2\left(1000\pi+400\right),\qquad f_s\geq1000+\frac{400}{\pi}\ \mathrm{Hz}", "2021 年真题：带通信号的时域抽样", "带通信号的奈奎斯特采样下限（用于按最高边带频率避免混叠）"),
        (r"\max\left(a_1+b_1,a_2+b_2\right)\ne\max\left(a_1,a_2\right)+\max\left(b_1,b_2\right)", "2022 年真题：系统性质判定", "最大值系统的非线性反例（用于证明最大值运算不满足可加性）"),
        (r"\begin{aligned}\mathcal{T}\{x[n-n_0]\}&=n x[n-n_0-1]+x[n-n_0-2],\\y[n-n_0]&=(n-n_0)x[n-n_0-1]+x[n-n_0-2].\end{aligned}", "2023 年真题：离散系统性质判定", "时变系统的时移比较（用于证明输出时移不等于输入时移后的响应）"),
        (r"\begin{aligned}x_e[n]&=\frac{1}{2}\left(x[n]+x[-n]\right)=\frac{1}{2}\left(R_6[n]+R_6[-n]\right),\\x_o[n]&=\frac{1}{2}\left(x[n]-x[-n]\right)=\frac{1}{2}\left(R_6[n]-R_6[-n]\right).\end{aligned}", "2024 年真题：有限序列的偶、奇分解", "有限序列的偶奇分解（用于把序列拆为偶对称和奇对称分量）"),
        (r"x_o[n]R_8[n]=\begin{cases}\dfrac{1}{2},&1\leq n\leq5,\\0,&\text{其他 }n.\end{cases}", "2024 年真题：有限序列的偶、奇分解", "奇分量的有限支撑表达（用于给出截取后各非零样值范围）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_sampling_modulation_and_roc_paper_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"X(jf)=\begin{cases}1-\left|f\right|/(1\,\mathrm{kHz}),&\left|f\right|\leq1\,\mathrm{kHz},\\0,&\text{其他 }f.\end{cases}", "2018 年真题：A/D、数字低通与 D/A 串联", "输入连续信号的三角形频谱（用于给出模数转换前的带限频谱）"),
        (r"Y_a(jf)=\begin{cases}1-\left|f\right|/(1\,\mathrm{kHz}),&\left|f\right|\leq0.5\,\mathrm{kHz},\\0,&\text{其他 }f.\end{cases}", "2018 年真题：A/D、数字低通与 D/A 串联", "A/D—低通—D/A 链的重构频谱（用于给出低通后保留的基带范围）"),
        (r"x_0[n]=\delta[n]-a\delta[n-1]", "2018 年真题：离散系统可逆性", "一阶 FIR 系统的逆系统冲激响应（用于构造消除相邻样值反馈的逆滤波器）"),
        (r"y(n)\cos(\omega_cn+\theta_c)=\frac{\cos\theta_c}{2}x(n)+\frac12x(n)\cos(2\omega_cn+\theta_c)", "2019 年真题：调制、解调与恢复条件", "相干解调后的乘积展开（用于分离基带项和两倍载波高频项）"),
        (r"G=\frac{2}{\cos\theta_c}", "2019 年真题：调制、解调与恢复条件", "相干解调的增益补偿（用于抵消相位失配造成的基带幅度缩放）"),
        (r"\omega_0<\omega_{cp}<\min\!\left\{2\omega_c-\omega_0,\;2\pi-2\omega_c-\omega_0\right\}", "2019 年真题：调制、解调与恢复条件", "相干解调低通截止频率条件（用于保留基带并抑制高频调制项）"),
        (r"h_1(n)=\frac14[\delta(n)-\delta(n-1)+\delta(n+2)-\delta(n-3)]", "2020 年真题：频响、幅相特性与频移", "四抽头 FIR 的单位冲激响应（用于由抽头系数求频率响应）"),
        (r"H_1(e^{j\omega})=\frac14\left(1-e^{-j\omega}+e^{j2\omega}-e^{-j3\omega}\right)", "2020 年真题：频响、幅相特性与频移", "四抽头 FIR 的频率响应分解（用于识别幅度因子和线性相位项）"),
        (r"|H_1(e^{j\omega})|=\left|\sin\!\left(\frac{3\omega}{2}\right)\cos\omega\right|", "2020 年真题：频响、幅相特性与频移", "四抽头 FIR 的幅频响应（用于确定零点频率和通阻带变化）"),
        (r"h_2(n)=(-1)^nh_1(n)=\frac14[\delta(n)+\delta(n-1)+\delta(n+2)+\delta(n-3)]", "2020 年真题：频响、幅相特性与频移", "FIR 冲激响应的交替调制（用于由时域变号得到频域 π 平移）"),
        (r"F(z)=\frac{8}{1-z^{-1}}-\frac{4}{1-\frac12z^{-1}}-\frac{4}{\left(1-\frac12z^{-1}\right)^2}", "2021 年真题：指定 ROC 的反 z 变换", "有理 z 函数的部分分式展开（用于按各极点项和 ROC 求反变换）"),
        (r"f(n)=-8u(-n-1)-4\left(\frac12\right)^nu(n)-4(n+1)\left(\frac12\right)^nu(n)", "2021 年真题：指定 ROC 的反 z 变换", "指定 ROC 下的反 z 变换结果（用于组合左边和右边序列恢复时域信号）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_iir_and_feedback_paper_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"\begin{aligned}H_1(e^{j\omega})&=\frac14\left(1-e^{-j\omega}+e^{j2\omega}-e^{-j3\omega}\right)\\&=j e^{-j\omega/2}\sin\!\left(\frac{3\omega}{2}\right)\cos\omega.\end{aligned}", "2020 年真题：频响、幅相特性与频移", "四抽头 FIR 的频率响应分解（用于识别幅度因子和线性相位项）"),
        (r"w[n]=x[n]-w[n-1]+\frac{3}{4}w[n-2],\qquad y[n]=w[n]-w[n-1]", "2022 年真题：离散系统结构", "二阶内部状态递推式（用于按输入和历史状态计算系统输出）"),
        (r"\frac{1}{2}<|z|<\frac{3}{2}", "2022 年真题：离散系统结构", "离散系统的收敛域（用于确定双边序列对应的 z 平面环域）"),
        (r"H(z)=-\frac{1}{4}\frac{1}{1-\frac{1}{2}z^{-1}}+\frac{5}{4}\frac{1}{1+\frac{3}{2}z^{-1}}", "2022 年真题：离散系统结构", "系统函数的部分分式展开（用于由一阶极点项求单位冲激响应）"),
        (r"F(z)=\frac{1}{(1-3z^{-1})(1+z^{-1})}=\frac{3}{4}\frac{1}{1-3z^{-1}}+\frac{1}{4}\frac{1}{1+z^{-1}}", "2023 年真题：指定收敛域的反 z 变换", "指定 ROC 反 z 变换的部分分式展开（用于按不同极点项选择左右边序列）"),
        (r"f[n]=\frac{1}{4}(-1)^n u[n]-\frac{3}{4}3^n u[-n-1]", "2023 年真题：指定收敛域的反 z 变换", "指定 ROC 下的双边时域序列（用于组合因果和反因果分量）"),
        (r"y[n]=x[n]+\frac{5}{2}y[n-1]-y[n-2]", "2015 年真题：两延时反馈系统", "两延时反馈系统的差分方程（用于由当前输入和两项历史输出递推求解）"),
        (r"H(z)=\frac{4}{3}\frac{1}{1-2z^{-1}}-\frac{1}{3}\frac{1}{1-\frac12z^{-1}}", "2015 年真题：两延时反馈系统", "两延时反馈系统的部分分式系统函数（用于确定各极点分量的响应）"),
        (r"h_{\mathrm{s}}[n]=-\frac{4}{3}2^n u[-n-1]-\frac{1}{3}\left(\frac12\right)^n u[n]", "2015 年真题：两延时反馈系统", "两延时反馈系统的稳定冲激响应（用于按 ROC 写出稳定的双边序列）"),
        (r"x[n]=x_1[n]+x_2[n],\qquad x_1[n]=\left(\frac13\right)^n u[n],\qquad x_2[n]=\left(\frac12\right)^n u[-n-1]", "年真题·第二组第 5 小题：双边序列的 z 变换", "双边序列的左右分解（用于分别确定因果与反因果分量的 z 变换和 ROC）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_delay_transform_and_bilateral_paper_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"y[n]=x[n]+\frac{1}{2}y[n-1]", "年真题：单延时反馈离散 LTI 系统", "单延时反馈 LTI 系统的差分方程（用于由输入和前一输出递推当前输出）"),
        (r"\begin{aligned}Y(z)&=X(z)+\frac{1}{2}z^{-1}Y(z),\\H(z)&=\frac{Y(z)}{X(z)}=\frac{1}{1-\frac{1}{2}z^{-1}}=\frac{z}{z-\frac{1}{2}}.\end{aligned}", "年真题：单延时反馈离散 LTI 系统", "单延时反馈 LTI 系统的系统函数（用于由差分方程求极点和频率响应）"),
        (r"\operatorname{ROC}:\left|z\right|>\frac{1}{2}", "年真题：单延时反馈离散 LTI 系统", "单延时反馈系统的因果 ROC（用于选择稳定因果的单位冲激响应）"),
        (r"h[n]=\left(\frac{1}{2}\right)^n u[n]", "年真题：单延时反馈离散 LTI 系统", "单延时反馈系统的单位冲激响应（用于写出极点为 1/2 的因果衰减序列）"),
        (r"Y(z)=\left(az^{-1}Y(z)+X(z)-a^Nz^{-N}X(z)\right),\qquad H(z)=\frac{1-a^Nz^{-N}}{1-az^{-1}}", "（2）含延时消零项的单位脉冲响应", "含延时消零项系统的系统函数（用于构造长度 N 的截断指数冲激响应）"),
        (r"\begin{aligned}h[n]&=a^nu[n]-a^N a^{n-N}u[n-N]\\&=a^n\left(u[n]-u[n-N]\right).\end{aligned}", "（2）含延时消零项的单位脉冲响应", "截断指数的单位冲激响应（用于显示延时消零项使响应在 N 后终止）"),
        (r"X(j\Omega)=X(s)\big|_{s=j\Omega}=\mathcal{F}\{x(t)\}", "年真题：FT、LT 与 ZT 的关系", "拉普拉斯变换到傅里叶变换的限制关系（用于在虚轴收敛时得到连续时间频谱）"),
        (r"X\!\left(e^{j\omega}\right)=X(z)\big|_{z=e^{j\omega}}=\mathcal{F}_{\mathrm{DT}}\{x[n]\}", "年真题：FT、LT 与 ZT 的关系", "z 变换到 DTFT 的单位圆取值关系（用于由 z 域函数得到离散时间频谱）"),
        (r"z=e^{sT}=e^{(\sigma+j\Omega)T}=e^{\sigma T}e^{j\Omega T},\qquad s=\sigma+j\Omega", "年真题：拉氏变换与 z 变换的映射", "拉普拉斯平面到 z 平面的指数映射（用于把连续系统极点映射为离散系统极点）"),
        (r"\operatorname{Re}\{s\}<0\quad\Longleftrightarrow\quad\left|z\right|<1", "年真题：拉氏变换与 z 变换的映射", "s 平面稳定半平面与 z 平面单位圆的对应（用于判断连续和离散系统稳定性）"),
        (r"\begin{aligned}F(z)&=\frac{z^2}{(z-3)(z+1)}\\&=\frac{1}{2}\frac{z}{z-3}+\frac{1}{2}\frac{z}{z+1}.\end{aligned}", "年真题：指定 ROC 的反 z 变换", "指定 ROC 反 z 变换的部分分式分解（用于分别处理极点 3 和 −1）"),
        (r"\frac{z}{z-3},\quad \left|z\right|<3\quad\Longleftrightarrow\quad-3^n u[-n-1]", "年真题：指定 ROC 的反 z 变换", "极点项与 ROC 对应的反 z 变换对（用于按 ROC 选择左边或右边序列）"),
        (r"f[n]=\frac{1}{2}(-1)^n u[n]-\frac{1}{2}3^n u[-n-1]", "年真题：指定 ROC 的反 z 变换", "指定 ROC 下的双边反 z 变换结果（用于合成两个极点项的时域序列）"),
        (r"\left(\frac{1}{3}\right)^nu[n]\Longleftrightarrow\frac{1}{1-\frac{1}{3}z^{-1}},\quad\left|z\right|>\frac{1}{3}", "年真题：双边序列的 z 变换", "左右边指数序列的 z 变换对（用于分别确定双边序列各分量的 ROC）"),
        (r"X(z)=\frac{1}{1-\frac{1}{3}z^{-1}}-\frac{1}{1-\frac{1}{2}z^{-1}},\qquad\frac{1}{3}<\left|z\right|<\frac{1}{2}", "年真题：双边序列的 z 变换", "双边指数序列的 z 变换与 ROC（用于给出两个收敛域的交集）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_dft_resolution_and_circular_convolution_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"z_k=e^{s_kT}", "年真题：拉氏变换与 z 变换的映射", "连续系统极点到 z 平面极点的映射（用于由采样周期定位离散极点）"),
        (r"X^*(e^{j\omega})\quad\Longleftrightarrow\quad x^*[-n]", "年真题：频谱实部对应的序列", "DTFT 的共轭时反性质（用于由频谱共轭得到时域共轭反折序列）"),
        (r"\begin{aligned}\left(\frac{1}{3}\right)^nu[n]&\Longleftrightarrow\frac{1}{1-\frac{1}{3}z^{-1}},\quad\left|z\right|>\frac{1}{3},\\\left(\frac{1}{2}\right)^nu[-n-1]&\Longleftrightarrow-\frac{1}{1-\frac{1}{2}z^{-1}},\quad\left|z\right|<\frac{1}{2}.\end{aligned}", "年真题：双边序列的 z 变换", "双边指数序列的分量 z 变换对（用于分别给出左右边分量及其 ROC）"),
        (r"f_s=2\times200=400\,\mathrm{Hz}", "2019 年真题", "奈奎斯特采样率计算（用于由最高频率 200 Hz 得到最低采样率）"),
        (r"N=\frac{f_s}{F_0}=40", "2019 年真题", "DFT 点数与频率分辨率关系（用于由采样率和频率间隔确定 N）"),
        (r"\omega_k=\frac{2\pi k}{N}=\frac{2\pi k}{40}=\frac{\pi k}{20}\ \mathrm{rad}", "2019 年真题", "DFT 频率栅格的数字角频率（用于标出第 k 个频率样点的位置）"),
        (r"f_k=kF_0=10k\,\mathrm{Hz}", "2019 年真题", "DFT 频率栅格的赫兹坐标（用于标出第 k 个频率样点的实际频率）"),
        (r"x_3(n)=x_1(n)\mathbin{\circledast}_N x_2(n)", "2019 年真题", "N 点循环卷积定义（用于表示周期序列在一个周期内的卷积）"),
        (r"N\geq5+3-1=7", "2019 年真题", "DFT 实现线性卷积的最小长度条件（用于避免循环卷积折回）"),
        (r"\Delta\Omega=\frac{2\pi}{NT}", "2019 年真题（第十题）", "DFT 的角频率分辨率（用于由采样时长和点数确定频率间隔）"),
        (r"\frac{2\pi}{N\times0.15}<2\quad\Longrightarrow\quad N>\frac{2\pi}{2\times0.15}\approx20.94", "2019 年真题（第十题）", "满足频率分辨率指标的点数下限（用于按最大允许间隔选择 N）"),
        (r"y(n)=x_5(n)\mathbin{\circledast}_5h_5(n)", "2019 年真题", "五点循环卷积（用于计算给定周期序列和滤波器的周期输出）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_remaining_dft_paper_short_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"\Delta\Omega=\frac{2\pi}{32\times0.15}\approx1.309\,\mathrm{rad/s}<2\,\mathrm{rad/s}", "2019 年真题（第十题）", "32 点 DFT 的实际角频率分辨率（用于验证分辨率满足题设上限）"),
        (r"\begin{aligned}y(0)&=3+3=6,&y(1)&=3+3=6,\\y(2)&=3+3+3=9,&y(3)&=3+3+3=9,\\y(4)&=3+3=6.\end{aligned}", "2019 年真题", "五点循环卷积的逐点计算结果（用于列出一个周期内的全部输出样值）"),
        (r"F_0=\frac{f_s}{N}=\frac{100}{256}=0.390625\,\mathrm{Hz}", "2019 年真题", "256 点 DFT 的频率分辨率（用于计算相邻频率栅格的赫兹间隔）"),
        (r"\left|f_3-f_1\right|=0.07\,\mathrm{Hz}&lt;F_0", "2019 年真题", "频率分量不可分辨判据（用于比较频率差与 DFT 分辨率）"),
        (r"Y(k)=e^{j2\pi k\cdot5/8}X(k)", "2019 年真题（判断题第 1 小题）", "DFT 循环时移的相位因子（用于由频域相位确定时域循环移位）"),
        (r"\left|Y(k)\right|=\left|X(k)\right|,\qquad k=0,1,\ldots,7", "2019 年真题（判断题第 1 小题）", "循环时移的幅度谱不变性（用于说明时移只改变频谱相位）"),
        (r"X(k)=1+2e^{-j2\pi k\cdot5/10}=1+2e^{-j\pi k}=1+2(-1)^k", "2019 年真题（第九题）", "两冲激周期序列的 DFT（用于把时域延时冲激写成频域相位和）"),
        (r"y(n)=x\left((n+2)\right)_{10}", "2019 年真题（第九题）", "十点循环时移序列（用于表示向左循环移动两个样点）"),
        (r"y(n)=x(n)\mathbin{\circledast}_{10}w(n)=w(n)+2w\left((n-5)\right)_{10}", "2019 年真题（第九题）", "十点循环卷积的移位叠加式（用于利用冲激分解快速计算输出）"),
        (r"y(n)=\left\{3,3,1,1,1,3,3,2,2,2\right\},\qquad 0\leq n\leq9", "2019 年真题（第九题）", "十点循环卷积的样值结果（用于列出一个周期内的输出序列）"),
        (r"N\geq100", "2019 年真题（填空题第 2 小题）", "DFT 点数下限（用于满足题设频率采样数量要求）"),
        (r"a_{k+N}=a_k,\qquad a_{-k}=a_k", "2019 年真题（填空题第 5 小题）", "实偶序列的 DFS 系数对称性（用于由已知系数扩展周期和偶对称位置）"),
        (r"a_{-3}=5,\qquad a_{-2}=a_2=3,\qquad a_{-1}=a_1=5", "2019 年真题（填空题第 5 小题）", "实偶序列的 DFS 系数补全（用于按周期和偶对称确定负索引系数）"),
        (r"X(k)=X(z)\left|_{z=e^{j2\pi k/N}}\right.", "2019 年真题（填空题第 3 小题）", "z 变换在单位圆上的 DFT 取样关系（用于由 z 域表达式求 N 点频谱）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_dft_symmetry_and_short_sequence_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"a_{-3}=a_3=\frac{1}{6},\qquad a_{-2}=a_2=2,\qquad a_{-1}=a_1=1,\qquad a_0=\frac{1}{3}", "年真题（填空题第 7 小题）", "实偶序列的 DFS 系数列（用于由偶对称性列出完整频域系数）"),
        (r"y(n)=x(n)+x(n+3),\qquad n=0,1,2", "年真题（DSP 第 3 小题）", "周期序列的延时相加（用于逐样点构造两个周期移位分量之和）"),
        (r"y(0)=2,\qquad y(1)=1,\qquad y(2)=1", "年真题（DSP 第 3 小题）", "周期序列延时相加的样值结果（用于列出一个周期内的输出）"),
        (r"x(n)=2+e^{j2\pi n/N}+e^{-j2\pi n/N}", "年真题（DSP 第 4 小题）", "三谱线周期序列的指数表示（用于直接读出 DFT 非零频点）"),
        (r"X(0)=2N,\qquad X(1)=N,\qquad X(N-1)=N", "年真题（DSP 第 4 小题）", "三谱线周期序列的 DFT 样值（用于给出直流和共轭频点幅度）"),
        (r"x(n)=x_1(n)+jx_2(n)", "年真题（第八题）", "复序列的实虚部分解（用于分别处理实部和虚部序列）"),
        (r"X_1(k)=\frac{1}{2}\left[X(k)+X^*\left((N-k)\right)_N\right],\qquad X_2(k)=\frac{1}{2j}\left[X(k)-X^*\left((N-k)\right)_N\right]", "年真题（第八题）", "复序列实虚分量的 DFT 分解（用于由总频谱恢复两个实序列频谱）"),
        (r"y(n)=x\left((n-2)\right)_{10}=\delta(n-2)+2\delta(n-7)", "年真题（第六题第 1 小题）", "十点循环时移的冲激表示（用于写出循环移位后非零样值位置）"),
        (r"m(n)=5\delta(n-2)+4\delta(n-7)", "年真题（第六题第 1 小题）", "加权冲激序列（用于表示两个指定位置的离散样值）"),
        (r"T_0=NT=102.4\,\mathrm{ms},\qquad f_{\max}=\frac{f_s}{2}=5\,\mathrm{kHz},\qquad F_0=\frac{1}{NT}=9.765625\,\mathrm{Hz}", "年真题（第六题第 3 小题）", "采样记录的周期、带宽与分辨率（用于由采样率和点数确定频域参数）"),
        (r"y(n)=x(n)+x(n+2)+x(n+4),\qquad n=0,1", "年真题（第三题）", "周期序列的多重延时相加（用于计算指定索引处的叠加输出）"),
        (r"y(0)=4+3+2=9,\qquad y(1)=7+1=8", "年真题（第三题）", "多重延时相加的样值结果（用于列出指定输出时刻的计算值）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_handles_fft_and_filter_design_paper_formulas():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (r"y(n)=x\left((n-4)\right)_6=2\delta(n)+\delta(n-1)+4\delta(n-4)+3\delta(n-5)", "年真题（第五题）", "六点循环时移的冲激表示（用于列出循环右移后的非零样值位置）"),
        (r"\cos\left(\frac{2\pi}{5}k\right)=\frac{1}{2}\left(W_{10}^{2k}+W_{10}^{-2k}\right)", "年真题（DSP 第 3 小题）", "余弦序列的 DFT 旋转因子表示（用于将实余弦分解为两条共轭频谱）"),
        (r"y(n)=\frac{1}{2}\left[x\left((n-2)\right)_{10}+x\left((n+2)\right)_{10}\right]", "年真题（DSP 第 3 小题）", "十点循环双向时移平均（用于构造两个对称移位分量的组合序列）"),
        (r"y(n)=\left\{1,\frac{3}{2},2,3,1,\frac{3}{2},2,\frac{5}{2},0,\frac{1}{2}\right\}", "年真题（DSP 第 3 小题）", "十点循环双向时移平均的样值结果（用于列出完整一个周期的输出）"),
        (r"(-1)^{N-1-n}=-(-1)^n", "年真题（DSP 第 3 小题）", "偶数点 DFT 的交替符号关系（用于判定半采样频率处的抵消）"),
        (r"X\left(\frac{N}{2}\right)=0", "年真题（DSP 第 3 小题）", "半采样频率 DFT 零点（用于给出交替符号相消后的频谱值）"),
        (r"X(k)=4+e^{-j\frac{\pi}{2}k}+e^{-j\pi k}+e^{-j\frac{3\pi}{2}k}", "年真题（第七题第 1 小题）", "四点序列的 DFT 计算式（用于由时域样值求四个频谱点）"),
        (r"X(0)=7,\qquad X(1)=X(2)=X(3)=3", "年真题（第七题第 1 小题）", "四点序列的 DFT 样值（用于列出直流和其余频率点幅度）"),
        (r"X_{\mathrm{ep}}(0)=7,\qquad X_{\mathrm{ep}}(1)=X_{\mathrm{ep}}(2)=X_{\mathrm{ep}}(3)=3", "年真题（第七题第 1 小题）", "四点序列偶分量的 DFT（用于说明原序列频谱的偶对称部分）"),
        (r"X_{\mathrm{op}}(k)=0,\qquad k=0,1,2,3", "年真题（第七题第 1 小题）", "四点序列奇分量的零频谱（用于说明该序列不含奇对称分量）"),
        (r"k_0=\frac{800}{16}=50", "年真题（第十三题第 1 问）", "DFT 频率索引计算（用于把 800 Hz 映射到 16 Hz 栅格的频点编号）"),
        (r"X_{\mathrm{ep}}(k)=X(k)=\{4,0,4,0\}", "年真题（第七题第 1 问）", "四点实偶序列的 DFT（用于列出偶序列的离散频谱样值）"),
        (r"\widetilde{x}(n)=\{1+a^6,\ a+a^7,\ a^2,\ a^3,\ a^4,\ a^5\}", "第 3 问：单位圆六点取样后的 IDFT", "六点单位圆取样的 IDFT 序列（用于写出频率取样后恢复的周期时域样值）"),
        (r"\begin{aligned}X(k)&=X_1(k)+W_8^kX_2(k),\\X\left(k+4\right)&=X_1(k)-W_8^kX_2(k),\\W_8&=e^{-j\frac{2\pi}{8}}.\end{aligned}", "年真题", "八点基 2 FFT 蝶形递推（用于由两个四点子 DFT 合成八点频谱）"),
        (r"\begin{aligned}a[n]&=x[2n],&b[n]&=x[2n+1],&0\leq n\leq L-1.\end{aligned}", "年真题", "实序列 FFT 的偶奇抽取（用于把输入拆为偶索引和奇索引两路）"),
        (r"\begin{aligned}c[n]&=a[n]+jb[n],\\C[k]&=\operatorname{FFT}_L\{c[n]\}=A[k]+jB[k].\end{aligned}", "年真题", "双实序列合成 FFT（用于用一次复 FFT 同时计算两路实序列频谱）"),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_uses_structured_fallbacks_before_topic_generic_labels():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (
            r"H(z)=\prod_{r=1}^{R}H_r(z)",
            "年真题",
            "级联滤波器的总系统函数（用于把各子节系统函数相乘得到整体传递关系）",
        ),
        (
            r"M=128-60+1=69",
            "年真题",
            "重叠保留法的有效输出长度（用于由 DFT 块长和滤波器长度确定无混叠样本数）",
        ),
        (
            r"H(j\omega)=\frac{1}{\sqrt{1+(\omega/\Omega_c)^{2N}}}",
            "年真题",
            "巴特沃斯低通滤波器的幅频响应（用于由截止频率和阶数检验通阻带指标）",
        ),
        (
            r"x(n)=2\cos\left(\frac{\pi}{3}n\right)",
            "年真题",
            "离散余弦序列表达式（用于确定指定离散频率下的时域样值）",
        ),
        (
            r"X(0)=0.",
            "年真题（第七题第 3 小题）",
            "交替符号序列的直流 DFT 零点（用于说明偶数点序列在直流频点发生相消）",
        ),
        (
            r"\operatorname{Re}\{s\}=\frac{2}{T}\operatorname{Re}\left\{\frac{z-1}{z+1}\right\}",
            "年真题",
            "双线性变换的实部映射（用于证明单位圆内外分别对应 s 平面的左右半平面）",
        ),
        (
            r"H_{\mathrm{bl}}(z)=H\!\left(2\frac{z-1}{z+1}\right)",
            "年真题",
            "双线性变换的数字系统函数（用于把模拟系统函数代换为数字滤波器传递函数）",
        ),
        (
            r"s_1=\frac{\ln0.5}{2},\qquad C_1=1",
            "年真题（第十二题）",
            "脉冲响应不变法的极点与留数映射（用于由数字极点反推对应模拟系统的部分分式项）",
        ),
        (
            r"H_{\mathrm{bl}}(s)=\frac{1}{1-0.5\frac{1-s}{1+s}}",
            "年真题（第十二题）",
            "双线性变换的反代换系统函数（用于把数字系统函数还原为模拟 s 域表达式）",
        ),
        (
            r"h_c(t)=h_{c1}(t)*h_{c2}(t)",
            "年真题",
            "连续系统串联的冲激响应卷积（用于由两个子系统响应求级联系统的总响应）",
        ),
        (
            r"N_{\min}=7,\qquad\tau_{\min}=\frac{7}{2}",
            "年真题",
            "线性相位 FIR 的最小阶数与群延迟（用于由零点总数确定可实现结构的最低延时）",
        ),
        (
            r"a=1,\qquad\theta=\frac{\pi}{3}",
            "年真题：窄带干扰抑制",
            "窄带陷波器的零点参数（用于把共轭零点准确放置在干扰频率）",
        ),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_prioritizes_bibo_conditions_over_system_function_heading():
    from full.tools.build_all_main_body import _formula_name

    cases = (
        (
            r"\left|x(n)\right|\le M<\infty\Longrightarrow \left|y(n)\right|\le P<\infty",
            "系统函数及其与系统性质的关系",
            "BIBO 稳定性定义（用于检验任意有界输入是否始终产生有界输出）",
        ),
        (
            r"\sum_{n=-\infty}^{\infty}\left|h(n)\right|<\infty",
            "系统函数及其与系统性质的关系",
            "离散 LSI 系统的绝对可和条件（用于由单位冲激响应判定 BIBO 稳定性）",
        ),
        (
            r"\sum_{n=-\infty}^{\infty}\left|h(n)\right|=\frac13+\frac13+\frac13=1<\infty",
            "系统函数及其与系统性质的关系",
            "绝对可和的稳定性验证（用于以冲激响应求和结果证明系统 BIBO 稳定）",
        ),
    )
    for formula, heading, expected in cases:
        assert _formula_name(formula, heading) == expected


def test_formula_name_distinguishes_sampling_spectrum_filter_and_frequency_samples():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"F_s(j\Omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}F(j(\Omega-k\Omega_s))",
        "采样与恢复",
    ) == "周期冲激采样的频谱复制关系（用于确定采样后频谱副本的位置和间隔）"
    assert _formula_name(
        r"H(\Omega)=\begin{cases}T,&\left|\Omega\right|\le1000\pi\\0,&\left|\Omega\right|>1000\pi\end{cases}",
        "采样与恢复",
    ) == "理想低通滤波器的频率响应（用于保留目标频带并抑制其余频谱副本）"
    assert _formula_name(
        r"H(k)=\begin{cases}e^{-j\frac{14\pi}{15}k},&k=4,5,\ldots,11\\0,&k=0,1,2,3,12,13,14\end{cases}",
        "15 点频率采样设计",
    ) == "频率采样设计的目标样值（用于指定各离散频率点的幅度和相位）"
    assert _formula_name(
        r"H(z)=\pm z^{-(N-1)}H\!\left(z^{-1}\right)",
        "线性相位 FIR 数字滤波器的条件和特点",
    ) == "FIR 系统函数的倒数对称关系（用于由零点镜像结构判断线性相位特性）"


def test_formula_name_prioritizes_zero_pole_geometry_over_stability_heading():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"H(z)=A\frac{\prod_r(z-c_r)}{\prod_r(z-d_r)}",
        "从累加器到稳定低通系统",
    ) == "系统函数的零极点分解（用于由零点、极点和增益分析频率响应）"
    assert _formula_name(
        r"\overrightarrow{c_rB}=e^{j\omega}-c_r,\qquad\overrightarrow{d_rB}=e^{j\omega}-d_r",
        "从累加器到稳定低通系统",
    ) == "零极点到单位圆频率点的向量关系（用于用几何距离解释幅频响应）"
