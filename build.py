#!/usr/bin/env python3
"""data/ + src/template.html -> book-recommender.html (단일 파일, 외부 의존성 없음).

사용법:  python build.py          (기본: data/events.json의 asOf 기준)
         python build.py --check  (형식 검증만, 파일은 안 씀)
"""
import json, sys, datetime, pathlib, re
from urllib.parse import quote
from html import escape

ROOT = pathlib.Path(__file__).parent
GENRES = [("inmun","인문·철학"),("social","사회·정치"),("history","역사"),("science","과학"),("econ","경제·경영"),("psych","심리"),("self","자기계발"),("knovel","한국소설"),("wnovel","해외소설"),("sf","SF·장르"),("essay","에세이"),("art","예술")]
GL = dict(GENRES)
KDC = {"100":"철학","300":"사회과학","400":"자연과학","600":"예술","800":"문학","900":"역사"}
LETTER = {"E":"대화거리가 되는 책","I":"혼자 깊게 파고드는 책","S":"사례와 사실이 단단한 책","N":"큰 그림과 관점을 주는 책","T":"논리와 구조가 선명한 책","F":"사람과 의미에 닿는 책","J":"완결된 체계를 갖춘 책","P":"낯선 시선을 열어주는 책"}
SRC_KEY = {"알라딘":"aladin","예스24":"yes24","민음사":"minum"}

