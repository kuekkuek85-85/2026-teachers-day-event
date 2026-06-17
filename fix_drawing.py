# -*- coding: utf-8 -*-
"""docs/{c}.html 페이지11(그림 분석) 카드를 analysis drawing_bullets(가변 개수)로 재구성"""
import sys, io, re, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# (shadow, grad1, grad2, boldcolor)
CARDC=[('rgba(194,24,91,.1)','#FF6B9D','#C2185B','#C2185B'),
       ('rgba(123,31,162,.1)','#CE93D8','#7B1FA2','#7B1FA2'),
       ('rgba(0,188,212,.12)','#4DD0E1','#00A5BC','#00A5BC'),
       ('rgba(255,112,67,.12)','#FFB74D','#FF7043','#FF7043'),
       ('rgba(102,187,106,.12)','#81C784','#43A047','#43A047'),
       ('rgba(194,24,91,.1)','#F06292','#C2185B','#C2185B')]
def esc(s): return html.escape(s, quote=False)
def fmt(text, bc):
    # **kw** -> <b>, 나머지 esc
    parts=re.split(r'\*\*(.+?)\*\*', text)
    out=''
    for i,p in enumerate(parts):
        out+= (f'<b style="color:{bc};">{esc(p)}</b>' if i%2 else esc(p))
    return out

def build_grid(bullets):
    n=len(bullets); cols=2 if n==4 else 3
    cards=[]
    for i,b in enumerate(bullets):
        sh,c1,c2,bc=CARDC[i%6]; delay=round(0.35+0.15*i,2)
        cards.append(f'          <div style="position:relative;background:#fff;border-radius:18px;padding:22px 20px 22px 64px;'
            f'box-shadow:0 12px 28px {sh};font-size:16px;line-height:1.55;color:#3A2230;font-weight:500;animation:popIn .5s {delay}s both;">'
            f'<span style="position:absolute;left:18px;top:20px;width:32px;height:32px;border-radius:50%;'
            f'background:linear-gradient(135deg,{c1},{c2});color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;">{i+1}</span>'
            f'{fmt(b,bc)}</div>')
    grid=(f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:18px;margin-top:auto;margin-bottom:auto;">\n'
          + '\n'.join(cards) + '\n        </div>')
    return grid

PAT=re.compile(r'<div style="display:grid;grid-template-columns:repeat\(3,1fr\);gap:18px;margin-top:auto;margin-bottom:auto;">.*?</div>(\s*</div>\s*</sc-if>)', re.DOTALL)

def fix(cls):
    fp=f'docs/{cls}.html'
    s=open(fp,encoding='utf-8').read()
    a=json.load(open(f'analysis/{cls}_analysis.json',encoding='utf-8'))
    bullets=a.get('drawing_bullets',[])
    if not bullets: print(cls,'no bullets'); return
    grid=build_grid(bullets)
    new,n=PAT.subn(grid+r'\1', s, count=1)
    if n!=1: print(cls,'WARN matched',n); return
    open(fp,'w',encoding='utf-8').write(new)
    print(cls,'OK ->',len(bullets),'개')

if __name__=='__main__':
    for c in (sys.argv[1:] or ['1-1','1-2','1-3','1-5','1-6','1-7','1-8']):
        fix(c)
