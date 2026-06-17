# -*- coding: utf-8 -*-
"""각 반 docs/{c}.html 의 7페이지 워드클라우드를 analysis/{c}_analysis.json 키워드로 교체"""
import sys, io, re, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# (tx, ty, base_fontsize, weight, color, delay)  — 1-1 레이아웃 17슬롯 (중앙→주변, 큰→작은)
SLOTS = [
 (0,-6,68,900,'#FF6B9D','.35'),
 (198,-58,50,900,'#4DD0E1','.5'),
 (-200,-72,46,900,'#FFD54F','.45'),
 (268,54,42,900,'#FF8A65','.6'),
 (-300,36,40,900,'#CE93D8','.55'),
 (86,-128,40,900,'#FFAB91','.9'),
 (120,104,38,800,'#80DEEA','.7'),
 (-128,96,36,800,'#F48FB1','.65'),
 (-70,-120,36,800,'#B39DDB','.85'),
 (360,-30,34,800,'#F8BBD0','.8'),
 (-30,150,34,800,'#F06292','1.05'),
 (-372,-44,32,800,'#FFCC80','.75'),
 (236,138,32,800,'#4DB6AC','1'),
 (-250,130,30,700,'#9FA8DA','.95'),
 (34,-178,30,700,'#FFD54F','1.1'),
 (408,104,30,800,'#4DD0E1','1.2'),
 (-420,78,28,700,'#CE93D8','1.15'),
]
def cap(n):
    return {0:999,1:999,2:999,3:58,4:44,5:36,6:30}.get(n,26)

def esc(s): return html.escape(s, quote=False)

def build_words(wc):
    words=sorted(wc, key=lambda w:(-int(w.get('size',1)), len(w['word'])))[:len(SLOTS)]
    out=[]
    for (tx,ty,fs,w,col,d), wd in zip(SLOTS, words):
        word=wd['word'].strip()
        f=min(fs, cap(len(word)))
        out.append(f'          <div style="position:absolute;left:50%;top:50%;--tx:{tx}px;--ty:{ty}px;'
                   f'font-size:{f}px;font-weight:{w};color:{col};animation:explode .7s {d}s both;">{esc(word)}</div>')
    return '\n'.join(out)

def fix(cls):
    fp=f'docs/{cls}.html'
    s=open(fp,encoding='utf-8').read()
    a=json.load(open(f'analysis/{cls}_analysis.json',encoding='utf-8'))
    wc=a.get('wordcloud',[])
    if not wc:
        print(cls,'no wordcloud'); return
    words_html=build_words(wc)
    new,n=re.subn(r'(<div style="position:relative;flex:1;margin-top:4px;">)(.*?)(\n        </div>)',
                  lambda m: m.group(1)+'\n'+words_html+m.group(3), s, count=1, flags=re.DOTALL)
    if n!=1:
        print(cls,'WARN: container not found / matched',n); return
    open(fp,'w',encoding='utf-8').write(new)
    top=sorted(wc,key=lambda w:-int(w.get('size',1)))[:5]
    print(cls,'OK ->', ', '.join(w['word'] for w in top))

if __name__=='__main__':
    classes=sys.argv[1:] or ['1-1','1-2','1-3','1-5','1-6','1-7','1-8']
    for c in classes: fix(c)
