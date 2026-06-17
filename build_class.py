# -*- coding: utf-8 -*-
"""1-1.html(애니메이션 템플릿)에 1-2 데이터를 주입해 docs/1-2.html 생성"""
import sys, io, re, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

import os, shutil, yaml

CLASS=sys.argv[1] if len(sys.argv)>1 else '1-2'
cfg=yaml.safe_load(open('config.yaml',encoding='utf-8'))
SCHOOL=cfg.get('school','장평중학교')
cc=cfg['classes'][CLASS]
TEACHER=cc['teacher']; SUBJECT=cc['subject']; ACR=cc['acrostic_chars']
assert TEACHER and len(ACR)==3, f'{CLASS} config 미완성: teacher/acrostic 확인'
print(f'>>> Building {CLASS} | {TEACHER} 선생님 | {SUBJECT} | {"·".join(ACR)}')

# ---- load students ----
wb=openpyxl.load_workbook(f'data/{CLASS}.xlsx',read_only=True,data_only=True); ws=wb.active
rows=list(ws.iter_rows(values_only=True))
students=[]
for r in rows[1:]:
    if not r or not r[1]: continue
    students.append({'id':int(r[0]),'name':str(r[1]).strip(),
        'a':[(r[2] or '').strip(),(r[3] or '').strip(),(r[4] or '').strip()],
        'ccl':(r[8] or '').strip()})
N=len(students)

A=json.load(open(f'analysis/{CLASS}_analysis.json',encoding='utf-8'))

# ---- map & copy images -> docs/images/{CLASS}/student-NN.ext ----
def _base(full):
    m=re.match(r'([가-힣A-Za-z]+)\s*\d{5}', full); return m.group(1) if m else full
def _kor(s):
    m=re.search(r'([가-힣]{2,4})\s*\d{5}', s); return m.group(1) if m else None
SRCDIR=f'images/{CLASS}'
allf=[f for f in os.listdir(SRCDIR) if not f.startswith('.') and os.path.isfile(os.path.join(SRCDIR,f))]
stu_by_name={_base(s['name']):s for s in students}
named={}; unnamed=[]
for f in allf:
    nm=_kor(f); sid=None
    if nm and nm in stu_by_name: sid=stu_by_name[nm]['id']
    else:
        for bn,s in stu_by_name.items():
            if bn in f: sid=s['id']; break
    if sid and sid not in named: named[sid]=f
    else: unnamed.append(f)
ordered=[(sid,named[sid]) for sid in sorted(named)]+[(None,f) for f in sorted(unnamed)]
destdir=f'docs/images/{CLASS}'; os.makedirs(destdir,exist_ok=True)
for f in os.listdir(destdir):
    if f.startswith('student-'): os.remove(os.path.join(destdir,f))
IMG=[]
for gi,(sid,sf) in enumerate(ordered,1):
    ext=os.path.splitext(sf)[1].lower().lstrip('.'); ext='jpg' if ext=='jpeg' else ext
    shutil.copy(os.path.join(SRCDIR,sf), os.path.join(destdir,f'student-{gi:02d}.{ext}'))
    IMG.append({'gi':gi,'sid':sid,'ext':ext})
print(f'    images: {len(IMG)} (named {len(named)}, unnamed {len(unnamed)})')

src=open('docs/1-1.html',encoding='utf-8').read()

def esc(s): return html.escape(s,quote=False)

# ================= 1. Firebase =================
src=src.replace("const CLASS_ID = '1-1';",f"const CLASS_ID = '{CLASS}';")
src=src.replace("const TEACHER_NAME = '이서영';",f"const TEACHER_NAME = '{TEACHER}';")

# ================= 2. Cover =================
src=src.replace("수신 : 이서영 선생님 💛",f"수신 : {TEACHER} 선생님 💛")
src=src.replace("장평중학교 1학년 1-1반 · 마음에는 유통기한이 없습니다 💝",
                f"{SCHOOL} 1학년 {CLASS}반 · 마음에는 유통기한이 없습니다 💝")

