# 성향 서가 — 인수인계 문서

MBTI·관심 분야·최근 읽은 책으로 다음 책을 추천하고, 서점·출판사 이벤트를 한곳에 모아 보여주는 **단일 HTML 파일** 프로젝트입니다.
작성일 2026-10-07 · 산출물 `book-recommender.html` (약 99KB) · 이 문서 맨 아래(부록)에 전체 소스가 들어 있습니다.

> **2026-10-07 갱신 — 빌드 구조로 전환됨.** 아래 내용 중 "8장 3번(데이터 분리)"은 완료됐고, 6장의 도서는 74권 → **139권**으로 늘었습니다(최신 목록은 `data/books.txt`가 기준이며 이 문서의 6장 표와 부록 소스는 이전 판).
>
> ```
> data/books.txt      책 (제목|저자|출판사|KDC|분야|성향글자|키워드|설명, 한 줄 한 권)
> data/events.json    이벤트 + asOf(조사 기준일)
> src/template.html   화면·스크립트 템플릿 (placeholder: /*@BOOKS*/, /*@EVENTS*/, @@NS_BOOKS@@, @@NS_EVENTS@@, @@ASOF@@)
> build.py            위 셋 → book-recommender.html 생성 (python build.py, --check 로 검증만)
> ```
> - `data/guides.txt`: 전체 139권의 **읽기 가이드**(난이도·후기 반응 요약·이런 분께·주의점·근거·참고글). 카드의 접이식 항목으로 표시되며 스크립트판·정적판 모두 반영됩니다. 2026-10-07 책당 웹 검색 1회의 결과를 바탕으로 직접 요약했고(원문 복사 없음), 구체적 후기를 못 찾은 49권은 `근거=약함`으로 표시돼 카드에 "근거 약함 · 검수 필요"가 뜹니다(후기 기반 90권). 난이도·반응은 독자 후기 일부에서 읽은 경향이지 통계가 아니며, 참고글 링크가 해당 문장을 뒷받침하는지는 개별 확인하지 않았습니다. 빌드는 books.txt에 없는 제목, 난이도·근거 값 오류를 막습니다.
> - `data/bestsellers.json`: **주간 베스트셀러**(알라딘·예스24, 2026-10-07 확인). "주간 베스트" 탭과 정적판 섹션에 상위 30위를 보여주고, 서가에 있는 책(build.py가 제목으로 매칭, 현재 19권; 서가는 이번 주 베스트에 있던 12권을 추가해 151권이며 이 12권은 읽기 가이드가 아직 없음)에는 추천 점수 보너스를 줍니다. 보너스는 서점별로 10위 이내 +2, 30위 이내 +1.5, 그 밖 +1(두 서점에 있으면 합산, 최대 4). 성향·분야 점수(최대 10점대)보다 작은 보정이고, 집계일이 28일을 넘으면 스크립트판은 자동으로 점수 반영을 끈다(7일 넘으면 탭에 경고). 정적판은 빌드 시점 기준이며 CSS 정렬에 같은 비율(`--bb`)로 반영됩니다.
> - **주간 갱신 방법**: 서점 주간 순위를 확인해 `bestsellers.json`의 `asOf`, `period`, `items`([순위,제목,저자,출판사])를 바꾸고 `python build.py`. 매칭은 정규화한 제목이 같거나 서가 제목(6자 이상)이 순위 제목에 포함될 때입니다. 한계: 교보문고 순위는 읽지 못해 없고, 알라딘 36~50위와 수험서·만화 일부는 빠져 있으며, 자동 수집이 아니라 수동 갱신입니다.
> - 검증 중 발견·수정: 『무의식은 어떻게 나를 설계하는가』(이글먼의 책)를 믈로디노프 저서로 잘못 넣었던 것을 『새로운 무의식』으로 바로잡음. 같은 종류의 저자·제목 오류가 더 있을 수 있어 books.txt 전수 검수가 필요합니다.
> - `book-recommender.v30guides.bak.html`은 가이드 30권 시점의 백업입니다(필요 없으면 삭제).
> - 책·이벤트는 `data/`만 고치고 `python build.py` 한 번이면 스크립트판과 정적(.ns)판이 함께 갱신됩니다. `book-recommender.html`은 생성물이므로 직접 고치지 마세요.
> - 빌드 전환 시 기존 파일과 **바이트 단위로 동일**하게 재현되는 것을 확인했습니다. 이후 추가한 65권은 형식 검증(칸 수·KDC·분야·성향글자·중복)을 통과했습니다.
> - 추천 로직 변경: 같은 저자의 책은 상위 8권 안에 **최대 2권**까지만(스크립트판). 정적판은 CSS 정렬이라 미적용.
> - **추가 65권의 출판사·성향글자는 작성자의 기억과 휴리스틱입니다. 서점에서 검증하지 않았으니 검수가 필요합니다.**
> - 이벤트 asOf를 갱신하면 정적판은 그 날짜 기준으로 지난 이벤트가 빠집니다(스크립트판은 열 때마다 계산).

---

## 1. 요구 사항 (사용자가 요청한 순서)

1. 책 추천과 출판사 이벤트를 모아주는 HTML. MBTI 기반으로 인문·사회 등 성향(관심 분야)을 고르고, 최근 감명 깊게 읽은 책을 적으면 책을 추천.
2. 결과물은 HTML **파일**로 (아티팩트 링크가 아니라).
3. **임베디드 제작, API 사용 안 함.** 외부 호출 없이 파일 하나로 동작.
4. 아이폰 파일 앱에서 열었을 때 동작해야 함 (처음엔 동작 안 함 → 빈 화면 → 정적 우선 구조로 수정).
5. **MBTI를 바꾸면 추천 순서도 바뀌어야 함.**
6. 이후 코드(개발 환경)로 넘길 예정 → 이 문서.

## 2. 현재 상태 한눈에

| 항목 | 상태 |
|---|---|
| 단일 HTML, 외부 의존성 | 없음. 글꼴·스크립트·API 모두 내장/시스템. 책·이벤트 링크는 사용자가 누를 때만 이동 |
| 내장 도서 | 74권 (아래 6장) |
| 내장 이벤트 | 21건 (아래 7장, 2026-10-07 기준 고정) |
| 스크립트 실행 환경 | 전체 기능 (추천 8권, 최근 읽은 책·감상 반영, D-day) |
| 스크립트 미실행 환경 (아이폰 파일 앱 미리보기 등) | 간단 버전 (CSS만으로 분야 필터 + MBTI 순서 정렬 + 이벤트 필터) |
| 테스트 | 컴퓨터 Chromium(Playwright)에서만 검증. **iOS 실기기·WebKit은 미검증** |
| AI 호출 | 제거됨. (과거 버전에 Claude `sample` 호출 버튼이 있었으나 삭제) |

## 3. 화면·기능 명세

### 3.1 책 추천 (탭 1)
- 입력: MBTI 4축(E/I, S/N, T/F, J/P 토글), 관심 분야 12개 칩(복수 선택), 최근 감명 깊게 읽은 책(텍스트), 좋았던 점(텍스트, 선택).
- 분야 12개: 인문·철학, 사회·정치, 역사, 과학, 경제·경영, 심리, 자기계발, 한국소설, 해외소설, SF·장르, 에세이, 예술.
- 출력: 독자 유형 요약(NT/NF/ST/SF 4종) + 추천 도서 카드 8권. 카드에는 제목·저자·출판사·KDC 책등·한 줄 설명·추천 근거 태그·서점 검색 링크(교보/예스24/알라딘).
- 최근 읽은 책이 내장 서가에 있으면 그 책과 겹치는 키워드·분야를 가산, 없으면 상단 상태줄에 "서가에 없어 성향과 분야로 골랐어요" 표시.
- 입력값은 `localStorage`(`seonghyang`)에 저장 (try/catch, 실패해도 동작).

### 3.2 이벤트 모음 (탭 2)
- 알라딘·예스24·민음사 진행 이벤트 21건. 출처 칩으로 필터.
- 마감 임박 순 정렬, 마감 7일 이내는 경고색, 60일 초과/상시는 점선 도장.
- 마감일은 **페이지를 여는 시점의 날짜** 기준으로 계산하고 지난 이벤트는 자동 숨김.
- 하단에 교보문고·예스24·알라딘·민음사·리디 이벤트 페이지 바로가기.

## 4. 추천 알고리즘

### 4.1 데이터 모델 (한 권)
`제목|저자|출판사|KDC|분야(콤마)|성향글자|키워드(콤마)|한 줄 설명`

- **성향글자**는 그 책이 어울리는 MBTI 글자 집합(예: `NT`, `INF`, `NTJ`). **작성자(Claude)가 임의로 부여한 휴리스틱이며 과학적 근거가 있는 매핑이 아닙니다.** 코드로 넘길 때 별도 JSON/CSV로 빼서 사람이 검수·수정하기 쉽게 하는 것을 권장합니다.

### 4.2 스크립트 환경 점수 (`score()`)
```
총점 = 분야점수 + 성향점수 + 키워드점수 + (최근 읽은 책과 분야 공유 × 1.5)
분야점수 = 선택한 분야와 겹치면 3 + 겹친 개수, 아니면 0
성향점수 = (책 성향글자 중 내 MBTI와 같은 글자 수 × 3) − (책 성향글자 중 내 MBTI와 다른 글자 수 × 1.5)
키워드점수 = (최근 읽은 책 또는 '좋았던 점' 텍스트와 겹치는 키워드 수 × 2.5)
```
정렬: 총점 내림차순, 동점은 서가 입력 순서. 상위 8권 표시.

### 4.3 스크립트 없는 환경 (CSS 정렬)
- 라디오(MBTI)·체크박스(분야)를 `<input class="vh">` + `<label class="chip">` 조합으로 만들고, `.nsapp:has(#m-X:checked)`로 선택 상태를 CSS 변수(`--sE`…`--sP`, 선택=1)로 올립니다.
- 각 카드는 인라인으로 `--i`(서가 순번)와 보유 글자 `--hN:1` 등을 가집니다.
- `order: calc(10000 - 100 * Σ(--hL * (3 * --sL - 1)) + --i)` 로 정렬. 즉 **성향 일치 +2, 반대 −1** (스크립트 환경과 같은 비율).
- 분야는 정렬이 아니라 **필터**(선택한 분야가 하나도 없으면 전체 표시).
- 전체를 `@supports selector(:has(a))` 안에 넣어, `:has()`를 모르는 브라우저에서는 필터·정렬 없이 전체 목록이 그대로 보이게 했습니다.

## 5. HTML 구조와 설계 결정

- 문서 구조: `<html><head>(스타일)</head><body>` → `div#jsapp.wrap.jsapp`(스크립트용 전체 화면) → `div.wrap.ns`(스크립트 없는 간단 버전) → `<script>` → `</body></html>`.
- **정적 우선, 스크립트로 향상(progressive enhancement)**: 기본은 `.ns`(간단 버전)가 보이고 `.jsapp`은 `display:none`. 스크립트가 끝까지 성공하면 마지막 줄에서 `document.documentElement.classList.add("js")` → `.js .jsapp{display:block}`, `.js .ns{display:none}`.
- 이렇게 한 이유: 아이폰 파일 앱 미리보기는 HTML 안의 스크립트를 실행하지 않고, `<noscript>` 방식도 빈 화면이 됐음. 현재 구조는 컴퓨터에서 ① 스크립트 켬 ② 스크립트 끔 ③ `<script>` 태그를 통째로 지운 경우 세 가지 모두 내용이 보이는 것을 확인했습니다.
- 테마: 색은 전부 `:root` 토큰, `prefers-color-scheme: dark` 및 `data-theme` 대응(라이트/다크).
- 글꼴: 시스템 한글 글꼴만 사용 (Noto Serif KR → Nanum Myeongjo → AppleMyungjo → Batang / Apple SD Gothic Neo → Noto Sans KR → Malgun Gothic / 모노는 ui-monospace).
- 디자인 의도: "도서관 대출 카드" 컨셉. 마감일은 대출 반납 도장 모양(`.due`), 카드 왼쪽은 KDC(한국십진분류) 책등.
- 모바일 폭 400px 기준으로 가로 스크롤 없음 확인(컴퓨터 Chromium, 390px).

## 6. 내장 도서 데이터 (74권)

> 성향글자 = 4.1의 임의 휴리스틱. 출판사 표기는 작성자의 기억에 기반하며 서점에서 개별 검증하지 않았습니다(개정판·이관으로 출판사가 다를 수 있음).

