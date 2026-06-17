import re, sys

with open(r'C:\claude_code_project\2026_스승의날_이벤트\docs\우리반 마음 소포.dc.html', encoding='utf-8') as f:
    src = f.read()

COLORS = [
    {'border':'#FF6B9D','acc':'#C2185B','bg':'#FFE7F0','shadow':'rgba(194,24,91,.1)'},
    {'border':'#7B1FA2','acc':'#7B1FA2','bg':'#F1E4F8','shadow':'rgba(123,31,162,.1)'},
    {'border':'#00BCD4','acc':'#00A5BC','bg':'#D9F4F8','shadow':'rgba(0,188,212,.12)'},
    {'border':'#FF7043','acc':'#E8531F','bg':'#FFE6DA','shadow':'rgba(255,112,67,.12)'},
    {'border':'#43A047','acc':'#388E3C','bg':'#E8F5E9','shadow':'rgba(67,160,71,.12)'},
    {'border':'#1976D2','acc':'#1565C0','bg':'#E3F2FD','shadow':'rgba(25,118,210,.12)'},
]

STUDENTS = [
    (1,'이롭고 항상 도움이 되어주시는 우리','서영쌤!!!','영원히 사랑할게요!!! 💗'),
    (2,'이렇게 좋은 선생님은 처음 봤어요','서로 웃으며 지낼 수 있게 해주셔서 감사해요','영원히 기억에 남을 선생님이에요'),
    (3,'이 세상에서 가장 착하고 예쁘고 존경스러운 분은','서영 선생님이다 선생님은 저의','영웅이다.'),
    (4,'이 세상에서 가장 착하고 아름다우신','서영 선생님','영원히 제 담임쌤 1위에요!!'),
    (5,'이서영 쌤은','서울 장평중에서','영원하다'),
    (6,'이렇게 이쁘시면','서영쌤','영원히 내꺼 해야해요!!!!'),
    (7,'이서영 선생님은','서로를 이해할 수 있도록 도와주는 선생님!','영원히 기억에 남을 좋은 선생님!'),
    (8,'이서영 선생님의 외모는','서울에서','영등이다'),
    (9,'이렇게 좋으신','서영쌤을','영원히 볼수없다니ㅠㅠ'),
    (10,'이서영쌤','서영쌤이 있어야','영원이 행복해요'),
    (11,'이서영선생님','서로 빛이나는','영원한 학생이 되겠습니다.'),
    (12,'이롭고','서로를 돕길 원하시는 이서영 선생님!','영원히 사랑합니다♡'),
    (13,'이서영 선생님! 선생님이 해주신 말에서','서로서로 날하자 라는 말이 기억에 남아요! 선생님이','영원히 제 기억에 남으실 것 같아요! 항상 건강하세요!'),
    (14,'이쁘신','서영쌤','영원히 함께 하고 싶어요ㅎ'),
    (15,'이서영 선생님','서영 선생님','영 선생님'),
    (16,'이 세상에서','서영쌤이 가장','영향적으로 좋습니다'),
    (17,'이렇게 예쁘신 선생님을 만나게 된 것은','서투르고 부족했던 저에게 인생 최고의 행운입니다','영원히 아니 죽을때까지 선생님을 기억하겠습니다!'),
    (18,'이서영 선생님','서영 선생님','영상 잘찍는 선생님'),
    (19,'이렇게 좋은 선생님을 만나','서툴었던 중학교의 첫 시작도 잘 해낼 수 있었어요.','영원히 감사한 마음을 기억하겠습니다.'),
    (20,'이제는 고백할수 있습니다','서영쌤 수업만 기다려진다는 것을','0순위인 우리 선생님!! 스승의날 축하드려요!'),
    (21,'이서영 쌤!','서영쌤은!','영어를 잘 하실꺼 같아요! 국어쌤이지만...ㅎ'),
    (22,'이만(2만)보다 더 사랑해요','서영쌤','영원히!'),
    (23,'이렇게 다정한 선생님은 역시!','서영쌤 이런 서영쌤을','영원히 기억할거예요'),
]

delays = [.35, .45, .55, .65, .75, .85]