# ================= 3. Prologue =================
src=src.replace('23<span style="font-size:22px;">명</span>',
                f'{N}<span style="font-size:22px;">명</span>')
src=src.replace('letter-spacing:1px;white-space:nowrap;">이 · 서 · 영</div>',
                f'letter-spacing:1px;white-space:nowrap;">{ACR[0]} · {ACR[1]} · {ACR[2]}</div>')
# prologue subject card (국어 -> 음악) : the 48px purple? no, 국어 is 00A5BC card3
src=src.replace('color:#00A5BC;line-height:1;margin-top:10px;">국어</div>',
                f'color:#00A5BC;line-height:1;margin-top:10px;">{SUBJECT}</div>')

# ================= 4. Samhangsi (scenes 2-5) =================
COLORS=[{'b':'#FF6B9D','a':'#C2185B','bg':'#FFE7F0','sh':'rgba(194,24,91,.1)'},
        {'b':'#7B1FA2','a':'#7B1FA2','bg':'#F1E4F8','sh':'rgba(123,31,162,.1)'},
        {'b':'#00BCD4','a':'#00A5BC','bg':'#D9F4F8','sh':'rgba(0,188,212,.12)'},
        {'b':'#FF7043','a':'#E8531F','bg':'#FFE6DA','sh':'rgba(255,112,67,.12)'},
        {'b':'#43A047','a':'#388E3C','bg':'#E8F5E9','sh':'rgba(67,160,71,.12)'},
        {'b':'#1976D2','a':'#1565C0','bg':'#E3F2FD','sh':'rgba(25,118,210,.12)'}]
def card(stu,cidx,delay):
    c=COLORS[cidx%6]
    return (f'          <div style="background:#fff;border-radius:18px;padding:16px 15px;'
            f'box-shadow:0 10px 24px {c["sh"]};border-top:5px solid {c["b"]};'
            f'animation:fadeUp .55s {delay}s both;overflow:hidden;">\n'
            f'            <div style="font-size:13px;font-weight:800;color:{c["a"]};'
            f'background:{c["bg"]};display:inline-block;padding:3px 11px;border-radius:999px;'
            f'margin-bottom:10px;">학생 {stu["id"]}</div>\n'
            f'            <div style="font-size:13px;line-height:1.75;color:#3A2230;">'
            f'<b style="color:{c["a"]}">{ACR[0]}!</b> {esc(stu["a"][0])}<br>'
            f'<b style="color:{c["a"]}">{ACR[1]}!</b> {esc(stu["a"][1])}<br>'
            f'<b style="color:{c["a"]}">{ACR[2]}!</b> {esc(stu["a"][2])}</div>\n'
            f'          </div>')

# AI block (slide 4) using story with 김/상/은 highlights
def hl(text):
    # 맨 앞의 '성함'(예: 김상은) 호칭은 그대로 두고, 문장 속에 엮인 각 성함 글자를 1회씩 하이라이팅
    EM='<em style="background:rgba(255,255,255,.28);padding:1px 6px;border-radius:5px;font-style:normal;font-weight:800;">{}</em>'
    start=text.find(TEACHER)
    skip=(start+len(TEACHER)) if start>=0 else 0
    BD=' .,!?\n\t·'
    pos=[]
    for ch in ACR:
        # 단어 시작(공백·문장부호 뒤) 위치를 우선, 없으면 첫 등장
        idx=-1; i=skip
        while True:
            j=text.find(ch,i)
            if j<0: break
            if j==0 or text[j-1] in BD: idx=j; break
            i=j+1
        if idx<0: idx=text.find(ch, skip)
        if idx>=0: pos.append((idx,ch))
    pos.sort()
    res=[]; last=0
    for idx,ch in pos:
        res.append(esc(text[last:idx])); res.append(EM.format(ch)); last=idx+1
    res.append(esc(text[last:]))
    return ''.join(res)
