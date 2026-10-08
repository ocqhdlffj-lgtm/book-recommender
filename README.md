# 성향 서가

MBTI·관심 분야·최근 읽은 책으로 다음 책을 추천하고, 주간 베스트셀러와 서점·출판사 이벤트를 한곳에 보여주는 **단일 HTML 파일** 프로젝트입니다. 외부 API 없이 `book-recommender.html` 하나로 동작합니다.

## 구조
```
data/books.txt         책 목록 (제목|저자|출판사|KDC|분야|성향글자|키워드|설명)
data/guides.txt        책별 읽기 가이드 (난이도·후기 요약·근거)
data/bestsellers.json  주간 베스트셀러 (수동 갱신)
data/events.json       서점·출판사 이벤트
data/review-checklist.md  추가 도서 검수 목록
src/template.html      화면·스크립트 템플릿
build.py               위 데이터 + 템플릿 -> book-recommender.html
```

## 사용
```
python build.py          # book-recommender.html 생성
python build.py --check  # 데이터 형식만 검증
```
`book-recommender.html`은 생성물입니다. 데이터는 `data/`에서 고치세요. 자세한 설계·한계는 `book-recommender-handoff.md`를 참고하세요.

## 주의
- 출판사·성향글자 일부는 작성자의 기억과 휴리스틱이라 검수가 필요합니다(`data/review-checklist.md`).
- 읽기 가이드는 웹 검색 결과를 직접 요약한 것으로, `근거=약함` 항목은 검수 대상입니다.
