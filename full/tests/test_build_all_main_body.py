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
