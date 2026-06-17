# -*- coding: utf-8 -*-
"""docs/{c}.html 마인드맵 SVG를 근거 키워드 포함 버전으로 교체"""
import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from make_mindmap import build_svg

def fix(cls):
    fp=f'docs/{cls}.html'
    s=open(fp,encoding='utf-8').read()
    a=json.load(open(f'analysis/{cls}_analysis.json',encoding='utf-8'))
    mm=a.get('mindmap',{})
    if len(mm)<5: print(cls,'WARN themes',len(mm)); return
    svg=build_svg(mm)
    new,n=re.subn(r'(<div style="position:relative;flex:1;margin-top:6px;">\s*)<svg.*?</svg>',
                  lambda m: m.group(1)+svg, s, count=1, flags=re.DOTALL)
    if n!=1: print(cls,'WARN svg matched',n); return
    open(fp,'w',encoding='utf-8').write(new)
    print(cls,'OK ->',list(mm.keys()))

if __name__=='__main__':
    for c in (sys.argv[1:] or ['1-1','1-2','1-3','1-5','1-6','1-7','1-8']):
        fix(c)
