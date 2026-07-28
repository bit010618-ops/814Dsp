from __future__ import annotations
import json, sys
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from sample.tools import build_sample as style
MODEL_PATH=Path('full/source/chapter_01_causal_stable_component.json')
CHAPTER='第一章 离散时间信号与系统'; PALE=HexColor('#F4F7F8')
def load_model(root=ROOT): return json.loads((root/MODEL_PATH).read_text(encoding='utf-8'))
def _restore_legacy_text(text):
 try:
  return text.encode('latin1').decode('gbk')
 except UnicodeEncodeError:
  return text

def start(p,n): style.draw_header(p,_restore_legacy_text(CHAPTER)); style.draw_footer(p,n)
def title(p,t,y=730):
 t=_restore_legacy_text(t)
 if t == 'LSI系统的稳定性条件':
  return style.draw_continuation_title(p,t,746)
 return style.draw_title(p,t,y)
def sec(p,t,y):
 t=_restore_legacy_text(t)
 if t == '例题': t='例：'
 return style.draw_continuation_title(p,t,y)
def para(p,t,y):
 t=_restore_legacy_text(t)
 if 'h(n)=\\delta(n-2)+\\delta(n+2)' in t and '非因果' in t:
  t='例：已知 LSI 系统的单位脉冲响应{{h(n)}}，判断系统的因果性。'+t
 if 'h(n)=\\delta(n-2)+\\delta(n+2)' in t and '稳定' in t and '非因果' not in t:
  t='例：已知 LSI 系统的单位脉冲响应{{h(n)}}，判断系统的稳定性。'+t
 return style.draw_rich_paragraph(p,t,62,y,A4[0]-124)
def box(p,f,y,h=50):
 a,iw,ih=style._math_metrics(f,style.DISPLAY_FORMULA_SIZE); dh=min(h-12,ih*72/300); dw=iw*dh/ih; lim=A4[0]-148
 if dw>lim: dw,dh=lim,dh*lim/dw
 p.setFillColor(PALE); p.roundRect(62,y-h,A4[0]-124,h,3,fill=1,stroke=0); p.drawImage(ImageReader(str(a)),(A4[0]-dw)/2,y-h+(h-dh)/2,dw,dh,mask='auto'); return y-h-12

def p1(p):
 start(p,1); y=title(p,'一般系统的因果性')
 y=para(p,'若任意时刻 {{n=n_0}} 的输出 {{y(n_0)}} 只依赖于 {{n\\leq n_0}} 的输入 {{x(n)}}，则该系统为因果系统；只要输出需要未来输入，系统便为非因果。',y)
 y=sec(p,'按输入索引判断',y-2)
 y=box(p,r'y(n_0)\quad\Longleftarrow\quad x(n),\ n\leq n_0',y,48)
 y=para(p,'判断时只看输出中出现的输入样值索引，不把已知的时间函数误判为输入。',y)
 y=sec(p,'例题',y-2)
 y=para(p,'（1）{{y(n)=n x(n)}}：因果，{{y(n_0)}} 只取决于 {{n=n_0}} 的输入 {{x(n)}}。 （2）{{y(n)=x(n+2)}}：非因果，{{y(0)=x(2)}}。 （3）{{y(n)=x(n^2)}}：非因果，{{y(2)=x(4)}}。 （4）{{y(n)=x(-n)}}：非因果，{{y(-2)=x(2)}}。 （5）{{y(n)=\\sin(n+2)x(n)}}：因果，{{\\sin(n+2)}} 不是输入。',y)
 y=sec(p,'LSI 系统的因果性条件',y-10)
 y=para(p,'对 LSI 系统，{{y(n)=h(n)*x(n)}}。若 {{h(m)}} 在 {{m<0}} 时非零，卷积和中会含有 {{x(n-m)=x(n+|m|)}}，这正是未来输入。',y)
 y=box(p,r'h(n)=0\quad(n<0)',y,52)
 y=sec(p,'四个单位脉冲响应例',y-2)
 para(p,'（1）{{h(n)=\\delta(n-2)+\\delta(n+2)}}：非因果，{{h(-2)\\ne0}}。 （2）{{h(n)=0.5^n u(n-2)}}：因果，当 {{n\\geq2}} 时 {{h(n)\\ne0}}。 （3）{{h(n)=2^n u(-n-1)}}：非因果，当 {{n\\leq-1}} 时 {{h(n)\\ne0}}。 （4）{{h(n)=0.5^n}}：非因果，当 {{-\\infty\\leq n\\leq\\infty}} 时 {{h(n)}} 有值。',y); p.showPage()

