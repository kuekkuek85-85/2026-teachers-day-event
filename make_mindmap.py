# -*- coding: utf-8 -*-
"""마인드맵 SVG 생성: 5개 노드(주제 라벨 + 근거 키워드) 방사형 배치"""
import math, html

EMOJI={'감사함':'🙏','존경심':'🌟','사랑함':'💗','미안함':'🥹','아쉬움':'🥲','성장함':'🌱',
 '성장의지':'🌱','행복감':'😊','신뢰감':'🤝','유대감':'🫂','애정함':'💕','따뜻함':'🤍',
 '다짐함':'💪','기대감':'✨','그리움':'🌙','응원함':'💪','즐거움':'😄','자부심':'✨',
 '의지':'🔥','기원함':'🍀','자랑스러움':'✨','미안한마음':'🥹'}
# (branch_grad_to, node_grad_from, node_grad_to)
COLORS=[('#FF6B9D','#FF9EC8','#C2185B'),
        ('#AB47BC','#CE93D8','#7B1FA2'),
        ('#00BCD4','#4DD0E1','#00838F'),
        ('#FF7043','#FFAB91','#E64A19'),
        ('#66BB6A','#A5D6A7','#2E7D32')]
DOT=['#FF6B9D','#AB47BC','#00BCD4','#FF7043','#66BB6A']

SUBEMO=[('감사','🙏'),('존경','🌟'),('사랑','💗'),('애정','💕'),('미안','🥹'),('아쉬','🥲'),
 ('성장','🌱'),('행복','😊'),('긍정','😊'),('신뢰','🤝'),('유대','🫂'),('관계','🫂'),('따뜻','🤍'),
 ('다짐','💪'),('의지','🔥'),('기대','✨'),('기원','🍀'),('그리','🌙'),('응원','💪'),('즐거','😄'),('영향','✨')]
def emoji_for(lab):
    if lab in EMOJI: return EMOJI[lab]
    for k,e in SUBEMO:
        if k in lab: return e
    return '💌'

def esc(s): return html.escape(str(s), quote=False)