AI_BLOCK=('\n        <div style="margin-top:16px;background:linear-gradient(135deg,#C2185B,#7B1FA2);'
    'border-radius:18px;padding:18px 24px;color:#fff;box-shadow:0 14px 36px rgba(123,31,162,.28);'
    'animation:fadeUp .6s 1s both;">\n'
    f'          <div style="font-size:14px;font-weight:800;opacity:.92;margin-bottom:6px;">🤖 AI가 {N}명의 삼행시를 하나로 연결했습니다</div>\n'
    '          <div style="font-size:14.5px;line-height:1.7;font-weight:500;">'
    + hl(A['story']) + '</div>\n        </div>')

def scene(idx, badge, sub, slc, ai=False):
    cards='\n'.join(card(s,i,round(0.35+i*0.1,2)) for i,s in enumerate(slc))
    letter=chr(65+idx)
    return (f'      <!-- ══ SCENE 3{letter} — ACROSTIC {idx+1}/4 ══ -->\n'
        f'      <sc-if value="{{{{ isScene{2+idx} }}}}">\n'
        f'      <div style="position:absolute;inset:0;display:flex;flex-direction:column;'
        f'padding:46px 60px 36px;background:linear-gradient(160deg,#FFF6FA,#F7E9F5);overflow:hidden;">\n'
        f'        <div style="display:flex;align-items:center;gap:12px;animation:slideL .6s both;">\n'
        f'          <div style="background:#C2185B;color:#fff;font-weight:800;font-size:17px;'
        f'padding:8px 18px;border-radius:999px;">📬 #1. 마음을 잇는 삼행시</div>\n'
        f'          <div style="font-size:14px;color:#9B5B73;font-weight:600;">{badge}</div>\n'
        f'        </div>\n'
        f'        <div style="font-size:38px;font-weight:900;color:#2A1622;letter-spacing:-1px;'
        f'margin-top:10px;animation:fadeUp .6s .1s both;">소포 안에 편지가 들어 있었습니다</div>\n'
        f'        <div style="font-size:16px;color:#9B5B73;font-weight:600;margin-top:4px;'
        f'animation:fadeUp .6s .2s both;">{sub} · 기준 글자 : <strong style="color:#C2185B;">'
        f'{ACR[0]} · {ACR[1]} · {ACR[2]}</strong></div>\n\n'
        f'        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'
        f'margin-top:16px;flex:1;">\n{cards}\n        </div>{AI_BLOCK if ai else ""}\n'
        f'      </div>\n      </sc-if>\n')

# distribute N students into 4 slides
import math
sizes=[]
base=N//4; extra=N%4
for i in range(4): sizes.append(base+(1 if i<extra else 0))
# build page slices
slices=[]; start=0
for sz in sizes:
    slices.append(students[start:start+sz]); start+=sz
PAGE_META=[]
s=0
for i,sl in enumerate(slices):
    lo=sl[0]['id']; hi=sl[-1]['id']
    PAGE_META.append((f'{["①","②","③","④"][i]} {lo}~{hi}번', f'학생 {lo}~{hi}/{N}명'))
new_acrostic='\n'.join(scene(i,PAGE_META[i][0],PAGE_META[i][1],slices[i], ai=(i==3)) for i in range(4))

# replace samhangsi block (isScene2 .. before isScene6)
m=re.search(r'      <!-- ══ SCENE 3A.*?isScene2 \}\}".*?', src, re.DOTALL)
a=src.index('<!-- ══ SCENE 3A')
a=src.rfind('\n',0,a)+1
b=src.index('<!-- ══ SCENE 4 — WORDCLOUD ══ -->')
b=src.rfind('\n',0,b)+1
src=src[:a]+new_acrostic+'\n'+src[b:]
print('samhangsi sizes', sizes)

