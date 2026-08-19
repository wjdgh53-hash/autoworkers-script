#!/usr/bin/env python3
"""규칙 회귀 검사 — 2026-08-19 감사에서 지운 규칙이 되살아났는지 본다.

    .venv/bin/python scripts/check_rules.py

왜 필요한가:
    2026-08-19 하루 동안 「시키는 규칙」 20여 개를 제거했는데,
    **같은 날 오후에 내가 그중 일부를 다시 써넣었다.** 원인을 지운 자리에
    불안해서 반대 규칙을 놓은 것이다. 그게 이 저장소에 규칙이 쌓여 온 방식이다.

    사람(또는 다음 세션의 에이전트)은 이걸 스스로 못 막는다. 기계가 막아야 한다.
    이 스크립트는 **대본을 검사하지 않는다.** 규칙 파일이 되돌아갔는지만 본다.

종료 코드:
    0 — 통과
    1 — 지운 규칙이 되살아났다
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 검사 대상. _archive·notes·_refs는 과거 기록이라 제외한다.
TARGET_GLOBS = [
    "prompts/*.md",
    ".claude/agents/*.md",
    ".claude/skills/*/SKILL.md",
    "channels/*/config/*.md",
]

# ── 되살아나면 안 되는 것 ────────────────────────────────────────
# (이름, 정규식, 왜 지웠나)
BANNED: list[tuple[str, str, str]] = [
    (
        "반문 하한",
        r"반문[^\n]{0,40}(하한|≥\s*3\.5|60초에 한 번)",
        "근거가 히트작 1편(7.9)뿐인데 발행 대본 91편 중 78%가 미달이었다. "
        "이 하한을 지킨 08-16이 반문 7.7로 답 없는 질문을 채워 넣었다.",
    ),
    (
        "권위 인용·전환어 하한",
        r"(권위 인용|전환어)[^\n]{0,30}(하한|≥\s*0\.[36])",
        "인용할 게 없는 소재에서 억지 출처를 붙이게 하고, \"자,\"를 뿌리게 했다.",
    ),
    (
        "확장 비유 필수",
        r"확장 비유[^\n]{0,10}(는|가|를)?\s*(필수|반드시)(?!가 아니)|(필수|반드시)[^\n]{0,20}확장 비유",
        "블록 3이 본문의 28~45%인데 비유가 그 블록의 정의였다. "
        "비유가 필요 없는 소재에서도 본문 3분의 1을 비유로 채우게 만들었다.",
    ),
    (
        "숫자 밀도 총량 상한",
        r"숫자 밀도[^\n]{0,40}(상한|이하|≤)\s*\d|1,?000자당\s*4~10",
        "탐정 91편 중 54편(59%)이 초과인데 전부 발행됐고 채널은 성과가 났다. "
        "총량은 소재가 정한다. 몰아쓰기는 문장당 4개 게이트가 잡는다.",
    ),
    (
        "한 문단 숫자 2개",
        r"한 문단[^\n]{0,20}(숫자|퍼센트)[^\n]{0,10}2개(까지|\s*이하)",
        "방구석 숫자 밀도 하한 12.0과 산술적으로 양립 불가였다(한 문단 200자면 2.4개 필요).",
    ),
    (
        "답 미루기 금지",
        r"(답을 뒤로 미루|유예 선언)[^\n]{0,30}(금지|않는다|쓰지)",
        "08-16 작가가 그 문장을 쓴 이유는 반문 개수를 채워야 했기 때문이다. "
        "압력이 사라졌으므로 결과를 금지할 이유가 없다. 오픈루프까지 막힌다.",
    ),
    (
        "클로징 열린 질문 2~3개",
        r"열린 질문 2~3개",
        "매 영상 답 없는 질문 2~3개를 강제했고, script-skeleton 블록 7의 "
        "\"질문 회수 → 답\"과 정면으로 어긋났다.",
    ),
    (
        "개수 강제 (독창성·레퍼 표현)",
        r"(고유한 관점[^\n]{0,20}최소 \d|레퍼[^\n]{0,20}최소 5개|웬만하면 있다)",
        "없는 것을 찾게 만들어, 평범한 표현까지 「레퍼 고유 표현」으로 올려 "
        "대본에서 못 쓰게 막았다.",
    ),
    (
        "썸네일 문구 L1 억제",
        r"(썸네일|제목)[^\n]{0,60}L1[^\n]{0,20}최후의 수단|"
        r"최소 2개는 L3[^\n]{0,30}(썸네일|제목|카피)",
        "2026-08-16에 제목·썸네일 어휘 제약이 전면 완화됐는데 이 등급표만 "
        "옛 상태로 남아 L1을 억제했다. 제목 공식 계승이 곧 L1이다. "
        "⚠️ 본문 Hook용 L1~L4(creative-strategy)는 의도적으로 유지한다 — 본문은 독창성 규칙이 살아 있다.",
    ),
    (
        "어려운 말 다 걷어내고",
        r"어려운 말 다 (걷어내|빼)(?![^\n]{0,20}(쓰지|않는|금지))",
        "어휘를 바꾸라는 요구로 읽혀 고유명사를 지우고 비유로 대체하는 사고를 냈다.",
    ),
    (
        "초등학생도 이해할 쉬운 「말」",
        r"초등학생[^\n]{0,20}쉬운 말",
        "쉽게 할 것은 「설명」이지 「어휘」가 아니다.",
    ),
]

# ── 있어야 하는 것 (지우면 안 되는 핵심 게이트) ──────────────────
REQUIRED: list[tuple[str, str]] = [
    ("경제·행정 용어 상한", r'"경제·행정 용어":\s*1\.5'),
    ("1인칭 상한", r'"1인칭":\s*1\.2'),
    ("문장당 숫자 제한", r"_SENT_NUM_LIMIT\s*=\s*4"),
    ("숫자 밀도 하한", r'_FLOORS\s*=\s*\{"숫자 밀도":\s*4\.0\}'),
    ("근접 중복 검사", r"def find_near_duplicates"),
]
REQUIRED_FILE = "scripts/src/check_tone.py"


# 규칙이 아니라 「지웠다는 기록」이거나 「하지 말라는 부정문」인 줄은 건너뛴다.
# 이걸 안 걸러내면 감사 기록 자체가 위반으로 잡힌다.
SKIP_RE = re.compile(
    r"삭제|폐기|철회|회수|되살|더 이상|옛 (규칙|항목|문구|예문|형식|\d+번)|"
    r"이었다|였다\.|개정|아니(다|라|며|고)|없다|않는다|없음|측정만|쓰지 않는다|금지 유지"
)


def iter_targets():
    for pat in TARGET_GLOBS:
        for p in sorted(ROOT.glob(pat)):
            if "_archive" in p.parts:
                continue
            yield p


def main() -> int:
    problems: list[str] = []

    # ① 지운 규칙이 되살아났는가
    for name, pattern, why in BANNED:
        rx = re.compile(pattern)
        for path in iter_targets():
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                # 「삭제했다」류 회고 서술은 규칙이 아니다.
                if SKIP_RE.search(line):
                    continue
                if rx.search(line):
                    rel = path.relative_to(ROOT)
                    problems.append(
                        f"🔴 되살아남: {name}\n"
                        f"   {rel}:{i}\n"
                        f"   {line.strip()[:110]}\n"
                        f"   ↳ 지운 이유: {why}"
                    )

    # ② 핵심 게이트가 사라졌는가
    gate_src = (ROOT / REQUIRED_FILE).read_text(encoding="utf-8")
    for name, pattern in REQUIRED:
        if not re.search(pattern, gate_src):
            problems.append(
                f"🔴 사라짐: {name}\n"
                f"   {REQUIRED_FILE}\n"
                f"   ↳ 이건 소재와 무관하게 항상 결함인 항목이라 지우면 안 된다."
            )

    if problems:
        print(f"\n{len(problems)}건 발견\n")
        print(("\n\n").join(problems))
        print(
            "\n\n판단이 필요하면 notes/rule-conflict-audit.md를 읽는다.\n"
            "정말 되살려야 한다면 이 스크립트의 BANNED 목록에서도 함께 빼고, "
            "왜 뒤집는지 근거를 커밋 메시지에 적는다.\n"
        )
        return 1

    print("✅ 통과 — 지운 규칙이 되살아나지 않았고 핵심 게이트도 전부 살아 있다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