| # | 제목 | 저자 | 출판사 | KDC | 분야 | 성향글자 | 키워드 | 한 줄 설명 |
|---|---|---|---|---|---|---|---|---|
| 1 | 사피엔스 | 유발 하라리 | 김영사 | 900 역사 | 역사, 인문·철학 | NT | 인류, 문명, 큰그림, 역사 | 인류사 전체를 하나의 이야기로 꿰는 거대한 설명 |
| 2 | 총 균 쇠 | 재레드 다이아몬드 | 문학사상 | 900 역사 | 역사, 과학 | NTJ | 문명, 지리, 인류, 역사 | 왜 어떤 문명이 앞서갔는지 환경과 지리로 답한다 |
| 3 | 정의란 무엇인가 | 마이클 샌델 | 와이즈베리 | 100 철학 | 인문·철학, 사회·정치 | EN | 정의, 토론, 윤리, 철학 | 사례마다 내 판단을 시험하게 하는 토론형 철학 |
| 4 | 공정하다는 착각 | 마이클 샌델 | 와이즈베리 | 300 사회과학 | 사회·정치, 인문·철학 | NF | 능력주의, 공정, 불평등, 사회 | 능력주의가 어떻게 사람을 갈라놓는지 짚는다 |
| 5 | 피로사회 | 한병철 | 문학과지성사 | 300 사회과학 | 인문·철학, 사회·정치 | IN | 피로, 성과, 현대사회, 철학 | 짧고 밀도 높은 현대인 진단서 |
| 6 | 미움받을 용기 | 기시미 이치로·고가 후미타케 | 인플루엔셜 | 100 철학 | 심리, 인문·철학 | F | 관계, 자유, 심리, 대화 | 대화체로 읽는 아들러 심리학 |
| 7 | 죽음의 수용소에서 | 빅터 프랭클 | 청아출판사 | 100 철학 | 심리, 인문·철학 | IF | 의미, 고통, 삶, 심리 | 극한 상황에서 붙잡은 삶의 의미 |
| 8 | 팩트풀니스 | 한스 로슬링 외 | 김영사 | 300 사회과학 | 사회·정치, 과학 | ST | 데이터, 통계, 세계, 편견 | 데이터로 세계를 다시 보는 법 |
| 9 | 넛지 | 리처드 탈러·캐스 선스타인 | 리더스북 | 300 사회과학 | 경제·경영, 심리 | T | 행동경제, 선택, 설계, 경제 | 사람의 선택을 설계하는 행동경제학 |
| 10 | 생각에 관한 생각 | 대니얼 카너먼 | 김영사 | 100 철학 | 심리, 과학 | INT | 인지, 편향, 사고, 심리 | 직관과 이성이 어떻게 엇갈리는지 실험으로 보여준다 |
| 11 | 이기적 유전자 | 리처드 도킨스 | 을유문화사 | 400 자연과학 | 과학 | INT | 진화, 유전자, 생물, 과학 | 진화를 유전자의 눈으로 다시 쓴 고전 |
| 12 | 코스모스 | 칼 세이건 | 사이언스북스 | 400 자연과학 | 과학 | NF | 우주, 과학, 경이, 인류 | 과학이 주는 경이를 문학처럼 전한다 |
| 13 | 물고기는 존재하지 않는다 | 룰루 밀러 | 곰출판 | 400 자연과학 | 과학, 에세이 | INF | 분류, 상실, 질서, 과학 | 과학 논픽션과 회고록이 겹쳐지는 책 |
| 14 | 열두 발자국 | 정재승 | 어크로스 | 400 자연과학 | 과학, 심리 | EN | 뇌, 선택, 창의, 과학 | 뇌과학으로 보는 선택과 창의성 |
| 15 | 도둑맞은 집중력 | 요한 하리 | 어크로스 | 300 사회과학 | 사회·정치, 심리 | NP | 집중, 기술, 현대사회, 심리 | 집중력 위기를 개인이 아닌 구조의 문제로 본다 |
| 16 | 침묵의 봄 | 레이첼 카슨 | 에코리브르 | 400 자연과학 | 과학, 사회·정치 | IFJ | 환경, 생태, 고발, 과학 | 환경운동의 출발점이 된 고발서 |
| 17 | 돈의 심리학 | 모건 하우절 | 인플루엔셜 | 300 사회과학 | 경제·경영 | SJ | 돈, 투자, 습관, 경제 | 숫자보다 태도로 다루는 돈 이야기 |
| 18 | 아주 작은 습관의 힘 | 제임스 클리어 | 비즈니스북스 | 300 사회과학 | 자기계발 | SJ | 습관, 실행, 루틴, 성장 | 작은 시스템으로 행동을 바꾸는 실전서 |
| 19 | 원씽 | 게리 켈러·제이 파파산 | 비즈니스북스 | 300 사회과학 | 자기계발, 경제·경영 | TJ | 집중, 우선순위, 목표, 성장 | 가장 중요한 한 가지를 고르는 우선순위 설계 |
| 20 | 그릿 | 앤절라 더크워스 | 비즈니스북스 | 100 철학 | 심리, 자기계발 | J | 끈기, 성장, 열정, 심리 | 재능보다 끈기를 연구한 심리학 |
| 21 | 사랑의 기술 | 에리히 프롬 | 문예출판사 | 100 철학 | 인문·철학, 심리 | F | 사랑, 관계, 철학, 심리 | 사랑을 감정이 아닌 배워야 할 능력으로 본다 |
| 22 | 역사의 쓸모 | 최태성 | 다산초당 | 900 역사 | 역사 | ESF | 역사, 인물, 삶, 교훈 | 역사 속 인물에게서 삶의 태도를 찾는다 |
| 23 | 거꾸로 읽는 세계사 | 유시민 | 돌베개 | 900 역사 | 역사, 사회·정치 | NT | 근현대사, 정치, 역사, 사회 | 근현대 세계사의 굵직한 사건을 다시 읽는다 |
| 24 | 지적 대화를 위한 넓고 얕은 지식 | 채사장 | 한빛비즈 | 300 사회과학 | 인문·철학, 사회·정치 | EN | 교양, 경제, 정치, 철학 | 역사·경제·정치·윤리를 한 흐름으로 정리한다 |
| 25 | 시민의 교양 | 채사장 | 웨일북 | 300 사회과학 | 사회·정치, 인문·철학 | EJ | 세금, 정치, 국가, 교양 | 세금과 국가, 정의를 시민의 눈으로 묻는다 |
| 26 | 군주론 | 니콜로 마키아벨리 | 까치 | 300 사회과학 | 인문·철학, 사회·정치 | NTJ | 권력, 정치, 리더십, 고전 | 권력이 실제로 움직이는 방식을 냉정하게 기술한 고전 |
| 27 | 서양미술사 | E. H. 곰브리치 | 예경 | 600 예술 | 예술, 역사 | INP | 미술, 역사, 감상, 예술 | 미술의 흐름을 이야기로 따라가는 입문서 |
| 28 | 소년이 온다 | 한강 | 창비 | 800 문학 | 한국소설 | IF | 기억, 폭력, 애도, 역사 | 1980년 광주를 여러 목소리로 증언하는 소설 |
| 29 | 작별하지 않는다 | 한강 | 문학동네 | 800 문학 | 한국소설 | INF | 기억, 애도, 우정, 역사 | 제주 4·3의 기억을 끝까지 붙드는 소설 |
| 30 | 채식주의자 | 한강 | 창비 | 800 문학 | 한국소설 | INP | 폭력, 몸, 거부, 가족 | 한 사람의 거부를 세 개의 시선으로 그린 연작 |
| 31 | 82년생 김지영 | 조남주 | 민음사 | 800 문학 | 한국소설, 사회·정치 | SF | 여성, 일상, 차별, 가족 | 평범한 삶의 결에 새겨진 차별의 기록 |
| 32 | 아몬드 | 손원평 | 창비 | 800 문학 | 한국소설 | F | 감정, 성장, 공감, 우정 | 감정을 느끼지 못하는 소년의 성장담 |
| 33 | 불편한 편의점 | 김호연 | 나무옆의자 | 800 문학 | 한국소설 | ESF | 위로, 이웃, 일상, 따뜻함 | 편의점에 모인 사람들의 따뜻한 회복기 |
| 34 | 달러구트 꿈 백화점 | 이미예 | 팩토리나인 | 800 문학 | 한국소설, SF·장르 | ENFP | 꿈, 판타지, 위로, 상상 | 꿈을 사고파는 백화점 판타지 |
| 35 | 우리가 빛의 속도로 갈 수 없다면 | 김초엽 | 허블 | 800 문학 | SF·장르, 한국소설 | INF | SF, 우주, 그리움, 소수자 | 다정하고 쓸쓸한 한국 SF 단편집 |
| 36 | 데미안 | 헤르만 헤세 | 민음사 | 800 문학 | 해외소설 | INF | 성장, 자아, 내면, 철학 | 자기 자신이 되어가는 길에 관한 고전 |
| 37 | 1984 | 조지 오웰 | 민음사 | 800 문학 | 해외소설, SF·장르 | INTJ | 감시, 권력, 디스토피아, 자유 | 감시 사회를 그린 디스토피아 고전 |
| 38 | 멋진 신세계 | 올더스 헉슬리 | 소담출판사 | 800 문학 | 해외소설, SF·장르 | NTP | 디스토피아, 쾌락, 통제, 자유 | 쾌락으로 통제되는 또 다른 디스토피아 |
| 39 | 이방인 | 알베르 카뮈 | 민음사 | 800 문학 | 해외소설, 인문·철학 | ITP | 부조리, 실존, 죽음, 철학 | 부조리를 정면으로 보는 실존주의 소설 |
| 40 | 페스트 | 알베르 카뮈 | 민음사 | 800 문학 | 해외소설 | IFJ | 재난, 연대, 실존, 공동체 | 재난 속에서 연대를 택하는 사람들 |
| 41 | 이처럼 사소한 것들 | 클레어 키건 | 다산책방 | 800 문학 | 해외소설 | IF | 양심, 침묵, 공동체, 선택 | 짧고 조용하게 양심을 묻는 소설 |
| 42 | 프로젝트 헤일메리 | 앤디 위어 | 알에이치코리아 | 800 문학 | SF·장르, 해외소설 | ENTP | 과학, 우주, 문제해결, 우정 | 과학으로 하나씩 문제를 푸는 우주 생존기 |
| 43 | 나미야 잡화점의 기적 | 히가시노 게이고 | 현대문학 | 800 문학 | 해외소설, SF·장르 | F | 위로, 편지, 시간, 연결 | 시간을 건너오는 고민 상담 편지 |
| 44 | 용의자 X의 헌신 | 히가시노 게이고 | 현대문학 | 800 문학 | SF·장르, 해외소설 | IT | 추리, 논리, 헌신, 트릭 | 논리와 헌신이 맞부딪치는 추리소설 |
| 45 | 언어의 온도 | 이기주 | 말글터 | 800 문학 | 에세이 | ISF | 말, 관계, 일상, 감성 | 일상의 말에 담긴 온도를 기록한 산문 |
| 46 | 호모 데우스 | 유발 하라리 | 김영사 | 900 역사 | 역사, 과학 | NT | 미래, 기술, 인공지능, 인류 | 데이터와 알고리즘이 인간을 어떻게 바꿀지 내다본다 |
| 47 | 안네의 일기 | 안네 프랑크 | 문학사상 | 900 역사 | 역사, 에세이 | IF | 전쟁, 일기, 성장, 기록 | 은신처에서 쓴 소녀의 일기, 전쟁을 개인의 목소리로 읽는다 |
| 48 | 우리는 왜 잠을 자야 할까 | 매슈 워커 | 열린책들 | 400 자연과학 | 과학 | ST | 수면, 뇌, 건강, 과학 | 수면 과학으로 하루의 쓸모를 다시 계산해 보게 한다 |
| 49 | 랩 걸 | 호프 자런 | 알마 | 400 자연과학 | 과학, 에세이 | INF | 식물, 과학자, 여성, 성장 | 식물학자의 연구실 이야기와 성장 회고가 함께 흐른다 |
| 50 | 설득의 심리학 | 로버트 치알디니 | 21세기북스 | 300 사회과학 | 심리, 경제·경영 | ET | 설득, 영향력, 심리, 마케팅 | 사람이 왜 '예'라고 말하는지 여섯 원칙으로 푼다 |
| 51 | 철학은 어떻게 삶의 무기가 되는가 | 야마구치 슈 | 다산초당 | 100 철학 | 인문·철학, 자기계발 | ST | 철학, 비즈니스, 사고, 교양 | 철학을 일과 판단에 쓰는 도구로 소개한다 |
| 52 | 어떻게 살 것인가 | 유시민 | 생각의길 | 300 사회과학 | 인문·철학, 사회·정치 | NF | 삶, 죽음, 태도, 철학 | 삶과 죽음, 사회를 하나의 질문으로 엮은 에세이 |
| 53 | 부의 추월차선 | MJ 드마코 | 토트 | 300 사회과학 | 경제·경영, 자기계발 | TJ | 부, 사업, 시간, 경제 | 시간과 소득 구조를 다시 짜보게 하는 직설적인 책 |
| 54 | 부자 아빠 가난한 아빠 | 로버트 기요사키 | 민음인 | 300 사회과학 | 경제·경영, 자기계발 | SJ | 돈, 자산, 금융교육, 경제 | 자산과 부채를 보는 기본 관점을 쉽게 잡아준다 |
| 55 | 데일 카네기 인간관계론 | 데일 카네기 | 현대지성 | 300 사회과학 | 자기계발 | ESF | 관계, 대화, 호감, 성장 | 사람을 대하는 태도를 사례로 정리한 고전 |
| 56 | 역행자 | 자청 | 웅진지식하우스 | 300 사회과학 | 자기계발, 경제·경영 | NT | 성장, 변화, 실행, 자수성가 | 변화를 단계별로 설계해 보는 자기계발서 |
| 57 | 빈센트 반 고흐 영혼의 편지 | 빈센트 반 고흐 | 위즈덤하우스 | 600 예술 | 예술, 에세이 | INF | 편지, 화가, 고독, 예술 | 편지로 읽는 화가의 내면과 작업 이야기 |
| 58 | 숨결이 바람 될 때 | 폴 칼라니티 | 흐름출판 | 800 문학 | 에세이 | IF | 죽음, 삶, 의사, 의미 | 의사이자 환자였던 저자가 남긴 삶의 기록 |
| 59 | 여행의 이유 | 김영하 | 문학동네 | 800 문학 | 에세이 | IP | 여행, 일상, 사유, 산문 | 여행을 통해 일상을 다시 보는 산문집 |
| 60 | 모순 | 양귀자 | 쓰다 | 800 문학 | 한국소설 | F | 삶, 선택, 사랑, 쌍둥이 | 두 자매의 삶으로 인생의 모순을 묻는 소설 |
| 61 | 지구 끝의 온실 | 김초엽 | 자이언트북스 | 800 문학 | SF·장르, 한국소설 | NF | 식물, 재난, 생태, 공동체 | 재난 이후의 세계에서 식물과 사람이 이어지는 이야기 |
| 62 | 시선으로부터, | 정세랑 | 문학동네 | 800 문학 | 한국소설 | NF | 가족, 세대, 여성, 연대 | 한 가족의 여러 세대를 경쾌하게 엮은 장편 |
| 63 | 파친코 | 이민진 | 문학사상 | 800 문학 | 해외소설, 역사 | SF | 이민, 가족, 역사, 세대 | 재일 한인 가족의 4대를 따라가는 대하소설 |
| 64 | 어린 왕자 | 앙투안 드 생텍쥐페리 | 열린책들 | 800 문학 | 해외소설 | INF | 관계, 순수, 어른, 철학 | 짧지만 읽는 나이마다 다르게 닿는 이야기 |
| 65 | 호밀밭의 파수꾼 | J. D. 샐린저 | 민음사 | 800 문학 | 해외소설 | INP | 청춘, 방황, 자아, 성장 | 세상과 어긋난 청춘의 목소리 |
| 66 | 앵무새 죽이기 | 하퍼 리 | 열린책들 | 800 문학 | 해외소설 | F | 정의, 편견, 성장, 인종 | 아이의 눈으로 정의와 편견을 묻는 소설 |
| 67 | 위대한 개츠비 | F. 스콧 피츠제럴드 | 민음사 | 800 문학 | 해외소설 | SF | 욕망, 계급, 사랑, 허무 | 욕망과 계급의 화려한 몰락을 그린 고전 |
| 68 | 노인과 바다 | 어니스트 헤밍웨이 | 민음사 | 800 문학 | 해외소설 | IJ | 도전, 고독, 품위, 삶 | 짧은 문장으로 패배 속의 품위를 그린다 |
| 69 | 변신 | 프란츠 카프카 | 민음사 | 800 문학 | 해외소설 | INP | 소외, 가족, 부조리, 불안 | 어느 날 벌레가 된 사람의 소외를 그린 중편 |
| 70 | 그리스인 조르바 | 니코스 카잔자키스 | 열린책들 | 800 문학 | 해외소설 | NP | 자유, 삶, 본능, 철학 | 책으로 사는 사람과 몸으로 사는 사람의 만남 |
| 71 | 삼체 | 류츠신 | 자음과모음 | 800 문학 | SF·장르, 해외소설 | NT | 우주, 문명, 과학, 생존 | 문명 사이의 충돌을 과학적 상상으로 밀어붙인다 |
| 72 | 듄 | 프랭크 허버트 | 황금가지 | 800 문학 | SF·장르, 해외소설 | NTJ | 생태, 권력, 정치, 운명 | 생태와 정치, 종교가 얽힌 SF 대서사 |
| 73 | 안드로이드는 전기양을 꿈꾸는가? | 필립 K. 딕 | 황금가지 | 800 문학 | SF·장르 | INT | 인공지능, 인간성, 정체성, 미래 | 무엇이 인간을 인간이게 하는지 묻는 SF |
| 74 | 파운데이션 | 아이작 아시모프 | 황금가지 | 800 문학 | SF·장르 | NTJ | 제국, 미래, 역사, 예측 | 역사를 수학으로 예측하려는 SF 고전 |

## 7. 내장 이벤트 데이터 (21건, 2026-10-07 조사)

> 출처: 알라딘 이벤트 페이지, 예스24 이벤트세상, 민음사 이벤트 페이지를 2026-10-07에 읽은 결과. 알라딘·예스24의 링크는 개별 이벤트 상세가 아니라 **이벤트 목록 페이지**입니다. 예스24 항목은 영문으로 요약된 형태로 수집해서 제목·혜택 문구를 한국어로 옮겨 적었고, 정확한 원문 제목·조건은 링크에서 확인해야 합니다. **교보문고 이벤트 목록은 확인하지 못해** 데이터에 없습니다(바로가기 링크만 있음). 이벤트는 자동 갱신되지 않습니다.

| 출처 | 제목 | 혜택 | 시작 | 마감 | 링크 |
|---|---|---|---|---|---|
| 알라딘 | 100일 습관 노트 · 김종원 작가 상담소 | 도서 구매 시 참여, 10월 20일 당첨자 발표 | 2026-10-07 | 2026-10-20 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『잘 살 궁리』 신간 알림 신청 | 추첨으로 적립금 1천 원, 10월 13일 발표 | 2026-10-06 | 2026-10-12 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『호신술 클럽』 출간 기념 북토크 | 10월 27일(화) 오후 7시 북토크 참여 신청 | 2026-10-06 | 2026-10-23 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『서늘한 대화』 정재승 사인본 · 강연회 초대 | 저자 사인 인쇄본, 출간 기념 강연회 초대 | 2026-10-06 | 상시 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『미스테리아』 65호 할인쿠폰 | 1천 원 할인쿠폰 | 2026-10-06 | 2026-10-31 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『엄마의 무릎 성경』 아메리카노 추첨 | 커피 기프티콘 추첨, 11월 27일 발표 | 2026-10-06 | 2026-11-20 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『노화 격파』 챌린지 플래너 | 노화 역행 4주 챌린지 플래너 증정 | 2026-10-06 | 2027-01-06 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 알라딘 | 『안식월 일기』 캐리어 키링 | 한정판 캐리어 키링 증정 | 2026-10-06 | 2027-01-06 | https://www.aladin.co.kr/events/wevent_sub.aspx |
| 예스24 | 경제경영 보너스 데이 | 매일 선착순 1천 원 상품권 | 2026-10-02 | 2026-10-11 | https://event.yes24.com/ |
| 예스24 | 경복궁 키캡 키링 | 굿즈 이벤트 | 2026-10-06 | 2026-10-26 | https://event.yes24.com/ |
| 예스24 | 무라카미 하루키 신간 예약판매 | 예약 구매 시 블랙 롱머그 증정 | 2026-09-29 | 2026-10-30 | https://event.yes24.com/ |
| 예스24 | 한글날 100주년 기획전 | 한국어·한글 주제 도서 기획전 | 2026-09-29 | 2026-10-31 | https://event.yes24.com/ |
| 예스24 | 박성준 작가에게 묻다 | 작가와 질문·답변 이벤트 | 2026-10-02 | 2026-11-05 | https://event.yes24.com/ |
| 예스24 | 가을 그림책 기획전 | 계절 그림책 모음 | 2026-10-06 | 2026-11-09 | https://event.yes24.com/ |
| 예스24 | NEXT PAGE | 대학생·취업준비생 대상 도서 프로그램 | 2026-10-01 | 2026-12-15 | https://event.yes24.com/ |
| 민음사 | 10월, 오늘의 젊은 독자단 모집 | 민음북클럽 독자단 모집 | 2026-10-06 | 2026-10-14 | https://minumsa.com/event/41950/ |
| 민음사 | 2026 세계문학 일력 | 매일 한 문장 세계문학 일력 | 2026-01-08 | 2026-10-31 | https://minumsa.com/event/40925/ |
| 민음사 | 예술의전당 토월정통연극 할인 | 민음사 멤버십 15% 할인 | 2026-09-18 | 2026-11-22 | https://minumsa.com/event/41905/ |
| 민음사 | 민음사 × 국립심포니오케스트라 | 멤버십 공연 할인 | 2026-01-21 | 2026-12-03 | https://minumsa.com/event/41010/ |
| 민음사 | 세계문학전집 앱 출시 | 세계문학전집 앱 이용 | 2026-06-12 | 2026-12-31 | https://minumsa.com/event/41534/ |
| 민음사 | 《한편》 뉴스레터 구독 | 인문잡지 뉴스레터 | 2020-01-14 | 상시 | https://minumsa.com/event/32747/ |

## 8. 알려진 한계 · 다음 작업 후보