# ================= 5. Ability tags =================
ABIL_BG={'공감':'#FFF6DC','관계':'#DCF5F9','정서':'#E2F5E3','매력':'#F3E4F8'}
ABIL_TC={'공감':'#A87A06','관계':'#0B7C8C','정서':'#2E7D32','매력':'#7B1FA2'}
def tag_spans(cat):
    bg=ABIL_BG[cat]; tc=ABIL_TC[cat]
    return ''.join(f'<span style="background:{bg};color:{tc};font-weight:700;font-size:14px;padding:7px 14px;border-radius:999px;">{esc(t)}</span>' for t in A['abilities'][cat])
for cat in ['공감','관계','정서','매력']:
    bg=ABIL_BG[cat]
    pat=re.compile(r'(?:<span style="background:'+re.escape(bg)+r';[^>]*>[^<]*</span>)+')
    src,n=pat.subn(tag_spans(cat), src, count=1)
    if n!=1: print('WARN ability', cat, n)

# ================= 6. Influence titles/descs =================
def trim(t, lim=120):
    t=t.strip()
    if len(t)<=lim: return t
    cut=t[:lim]
    p=max(cut.rfind('. '),cut.rfind('! '),cut.rfind('? '),cut.rfind('다 '))
    if p>40: return cut[:p+1]
    return cut.rstrip()+'…'
# titles (2nd span in each influence card)
inf_titles=[esc(i['title']) for i in A['influences']]
ti=[0]
def rep_title(m):
    t=inf_titles[ti[0]]; ti[0]+=1; return m.group(1)+t+m.group(3)
src=re.sub(r'(<span style="font-size:19px;font-weight:900;color:#2A1622;">)(.*?)(</span>)', rep_title, src, count=4)
inf_descs=[esc(trim(i['desc'])) for i in A['influences']]
di=[0]
def rep_desc(m):
    t=inf_descs[di[0]]; di[0]+=1; return m.group(1)+t+m.group(3)
src=re.sub(r'(<div style="font-size:14px;line-height:1.7;color:#5C4452;margin-top:10px;">)(.*?)(</div>)', rep_desc, src, count=4)

# ability subtitle teacher name
src=src.replace('이서영 선생님이 가진 4가지 매력 카테고리', f'{TEACHER} 선생님이 가진 4가지 매력 카테고리')
# influence bottom quote -> 1-2 quote
inf_quote=esc(trim(A['quote'],120))
src=re.sub(r'(margin-top:18px;background:#FFEAF2;[^>]*>)💬 .*?(</div>)',
           r'\g<1>💬 "'+inf_quote+r'"\g<2>', src, count=1, flags=re.DOTALL)

# ================= 6b. Wordcloud (반별 키워드) =================
WC_SLOTS=[(0,-6,68,900,'#FF6B9D','.35'),(198,-58,50,900,'#4DD0E1','.5'),(-200,-72,46,900,'#FFD54F','.45'),
 (268,54,42,900,'#FF8A65','.6'),(-300,36,40,900,'#CE93D8','.55'),(86,-128,40,900,'#FFAB91','.9'),
 (120,104,38,800,'#80DEEA','.7'),(-128,96,36,800,'#F48FB1','.65'),(-70,-120,36,800,'#B39DDB','.85'),
 (360,-30,34,800,'#F8BBD0','.8'),(-30,150,34,800,'#F06292','1.05'),(-372,-44,32,800,'#FFCC80','.75'),
 (236,138,32,800,'#4DB6AC','1'),(-250,130,30,700,'#9FA8DA','.95'),(34,-178,30,700,'#FFD54F','1.1'),
 (408,104,30,800,'#4DD0E1','1.2'),(-420,78,28,700,'#CE93D8','1.15')]
