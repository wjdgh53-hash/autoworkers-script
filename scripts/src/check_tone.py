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

상한/하한/주의 설계:
    상한만 FAIL로 막는다. 하한과 주의는 WARN에 그친다.
    하한을 FAIL로 걸면 카운터를 채우려고 "뭉클"을 억지로 뿌리는 대본이 나온다.
    분량 검증은 이 문제가 없다 — 글자수는 채우려면 내용을 넣는 수밖에 없다. 문체는 다르다.
    구조는 prompts/script-skeleton.md, 문체는 prompts/tone-guide.md가 원본이고 여기서는 확인만 한다.

기준값 교정 (2026-08-10 재교정. 벤치마크 2개 채널 7편 + 우리 3편 실측):
    「코믹스 경제」 4편 — 캐나다 잠수함(203k) · 폭염(63k) · 수소(11k) · 광물(4k)
    「경제라는 게임」 3편 — 밥상 식자재 · 구글 인재유출 · 삼성 AI 모듈러홈

    | 지표          | 벤치마크 7편 | 우리 3편   | 채택 기준        |
    |---------------|-------------|-----------|-----------------|
    | 숫자 밀도      | 4.6 ~ 21.9  | 2.0 ~ 5.1 | 4.0 ≤ x ≤ 10.0  |
    | 경제·행정 용어 | 0.0 ~  0.4  | 0.0       | ≤ 1.5           |
    | 1인칭          | 0.2 ~  0.6  | 2.8 ~ 3.7 | ≤ 1.2           |
    | 반문           | 4.3 ~  8.8  | 1.7 ~ 2.0 | ≥ 3.5           |
    | 권위 인용      | 0.2 ~  1.1  | 0.0 ~ 0.5 | ≥ 0.3           |
    | 전환어         | 0.6 ~  3.5  | 0.3 ~ 1.5 | ≥ 0.6           |
    | 비유 소재      | 0.2 ~  3.5  | 3.4 ~ 4.1 | ≤ 3.0 (주의)    |

    ⚠️ 숫자 밀도 상한만은 벤치마크보다 엄하게 잡았다. 벤치마크 다수가 13~21이지만
       우리는 시니어 타겟이고, **203k 히트작이 4.6**이다. 그쪽을 목표점으로 본다.
       그래서 "벤치마크가 전부 통과해야 한다"는 옛 교정 논리는 더 이상 쓰지 않는다.

    ⚠️ 벤치마크로 이 스크립트를 검증할 때는 상한·하한 수치만 본다.
       자동자막 텍스트는 같은 문장이 중복 기록되어 근접 반복 항목에서 오탐이 난다.

종료 코드:
    0 — 상한 항목 전부 통과 (하한 미달·주의 초과는 WARN이며 0을 반환한다)
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

# 측정 장치 (2026-08-10 재교정. 모듈 docstring 표 참조)
_DEVICES = {
    # 리텐션 백본. 벤치마크가 60초에 한 번꼴로 던진다. 우리와 가장 크게 갈린 지표다.
    "반문": re.compile(r"(\?|까요|겠습니까|나요\b|셨나요|을까|를까)"),
    # 1인칭은 "온기"지만 과하면 발표자 말투가 된다. 벤치마크는 우리의 1/6만 쓴다.
    # 지우라는 뜻이 아니라, 그 자리를 권위 인용·대조로 바꿔 앉히라는 뜻이다.
    "1인칭": re.compile(
        r"(저도 그랬|저는 좀|저도 처음|화가 나|얼떨떨|놀랐|믿기지|솔직히|"
        r"제가 |저는 |저도 )"
    ),
    # 2인칭. 시청자를 화면 안으로 끌어들이는 장치. (2026-08-19 신설)
    #   실측: 방구석 결 벤치 히트 1.2~2.7 / 실패 0.8~1.1 / 우리 08-18 0.8·08-16 3.7.
    #   ⚠️ 상한은 두지 않는다 — 우리 최고작(08-16, 26.6배)이 3.7이라 상한 근거가 없다.
    "2인칭": re.compile(r"(여러분|당신|본인|내 돈|내 계좌|우리 돈)"),
    # 발언·보고서·통계 인용. 1인칭이 빠진 자리를 이것이 채운다. 제재 방어도 겸한다.
    "권위 인용": re.compile(
        r"(따르면|자료를 보면|통계를 보면|보도에|발표에|보고서|밝혔|전했|"
        r"분석이|평가|지적|관계자|전문가|기관)"
    ),
    # 구어 전환어. 블록이 바뀌는 자리의 리듬. 203k 히트작이 1,000자당 3.5회 썼다.
    "전환어": re.compile(r"(자,|자 |그런데 말입니다|여기서 한번|그럼 여기서|자\.)"),
    # 비유 소재어. ⚠️ 판정이 아니라 "볼 자리" 표시다 — 아래 _WATCH 주석 참조.
    "비유 소재": re.compile(
        r"(살림|가게|장바구니|밥상|월급|이자|달력|장롱|목수|고지서|통장|냉장고|"
        r"동네|아파트|집주인|숟가락|밥솥|빚쟁이|금고|장부|치면|셈이|비유)"
    ),
}

