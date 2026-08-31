"""Formula leads must identify the actual mathematical relation, not a generic display shape."""


def test_real_and_imaginary_sequence_dtft_relation_has_a_specific_formula_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[\mathcal{F}\{\operatorname{Re}\{x(n)\}\}=X_e(e^{j\omega}),\qquad"
        r"\mathcal{F}\{j\operatorname{Im}\{x(n)\}\}=X_o(e^{j\omega})\]",
        "实序列频谱的共轭对称关系",
    )

    assert label == "实序列实部与虚部的 DTFT 分量关系（用于分别分析共轭对称频谱的偶分量和奇分量）"


def test_rendered_square_bracket_real_imaginary_dtft_relation_has_the_same_specific_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[\mathcal{F}\{\operatorname{Re}[x(n)]\}=X_e(e^{j\omega}),\qquad"
        r"\mathcal{F}\{j\operatorname{Im}[x(n)]\}=X_o(e^{j\omega})\]",
        "实序列频谱的共轭对称关系",
    )

    assert label == "实序列实部与虚部的 DTFT 分量关系（用于分别分析共轭对称频谱的偶分量和奇分量）"


def test_conjugate_symmetric_time_components_have_a_specific_dtft_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[\mathcal{F}\{x_e(n)\}=\operatorname{Re}\{X(e^{j\omega})\},\qquad"
        r"\mathcal{F}\{x_o(n)\}=j\operatorname{Im}\{X(e^{j\omega})\}\]",
        "实序列频谱的共轭对称关系",
    )

    assert label == "共轭对称时域分量的 DTFT 关系（用于由完整频谱分离对应的实部和虚部）"


def test_conjugate_component_reconstruction_derivation_has_a_specific_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[\begin{aligned}\mathcal{F}\{x_e(n)\}&=\frac{1}{2}"
        r"\left[X(e^{j\omega})+X^*(e^{j\omega})\right]\\"
        r"&=\operatorname{Re}\{X(e^{j\omega})\}\end{aligned}\]",
        "实序列频谱的共轭对称关系",
    )

    assert label == "共轭对称分量的频谱重构推导（用于验证时域分量与频谱实部的对应）"


def test_complex_exponential_components_have_a_specific_formula_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[\operatorname{Re}\{x(n)\}=e^{\sigma n}\cos(\omega n),"
        r"\quad\operatorname{Im}\{x(n)\}=e^{\sigma n}\sin(\omega n),"
        r"\quad\left|x(n)\right|=e^{\sigma n}\]",
        "复指数序列",
    )

    assert label == "复指数序列的实部、虚部与模（用于分解指数包络和正弦振荡）"


def test_z_transform_property_formulae_have_specific_leads():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"\[\begin{aligned}\mathcal{Z}\{ax(n)+by(n)\}&=aX(z)+bY(z),\\"
        r"\operatorname{ROC}\{ax(n)+by(n)\}&\supseteq R_x\cap R_y\end{aligned}\]",
        "z 变换性质",
    ) == "z 变换的线性性与 ROC 关系（用于把加权序列拆成已知变换）"
    assert _formula_name(
        r"\[\mathcal{Z}\{x(-n)\}=X(z^{-1}),\qquad"
        r"\mathcal{Z}\{a^nx(n)\}=X(a^{-1}z)\]",
        "z 变换性质",
    ) == "z 变换的时间反转与指数加权性质（用于处理反折序列和改变指数衰减率）"
    assert _formula_name(
        r"\[\mathcal{Z}\{nx(n)\}=-z\frac{\mathrm{d}X(z)}{\mathrm{d}z}\]",
        "z 变换性质",
    ) == "z 变换的时域乘 n 性质（用于把时域加权转为 z 域微分）"


def test_median_filter_formula_has_a_specific_formula_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[y(n)=\operatorname{med}\left\{x(n-M),\ldots,x(n),\ldots,x(n+M)\right\}\]",
        "非线性滤波",
    )

    assert label == "中值滤波器的输出定义（用于抑制孤立脉冲干扰）"


def test_partial_fraction_general_form_has_a_specific_formula_lead():
    from full.tools.build_all_main_body import _formula_name

    label = _formula_name(
        r"\[X(z)=\sum_k\frac{A_k}{1-p_kz^{-1}}+"
        r"\sum_{\ell}\sum_{r=1}^{q_\ell}\frac{C_{\ell,r}}{\left(1-p_\ell z^{-1}\right)^r}"
        r"+\sum_{m=0}^{M}B_mz^{-m}\]",
        "部分分式展开法",
    )

    assert label == "有理 z 函数的部分分式通式（用于按单极点、重极点和多项式项分别反变换）"


def test_inverse_z_partial_fraction_formulae_keep_specific_names_outside_their_section():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"\[x(n)=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,\mathrm{d}z\]",
        "公式汇总",
    ) == "z 反变换的围线积分定义（用于由 z 域函数恢复时域序列）"
    assert _formula_name(
        r"\[A_k=\left.\left(1-p_kz^{-1}\right)X(z)\right|_{z=p_k}\]",
        "公式汇总",
    ) == "部分分式展开的留数系数（用于把有理 z 函数拆成可直接反变换的简单项）"
    assert _formula_name(
        r"\[C_{\ell,r}=\frac{1}{(q_\ell-r)!}\left.\frac{\mathrm{d}^{q_\ell-r}}"
        r"{\mathrm{d}z^{q_\ell-r}}\left[(z-p_\ell)^{q_\ell}X(z)\right]\right|_{z=p_\ell},"
        r"\qquad r=1,\ldots,q_\ell\]",
        "公式汇总",
    ) == "重极点系数的导数公式（用于求有理 z 函数高阶极点项的部分分式系数）"


def test_conjugate_symmetric_decomposition_formulae_keep_distinct_names_in_the_appendix():
    from full.tools.build_all_main_body import _formula_name

    assert _formula_name(
        r"\[x_e(n)=\frac{1}{2}\left[x(n)+x^*(-n)\right],\qquad"
        r"x_o(n)=\frac{1}{2}\left[x(n)-x^*(-n)\right]\]",
        "公式汇总",
    ) == "共轭对称与共轭反对称分量分解（用于将任意复序列按共轭对称性拆分）"
    assert _formula_name(
        r"\[\begin{aligned}x_e(n)&=x_{er}(n)+jx_{ei}(n), & x_{er}(n)&=x_{er}(-n),"
        r" & x_{ei}(n)&=-x_{ei}(-n),\\x_o(n)&=x_{or}(n)+jx_{oi}(n),"
        r" & x_{or}(n)&=-x_{or}(-n), & x_{oi}(n)&=x_{oi}(-n).\end{aligned}\]",
        "公式汇总",
    ) == "共轭对称分量的实虚部奇偶性（用于由实部和虚部判断序列的共轭对称类型）"
    assert _formula_name(
        r"\[X_e(e^{j\omega})=\frac{1}{2}\left[X(e^{j\omega})+X^*(e^{-j\omega})\right],"
        r"\quad X_o(e^{j\omega})=\frac{1}{2}\left[X(e^{j\omega})-X^*(e^{-j\omega})\right]\]",
        "公式汇总",
    ) == "频谱的共轭对称分量分解（用于由完整频谱构造共轭对称和共轭反对称频谱）"
