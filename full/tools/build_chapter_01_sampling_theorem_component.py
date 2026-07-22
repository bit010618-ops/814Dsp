from __future__ import annotations
import json, sys
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from sample.tools import build_sample as style
MODEL_PATH=Path('full/source/chapter_01_sampling_theorem_component.json')
CHAPTER='第一章 离散时间信号与系统'; PALE=HexColor('#F4F7F8'); BLUE=HexColor('#123B5D'); TEAL=HexColor('#0F8B8D'); RED=HexColor('#B13A3A')
def load_model(root=ROOT): return json.loads((root/MODEL_PATH).read_text(encoding='utf-8'))
def start(p,n): style.draw_header(p,CHAPTER); style.draw_footer(p,n)
def title(p,t,y=774): return style.draw_title(p,t,y)
def sec(p,t,y): return style.draw_continuation_title(p,t,y)
def para(p,t,y): return style.draw_rich_paragraph(p,t,62,y,A4[0]-124)
def box(p,f,y,h=50):
 a,iw,ih=style._math_metrics(f,style.DISPLAY_FORMULA_SIZE); dh=min(h-12,ih*72/300); dw=iw*dh/ih; lim=A4[0]-148
 if dw>lim: dw,dh=lim,dh*lim/dw
 p.setFillColor(PALE); p.roundRect(62,y-h,A4[0]-124,h,3,fill=1,stroke=0); p.drawImage(ImageReader(str(a)),(A4[0]-dw)/2,y-h+(h-dh)/2,dw,dh,mask='auto'); return y-h-12
def arrow(p,x1,y1,x2,y2):
 p.line(x1,y1,x2,y2); p.line(x2,y2,x2-6,y2+3); p.line(x2,y2,x2-6,y2-3)
def spectrum(p,x,y,w,h,centers,half,color=TEAL):
 p.setStrokeColor(BLUE); p.setLineWidth(.65); p.line(x,y,x+w,y); p.line(x+w,y,x+w-6,y+3); p.line(x+w,y,x+w-6,y-3)
 p.setStrokeColor(color); p.setLineWidth(1.1)
 for c in centers:
  xx=x+c*w
  p.line(xx-half*w,y,xx,y+h); p.line(xx,y+h,xx+half*w,y)
 p.setFillColor(BLUE); p.setFont(style.FONT_SERIF,8); p.drawString(x+w+4,y-3,'Ω')
def p1(p):
 start(p,1); y=title(p,'理想时域采样')
 y=para(p,'采样器可看作每隔 {{T}} 秒闭合一次的电子开关。它利用周期冲激函数序列从连续信号 {{x_a(t)}} 中抽取样值，使时间变量离散。',y)
 y=box(p,r'\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT),\qquad x_s(t)=x_a(t)\delta_T(t)',y,58)
 y=box(p,r'x(n)=x_a(nT),\qquad f_s=\frac{1}{T},\qquad \Omega_s=\frac{2\pi}{T}',y,52)
 y=sec(p,'采样瞬间的幅度',y-2)
 y=para(p,'理想采样输出在 {{t=nT}} 处的冲激权重等于原连续信号的瞬时幅度；{{T}} 是采样间隔，{{f_s}} 和 {{\\Omega_s}} 分别是采样频率与采样角频率。',y)
 style.draw_note(p,'采样不是把波形“压缩”成点，而是在均匀时刻保留其精确样值。',y-3); p.showPage()
def p2(p):
 start(p,2); y=title(p,'采样后的频域周期延拓')
 y=para(p,'时域相乘对应频域卷积。冲激序列在频域仍为间隔 {{\\Omega_s}} 的冲激序列，因此原信号频谱会以 {{\\Omega_s}} 为周期被复制。',y)
 y=box(p,r'X_s(j\Omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}X_a\!\left[j(\Omega-k\Omega_s)\right]',y,56)
 y=sec(p,'频域示意',y-2); base=y-100
 spectrum(p,92,base,410,55,[.1,.5,.9],.11); p.setFillColor(BLUE); p.setFont(style.FONT_SERIF,8); p.drawCentredString(297,base-15,'−Ωs                 0                 Ωs')
 y=base-37; y=para(p,'每个三角谱表示原频谱的一个平移副本。时域离散必然对应频域周期；这也是后续混叠与重构判断的起点。',y)
 style.draw_note(p,'只要谱副本间仍有空隙，就可通过低通滤波器取回中央的原频谱。',y-3); p.showPage()
def p3(p):
 start(p,3); y=title(p,'不混叠与混叠')
 y=para(p,'设 {{x_a(t)}} 为带限信号，其最高角频率为 {{\\Omega_h}}。谱副本是否重叠完全由 {{\\Omega_h}} 与 {{\\frac{\\Omega_s}{2}}} 的关系决定。',y)
 y=sec(p,'情况一：不混叠',y-2); y=box(p,r'\Omega_h\leq\frac{\Omega_s}{2}',y,45)
 base=y-68; spectrum(p,92,base,410,42,[.1,.5,.9],.075); y=base-26
 y=para(p,'相邻频谱副本互不重叠。理论上用截止角频率为 {{\\frac{\\Omega_s}{2}}} 的理想低通滤波器即可恢复原信号。',y)
 y=sec(p,'情况二：混叠',y-2); y=box(p,r'\Omega_h>\frac{\Omega_s}{2}',y,45)
 base=y-68; spectrum(p,92,base,410,42,[.16,.5,.84],.20,RED); y=base-26
 y=para(p,'副本相互交叠，原频谱不再能唯一分离；这种不可逆失真称为混叠。',y)
 style.draw_note(p,'提高采样频率或先限制输入带宽，才能避免混叠。',y-3); p.showPage()
def p4(p):
 start(p,4); y=title(p,'Nyquist-Shannon 时域采样定理')
 y=para(p,'若 {{x_a(t)}} 是带限信号，且 {{|\\Omega|\\geq\\Omega_h}} 时 {{X_a(j\\Omega)=0}}，则它能由样本 {{x(n)=x_a(nT)}} 唯一确定，当且仅当满足下式。',y)
 y=box(p,r'\Omega_s\geq2\Omega_h\qquad\Longleftrightarrow\qquad f_s\geq2f_h',y,52)
 y=sec(p,'折叠频率与三种频率',y-2)
 y=para(p,'{{\\frac{\\Omega_s}{2}}} 称为折叠频率：超过它的频率成分会折回并造成混叠。连续时间角频率单位为弧度每秒，普通频率单位为赫兹，离散时间的数字角频率单位为弧度。',y)
 y=box(p,r'\omega=\Omega T=2\pi\frac{f}{f_s}',y,48)
 y=para(p,'因此，时域离散与频域周期是一对对应关系；采样定理给出了在不丢失信息的条件下把连续信号转化为序列的最低采样率。',y)
 style.draw_note(p,'考试中先统一频率单位，再比较最高频率与采样频率的一半。',y-3); p.showPage()
def build_pdf(root=ROOT,output_path=None):
 style.register_fonts(); load_model(root); out=output_path or root/'full/outputs/chapter_01_sampling_theorem_component.pdf'; out.parent.mkdir(parents=True,exist_ok=True); p=canvas.Canvas(str(out),pagesize=A4); p.setTitle('数字信号处理讲义：时域采样定理'); p1(p);p2(p);p3(p);p4(p);p.save(); return out
if __name__=='__main__': print(build_pdf())
