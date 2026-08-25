#!/usr/bin/env python3
"""
유튜브 채널 배너를 코드로 조립한다. 안전영역 초과가 구조적으로 불가능하다.

규격 (2026 확인):
  업로드   2560 x 1440 (16:9), 최소 2048x1152, 최대 6MB
  TV       2560 x 1440  전체
  데스크톱  2560 x 423
  모바일   1546 x 423   ← 모든 기기 공통. 중요한 건 전부 여기 안에

사용:
    python scripts/make_banner.py <캐릭터이미지> [출력경로]

  <캐릭터이미지> : 마스코트가 그려진 아무 이미지(프로필용 정사각이어도 되고,
                  앞서 만든 배너여도 된다). 배경은 자동으로 어둡게 깔리므로
                  캐릭터가 크게 보이는 이미지일수록 좋다.

동작:
  1) 2560x1440 캔버스에 진한 네이비 배경 + 왼쪽 따뜻한 주황 글로우
  2) 캐릭터 이미지를 안전영역 높이(423px)의 92% 이하로 축소해 안전영역 '왼쪽'에 배치
  3) 한글 2줄을 안전영역 '오른쪽'에 배치. 폰트 크기는 자동으로 줄여 절대 넘치지 않게 함
  4) 배치 후 모든 요소가 안전영역 안인지 검증해 출력
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SAFE_X = (CANVAS_W - SAFE_W) // 2          # 507
SAFE_Y = (CANVAS_H - SAFE_H) // 2          # 508
MAX_BYTES = 6 * 1024 * 1024

LINE1 = "내 돈이 어떻게 되는지"
LINE2 = "쉬운 말로"

NAVY = (16, 22, 43)
GLOW = (94, 52, 18)
CREAM = (255, 244, 224)

FONT_CANDIDATES = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "C:/Windows/Fonts/malgunbd.ttf",
    "C:/Windows/Fonts/malgun.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size, index=(2 if path.endswith(".ttc") else 0))
            except Exception:
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    raise SystemExit("한글 폰트를 찾지 못했습니다. FONT_CANDIDATES에 경로를 추가하세요.")


def make_background():
    """진한 네이비 + 왼쪽에서 들어오는 따뜻한 주황 글로우."""
    bg = Image.new("RGB", (CANVAS_W, CANVAS_H), NAVY)
    px = bg.load()
    for x in range(CANVAS_W):
        t = max(0.0, 1.0 - (x / (CANVAS_W * 0.42)))     # 왼쪽 42%까지 글로우
        t = t * t
        r = int(NAVY[0] + (GLOW[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (GLOW[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (GLOW[2] - NAVY[2]) * t)
        for y in range(CANVAS_H):
            px[x, y] = (r, g, b)
    return bg


def trim_borders(im, tol=18):
    """캐릭터 이미지 주변의 단색 여백을 잘라내 실제 그림만 남긴다."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    corner = rgb.getpixel((1, 1))

    def close(p):
        return all(abs(p[i] - corner[i]) <= tol for i in range(3))

    left, right, top, bottom = 0, w - 1, 0, h - 1
    while left < right and all(close(rgb.getpixel((left, y))) for y in range(0, h, max(1, h // 60))):
        left += 1
    while right > left and all(close(rgb.getpixel((right, y))) for y in range(0, h, max(1, h // 60))):
        right -= 1
    while top < bottom and all(close(rgb.getpixel((x, top))) for x in range(0, w, max(1, w // 60))):
        top += 1
    while bottom > top and all(close(rgb.getpixel((x, bottom))) for x in range(0, w, max(1, w // 60))):
        bottom -= 1
    if right - left < 40 or bottom - top < 40:
        return im
    return im.crop((left, top, right + 1, bottom + 1))


def chroma_key(im, key=(255, 0, 255), tol=110):
    """마젠타 단색 배경을 투명하게 만들고, 남은 그림 영역만 잘라낸다."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # 마젠타 판정: R·B가 높고 G가 낮다
            if r > 150 and b > 150 and g < 120 and abs(r - b) < 90:
                px[x, y] = (r, g, b, 0)
            else:
                if x < minx: minx = x
                if y < miny: miny = y
                if x > maxx: maxx = x
                if y > maxy: maxy = y
    if maxx < 0:
        return im
    return im.crop((minx, miny, maxx + 1, maxy + 1))


def build(src_path, out_path):
    canvas = make_background()

    # ---- 캐릭터: 마젠타 배경 제거 후 안전영역 높이의 92% 이하 ----
    ch = Image.open(src_path).convert("RGBA")
    # 마젠타 픽셀이 화면의 15% 이상이면 크로마키로 처리, 아니면 단색 여백만 잘라낸다
    small = ch.resize((120, max(1, round(120 * ch.height / ch.width))))
    sp = small.load()
    mg = sum(1 for yy in range(small.height) for xx in range(small.width)
             if sp[xx, yy][0] > 150 and sp[xx, yy][2] > 150 and sp[xx, yy][1] < 120)
    if mg / (small.width * small.height) > 0.15:
        ch = chroma_key(ch)
    else:
        ch = trim_borders(ch)
    target_h = int(SAFE_H * 0.92)                       # 389px
    scale = target_h / ch.height
    ch_w, ch_h = max(1, round(ch.width * scale)), target_h
    # 캐릭터가 안전영역 폭의 42%를 넘지 않게 한 번 더 제한
    max_ch_w = int(SAFE_W * 0.42)
    if ch_w > max_ch_w:
        scale2 = max_ch_w / ch_w
        ch_w, ch_h = max_ch_w, max(1, round(ch_h * scale2))
    ch = ch.resize((ch_w, ch_h), Image.LANCZOS)

    ch_x = SAFE_X + 24
    ch_y = SAFE_Y + (SAFE_H - ch_h) // 2
    canvas.paste(ch, (ch_x, ch_y), ch if ch.mode == "RGBA" else None)

    # ---- 텍스트: 안전영역 오른쪽. 넘치면 자동 축소 ----
    text_x = ch_x + ch_w + 48
    text_avail_w = SAFE_X + SAFE_W - text_x - 24
    text_avail_h = SAFE_H - 32

    draw = ImageDraw.Draw(canvas)
    size = 190
    while size > 40:
        f1 = load_font(size)
        f2 = load_font(int(size * 1.18))               # 둘째 줄을 더 크게
        b1 = draw.textbbox((0, 0), LINE1, font=f1)
        b2 = draw.textbbox((0, 0), LINE2, font=f2)
        w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
        w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
        gap = int(size * 0.30)
        if max(w1, w2) <= text_avail_w and (h1 + gap + h2) <= text_avail_h:
            break
        size -= 6

    total_h = h1 + gap + h2
    ty = SAFE_Y + (SAFE_H - total_h) // 2

    def shadowed(x, y, text, font):
        for dx, dy in ((3, 3), (3, -3), (-3, 3), (-3, -3)):
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=CREAM)

    shadowed(text_x - b1[0], ty - b1[1], LINE1, f1)
    shadowed(text_x - b2[0], ty + h1 + gap - b2[1], LINE2, f2)

    # ---- 저장 ----
    for q in (95, 90, 85, 80, 72):
        canvas.save(out_path, "JPEG", quality=q, optimize=True)
        if os.path.getsize(out_path) <= MAX_BYTES:
            break

    # ---- 검증 ----
    right_edge = max(text_x + w1, text_x + w2)
    ok_ch = (ch_x >= SAFE_X and ch_x + ch_w <= SAFE_X + SAFE_W
             and ch_y >= SAFE_Y and ch_y + ch_h <= SAFE_Y + SAFE_H)
    ok_tx = (text_x >= SAFE_X and right_edge <= SAFE_X + SAFE_W
             and ty >= SAFE_Y and ty + total_h <= SAFE_Y + SAFE_H)

    print(f"저장: {out_path}")
    print(f"  캔버스 {CANVAS_W}x{CANVAS_H} · {os.path.getsize(out_path)/1024/1024:.2f}MB (상한 6MB)")
    print(f"  안전영역 x {SAFE_X}~{SAFE_X+SAFE_W} · y {SAFE_Y}~{SAFE_Y+SAFE_H}")
    print(f"  캐릭터  x {ch_x}~{ch_x+ch_w} · y {ch_y}~{ch_y+ch_h}   {'OK' if ok_ch else '초과!'}")
    print(f"  텍스트  x {text_x}~{right_edge} · y {ty}~{ty+total_h}  글자크기 {size}  {'OK' if ok_tx else '초과!'}")
    if ok_ch and ok_tx:
        print("  → 모든 요소가 「모든 기기에 표시 가능」 영역 안에 있습니다.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + "_banner_2560x1440.jpg"
    build(src, out)


if __name__ == "__main__":
    main()