1. **iOS 실기기 미검증.** 아이폰 파일 앱·Safari에서 실제로 어떻게 보이는지 확인 필요. 안 되면 (a) 어떤 앱으로 열었는지, (b) 스크린샷을 기준으로 수정.
2. **이벤트 최신화.** 현재는 `EVENTS` 배열에 손으로 넣은 고정 데이터. 자동화하려면 출처 페이지를 주기적으로 읽어 변경분을 제안 → 승인 → 반영하는 파이프라인이 필요(스크래핑 허용 범위·약관 확인 필요).
3. **데이터 분리.** `RAW`(책)와 `EVENTS`(이벤트)를 JSON/CSV로 분리하고 빌드 단계에서 HTML에 인라인하는 구조 권장. 지금은 정적 간단 버전(`.ns`)의 카드·이벤트 HTML이 **파이썬 스크립트로 생성된 결과물**이라, 데이터를 바꾸면 두 군데(스크립트용 `RAW`/`EVENTS` + 정적 마크업)를 다시 만들어야 합니다. 빌드 스크립트로 한 번에 생성하도록 정리하는 것이 1순위.
4. **성향 매핑 검수.** 책별 성향글자는 휴리스틱. 사용자/전문가 검수 필요.
5. **KDC 표기.** 책등에는 대분류(100·300·400·600·800·900)만 표시. 세부 분류는 없음.
6. **교보문고 이벤트 추가**, 리디북스 등 출처 확장.
7. **추천 품질.** 서가가 74권이라 분야를 많이 좁히면 결과가 적게 나옴. 도서 수 확대 또는 외부 도서 API(별도 합의 필요, 현재는 사용 안 함) 검토.
8. 과거 버전의 **Claude 호출 맞춤 추천**(아티팩트 `sample` 기능)은 요청에 따라 제거. 필요하면 아티팩트 버전으로만 부활 가능.
9. 참고: 초기 버전은 claude.ai 아티팩트로도 게시됨(비공개, 본인만 열람). 현재 파일 기준 소스는 이 문서 부록이 최신입니다. 아티팩트 쪽은 구조가 약간 다른 이전 판입니다.

## 9. 부록 — 전체 소스 `book-recommender.html`

````html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>html{color-scheme:light dark}body{margin:0;font-size:15px}</style>
<title>성향 서가</title>
<style>
/* Layout: a library desk. Left = reader card (input), right = shelf (results). Events tab = due-date stamped list. */
:root{
  --paper:#F5F7F4; --card:#FFFFFF; --ink:#1B2A25; --muted:#5B6B64; --line:#D3DCD7;
  --accent:#1F5C4A; --accent-soft:#E3EEE9; --stamp:#A8701A; --stamp-soft:#F6ECDB; --warn:#B4442F;
  --f-display:"Noto Serif KR","Nanum Myeongjo","AppleMyungjo","Batang",serif;
  --f-body:"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic","Segoe UI",system-ui,sans-serif;
  --f-mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#111916; --card:#17211D; --ink:#E4ECE8; --muted:#9AABA3; --line:#2A3833;
  --accent:#72C4A7; --accent-soft:#1D332B; --stamp:#E2B460; --stamp-soft:#302714; --warn:#EE8A74; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#111916; --card:#17211D; --ink:#E4ECE8; --muted:#9AABA3; --line:#2A3833;
  --accent:#72C4A7; --accent-soft:#1D332B; --stamp:#E2B460; --stamp-soft:#302714; --warn:#EE8A74; color-scheme:dark}

*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:var(--f-body);font-size:15px;line-height:1.6;padding-inline:16px;padding-block:0 48px}
.wrap{max-width:1120px;margin:0 auto}
button,input,textarea{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

header.top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px 24px;padding-block:28px 18px;border-bottom:1px solid var(--line)}
.brand h1{font-family:var(--f-display);font-weight:700;font-size:clamp(28px,4.4vw,40px);line-height:1.15;margin:0;letter-spacing:-.01em;text-wrap:balance}
.brand p{margin:6px 0 0;color:var(--muted);font-size:14px}
nav.tabs{display:flex;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:4px}
nav.tabs button{border:0;background:transparent;padding:8px 16px;border-radius:999px;cursor:pointer;font-weight:500;color:var(--muted)}
nav.tabs button[aria-selected="true"]{background:var(--accent);color:var(--paper)}

.eyebrow{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}

/* Recommend */
.desk{display:grid;grid-template-columns:minmax(0,360px) minmax(0,1fr);gap:28px;padding-top:24px;align-items:start}
@media (max-width:820px){.desk{grid-template-columns:minmax(0,1fr)}}
.reader{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:20px;display:flex;flex-direction:column;gap:20px;position:sticky;top:calc(env(safe-area-inset-top,0px) + 12px)}
@media (max-width:820px){.reader{position:static}}
.reader h2{font-family:var(--f-display);font-size:20px;margin:0}
.field{display:flex;flex-direction:column;gap:8px}
.field label,.field .lab{font-weight:600;font-size:14px}
.hint{font-size:12.5px;color:var(--muted);margin:0}

.mbti{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
.axis{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:4px;overflow:hidden}
.axis button{border:0;background:transparent;padding:7px 0;cursor:pointer;font-family:var(--f-mono);font-size:17px;font-weight:500;color:var(--muted)}
.axis button+button{border-top:1px solid var(--line)}
.axis button[aria-pressed="true"]{background:var(--accent);color:var(--paper)}
.typeline{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.typeline b{font-family:var(--f-mono);font-size:22px;letter-spacing:.06em;color:var(--accent)}
.typeline span{font-size:13px;color:var(--muted)}

.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--line);background:transparent;border-radius:999px;padding:5px 11px;font-size:13.5px;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);font-weight:600}

input[type=text],textarea{width:100%;border:1px solid var(--line);background:var(--paper);border-radius:4px;padding:9px 11px}
textarea{min-height:76px;resize:vertical}
.actions{display:flex;flex-direction:column;gap:8px}
.btn{border:1px solid var(--accent);background:var(--accent);color:var(--paper);border-radius:4px;padding:11px 14px;font-weight:600;cursor:pointer}
.btn.ghost{background:transparent;color:var(--accent)}
.btn:disabled{opacity:.55;cursor:default}

.shelf{display:flex;flex-direction:column;gap:28px;min-width:0}
.profile{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 18px;align-items:start;padding-bottom:20px;border-bottom:1px solid var(--line)}
.profile .code{font-family:var(--f-mono);font-size:44px;line-height:1;color:var(--accent);font-weight:500;grid-row:span 2}
.profile h3{font-family:var(--f-display);font-size:21px;margin:0;text-wrap:balance}
.profile p{margin:0;color:var(--muted);max-width:62ch}

