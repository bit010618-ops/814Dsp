from __future__ import annotations
import sys
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style

CHAPTER = "第二章 z 变换与 LSI 系统频域分析"
PALE = HexColor("#F4F7F8")


def para(p, text, y):
    return style.draw_rich_paragraph(p, text, 62, y, A4[0] - 124)


def sub(p, text, y):
    return style.draw_continuation_title(p, text, y)


def begin(p, n, text):
    style.draw_header(p, CHAPTER)
    style.draw_footer(p, n)
    return style.draw_title(p, text, 746)


def box(p, latex, y, height=54):
    asset, width, image_height = style._math_metrics(latex, style.DISPLAY_FORMULA_SIZE)
    draw_h = min(height - 12, image_height * 72 / 300)
    draw_w = width * draw_h / image_height
    limit = A4[0] - 148
    if draw_w > limit:
        draw_h *= limit / draw_w
        draw_w = limit
    p.setFillColor(PALE)
    p.roundRect(62, y - height, A4[0] - 124, height, 3, fill=1, stroke=0)
    p.drawImage(ImageReader(str(asset)), (A4[0] - draw_w) / 2, y - height + (height - draw_h) / 2, draw_w, draw_h, mask="auto")
    return y - height - 12


def page_one(p):
    y = begin(p, 1, "系统频率响应的基本概念")
    y = para(p, r"LSI 系统的频率响应是单位脉冲响应 {{h(n)}} 的离散时间傅里叶变换：", y)
    y = box(p, r"H(e^{j\omega})=\sum_{n=-\infty}^{\infty}h(n)e^{-j\omega n}", y, 58)
    y = para(p, r"时域卷积在频域中对应相乘，因此输入频谱 {{X(e^{j\omega})}} 经系统后得到：", y)
    y = box(p, r"Y(e^{j\omega})=X(e^{j\omega})H(e^{j\omega})", y, 54)
    y = sub(p, "幅频响应", y - 6)
    y = para(p, r"幅频响应 {{|H(e^{j\omega})|}} 决定各频率成分是否通过、被增强或被抑制。设计系统时，所需频段应有较大幅度，不需要的频段则应有较小幅度。", y)
    y = box(p, r"|Y(e^{j\omega})|=|X(e^{j\omega})|\,|H(e^{j\omega})|", y, 54)
    y = sub(p, "对数幅度", y - 6)
    y = para(p, r"增益或衰减常用分贝表示。幅度比为 {{A}} 时，其分贝值为：", y)
    y = box(p, r"G_{\mathrm{dB}}=20\log_{10}A", y, 52)
    para(p, "例如幅度增益 10 倍约为 20 dB；幅度衰减到原来的十分之一约为 -20 dB。", y)
    p.showPage()


def page_two(p):
    y = begin(p, 2, "相频响应与群延迟")
    y = para(p, r"相频响应 {{\arg H(e^{j\omega})}} 决定各频率分量的相位变化，因而对应时域中的移位或波形畸变。", y)
    y = sub(p, "理想延时系统", y - 6)
    y = para(p, r"若系统仅把信号延时 {{n_d}} 个样本，则其频率响应为：", y)
    y = box(p, r"H(e^{j\omega})=e^{-j\omega n_d},\qquad |H(e^{j\omega})|=1,\qquad \arg H(e^{j\omega})=-\omega n_d", y, 58)
    y = para(p, "此时所有频率分量具有相同延时，波形形状不变。", y)
    y = sub(p, "群延迟", y - 6)
    y = para(p, r"群延迟描述相位响应对频率的变化率：", y)
    y = box(p, r"\tau_g(\omega)=-\frac{d}{d\omega}\arg H(e^{j\omega})", y, 54)
    y = para(p, "当群延迟在关心频段近似为常数时，系统近似线性相位；不同频率分量会一起到达，输出波形较少失真。", y)
    y = sub(p, "低通滤波的频域含义", y - 6)
    y = para(p, "低通系统使低频分量通过、高频分量受到抑制。频率响应不是“消灭时间信号”，而是逐频率地改变各分量的幅度和相位。", y)
    p.showPage()


def page_three(p):
    y = begin(p, 3, "固定频率输入下的系统输出")
    y = para(p, r"若输入为复指数序列 {{x(n)=e^{j\omega_0n}}}，且系统频率响应在 {{\omega_0}} 处存在，则输出仍是相同频率的复指数序列：", y)
    y = box(p, r"y(n)=H(e^{j\omega_0})e^{j\omega_0n}", y, 54)
    y = para(p, r"对于实正弦输入 {{x(n)=A\cos(\omega_0n+\varphi)}}，输出频率不变，幅度由频率响应幅度加权，相位增加系统相位：", y)
    y = box(p, r"y(n)=A|H(e^{j\omega_0})|\cos\!\left[\omega_0n+\varphi+\arg H(e^{j\omega_0})\right]", y, 58)
    y = sub(p, "三点算术平均滤波系统", y - 6)
    y = para(p, r"三点平均系统满足 {{y(n)=\frac{x(n)+x(n-1)+x(n-2)}{3}}}。它的频率响应为：", y)
    y = box(p, r"H(e^{j\omega})=\frac{1+e^{-j\omega}+e^{-j2\omega}}{3}", y, 56)
    y = para(p, r"在 {{\omega=\frac{2\pi}{3}}} 处，三个复指数相量之和为零，因此该频率被完全抑制。低频附近幅度较大，故它具有平滑、抑制高频干扰的作用。", y)
    y = sub(p, "判读顺序", y - 6)
    para(p, "先从幅频响应判断每个频率成分的去留，再从相频响应或群延迟判断到达时间和波形失真；两者必须结合阅读。", y)
    p.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_frequency_response_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    p = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    p.setTitle("数字信号处理讲义：第二章系统频率响应")
    for draw in (page_one, page_two, page_three):
        draw(p)
    p.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
