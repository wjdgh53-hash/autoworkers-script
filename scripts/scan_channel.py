#!/usr/bin/env python3
"""
채널 전편 스캔 → TSV 저장 → 시점 보정 배수 계산.

사용:
    python scan_channel.py <채널URL> <저장이름> [최대편수]

산출: <저장이름>.tsv  (id, upload_date, view_count, duration, title)
      화면에는 「시점 보정 배수」 상위 목록을 출력.

시점 보정 배수 = 그 영상 조회수 ÷ (같은 채널에서 업로드일 ±window_days 안에 올라온 편들의 조회수 중앙값)
  - 분모에서 자기 자신은 제외한다 (이상치가 자기 분모를 부풀리는 것을 막는다)
  - ±window 안에 이웃이 3편 미만이면 window를 2배로 넓혀 재시도, 그래도 부족하면 NA
"""
import subprocess
import statistics
import sys
import os
from datetime import datetime

VENV_YTDLP = os.path.join(os.getcwd(), ".venv", "bin", "yt-dlp")
if not os.path.exists(VENV_YTDLP):  # Windows
    VENV_YTDLP = os.path.join(os.getcwd(), ".venv", "Scripts", "yt-dlp.exe")

FIELDS = "%(id)s\t%(upload_date)s\t%(view_count)s\t%(duration)s\t%(title)s"
WINDOW_DAYS = 21


def scan(channel_url, limit):
    """채널 videos 탭을 전체 추출한다. flat-playlist는 조회수가 NA로 나와서 쓰지 않는다."""
    url = channel_url.rstrip("/") + "/videos"
    cmd = [
        VENV_YTDLP, "--no-warnings", "--ignore-errors",
        "--extractor-args", "youtube:lang=ko",
        "--playlist-end", str(limit),
        "--print", FIELDS,
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    rows = []
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        vid, date, views, dur, title = parts[0], parts[1], parts[2], parts[3], "\t".join(parts[4:])
        if not date.isdigit() or not views.isdigit():
            continue
        rows.append({
            "id": vid,
            "date": date,
            "views": int(views),
            "dur": int(dur) if dur.isdigit() else 0,
            "title": title,
        })
    if not rows:
        sys.stderr.write(proc.stderr[-2000:] + "\n")
    return rows


def days_between(a, b):
    fa = datetime.strptime(a, "%Y%m%d")
    fb = datetime.strptime(b, "%Y%m%d")
    return abs((fa - fb).days)


def time_adjusted_multiple(rows, window=WINDOW_DAYS):
    """각 편의 시점 보정 배수를 계산해 rows에 mult/denom/n을 채운다."""
    for r in rows:
        for w in (window, window * 2):
            neighbors = [
                o["views"] for o in rows
                if o["id"] != r["id"] and days_between(o["date"], r["date"]) <= w
            ]
            if len(neighbors) >= 3:
                denom = statistics.median(neighbors)
                r["denom"] = denom
                r["n"] = len(neighbors)
                r["window"] = w
                r["mult"] = round(r["views"] / denom, 1) if denom else None
                break
        else:
            r["denom"], r["n"], r["window"], r["mult"] = None, 0, None, None
    return rows


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    channel_url, name = sys.argv[1], sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 60

    rows = scan(channel_url, limit)
    if not rows:
        print(f"[{name}] 수집 실패 — 0편. 임의 진행하지 말 것.")
        sys.exit(2)

    rows = time_adjusted_multiple(rows)
    out = f"{name}.tsv"
    with open(out, "w", encoding="utf-8") as f:
        f.write("id\tdate\tviews\tdur\tmult\tdenom\tn\ttitle\n")
        for r in sorted(rows, key=lambda x: x["date"], reverse=True):
            f.write(f"{r['id']}\t{r['date']}\t{r['views']}\t{r['dur']}\t"
                    f"{r['mult']}\t{r['denom']}\t{r['n']}\t{r['title']}\n")

    overall_median = statistics.median([r["views"] for r in rows])
    print(f"\n=== {name} · {len(rows)}편 · 전체 중앙값 {overall_median:,.0f} · 저장 {out} ===")
    print(f"기간: {min(r['date'] for r in rows)} ~ {max(r['date'] for r in rows)}")
    print("\n--- 시점 보정 배수 상위 15 ---")
    ranked = [r for r in rows if r["mult"] is not None]
    ranked.sort(key=lambda x: x["mult"], reverse=True)
    for r in ranked[:15]:
        mins = f"{r['dur']//60}:{r['dur']%60:02d}"
        print(f"{r['mult']:>7.1f}x | {r['views']:>8,} | {r['date']} | {mins:>6} | "
              f"분모{r['denom']:>8,.0f}(n={r['n']}) | {r['title'][:52]}")
    print("\n--- 최근 8편 (건전성 확인용) ---")
    for r in sorted(rows, key=lambda x: x["date"], reverse=True)[:8]:
        mins = f"{r['dur']//60}:{r['dur']%60:02d}"
        m = f"{r['mult']:.1f}x" if r["mult"] is not None else "  NA"
        print(f"{m:>7} | {r['views']:>8,} | {r['date']} | {mins:>6} | {r['title'][:52]}")


if __name__ == "__main__":
    main()
