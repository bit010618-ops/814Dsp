from __future__ import annotations
import json, sys
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from sample.tools import build_sample as style
MODEL_PATH=Path('full/source/chapter_01_difference_equation_component.json')
STRUCTURE_SLIDE=Path('full/artifacts/source_pages/chapter_01/difference_equation_feedback_structure.png')
CHAPTER='第一章 离散时间信号与系统'; PALE=HexColor('#F4F7F8'); BLUE=HexColor('#123B5D')
def load_model(root=ROOT): return json.loads((root/MODEL_PATH).read_text(encoding='utf-8'))
def start(p,n): style.draw_header(p,CHAPTER); style.draw_footer(p,n)
def title(p,t,y=774): return style.draw_title(p,t,y)
def sec(p,t,y): return style.draw_continuation_title(p,t,y)
def para(p,t,y): return style.draw_rich_paragraph(p,t,62,y,A4[0]-124)
def box(p,f,y,h=50):
 a,iw,ih=style._math_metrics(f,style.DISPLAY_FORMULA_SIZE); dh=min(h-12,ih*72/300); dw=iw*dh/ih; lim=A4[0]-148
 if dw>lim: dw,dh=lim,dh*lim/dw
 p.setFillColor(PALE); p.roundRect(62,y-h,A4[0]-124,h,3,fill=1,stroke=0); p.drawImage(ImageReader(str(a)),(A4[0]-dw)/2,y-h+(h-dh)/2,dw,dh,mask='auto'); return y-h-12

def p1(p):
 start(p,1); y=title(p,'常系数线性差分方程')
 y=para(p,'常系数线性差分方程以过去和当前的输入、输出样值建立关系，是离散时间系统的重要表示方法。',y)
 y=box(p,r'\sum_{k=0}^{N}a_k y(n-k)=\sum_{m=0}^{M}b_m x(n-m),\qquad a_0\ne0',y,55)
 y=sec(p,'三个术语',y-2)
 y=para(p,'常系数指 {{a_k}} 与 {{b_m}} 都是常数；阶数是输出项 {{y(n)}} 中变量序号最大值与最小值之差；线性指各输入、输出样值只出现一次幂且没有相乘项。这里“线性”的含义不同于系统线性。',y)
 y=sec(p,'四种求解思路',y-2)
 y=para(p,'经典解法通过齐次解、特解和边界条件求待定系数；迭代法直接逐项求数值；变换域法转入 {{z}} 域；卷积法先求 {{h(n)}}，再与 {{x(n)}} 卷积。',y)
 y=title(p,'迭代法：因果单位脉冲响应',y-12)
 y=para(p,'考虑一阶差分方程 {{y(n)-a y(n-1)=x(n)}}。令 {{x(n)=\\delta(n)}}，并采用因果零状态边界条件 {{h(n)=0}}（{{n<0}}）。',y); p.showPage()

def p2(p):
 start(p,2); y=sec(p,'迭代法：因果单位脉冲响应（续）',746)
 y=sec(p,'逐项迭代',y-2)
 y=box(p,r'h(0)=1,\qquad h(1)=a,\qquad h(2)=a^2',y,50)
 y=box(p,r'h(n)=a h(n-1)=a^n u(n)',y,50)
 y=para(p,'因此该解是因果的；当 {{|a|<1}} 时，{{h(n)}} 绝对可和，系统还稳定。',y)
 y=title(p,'迭代法：非因果单位脉冲响应',y-12)
 y=para(p,'对同一方程 {{y(n)-a y(n-1)=x(n)}}，若改用另一边界条件 {{h(n)=0}}（{{n>0}}），应从反向递推关系出发。',y)
 y=sec(p,'迭代法：非因果单位脉冲响应（续）',y-4)
 box(p,r'y(n-1)=a^{-1}[y(n)-x(n)]',y,50)
 p.showPage()

