# -*- coding: utf-8 -*-
"""docs/{c}.html 마인드맵 SVG의 5개 노드 라벨/이모지를 analysis mindmap 주제로 교체"""
import sys, io, re, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMOJI={'감사함':'🙏','존경심':'🌟','사랑함':'💗','미안함':'🥹','아쉬움':'🥲','성장함':'🌱',
 '성장의지':'🌱','행복감':'😊','신뢰감':'🤝','유대감':'🫂','애정함':'💕','따뜻함':'🤍',
 '다짐함':'💪','기대감':'✨','그리움':'🌙','응원함':'💪','즐거움':'😄','자부심':'✨','의지':'🔥'}
DEFAULT='💌'

def fix(cls):
    fp=f'docs/{cls}.html'
    s=open(fp,encoding='utf-8').read()
    a=json.load(open(f'analysis/{cls}_analysis.json',encoding='utf-8'))
    themes=list(a.get('mindmap',{}).keys())[:5]
    if len(themes)<5:
        print(cls,'WARN themes',len(themes)); return
    miss=0
    for i,lab in enumerate(themes):
        emo=EMOJI.get(lab,DEFAULT)
        # node i: 첫 text(font-size 22)=이모지, 둘째 text(font-size 16 fill white)=라벨
        pat=re.compile(r'(<g class="mnd mnd%d">.*?font-size="22">)([^<]*)(</text>.*?font-size="16" fill="white">)([^<]*)(</text>)'%i, re.DOTALL)
        new,n=pat.subn(lambda m: m.group(1)+emo+m.group(3)+lab+m.group(5), s, count=1)
        if n!=1: miss+=1; print(f'  {cls} mnd{i} NOT matched')
        else: s=new
    if miss==0:
        open(fp,'w',encoding='utf-8').write(s)
        print(cls,'OK ->',themes)

if __name__=='__main__':
    for c in (sys.argv[1:] or ['1-1','1-2','1-3','1-5','1-6','1-7','1-8']):
        fix(c)
