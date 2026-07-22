from __future__ import annotations
import json, sys
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from sample.tools import build_sample as style
MODEL_PATH=Path('full/source/chapter_01_convolution_properties_component.json')
CHAPTER='第一章 离散时间信号与系统'; PALE=HexColor('#F4F7F8')

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
 start(p,1); y=title(p,'线性卷积的运算规则')
 y=para(p,'卷积满足交换律、结合律和分配律。这些规律分别对应 LSI 系统的级联顺序可交换、多个级联系统可合并，以及并联系统可合并。',y)
 y=sec(p,'交换律',y-2); y=box(p,r'x(n)*h(n)=h(n)*x(n)',y,45)
 y=para(p,'因此串联系统中，两个单位脉冲响应 {{h_1(n)}}、{{h_2(n)}} 的先后顺序不改变总响应。',y)
 y=sec(p,'结合律',y-2); y=box(p,r'[x(n)*h_1(n)]*h_2(n)=x(n)*[h_1(n)*h_2(n)]',y,50)
 y=para(p,'可先把两个系统合成为等效冲激响应 {{h_1(n)*h_2(n)}}，再和输入卷积。',y)
 y=sec(p,'分配律',y-2); y=box(p,r'x(n)*[h_1(n)+h_2(n)]=x(n)*h_1(n)+x(n)*h_2(n)',y,50)
 style.draw_note(p,'记忆：串联对应卷积、并联对应相加；卷积交换律允许改变级联次序。',y-3); p.showPage()

def p2(p):
 start(p,2); y=title(p,'有限支持序列的卷积区间')
 y=para(p,'设 {{x(n)}} 仅在 {{N_1\\leq n\\leq N_2}} 非零，{{h(n)}} 仅在 {{N_3\\leq n\\leq N_4}} 非零。求 {{y(n)=x(n)*h(n)}} 的非零区间。',y)
 y=sec(p,'由重叠条件判断首尾位置',y-2)
 y=box(p,r'x(m)\ne0:\ N_1\leq m\leq N_2,\qquad h(n-m)\ne0:\ n-N_4\leq m\leq n-N_3',y,58)
 y=para(p,'当 {{n<N_1+N_3}} 时二者尚未重叠，输出为零；第一次重叠发生在 {{n=N_1+N_3}}。最后一次重叠发生在 {{n=N_2+N_4}}。',y)
 y=box(p,r'N_1+N_3\leq n\leq N_2+N_4',y,48)
 y=para(p,'若两序列分别有长度 {{L_x=N_2-N_1+1}} 与 {{L_h=N_4-N_3+1}}，则输出长度为 {{L_x+L_h-1}}。',y)
 y=sec(p,'用求和上下限复核',y-2)
 y=para(p,'卷积和中同时满足两段非零条件的求和变量必须落在它们的交集内。该交集非空时，便得到上面的输出区间。',y)
 style.draw_note(p,'区间端点相加是有限长卷积最重要的快速检查；它不替代逐项计算，但可立刻发现漏项。',y-3); p.showPage()

def p3(p):
 start(p,3); y=title(p,'应用例：延时叠加系统')
 y=para(p,'某 LSI 系统的单位脉冲响应为 {{h(n)=\\delta(n)+\\alpha\\delta(n-R)}}，其中 {{0<\\alpha<1}}，{{R}} 为正整数。',y)
 y=sec(p,'输出推导',y-2); y=box(p,r'y(n)=x(n)*[\delta(n)+\alpha\delta(n-R)]',y,48)
 y=box(p,r'y(n)=x(n)+\alpha x(n-R)',y,48)
 y=para(p,'第一项是原信号，第二项是延迟 {{R}} 个采样点并衰减 {{\\alpha}} 倍的副本。因此该系统形成单次回声；{{R}} 决定回声延迟，{{\\alpha}} 决定回声强度。',y)
 y=sec(p,'与范围约束的关系',y-2)
 y=para(p,'这里保留回声的离散时间系统模型与推导；原课件中的音频读写、程序代码和试听实验均不纳入讲义。',y)
 y=sec(p,'参数的作用',y-2)
 y=para(p,'R 决定副本相对原信号向右平移的采样点数；α 决定副本的幅度比例。因此同一模型既能描述回声，也能描述一般离散信号的延时叠加。',y)
 style.draw_note(p,'同一表达式也可用于一般信号的延迟叠加分析，不依赖特定软件或音频文件。',y-4); p.showPage()

def p4(p):
 start(p,4); y=title(p,'实序列的相关：相似度与延时')
 y=para(p,'相关函数用于衡量两个序列在不同相对位移下的相似程度。对实序列，互相关和自相关可写为卷积形式。',y)
 y=sec(p,'互相关与自相关',y-2)
 y=box(p,r'r_{xy}(n)=x(n)*y(-n),\qquad r_{yx}(n)=y(n)*x(-n)',y,50)
 y=box(p,r'r_{xx}(n)=x(n)*x(-n)',y,48)
 y=para(p,'计算相关时，先将其中一个序列反褶，再随 {{n}} 移位，与另一个序列逐点相乘并相加。相关峰值对应两序列最匹配的相对位置。',y)
 y=sec(p,'延时估计例',y-2)
 y=para(p,'若 {{y(n)=x(n-2)+w(n)}}，其中 {{w(n)}} 为零均值噪声，则 {{r_{yx}(n)}} 在 {{n=2}} 附近出现显著峰值；这表明 {{y(n)}} 与延迟两点的 {{x(n)}} 最相似。',y)
 style.draw_note(p,'相关强调“对齐后有多像”，卷积强调“系统如何叠加响应”。两者都包含反褶、移位、相乘、相加，但解释不同。',y-4); p.showPage()

def build_pdf(root=ROOT,output_path=None):
 style.register_fonts(); load_model(root); out=output_path or root/'full/outputs/chapter_01_convolution_properties_component.pdf'; out.parent.mkdir(parents=True,exist_ok=True); p=canvas.Canvas(str(out),pagesize=A4); p.setTitle('数字信号处理讲义：卷积性质与相关'); p1(p);p2(p);p3(p);p4(p);p.save();return out
if __name__=='__main__': print(build_pdf())