def card(n, yi, seo, young, cidx, delay):
    c = COLORS[cidx % 6]
    return (
        f'          <div style="background:#fff;border-radius:18px;padding:16px 15px;'
        f'box-shadow:0 10px 24px {c["shadow"]};border-top:5px solid {c["border"]};'
        f'animation:fadeUp .55s {delay}s both;overflow:hidden;">\n'
        f'            <div style="font-size:13px;font-weight:800;color:{c["acc"]};'
        f'background:{c["bg"]};display:inline-block;padding:3px 11px;border-radius:999px;'
        f'margin-bottom:10px;">학생 {n}</div>\n'
        f'            <div style="font-size:13px;line-height:1.75;color:#3A2230;">'
        f'<b style="color:{c["acc"]}">이!</b> {yi}<br>'
        f'<b style="color:{c["acc"]}">서!</b> {seo}<br>'
        f'<b style="color:{c["acc"]}">영!</b> {young}</div>\n'
        f'          </div>'
    )

AI_BLOCK = (
    '\n        <div style="margin-top:16px;background:linear-gradient(135deg,#C2185B,#7B1FA2);'
    'border-radius:18px;padding:18px 24px;color:#fff;box-shadow:0 14px 36px rgba(123,31,162,.28);'
    'animation:fadeUp .6s 1s both;">\n'
    '          <div style="font-size:14px;font-weight:800;opacity:.92;margin-bottom:6px;">'
    '🤖 AI가 23명의 삼행시를 하나로 연결했습니다</div>\n'
    '          <div style="font-size:15px;line-height:1.7;font-weight:500;">'
    '선생님, 저희 마음을 담은 <em style="background:rgba(255,255,255,.28);padding:1px 6px;'
    'border-radius:5px;font-style:normal;font-weight:800;">이</em> 편지가 도착하기까지 시간이 걸렸어요. '
    '이 세상에<em style="background:rgba(255,255,255,.28);padding:1px 6px;border-radius:5px;'
    'font-style:normal;font-weight:800;">서</em> 가장 착하고 예쁜 저희의 '
    '<em style="background:rgba(255,255,255,.28);padding:1px 6px;border-radius:5px;'
    'font-style:normal;font-weight:800;">영</em>웅, 영원히 사랑해요!</div>\n'
    '        </div>'
)

def scene(scene_idx, badge, subtitle, students_slice, show_ai=False):
    cards_html = '\n'.join(
        card(s[0], s[1], s[2], s[3], i, delays[i])
        for i, s in enumerate(students_slice)
    )
    ai = AI_BLOCK if show_ai else ''
    letter = chr(65 + scene_idx)
    return (
        f'      <!-- ══ SCENE 3{letter} — ACROSTIC {scene_idx+1}/4 ══ -->\n'
        f'      <sc-if value="{{{{ isScene{2+scene_idx} }}}}">\n'
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
        f'animation:fadeUp .6s .2s both;">{subtitle} · 기준 글자 : <strong style="color:#C2185B;">'
        f'이 · 서 · 영</strong></div>\n\n'
        f'        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'
        f'margin-top:16px;flex:1;">\n'
        f'{cards_html}\n'
        f'        </div>{ai}\n'
        f'      </div>\n'
        f'      </sc-if>\n'
    )

PAGES = [
    (0, '① 1~6번', '학생 1~6/23명', STUDENTS[0:6],  False),
    (1, '② 7~12번', '학생 7~12/23명', STUDENTS[6:12], False),
    (2, '③ 13~18번', '학생 13~18/23명', STUDENTS[12:18], False),
    (3, '④ 19~23번', '학생 19~23/23명', STUDENTS[18:23], True),
]
new_acrostic = '\n'.join(scene(pi, b, s, sl, ai) for pi, b, s, sl, ai in PAGES)

# Step 1: Renumber FIRST on original source (shift N>=3 by +3), reverse to avoid double-replace
for old_n in range(11, 2, -1):
    src = src.replace(
        '{{ isScene' + str(old_n) + ' }}',
        '{{ isScene' + str(old_n + 3) + ' }}'
    )

# Step 2: Replace old single acrostic scene (still isScene2 after renumbering)
old_scene = re.search(
    r'      <!-- ══ SCENE 3 — ACROSTIC ══ -->\n.*?      </sc-if>\n',
    src, re.DOTALL
)
if not old_scene:
    print('ERROR: Could not find old acrostic scene')
    sys.exit(1)

src = src[:old_scene.start()] + new_acrostic + src[old_scene.end():]

with open(r'C:\claude_code_project\2026_스승의날_이벤트\docs\우리반 마음 소포.dc.html', 'w', encoding='utf-8') as f:
    f.write(src)

count = src.count('<sc-if value=')
scenes = re.findall(r'isScene(\d+)', src)
max_scene = max(int(x) for x in scenes) if scenes else 0
print(f'Done. sc-if count={count}, max isScene index={max_scene}')
print('Scene indices found:', sorted(set(int(x) for x in scenes)))
