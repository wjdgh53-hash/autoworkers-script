#!/usr/bin/env python3
"""세션 실제 비용 측정 — Claude Code 세션 로그의 토큰 사용량을 읽어 모델별로 집계한다.

`/cost`를 사람이 확인해 옮겨 적을 필요가 없다. Claude Code가
`~/.claude/projects/{프로젝트}/{세션ID}.jsonl`에 요청마다 usage를 기록하므로 그걸 읽는다.

사용법:
  python scripts/src/measure_cost.py                # 최근 세션
  python scripts/src/measure_cost.py --list         # 세션 목록 (어느 세션이 대본인지 고를 때)
  python scripts/src/measure_cost.py --session {ID} # 특정 세션
  python scripts/src/measure_cost.py --all          # 전 세션 합계 + 세션별 표

단가 (2026-08-17 기준, Anthropic 1st-party API, 100만 토큰당):
  Opus 5     $5 입력 / $25 출력
  Sonnet 5   $2 입력 / $10 출력  ← 2026-08-31까지 도입가. 이후 $3 / $15
  Haiku 4.5  $1 입력 / $5 출력
  캐시 읽기 = 입력 × 0.1 / 캐시 쓰기 = 입력 × 2.0 (1시간 TTL) 또는 × 1.25 (5분 TTL)

⚠️ 단가는 바뀔 수 있다. 큰 금액을 판단할 때는 platform.claude.com/docs/en/pricing 확인.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys

# 100만 토큰당 USD — (입력, 출력)
PRICING = {
    "claude-opus-5": (5.0, 25.0),
    "claude-opus-4-8": (5.0, 25.0),
    "claude-sonnet-5": (2.0, 10.0),   # 도입가. 2026-09-01부터 (3.0, 15.0)
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}
CACHE_READ_MULT = 0.1
CACHE_WRITE_MULT_1H = 2.0
CACHE_WRITE_MULT_5M = 1.25


def project_dir() -> str:
    """현재 작업 폴더에 대응하는 Claude Code 로그 디렉토리를 찾는다."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Claude Code는 경로의 비영문·구분자를 '-'로 치환해 디렉토리명을 만든다.
    # 정확한 규칙에 의존하지 않고, 후보 중 가장 최근에 쓰인 것을 고른다.
    base = os.path.expanduser("~/.claude/projects")
    leaf = os.path.basename(root)
    cands = [d for d in glob.glob(os.path.join(base, "*")) if os.path.isdir(d) and d.endswith(leaf)]
    if not cands:
        cands = [d for d in glob.glob(os.path.join(base, "*")) if os.path.isdir(d)]
    if not cands:
        print("세션 로그 디렉토리를 찾지 못했습니다.", file=sys.stderr)
        sys.exit(1)
    return max(cands, key=os.path.getmtime)


def price(model: str, c: collections.Counter) -> tuple[float, bool]:
    """(비용 USD, 단가를 알고 있는지)."""
    key = next((k for k in PRICING if model.startswith(k)), None)
    if key is None:
        return 0.0, False
    pin, pout = PRICING[key]
    w1h, w5m = c["cache_write_1h"], c["cache_write_5m"]
    # 세부 내역이 없으면 전체를 1시간 TTL로 본다(보수적 — 더 비싼 쪽)
    if w1h == 0 and w5m == 0:
        w1h = c["cache_creation_input_tokens"]
    cost = (
        c["input_tokens"] * pin
        + c["output_tokens"] * pout
        + c["cache_read_input_tokens"] * pin * CACHE_READ_MULT
        + w1h * pin * CACHE_WRITE_MULT_1H
        + w5m * pin * CACHE_WRITE_MULT_5M
    ) / 1_000_000
    return cost, True


def scan(path: str) -> dict[str, collections.Counter]:
    """세션 파일 1개를 모델별 usage로 집계한다."""
    agg: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = d.get("message")
            if not isinstance(msg, dict) or "usage" not in msg:
                continue
            u = msg["usage"]
            if not isinstance(u, dict):
                continue
            c = agg[msg.get("model", "(unknown)")]
            for k in ("input_tokens", "output_tokens",
                      "cache_creation_input_tokens", "cache_read_input_tokens"):
                c[k] += u.get(k) or 0
            cc = u.get("cache_creation")
            if isinstance(cc, dict):
                c["cache_write_1h"] += cc.get("ephemeral_1h_input_tokens") or 0
                c["cache_write_5m"] += cc.get("ephemeral_5m_input_tokens") or 0
            c["requests"] += 1
    return agg


def report(agg: dict[str, collections.Counter], label: str) -> float:
    print(f"\n{'=' * 74}\n  {label}\n{'=' * 74}")
    if not agg:
        print("  usage 기록이 없습니다.")
        return 0.0
    total = 0.0
    unknown = []
    for model, c in sorted(agg.items(), key=lambda kv: -sum(kv[1].values())):
        cost, known = price(model, c)
        total += cost
        if not known:
            unknown.append(model)
        print(f"\n  {model}  ({c['requests']:,}회 요청)"
              + ("" if known else "   ⚠️ 단가 미등록 — 비용 0으로 집계"))
        print(f"    {'입력':<22}{c['input_tokens']:>14,}")
        print(f"    {'출력':<22}{c['output_tokens']:>14,}")
        print(f"    {'캐시 쓰기':<21}{c['cache_creation_input_tokens']:>14,}")
        print(f"    {'캐시 읽기':<21}{c['cache_read_input_tokens']:>14,}")
        if known:
            print(f"    {'→ 비용':<21}{'$' + format(cost, ',.2f'):>14}")
    print(f"\n  {'합계':<23}{'$' + format(total, ',.2f'):>14}")
    if unknown:
        print(f"  ⚠️ 단가를 모르는 모델이 있어 합계가 실제보다 낮습니다: {', '.join(unknown)}")
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", help="세션 ID 또는 jsonl 경로")
    ap.add_argument("--all", action="store_true", help="전 세션")
    ap.add_argument("--list", action="store_true", help="세션 목록만")
    args = ap.parse_args()

    d = project_dir()
    files = sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime, reverse=True)
    if not files:
        print("세션 파일이 없습니다.", file=sys.stderr)
        return 1

    if args.list:
        import datetime
        print(f"{'수정시각':<20}{'크기':>10}  세션 ID")
        for f in files[:30]:
            ts = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M")
            print(f"{ts:<20}{os.path.getsize(f) // 1024:>8,}KB  {os.path.basename(f)[:-6]}")
        return 0

    if args.all:
        grand = 0.0
        for f in files:
            grand += report(scan(f), os.path.basename(f)[:-6])
        print(f"\n{'=' * 74}\n  전 세션 합계: ${grand:,.2f}  ({len(files)}개 세션)\n{'=' * 74}")
        return 0

    if args.session:
        target = args.session if args.session.endswith(".jsonl") else os.path.join(d, args.session + ".jsonl")
        if not os.path.exists(target):
            print(f"세션을 찾지 못했습니다: {target}", file=sys.stderr)
            return 1
    else:
        target = files[0]

    report(scan(target), os.path.basename(target)[:-6])
    return 0


if __name__ == "__main__":
    sys.exit(main())