def _wcap(n): return {0:999,1:999,2:999,3:58,4:44,5:36,6:30}.get(n,26)
wc=sorted(A.get('wordcloud',[]), key=lambda w:(-int(w.get('size',1)), len(w['word'])))[:len(WC_SLOTS)]
if wc:
    wdivs=[]
    for (tx,ty,fs,w,col,d),wd in zip(WC_SLOTS,wc):
        word=wd['word'].strip(); f=min(fs,_wcap(len(word)))
        wdivs.append(f'          <div style="position:absolute;left:50%;top:50%;--tx:{tx}px;--ty:{ty}px;'
                     f'font-size:{f}px;font-weight:{w};color:{col};animation:explode .7s {d}s both;">{esc(word)}</div>')
    src=re.sub(r'(<div style="position:relative;flex:1;margin-top:4px;">)(.*?)(\n        </div>)',
               lambda m: m.group(1)+'\n'+'\n'.join(wdivs)+m.group(3), src, count=1, flags=re.DOTALL)

# ================= 6c. Mindmap (반별 '마음의 결' 5개 + 근거 키워드) =================
from make_mindmap import build_svg as _mm_svg
_mm=A.get('mindmap',{})
if len(_mm)>=5:
    src=re.sub(r'(<div style="position:relative;flex:1;margin-top:6px;">\s*)<svg.*?</svg>',
               lambda m: m.group(1)+_mm_svg(_mm), src, count=1, flags=re.DOTALL)

# ================= 6d. Drawing analysis (반별 비전 분석, 가변 개수) =================
DRAWC=[('rgba(194,24,91,.1)','#FF6B9D','#C2185B','#C2185B'),('rgba(123,31,162,.1)','#CE93D8','#7B1FA2','#7B1FA2'),
 ('rgba(0,188,212,.12)','#4DD0E1','#00A5BC','#00A5BC'),('rgba(255,112,67,.12)','#FFB74D','#FF7043','#FF7043'),
 ('rgba(102,187,106,.12)','#81C784','#43A047','#43A047'),('rgba(194,24,91,.1)','#F06292','#C2185B','#C2185B')]
def _dfmt(text,bc):
    return ''.join((f'<b style="color:{bc};">{esc(p)}</b>' if i%2 else esc(p)) for i,p in enumerate(re.split(r'\*\*(.+?)\*\*', text)))
db=A.get('drawing_bullets',[])
if db:
    cols=2 if len(db)==4 else 3
    dcards=[]
    for i,b in enumerate(db):
        sh,c1,c2,bc=DRAWC[i%6]; delay=round(0.35+0.15*i,2)
        dcards.append(f'          <div style="position:relative;background:#fff;border-radius:18px;padding:22px 20px 22px 64px;'
            f'box-shadow:0 12px 28px {sh};font-size:16px;line-height:1.55;color:#3A2230;font-weight:500;animation:popIn .5s {delay}s both;">'
            f'<span style="position:absolute;left:18px;top:20px;width:32px;height:32px;border-radius:50%;'
            f'background:linear-gradient(135deg,{c1},{c2});color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;">{i+1}</span>'
            f'{_dfmt(b,bc)}</div>')
    dgrid=f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:18px;margin-top:auto;margin-bottom:auto;">\n'+'\n'.join(dcards)+'\n        </div>'
    src=re.sub(r'<div style="display:grid;grid-template-columns:repeat\(3,1fr\);gap:18px;margin-top:auto;margin-bottom:auto;">.*?</div>(\s*</div>\s*</sc-if>)',
               dgrid+r'\1', src, count=1, flags=re.DOTALL)

# ================= 7. Gallery (scenes 11-14) =================
GAL_DELAYS=['0.3','0.4','0.5','0.6','0.7']
def gcard(gi, ext, delay):
    return ('<div style="background:#fff;border-radius:14px;overflow:hidden;'
            'box-shadow:0 10px 24px rgba(123,31,162,.14);display:flex;flex-direction:column;min-height:0;'
            f'animation:flipIn .5s {delay}s both;">'
            '<div style="flex:1;min-height:0;overflow:hidden;">'
            f'<img src="images/{CLASS}/student-{gi:02d}.{ext}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="학생 작품">'
            '</div>'
            '<div style="flex-shrink:0;font-size:12px;font-weight:700;color:#9B5B73;text-align:center;padding:6px;background:#fff;">'
            f'학생 {gi}</div></div>')
