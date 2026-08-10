from __future__ import annotations
"""draft.md 파트별 분량 검증 — outline.md 목표 대비 실제 글자수 비교.

사용법:
    .venv/bin/python scripts/src/validate_draft.py <outline_path> <draft_path>
        [--threshold 0.9] [--max-threshold 1.3] [--total-max-threshold 1.2]

세 가지를 본다:
1. 파트별 하한(threshold) — 내용이 빠졌는지
2. 파트별 상한(max-threshold) — 한 파트가 폭주했는지
3. 총합 상한(total-max-threshold) — 파트가 골고루 부풀어 러닝타임을 넘겼는지

3번이 없으면 모든 파트가 106~114%로 균일하게 부풀 때 전부 PASS가 뜨면서
총합만 조용히 초과한다(실측: 전 프로젝트 총합 중앙값 109%).

임계값은 "정밀 관리"가 아니라 "폭주 감지" 기준으로 잡혀 있다.
파트 상한을 115%로 조이면 실측 55개 프로젝트 중 67%에서 압축 라운드가 발동해
비용이 폭증한다. 130%는 script-review-checklist.md의 군살 기준선과 동일하다.

종료 코드:
    0 — 전 파트가 범위 안이고 총합도 상한 이하
    1 — FAIL 섹션 1개 이상 (부족/초과) 또는 총합 초과
    2 — 파싱 에러 (목표/섹션 추출 불가, 또는 목표 수 ≠ 섹션 수)
"""

import argparse
import re
import sys
from pathlib import Path

# ── outline.md 파트 목표 추출 ──────────────────────────────────
# 헤더의 괄호 안에서 "N분"과 "N자"를 함께 갖는 그룹을 찾는다.
# 괄호 앞뒤에 다른 말이 붙어도 인식해야 한다. 실제로 쓰이는 형태들:
#   `### 파트 4: 제목 (크리에이터 분석, ~4분, ~1,650자)`           ← 괄호 안 접두어
#   `### 파트 4: 제목 (~2분, ~800자) — 7~9분 지점 고정`            ← 괄호 뒤 꼬리말
#   `### 파트 4: 제목 (~5분, ~2,000자) [크리에이터 분석 포함]`
# 예전 정규식은 괄호가 곧바로 "분"으로 시작할 때만 매칭돼 목표를 통째로 놓쳤고,
# 그 결과 뒤쪽 파트가 한 칸씩 밀려 엉뚱한 목표와 비교됐다.
_HEADER_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
_PAREN_RE = re.compile(r"\(([^()]*)\)")
# 분 또는 초 — 짧은 클로징은 `(~30초, ~200자)`로 적히기도 한다
_DURATION_RE = re.compile(r"[\d.]+\s*[분초]")
_CHARS_RE = re.compile(r"([\d,]+)\s*자")
# Hook/Intro 헤더는 목표 대상이 아니다 (draft에서도 sections[0]으로 따로 뺀다).
# 초 단위를 허용하므로 `### Hook (76자, ~11초)`를 걸러내는 건 이 제목 필터다.
#
# ⚠️ 부분 일치가 아니라 **완전 일치**다. "Hook", "Intro", "Hook & Intro", "훅", "인트로"만
# 걸러낸다. 예전에는 부분 일치라서 "파트 1: 진짜 훅이 뭐길래" 같은 본문 파트가 목표에서
# 조용히 사라졌고, 개수 불일치로 exit 2가 나면서도 원인을 알 수 없었다.
_HOOK_KEYWORD = r"(?:hook|훅|intro|인트로)"
_HOOK_TITLE_RE = re.compile(
    rf"^\s*{_HOOK_KEYWORD}(?:\s*[&+,·/와과]\s*{_HOOK_KEYWORD})*\s*$", re.IGNORECASE
)

# ── draft.md 섹션 파싱 (finalize.py 동일 로직) ────────────────
_SECTION_HEADER_RE = re.compile(r"^#{2}\s+(.*)$")
_ANY_HEADER_RE = re.compile(r"^#{1,6}\s+")
_HR_RE = re.compile(r"^-{3,}$")
_BLOCKQUOTE_RE = re.compile(r"^>.*$")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)