# 상한 — 넘으면 FAIL
_CEILINGS = {"숫자 밀도": 10.0, "경제·행정 용어": 1.5, "1인칭": 1.2}

# 하한 — 미달이면 WARN (차단하지 않는다)
#   숫자 밀도 4.0은 정보량 하한이다. 비유로 분량을 때우면 여기에 걸린다.
_FLOORS = {"숫자 밀도": 4.0, "반문": 3.5, "권위 인용": 0.3, "전환어": 0.6}

# ─────────────────────────────────────────────────────────────────────
# 채널별 밴드 재정의 (2026-08-19 신설)
#
# 위 기본값은 **탐정경제학 계열 근거**로 잡혔다. 모듈 docstring이 그렇게 적고 있다 —
# "우리는 시니어 타겟이고 203k 히트작이 4.6이다. 그쪽이 목표점이다."
#
# 🔴 그런데 방구석 경제는 축이 다르다(주어=시청자 본인의 돈). 결이 같은 벤치 7편을
#    **이 파일과 같은 잣대로** 재 보니 아래와 같았다(2026-08-19, 자동자막 기준).
#
#      숫자 밀도   히트 26.7 · 32.8 · 23.3 · 23.5(해설형) / 12.2(사연형)
#                  실패 20.8 · 30.0
#                  우리 8.7 · 7.0
#      2인칭       히트 1.8 · 2.4 · 1.0 · 2.1 · 1.2
#                  실패 0.6 · 1.3
#                  우리 0.3 · 0.9
#
# ⚠️ **숫자 밀도는 히트와 실패를 가르지 못한다**(20.8~32.8로 겹친다). 하한을 올린다고
#    성적이 오른다는 증거는 없다. 다만 **기본 상한 10.0은 벤치 7편 전부를 차단**하므로
#    그건 명백히 잘못된 값이다. 상한만 실측 위로 올리고, 하한은 "벤치 어느 편보다도
#    낮은 상태"만 벗어나게 12.0으로 둔다(WARN이라 차단하지 않는다).
#
# ⚠️ 2인칭은 상대적으로 깨끗하게 갈렸다(히트 1.0~2.4 vs 우리 0.3~0.9). 하한 1.2.
#    ⛔ 상한은 두지 않는다 — 우리 최고작(08-16, 26.6배)이 다른 잣대로 3.7이었다.
#
# 상한을 푸는 근거: 나열식 몰아쓰기는 _SENT_NUM_LIMIT(한 문장 4개)와
# find_number_clusters()가 이미 따로 막는다. 밀도 상한이 그 역할까지 겸할 필요가 없다.
# (실측 원본: channels/bangguseok-economy/config/_benchmarks/script-patterns.md)
_CHANNEL_BANDS: dict[str, dict[str, dict[str, float]]] = {
    "bangguseok-economy": {
        # 벤치 최고 32.8 바로 위. 이 값을 넘기면 그때는 정말 나열이다.
        "ceilings": {"숫자 밀도": 34.0},
        # 12.0 = 벤치 7편 중 최저(사연형 12.2) 바로 아래. 히트 보장이 아니라 하한선이다.
        "floors": {"숫자 밀도": 12.0, "2인칭": 1.2},
    },
}


