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

# 한글로 쓴 수사도 청자에겐 똑같은 "숫자"다.
# 우리 대본은 TTS 규칙 때문에 큰 수를 한글로 적는다("백이십조", "마흔 명", "예순 개").
# 반면 레퍼는 유튜브 자동자막이라 아라비아 숫자다 → 아라비아만 세면 우리만 과소 측정된다.
# 실측: russia-nk-front-collapse는 아라비아만 세면 2.6인데 한글까지 세면 4.2였다.
# 단위·계수사가 뒤에 붙는 경우만 센다 — "구조", "사기", "한번"처럼 수사가 아닌 동음이의를 걸러야 한다.
_KO_UNIT = (
    r"(?:명|개|곳|대|기|발|번|해|달|년|월|일|배|가지|차례|만|억|조|원|톤|킬로|"
    r"퍼센트|프로|도|시간|분|초|권|척|편|줄|겹|판|채|살|평|자루|마리|사람|나라|군데)"
)
# ⚠️ 작은 고유어 수사(한/두/세/네/다섯~열)는 일부러 뺐다.
# "한 번 보시죠", "하나만 기억하세요", "한 사람이"는 수치가 아니라 일상 표현이고,
# 무엇보다 **"열 곳 중 세 곳"은 우리가 권장하는 형태**다(퍼센트→분수 치환, tone-guide §1③).
# 그걸 숫자로 세면 규칙을 잘 지킨 대본이 벌을 받는다.
# 세야 하는 건 "귀로 듣기 부담스러운 수치" — 만·억·조·백·천 규모와 스물 이상의 정확한 수다.
_KO_HEAD = r"(?:[일이삼사오육칠팔구]?[십백천]|스물|서른|마흔|쉰|예순|일흔|여든|아흔)"
# 머리 수사 + (자릿수 이어짐)* + [공백+단위 | 만·억·조].
# 단위 앞 공백을 필수로 둬서 "구조(구+조)", "사기(사+기)", "세기" 같은 오탐을 막는다.
# "백이십조"처럼 만/억/조로 끝나는 형태는 그 자체가 수이므로 공백 없이도 인정하되,
# 뒤에 "의/에/해"가 붙으면 "천만의 말씀" 류 관용구이므로 제외한다.
_KO_NUM_RE = re.compile(
    rf"{_KO_HEAD}(?:[일이삼사오육칠팔구십백천]|만|억|조)*"
    rf"(?:\s+{_KO_UNIT}|(?:만|억|조){_KO_UNIT}|(?:만|억|조)(?![의에해]))"
)

# 경제·행정 용어. tone-guide.md "용어 치환표"와 짝을 이룬다.
# ⚠️ 한쪽만 고치지 말 것 — 여기에만 있는 단어는 "기계는 잡는데 작가는 대체어를 모르는" 상태가 된다.
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


_ANY_HEADER_LINE_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def load_body_with_parts(path: Path) -> tuple[str, list[tuple[str, int]]]:
    """본문 + 각 `## ` 파트의 시작 offset(본문 좌표).

    `load_body`와 달리 offset을 보존해야 하므로 strip 하지 않는다. 파트 귀속을
    찍어주는 원거리 반복 리포트 전용이며, 밀도 측정에는 쓰지 않는다.
    """
    raw = _HTML_COMMENT_RE.sub("", path.read_text(encoding="utf-8"))
    lines: list[str] = []
    parts: list[tuple[str, int]] = []
    offset = 0
    for line in raw.splitlines():
        m = _ANY_HEADER_LINE_RE.match(line)
        if m or line.startswith(">"):
            if m and len(m.group(1)) == 2:
                parts.append((m.group(2).strip(), offset))
            lines.append("")
            offset += 1
            continue
        lines.append(line)
        offset += len(line) + 1
    return "\n".join(lines), parts


def part_of(pos: int, parts: list[tuple[str, int]]) -> str:
    """offset이 속한 파트 이름. 파트 헤더가 없으면 빈 문자열."""
    name = ""
    for title, start in parts:
        if start <= pos:
            name = title
        else:
            break
    return name


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


def count_numbers(text: str) -> int:
    """아라비아 숫자 + 한글 수사. 청자에게는 둘 다 똑같은 '숫자 하나'다."""
    return len(_NUM_RE.findall(text)) + len(_KO_NUM_RE.findall(text))


def find_number_heavy_sentences(body: str, limit: int = _SENT_NUM_LIMIT) -> list[str]:
    """한 문장에 숫자가 limit개 이상인 문장 — 기존 체크리스트 규칙의 기계 판정."""
    out = []
    for s in _SENT_SPLIT_RE.split(body):
        s = s.strip()
        if s and count_numbers(s) >= limit:
            out.append(s)
    return out