def parse_outline_targets(text: str) -> list[dict]:
    """outline.md에서 파트별 목표 글자수를 추출한다.

    Hook/Intro 헤더는 목표 대상이 아니므로 제외한다. 제목이 'Hook', 'Intro',
    'Hook & Intro' 처럼 **그 단어만으로 이루어졌을 때만** 제외한다 — 본문 파트 제목에
    '훅'이 우연히 들어갔다고 목표를 조용히 없애면 개수 불일치로 exit 2가 난다.
    """
    targets = []
    for m in _HEADER_RE.finditer(text):
        raw = m.group(1).strip()

        # 시간(분/초)과 "자"를 모두 담은 첫 괄호 그룹이 분량 표기다.
        for paren in _PAREN_RE.finditer(raw):
            inner = paren.group(1)
            if not _DURATION_RE.search(inner):
                continue
            chars = _CHARS_RE.search(inner)
            if not chars:
                continue

            title = raw[:paren.start()].strip()
            if _HOOK_TITLE_RE.match(title):
                break

            targets.append({
                "title": title,
                "chars": int(chars.group(1).replace(",", "")),
            })
            break
    return targets


def parse_draft_sections(text: str) -> list[dict]:
    """draft.md에서 ## 헤더 기준으로 섹션별 글자수를 측정한다."""
    text = _HTML_COMMENT_RE.sub("", text)

    sections: list[dict] = []
    current_label: str | None = None
    current_chars = 0
    prev_had_text = False

    def _flush():
        nonlocal current_label, current_chars, prev_had_text
        if current_label is not None:
            sections.append({"title": current_label, "chars": current_chars})
        current_label = None
        current_chars = 0
        prev_had_text = False

    for line in text.splitlines():
        stripped = line.strip()

        if _HR_RE.match(stripped):
            continue
        if _BLOCKQUOTE_RE.match(stripped):
            continue

        m = _SECTION_HEADER_RE.match(stripped)
        if m:
            _flush()
            current_label = m.group(1).strip()
            continue

        if _ANY_HEADER_RE.match(stripped):
            continue

        if stripped:
            if prev_had_text:
                current_chars += 1  # 줄 간 공백 구분자
            current_chars += len(stripped)
            prev_had_text = True

    _flush()
    return sections


