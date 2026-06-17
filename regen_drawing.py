# -*- coding: utf-8 -*-
"""각 반 학생 그림을 Gemini 비전으로 실제 분석해 analysis/{c}_analysis.json 의 drawing_bullets 갱신"""
import sys, io, os, re, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
load_dotenv()

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

def thumb(path, maxpx=420, q=72):
    im=Image.open(path)
    if im.mode in ('RGBA','P','LA'): im=im.convert('RGB')
    w,h=im.size; s=min(maxpx/max(w,h),1.0)
    if s<1.0: im=im.resize((int(w*s),int(h*s)))
    b=io.BytesIO(); im.save(b,format='JPEG',quality=q); return b.getvalue()

PROMPT="""첨부된 이미지들은 한 학급 학생들이 '선생님'을 그린 그림 작품 모음입니다.
이 그림들을 실제로 관찰하여, 이 학급 그림들에서 공통적으로 나타나는 특징을 한국어로 분석해주세요.
표정, 헤어스타일/외모 표현, 배경(교실·칠판·하트·꽃 등), 색채, 구도, 함께 등장하는 인물/사물, 글귀, 화풍 등 실제로 보이는 요소를 근거로 작성하세요.
- 항목 4~6개, 각 항목은 한 문장(존댓말, 25자 내외)
- 이 학급 그림에서 실제로 두드러지는 점 위주로 (일반론 금지)
- 핵심 키워드 1개를 **별표**로 감싸기 (예: **밝은 표정**)
JSON만 출력: {"bullets":["...","..."]}"""

def regen(cls):
    imgs=sorted(glob.glob(f'docs/images/{cls}/student-*.*'))
    if not imgs: print(cls,'no images'); return
    parts=[PROMPT]+[types.Part.from_bytes(data=thumb(p), mime_type='image/jpeg') for p in imgs]
    txt=client.models.generate_content(model="gemini-2.5-flash", contents=parts).text.strip()
    data=json.loads(re.search(r'\{.*\}', txt, re.DOTALL).group())
    bullets=[b.strip() for b in data['bullets'] if b.strip()][:6]
    p=f'analysis/{cls}_analysis.json'
    a=json.load(open(p,encoding='utf-8')); a['drawing_bullets']=bullets
    json.dump(a, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'{cls} ({len(imgs)}장) -> {len(bullets)}개')
    for b in bullets: print('    -',b)

if __name__=='__main__':
    for c in (sys.argv[1:] or ['1-1','1-2','1-3','1-5','1-6','1-7','1-8']):
        try: regen(c)
        except Exception as e: print(f'{c} ERROR: {e}')
