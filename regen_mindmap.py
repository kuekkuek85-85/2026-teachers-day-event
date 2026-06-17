# -*- coding: utf-8 -*-
"""각 반 편지에서 '마음의 결' 5개 주제를 새로 도출해 analysis/{c}_analysis.json 의 mindmap만 갱신"""
import sys, io, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from dotenv import load_dotenv
from google import genai
load_dotenv()

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
def ask(p):
    return client.models.generate_content(model="gemini-2.5-flash", contents=p).text.strip()

def letters_of(cls):
    wb=openpyxl.load_workbook(f'data/{cls}.xlsx',read_only=True,data_only=True); ws=wb.active
    rows=list(ws.iter_rows(values_only=True))
    out=[]
    for r in rows[1:]:
        if r and r[1] and r[6]:
            out.append(f"- {str(r[1]).strip()}: {str(r[6]).strip()}")
    return "\n".join(out)

PROMPT="""다음은 한 학급 학생들이 담임/교과 선생님께 쓴 감사 편지 모음입니다.
이 편지들에서 실제로 두드러지는 '마음의 결'을 대표하는 핵심 주제 5개를 뽑아주세요.

규칙:
- 각 주제 라벨(label)은 한국어 명사형 3~4글자 (예: 감사함, 존경심, 그리움, 미안함, 응원함, 행복감, 신뢰감, 유대감, 기대감, 성장의지)
- 5개 주제는 서로 겹치지 않게, 이 학급 편지의 실제 내용을 반영해 선택
- 각 주제마다 "왜 그렇게 느꼈는지" 근거를 보여주는 짧은 키워드(keywords) 3개를 편지 내용에서 요약
  · 각 키워드는 4~9글자의 짧은 구절 (예: "잘 가르쳐 주심", "늘 챙겨주심", "이별이 아쉬움", "더 함께하고파")
  · 완전한 문장 금지, 핵심만
- JSON만 출력: {"themes":[{"label":"감사함","keywords":["키워드1","키워드2","키워드3"]}, ... 정확히 5개]}

편지:
%s"""

def regen(cls):
    letters=letters_of(cls)
    txt=ask(PROMPT % letters[:3000])
    data=json.loads(re.search(r'\{.*\}', txt, re.DOTALL).group())
    themes=data['themes'][:5]
    mm={}
    for t in themes:
        lab=t['label'].strip()
        kws=[k.strip() for k in t.get('keywords', t.get('quotes',[])) if k.strip()][:3]
        mm[lab]=kws
    assert len(mm)==5, f'{cls}: {len(mm)} themes'
    p=f'analysis/{cls}_analysis.json'
    a=json.load(open(p,encoding='utf-8'))
    a['mindmap']=mm
    json.dump(a, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'{cls} ->', list(mm.keys()))

if __name__=='__main__':
    for c in (sys.argv[1:] or ['1-1','1-2','1-3','1-5','1-6','1-7','1-8']):
        try: regen(c)
        except Exception as e: print(f'{c} ERROR: {e}')
