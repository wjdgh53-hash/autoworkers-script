from __future__ import annotations
"""대본 문체 검증 — 숫자 밀도·전문용어·친근함 장치를 기계로 측정한다.

사용법:
    .venv/bin/python scripts/src/check_tone.py <대본 경로> [--json]
    .venv/bin/python scripts/src/check_tone.py channels/{ch}/projects/{p}/_script/draft.md

왜 필요한가:
    숫자 밀도 기준(1,000자당 8개)은 2026-08-02부터 script-review-checklist.md에 있었다.
    그런데 70개 프로젝트 중 57개(81%)가 위반했다. 검사 주체가 에이전트 눈대중이라
    ① 등급이 "개선 권장"으로 깎이거나(changwon) ② 검사가 통째로 누락됐다(china-rice-cadmium).
    같은 기간 파이썬이 재는 분량 검증(validate_draft.py)은 70편 전부 준수했다.
    기준을 숫자로 적는 것만으로는 부족하고, 재는 주체가 기계여야 한다.

상한/하한 설계:
    상한(숫자·전문용어)만 FAIL로 막는다. 하한(감정어·비유·말걸기)은 WARN에 그친다.
    하한을 FAIL로 걸면 카운터를 채우려고 "뭉클"을 억지로 뿌리는 대본이 나온다.
    분량 검증은 이 문제가 없다 — 글자수는 채우려면 내용을 넣는 수밖에 없다. 문체는 다르다.
    친근함은 prompts/tone-guide.md의 대조쌍으로 만들고, 여기서는 확인만 한다.

기준값 교정 (모두 실측):
    상한은 "레퍼 히트작이 전부 통과하고 우리 최근작이 전부 실패하는" 선으로 잡았다.
    기준을 이론값으로 잡으면 레퍼 히트작(40,211뷰·194,112뷰)까지 FAIL이 떠서 게이트가 무의미해진다.

    | 지표          | 레퍼 히트 3편 | 우리 창원/쌀 | 채택 기준 |
    |---------------|--------------|-------------|-----------|
    | 숫자 밀도      | 5.9 7.4 9.7  | 19.8 21.8   | ≤ 10.0    |
    | 경제·행정 용어 | 0.4 0.7 0.9  | 3.4  3.5    | ≤ 1.5     |
    | 문장당 숫자 4+ | 0건 0건 0건   | 3건  7건    | 0건       |

    숫자 밀도 상한이 체크리스트의 기존 문구(8개)보다 느슨한 것은 의도적이다.
    정호님이 지목한 레퍼 원본이 9.7이다. 8로 조이면 그 대본도 실패 처리된다.

종료 코드:
    0 — 상한 항목 전부 통과 (하한 미달은 WARN이며 0을 반환한다)
    1 — 상한 항목 1개 이상 실패
    2 — 파일을 읽을 수 없거나 본문이 비어 있음
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── 측정 대상 ──────────────────────────────────────────────────
# 숫자 하나 = 사람이 "한 개의 수"로 듣는 단위.
# 만/억/조/천으로 이어진 자릿수는 하나로 묶는다 — "3만 5,000곳"은 두 개가 아니라 하나다.
# 묶지 않으면 "전국에 3만 5,000곳 넘게 있던 노래방이 지금은 2만 5,000곳입니다"가
# 숫자 4개로 잡혀 오탐이 난다(실제로는 두 개다).
# 대본은 큰 수를 한글로 풀어 쓰기도 하므로("이십팔만 대") 실제 체감 밀도는
# 여기서 세는 값보다 조금 높다. 기준선도 그 전제로 잡혀 있다.
_NUM_RE = re.compile(
    r"\d+(?:[.,]\d+)*(?:\s*[조억만천]\s*\d+(?:[.,]\d+)*)*(?:\s*[조억만천])?"
)

# 경제·행정 용어. tone-guide.md "용어 치환표"와 짝을 이룬다.
# "인수·매각·승인·당국"처럼 뉴스에서 흔히 쓰이는 말은 뺐다. 넣으면 레퍼 히트작도
# 걸려서 신호가 안 된다. 남긴 건 "우리 아버지가 이 단어를 아실까"에서 아니오인 것들이다.
_JARGON_RE = re.compile(
    r"(공시|지분|사모펀드|컨소시엄|규제당국|전략물자|조업단축|정규직|순손실|영업손실|수주|"
    r"연결\s?매출|부채비율|점유율|시행령|고시|조항|법령|의무수입|저율관세할당|국영무역|"
    r"주정용|가공용|단립종|중립종|장립종|코덱스|안전이용률|우선협상대상자|국가핵심기술|"
    r"수치제어장치|복합원재료|이관|인증서)"
)

# 친근함 장치 (하한 항목, WARN 전용)
_DEVICES = {
    "말 걸기": re.compile(
        r"(여러분|보고 계신|들고 계신|쓰고 계신|아십니까|아시나요|기억하시|하시죠|"
        r"보셨을 겁니다|들어는 보셨|하실 겁니다|하실 거예요)"
    ),
    "쉽게 풀어주기": re.compile(
        r"(쉽게 말|쉽게 풀|풀어 드리|풀어드리|풀어 볼|한 번 더 풀|다시 풀|"
        r"감이 잘|감이 안|와닿게|말씀드릴게요|무슨 말이냐|무슨 소리냐|무슨 뜻이냐)"
    ),
    "일상 비유": re.compile(
        r"(살림|가게|장바구니|밥상|월급|이자|달력|장롱|목수|고지서|통장|냉장고|"
        r"동네|아파트|집주인|숟가락|밥솥|빚쟁이|금고|장부|치면|셈이|비유)"
    ),
    "1인칭 리액션": re.compile(
        r"(저도 그랬|저는 좀|저도 처음|화가 나|얼떨떨|놀랐|믿기지|솔직히|"
        r"제가 |저는 |저도 |참 안타|참 딱)"
    ),
    "혼잣말 되받기": re.compile(r"(천만의 말씀|그건 아닙니다|사실과 다릅니다|반은 맞|글쎄요|아닙니다\.)"),
}

# 상한 — 넘으면 FAIL (레퍼 히트작 실측으로 교정. 모듈 docstring 표 참조)
_LIMITS = {"숫자 밀도": 10.0, "경제·행정 용어": 1.5}
# 하한 — 미달이면 WARN (16분 대본 ≈ 7,000자 기준 8회 → 1,000자당 약 1.1)
_FLOORS = {
    "말 걸기": 1.1,
    "쉽게 풀어주기": 1.1,
    "일상 비유": 1.1,
    "1인칭 리액션": 1.1,
    "혼잣말 되받기": 0.5,
}
# 한 문장 안 숫자 — 4개부터 FAIL. 3개로 조이면 레퍼의 모범 문장
# ("내 돈 1억으로 산 집에 빚이 3억 8천")까지 걸린다. 그건 비유지 나열이 아니다.
_SENT_NUM_LIMIT = 4

_SENT_SPLIT_RE = re.compile(r"(?<=[.?!])\s+")
_MD_HEADER_RE = re.compile(r"^#{1,6}\s+.*$", re.MULTILINE)
_MD_QUOTE_RE = re.compile(r"^>.*$", re.MULTILINE)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)


def load_body(path: Path) -> str:
    """대본 본문만 남긴다. draft.md의 헤더·주석·인용은 측정 대상이 아니다."""
    raw = path.read_text(encoding="utf-8")
    raw = _HTML_COMMENT_RE.sub("", raw)
    raw = _MD_HEADER_RE.sub("", raw)
    raw = _MD_QUOTE_RE.sub("", raw)
    return raw.strip()


def per_1k(count: int, chars: int) -> float:
    return round(count / chars * 1000, 1) if chars else 0.0


def find_number_clusters(body: str, window: int = 150, limit: int = 6) -> list[str]:
    """숫자가 좁은 구간에 몰린 자리를 찾는다 — 고칠 지점을 짚어주는 용도(WARN).

    문장 단위만 보면 "…7,917억이었어요. 3억 9,100만 유로에 그쳤어요."처럼
    짧은 문장으로 쪼개서 몰아넣는 경우를 놓친다. 그래서 글자 구간으로 본다.

    FAIL로 걸지 않는 이유: 레퍼 히트작도 3곳이 잡힌다. 숫자를 다른 숫자로 설명하는
    좋은 구간("200%만 넘어도 위험, 300%면 파산 직전")이 여기 걸리기 때문이다.
    실패 판정은 밀도와 문장 단위가 맡고, 이건 어디를 손볼지 알려주기만 한다.
    """
    positions = [m.start() for m in _NUM_RE.finditer(body)]
    hits, i = [], 0
    while i < len(positions):
        j = i
        while j + 1 < len(positions) and positions[j + 1] - positions[i] < window:
            j += 1
        if j - i + 1 >= limit:
            hits.append(body[positions[i] : positions[i] + window].replace("\n", " "))
            i = j + 1
        else:
            i += 1
    return hits


def find_number_heavy_sentences(body: str, limit: int = _SENT_NUM_LIMIT) -> list[str]:
    """한 문장에 숫자가 limit개 이상인 문장 — 기존 체크리스트 규칙의 기계 판정."""
    out = []
    for s in _SENT_SPLIT_RE.split(body):
        s = s.strip()
        if s and len(_NUM_RE.findall(s)) >= limit:
            out.append(s)
    return out


def analyze(path: Path) -> dict:
    body = load_body(path)
    chars = len(re.sub(r"\s", "", body))
    if chars == 0:
        raise ValueError(f"본문이 비어 있다: {path}")

    ceilings, floors = {}, {}
    for label, cap in _LIMITS.items():
        pat = _NUM_RE if label == "숫자 밀도" else _JARGON_RE
        v = per_1k(len(pat.findall(body)), chars)
        ceilings[label] = {"value": v, "limit": cap, "pass": v <= cap}
    for label, floor in _FLOORS.items():
        v = per_1k(len(_DEVICES[label].findall(body)), chars)
        floors[label] = {"value": v, "floor": floor, "pass": v >= floor}

    return {
        "path": str(path),
        "chars": chars,
        "ceilings": ceilings,
        "floors": floors,
        "clusters": find_number_clusters(body),
        "heavy_sentences": find_number_heavy_sentences(body),
    }


def report(r: dict) -> int:
    print(f"\n대본: {r['path']}  (공백 제외 {r['chars']:,}자)")
    print("\n── 상한 (넘으면 실패) " + "─" * 34)
    failed = 0
    for label, d in r["ceilings"].items():
        mark = "✅ PASS" if d["pass"] else "❌ FAIL"
        print(f"  {label:<14} {d['value']:>6.1f} / {d['limit']:>4.1f}   {mark}")
        if not d["pass"]:
            failed += 1

    print("\n── 하한 (미달이면 경고) " + "─" * 33)
    for label, d in r["floors"].items():
        mark = "✅" if d["pass"] else "⚠️  미달"
        print(f"  {label:<14} {d['value']:>6.1f} / {d['floor']:>4.1f}   {mark}")

    if r["heavy_sentences"]:
        failed += 1
        print(f"\n❌ 한 문장에 숫자 {_SENT_NUM_LIMIT}개 이상 — {len(r['heavy_sentences'])}건")
        for s in r["heavy_sentences"][:5]:
            print(f"     · {s[:80]}…")

    if r["clusters"]:
        print(f"\n⚠️  숫자가 150자 안에 6개 이상 몰린 구간 — {len(r['clusters'])}곳 (실패는 아니지만 손볼 자리)")
        for s in r["clusters"][:5]:
            print(f"     · {s[:80]}…")

    print()
    if failed:
        print(f"→ {failed}개 항목 실패. prompts/tone-guide.md의 대조쌍대로 고쳐 쓴다.")
        print("  숫자는 반올림하고, 퍼센트는 '몇 중에 몇'으로 바꾸고, 전문용어는 치환표대로 바꾼다.")
        return 1
    if any(not d["pass"] for d in r["floors"].values()):
        print("→ 상한은 통과. 다만 친근함 장치가 부족하다 (위 ⚠️ 항목).")
        print("  tone-guide.md §4를 보고 문장 단위로 보강한다. 단어만 뿌리지 않는다.")
        return 0
    print("→ 전 항목 통과.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="대본 문체 검증")
    ap.add_argument("script", help="draft.md 또는 script.txt 경로")
    ap.add_argument("--json", action="store_true", help="결과를 JSON으로 출력")
    args = ap.parse_args()

    path = Path(args.script)
    if not path.is_file():
        print(f"파일을 찾을 수 없다: {path}", file=sys.stderr)
        return 2
    try:
        r = analyze(path)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        ceil_fail = any(not d["pass"] for d in r["ceilings"].values())
        return 1 if (ceil_fail or r["heavy_sentences"]) else 0
    return report(r)


if __name__ == "__main__":
    sys.exit(main())