.sechead{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.sechead h3{font-family:var(--f-display);font-size:19px;margin:0}
.status{font-size:13px;color:var(--muted)}

.books{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.book{display:grid;grid-template-columns:44px minmax(0,1fr);background:var(--card);border:1px solid var(--line);border-radius:4px;overflow:hidden}
.spine{background:var(--accent-soft);color:var(--accent);font-family:var(--f-mono);font-size:12px;writing-mode:vertical-rl;text-orientation:mixed;display:flex;align-items:center;justify-content:center;gap:6px;letter-spacing:.08em;padding:10px 0;border-right:1px solid var(--line)}
.book.ai .spine{background:var(--stamp-soft);color:var(--stamp)}
.bbody{padding:13px 14px;display:flex;flex-direction:column;gap:6px;min-width:0}
.bbody h4{font-family:var(--f-display);font-size:17px;line-height:1.35;margin:0}
.meta{font-size:12.5px;color:var(--muted)}
.why{font-size:13.5px;margin:0}
.tags{display:flex;flex-wrap:wrap;gap:4px;margin-top:auto;padding-top:4px}
.tag{font-size:11.5px;border:1px solid var(--line);border-radius:3px;padding:1px 6px;color:var(--muted)}
.tag.hit{border-color:var(--accent);color:var(--accent)}
.links{display:flex;gap:10px;font-size:12.5px}
.links a{color:var(--accent);text-underline-offset:3px}
.empty{border:1px dashed var(--line);border-radius:4px;padding:18px;color:var(--muted);font-size:14px}
.err{color:var(--warn);font-size:13.5px}

/* Events */
.evbar{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:center;padding-top:24px}
.evlist{display:flex;flex-direction:column;margin-top:14px;border-top:1px solid var(--line)}
.ev{display:grid;grid-template-columns:92px minmax(0,1fr) auto;gap:16px;align-items:center;padding:14px 4px;border-bottom:1px solid var(--line)}
@media (max-width:560px){.ev{grid-template-columns:78px minmax(0,1fr)}.ev .go{grid-column:2}}
.due{border:1.5px solid var(--stamp);color:var(--stamp);border-radius:4px;text-align:center;padding:5px 2px;font-family:var(--f-mono);transform:rotate(-2deg)}
.due small{display:block;font-size:10px;letter-spacing:.1em}
.due b{display:block;font-size:17px;font-weight:500;font-variant-numeric:tabular-nums}
.due.soon{border-color:var(--warn);color:var(--warn)}
.due.long{border-style:dashed}
.ev h4{margin:0;font-size:15.5px;font-weight:600}
.ev .src{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.06em;color:var(--accent);margin-right:8px}
.ev p{margin:2px 0 0;font-size:13.5px;color:var(--muted)}
.go{font-size:13px;color:var(--accent);white-space:nowrap;text-underline-offset:3px}
.more{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:22px;font-size:13.5px;color:var(--muted)}
.more a{color:var(--accent)}
.note{font-size:12.5px;color:var(--muted);margin-top:10px}

@media (prefers-reduced-motion:no-preference){.book{animation:rise .35s ease both}@keyframes rise{from{transform:translateY(6px)}to{transform:none}}}
</style>

<style>
.jsapp{display:none}
.js .jsapp{display:block}
.js .ns{display:none}
.ns .vh{position:absolute;opacity:0;width:1px;height:1px;pointer-events:none}
.ns label.chip{display:inline-block;user-select:none}
.ns .vh:checked+label.chip{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);font-weight:600}
.ns .vh:focus-visible+label.chip{outline:2px solid var(--accent);outline-offset:2px}
.ns .mrow{display:flex;gap:6px;flex-wrap:wrap}
.ns .mrow label.chip{font-family:var(--f-mono);font-size:16px;min-width:48px;text-align:center}
.ns .pbox{display:none}
.ns .nsintro{background:var(--stamp-soft);border:1px solid var(--stamp);border-radius:4px;padding:10px 12px;font-size:13.5px;margin:16px 0 0}
.ns .nsnav{display:flex;gap:14px;margin-top:12px;font-size:14px}.ns .nsnav a{color:var(--accent)}
.ns .sechead{margin-top:6px}
.ns .ev{display:grid}
@supports selector(:has(a)){
.nsapp .book{display:none}
.nsapp:not(:has(.gv:checked)) .book{display:grid}
.nsapp .ctag{display:none}
.nsapp:has(#g-inmun:checked) .book.g-inmun{display:grid}
.nsapp:has(#g-social:checked) .book.g-social{display:grid}
.nsapp:has(#g-history:checked) .book.g-history{display:grid}
.nsapp:has(#g-science:checked) .book.g-science{display:grid}
.nsapp:has(#g-econ:checked) .book.g-econ{display:grid}
.nsapp:has(#g-psych:checked) .book.g-psych{display:grid}
.nsapp:has(#g-self:checked) .book.g-self{display:grid}
.nsapp:has(#g-knovel:checked) .book.g-knovel{display:grid}
.nsapp:has(#g-wnovel:checked) .book.g-wnovel{display:grid}
.nsapp:has(#g-sf:checked) .book.g-sf{display:grid}
.nsapp:has(#g-essay:checked) .book.g-essay{display:grid}
.nsapp:has(#g-art:checked) .book.g-art{display:grid}
.nsapp:has(#m-E:checked) .ctag.c-E{display:inline-block}
.nsapp:has(#m-E:checked) .book.a-E{border-color:var(--accent)}
.nsapp:has(#m-I:checked) .ctag.c-I{display:inline-block}
.nsapp:has(#m-I:checked) .book.a-I{border-color:var(--accent)}
.nsapp:has(#m-S:checked) .ctag.c-S{display:inline-block}
.nsapp:has(#m-S:checked) .book.a-S{border-color:var(--accent)}
.nsapp:has(#m-N:checked) .ctag.c-N{display:inline-block}
.nsapp:has(#m-N:checked) .book.a-N{border-color:var(--accent)}
.nsapp:has(#m-T:checked) .ctag.c-T{display:inline-block}
.nsapp:has(#m-T:checked) .book.a-T{border-color:var(--accent)}
.nsapp:has(#m-F:checked) .ctag.c-F{display:inline-block}
.nsapp:has(#m-F:checked) .book.a-F{border-color:var(--accent)}
.nsapp:has(#m-J:checked) .ctag.c-J{display:inline-block}
.nsapp:has(#m-J:checked) .book.a-J{border-color:var(--accent)}
.nsapp:has(#m-P:checked) .ctag.c-P{display:inline-block}
.nsapp:has(#m-P:checked) .book.a-P{border-color:var(--accent)}
.nsapp:has(#m-N:checked):has(#m-T:checked) .p-NT{display:grid}
.nsapp:has(#m-N:checked):has(#m-F:checked) .p-NF{display:grid}
.nsapp:has(#m-S:checked):has(#m-T:checked) .p-ST{display:grid}
.nsapp:has(#m-S:checked):has(#m-F:checked) .p-SF{display:grid}
.evs .ev{display:grid}
.evs:has(#s-aladin:checked) .ev:not(.e-aladin){display:none}
.evs:has(#s-yes24:checked) .ev:not(.e-yes24){display:none}
.evs:has(#s-minum:checked) .ev:not(.e-minum){display:none}
.nsapp{--sE:0;--sI:1;--sS:0;--sN:1;--sT:1;--sF:0;--sJ:1;--sP:0}
.nsapp .book{--hE:0;--hI:0;--hS:0;--hN:0;--hT:0;--hF:0;--hJ:0;--hP:0;order:calc(10000 - 100 * (var(--hE) * (3 * var(--sE) - 1) + var(--hI) * (3 * var(--sI) - 1) + var(--hS) * (3 * var(--sS) - 1) + var(--hN) * (3 * var(--sN) - 1) + var(--hT) * (3 * var(--sT) - 1) + var(--hF) * (3 * var(--sF) - 1) + var(--hJ) * (3 * var(--sJ) - 1) + var(--hP) * (3 * var(--sP) - 1)) + var(--i))}
.nsapp:has(#m-E:checked){--sE:1;--sI:0}
.nsapp:has(#m-I:checked){--sI:1;--sE:0}
.nsapp:has(#m-S:checked){--sS:1;--sN:0}
.nsapp:has(#m-N:checked){--sN:1;--sS:0}
.nsapp:has(#m-T:checked){--sT:1;--sF:0}
.nsapp:has(#m-F:checked){--sF:1;--sT:0}
.nsapp:has(#m-J:checked){--sJ:1;--sP:0}
.nsapp:has(#m-P:checked){--sP:1;--sJ:0}
}
</style>
</head>
<body>
<div class="wrap jsapp" id="jsapp">
  <header class="top">
    <div class="brand">
      <div class="eyebrow">Reading desk · 2026 가을</div>
      <h1>성향 서가</h1>
      <p>MBTI와 관심 분야, 최근 마음에 남은 책으로 다음 책을 고르고, 서점·출판사 이벤트도 한 번에 봅니다.</p>
    </div>
    <nav class="tabs" role="tablist">
      <button role="tab" id="tab-rec" aria-selected="true" data-tab="recommend">책 추천</button>
      <button role="tab" id="tab-ev" aria-selected="false" data-tab="events">이벤트 모음</button>
    </nav>
  </header>

  <section id="pane-recommend">
    <div class="desk">
      <form class="reader" id="form" autocomplete="off">
        <div>
          <div class="eyebrow">독서 카드</div>
          <h2>나의 독서 성향</h2>
        </div>
        <div class="field">
          <span class="lab">MBTI</span>
          <div class="mbti" id="mbti"></div>
          <div class="typeline"><b id="typeCode">INTJ</b><span id="typeShort"></span></div>
        </div>
        <div class="field">
          <span class="lab">관심 분야 <span class="hint" style="display:inline">· 여러 개 선택</span></span>
          <div class="chips" id="genres"></div>
        </div>
        <div class="field">
          <label for="recent">최근 감명 깊게 읽은 책</label>
          <input type="text" id="recent" placeholder="예: 공정하다는 착각">
        </div>
        <div class="field">
          <label for="liked">어떤 점이 좋았나요? <span class="hint" style="display:inline">· 선택</span></label>
          <textarea id="liked" placeholder="예: 익숙한 생각을 뒤집는 논리, 사례가 많아서 좋았어요"></textarea>
        </div>
        <div class="actions">
          <button class="btn" type="submit" id="go">서가에서 찾기</button>
        </div>
      </form>

      <div class="shelf">
        <div class="profile" id="profile"></div>
        <div>
          <div class="sechead"><h3>서가 추천</h3><span class="status" id="shelfStatus"></span></div>
          <div class="books" id="books"></div>
        </div>
      </div>
    </div>
  </section>

  <section id="pane-events" hidden>
    <div class="evbar">
      <div class="chips" id="evFilter"></div>
      <span class="status" id="evCount"></span>
    </div>
    <div class="evlist" id="evList"></div>
    <p class="note">2026년 10월 7일 각 사이트 이벤트 페이지 기준으로 모았습니다. 혜택과 기간은 바뀔 수 있으니 참여 전에 원문을 확인하세요.</p>
    <div class="more"><span>더 보기</span>
      <a href="https://event.kyobobook.co.kr/" target="_blank" rel="noopener">교보문고 이벤트</a>
      <a href="https://event.yes24.com/" target="_blank" rel="noopener">예스24 이벤트세상</a>
      <a href="https://www.aladin.co.kr/events/wevent_sub.aspx" target="_blank" rel="noopener">알라딘 이벤트</a>
      <a href="https://minumsa.com/event/" target="_blank" rel="noopener">민음사 이벤트</a>
      <a href="https://ridibooks.com/event/general" target="_blank" rel="noopener">리디 일반도서 이벤트</a>
    </div>
  </section>
</div>

<div class="wrap ns">
  <header class="top"><div class="brand"><div class="eyebrow">Reading desk · 2026 가을</div><h1>성향 서가</h1>
  <p>MBTI와 관심 분야로 다음 책을 고르고, 서점·출판사 이벤트도 한 번에 봅니다.</p></div></header>
  <p class="nsintro">지금 화면은 스크립트를 실행하지 않는 미리보기(파일 앱 등)라서 간단 버전으로 보여요. 최근 읽은 책을 입력해 추천받는 기능은 Safari 같은 브라우저에서 열 때 쓸 수 있어요.</p>
  <div class="nsnav"><a href="#ns-rec">책 추천</a><a href="#ns-ev">이벤트 모음</a></div>
  <div class="nsapp" id="ns-rec">
    <div class="desk" style="grid-template-columns:minmax(0,1fr)">
      <div class="reader" style="position:static">
        <div><div class="eyebrow">독서 카드</div><h2>나의 독서 성향</h2></div>
        <div class="field"><span class="lab">MBTI</span><div class="mrow"><input class="vh" type="radio" name="m0" id="m-E"><label class="chip" for="m-E">E</label><input class="vh" type="radio" name="m0" id="m-I" checked><label class="chip" for="m-I">I</label></div><div class="mrow"><input class="vh" type="radio" name="m1" id="m-S"><label class="chip" for="m-S">S</label><input class="vh" type="radio" name="m1" id="m-N" checked><label class="chip" for="m-N">N</label></div><div class="mrow"><input class="vh" type="radio" name="m2" id="m-T" checked><label class="chip" for="m-T">T</label><input class="vh" type="radio" name="m2" id="m-F"><label class="chip" for="m-F">F</label></div><div class="mrow"><input class="vh" type="radio" name="m3" id="m-J" checked><label class="chip" for="m-J">J</label><input class="vh" type="radio" name="m3" id="m-P"><label class="chip" for="m-P">P</label></div></div>
        <div class="field"><span class="lab">관심 분야 <span class="hint" style="display:inline">· 여러 개 선택, 아무것도 안 고르면 전체</span></span><div class="chips"><input class="vh gv" type="checkbox" id="g-inmun" checked><label class="chip" for="g-inmun">인문·철학</label><input class="vh gv" type="checkbox" id="g-social" checked><label class="chip" for="g-social">사회·정치</label><input class="vh gv" type="checkbox" id="g-history"><label class="chip" for="g-history">역사</label><input class="vh gv" type="checkbox" id="g-science"><label class="chip" for="g-science">과학</label><input class="vh gv" type="checkbox" id="g-econ"><label class="chip" for="g-econ">경제·경영</label><input class="vh gv" type="checkbox" id="g-psych"><label class="chip" for="g-psych">심리</label><input class="vh gv" type="checkbox" id="g-self"><label class="chip" for="g-self">자기계발</label><input class="vh gv" type="checkbox" id="g-knovel"><label class="chip" for="g-knovel">한국소설</label><input class="vh gv" type="checkbox" id="g-wnovel"><label class="chip" for="g-wnovel">해외소설</label><input class="vh gv" type="checkbox" id="g-sf"><label class="chip" for="g-sf">SF·장르</label><input class="vh gv" type="checkbox" id="g-essay"><label class="chip" for="g-essay">에세이</label><input class="vh gv" type="checkbox" id="g-art"><label class="chip" for="g-art">예술</label></div></div>
      </div>
      <div class="shelf">
        <div class="profile pbox p-NT" style="border-bottom:0;padding-bottom:0"><div class="code">NT</div><h3>개념의 설계자</h3><p>구조와 원리를 이해할 때 가장 즐거운 독자입니다. 세계를 설명하는 큰 이론, 논증이 촘촘한 책이 잘 맞습니다.</p></div><div class="profile pbox p-NF" style="border-bottom:0;padding-bottom:0"><div class="code">NF</div><h3>의미를 찾는 독자</h3><p>책에서 사람과 가치를 찾습니다. 삶의 방향을 묻는 인문서와 여운이 긴 소설이 오래 남습니다.</p></div><div class="profile pbox p-ST" style="border-bottom:0;padding-bottom:0"><div class="code">ST</div><h3>사실을 쌓는 독자</h3><p>검증된 사실과 쓸모를 중시합니다. 데이터와 사례가 풍부하고 바로 적용할 수 있는 책을 좋아합니다.</p></div><div class="profile pbox p-SF" style="border-bottom:0;padding-bottom:0"><div class="code">SF</div><h3>이야기에 머무는 독자</h3><p>구체적인 장면과 인물에게 마음이 갑니다. 일상의 결이 살아 있는 소설과 에세이가 잘 맞습니다.</p></div>
        <div><div class="sechead"><h3>서가</h3><span class="status">고른 분야의 책이 나오고, 내 성향과 맞는 책은 테두리와 태그로 표시돼요</span></div>
        <div class="books"><article class="book g-history g-inmun a-N a-T" style="--i:0;--hN:1;--hT:1"><div class="spine">KDC 900<span>역사</span></div><div class="bbody"><h4>사피엔스</h4><div class="meta">유발 하라리 · 김영사</div><p class="why">인류사 전체를 하나의 이야기로 꿰는 거대한 설명</p><div class="tags"><span class="tag">역사</span><span class="tag">인문·철학</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%82%AC%ED%94%BC%EC%97%94%EC%8A%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%82%AC%ED%94%BC%EC%97%94%EC%8A%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%82%AC%ED%94%BC%EC%97%94%EC%8A%A4">알라딘</a></div></div></article><article class="book g-history g-science a-N a-T a-J" style="--i:1;--hN:1;--hT:1;--hJ:1"><div class="spine">KDC 900<span>역사</span></div><div class="bbody"><h4>총 균 쇠</h4><div class="meta">재레드 다이아몬드 · 문학사상</div><p class="why">왜 어떤 문명이 앞서갔는지 환경과 지리로 답한다</p><div class="tags"><span class="tag">역사</span><span class="tag">과학</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%B4%9D%20%EA%B7%A0%20%EC%87%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%B4%9D%20%EA%B7%A0%20%EC%87%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%B4%9D%20%EA%B7%A0%20%EC%87%A0">알라딘</a></div></div></article><article class="book g-inmun g-social a-E a-N" style="--i:2;--hE:1;--hN:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>정의란 무엇인가</h4><div class="meta">마이클 샌델 · 와이즈베리</div><p class="why">사례마다 내 판단을 시험하게 하는 토론형 철학</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">사회·정치</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%A0%95%EC%9D%98%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%A0%95%EC%9D%98%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%A0%95%EC%9D%98%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80">알라딘</a></div></div></article><article class="book g-social g-inmun a-N a-F" style="--i:3;--hN:1;--hF:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>공정하다는 착각</h4><div class="meta">마이클 샌델 · 와이즈베리</div><p class="why">능력주의가 어떻게 사람을 갈라놓는지 짚는다</p><div class="tags"><span class="tag">사회·정치</span><span class="tag">인문·철학</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EA%B3%B5%EC%A0%95%ED%95%98%EB%8B%A4%EB%8A%94%20%EC%B0%A9%EA%B0%81">교보</a><a href="https://www.yes24.com/Product/Search?query=%EA%B3%B5%EC%A0%95%ED%95%98%EB%8B%A4%EB%8A%94%20%EC%B0%A9%EA%B0%81">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EA%B3%B5%EC%A0%95%ED%95%98%EB%8B%A4%EB%8A%94%20%EC%B0%A9%EA%B0%81">알라딘</a></div></div></article><article class="book g-inmun g-social a-I a-N" style="--i:4;--hI:1;--hN:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>피로사회</h4><div class="meta">한병철 · 문학과지성사</div><p class="why">짧고 밀도 높은 현대인 진단서</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">사회·정치</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%94%BC%EB%A1%9C%EC%82%AC%ED%9A%8C">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%94%BC%EB%A1%9C%EC%82%AC%ED%9A%8C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%94%BC%EB%A1%9C%EC%82%AC%ED%9A%8C">알라딘</a></div></div></article><article class="book g-psych g-inmun a-F" style="--i:5;--hF:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>미움받을 용기</h4><div class="meta">기시미 이치로·고가 후미타케 · 인플루엔셜</div><p class="why">대화체로 읽는 아들러 심리학</p><div class="tags"><span class="tag">심리</span><span class="tag">인문·철학</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%AF%B8%EC%9B%80%EB%B0%9B%EC%9D%84%20%EC%9A%A9%EA%B8%B0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%AF%B8%EC%9B%80%EB%B0%9B%EC%9D%84%20%EC%9A%A9%EA%B8%B0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%AF%B8%EC%9B%80%EB%B0%9B%EC%9D%84%20%EC%9A%A9%EA%B8%B0">알라딘</a></div></div></article><article class="book g-psych g-inmun a-I a-F" style="--i:6;--hI:1;--hF:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>죽음의 수용소에서</h4><div class="meta">빅터 프랭클 · 청아출판사</div><p class="why">극한 상황에서 붙잡은 삶의 의미</p><div class="tags"><span class="tag">심리</span><span class="tag">인문·철학</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%A3%BD%EC%9D%8C%EC%9D%98%20%EC%88%98%EC%9A%A9%EC%86%8C%EC%97%90%EC%84%9C">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%A3%BD%EC%9D%8C%EC%9D%98%20%EC%88%98%EC%9A%A9%EC%86%8C%EC%97%90%EC%84%9C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%A3%BD%EC%9D%8C%EC%9D%98%20%EC%88%98%EC%9A%A9%EC%86%8C%EC%97%90%EC%84%9C">알라딘</a></div></div></article><article class="book g-social g-science a-S a-T" style="--i:7;--hS:1;--hT:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>팩트풀니스</h4><div class="meta">한스 로슬링 외 · 김영사</div><p class="why">데이터로 세계를 다시 보는 법</p><div class="tags"><span class="tag">사회·정치</span><span class="tag">과학</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%8C%A9%ED%8A%B8%ED%92%80%EB%8B%88%EC%8A%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%8C%A9%ED%8A%B8%ED%92%80%EB%8B%88%EC%8A%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%8C%A9%ED%8A%B8%ED%92%80%EB%8B%88%EC%8A%A4">알라딘</a></div></div></article><article class="book g-econ g-psych a-T" style="--i:8;--hT:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>넛지</h4><div class="meta">리처드 탈러·캐스 선스타인 · 리더스북</div><p class="why">사람의 선택을 설계하는 행동경제학</p><div class="tags"><span class="tag">경제·경영</span><span class="tag">심리</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%84%9B%EC%A7%80">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%84%9B%EC%A7%80">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%84%9B%EC%A7%80">알라딘</a></div></div></article><article class="book g-psych g-science a-I a-N a-T" style="--i:9;--hI:1;--hN:1;--hT:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>생각에 관한 생각</h4><div class="meta">대니얼 카너먼 · 김영사</div><p class="why">직관과 이성이 어떻게 엇갈리는지 실험으로 보여준다</p><div class="tags"><span class="tag">심리</span><span class="tag">과학</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%83%9D%EA%B0%81%EC%97%90%20%EA%B4%80%ED%95%9C%20%EC%83%9D%EA%B0%81">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%83%9D%EA%B0%81%EC%97%90%20%EA%B4%80%ED%95%9C%20%EC%83%9D%EA%B0%81">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%83%9D%EA%B0%81%EC%97%90%20%EA%B4%80%ED%95%9C%20%EC%83%9D%EA%B0%81">알라딘</a></div></div></article><article class="book g-science a-I a-N a-T" style="--i:10;--hI:1;--hN:1;--hT:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>이기적 유전자</h4><div class="meta">리처드 도킨스 · 을유문화사</div><p class="why">진화를 유전자의 눈으로 다시 쓴 고전</p><div class="tags"><span class="tag">과학</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9D%B4%EA%B8%B0%EC%A0%81%20%EC%9C%A0%EC%A0%84%EC%9E%90">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9D%B4%EA%B8%B0%EC%A0%81%20%EC%9C%A0%EC%A0%84%EC%9E%90">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9D%B4%EA%B8%B0%EC%A0%81%20%EC%9C%A0%EC%A0%84%EC%9E%90">알라딘</a></div></div></article><article class="book g-science a-N a-F" style="--i:11;--hN:1;--hF:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>코스모스</h4><div class="meta">칼 세이건 · 사이언스북스</div><p class="why">과학이 주는 경이를 문학처럼 전한다</p><div class="tags"><span class="tag">과학</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%BD%94%EC%8A%A4%EB%AA%A8%EC%8A%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%BD%94%EC%8A%A4%EB%AA%A8%EC%8A%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%BD%94%EC%8A%A4%EB%AA%A8%EC%8A%A4">알라딘</a></div></div></article><article class="book g-science g-essay a-I a-N a-F" style="--i:12;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>물고기는 존재하지 않는다</h4><div class="meta">룰루 밀러 · 곰출판</div><p class="why">과학 논픽션과 회고록이 겹쳐지는 책</p><div class="tags"><span class="tag">과학</span><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%AC%BC%EA%B3%A0%EA%B8%B0%EB%8A%94%20%EC%A1%B4%EC%9E%AC%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%AC%BC%EA%B3%A0%EA%B8%B0%EB%8A%94%20%EC%A1%B4%EC%9E%AC%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%AC%BC%EA%B3%A0%EA%B8%B0%EB%8A%94%20%EC%A1%B4%EC%9E%AC%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4">알라딘</a></div></div></article><article class="book g-science g-psych a-E a-N" style="--i:13;--hE:1;--hN:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>열두 발자국</h4><div class="meta">정재승 · 어크로스</div><p class="why">뇌과학으로 보는 선택과 창의성</p><div class="tags"><span class="tag">과학</span><span class="tag">심리</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%97%B4%EB%91%90%20%EB%B0%9C%EC%9E%90%EA%B5%AD">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%97%B4%EB%91%90%20%EB%B0%9C%EC%9E%90%EA%B5%AD">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%97%B4%EB%91%90%20%EB%B0%9C%EC%9E%90%EA%B5%AD">알라딘</a></div></div></article><article class="book g-social g-psych a-N a-P" style="--i:14;--hN:1;--hP:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>도둑맞은 집중력</h4><div class="meta">요한 하리 · 어크로스</div><p class="why">집중력 위기를 개인이 아닌 구조의 문제로 본다</p><div class="tags"><span class="tag">사회·정치</span><span class="tag">심리</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%8F%84%EB%91%91%EB%A7%9E%EC%9D%80%20%EC%A7%91%EC%A4%91%EB%A0%A5">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%8F%84%EB%91%91%EB%A7%9E%EC%9D%80%20%EC%A7%91%EC%A4%91%EB%A0%A5">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%8F%84%EB%91%91%EB%A7%9E%EC%9D%80%20%EC%A7%91%EC%A4%91%EB%A0%A5">알라딘</a></div></div></article><article class="book g-science g-social a-I a-F a-J" style="--i:15;--hI:1;--hF:1;--hJ:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>침묵의 봄</h4><div class="meta">레이첼 카슨 · 에코리브르</div><p class="why">환경운동의 출발점이 된 고발서</p><div class="tags"><span class="tag">과학</span><span class="tag">사회·정치</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%B9%A8%EB%AC%B5%EC%9D%98%20%EB%B4%84">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%B9%A8%EB%AC%B5%EC%9D%98%20%EB%B4%84">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%B9%A8%EB%AC%B5%EC%9D%98%20%EB%B4%84">알라딘</a></div></div></article><article class="book g-econ a-S a-J" style="--i:16;--hS:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>돈의 심리학</h4><div class="meta">모건 하우절 · 인플루엔셜</div><p class="why">숫자보다 태도로 다루는 돈 이야기</p><div class="tags"><span class="tag">경제·경영</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%8F%88%EC%9D%98%20%EC%8B%AC%EB%A6%AC%ED%95%99">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%8F%88%EC%9D%98%20%EC%8B%AC%EB%A6%AC%ED%95%99">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%8F%88%EC%9D%98%20%EC%8B%AC%EB%A6%AC%ED%95%99">알라딘</a></div></div></article><article class="book g-self a-S a-J" style="--i:17;--hS:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>아주 작은 습관의 힘</h4><div class="meta">제임스 클리어 · 비즈니스북스</div><p class="why">작은 시스템으로 행동을 바꾸는 실전서</p><div class="tags"><span class="tag">자기계발</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%95%84%EC%A3%BC%20%EC%9E%91%EC%9D%80%20%EC%8A%B5%EA%B4%80%EC%9D%98%20%ED%9E%98">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%95%84%EC%A3%BC%20%EC%9E%91%EC%9D%80%20%EC%8A%B5%EA%B4%80%EC%9D%98%20%ED%9E%98">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%95%84%EC%A3%BC%20%EC%9E%91%EC%9D%80%20%EC%8A%B5%EA%B4%80%EC%9D%98%20%ED%9E%98">알라딘</a></div></div></article><article class="book g-self g-econ a-T a-J" style="--i:18;--hT:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>원씽</h4><div class="meta">게리 켈러·제이 파파산 · 비즈니스북스</div><p class="why">가장 중요한 한 가지를 고르는 우선순위 설계</p><div class="tags"><span class="tag">자기계발</span><span class="tag">경제·경영</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9B%90%EC%94%BD">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9B%90%EC%94%BD">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9B%90%EC%94%BD">알라딘</a></div></div></article><article class="book g-psych g-self a-J" style="--i:19;--hJ:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>그릿</h4><div class="meta">앤절라 더크워스 · 비즈니스북스</div><p class="why">재능보다 끈기를 연구한 심리학</p><div class="tags"><span class="tag">심리</span><span class="tag">자기계발</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EA%B7%B8%EB%A6%BF">교보</a><a href="https://www.yes24.com/Product/Search?query=%EA%B7%B8%EB%A6%BF">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EA%B7%B8%EB%A6%BF">알라딘</a></div></div></article><article class="book g-inmun g-psych a-F" style="--i:20;--hF:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>사랑의 기술</h4><div class="meta">에리히 프롬 · 문예출판사</div><p class="why">사랑을 감정이 아닌 배워야 할 능력으로 본다</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">심리</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%82%AC%EB%9E%91%EC%9D%98%20%EA%B8%B0%EC%88%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%82%AC%EB%9E%91%EC%9D%98%20%EA%B8%B0%EC%88%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%82%AC%EB%9E%91%EC%9D%98%20%EA%B8%B0%EC%88%A0">알라딘</a></div></div></article><article class="book g-history a-E a-S a-F" style="--i:21;--hE:1;--hS:1;--hF:1"><div class="spine">KDC 900<span>역사</span></div><div class="bbody"><h4>역사의 쓸모</h4><div class="meta">최태성 · 다산초당</div><p class="why">역사 속 인물에게서 삶의 태도를 찾는다</p><div class="tags"><span class="tag">역사</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%97%AD%EC%82%AC%EC%9D%98%20%EC%93%B8%EB%AA%A8">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%97%AD%EC%82%AC%EC%9D%98%20%EC%93%B8%EB%AA%A8">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%97%AD%EC%82%AC%EC%9D%98%20%EC%93%B8%EB%AA%A8">알라딘</a></div></div></article><article class="book g-history g-social a-N a-T" style="--i:22;--hN:1;--hT:1"><div class="spine">KDC 900<span>역사</span></div><div class="bbody"><h4>거꾸로 읽는 세계사</h4><div class="meta">유시민 · 돌베개</div><p class="why">근현대 세계사의 굵직한 사건을 다시 읽는다</p><div class="tags"><span class="tag">역사</span><span class="tag">사회·정치</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EA%B1%B0%EA%BE%B8%EB%A1%9C%20%EC%9D%BD%EB%8A%94%20%EC%84%B8%EA%B3%84%EC%82%AC">교보</a><a href="https://www.yes24.com/Product/Search?query=%EA%B1%B0%EA%BE%B8%EB%A1%9C%20%EC%9D%BD%EB%8A%94%20%EC%84%B8%EA%B3%84%EC%82%AC">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EA%B1%B0%EA%BE%B8%EB%A1%9C%20%EC%9D%BD%EB%8A%94%20%EC%84%B8%EA%B3%84%EC%82%AC">알라딘</a></div></div></article><article class="book g-inmun g-social a-E a-N" style="--i:23;--hE:1;--hN:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>지적 대화를 위한 넓고 얕은 지식</h4><div class="meta">채사장 · 한빛비즈</div><p class="why">역사·경제·정치·윤리를 한 흐름으로 정리한다</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">사회·정치</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%A7%80%EC%A0%81%20%EB%8C%80%ED%99%94%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EB%84%93%EA%B3%A0%20%EC%96%95%EC%9D%80%20%EC%A7%80%EC%8B%9D">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%A7%80%EC%A0%81%20%EB%8C%80%ED%99%94%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EB%84%93%EA%B3%A0%20%EC%96%95%EC%9D%80%20%EC%A7%80%EC%8B%9D">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%A7%80%EC%A0%81%20%EB%8C%80%ED%99%94%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EB%84%93%EA%B3%A0%20%EC%96%95%EC%9D%80%20%EC%A7%80%EC%8B%9D">알라딘</a></div></div></article><article class="book g-social g-inmun a-E a-J" style="--i:24;--hE:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>시민의 교양</h4><div class="meta">채사장 · 웨일북</div><p class="why">세금과 국가, 정의를 시민의 눈으로 묻는다</p><div class="tags"><span class="tag">사회·정치</span><span class="tag">인문·철학</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%8B%9C%EB%AF%BC%EC%9D%98%20%EA%B5%90%EC%96%91">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%8B%9C%EB%AF%BC%EC%9D%98%20%EA%B5%90%EC%96%91">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%8B%9C%EB%AF%BC%EC%9D%98%20%EA%B5%90%EC%96%91">알라딘</a></div></div></article><article class="book g-inmun g-social a-N a-T a-J" style="--i:25;--hN:1;--hT:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>군주론</h4><div class="meta">니콜로 마키아벨리 · 까치</div><p class="why">권력이 실제로 움직이는 방식을 냉정하게 기술한 고전</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">사회·정치</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EA%B5%B0%EC%A3%BC%EB%A1%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EA%B5%B0%EC%A3%BC%EB%A1%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EA%B5%B0%EC%A3%BC%EB%A1%A0">알라딘</a></div></div></article><article class="book g-art g-history a-I a-N a-P" style="--i:26;--hI:1;--hN:1;--hP:1"><div class="spine">KDC 600<span>예술</span></div><div class="bbody"><h4>서양미술사</h4><div class="meta">E. H. 곰브리치 · 예경</div><p class="why">미술의 흐름을 이야기로 따라가는 입문서</p><div class="tags"><span class="tag">예술</span><span class="tag">역사</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%84%9C%EC%96%91%EB%AF%B8%EC%88%A0%EC%82%AC">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%84%9C%EC%96%91%EB%AF%B8%EC%88%A0%EC%82%AC">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%84%9C%EC%96%91%EB%AF%B8%EC%88%A0%EC%82%AC">알라딘</a></div></div></article><article class="book g-knovel a-I a-F" style="--i:27;--hI:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>소년이 온다</h4><div class="meta">한강 · 창비</div><p class="why">1980년 광주를 여러 목소리로 증언하는 소설</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%86%8C%EB%85%84%EC%9D%B4%20%EC%98%A8%EB%8B%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%86%8C%EB%85%84%EC%9D%B4%20%EC%98%A8%EB%8B%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%86%8C%EB%85%84%EC%9D%B4%20%EC%98%A8%EB%8B%A4">알라딘</a></div></div></article><article class="book g-knovel a-I a-N a-F" style="--i:28;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>작별하지 않는다</h4><div class="meta">한강 · 문학동네</div><p class="why">제주 4·3의 기억을 끝까지 붙드는 소설</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9E%91%EB%B3%84%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9E%91%EB%B3%84%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9E%91%EB%B3%84%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EB%8B%A4">알라딘</a></div></div></article><article class="book g-knovel a-I a-N a-P" style="--i:29;--hI:1;--hN:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>채식주의자</h4><div class="meta">한강 · 창비</div><p class="why">한 사람의 거부를 세 개의 시선으로 그린 연작</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%B1%84%EC%8B%9D%EC%A3%BC%EC%9D%98%EC%9E%90">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%B1%84%EC%8B%9D%EC%A3%BC%EC%9D%98%EC%9E%90">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%B1%84%EC%8B%9D%EC%A3%BC%EC%9D%98%EC%9E%90">알라딘</a></div></div></article><article class="book g-knovel g-social a-S a-F" style="--i:30;--hS:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>82년생 김지영</h4><div class="meta">조남주 · 민음사</div><p class="why">평범한 삶의 결에 새겨진 차별의 기록</p><div class="tags"><span class="tag">한국소설</span><span class="tag">사회·정치</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=82%EB%85%84%EC%83%9D%20%EA%B9%80%EC%A7%80%EC%98%81">교보</a><a href="https://www.yes24.com/Product/Search?query=82%EB%85%84%EC%83%9D%20%EA%B9%80%EC%A7%80%EC%98%81">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=82%EB%85%84%EC%83%9D%20%EA%B9%80%EC%A7%80%EC%98%81">알라딘</a></div></div></article><article class="book g-knovel a-F" style="--i:31;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>아몬드</h4><div class="meta">손원평 · 창비</div><p class="why">감정을 느끼지 못하는 소년의 성장담</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%95%84%EB%AA%AC%EB%93%9C">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%95%84%EB%AA%AC%EB%93%9C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%95%84%EB%AA%AC%EB%93%9C">알라딘</a></div></div></article><article class="book g-knovel a-E a-S a-F" style="--i:32;--hE:1;--hS:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>불편한 편의점</h4><div class="meta">김호연 · 나무옆의자</div><p class="why">편의점에 모인 사람들의 따뜻한 회복기</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%B6%88%ED%8E%B8%ED%95%9C%20%ED%8E%B8%EC%9D%98%EC%A0%90">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%B6%88%ED%8E%B8%ED%95%9C%20%ED%8E%B8%EC%9D%98%EC%A0%90">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%B6%88%ED%8E%B8%ED%95%9C%20%ED%8E%B8%EC%9D%98%EC%A0%90">알라딘</a></div></div></article><article class="book g-knovel g-sf a-E a-N a-F a-P" style="--i:33;--hE:1;--hN:1;--hF:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>달러구트 꿈 백화점</h4><div class="meta">이미예 · 팩토리나인</div><p class="why">꿈을 사고파는 백화점 판타지</p><div class="tags"><span class="tag">한국소설</span><span class="tag">SF·장르</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%8B%AC%EB%9F%AC%EA%B5%AC%ED%8A%B8%20%EA%BF%88%20%EB%B0%B1%ED%99%94%EC%A0%90">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%8B%AC%EB%9F%AC%EA%B5%AC%ED%8A%B8%20%EA%BF%88%20%EB%B0%B1%ED%99%94%EC%A0%90">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%8B%AC%EB%9F%AC%EA%B5%AC%ED%8A%B8%20%EA%BF%88%20%EB%B0%B1%ED%99%94%EC%A0%90">알라딘</a></div></div></article><article class="book g-sf g-knovel a-I a-N a-F" style="--i:34;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>우리가 빛의 속도로 갈 수 없다면</h4><div class="meta">김초엽 · 허블</div><p class="why">다정하고 쓸쓸한 한국 SF 단편집</p><div class="tags"><span class="tag">SF·장르</span><span class="tag">한국소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9A%B0%EB%A6%AC%EA%B0%80%20%EB%B9%9B%EC%9D%98%20%EC%86%8D%EB%8F%84%EB%A1%9C%20%EA%B0%88%20%EC%88%98%20%EC%97%86%EB%8B%A4%EB%A9%B4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9A%B0%EB%A6%AC%EA%B0%80%20%EB%B9%9B%EC%9D%98%20%EC%86%8D%EB%8F%84%EB%A1%9C%20%EA%B0%88%20%EC%88%98%20%EC%97%86%EB%8B%A4%EB%A9%B4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9A%B0%EB%A6%AC%EA%B0%80%20%EB%B9%9B%EC%9D%98%20%EC%86%8D%EB%8F%84%EB%A1%9C%20%EA%B0%88%20%EC%88%98%20%EC%97%86%EB%8B%A4%EB%A9%B4">알라딘</a></div></div></article><article class="book g-wnovel a-I a-N a-F" style="--i:35;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>데미안</h4><div class="meta">헤르만 헤세 · 민음사</div><p class="why">자기 자신이 되어가는 길에 관한 고전</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%8D%B0%EB%AF%B8%EC%95%88">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%8D%B0%EB%AF%B8%EC%95%88">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%8D%B0%EB%AF%B8%EC%95%88">알라딘</a></div></div></article><article class="book g-wnovel g-sf a-I a-N a-T a-J" style="--i:36;--hI:1;--hN:1;--hT:1;--hJ:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>1984</h4><div class="meta">조지 오웰 · 민음사</div><p class="why">감시 사회를 그린 디스토피아 고전</p><div class="tags"><span class="tag">해외소설</span><span class="tag">SF·장르</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=1984">교보</a><a href="https://www.yes24.com/Product/Search?query=1984">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=1984">알라딘</a></div></div></article><article class="book g-wnovel g-sf a-N a-T a-P" style="--i:37;--hN:1;--hT:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>멋진 신세계</h4><div class="meta">올더스 헉슬리 · 소담출판사</div><p class="why">쾌락으로 통제되는 또 다른 디스토피아</p><div class="tags"><span class="tag">해외소설</span><span class="tag">SF·장르</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%A9%8B%EC%A7%84%20%EC%8B%A0%EC%84%B8%EA%B3%84">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%A9%8B%EC%A7%84%20%EC%8B%A0%EC%84%B8%EA%B3%84">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%A9%8B%EC%A7%84%20%EC%8B%A0%EC%84%B8%EA%B3%84">알라딘</a></div></div></article><article class="book g-wnovel g-inmun a-I a-T a-P" style="--i:38;--hI:1;--hT:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>이방인</h4><div class="meta">알베르 카뮈 · 민음사</div><p class="why">부조리를 정면으로 보는 실존주의 소설</p><div class="tags"><span class="tag">해외소설</span><span class="tag">인문·철학</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9D%B4%EB%B0%A9%EC%9D%B8">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9D%B4%EB%B0%A9%EC%9D%B8">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9D%B4%EB%B0%A9%EC%9D%B8">알라딘</a></div></div></article><article class="book g-wnovel a-I a-F a-J" style="--i:39;--hI:1;--hF:1;--hJ:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>페스트</h4><div class="meta">알베르 카뮈 · 민음사</div><p class="why">재난 속에서 연대를 택하는 사람들</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%8E%98%EC%8A%A4%ED%8A%B8">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%8E%98%EC%8A%A4%ED%8A%B8">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%8E%98%EC%8A%A4%ED%8A%B8">알라딘</a></div></div></article><article class="book g-wnovel a-I a-F" style="--i:40;--hI:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>이처럼 사소한 것들</h4><div class="meta">클레어 키건 · 다산책방</div><p class="why">짧고 조용하게 양심을 묻는 소설</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9D%B4%EC%B2%98%EB%9F%BC%20%EC%82%AC%EC%86%8C%ED%95%9C%20%EA%B2%83%EB%93%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9D%B4%EC%B2%98%EB%9F%BC%20%EC%82%AC%EC%86%8C%ED%95%9C%20%EA%B2%83%EB%93%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9D%B4%EC%B2%98%EB%9F%BC%20%EC%82%AC%EC%86%8C%ED%95%9C%20%EA%B2%83%EB%93%A4">알라딘</a></div></div></article><article class="book g-sf g-wnovel a-E a-N a-T a-P" style="--i:41;--hE:1;--hN:1;--hT:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>프로젝트 헤일메리</h4><div class="meta">앤디 위어 · 알에이치코리아</div><p class="why">과학으로 하나씩 문제를 푸는 우주 생존기</p><div class="tags"><span class="tag">SF·장르</span><span class="tag">해외소설</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%ED%97%A4%EC%9D%BC%EB%A9%94%EB%A6%AC">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%ED%97%A4%EC%9D%BC%EB%A9%94%EB%A6%AC">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%ED%97%A4%EC%9D%BC%EB%A9%94%EB%A6%AC">알라딘</a></div></div></article><article class="book g-wnovel g-sf a-F" style="--i:42;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>나미야 잡화점의 기적</h4><div class="meta">히가시노 게이고 · 현대문학</div><p class="why">시간을 건너오는 고민 상담 편지</p><div class="tags"><span class="tag">해외소설</span><span class="tag">SF·장르</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%82%98%EB%AF%B8%EC%95%BC%20%EC%9E%A1%ED%99%94%EC%A0%90%EC%9D%98%20%EA%B8%B0%EC%A0%81">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%82%98%EB%AF%B8%EC%95%BC%20%EC%9E%A1%ED%99%94%EC%A0%90%EC%9D%98%20%EA%B8%B0%EC%A0%81">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%82%98%EB%AF%B8%EC%95%BC%20%EC%9E%A1%ED%99%94%EC%A0%90%EC%9D%98%20%EA%B8%B0%EC%A0%81">알라딘</a></div></div></article><article class="book g-sf g-wnovel a-I a-T" style="--i:43;--hI:1;--hT:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>용의자 X의 헌신</h4><div class="meta">히가시노 게이고 · 현대문학</div><p class="why">논리와 헌신이 맞부딪치는 추리소설</p><div class="tags"><span class="tag">SF·장르</span><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9A%A9%EC%9D%98%EC%9E%90%20X%EC%9D%98%20%ED%97%8C%EC%8B%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9A%A9%EC%9D%98%EC%9E%90%20X%EC%9D%98%20%ED%97%8C%EC%8B%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9A%A9%EC%9D%98%EC%9E%90%20X%EC%9D%98%20%ED%97%8C%EC%8B%A0">알라딘</a></div></div></article><article class="book g-essay a-I a-S a-F" style="--i:44;--hI:1;--hS:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>언어의 온도</h4><div class="meta">이기주 · 말글터</div><p class="why">일상의 말에 담긴 온도를 기록한 산문</p><div class="tags"><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%96%B8%EC%96%B4%EC%9D%98%20%EC%98%A8%EB%8F%84">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%96%B8%EC%96%B4%EC%9D%98%20%EC%98%A8%EB%8F%84">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%96%B8%EC%96%B4%EC%9D%98%20%EC%98%A8%EB%8F%84">알라딘</a></div></div></article><article class="book g-history g-science a-N a-T" style="--i:45;--hN:1;--hT:1"><div class="spine">KDC 900<span>역사</span></div><div class="bbody"><h4>호모 데우스</h4><div class="meta">유발 하라리 · 김영사</div><p class="why">데이터와 알고리즘이 인간을 어떻게 바꿀지 내다본다</p><div class="tags"><span class="tag">역사</span><span class="tag">과학</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%98%B8%EB%AA%A8%20%EB%8D%B0%EC%9A%B0%EC%8A%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%98%B8%EB%AA%A8%20%EB%8D%B0%EC%9A%B0%EC%8A%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%98%B8%EB%AA%A8%20%EB%8D%B0%EC%9A%B0%EC%8A%A4">알라딘</a></div></div></article><article class="book g-history g-essay a-I a-F" style="--i:46;--hI:1;--hF:1"><div class="spine">KDC 900<span>역사</span></div><div class="bbody"><h4>안네의 일기</h4><div class="meta">안네 프랑크 · 문학사상</div><p class="why">은신처에서 쓴 소녀의 일기, 전쟁을 개인의 목소리로 읽는다</p><div class="tags"><span class="tag">역사</span><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%95%88%EB%84%A4%EC%9D%98%20%EC%9D%BC%EA%B8%B0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%95%88%EB%84%A4%EC%9D%98%20%EC%9D%BC%EA%B8%B0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%95%88%EB%84%A4%EC%9D%98%20%EC%9D%BC%EA%B8%B0">알라딘</a></div></div></article><article class="book g-science a-S a-T" style="--i:47;--hS:1;--hT:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>우리는 왜 잠을 자야 할까</h4><div class="meta">매슈 워커 · 열린책들</div><p class="why">수면 과학으로 하루의 쓸모를 다시 계산해 보게 한다</p><div class="tags"><span class="tag">과학</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9A%B0%EB%A6%AC%EB%8A%94%20%EC%99%9C%20%EC%9E%A0%EC%9D%84%20%EC%9E%90%EC%95%BC%20%ED%95%A0%EA%B9%8C">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9A%B0%EB%A6%AC%EB%8A%94%20%EC%99%9C%20%EC%9E%A0%EC%9D%84%20%EC%9E%90%EC%95%BC%20%ED%95%A0%EA%B9%8C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9A%B0%EB%A6%AC%EB%8A%94%20%EC%99%9C%20%EC%9E%A0%EC%9D%84%20%EC%9E%90%EC%95%BC%20%ED%95%A0%EA%B9%8C">알라딘</a></div></div></article><article class="book g-science g-essay a-I a-N a-F" style="--i:48;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 400<span>자연과학</span></div><div class="bbody"><h4>랩 걸</h4><div class="meta">호프 자런 · 알마</div><p class="why">식물학자의 연구실 이야기와 성장 회고가 함께 흐른다</p><div class="tags"><span class="tag">과학</span><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%9E%A9%20%EA%B1%B8">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%9E%A9%20%EA%B1%B8">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%9E%A9%20%EA%B1%B8">알라딘</a></div></div></article><article class="book g-psych g-econ a-E a-T" style="--i:49;--hE:1;--hT:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>설득의 심리학</h4><div class="meta">로버트 치알디니 · 21세기북스</div><p class="why">사람이 왜 &#x27;예&#x27;라고 말하는지 여섯 원칙으로 푼다</p><div class="tags"><span class="tag">심리</span><span class="tag">경제·경영</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%84%A4%EB%93%9D%EC%9D%98%20%EC%8B%AC%EB%A6%AC%ED%95%99">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%84%A4%EB%93%9D%EC%9D%98%20%EC%8B%AC%EB%A6%AC%ED%95%99">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%84%A4%EB%93%9D%EC%9D%98%20%EC%8B%AC%EB%A6%AC%ED%95%99">알라딘</a></div></div></article><article class="book g-inmun g-self a-S a-T" style="--i:50;--hS:1;--hT:1"><div class="spine">KDC 100<span>철학</span></div><div class="bbody"><h4>철학은 어떻게 삶의 무기가 되는가</h4><div class="meta">야마구치 슈 · 다산초당</div><p class="why">철학을 일과 판단에 쓰는 도구로 소개한다</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">자기계발</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%B2%A0%ED%95%99%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%82%B6%EC%9D%98%20%EB%AC%B4%EA%B8%B0%EA%B0%80%20%EB%90%98%EB%8A%94%EA%B0%80">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%B2%A0%ED%95%99%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%82%B6%EC%9D%98%20%EB%AC%B4%EA%B8%B0%EA%B0%80%20%EB%90%98%EB%8A%94%EA%B0%80">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%B2%A0%ED%95%99%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%82%B6%EC%9D%98%20%EB%AC%B4%EA%B8%B0%EA%B0%80%20%EB%90%98%EB%8A%94%EA%B0%80">알라딘</a></div></div></article><article class="book g-inmun g-social a-N a-F" style="--i:51;--hN:1;--hF:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>어떻게 살 것인가</h4><div class="meta">유시민 · 생각의길</div><p class="why">삶과 죽음, 사회를 하나의 질문으로 엮은 에세이</p><div class="tags"><span class="tag">인문·철학</span><span class="tag">사회·정치</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%82%B4%20%EA%B2%83%EC%9D%B8%EA%B0%80">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%82%B4%20%EA%B2%83%EC%9D%B8%EA%B0%80">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%82%B4%20%EA%B2%83%EC%9D%B8%EA%B0%80">알라딘</a></div></div></article><article class="book g-econ g-self a-T a-J" style="--i:52;--hT:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>부의 추월차선</h4><div class="meta">MJ 드마코 · 토트</div><p class="why">시간과 소득 구조를 다시 짜보게 하는 직설적인 책</p><div class="tags"><span class="tag">경제·경영</span><span class="tag">자기계발</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%B6%80%EC%9D%98%20%EC%B6%94%EC%9B%94%EC%B0%A8%EC%84%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%B6%80%EC%9D%98%20%EC%B6%94%EC%9B%94%EC%B0%A8%EC%84%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%B6%80%EC%9D%98%20%EC%B6%94%EC%9B%94%EC%B0%A8%EC%84%A0">알라딘</a></div></div></article><article class="book g-econ g-self a-S a-J" style="--i:53;--hS:1;--hJ:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>부자 아빠 가난한 아빠</h4><div class="meta">로버트 기요사키 · 민음인</div><p class="why">자산과 부채를 보는 기본 관점을 쉽게 잡아준다</p><div class="tags"><span class="tag">경제·경영</span><span class="tag">자기계발</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%B6%80%EC%9E%90%20%EC%95%84%EB%B9%A0%20%EA%B0%80%EB%82%9C%ED%95%9C%20%EC%95%84%EB%B9%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%B6%80%EC%9E%90%20%EC%95%84%EB%B9%A0%20%EA%B0%80%EB%82%9C%ED%95%9C%20%EC%95%84%EB%B9%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%B6%80%EC%9E%90%20%EC%95%84%EB%B9%A0%20%EA%B0%80%EB%82%9C%ED%95%9C%20%EC%95%84%EB%B9%A0">알라딘</a></div></div></article><article class="book g-self a-E a-S a-F" style="--i:54;--hE:1;--hS:1;--hF:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>데일 카네기 인간관계론</h4><div class="meta">데일 카네기 · 현대지성</div><p class="why">사람을 대하는 태도를 사례로 정리한 고전</p><div class="tags"><span class="tag">자기계발</span><span class="tag hit ctag c-E">E · 대화거리가 되는 책</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%8D%B0%EC%9D%BC%20%EC%B9%B4%EB%84%A4%EA%B8%B0%20%EC%9D%B8%EA%B0%84%EA%B4%80%EA%B3%84%EB%A1%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%8D%B0%EC%9D%BC%20%EC%B9%B4%EB%84%A4%EA%B8%B0%20%EC%9D%B8%EA%B0%84%EA%B4%80%EA%B3%84%EB%A1%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%8D%B0%EC%9D%BC%20%EC%B9%B4%EB%84%A4%EA%B8%B0%20%EC%9D%B8%EA%B0%84%EA%B4%80%EA%B3%84%EB%A1%A0">알라딘</a></div></div></article><article class="book g-self g-econ a-N a-T" style="--i:55;--hN:1;--hT:1"><div class="spine">KDC 300<span>사회과학</span></div><div class="bbody"><h4>역행자</h4><div class="meta">자청 · 웅진지식하우스</div><p class="why">변화를 단계별로 설계해 보는 자기계발서</p><div class="tags"><span class="tag">자기계발</span><span class="tag">경제·경영</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%97%AD%ED%96%89%EC%9E%90">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%97%AD%ED%96%89%EC%9E%90">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%97%AD%ED%96%89%EC%9E%90">알라딘</a></div></div></article><article class="book g-art g-essay a-I a-N a-F" style="--i:56;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 600<span>예술</span></div><div class="bbody"><h4>빈센트 반 고흐 영혼의 편지</h4><div class="meta">빈센트 반 고흐 · 위즈덤하우스</div><p class="why">편지로 읽는 화가의 내면과 작업 이야기</p><div class="tags"><span class="tag">예술</span><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%B9%88%EC%84%BC%ED%8A%B8%20%EB%B0%98%20%EA%B3%A0%ED%9D%90%20%EC%98%81%ED%98%BC%EC%9D%98%20%ED%8E%B8%EC%A7%80">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%B9%88%EC%84%BC%ED%8A%B8%20%EB%B0%98%20%EA%B3%A0%ED%9D%90%20%EC%98%81%ED%98%BC%EC%9D%98%20%ED%8E%B8%EC%A7%80">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%B9%88%EC%84%BC%ED%8A%B8%20%EB%B0%98%20%EA%B3%A0%ED%9D%90%20%EC%98%81%ED%98%BC%EC%9D%98%20%ED%8E%B8%EC%A7%80">알라딘</a></div></div></article><article class="book g-essay a-I a-F" style="--i:57;--hI:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>숨결이 바람 될 때</h4><div class="meta">폴 칼라니티 · 흐름출판</div><p class="why">의사이자 환자였던 저자가 남긴 삶의 기록</p><div class="tags"><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%88%A8%EA%B2%B0%EC%9D%B4%20%EB%B0%94%EB%9E%8C%20%EB%90%A0%20%EB%95%8C">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%88%A8%EA%B2%B0%EC%9D%B4%20%EB%B0%94%EB%9E%8C%20%EB%90%A0%20%EB%95%8C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%88%A8%EA%B2%B0%EC%9D%B4%20%EB%B0%94%EB%9E%8C%20%EB%90%A0%20%EB%95%8C">알라딘</a></div></div></article><article class="book g-essay a-I a-P" style="--i:58;--hI:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>여행의 이유</h4><div class="meta">김영하 · 문학동네</div><p class="why">여행을 통해 일상을 다시 보는 산문집</p><div class="tags"><span class="tag">에세이</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%97%AC%ED%96%89%EC%9D%98%20%EC%9D%B4%EC%9C%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%97%AC%ED%96%89%EC%9D%98%20%EC%9D%B4%EC%9C%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%97%AC%ED%96%89%EC%9D%98%20%EC%9D%B4%EC%9C%A0">알라딘</a></div></div></article><article class="book g-knovel a-F" style="--i:59;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>모순</h4><div class="meta">양귀자 · 쓰다</div><p class="why">두 자매의 삶으로 인생의 모순을 묻는 소설</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%AA%A8%EC%88%9C">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%AA%A8%EC%88%9C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%AA%A8%EC%88%9C">알라딘</a></div></div></article><article class="book g-sf g-knovel a-N a-F" style="--i:60;--hN:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>지구 끝의 온실</h4><div class="meta">김초엽 · 자이언트북스</div><p class="why">재난 이후의 세계에서 식물과 사람이 이어지는 이야기</p><div class="tags"><span class="tag">SF·장르</span><span class="tag">한국소설</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%A7%80%EA%B5%AC%20%EB%81%9D%EC%9D%98%20%EC%98%A8%EC%8B%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%A7%80%EA%B5%AC%20%EB%81%9D%EC%9D%98%20%EC%98%A8%EC%8B%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%A7%80%EA%B5%AC%20%EB%81%9D%EC%9D%98%20%EC%98%A8%EC%8B%A4">알라딘</a></div></div></article><article class="book g-knovel a-N a-F" style="--i:61;--hN:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>시선으로부터,</h4><div class="meta">정세랑 · 문학동네</div><p class="why">한 가족의 여러 세대를 경쾌하게 엮은 장편</p><div class="tags"><span class="tag">한국소설</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%8B%9C%EC%84%A0%EC%9C%BC%EB%A1%9C%EB%B6%80%ED%84%B0%2C">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%8B%9C%EC%84%A0%EC%9C%BC%EB%A1%9C%EB%B6%80%ED%84%B0%2C">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%8B%9C%EC%84%A0%EC%9C%BC%EB%A1%9C%EB%B6%80%ED%84%B0%2C">알라딘</a></div></div></article><article class="book g-wnovel g-history a-S a-F" style="--i:62;--hS:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>파친코</h4><div class="meta">이민진 · 문학사상</div><p class="why">재일 한인 가족의 4대를 따라가는 대하소설</p><div class="tags"><span class="tag">해외소설</span><span class="tag">역사</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%8C%8C%EC%B9%9C%EC%BD%94">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%8C%8C%EC%B9%9C%EC%BD%94">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%8C%8C%EC%B9%9C%EC%BD%94">알라딘</a></div></div></article><article class="book g-wnovel a-I a-N a-F" style="--i:63;--hI:1;--hN:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>어린 왕자</h4><div class="meta">앙투안 드 생텍쥐페리 · 열린책들</div><p class="why">짧지만 읽는 나이마다 다르게 닿는 이야기</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%96%B4%EB%A6%B0%20%EC%99%95%EC%9E%90">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%96%B4%EB%A6%B0%20%EC%99%95%EC%9E%90">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%96%B4%EB%A6%B0%20%EC%99%95%EC%9E%90">알라딘</a></div></div></article><article class="book g-wnovel a-I a-N a-P" style="--i:64;--hI:1;--hN:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>호밀밭의 파수꾼</h4><div class="meta">J. D. 샐린저 · 민음사</div><p class="why">세상과 어긋난 청춘의 목소리</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%98%B8%EB%B0%80%EB%B0%AD%EC%9D%98%20%ED%8C%8C%EC%88%98%EA%BE%BC">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%98%B8%EB%B0%80%EB%B0%AD%EC%9D%98%20%ED%8C%8C%EC%88%98%EA%BE%BC">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%98%B8%EB%B0%80%EB%B0%AD%EC%9D%98%20%ED%8C%8C%EC%88%98%EA%BE%BC">알라딘</a></div></div></article><article class="book g-wnovel a-F" style="--i:65;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>앵무새 죽이기</h4><div class="meta">하퍼 리 · 열린책들</div><p class="why">아이의 눈으로 정의와 편견을 묻는 소설</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%95%B5%EB%AC%B4%EC%83%88%20%EC%A3%BD%EC%9D%B4%EA%B8%B0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%95%B5%EB%AC%B4%EC%83%88%20%EC%A3%BD%EC%9D%B4%EA%B8%B0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%95%B5%EB%AC%B4%EC%83%88%20%EC%A3%BD%EC%9D%B4%EA%B8%B0">알라딘</a></div></div></article><article class="book g-wnovel a-S a-F" style="--i:66;--hS:1;--hF:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>위대한 개츠비</h4><div class="meta">F. 스콧 피츠제럴드 · 민음사</div><p class="why">욕망과 계급의 화려한 몰락을 그린 고전</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-S">S · 사례와 사실이 단단한 책</span><span class="tag hit ctag c-F">F · 사람과 의미에 닿는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%9C%84%EB%8C%80%ED%95%9C%20%EA%B0%9C%EC%B8%A0%EB%B9%84">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%9C%84%EB%8C%80%ED%95%9C%20%EA%B0%9C%EC%B8%A0%EB%B9%84">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%9C%84%EB%8C%80%ED%95%9C%20%EA%B0%9C%EC%B8%A0%EB%B9%84">알라딘</a></div></div></article><article class="book g-wnovel a-I a-J" style="--i:67;--hI:1;--hJ:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>노인과 바다</h4><div class="meta">어니스트 헤밍웨이 · 민음사</div><p class="why">짧은 문장으로 패배 속의 품위를 그린다</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%85%B8%EC%9D%B8%EA%B3%BC%20%EB%B0%94%EB%8B%A4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%85%B8%EC%9D%B8%EA%B3%BC%20%EB%B0%94%EB%8B%A4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%85%B8%EC%9D%B8%EA%B3%BC%20%EB%B0%94%EB%8B%A4">알라딘</a></div></div></article><article class="book g-wnovel a-I a-N a-P" style="--i:68;--hI:1;--hN:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>변신</h4><div class="meta">프란츠 카프카 · 민음사</div><p class="why">어느 날 벌레가 된 사람의 소외를 그린 중편</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%B3%80%EC%8B%A0">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%B3%80%EC%8B%A0">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%B3%80%EC%8B%A0">알라딘</a></div></div></article><article class="book g-wnovel a-N a-P" style="--i:69;--hN:1;--hP:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>그리스인 조르바</h4><div class="meta">니코스 카잔자키스 · 열린책들</div><p class="why">책으로 사는 사람과 몸으로 사는 사람의 만남</p><div class="tags"><span class="tag">해외소설</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-P">P · 낯선 시선을 열어주는 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EA%B7%B8%EB%A6%AC%EC%8A%A4%EC%9D%B8%20%EC%A1%B0%EB%A5%B4%EB%B0%94">교보</a><a href="https://www.yes24.com/Product/Search?query=%EA%B7%B8%EB%A6%AC%EC%8A%A4%EC%9D%B8%20%EC%A1%B0%EB%A5%B4%EB%B0%94">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EA%B7%B8%EB%A6%AC%EC%8A%A4%EC%9D%B8%20%EC%A1%B0%EB%A5%B4%EB%B0%94">알라딘</a></div></div></article><article class="book g-sf g-wnovel a-N a-T" style="--i:70;--hN:1;--hT:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>삼체</h4><div class="meta">류츠신 · 자음과모음</div><p class="why">문명 사이의 충돌을 과학적 상상으로 밀어붙인다</p><div class="tags"><span class="tag">SF·장르</span><span class="tag">해외소설</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%82%BC%EC%B2%B4">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%82%BC%EC%B2%B4">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%82%BC%EC%B2%B4">알라딘</a></div></div></article><article class="book g-sf g-wnovel a-N a-T a-J" style="--i:71;--hN:1;--hT:1;--hJ:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>듄</h4><div class="meta">프랭크 허버트 · 황금가지</div><p class="why">생태와 정치, 종교가 얽힌 SF 대서사</p><div class="tags"><span class="tag">SF·장르</span><span class="tag">해외소설</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EB%93%84">교보</a><a href="https://www.yes24.com/Product/Search?query=%EB%93%84">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EB%93%84">알라딘</a></div></div></article><article class="book g-sf a-I a-N a-T" style="--i:72;--hI:1;--hN:1;--hT:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>안드로이드는 전기양을 꿈꾸는가?</h4><div class="meta">필립 K. 딕 · 황금가지</div><p class="why">무엇이 인간을 인간이게 하는지 묻는 SF</p><div class="tags"><span class="tag">SF·장르</span><span class="tag hit ctag c-I">I · 혼자 깊게 파고드는 책</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%EC%95%88%EB%93%9C%EB%A1%9C%EC%9D%B4%EB%93%9C%EB%8A%94%20%EC%A0%84%EA%B8%B0%EC%96%91%EC%9D%84%20%EA%BF%88%EA%BE%B8%EB%8A%94%EA%B0%80%3F">교보</a><a href="https://www.yes24.com/Product/Search?query=%EC%95%88%EB%93%9C%EB%A1%9C%EC%9D%B4%EB%93%9C%EB%8A%94%20%EC%A0%84%EA%B8%B0%EC%96%91%EC%9D%84%20%EA%BF%88%EA%BE%B8%EB%8A%94%EA%B0%80%3F">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%EC%95%88%EB%93%9C%EB%A1%9C%EC%9D%B4%EB%93%9C%EB%8A%94%20%EC%A0%84%EA%B8%B0%EC%96%91%EC%9D%84%20%EA%BF%88%EA%BE%B8%EB%8A%94%EA%B0%80%3F">알라딘</a></div></div></article><article class="book g-sf a-N a-T a-J" style="--i:73;--hN:1;--hT:1;--hJ:1"><div class="spine">KDC 800<span>문학</span></div><div class="bbody"><h4>파운데이션</h4><div class="meta">아이작 아시모프 · 황금가지</div><p class="why">역사를 수학으로 예측하려는 SF 고전</p><div class="tags"><span class="tag">SF·장르</span><span class="tag hit ctag c-N">N · 큰 그림과 관점을 주는 책</span><span class="tag hit ctag c-T">T · 논리와 구조가 선명한 책</span><span class="tag hit ctag c-J">J · 완결된 체계를 갖춘 책</span></div><div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=%ED%8C%8C%EC%9A%B4%EB%8D%B0%EC%9D%B4%EC%85%98">교보</a><a href="https://www.yes24.com/Product/Search?query=%ED%8C%8C%EC%9A%B4%EB%8D%B0%EC%9D%B4%EC%85%98">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=%ED%8C%8C%EC%9A%B4%EB%8D%B0%EC%9D%B4%EC%85%98">알라딘</a></div></div></article></div></div>
      </div>
    </div>
  </div>
  <div class="evs" id="ns-ev" style="margin-top:36px">
    <div class="sechead"><h3>이벤트 모음</h3><span class="status">마감 임박 순 · 2026년 10월 7일 기준</span></div>
    <div class="chips"><input class="vh" type="radio" name="src" id="s-all" checked><label class="chip" for="s-all">전체</label><input class="vh" type="radio" name="src" id="s-aladin"><label class="chip" for="s-aladin">알라딘</label><input class="vh" type="radio" name="src" id="s-yes24"><label class="chip" for="s-yes24">예스24</label><input class="vh" type="radio" name="src" id="s-minum"><label class="chip" for="s-minum">민음사</label></div>
    <div class="evlist"><div class="ev e-yes24"><div class="due"><small>마감</small><b>~10.11</b></div><div><h4><span class="src">예스24</span>경제경영 보너스 데이</h4><p>매일 선착순 1천 원 상품권</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~10.12</b></div><div><h4><span class="src">알라딘</span>『잘 살 궁리』 신간 알림 신청</h4><p>추첨으로 적립금 1천 원, 10월 13일 발표</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-minum"><div class="due"><small>마감</small><b>~10.14</b></div><div><h4><span class="src">민음사</span>10월, 오늘의 젊은 독자단 모집</h4><p>민음북클럽 독자단 모집</p></div><a class="go" href="https://minumsa.com/event/41950/">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~10.20</b></div><div><h4><span class="src">알라딘</span>100일 습관 노트 · 김종원 작가 상담소</h4><p>도서 구매 시 참여, 10월 20일 당첨자 발표</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~10.23</b></div><div><h4><span class="src">알라딘</span>『호신술 클럽』 출간 기념 북토크</h4><p>10월 27일(화) 오후 7시 북토크 참여 신청</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-yes24"><div class="due"><small>마감</small><b>~10.26</b></div><div><h4><span class="src">예스24</span>경복궁 키캡 키링</h4><p>굿즈 이벤트</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-yes24"><div class="due"><small>마감</small><b>~10.30</b></div><div><h4><span class="src">예스24</span>무라카미 하루키 신간 예약판매</h4><p>예약 구매 시 블랙 롱머그 증정</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~10.31</b></div><div><h4><span class="src">알라딘</span>『미스테리아』 65호 할인쿠폰</h4><p>1천 원 할인쿠폰</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-yes24"><div class="due"><small>마감</small><b>~10.31</b></div><div><h4><span class="src">예스24</span>한글날 100주년 기획전</h4><p>한국어·한글 주제 도서 기획전</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-minum"><div class="due"><small>마감</small><b>~10.31</b></div><div><h4><span class="src">민음사</span>2026 세계문학 일력</h4><p>매일 한 문장 세계문학 일력</p></div><a class="go" href="https://minumsa.com/event/40925/">이벤트 보기 →</a></div><div class="ev e-yes24"><div class="due"><small>마감</small><b>~11.05</b></div><div><h4><span class="src">예스24</span>박성준 작가에게 묻다</h4><p>작가와 질문·답변 이벤트</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-yes24"><div class="due"><small>마감</small><b>~11.09</b></div><div><h4><span class="src">예스24</span>가을 그림책 기획전</h4><p>계절 그림책 모음</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~11.20</b></div><div><h4><span class="src">알라딘</span>『엄마의 무릎 성경』 아메리카노 추첨</h4><p>커피 기프티콘 추첨, 11월 27일 발표</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-minum"><div class="due"><small>마감</small><b>~11.22</b></div><div><h4><span class="src">민음사</span>예술의전당 토월정통연극 할인</h4><p>민음사 멤버십 15% 할인</p></div><a class="go" href="https://minumsa.com/event/41905/">이벤트 보기 →</a></div><div class="ev e-minum"><div class="due"><small>마감</small><b>~12.03</b></div><div><h4><span class="src">민음사</span>민음사 × 국립심포니오케스트라</h4><p>멤버십 공연 할인</p></div><a class="go" href="https://minumsa.com/event/41010/">이벤트 보기 →</a></div><div class="ev e-yes24"><div class="due"><small>마감</small><b>~12.15</b></div><div><h4><span class="src">예스24</span>NEXT PAGE</h4><p>대학생·취업준비생 대상 도서 프로그램</p></div><a class="go" href="https://event.yes24.com/">이벤트 보기 →</a></div><div class="ev e-minum"><div class="due"><small>마감</small><b>~12.31</b></div><div><h4><span class="src">민음사</span>세계문학전집 앱 출시</h4><p>세계문학전집 앱 이용</p></div><a class="go" href="https://minumsa.com/event/41534/">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~01.06</b></div><div><h4><span class="src">알라딘</span>『노화 격파』 챌린지 플래너</h4><p>노화 역행 4주 챌린지 플래너 증정</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due"><small>마감</small><b>~01.06</b></div><div><h4><span class="src">알라딘</span>『안식월 일기』 캐리어 키링</h4><p>한정판 캐리어 키링 증정</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-aladin"><div class="due long"><small>상시</small><b>—</b></div><div><h4><span class="src">알라딘</span>『서늘한 대화』 정재승 사인본 · 강연회 초대</h4><p>저자 사인 인쇄본, 출간 기념 강연회 초대</p></div><a class="go" href="https://www.aladin.co.kr/events/wevent_sub.aspx">이벤트 보기 →</a></div><div class="ev e-minum"><div class="due long"><small>상시</small><b>—</b></div><div><h4><span class="src">민음사</span>《한편》 뉴스레터 구독</h4><p>인문잡지 뉴스레터</p></div><a class="go" href="https://minumsa.com/event/32747/">이벤트 보기 →</a></div></div>
    <p class="note">혜택과 기간은 바뀔 수 있으니 참여 전에 원문을 확인하세요.</p>
  </div>
</div>
<script>
const KDC={"100":"철학","300":"사회과학","400":"자연과학","600":"예술","800":"문학","900":"역사"};
const GENRES=[["inmun","인문·철학"],["social","사회·정치"],["history","역사"],["science","과학"],["econ","경제·경영"],["psych","심리"],["self","자기계발"],["knovel","한국소설"],["wnovel","해외소설"],["sf","SF·장르"],["essay","에세이"],["art","예술"]];
const GL=Object.fromEntries(GENRES);
// title|author|publisher|kdc|genres|affinity letters|keywords|why
const RAW=`사피엔스|유발 하라리|김영사|900|history,inmun|NT|인류,문명,큰그림,역사|인류사 전체를 하나의 이야기로 꿰는 거대한 설명
총 균 쇠|재레드 다이아몬드|문학사상|900|history,science|NTJ|문명,지리,인류,역사|왜 어떤 문명이 앞서갔는지 환경과 지리로 답한다
정의란 무엇인가|마이클 샌델|와이즈베리|100|inmun,social|EN|정의,토론,윤리,철학|사례마다 내 판단을 시험하게 하는 토론형 철학
공정하다는 착각|마이클 샌델|와이즈베리|300|social,inmun|NF|능력주의,공정,불평등,사회|능력주의가 어떻게 사람을 갈라놓는지 짚는다
피로사회|한병철|문학과지성사|300|inmun,social|IN|피로,성과,현대사회,철학|짧고 밀도 높은 현대인 진단서
미움받을 용기|기시미 이치로·고가 후미타케|인플루엔셜|100|psych,inmun|F|관계,자유,심리,대화|대화체로 읽는 아들러 심리학
죽음의 수용소에서|빅터 프랭클|청아출판사|100|psych,inmun|IF|의미,고통,삶,심리|극한 상황에서 붙잡은 삶의 의미
팩트풀니스|한스 로슬링 외|김영사|300|social,science|ST|데이터,통계,세계,편견|데이터로 세계를 다시 보는 법
넛지|리처드 탈러·캐스 선스타인|리더스북|300|econ,psych|T|행동경제,선택,설계,경제|사람의 선택을 설계하는 행동경제학
생각에 관한 생각|대니얼 카너먼|김영사|100|psych,science|INT|인지,편향,사고,심리|직관과 이성이 어떻게 엇갈리는지 실험으로 보여준다
이기적 유전자|리처드 도킨스|을유문화사|400|science|INT|진화,유전자,생물,과학|진화를 유전자의 눈으로 다시 쓴 고전
코스모스|칼 세이건|사이언스북스|400|science|NF|우주,과학,경이,인류|과학이 주는 경이를 문학처럼 전한다
물고기는 존재하지 않는다|룰루 밀러|곰출판|400|science,essay|INF|분류,상실,질서,과학|과학 논픽션과 회고록이 겹쳐지는 책
열두 발자국|정재승|어크로스|400|science,psych|EN|뇌,선택,창의,과학|뇌과학으로 보는 선택과 창의성
도둑맞은 집중력|요한 하리|어크로스|300|social,psych|NP|집중,기술,현대사회,심리|집중력 위기를 개인이 아닌 구조의 문제로 본다
침묵의 봄|레이첼 카슨|에코리브르|400|science,social|IFJ|환경,생태,고발,과학|환경운동의 출발점이 된 고발서
돈의 심리학|모건 하우절|인플루엔셜|300|econ|SJ|돈,투자,습관,경제|숫자보다 태도로 다루는 돈 이야기
아주 작은 습관의 힘|제임스 클리어|비즈니스북스|300|self|SJ|습관,실행,루틴,성장|작은 시스템으로 행동을 바꾸는 실전서
원씽|게리 켈러·제이 파파산|비즈니스북스|300|self,econ|TJ|집중,우선순위,목표,성장|가장 중요한 한 가지를 고르는 우선순위 설계
그릿|앤절라 더크워스|비즈니스북스|100|psych,self|J|끈기,성장,열정,심리|재능보다 끈기를 연구한 심리학
사랑의 기술|에리히 프롬|문예출판사|100|inmun,psych|F|사랑,관계,철학,심리|사랑을 감정이 아닌 배워야 할 능력으로 본다
역사의 쓸모|최태성|다산초당|900|history|ESF|역사,인물,삶,교훈|역사 속 인물에게서 삶의 태도를 찾는다
거꾸로 읽는 세계사|유시민|돌베개|900|history,social|NT|근현대사,정치,역사,사회|근현대 세계사의 굵직한 사건을 다시 읽는다
지적 대화를 위한 넓고 얕은 지식|채사장|한빛비즈|300|inmun,social|EN|교양,경제,정치,철학|역사·경제·정치·윤리를 한 흐름으로 정리한다
시민의 교양|채사장|웨일북|300|social,inmun|EJ|세금,정치,국가,교양|세금과 국가, 정의를 시민의 눈으로 묻는다
군주론|니콜로 마키아벨리|까치|300|inmun,social|NTJ|권력,정치,리더십,고전|권력이 실제로 움직이는 방식을 냉정하게 기술한 고전
서양미술사|E. H. 곰브리치|예경|600|art,history|INP|미술,역사,감상,예술|미술의 흐름을 이야기로 따라가는 입문서
소년이 온다|한강|창비|800|knovel|IF|기억,폭력,애도,역사|1980년 광주를 여러 목소리로 증언하는 소설
작별하지 않는다|한강|문학동네|800|knovel|INF|기억,애도,우정,역사|제주 4·3의 기억을 끝까지 붙드는 소설
채식주의자|한강|창비|800|knovel|INP|폭력,몸,거부,가족|한 사람의 거부를 세 개의 시선으로 그린 연작
82년생 김지영|조남주|민음사|800|knovel,social|SF|여성,일상,차별,가족|평범한 삶의 결에 새겨진 차별의 기록
아몬드|손원평|창비|800|knovel|F|감정,성장,공감,우정|감정을 느끼지 못하는 소년의 성장담
불편한 편의점|김호연|나무옆의자|800|knovel|ESF|위로,이웃,일상,따뜻함|편의점에 모인 사람들의 따뜻한 회복기
달러구트 꿈 백화점|이미예|팩토리나인|800|knovel,sf|ENFP|꿈,판타지,위로,상상|꿈을 사고파는 백화점 판타지
우리가 빛의 속도로 갈 수 없다면|김초엽|허블|800|sf,knovel|INF|SF,우주,그리움,소수자|다정하고 쓸쓸한 한국 SF 단편집
데미안|헤르만 헤세|민음사|800|wnovel|INF|성장,자아,내면,철학|자기 자신이 되어가는 길에 관한 고전
1984|조지 오웰|민음사|800|wnovel,sf|INTJ|감시,권력,디스토피아,자유|감시 사회를 그린 디스토피아 고전
멋진 신세계|올더스 헉슬리|소담출판사|800|wnovel,sf|NTP|디스토피아,쾌락,통제,자유|쾌락으로 통제되는 또 다른 디스토피아
이방인|알베르 카뮈|민음사|800|wnovel,inmun|ITP|부조리,실존,죽음,철학|부조리를 정면으로 보는 실존주의 소설
페스트|알베르 카뮈|민음사|800|wnovel|IFJ|재난,연대,실존,공동체|재난 속에서 연대를 택하는 사람들
이처럼 사소한 것들|클레어 키건|다산책방|800|wnovel|IF|양심,침묵,공동체,선택|짧고 조용하게 양심을 묻는 소설
프로젝트 헤일메리|앤디 위어|알에이치코리아|800|sf,wnovel|ENTP|과학,우주,문제해결,우정|과학으로 하나씩 문제를 푸는 우주 생존기
나미야 잡화점의 기적|히가시노 게이고|현대문학|800|wnovel,sf|F|위로,편지,시간,연결|시간을 건너오는 고민 상담 편지
용의자 X의 헌신|히가시노 게이고|현대문학|800|sf,wnovel|IT|추리,논리,헌신,트릭|논리와 헌신이 맞부딪치는 추리소설
언어의 온도|이기주|말글터|800|essay|ISF|말,관계,일상,감성|일상의 말에 담긴 온도를 기록한 산문
호모 데우스|유발 하라리|김영사|900|history,science|NT|미래,기술,인공지능,인류|데이터와 알고리즘이 인간을 어떻게 바꿀지 내다본다
안네의 일기|안네 프랑크|문학사상|900|history,essay|IF|전쟁,일기,성장,기록|은신처에서 쓴 소녀의 일기, 전쟁을 개인의 목소리로 읽는다
우리는 왜 잠을 자야 할까|매슈 워커|열린책들|400|science|ST|수면,뇌,건강,과학|수면 과학으로 하루의 쓸모를 다시 계산해 보게 한다
랩 걸|호프 자런|알마|400|science,essay|INF|식물,과학자,여성,성장|식물학자의 연구실 이야기와 성장 회고가 함께 흐른다
설득의 심리학|로버트 치알디니|21세기북스|300|psych,econ|ET|설득,영향력,심리,마케팅|사람이 왜 '예'라고 말하는지 여섯 원칙으로 푼다
철학은 어떻게 삶의 무기가 되는가|야마구치 슈|다산초당|100|inmun,self|ST|철학,비즈니스,사고,교양|철학을 일과 판단에 쓰는 도구로 소개한다
어떻게 살 것인가|유시민|생각의길|300|inmun,social|NF|삶,죽음,태도,철학|삶과 죽음, 사회를 하나의 질문으로 엮은 에세이
부의 추월차선|MJ 드마코|토트|300|econ,self|TJ|부,사업,시간,경제|시간과 소득 구조를 다시 짜보게 하는 직설적인 책
부자 아빠 가난한 아빠|로버트 기요사키|민음인|300|econ,self|SJ|돈,자산,금융교육,경제|자산과 부채를 보는 기본 관점을 쉽게 잡아준다
데일 카네기 인간관계론|데일 카네기|현대지성|300|self|ESF|관계,대화,호감,성장|사람을 대하는 태도를 사례로 정리한 고전
역행자|자청|웅진지식하우스|300|self,econ|NT|성장,변화,실행,자수성가|변화를 단계별로 설계해 보는 자기계발서
빈센트 반 고흐 영혼의 편지|빈센트 반 고흐|위즈덤하우스|600|art,essay|INF|편지,화가,고독,예술|편지로 읽는 화가의 내면과 작업 이야기
숨결이 바람 될 때|폴 칼라니티|흐름출판|800|essay|IF|죽음,삶,의사,의미|의사이자 환자였던 저자가 남긴 삶의 기록
여행의 이유|김영하|문학동네|800|essay|IP|여행,일상,사유,산문|여행을 통해 일상을 다시 보는 산문집
모순|양귀자|쓰다|800|knovel|F|삶,선택,사랑,쌍둥이|두 자매의 삶으로 인생의 모순을 묻는 소설
지구 끝의 온실|김초엽|자이언트북스|800|sf,knovel|NF|식물,재난,생태,공동체|재난 이후의 세계에서 식물과 사람이 이어지는 이야기
시선으로부터,|정세랑|문학동네|800|knovel|NF|가족,세대,여성,연대|한 가족의 여러 세대를 경쾌하게 엮은 장편
파친코|이민진|문학사상|800|wnovel,history|SF|이민,가족,역사,세대|재일 한인 가족의 4대를 따라가는 대하소설
어린 왕자|앙투안 드 생텍쥐페리|열린책들|800|wnovel|INF|관계,순수,어른,철학|짧지만 읽는 나이마다 다르게 닿는 이야기
호밀밭의 파수꾼|J. D. 샐린저|민음사|800|wnovel|INP|청춘,방황,자아,성장|세상과 어긋난 청춘의 목소리
앵무새 죽이기|하퍼 리|열린책들|800|wnovel|F|정의,편견,성장,인종|아이의 눈으로 정의와 편견을 묻는 소설
위대한 개츠비|F. 스콧 피츠제럴드|민음사|800|wnovel|SF|욕망,계급,사랑,허무|욕망과 계급의 화려한 몰락을 그린 고전
노인과 바다|어니스트 헤밍웨이|민음사|800|wnovel|IJ|도전,고독,품위,삶|짧은 문장으로 패배 속의 품위를 그린다
변신|프란츠 카프카|민음사|800|wnovel|INP|소외,가족,부조리,불안|어느 날 벌레가 된 사람의 소외를 그린 중편
그리스인 조르바|니코스 카잔자키스|열린책들|800|wnovel|NP|자유,삶,본능,철학|책으로 사는 사람과 몸으로 사는 사람의 만남
삼체|류츠신|자음과모음|800|sf,wnovel|NT|우주,문명,과학,생존|문명 사이의 충돌을 과학적 상상으로 밀어붙인다
듄|프랭크 허버트|황금가지|800|sf,wnovel|NTJ|생태,권력,정치,운명|생태와 정치, 종교가 얽힌 SF 대서사
안드로이드는 전기양을 꿈꾸는가?|필립 K. 딕|황금가지|800|sf|INT|인공지능,인간성,정체성,미래|무엇이 인간을 인간이게 하는지 묻는 SF
파운데이션|아이작 아시모프|황금가지|800|sf|NTJ|제국,미래,역사,예측|역사를 수학으로 예측하려는 SF 고전`;
const BOOKS=RAW.trim().split("\n").map(l=>{const[t,a,p,k,g,af,kw,w]=l.split("|");return{t,a,p,k,g:g.split(","),af,kw:kw.split(","),w}});

const AXES=[["E","I"],["S","N"],["T","F"],["J","P"]];
const LETTER={E:"대화거리가 되는 책",I:"혼자 깊게 파고드는 책",S:"사례와 사실이 단단한 책",N:"큰 그림과 관점을 주는 책",T:"논리와 구조가 선명한 책",F:"사람과 의미에 닿는 책",J:"완결된 체계를 갖춘 책",P:"낯선 시선을 열어주는 책"};
const PAIR={NT:["개념의 설계자","구조와 원리를 이해할 때 가장 즐거운 독자입니다. 세계를 설명하는 큰 이론, 논증이 촘촘한 책이 잘 맞습니다."],
NF:["의미를 찾는 독자","책에서 사람과 가치를 찾습니다. 삶의 방향을 묻는 인문서와 여운이 긴 소설이 오래 남습니다."],
ST:["사실을 쌓는 독자","검증된 사실과 쓸모를 중시합니다. 데이터와 사례가 풍부하고 바로 적용할 수 있는 책을 좋아합니다."],
SF:["이야기에 머무는 독자","구체적인 장면과 인물에게 마음이 갑니다. 일상의 결이 살아 있는 소설과 에세이가 잘 맞습니다."]};

const S={mbti:["I","N","T","J"],genres:new Set(["inmun","social"]),recent:"",liked:""};
try{const sv=JSON.parse(localStorage.getItem("seonghyang")||"null");if(sv){S.mbti=sv.mbti||S.mbti;S.genres=new Set(sv.genres||[]);S.recent=sv.recent||"";S.liked=sv.liked||""}}catch(e){}
const save=()=>{try{localStorage.setItem("seonghyang",JSON.stringify({mbti:S.mbti,genres:[...S.genres],recent:S.recent,liked:S.liked}))}catch(e){}};
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const norm=s=>String(s||"").replace(/[\s·.,!?'"《》「」『』<>]/g,"").toLowerCase();

/* MBTI control */
function renderMbti(){
  $("mbti").innerHTML=AXES.map((ax,i)=>`<div class="axis">${ax.map(l=>`<button type="button" data-i="${i}" data-l="${l}" aria-pressed="${S.mbti[i]===l}">${l}</button>`).join("")}</div>`).join("");
  const code=S.mbti.join("");$("typeCode").textContent=code;
  $("typeShort").textContent=PAIR[S.mbti[1]+S.mbti[2]][0];
}
$("mbti").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;S.mbti[+b.dataset.i]=b.dataset.l;renderMbti();recommend()});

function renderGenres(){
  $("genres").innerHTML=GENRES.map(([k,l])=>`<button type="button" class="chip" data-g="${k}" aria-pressed="${S.genres.has(k)}">${l}</button>`).join("");
}
$("genres").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;const g=b.dataset.g;S.genres.has(g)?S.genres.delete(g):S.genres.add(g);renderGenres();recommend()});

function renderProfile(){
  const code=S.mbti.join(""),pair=PAIR[S.mbti[1]+S.mbti[2]];
  $("profile").innerHTML=`<div class="code">${code}</div><h3>${pair[0]}</h3><p>${pair[1]} ${S.mbti[0]==="I"?"혼자 오래 곱씹을 수 있는":"읽고 나서 누군가와 이야기하고 싶은"} 책, ${S.mbti[3]==="J"?"끝까지 체계가 잡힌 구성":"생각의 방향을 틀어주는 새로운 관점"}을 우선했습니다.</p>`;
}

/* Scoring */
function findRecent(){
  const q=norm(S.recent);if(q.length<2)return null;
  return BOOKS.find(b=>norm(b.t)===q)||BOOKS.find(b=>norm(b.t).includes(q)||q.includes(norm(b.t)))||null;
}
function score(b,ref){
  let s=0;const why=[];
  const gm=b.g.filter(g=>S.genres.has(g));
  if(gm.length){s+=3+gm.length;why.push(`관심 분야 ${gm.map(g=>GL[g]).join("·")}`)}
  const am=[...b.af].filter(l=>S.mbti.includes(l));
  const opp=[...b.af].filter(l=>!S.mbti.includes(l)).length;s+=am.length*3-opp*1.5;
  if(am.length)why.push(am.map(l=>LETTER[l]).slice(0,2).join(", "));
  const liked=norm(S.liked);
  const kwHits=b.kw.filter(k=>(ref&&ref.kw.includes(k))||(liked&&liked.includes(norm(k))));
  if(ref){const gShare=b.g.filter(g=>ref.g.includes(g)).length;s+=gShare*1.5}
  s+=kwHits.length*2.5;
  if(kwHits.length)why.unshift(ref?`『${ref.t}』와 겹치는 주제: ${kwHits.join(", ")}`:`좋았던 점과 닿는 주제: ${kwHits.join(", ")}`);
  return{b,s,why,kwHits};
}
function bookCard(o,ai){
  const b=o.b, q=encodeURIComponent(b.t);
  return `<article class="book${ai?" ai":""}"><div class="spine">KDC ${esc(b.k||"—")}<span>${esc(KDC[b.k]||"")}</span></div>
  <div class="bbody"><h4>${esc(b.t)}</h4><div class="meta">${esc(b.a)}${b.p?" · "+esc(b.p):""}</div>
  <p class="why">${esc(b.w)}</p>
  ${o.why&&o.why.length?`<div class="tags">${o.why.map((w,i)=>`<span class="tag${i===0&&o.kwHits&&o.kwHits.length?" hit":""}">${esc(w)}</span>`).join("")}</div>`:""}
  <div class="links"><a href="https://search.kyobobook.co.kr/search?keyword=${q}" target="_blank" rel="noopener">교보</a><a href="https://www.yes24.com/Product/Search?query=${q}" target="_blank" rel="noopener">예스24</a><a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord=${q}" target="_blank" rel="noopener">알라딘</a></div>
  </div></article>`;
}
function recommend(){
  renderProfile();save();
  const ref=findRecent();
  const list=BOOKS.filter(b=>b!==ref).map(b=>score(b,ref)).sort((a,b)=>b.s-a.s||BOOKS.indexOf(a.b)-BOOKS.indexOf(b.b)).slice(0,8);
  $("books").innerHTML=list.map(o=>bookCard(o)).join("");
  let st=`${BOOKS.length}권 서가에서 ${list.length}권`;
  if(S.recent&&!ref)st+=` · 『${S.recent}』는 서가에 없어 성향과 분야로 골랐어요`;
  if(ref)st+=` · 『${ref.t}』 기준`;
  $("shelfStatus").textContent=st;
}
$("form").addEventListener("submit",e=>{e.preventDefault();S.recent=$("recent").value.trim();S.liked=$("liked").value.trim();recommend()});
$("recent").addEventListener("input",()=>{S.recent=$("recent").value.trim();save()});
$("liked").addEventListener("input",()=>{S.liked=$("liked").value.trim();save()});


/* Events */
const EVENTS=[
["알라딘","100일 습관 노트 · 김종원 작가 상담소","도서 구매 시 참여, 10월 20일 당첨자 발표","2026-10-07","2026-10-20","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『잘 살 궁리』 신간 알림 신청","추첨으로 적립금 1천 원, 10월 13일 발표","2026-10-06","2026-10-12","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『호신술 클럽』 출간 기념 북토크","10월 27일(화) 오후 7시 북토크 참여 신청","2026-10-06","2026-10-23","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『서늘한 대화』 정재승 사인본 · 강연회 초대","저자 사인 인쇄본, 출간 기념 강연회 초대","2026-10-06","","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『미스테리아』 65호 할인쿠폰","1천 원 할인쿠폰","2026-10-06","2026-10-31","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『엄마의 무릎 성경』 아메리카노 추첨","커피 기프티콘 추첨, 11월 27일 발표","2026-10-06","2026-11-20","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『노화 격파』 챌린지 플래너","노화 역행 4주 챌린지 플래너 증정","2026-10-06","2027-01-06","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["알라딘","『안식월 일기』 캐리어 키링","한정판 캐리어 키링 증정","2026-10-06","2027-01-06","https://www.aladin.co.kr/events/wevent_sub.aspx"],
["예스24","경제경영 보너스 데이","매일 선착순 1천 원 상품권","2026-10-02","2026-10-11","https://event.yes24.com/"],
["예스24","경복궁 키캡 키링","굿즈 이벤트","2026-10-06","2026-10-26","https://event.yes24.com/"],
["예스24","무라카미 하루키 신간 예약판매","예약 구매 시 블랙 롱머그 증정","2026-09-29","2026-10-30","https://event.yes24.com/"],
["예스24","한글날 100주년 기획전","한국어·한글 주제 도서 기획전","2026-09-29","2026-10-31","https://event.yes24.com/"],
["예스24","박성준 작가에게 묻다","작가와 질문·답변 이벤트","2026-10-02","2026-11-05","https://event.yes24.com/"],
["예스24","가을 그림책 기획전","계절 그림책 모음","2026-10-06","2026-11-09","https://event.yes24.com/"],
["예스24","NEXT PAGE","대학생·취업준비생 대상 도서 프로그램","2026-10-01","2026-12-15","https://event.yes24.com/"],
["민음사","10월, 오늘의 젊은 독자단 모집","민음북클럽 독자단 모집","2026-10-06","2026-10-14","https://minumsa.com/event/41950/"],
["민음사","2026 세계문학 일력","매일 한 문장 세계문학 일력","2026-01-08","2026-10-31","https://minumsa.com/event/40925/"],
["민음사","예술의전당 토월정통연극 할인","민음사 멤버십 15% 할인","2026-09-18","2026-11-22","https://minumsa.com/event/41905/"],
["민음사","민음사 × 국립심포니오케스트라","멤버십 공연 할인","2026-01-21","2026-12-03","https://minumsa.com/event/41010/"],
["민음사","세계문학전집 앱 출시","세계문학전집 앱 이용","2026-06-12","2026-12-31","https://minumsa.com/event/41534/"],
["민음사","《한편》 뉴스레터 구독","인문잡지 뉴스레터","2020-01-14","","https://minumsa.com/event/32747/"]
].map(([src,title,benefit,start,end,url])=>({src,title,benefit,start,end,url}));
const SRCS=["전체",...new Set(EVENTS.map(e=>e.src))];
let evSrc="전체";
try{evSrc=localStorage.getItem("seonghyang-ev")||"전체"}catch(e){}
function dday(end){if(!end)return null;const t=new Date();t.setHours(0,0,0,0);return Math.round((new Date(end+"T00:00:00")-t)/864e5)}
function renderEvents(){
  $("evFilter").innerHTML=SRCS.map(s=>`<button type="button" class="chip" data-s="${s}" aria-pressed="${s===evSrc}">${s}</button>`).join("");
  const list=EVENTS.filter(e=>evSrc==="전체"||e.src===evSrc).map(e=>({...e,d:dday(e.end)})).filter(e=>e.d===null||e.d>=0)
    .sort((a,b)=>(a.d??9999)-(b.d??9999));
  $("evCount").textContent=`진행 중 ${list.length}건 · 마감 임박 순`;
  $("evList").innerHTML=list.map(e=>{
    const md=e.end?e.end.slice(5).replace("-","."):"상시";
    const cls=e.d!==null&&e.d<=7?"soon":(e.d===null||e.d>60?"long":"");
    const label=e.d===null?"기한 없음":e.d===0?"오늘 마감":`D-${e.d}`;
    return `<div class="ev"><div class="due ${cls}"><small>${label}</small><b>~${md}</b></div>
    <div><h4><span class="src">${esc(e.src)}</span>${esc(e.title)}</h4><p>${esc(e.benefit)}</p></div>
    <a class="go" href="${e.url}" target="_blank" rel="noopener">이벤트 보기 →</a></div>`}).join("")||`<div class="empty">진행 중인 이벤트가 없어요.</div>`;
}
$("evFilter").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;evSrc=b.dataset.s;try{localStorage.setItem("seonghyang-ev",evSrc)}catch(_){}renderEvents()});

/* Tabs */
function showTab(t){
  document.querySelectorAll("nav.tabs button").forEach(b=>b.setAttribute("aria-selected",b.dataset.tab===t));
  $("pane-recommend").hidden=t!=="recommend";$("pane-events").hidden=t!=="events";
}
document.querySelector("nav.tabs").addEventListener("click",e=>{const b=e.target.closest("button");if(b)showTab(b.dataset.tab)});
if(location.hash==="#events")showTab("events");

$("recent").value=S.recent;$("liked").value=S.liked;
if(!S.recent){$("recent").value="공정하다는 착각";S.recent="공정하다는 착각"}
renderMbti();renderGenres();recommend();renderEvents();
document.documentElement.classList.add("js");
</script>
</body>
</html>

````