def p2(p):
 start(p,2); y=sec(p,'判题步骤',746)
 y=para(p,'先确认系统是否为 LSI；再检查 {{n<0}} 的单位脉冲响应是否全为零。对有限长序列，只需找最左侧非零样值。',y)
 y=sec(p,'一般系统的稳定性',y-10)
 y=para(p,'稳定性采用 BIBO（有界输入、有界输出）定义：若任意有界输入都产生有界输出，则系统稳定。时间索引 {{n}} 不受限制。',y)
 box(p,r'|x(n)|\leq M<\infty\ \Longrightarrow\ |y(n)|\leq P<\infty',y,50); p.showPage()

def p3(p):
 start(p,3); y=sec(p,'一般系统的稳定性（续）',746)
 y=sec(p,'例题',y-2)
 y=para(p,'（1）{{y(n)=n x(n)}}：不稳定，{{n=\\infty}} 时 {{y(n)=\\infty}}。 （2）{{y(n)=x(n^2)}}：稳定，有界输入产生有界输出。',y)
 y=box(p,r'y(n)=\frac{1}{3}\sum_{k=n-1}^{n+1}x(k)',y,48)
 y=para(p,'（3）稳定，有界输入产生有界输出。',y)
 y=box(p,r'y(n)=\sum_{k=n_0}^{n}x(k)',y,48)
 y=para(p,'（4）不稳定，{{y(n)}} 是 {{n-n_0+1}} 项输入的求和；当 {{n=\\infty}} 时，{{y(n)=\\infty}}。',y)
 y=sec(p,'与因果性的区别',y-2)
 y=para(p,'因果性问“是否依赖未来输入”，稳定性问“有界输入是否仍有界”。两种性质彼此独立，判断时不能互相替代。',y)
 style.draw_note(p,'反例常取 {{x(n)=1}}；它有界，却能使累加器输出持续增长。',y-3); p.showPage()

def p4(p):
 start(p,4); y=title(p,'LSI 系统的稳定性条件')
 y=para(p,'LSI 系统稳定的充分必要条件是单位脉冲响应绝对可和。由线性卷积可直接建立有界输出的上界。',y)
 y=box(p,r'\sum_{n=-\infty}^{\infty}|h(n)|=q<\infty',y,50)
 y=box(p,r'|y(n)|\leq\sum_{m=-\infty}^{\infty}|h(m)|\,|x(n-m)|\leq Mq',y,54)
 y=sec(p,'四个单位脉冲响应例',y-2)
 y=para(p,'（1）{{h(n)=\\delta(n-2)+\\delta(n+2)}}：稳定。 （2）{{h(n)=0.5^n u(n-2)}}：稳定，{{n\\geq2}} 有值，收敛。 （3）{{h(n)=2^n u(-n-1)}}：稳定，{{n<-1}} 有值，收敛。 （4）{{h(n)=0.5^n}}：不稳定，{{h(n)}} 不满足绝对可和。',y)
 style.draw_note(p,'考研判据：LSI 看 {{\\sum|h(n)|}}；一般系统则必须从 BIBO 定义或反例出发。',y-3); p.showPage()

def build_pdf(root=ROOT,output_path=None):
 style.register_fonts(); load_model(root); out=output_path or root/'full/outputs/chapter_01_causal_stable_component.pdf'; out.parent.mkdir(parents=True,exist_ok=True); p=canvas.Canvas(str(out),pagesize=A4); p.setTitle('数字信号处理讲义：因果性与稳定性'); p1(p);p2(p);p3(p);p4(p);p.save();return out
if __name__=='__main__': print(build_pdf())
