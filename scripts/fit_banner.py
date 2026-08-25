#!/usr/bin/env python3
"""
완성된 배너 이미지를 유튜브 「모든 기기 안전영역」에 맞추되,
배경이 캔버스 끝까지 경계선 없이 이어지게 만든다.

규격 (2026 확인):
  업로드   2560 x 1440 (16:9) · 최소 2048x1152 · 최대 6MB
  TV       2560 x 1440 전체
  데스크톱  2560 x 423
  모바일   1546 x 423   ← 모든 기기 공통

핵심 아이디어:
  1) 원본에서 **콘텐츠 띠(3.655:1)만** 잘라낸다.
     원본에 이미 들어 있는 위아래 여백은 버린다 — 이걸 남기면 경계선이 그대로 보인다.
  2) 그 띠를 안전영역(1546x423)에 1:1로 앉힌다 → 모바일에서 절대 안 잘린다.
  3) **띠 자신의 가장자리 픽셀을 늘려** 캔버스 바깥을 채운다.
     늘리는 소스가 띠 자체이므로 색이 그대로 이어져 경계가 생기지 않는다.
  4) 늘린 영역에 세로 그라데이션 블러를 줘 결(밴딩)을 지운다.

사용:
    python scripts/fit_banner.py <입력이미지> [출력경로] [--offset N] [--hard]

    --offset N : 잘라낼 띠의 세로 중심을 N픽셀 이동(원본 기준). +면 아래로
    --hard     : 늘린 영역 블러를 끄고 픽셀을 그대로 늘린다
"""
import os
import sys
from PIL import Image, ImageFilter

CANVAS_W, CANVAS_H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SAFE_X = (CANVAS_W - SAFE_W) // 2      # 507
SAFE_Y = (CANVAS_H - SAFE_H) // 2      # 508
SAFE_RATIO = SAFE_W / SAFE_H           # 3.655
MAX_BYTES = 6 * 1024 * 1024


def build(src_path, out_path, offset=0, hard=False):
    src = Image.open(src_path).convert("RGB")
    W, H = src.size

    # ---- 1) 콘텐츠 띠만 잘라낸다 (원본의 위아래 여백은 버린다) ----
    band_w = W
    band_h = round(W / SAFE_RATIO)
    if band_h > H:
        band_h, band_w = H, round(H * SAFE_RATIO)

    cy = H // 2 + offset
    top = max(0, min(H - band_h, cy - band_h // 2))
    left = max(0, min(W - band_w, W // 2 - band_w // 2))
    band = src.crop((left, top, left + band_w, top + band_h)).resize((SAFE_W, SAFE_H), Image.LANCZOS)

    # ---- 2) 안전영역에 1:1 배치 ----
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H))
    canvas.paste(band, (SAFE_X, SAFE_Y))

    # ---- 3) 띠 자신의 가장자리를 늘려 바깥을 채운다 ----
    up_h, dn_h = SAFE_Y, CANVAS_H - (SAFE_Y + SAFE_H)
    canvas.paste(band.crop((0, 0, SAFE_W, 1)).resize((SAFE_W, up_h), Image.BILINEAR), (SAFE_X, 0))
    canvas.paste(band.crop((0, SAFE_H - 1, SAFE_W, SAFE_H)).resize((SAFE_W, dn_h), Image.BILINEAR),
                 (SAFE_X, SAFE_Y + SAFE_H))

    lf_w, rt_w = SAFE_X, CANVAS_W - (SAFE_X + SAFE_W)
    canvas.paste(canvas.crop((SAFE_X, 0, SAFE_X + 1, CANVAS_H)).resize((lf_w, CANVAS_H), Image.BILINEAR), (0, 0))
    canvas.paste(canvas.crop((SAFE_X + SAFE_W - 1, 0, SAFE_X + SAFE_W, CANVAS_H)).resize((rt_w, CANVAS_H), Image.BILINEAR),
                 (SAFE_X + SAFE_W, 0))

    # ---- 4) 바깥을 강하게 뭉개고, 띠 가장자리를 페이드로 녹여 넣는다 ----
    if not hard:
        canvas = canvas.filter(ImageFilter.GaussianBlur(radius=90))

        # 띠 가장자리 feather 마스크 — 중앙은 불투명, 테두리로 갈수록 투명
        feather = 34
        mask = Image.new("L", (SAFE_W, SAFE_H), 255)
        mp = mask.load()
        for i in range(feather):
            v = int(255 * (i / feather) ** 0.7)
            for x in range(SAFE_W):
                mp[x, i] = min(mp[x, i], v)
                mp[x, SAFE_H - 1 - i] = min(mp[x, SAFE_H - 1 - i], v)
            for y in range(SAFE_H):
                mp[i, y] = min(mp[i, y], v)
                mp[SAFE_W - 1 - i, y] = min(mp[SAFE_W - 1 - i, y], v)
        canvas.paste(band, (SAFE_X, SAFE_Y), mask)

    # ---- 5) 저장 ----
    for q in (95, 90, 85, 80, 72):
        canvas.save(out_path, "JPEG", quality=q, optimize=True)
        if os.path.getsize(out_path) <= MAX_BYTES:
            break

    print(f"저장: {out_path}")
    print(f"  원본 {W}x{H} → 잘라낸 띠 {band_w}x{band_h} (원본 y {top}~{top+band_h}, offset={offset})")
    print(f"  띠를 안전영역 {SAFE_W}x{SAFE_H} 에 1:1 배치 — 모바일에서 잘리지 않습니다")
    print(f"  바깥은 띠 자신의 가장자리를 늘려 채움 (위 {up_h}px · 아래 {dn_h}px · 좌우 {lf_w}px)")
    print(f"  {'가장자리 블러 없음(--hard)' if hard else '늘린 영역만 블러 처리 → 경계선·밴딩 없음'}")
    print(f"  캔버스 {CANVAS_W}x{CANVAS_H} · {os.path.getsize(out_path)/1024/1024:.2f}MB (상한 6MB)")
    print("  → 콘텐츠가 위아래로 잘렸으면 --offset 으로 띠 중심을 옮기세요.")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    offset, hard, pos = 0, False, []
    i = 0
    while i < len(args):
        if args[i] == "--offset":
            offset = int(args[i + 1]); i += 2
        elif args[i] == "--hard":
            hard = True; i += 1
        else:
            pos.append(args[i]); i += 1
    src = pos[0]
    out = pos[1] if len(pos) > 1 else os.path.splitext(src)[0] + "_banner_2560x1440.jpg"
    build(src, out, offset, hard)


if __name__ == "__main__":
    main()