def build_svg(themes):
    """themes: dict {label: [kw1,kw2,kw3]} (5개)"""
    labels=list(themes.keys())[:5]
    CX,CY,R=480,255,185
    BW,BH=176,112
    angles=[-90,-18,54,126,198]
    defs=['<defs>']
    for i,(bg,nf,nt) in enumerate(COLORS):
        defs.append(f'<radialGradient id="ng{i}" cx="40%" cy="30%" r="75%"><stop offset="0%" stop-color="{nf}"/><stop offset="100%" stop-color="{nt}"/></radialGradient>')
    defs.append('<radialGradient id="cg" cx="40%" cy="35%" r="70%"><stop offset="0%" stop-color="#F06292"/><stop offset="55%" stop-color="#AD1457"/><stop offset="100%" stop-color="#6A1B9A"/></radialGradient>')
    defs.append('<filter id="mds" x="-25%" y="-25%" width="150%" height="150%"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="rgba(0,0,0,0.22)"/></filter>')
    defs.append('<filter id="mds2" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="rgba(194,24,91,0.4)"/></filter>')
    defs.append('</defs>')
    style=('<style>'
      '.mbr{stroke-dasharray:200;stroke-dashoffset:200;animation:mDrawBr .6s ease-out forwards;}'
      '.mbr0{animation-delay:.4s}.mbr1{animation-delay:.52s}.mbr2{animation-delay:.64s}.mbr3{animation-delay:.76s}.mbr4{animation-delay:.88s}'
      '@keyframes mDrawBr{to{stroke-dashoffset:0}}'
      '.mnd{opacity:0;transform-box:fill-box;transform-origin:center;animation:mNdPop .5s ease-out forwards;}'
      '.mnd0{animation-delay:.9s}.mnd1{animation-delay:1.02s}.mnd2{animation-delay:1.14s}.mnd3{animation-delay:1.26s}.mnd4{animation-delay:1.38s}'
      '@keyframes mNdPop{0%{opacity:0;transform:scale(.25)}70%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}'
      '.mct{opacity:0;transform-box:fill-box;transform-origin:center;animation:mNdPop .65s ease-out .2s forwards;}'
      '.mdc{opacity:0;animation:mDcFade 1.2s ease .3s forwards;}@keyframes mDcFade{to{opacity:1}}'
      '</style>')
    nodes_pos=[]
    for a in angles:
        rad=math.radians(a)
        nodes_pos.append((CX+R*math.cos(rad), CY+R*math.sin(rad)))
    parts=[f'<svg viewBox="0 0 960 525" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:50%;top:50%;width:960px;height:525px;transform:translate(-50%,-50%);overflow:visible;">']
    parts.append(''.join(defs)); parts.append(style)
    # decorative
    parts.append('<ellipse class="mdc" cx="120" cy="80" rx="92" ry="66" fill="#FFE4EE" opacity="0.4"/>')
    parts.append('<ellipse class="mdc" cx="840" cy="70" rx="80" ry="58" fill="#EDE7F6" opacity="0.38"/>')
    parts.append('<ellipse class="mdc" cx="820" cy="455" rx="98" ry="66" fill="#E0F7FA" opacity="0.4"/>')
    parts.append('<ellipse class="mdc" cx="120" cy="450" rx="84" ry="62" fill="#E8F5E9" opacity="0.4"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="170" fill="#FFF0F6" opacity="0.16"/>')
    # branches (center -> node center)
    for i,(nx,ny) in enumerate(nodes_pos):
        parts.append(f'<line class="mbr mbr{i}" x1="{CX}" y1="{CY}" x2="{nx:.0f}" y2="{ny:.0f}" stroke="{COLORS[i][0]}" stroke-width="6" stroke-linecap="round" opacity="0.85"/>')
    # node dots (on circle edge toward node)
    for i,(nx,ny) in enumerate(nodes_pos):
        a=math.atan2(ny-CY,nx-CX); ex=CX+84*math.cos(a); ey=CY+84*math.sin(a)
        parts.append(f'<circle class="mnd mnd{i}" cx="{ex:.0f}" cy="{ey:.0f}" r="6.5" fill="{DOT[i]}"/>')
    # node boxes
    for i,lab in enumerate(labels):
        nx,ny=nodes_pos[i]; x=nx-BW/2; y=ny-BH/2
        emo=emoji_for(lab); kws=themes[lab][:3]
        parts.append(f'<g class="mnd mnd{i}">')
        parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{BW}" height="{BH}" rx="20" fill="url(#ng{i})" filter="url(#mds)"/>')
        parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{BW}" height="{BH}" rx="20" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>')
        parts.append(f'<text x="{nx:.0f}" y="{y+27:.0f}" text-anchor="middle" font-size="20">{emo}</text>')
        parts.append(f'<text x="{nx:.0f}" y="{y+49:.0f}" text-anchor="middle" font-family="Noto Sans KR,sans-serif" font-weight="900" font-size="16" fill="white">{esc(lab)}</text>')
        for j,kw in enumerate(kws):
            t=kw if len(kw)<=11 else kw[:10]+'…'
            parts.append(f'<text x="{nx:.0f}" y="{y+68+j*16:.0f}" text-anchor="middle" font-family="Noto Sans KR,sans-serif" font-weight="600" font-size="10.5" fill="rgba(255,255,255,0.92)">{esc(t)}</text>')
        parts.append('</g>')
    # center
    parts.append('<g class="mct">')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="84" fill="url(#cg)" filter="url(#mds2)"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="84" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="4.5"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="73" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1.5"/>')
    parts.append(f'<text x="{CX}" y="{CY-18}" text-anchor="middle" font-size="30">💝</text>')
    parts.append(f'<text x="{CX}" y="{CY+10}" text-anchor="middle" font-family="Noto Sans KR,sans-serif" font-weight="900" font-size="19" fill="white">우리</text>')
    parts.append(f'<text x="{CX}" y="{CY+34}" text-anchor="middle" font-family="Noto Sans KR,sans-serif" font-weight="900" font-size="19" fill="white">선생님께</text>')
    parts.append('</g>')
    parts.append('</svg>')
    return ''.join(parts)
