#!/usr/bin/env python3
"""중간 산출물 분량 상한 검수 — 생성 비용 절감 규칙이 실제로 지켜졌는지 확인한다.

2026-08-17 비용 절감(커밋 d7418fc)으로 도입된 상한을 기계로 검사한다.
상한의 정본은 각 프롬프트 파일이다. 이 스크립트는 그 값을 복제해 검사만 한다:
  - analysis.md  5,000자  → prompts/reference-analyze.md 「🚨 분량 상한」
  - patterns.md 12,000자  → prompts/reference-patterns.md 「🚨 분량 상한」

사용법:
  python scripts/src/check_artifacts.py                      # 최근 수정 프로젝트 자동 선택
  python scripts/src/check_artifacts.py channels/{채널}/projects/{프로젝트}
  python scripts/src/check_artifacts.py --all                 # 전 프로젝트 요약

exit 0 = 전부 통과 / exit 1 = 초과 있음 (파이프라인을 막지는 않는다. 보고용이다)
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CAP_ANALYSIS = 5_000
CAP_PATTERNS = 12_000

# reference-analyze.md 8번 항목의 정확한 제목. 옛 프로젝트에는 다른 `## 8.`이 있어
# 번호만 맞춰 보면 오탐한다(실측: "## 8. ⛔ 계승 금지 목록", "## 8. 【이 편 전용】…").
SECTION_8 = re.compile(r"^##\s*8\.\s*레퍼\s*고유\s*표현\s*목록", re.M)


def size(path: str) -> int | None:
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="ignore") as f:
        return len(f.read())


def verdict(actual: int, cap: int) -> str:
    if actual <= cap:
        return "✅"
    return f"❌ {actual / cap:.1f}배 초과"


def check(project_dir: str) -> bool:
    """한 프로젝트를 검사한다. 모두 통과면 True."""
    rel = os.path.relpath(project_dir, ROOT)
    print(f"\n{'=' * 72}\n  {rel}\n{'=' * 72}")

    rows: list[tuple[str, int | None, int, str]] = []
    ok = True

    analyses = sorted(glob.glob(os.path.join(project_dir, "_refs", "*", "analysis.md")))
    if not analyses:
        print("  ⚠️  _refs/*/analysis.md 없음 — 레퍼 수집 전이거나 다른 구조입니다")
    for path in analyses:
        ref = os.path.basename(os.path.dirname(path))
        n = size(path)
        rows.append((f"_refs/{ref}/analysis.md", n, CAP_ANALYSIS, verdict(n, CAP_ANALYSIS)))
        if n > CAP_ANALYSIS:
            ok = False

        with open(path, encoding="utf-8", errors="ignore") as f:
            has8 = bool(SECTION_8.search(f.read()))
        rows.append((f"  └ ## 8. 레퍼 고유 표현 목록", None, 0, "✅ 있음" if has8 else "❌ 없음"))
        if not has8:
            ok = False

    patterns = os.path.join(project_dir, "_script", "patterns.md")
    n = size(patterns)
    if n is None:
        print("  ⚠️  _script/patterns.md 없음 — DATA_PREP 전입니다")
    else:
        rows.append(("_script/patterns.md", n, CAP_PATTERNS, verdict(n, CAP_PATTERNS)))
        if n > CAP_PATTERNS:
            ok = False

    print(f"\n  {'항목':<34}{'실측':>9}{'상한':>9}   판정")
    print(f"  {'-' * 68}")
    for name, actual, cap, mark in rows:
        a = f"{actual:,}" if actual is not None else "-"
        c = f"{cap:,}" if cap else "-"
        print(f"  {name:<34}{a:>9}{c:>9}   {mark}")

    # 참고용 — 상한 대상은 아니지만 비용에 직결되는 산출물
    extras = [
        ("_script/outline.md", "_script", "outline.md"),
        ("_script/concept.md", "_script", "concept.md"),
        ("_script/verified-data.md", "_script", "verified-data.md"),
        ("_script/script.txt", "_script", "script.txt"),
    ]
    ref_lines = []
    for label, sub, fn in extras:
        v = size(os.path.join(project_dir, sub, fn))
        if v is not None:
            ref_lines.append(f"{label} {v:,}자")
    thumbs = sorted(glob.glob(os.path.join(project_dir, "output", "thumbnails", "*.json")))
    if thumbs:
        tot = sum(size(t) for t in thumbs)
        ref_lines.append(f"썸네일 json {len(thumbs)}개 합 {tot:,}자")
    if ref_lines:
        print(f"\n  참고(상한 없음): " + " · ".join(ref_lines))

    print(f"\n  → {'전부 통과' if ok else '초과 항목 있음'}")
    return ok


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--all"]
    all_mode = "--all" in sys.argv[1:]

    if all_mode:
        targets = sorted(glob.glob(os.path.join(ROOT, "channels", "*", "projects", "*")))
    elif args:
        targets = [os.path.abspath(args[0])]
    else:
        scripts = glob.glob(os.path.join(ROOT, "channels", "*", "projects", "*", "_script"))
        if not scripts:
            print("프로젝트를 찾지 못했습니다. 경로를 직접 지정하세요.")
            return 1
        latest = max(scripts, key=os.path.getmtime)
        targets = [os.path.dirname(latest)]

    targets = [t for t in targets if os.path.isdir(t)]
    results = [check(t) for t in targets]

    if len(results) > 1:
        bad = results.count(False)
        print(f"\n{'=' * 72}\n  요약: {len(results)}개 중 {bad}개에 초과 항목\n{'=' * 72}")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