def validate(
    outline_path: Path,
    draft_path: Path,
    threshold: float,
    max_threshold: float,
    total_max_threshold: float,
) -> int:
    """검증 실행. 종료 코드 반환."""
    outline_text = outline_path.read_text(encoding="utf-8")
    draft_text = draft_path.read_text(encoding="utf-8")

    targets = parse_outline_targets(outline_text)
    if not targets:
        print(f"ERROR: outline.md에서 파트별 목표를 추출하지 못했습니다: {outline_path}", file=sys.stderr)
        print("       파트 헤더 형식을 확인하세요: `### 파트 N: 제목 (~4분, ~1,650자)`", file=sys.stderr)
        return 2

    sections = parse_draft_sections(draft_text)
    if not sections:
        print(f"ERROR: draft.md에서 섹션을 감지하지 못했습니다: {draft_path}", file=sys.stderr)
        return 2

    # 첫 번째 섹션 = Hook & Intro (목표 없음, SKIP)
    hook = sections[0]
    body_sections = sections[1:]

    # 개수가 어긋나면 인덱스가 밀려 엉뚱한 목표와 비교된다.
    # 예전에는 WARNING만 찍고 비교를 강행해서, 파트4를 클로징 목표와 대조해
    # 220% 같은 허수를 만들고 진짜 클로징은 검증조차 안 됐다. 무조건 중단한다.
    if len(body_sections) != len(targets):
        print(
            f"ERROR: outline 목표 {len(targets)}개 vs draft 섹션(Hook 제외) {len(body_sections)}개 — 개수가 다릅니다.",
            file=sys.stderr,
        )
        print("       개수가 다르면 파트가 밀려 엉뚱한 목표와 비교되므로 검증을 중단합니다.", file=sys.stderr)
        print(f"       outline 목표: {[t['title'] for t in targets]}", file=sys.stderr)
        print(f"       draft 섹션  : {[s['title'] for s in body_sections]}", file=sys.stderr)
        print("       outline 파트 헤더의 글자수 표기 누락, 또는 draft에 outline에 없는 파트가 있는지 확인하세요.", file=sys.stderr)
        return 2

    # ── 결과 테이블 ──────────────────────────────────────────
    rows: list[dict] = []

    # Hook 행
    rows.append({
        "title": hook["title"],
        "target": None,
        "actual": hook["chars"],
        "ratio": None,
        "result": "SKIP",
    })

    # 본문 + 클로징 행 (개수 일치는 위에서 보장됨)
    for i in range(len(targets)):
        t = targets[i]
        s = body_sections[i]
        ratio = s["chars"] / t["chars"] if t["chars"] > 0 else 1.0
        if ratio < threshold:
            result = "FAIL(부족)"
        elif ratio > max_threshold:
            result = "FAIL(초과)"
        else:
            result = "PASS"
        rows.append({
            "title": s["title"],
            "target": t["chars"],
            "actual": s["chars"],
            "ratio": ratio,
            "result": result,
        })

    # ── 출력 ─────────────────────────────────────────────────
    col_w = max(len(r["title"]) for r in rows)
    col_w = max(col_w, 10)  # 최소 너비
    header = f"{'섹션':<{col_w}} | {'목표':>6} | {'실제':>6} | {'비율':>5} | 결과"
    sep = "─" * len(header)

    print(header)
    print(sep)
    for r in rows:
        target_str = f"{r['target']:>,}" if r["target"] is not None else "-"
        actual_str = f"{r['actual']:>,}"
        ratio_str = f"{r['ratio']:.0%}" if r["ratio"] is not None else "-"
        print(f"{r['title']:<{col_w}} | {target_str:>6} | {actual_str:>6} | {ratio_str:>5} | {r['result']}")
    print(sep)

    # ── 총합 ─────────────────────────────────────────────────
    # Hook은 outline에 목표가 없으므로 비율 계산에서 제외한다.
    # (예전에는 Hook 글자수를 분자에만 넣어 비율이 부풀려 보였다.)
    total_target = sum(t["chars"] for t in targets)
    body_actual = sum(s["chars"] for s in body_sections)
    total_ratio = body_actual / total_target if total_target > 0 else 0
    print(f"본문 총합: {body_actual:,} / {total_target:,} ({total_ratio:.0%})")

    script_chars = hook["chars"] + body_actual
    print(f"대본 전체: {script_chars:,}자 (Hook 포함) → 약 {script_chars / 440:.1f}분")

    short_parts = [r["title"] for r in rows if r["result"] == "FAIL(부족)"]
    over_parts = [r["title"] for r in rows if r["result"] == "FAIL(초과)"]
    total_over = total_ratio > total_max_threshold

    if short_parts:
        print(f"FAIL(부족) 섹션: {', '.join(short_parts)}")
    if over_parts:
        print(f"FAIL(초과) 섹션: {', '.join(over_parts)}")
    if total_over:
        print(
            f"FAIL(총합 초과): 본문 총합이 목표의 {total_ratio:.0%}로 "
            f"상한 {total_max_threshold:.0%}를 넘었습니다. 파트별로는 통과해도 "
            f"골고루 부풀면 러닝타임이 넘칩니다 — 압축 후 재검증하세요."
        )

    if short_parts or over_parts or total_over:
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="draft.md 파트별 분량 검증")
    parser.add_argument("outline", type=Path, help="outline.md 경로")
    parser.add_argument("draft", type=Path, help="draft.md 경로")
    parser.add_argument("--threshold", type=float, default=0.9, help="파트별 하한 비율 (기본 0.9)")
    parser.add_argument(
        "--max-threshold", type=float, default=1.3,
        help="파트별 상한 비율 (기본 1.3 — 폭주 감지용. 조이면 압축 라운드가 매번 돈다)",
    )
    parser.add_argument(
        "--total-max-threshold", type=float, default=1.2,
        help="본문 총합 상한 비율 (기본 1.2 — 파트가 골고루 부푸는 것을 잡는다)",
    )
    args = parser.parse_args()

    if not args.outline.exists():
        print(f"ERROR: outline.md를 찾을 수 없습니다: {args.outline}", file=sys.stderr)
        sys.exit(2)
    if not args.draft.exists():
        print(f"ERROR: draft.md를 찾을 수 없습니다: {args.draft}", file=sys.stderr)
        sys.exit(2)

    sys.exit(validate(
        args.outline, args.draft,
        args.threshold, args.max_threshold, args.total_max_threshold,
    ))


if __name__ == "__main__":
    main()