def p3(p):
 start(p,3); y=sec(p,'迭代法：非因果单位脉冲响应（续）',746)
 y=sec(p,'反向迭代',y-2)
 y=box(p,r'h(0)=0,\qquad h(-1)=-a^{-1},\qquad h(-2)=-a^{-2}',y,52)
 y=box(p,r'h(n)=-a^n u(-n-1)',y,50)
 y=para(p,'这个单位脉冲响应在负时间一侧有非零值，所以系统非因果。它与上一页具有相同的差分方程，却对应不同的边界条件。',y)
 y=title(p,'由差分方程得到系统结构',y-12)
 y=para(p,'差分方程表示法的优点之一，是可以直接读出把输入变成输出的运算结构。以一阶关系为例：',y)
 y=box(p,r'y(n)=b_0x(n)-a_1y(n-1)',y,48)
 y=sec(p,'一阶反馈结构',y-2); p.showPage()

def p4(p):
 start(p,4); y=sec(p,'由差分方程得到系统结构（续）',746)
 y=sec(p,'一阶反馈结构（续）',y-2)
 slide=ROOT/STRUCTURE_SLIDE
 if not slide.exists(): raise FileNotFoundError(slide)
 y=para(p,'下图保留原课件中完整的一阶反馈结构，以确保乘法器、加法器、延迟单元、反馈支路及其系数位置均可直接辨认。',y)
 w=A4[0]-124; h=w*1050/1867
 p.drawImage(ImageReader(str(slide)),62,y-h,w,h,mask='auto')
 y=y-h-16
 y=para(p,'{{b_0}} 对当前输入进行乘法，{{z^{-1}}} 表示一个采样周期的延迟，{{-a_1}} 形成反馈支路，求和器给出输出。由图可数出乘法器、加法器和延迟单元。',y)
 style.draw_note(p,'结构图中的每一条线都对应差分方程的一项；系数与延迟的位置不得互换。',y-3); p.showPage(); return
 left,cy=92,y-55; bw,bh=64,36
 p.setStrokeColor(BLUE); p.setFillColor(HexColor('#F4F7F8'))
 for x,label in [(180,'b0'),(320,'Σ')]:
  p.roundRect(x,cy-bh/2,bw,bh,3,fill=1,stroke=1); p.setFillColor(BLUE); p.setFont(style.FONT_SANS,12); p.drawCentredString(x+bw/2,cy-4,label); p.setFillColor(HexColor('#F4F7F8'))
 for x,label in [(300,'-a1'),(420,'z^-1')]:
  p.roundRect(x,cy-76-bh/2,bw,bh,3,fill=1,stroke=1); p.setFillColor(BLUE); p.setFont(style.FONT_SANS,12); p.drawCentredString(x+bw/2,cy-80,label); p.setFillColor(HexColor('#F4F7F8'))
 p.setFillColor(BLUE); p.setFont(style.FONT_SANS,11); p.drawString(82,cy-4,'x(n)'); p.drawString(530,cy-4,'y(n)')
 for x1,x2 in [(118,180),(244,320),(384,520)]: p.line(x1,cy,x2,cy); p.line(x2,cy,x2-7,cy+3); p.line(x2,cy,x2-7,cy-3)
 p.line(520,cy,520,cy-76); p.line(520,cy-76,484,cy-76); p.line(484,cy-76,484,cy-18)
 p.line(420,cy-76,364,cy-76); p.line(364,cy-76,364,cy-18)
 p.line(300,cy-76,288,cy-76); p.line(288,cy-76,288,cy-34); p.line(288,cy-34,320,cy-18); p.line(320,cy-18,315,cy-21); p.line(320,cy-18,318,cy-24)
 y=cy-112
 y=para(p,'{{b_0}} 对当前输入进行乘法，{{z^{-1}}} 表示一个采样周期的延迟，{{-a_1}} 形成反馈支路，求和器给出输出。由图可数出乘法器、加法器和延迟单元。',y)
 style.draw_note(p,'结构图中的每一条线都对应差分方程的一项；系数与延迟的位置不得交换。',y-3); p.showPage()