def load_books():
    books, seen = [], set()
    for n, line in enumerate((ROOT/"data/books.txt").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"): continue
        f = line.split("|")
        assert len(f) == 8, f"books.txt {n}행: 칸이 {len(f)}개 (8개여야 함): {line[:40]}"
        t,a,p,k,g,af,kw,w = f
        assert k in KDC, f"books.txt {n}행: KDC '{k}' 미등록"
        for x in g.split(","): assert x in GL, f"books.txt {n}행: 분야 '{x}' 미등록"
        assert af and set(af) <= set("EISNTFJP"), f"books.txt {n}행: 성향글자 '{af}' 오류"
        assert (t,a) not in seen, f"books.txt {n}행: 중복 {t}"
        seen.add((t,a))
        books.append(dict(raw=line, t=t,a=a,p=p,k=k,g=g.split(","),af=af,w=w))
    return books

def load_guides(books):
    titles = {b["t"] for b in books}
    out = {}
    for n, line in enumerate((ROOT/"data/guides.txt").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"): continue
        f = line.split("|")
        assert len(f) == 7, f"guides.txt {n}행: 칸이 {len(f)}개 (7개여야 함)"
        t, lv, sm, fw, ct, ev, url = f
        assert t in titles, f"guides.txt {n}행: books.txt에 없는 책 '{t}'"
        assert lv in ("쉬움","보통","어려움"), f"guides.txt {n}행: 난이도 '{lv}'"
        assert ev in ("후기","약함"), f"guides.txt {n}행: 근거 '{ev}'"
        assert t not in out, f"guides.txt {n}행: 중복 {t}"
        out[t] = dict(raw=line, lv=lv, sm=sm, fw=fw, ct=ct, ev=ev, url=url)
    return out

def guide_html(g):
    if not g: return ""
    weak = g["ev"] == "약함"
    link = f' · <a href="{escape(g["url"])}" target="_blank" rel="noopener">참고글</a>' if g["url"] else ""
    return (f'<details class="gd"><summary>읽기 가이드 · 난이도 {g["lv"]}</summary><p>{escape(g["sm"])}</p>'
            f'<p><b>이런 분께</b> {escape(g["fw"])}</p><p><b>주의</b> {escape(g["ct"])}</p>'
            f'<p class="gsrc"><span class="{"weak" if weak else ""}">{"근거 약함 · 검수 필요" if weak else "후기 기반 요약"}</span>{link}</p></details>')

def _n(s):
    return re.sub(r"[\s·.,!?'\"《》「」『』<>:\-—()]", "", s).lower()

def load_best(books):
    """data/bestsellers.json -> (dict, bmap). 서가 매칭: 정규화 제목이 같거나, 서가 제목(6자 이상)이 순위 제목에 포함."""
    d = json.loads((ROOT/"data/bestsellers.json").read_text(encoding="utf-8"))
    shelf = {_n(b["t"]): b["t"] for b in books}
    bmap = {}
    for sr in d["sources"]:
        seen = set()
        for it in sr["items"]:
            assert len(it) == 4 and isinstance(it[0], int), f"bestsellers.json: 형식 오류 {it}"
            assert it[0] not in seen, f"bestsellers.json: {sr['name']} {it[0]}위 중복"
            seen.add(it[0])
            nt = _n(it[1])
            hit = shelf.get(nt) or next((st for k, st in shelf.items() if len(k) >= 6 and k in nt), None)
            it.append(hit or "")
            if hit: bmap.setdefault(hit, []).append((sr["name"], it[0]))
    return d, bmap

def best_pts(rank):
    return 2 if rank <= 10 else 1.5 if rank <= 30 else 1

def best_label(lst):
    return "주간 베스트 · " + ", ".join(f"{s} {r}위" for s, r in lst)

def ns_best(d):
    out = ['<div class="sechead"><h3>주간 베스트</h3><span class="status">서점별 상위 30위 · 서가에 있는 책은 표시돼요</span></div>']
    for sr in d["sources"]:
        badge = '<span class="tag hit">서가에 있음</span> '
        rows = "".join(
            f'<div class="ev"><div class="due {"" if r <= 3 else "long"}"><small>주간</small><b>{r}위</b></div>'
            f'<div><h4>{badge if shelf else ""}{escape(t)}</h4><p>{escape(a)}{" · " + escape(p) if p else ""}</p></div>'
            f'<a class="go" href="https://search.kyobobook.co.kr/search?keyword={quote(t)}">교보 검색 →</a></div>'
            for r, t, a, p, shelf in sr["items"] if r <= 30)
        out.append(f'<p class="status" style="margin:14px 0 0"><b>{sr["name"]}</b> · {sr["period"]}</p><div class="evlist">{rows}</div>')
    return "".join(out)

def ns_book(i, b, g=None, bl=None):
    q = quote(b["t"])
    cls = " ".join(f"g-{g}" for g in b["g"]) + " " + " ".join(f"a-{l}" for l in b["af"])
    style = f"--i:{i};" + ";".join(f"--h{l}:1" for l in b["af"])
    if bl: style += f";--bb:{round(sum(best_pts(r) for _, r in bl) / 1.5, 2)}"
    tags = "".join(f'<span class="tag">{GL[g]}</span>' for g in b["g"]) + \
           "".join(f'<span class="tag hit ctag c-{l}">{l} · {LETTER[l]}</span>' for l in b["af"]) + \
           (f'<span class="tag hit">{best_label(bl)}</span>' if bl else "")
    return (f'<article class="book {cls}" style="{style}"><div class="spine">KDC {b["k"]}<span>{KDC[b["k"]]}</span></div>'
            f'<div class="bbody"><h4>{escape(b["t"])}</h4><div class="meta">{escape(b["a"])} · {escape(b["p"])}</div>'
            f'<p class="why">{escape(b["w"])}</p>{guide_html(g)}<div class="tags">{tags}</div>'
            f'<div class="links"><a href="https://search.kyobobook.co.kr/search?keyword={q}">교보</a>'
            f'<a href="https://www.yes24.com/Product/Search?query={q}">예스24</a>'
            f'<a href="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord={q}">알라딘</a></div></div></article>')

def ns_event(e):
    key = SRC_KEY[e["src"]]
    due = ('<div class="due long"><small>상시</small><b>—</b></div>' if not e["end"]
           else f'<div class="due"><small>마감</small><b>~{e["end"][5:].replace("-",".")}</b></div>')
    return (f'<div class="ev e-{key}">{due}<div><h4><span class="src">{e["src"]}</span>{escape(e["title"])}</h4>'
            f'<p>{escape(e["benefit"])}</p></div><a class="go" href="{e["url"]}">이벤트 보기 →</a></div>')

def main():
    books = load_books()
    guides = load_guides(books)
    best, bmap = load_best(books)
    ev =json.loads((ROOT/"data/events.json").read_text(encoding="utf-8"))
    asof = datetime.date.fromisoformat(ev["asOf"])
    for e in ev["events"]: assert e["src"] in SRC_KEY, f"이벤트 출처 '{e['src']}' 미등록 (build.py SRC_KEY + 템플릿 칩 추가 필요)"
    # 정적 버전은 빌드 시점(asOf) 기준으로 지난 이벤트를 걸러 마감순 정렬 (스크립트 버전은 열 때마다 계산)
    live = [e for e in ev["events"] if not e["end"] or e["end"] >= ev["asOf"]]
    live.sort(key=lambda e: e["end"] or "9999")
    if "--check" in sys.argv:
        print(f"베스트셀러 서가 매칭 {len(bmap)}권: " + ", ".join(f"{k}({best_label(v)})" for k, v in bmap.items()))
        print(f"OK 책 {len(books)}권 · 가이드 {len(guides)}권 · 이벤트 {len(ev['events'])}건 (표시 {len(live)}건)"); return
    t = (ROOT/"src/template.html").read_text(encoding="utf-8")
    t = t.replace("/*@BOOKS*/", "\n".join(b["raw"] for b in books))
    evjs = "\n".join(json.dumps([e["src"],e["title"],e["benefit"],e["start"],e["end"],e["url"]], ensure_ascii=False, separators=(",",":"))+"," for e in ev["events"])
    t = t.replace("/*@EVENTS*/[\n", "[\n" + evjs.rstrip(",") + "\n")
    t = t.replace("/*@GUIDES*/", "\n".join(g["raw"] for g in guides.values()))
    t = t.replace("/*@BEST*/{}", json.dumps({"asOf": best["asOf"], "sources": [{"name": s["name"], "period": s["period"], "items": s["items"]} for s in best["sources"]]}, ensure_ascii=False, separators=(",", ":")))
    t = t.replace("@@NS_BEST@@", ns_best(best))
    t = t.replace("@@BEST_NOTE@@", escape(best["note"]))
    t = t.replace("@@NS_BOOKS@@", "".join(ns_book(i,b,guides.get(b["t"]),bmap.get(b["t"])) for i,b in enumerate(books)))
    t = t.replace("@@NS_EVENTS@@", "".join(ns_event(e) for e in live))
    t = t.replace("@@ASOF@@", f"{asof.year}년 {asof.month}월 {asof.day}일")
    (ROOT/"book-recommender.html").write_text(t, encoding="utf-8", newline="\n")
    (ROOT/"docs").mkdir(exist_ok=True)  # GitHub Pages(/docs)용 사본
    (ROOT/"docs/index.html").write_text(t, encoding="utf-8", newline="\n")
    print(f"빌드 완료: 책 {len(books)}권, 이벤트 {len(live)}건, {len(t.encode())//1024}KB")

main()