def channel_of(path: Path) -> str:
    """경로에서 채널 id를 뽑는다 — channels/{채널}/projects/... 규약.

    호출부를 바꾸지 않으려고 경로에서 읽는다. 규약에 안 맞으면 빈 문자열이라
    기본 밴드가 그대로 쓰인다(기존 동작 유지).
    """
    parts = path.resolve().parts
    if "channels" in parts:
        i = parts.index("channels")
        if i + 1 < len(parts):
            return parts[i + 1]
    return ""


def bands_for(path: Path) -> tuple[dict, dict]:
    """이 대본에 적용할 (상한, 하한)을 돌려준다."""
    ceilings = dict(_CEILINGS)
    floors = dict(_FLOORS)
    override = _CHANNEL_BANDS.get(channel_of(path))
    if override:
        ceilings.update(override.get("ceilings", {}))
        floors.update(override.get("floors", {}))
    return ceilings, floors

# 주의 — 넘으면 WARN. FAIL로 막지 않는 이유가 있다.
#   이 정규식은 "확장 비유 하나"와 "잘게 뿌린 비유 열 개"를 구분하지 못한다.
#   게다가 주제가 가전·부동산이면 소재어가 그냥 본문에 나온다(벤치마크 삼성편 3.5).
#   그래서 기계는 "여기를 보라"까지만 하고, 판정은 검수자가 한다.
#   판정 기준은 prompts/script-skeleton.md §5 "비유 운용 규칙".
_WATCH = {"비유 소재": 3.0}
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

    def measure(label: str) -> float:
        if label == "숫자 밀도":
            return per_1k(count_numbers(body), chars)
        if label == "경제·행정 용어":
            return per_1k(len(_JARGON_RE.findall(body)), chars)
        return per_1k(len(_DEVICES[label].findall(body)), chars)

    cap_band, floor_band = bands_for(path)
    ch = channel_of(path)

    ceilings, floors, watch = {}, {}, {}
    for label, cap in cap_band.items():
        ceilings[label] = {"value": (v := measure(label)), "limit": cap, "pass": v <= cap}
    for label, floor in floor_band.items():
        floors[label] = {"value": (v := measure(label)), "floor": floor, "pass": v >= floor}
    for label, cap in _WATCH.items():
        watch[label] = {"value": (v := measure(label)), "limit": cap, "pass": v <= cap}

    return {
        "path": str(path),
        "channel": ch,
        "band_override": ch in _CHANNEL_BANDS,
        "chars": chars,
        "ceilings": ceilings,
        "floors": floors,
        "watch": watch,
        "clusters": find_number_clusters(body),
        "heavy_sentences": find_number_heavy_sentences(body),
        "near_duplicates": find_near_duplicates(body),
        "distant_repeats": find_distant_repeats(body_with_pos, parts),
        "spelled_out": find_spelled_out_numbers(body),
    }


# 🔴🔴 **금액·규모를 한글로 풀어 쓴 자리** (2026-08-12 정호님이 완성 자막에서 잡으심)
#
#   「지난달 우리 증시에서 **팔백조**가 사라졌습니다」  ← 자막에 이대로 나갔다
#
#   대본 글자는 **자막으로 그대로** 나간다. 읽는 것은 툴이 맡으므로
#   `800조` 라고 적어야 화면이 자연스럽고, 소리는 이지롱폼 발음 규칙이
#   「팔백조」 로 알아서 바꾼다. `tts-rules.md` 8번에 이미 있던 규칙인데
#   tone-guide 가 우선이라 무력화됐다 — **규칙만으로는 또 샌다. 기계가 잡는다.**
#
#   ⚠️ 나이·고유어 단위(쉰두 살·스무 개)는 한글이 맞다 → 안 잡는다.
#      큰 자릿수(백·천·만·억·조)를 한글로 쓴 것만 본다.
_KO_BIG_NUM = re.compile(
    r"(?:[일이삼사오육칠팔구]|십|백|천)?"
    r"(?:[일이삼사오육칠팔구십백천]{0,6})"
    r"(?:조|억|만)(?:\s*원|\s*개|\s*명|\s*곳|\s*대)?"
)
# 진짜 한글 수사인지 — 머리에 한자 수사가 와야 한다 (「구조」·「사기」 같은 말을 거른다)
_KO_BIG_HEAD = re.compile(r"^(?:[일이삼사오육칠팔구]|십|백|천)")


