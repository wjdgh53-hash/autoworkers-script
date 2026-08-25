#!/usr/bin/env python3
"""썸네일 복사용 통합본(.txt) 생성 + 규격 검증.

사용:
    python scripts/build_thumb_txt.py --project {프로젝트} --channel {채널}
    python scripts/build_thumb_txt.py --dir channels/{ch}/projects/{p}/output/thumbnails
    python scripts/build_thumb_txt.py --project {p} --channel {ch} --check   # 만들지 않고 검사만

무엇을 하나:
    output/thumbnails/prompts*.json 을 찾아 계열마다 같은 이름의 .txt 를 만든다.
    각 장은 `meta.prompt_prefix + prompt_en + meta.prompt_suffix` 를 이어 붙인 **완성 프롬프트**다.

🔴 왜 스크립트로 만드나 (2026-08-21 사고):
    서브에이전트 Write 가 막힌 세션에서 PD 가 txt 를 손으로 조립하다가
    규격을 확인하지 않고 `### 1 (content)` 헤더와 `---` 구분선을 넣었다.
    사용자가 파일을 열었을 때 "원래 이렇게 안 주잖아"로 바로 걸렸다.
    → **txt 는 손으로 쓰지 않는다. 이 스크립트로만 만든다.**

규격 (원본: prompts/pd-script.md 「복사용 통합본(.txt) 생성」):
    · 영어 프롬프트 원문만 넣는다. 번호·제목·한국어 설명·구분선을 넣지 않는다
    · 프롬프트 사이는 빈 줄 하나로만 구분한다
    · 계열을 한 파일에 섞지 않는다
    · 장당 1,200자 미만이면 prefix/suffix 가 빠졌을 가능성이 높다
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

SERIES = ["prompts", "prompts-countryball", "prompts-geopolitics", "prompts-illustration"]
MIN_CHARS = 1200

# 규격 위반 패턴 — 줄 맨 앞에 오면 안 되는 것들
BAD_LINE = re.compile(r"^\s*(#{1,6}\s|-{3,}\s*$|={3,}\s*$|\*{3,}\s*$|\[\d+\]|\d+\s*[.)]\s)")
# 한글이 섞이면 설명을 넣은 것이다 (프롬프트 안의 한글 라벨은 따옴표 안에만 있어야 한다)
HANGUL = re.compile(r"[가-힣]")


def assemble(data: dict) -> list[str]:
    meta = data.get("meta", {})
    pre = (meta.get("prompt_prefix") or "").strip()
    suf = (meta.get("prompt_suffix") or "").strip()
    out = []
    for t in data["thumbnails"]:
        out.append(" ".join(x for x in (pre, t["prompt_en"].strip(), suf) if x))
    return out


def check_text(name: str, text: str) -> list[str]:
    """규격 위반을 목록으로 돌려준다. 비어 있으면 통과."""
    problems = []
    chunks = [c for c in text.strip().split("\n\n")]

    for i, line in enumerate(text.splitlines(), 1):
        if BAD_LINE.match(line):
            problems.append(f"{name}:{i}행 — 번호·제목·구분선이 들어갔다: {line[:60]!r}")

    for i, c in enumerate(chunks, 1):
        if "\n" in c:
            problems.append(f"{name} {i}번째 덩어리 — 한 장은 한 줄이어야 한다(줄바꿈 발견)")
        if len(c) < MIN_CHARS:
            problems.append(
                f"{name} {i}번째 덩어리 — {len(c)}자로 너무 짧다. "
                f"prefix/suffix 조립이 빠졌는지 meta 를 확인할 것 (기준 {MIN_CHARS}자)"
            )
        # 따옴표 밖 한글 = 설명을 끼워 넣은 것
        outside = re.sub(r'"[^"]*"', "", c)
        if HANGUL.search(outside):
            bad = HANGUL.search(outside).group()
            problems.append(
                f"{name} {i}번째 덩어리 — 따옴표 밖에 한글이 있다({bad!r}). "
                f"한국어 설명·제목을 넣지 않는다"
            )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="썸네일 복사용 통합본(.txt) 생성 + 규격 검증")
    ap.add_argument("--project")
    ap.add_argument("--channel")
    ap.add_argument("--dir", help="thumbnails 디렉토리를 직접 지정")
    ap.add_argument("--check", action="store_true", help="생성하지 않고 기존 txt 를 검사만 한다")
    a = ap.parse_args()

    if a.dir:
        d = a.dir
    elif a.project and a.channel:
        d = os.path.join("channels", a.channel, "projects", a.project, "output", "thumbnails")
    else:
        ap.error("--project 와 --channel 을 함께 주거나, --dir 를 주십시오")

    if not os.path.isdir(d):
        print(f"❌ 폴더가 없습니다: {d}")
        return 2

    found = 0
    problems: list[str] = []

    for src in SERIES:
        jp = os.path.join(d, src + ".json")
        tp = os.path.join(d, src + ".txt")
        if not os.path.exists(jp):
            continue
        found += 1

        if a.check:
            if not os.path.exists(tp):
                problems.append(f"{src}.txt 가 없다 — JSON 이 있으면 txt 도 있어야 한다")
                continue
            text = open(tp, encoding="utf-8").read()
        else:
            data = json.load(open(jp, encoding="utf-8"))
            chunks = assemble(data)
            text = "\n\n".join(chunks) + "\n"
            open(tp, "w", encoding="utf-8").write(text)

        chunks = text.strip().split("\n\n")
        avg = sum(len(c) for c in chunks) // max(len(chunks), 1)
        problems += check_text(src + ".txt", text)
        verb = "검사" if a.check else "생성"
        print(f"{src}.txt {verb} — {len(chunks)}장, 장당 평균 {avg:,}자")

    if found == 0:
        print(f"❌ prompts*.json 을 찾지 못했습니다: {d}")
        return 2

    if problems:
        print("\n🚨 규격 위반")
        for p in problems:
            print("  · " + p)
        print("\n규격 원본: prompts/pd-script.md 「복사용 통합본(.txt) 생성」")
        return 1

    print("\n✅ 규격 통과 — 영문 원문만, 장 사이는 빈 줄 하나.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