def p1_reflow(p):
 start(p,1); y=title(p,'常系数线性差分方程')
 y=para(p,'常系数线性差分方程以过去和当前的输入、输出样值建立关系，是离散时间系统的重要表示方法。',y)
 y=box(p,r'\sum_{k=0}^{N}a_k y(n-k)=\sum_{m=0}^{M}b_m x(n-m),\qquad a_0\ne0',y,55)
 y=sec(p,'三个术语',y-2)
 y=para(p,'常系数指 {{a_k}} 与 {{b_m}} 都是常数；阶数是输出项 {{y(n)}} 中变量序号最大值与最小值之差；线性指各输入、输出样值只出现一次幂且没有相乘项。这里“线性”的含义不同于系统线性。',y)
 y=sec(p,'四种求解思路',y-2)
 y=para(p,'经典解法通过齐次解、特解和边界条件求待定系数；迭代法直接逐项求数值；变换域法转入 {{z}} 域；卷积法先求 {{h(n)}}，再与 {{x(n)}} 卷积。',y)
 y=title(p,'迭代法：因果单位脉冲响应',y-12)
 y=para(p,'考虑一阶差分方程 {{y(n)-a y(n-1)=x(n)}}。令 {{x(n)=\\delta(n)}}，并采用因果零状态边界条件 {{h(n)=0}}（{{n<0}}）。',y)
 y=sec(p,'逐项迭代',y-2)
 y=box(p,r'h(0)=1,\qquad h(1)=a,\qquad h(2)=a^2',y,50)
 y=box(p,r'h(n)=a h(n-1)=a^n u(n)',y,50)
 para(p,'因此该解是因果的；当 {{|a|<1}} 时，{{h(n)}} 绝对可和，系统还稳定。',y)
 p.showPage()


def p2_reflow(p):
 start(p,2); y=title(p,'迭代法：非因果单位脉冲响应')
 y=para(p,'对同一方程 {{y(n)-a y(n-1)=x(n)}}，若改用另一边界条件 {{h(n)=0}}（{{n>0}}），应从反向递推关系出发。',y)
 y=sec(p,'反向迭代',y-4)
 y=box(p,r'y(n-1)=a^{-1}[y(n)-x(n)]',y,50)
 y=box(p,r'h(0)=0,\qquad h(-1)=-a^{-1},\qquad h(-2)=-a^{-2}',y,52)
 y=box(p,r'h(n)=-a^n u(-n-1)',y,50)
 y=para(p,'这个单位脉冲响应在负时间一侧有非零值，所以系统非因果。它与上一页具有相同的差分方程，却对应不同的边界条件。',y)
 y=title(p,'由差分方程得到系统结构',y-12)
 y=para(p,'差分方程表示法的优点之一，是可以直接读出把输入变成输出的运算结构。以一阶关系为例：',y)
 y=box(p,r'y(n)=b_0x(n)-a_1y(n-1)',y,48)
 sec(p,'一阶反馈结构',y-2)
 p.showPage()


def p3_reflow(p):
 start(p,3); y=sec(p,'由差分方程得到系统结构（续）',746)
 y=sec(p,'一阶反馈结构（续）',y-2)
 slide=ROOT/STRUCTURE_SLIDE
 if not slide.exists(): raise FileNotFoundError(slide)
 y=para(p,'下图给出完整的一阶反馈结构，以确保乘法器、加法器、延迟单元、反馈支路及其系数位置均可直接辨认。',y)
 w=A4[0]-124; h=w*1050/1867
 p.drawImage(ImageReader(str(slide)),62,y-h,w,h,mask='auto')
 y=y-h-16
 y=para(p,'{{b_0}} 对当前输入进行乘法，{{z^{-1}}} 表示一个采样周期的延迟，{{-a_1}} 形成反馈支路，求和器给出输出。由图可数出乘法器、加法器和延迟单元。',y)
 y=title(p,'理想时域采样',y-18)
 y=para(p,'采样器可看作每隔 {{T}} 秒闭合一次的电子开关。它利用周期冲激函数序列从连续信号 {{x_a(t)}} 中抽取样值，使时间变量离散。',y)
 box(p,r'\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT),\qquad x_s(t)=x_a(t)\delta_T(t)',y,58)
 p.showPage()


def build_pdf(root=ROOT,output_path=None):
 style.register_fonts(); load_model(root); out=output_path or root/'full/outputs/chapter_01_difference_equation_component.pdf'; out.parent.mkdir(parents=True,exist_ok=True); p=canvas.Canvas(str(out),pagesize=A4); p.setTitle('数字信号处理讲义：常系数线性差分方程'); p1_reflow(p);p2_reflow(p);p3_reflow(p);p.save();return out
if __name__=='__main__': print(build_pdf())