def find_spelled_out_numbers(body: str, limit: int = 8) -> list[str]:
    """금액·규모를 한글로 풀어 쓴 자리. **찾으면 FAIL 이다.**

    자막에 그대로 나가므로 「팔백조」 가 화면에 뜬다.
    """
    나온것 = []
    for ㅁ in _KO_BIG_NUM.finditer(body):
        말 = ㅁ.group(0)
        # 🔴 앞에 아라비아 숫자가 붙어 있으면 **규칙대로 쓴 것**이다 — 잡지 않는다
        #   「5천만 원」·「3천억」·「4조 6,000억 원」 은 tts-rules 8번이 권하는 형식이다
        #   (아라비아 + 한글 단위). 「천만」 만 떼어 보면 한글 수사로 오인한다.
        #   (2026-08-12 정호님이 「5천만 원이 FAIL 로 잡힌다」 고 잡으심)
        if ㅁ.start() > 0 and body[ㅁ.start() - 1].isdigit():
            continue
        if not _KO_BIG_HEAD.match(말) or len(말) < 3:
            continue
        # 「만」 하나짜리(「만 원」)나 관용구는 뺀다 — 자릿수가 둘 이상이어야 수사다
        if not re.search(r"[십백천]", 말) and not re.match(r"^[일이삼사오육칠팔구]{2,}", 말):
            continue
        앞 = max(0, ㅁ.start() - 14)
        나온것.append(f"…{body[앞:ㅁ.end() + 10]}…")
        if len(나온것) >= limit:
            break
    return 나온것


def report(r: dict) -> int:
    print(f"\n대본: {r['path']}  (공백 제외 {r['chars']:,}자)")
    print("\n── 상한 (넘으면 실패) " + "─" * 34)
    failed = 0
    for label, d in r["ceilings"].items():
        mark = "✅ PASS" if d["pass"] else "❌ FAIL"
        print(f"  {label:<14} {d['value']:>6.1f} / {d['limit']:>4.1f}   {mark}")
        if not d["pass"]:
            failed += 1

    # 🔴 한글로 풀어 쓴 금액·규모 — **자막에 그대로 나간다**
    if r.get("spelled_out"):
        failed += 1
        print(f"\n  {'한글로 쓴 금액':<14} {len(r['spelled_out']):>6}곳          ❌ FAIL")
        print("     → 자막에 그대로 나갑니다. **아라비아 숫자로** 적으세요"
              " (800조 ○ / 팔백조 ✗).")
        print("       읽는 것은 툴이 맡습니다 — 이지롱폼이 「팔백조」 로 읽어 줍니다.")
        for ㄱ in r["spelled_out"][:5]:
            print(f"       {ㄱ}")

    print("\n── 하한 (미달이면 경고) " + "─" * 33)
    for label, d in r["floors"].items():
        mark = "✅" if d["pass"] else "⚠️  미달"
        print(f"  {label:<14} {d['value']:>6.1f} / {d['floor']:>4.1f}   {mark}")

    if r.get("watch"):
        print("\n── 주의 (검수자가 판정한다) " + "─" * 29)
        for label, d in r["watch"].items():
            mark = "✅" if d["pass"] else "⚠️  초과"
            print(f"  {label:<14} {d['value']:>6.1f} / {d['limit']:>4.1f}   {mark}")
        if not all(d["pass"] for d in r["watch"].values()):
            print("     → 확장 비유 하나인지, 잘게 뿌린 비유 여러 개인지 직접 본다")
            print("       (prompts/script-skeleton.md §5 '비유 운용 규칙')")

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
        print("  1인칭이 넘쳤으면 감정을 지우는 게 아니라 권위 인용·대조로 바꿔 앉힌다.")
        return 1
    if any(not d["pass"] for d in r["floors"].values()):
        print("→ 상한은 통과. 다만 하한 미달 항목이 있다 (위 ⚠️).")
        print("  반문이 모자라면 60초에 한 번꼴로 시청자에게 되묻는다.")
        print("  숫자 밀도가 모자라면 비유로 때운 자리를 사실·사례로 바꾼다.")
        print("  (prompts/script-skeleton.md — 확장 비유는 1~3개, 나머지는 사례·대조·인용)")
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