ext_by_gi={d['gi']:d['ext'] for d in IMG}
NIMG=len(IMG)
# distribute NIMG images into gallery slides of max 5, balanced
NGAL=(NIMG+4)//5
gsizes=[NIMG//NGAL+(1 if i<NIMG%NGAL else 0) for i in range(NGAL)]
CIRC=['①','②','③','④','⑤','⑥','⑦','⑧']
FIRST_GAL=11
EPI=FIRST_GAL+NGAL      # epilogue scene index
CCL_=EPI+1              # ccl scene index
def gscene(sc, badge_i, gis):
    cards='\n          '.join(gcard(gi, ext_by_gi[gi], GAL_DELAYS[i%5]) for i,gi in enumerate(gis))
    lo,hi=gis[0],gis[-1]
    return (f'      <sc-if value="{{{{ isScene{sc} }}}}">\n'
        f'      <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:46px 60px 64px;background:linear-gradient(160deg,#FFF6FA,#FBEAF6);overflow:hidden;">\n'
        f'        <div style="align-self:flex-start;background:#7B1FA2;color:#fff;font-weight:800;font-size:17px;padding:8px 18px;border-radius:999px;animation:slideL .6s both;">🖼️ #5. 그리기 갤러리 {CIRC[badge_i]}</div>\n'
        f'        <div style="font-size:40px;font-weight:900;color:#2A1622;letter-spacing:-1px;margin-top:12px;animation:fadeUp .6s .1s both;">우리가 그린 선생님</div>\n'
        f'        <div style="font-size:17px;color:#9B5B73;font-weight:600;margin-top:5px;animation:fadeUp .6s .2s both;">익명으로 전시된 작품 {CIRC[badge_i]} · 학생 {lo}~{hi}</div>\n'
        f'        <div style="display:grid;grid-template-columns:repeat(5,1fr);grid-auto-rows:minmax(0,1fr);gap:14px;flex:1;min-height:0;margin-top:20px;">\n          {cards}\n        </div>\n'
        f'      </div>\n      </sc-if>')
# build gi ranges per slide
gal_blocks=[]; start=1
for bi,sz in enumerate(gsizes):
    gis=list(range(start,start+sz)); start+=sz
    gal_blocks.append('      <!-- GALLERY '+str(FIRST_GAL+bi)+' -->\n'+gscene(FIRST_GAL+bi, bi, gis))
gal_all='\n\n      <!-- ══ GALLERY ══ -->\n'+'\n'.join(gal_blocks)+'\n'

# --- renumber epilogue/CCL if gallery count != 4 (template has epi=15, ccl=16) ---
if EPI!=15:
    # shift high->low to avoid collision
    src=src.replace('{{ isScene16 }}', f'{{{{ isScene{CCL_} }}}}')
    src=src.replace('{{ isScene15 }}', f'{{{{ isScene{EPI} }}}}')
    # extend durs array: insert gallery-duration entries so length == CCL_+1
    m=re.search(r'durs = \[([^\]]*)\];', src)
    vals=[v.strip() for v in m.group(1).split(',')]
    need=(CCL_+1)-len(vals)
    if need>0:
        vals[15:15]=['11']*need   # insert extra gallery durations after the 4 base galleries
    src=src.replace(m.group(0), 'durs = ['+', '.join(vals)+'];')

# replace whole gallery block (first gallery sc-if .. last before epilogue)
ga=src.index('<sc-if value="{{ isScene11 }}">'); ga=src.rfind('\n',0,ga)+1
gb=src.index('SCENE 15 — EPILOGUE'); gb=src.rfind('<!--',0,gb); gb=src.rfind('\n',0,gb)+1
src=src[:ga]+gal_all+'\n'+src[gb:]

# ================= 8. Epilogue =================
src=src.replace('1학년 1반이 이서영 선생님을 위해',f'1학년 {CLASS.split("-")[1]}반이 {TEACHER} 선생님을 위해')
src=src.replace('To. 사랑하는 우리 1-1반 친구들 ♡',f'To. 사랑하는 우리 {CLASS}반 친구들 ♡')
src=src.replace('From. 이서영 선생님 💛',f'From. {TEACHER} 선생님 💛')

# ================= 9. CCL =================
from collections import Counter
def norm_ccl(s):
    return s.replace('변경금리','변경금지')
ccl_counts=Counter(norm_ccl(s['ccl']) for s in students if s['ccl'])
total=sum(ccl_counts.values())
ordered=ccl_counts.most_common()
BAR_COLORS=[('#FF4500','#FF7043'),('#FF1493','#FF6B9D'),('#7B1FA2','#AB47BC'),('#0288D1','#00BCD4'),('#2E7D32','#66BB6A')]
PCT_COLORS=['#FF4500','#FF1493','#7B1FA2','#0288D1','#2E7D32']
bars=[]
for i,(lic,cnt) in enumerate(ordered):
    pct=round(cnt/total*100)
    c1,c2=BAR_COLORS[i%5]; pc=PCT_COLORS[i%5]; delay=round(0.5+i*0.15,2)
    bars.append(
      '              <div>\n'
      f'                <div style="display:flex;justify-content:space-between;font-size:14px;font-weight:700;color:#3A2230;margin-bottom:5px;"><span>{esc(lic)}</span><span style="color:{pc};">{cnt}명 · {pct}%</span></div>\n'
      f'                <div style="height:22px;background:#F3E4EC;border-radius:11px;overflow:hidden;"><div style="height:100%;width:{pct}%;--bw:{pct}%;background:linear-gradient(90deg,{c1},{c2});border-radius:11px;animation:barGrow 1s {delay}s both;"></div></div>\n'
      '              </div>')
bars_html='\n'.join(bars)
# replace the bars container (between the gap:16px flex column div and its close)
cb_start=src.index('<div style="display:flex;flex-direction:column;gap:16px;flex:1;justify-content:center;">')
cb_a=src.index('>',cb_start)+1
# find matching close: the bars are followed by '\n            </div>\n          </div>' (end of left panel inner)
cb_b=src.index('\n            </div>\n          </div>', cb_a)
src=src[:cb_a]+'\n'+bars_html+'\n            '+src[cb_b+1:]
# header counts & source
src=src.replace('출처 : 장평중학교 1-1반 (2026)',f'출처 : {SCHOOL} {CLASS}반 (2026)')
src=src.replace('CCL 선택 현황<span style="color:#9B5B73;font-weight:600;font-size:14px;">(총 23명)',
                f'CCL 선택 현황<span style="color:#9B5B73;font-weight:600;font-size:14px;">(총 {N}명)')
# AI ccl analysis block text
ccl_ai=esc(trim(A['ccl_analysis'],160))
src=re.sub(r'(<div style="font-size:14\.5px;line-height:1\.7;margin-top:10px;font-weight:500;">).*?(</div>)',
           r'\g<1> '+ccl_ai+r'\g<2>', src, count=1, flags=re.DOTALL)
# applied license chips
uniq_lics=[lic for lic,_ in ordered]
chip='\n                '.join(f'<span style="background:#F3E4F8;color:#7B1FA2;font-weight:700;font-size:12.5px;padding:6px 12px;border-radius:999px;border:1px solid #E1C9ED;">{esc(l)}</span>' for l in uniq_lics)
src=re.sub(r'(<div style="display:flex;flex-wrap:wrap;gap:7px;">)\s*.*?(\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</sc-if>)',
           r'\g<1>\n                '+chip+r'\g<2>', src, count=1, flags=re.DOTALL)

open(f'docs/{CLASS}.html','w',encoding='utf-8').write(src)
print(f'    docs/{CLASS}.html done. div', src.count('<div'),'/',src.count('</div>'),
      '| sc-if', src.count('<sc-if'),'/',src.count('</sc-if>'),'| students',N,'| galleries',NGAL)
print('    CCL:', dict(ccl_counts), 'total', total)