def find_near_duplicates(body: str, max_chars: int = 220, head: int = 6) -> list[tuple]:
    """가까운 거리에서 같은 문장이 두 번 나오는 자리를 찾는다.

    파트를 병렬로 쓰기 때문에 파트 N의 브릿지와 파트 N+1의 첫 문장이 겹친다.
    최종 대본에서는 두 파트가 그대로 이어붙으므로 실제로는 몇 초 간격으로 붙어 있고,
    TTS는 같은 말을 두 번 읽는다.

    실측(2026-08-05): 72편 중 6편에서 3~11초 간격 중복. 전부 outline의
    `- 다음 파트로의 전환:` 필드가 출처였다(그 필드는 위치가 파트 N인데 내용은 파트 N+1을
    여는 문장이라 주인이 없었다).

    max_chars=220 ≈ 30초(1분 ≈ 440자). 이보다 멀리 떨어진 재등장은 잡지 않는다 —
    "근데요, 여기서 진짜 핵심은" 같은 시그니처는 2분 이상 간격으로 다시 쓰는 게 정상이고,
    profile.md가 영상당 최대 2회로 허용한 장치다.

    앞 6글자(공백 제외)로 비교한다. 어미만 바꿔 되풀이하는 게 흔하기 때문이다 —
    "이제 우리 얘기예요" ↔ "이제 우리 얘기입니다", "사람 내주고" ↔ "사람 보내 주고".
    앞부분 20자를 통째로 비교하면 이런 걸 통째로 놓친다.
    짧은 문장도 뺄 수 없다. "정리해 볼까요."(7자)가 파트 7 끝과 클로징 시작에 연달아 나온
    실제 사례가 있다. 대신 짧은 문장은 간격 조건을 더 좁게 본다.
    """
    sents, pos, cursor = [], [], 0
    for s in _SENT_SPLIT_RE.split(body):
        s = s.strip()
        if len(re.sub(r"\s", "", s)) < 5:  # "맞습니다." 같은 맞장구는 반복돼도 자연스럽다
            continue
        i = body.find(s, cursor)
        if i < 0:
            continue
        cursor = i + len(s)
        sents.append(s)
        pos.append(i)

    bares = [re.sub(r"\s", "", s) for s in sents]

    def common_prefix(a: str, b: str) -> int:
        n = 0
        for x, y in zip(a, b):
            if x != y:
                break
            n += 1
        return n

    out = []
    for n in range(len(sents)):
        m = n - 1
        while m >= 0:
            gap = pos[n] - pos[m]
            if gap > max_chars:
                break
            shorter = min(len(bares[n]), len(bares[m]))
            # ① 앞부분 일치 — 어미만 바꾼 되풀이("이제 우리 얘기예요/입니다")를 잡는다.
            #    고정 길이(앞 N자)로 재면 "그럼에도 불구하고 …"처럼 접속어만 같은
            #    서로 다른 문장이 오탐으로 걸리므로, 짧은 쪽의 절반은 겹쳐야 한다.
            hit = common_prefix(bares[n], bares[m]) >= max(head, shorter // 2)
            # ⚠️ 이 검사는 "같은 말의 되풀이"만 잡는다. **뜻만 같고 어순·어휘가 다른
            #    재진술(paraphrase)은 못 잡는다.** 글자 유사도(2-gram 자카드)로 잡아보려
            #    시도했으나 실패했다 — 실측에서 오탐("다섯 곳 중 한 곳이에요" ↔
            #    "세 곳 중 한 곳이죠", 0.40)이 진짜 재진술("돈만 있으면 어떻게든 구해 와요"
            #    ↔ "기름은 그래도 돈만 있으면 어디서든 구해 옵니다", 0.29)보다 높아서
            #    어떤 임계값으로도 갈리지 않는다.
            #    재진술은 outline 브릿지 소유권 규칙(outline-guide.md)과 검수자가 막는다.
            if hit:
                out.append((sents[m], sents[n], gap, round(gap / 440 * 60)))
                break
            m -= 1
    return out


# 원거리 반복 WARN 구간 — 30초 밖 전부. 실측 노이즈가 편당 0.5건이라 상한을 두지 않는다
# (3,000자로 자르면 실제 사고였던 6,300자 간격 중복을 놓친다).
_DISTANT_MIN = 221
_DISTANT_MAX = 10**9
_DISTANT_PREFIX = 18


def find_distant_repeats(
    body: str,
    parts: list[tuple[str, int]],
    min_gap: int = _DISTANT_MIN,
    max_gap: int = _DISTANT_MAX,
    prefix: int = _DISTANT_PREFIX,
) -> list[dict]:
    """30초 밖에서 같은 말이 다시 나오는 자리 — **WARN 전용**.

    `find_near_duplicates`(220자 이내, FAIL)가 보지 못하는 사각지대다. 실측
    (2026-08-05, script.txt 76편): 18자 이상 동일 문자열 재등장 1,051건 중
    220자 이내는 205건뿐이었다. 나머지 80%를 아무도 보지 않고 있었다.

    **FAIL로 걸지 않는다.** 이 구간의 반복 중 상당수는 outline이 의도적으로 설계한
    오픈루프 회수다("푸틴이 이 구멍을 뭘로 메울까요" → 뒤에서 회수). 정상과 사고를
    가르는 건 outline의 `[회수]` 표시뿐이고, 그 판단은 검수자가 한다.

    파트 귀속을 함께 돌려준다 — 어느 파트와 어느 파트가 겹쳤는지 알아야 고칠 수 있다.

    문장 단위가 아니라 **글자 단위**로 본다. 실제 사고의 상당수가 문장 중간에서 겹치기
    때문이다 — "…이거 하나예요. **나머지 숫자는 다 곁가지입니다.**"의 뒷부분만 클로징에
    다시 나오는 식이라, 문장 앞부분만 비교하면 통째로 놓친다.
    """
    bare_chars: list[str] = []
    idx: list[int] = []  # bare 좌표 → body 좌표
    for i, ch in enumerate(body):
        if not ch.isspace():
            bare_chars.append(ch)
            idx.append(i)
    bare = "".join(bare_chars)

    seen: dict[str, int] = {}
    out: list[dict] = []
    i = 0
    while i + prefix <= len(bare):
        gram = bare[i : i + prefix]
        j = seen.get(gram)
        if j is None:
            seen[gram] = i
            i += 1
            continue

        gap = idx[i] - idx[j]
        if not (min_gap <= gap <= max_gap):
            i += 1
            continue

        # 일치 구간을 최대한 늘려 잡는다 — 18자는 하한일 뿐이다.
        k = 0
        while (
            i + prefix + k < len(bare)
            and j + prefix + k < i
            and bare[j + prefix + k] == bare[i + prefix + k]
        ):
            k += 1
        end_first = idx[j + prefix + k - 1] + 1
        end_second = idx[i + prefix + k - 1] + 1

        out.append({
            "first": body[idx[j] : end_first].replace("\n", " ").strip(" .,·"),
            "second": body[idx[i] : end_second].replace("\n", " ").strip(" .,·"),
            "gap": gap,
            "seconds": round(gap / 440 * 60),
            "first_part": part_of(idx[j], parts),
            "second_part": part_of(idx[i], parts),
        })
        i += prefix + k  # 같은 반복을 n-gram마다 중복 보고하지 않는다
    return out


def analyze(path: Path) -> dict:
    body = load_body(path)
    chars = len(re.sub(r"\s", "", body))
    if chars == 0:
        raise ValueError(f"본문이 비어 있다: {path}")

    # 원거리 반복은 파트 귀속을 찍어야 하므로 offset을 보존한 본문을 따로 쓴다.
    body_with_pos, parts = load_body_with_parts(path)

    ceilings, floors = {}, {}
    for label, cap in _LIMITS.items():
        n = count_numbers(body) if label == "숫자 밀도" else len(_JARGON_RE.findall(body))
        v = per_1k(n, chars)
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
        "near_duplicates": find_near_duplicates(body),
        "distant_repeats": find_distant_repeats(body_with_pos, parts),
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

    if r["near_duplicates"]:
        failed += 1
        print(f"\n❌ 30초 안에 같은 문장이 두 번 — {len(r['near_duplicates'])}건")
        for a, b, gap, sec in r["near_duplicates"][:5]:
            print(f"     · 간격 {sec}초")
            print(f"       앞: {a[:64]}…")
            print(f"       뒤: {b[:64]}…")
        print("       → 파트 경계일 가능성이 높다. 뒷 파트 첫 문장을 새로 쓴다")
        print("         (outline-guide.md '파트 경계 — 브릿지 소유권')")

    if r["heavy_sentences"]:
        failed += 1
        print(f"\n❌ 한 문장에 숫자 {_SENT_NUM_LIMIT}개 이상 — {len(r['heavy_sentences'])}건")
        for s in r["heavy_sentences"][:5]:
            print(f"     · {s[:80]}…")

    if r["clusters"]:
        print(f"\n⚠️  숫자가 150자 안에 6개 이상 몰린 구간 — {len(r['clusters'])}곳 (실패는 아니지만 손볼 자리)")
        for s in r["clusters"][:5]:
            print(f"     · {s[:80]}…")

    if r.get("distant_repeats"):
        n = len(r["distant_repeats"])
        print(f"\n⚠️  30초 밖에서 같은 말이 다시 나옴 — {n}건 (실패는 아니다. 검수자가 판단한다)")
        for d in r["distant_repeats"][:5]:
            where = f"{d['first_part'] or '?'} → {d['second_part'] or '?'}"
            print(f"     · {where}  (간격 {d['seconds']}초)")
            print(f"       앞: {d['first'][:64]}…")
            print(f"       뒤: {d['second'][:64]}…")
        if n > 5:
            print(f"     … 외 {n - 5}건")
        print("       → outline에 [회수]로 설계된 오픈루프면 정상이다.")
        print("         표시가 없는데 반복이면 뒤쪽을 새로 쓴다 (script-review-checklist.md '구조 검수')")

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
        return 1 if (ceil_fail or r["heavy_sentences"] or r["near_duplicates"]) else 0
    return report(r)


if __name__ == "__main__":
    sys.exit(main())
