# 2026 스승의 날 — 우리반 마음 소포 📦

장평중학교 1학년 학생들이 선생님께 전하는 스승의 날 애니메이티드 카드뉴스 ("배송 지연 에디션").
학생들의 삼행시·감사 편지·그림 작품을 바탕으로 반별 페이지를 생성합니다.

## 구조

- `docs/` — 공개 사이트 (GitHub Pages)
  - `index.html` — 반 선택 허브
  - `1-1.html` ~ `1-8.html` — 반별 애니메이티드 카드뉴스
  - `images/{반}/` — 익명화된 학생 그림 (student-NN)
  - `support.js` — Claude Design 애니메이션 런타임
- 생성기 (Python)
  - `generate.py` — xlsx + Gemini 분석 → 정적 카드뉴스
  - `build_class.py <반>` — `docs/1-1.html` 템플릿에 반별 데이터를 주입해 애니메이티드 페이지 생성
  - `make_mindmap.py` — 편지 '마음의 결' 마인드맵 SVG 생성
  - `regen_mindmap.py` / `regen_drawing.py` — Gemini로 마인드맵 주제·그림 비전 분석 재생성
  - `fix_wordcloud.py` / `fix_drawing.py` / `fix_mindmap_svg.py` — 반별 콘텐츠 적용
- `config.yaml` — 반별 선생님·과목·삼행시 글자
- `templates/card_news.html.jinja2` — 정적 카드뉴스 템플릿

## 페이지 구성 (반별)

표지 · 프롤로그 · 삼행시 · 감정 워드클라우드 · 능력치 · 영향력 · 마인드맵 · 그림 분석 · 갤러리 · 에필로그 · CCL 저작권

## 개인정보

원본 학생 데이터(`data/`, `images/` 원본, `analysis/`)와 API 키(`.env`)는 저장소에서 제외됩니다.
공개되는 `docs/`는 학생을 "학생 N"으로 익명 처리합니다.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
