# 채널 브랜딩 — 방구석 경제 (2026-08-21 리세팅)

> 대상 [방구석 경제](https://www.youtube.com/channel/UCrNcQ8S9iPujI8ZGxquAhlA) · 구독 6,370 · 핸들 `@방구석economy`
> 근거 [_diagnosis/2026-08-21_방구석economy.md](../_diagnosis/2026-08-21_방구석economy.md) · 축 [direction.md](../direction.md)
>
> 🔴 **채널명 「방구석 경제」와 핸들은 바꾸지 않는다.** 이름은 이미 「내 방, 내 돈」을 정확히 가리킨다.
> **문제는 이름이 아니라 이름과 이미지가 따로 논다는 것이다.**

---

## 1. 왜 바꾸나 — 기존 프로필이 다른 채널을 가리킨다

기존 프로필: **검정 가죽 배경 + 금테 원 + 지구본 + 스마트폰 + 나침반 + 그리스 신전 + 두루마리**

| 요소 | 읽히는 것 | 현재 축과 |
|---|---|---|
| 지구본·나침반 | 세계 정세·국제 경제 | ❌ 내 돈이 아니다 |
| 그리스 신전·두루마리 | 역사·고전 | ❌ **1기(방구석 역사) 잔재** |
| 금테 + 검정 가죽 | 권위·고급·거리감 | ❌ 친근함의 반대 |

**이것은 CTR과 직결된다.** 추천 피드에서 썸네일 옆에 이 아이콘이 붙는다.
「금융자산 10억이 생기면」 같은 제목 옆에 지구본·신전이 있으면 시청자가 0.3초 만에 "내 얘기 아니네"로 넘긴다.
[08-20 편 CTR 2.1%](https://www.youtube.com/watch?v=j_8XiFOQsW0)의 한 원인으로 본다.

---

## 2. 프로필 이미지

### 🔴 톤 통일 원칙과 그 예외

**얼굴 사양은 [thumbnail-illustration.md](thumbnail-illustration.md) §3 마스코트와 100% 동일하다.** 썸네일에 나오는 그 캐릭터가 그대로 채널 얼굴이 된다.

⛔ **단, 「화면이 붐빈다(CROWDED)」는 썸네일 규칙을 여기 적용하지 않는다. 정반대로 간다.**

| | 썸네일 | 프로필 |
|---|---|---|
| 밀도 | 카드·차트·상징물로 꽉 채운다 | **얼굴 하나. 배경은 단색+글로우** |
| 텍스트 | 2줄 필수 | **없음** |
| 표시 크기 | 320×180 이상 | **댓글 24px · 피드 36px** |

**근거**: 프로필은 유튜브가 **정사각을 원형으로 잘라** 아주 작게 띄운다. 소품을 넣으면 24px에서 회색 얼룩이 된다.

### 📐 유튜브 프로필 이미지 규격 (반드시 맞춘다)

| 항목 | 값 |
|---|---|
| **권장 크기** | **800 × 800 px (1:1 정사각)** |
| 최소 크기 | 98 × 98 px |
| 파일 형식 | PNG · JPG · GIF(비애니메이션) |
| 용량 | **2MB 이하** |
| 표시 방식 | **정사각을 원형으로 잘라** 표시 — 모서리는 반드시 버려진다 |
| 실제 표시 크기 | 댓글 **24px** · 추천 피드 **36px** · 채널 홈 **80~144px** |

> **작업 순서**: 나노바나나에서 **1:1로 1024×1024 이상** 생성 → **800×800으로 리사이즈** → PNG 저장(2MB 이하) → 업로드.
> ⚠️ 생성 모델은 픽셀 수치를 정확히 지키지 못한다. **비율(1:1)만 프롬프트로 강제하고 크기는 리사이즈로 맞춘다.**

### 🚨 1차 실패 기록 (2026-08-21) — 실사 사진이 나왔다

첫 프롬프트가 **실사 인물 사진**을 뱉었다. 원인 3개 전부 내 작성 실수였다.

| 원인 | 왜 |
|---|---|
| `believable material shading` | [thumbnail-illustration.md](thumbnail-illustration.md) §2가 **명시적으로 금지한 어휘**다(62행). 그걸 내가 썼다 |
| `portrait` | 이미지 모델에서 **인물 사진**을 직접 유도하는 단어다 |
| 스타일 지시가 맨 뒤 | 프롬프트가 길어 `HIGHEST PRIORITY`(구도) 뒤에 스타일이 묻혔다. **매체(medium)를 첫 줄에 박아야 한다** |

> 🔴 **교훈: 프롬프트 첫 문장이 매체를 확정한다.** 구도·규격은 그다음이다.
> ⛔ 금지 어휘 재확인 — `photograph` · `photo` · `portrait` · `photorealistic` · `realistic` · `believable` · `documentary` · `35mm` · `f/2.8` · `skin texture` · `bokeh` · `studio lighting`

### 3안 공통 블록 — 아래 세 시안 모두 이 블록으로 시작한다

```
A flat cartoon mascot character illustration, hand-drawn digital art in the style of Korean
finance-explainer YouTube thumbnails. This is a DRAWING, not a photo. Square 1:1 aspect ratio.

NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin
pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh,
studio photo lighting.

CHARACTER — draw exactly this, nothing else: a large smooth round OFF-WHITE head shaped like a
simple ball, completely BALD with NO hair whatsoever and NO nose, drawn with a thick clean BLACK
OUTLINE around the whole head, flat cel shading inside, and it is the brightest thing in the
picture. Two big round WHITE eyes with solid round black pupils and simple drawn eyelids, looking
straight at the viewer. Thick solid BLACK eyebrows drawn as two bold shapes above the eyes. A
mouth drawn as a simple bold line. A small simple cartoon body in a flat deep-navy suit jacket
over a white collar, only the shoulders visible along the bottom edge, hands drawn as simple
rounded mitten shapes.

COMPOSITION: the head sits exactly in the centre of the square and fills about 65% of the frame
height, with generous empty margin on all four sides, because the square will be cropped into a
circle and every corner will be discarded. Nothing important may touch the outer edge. There is
no lettering anywhere in the image.

COLOUR: bold flat poster colours with a warm golden glow — warm gold and orange background,
off-white face, deep navy clothing, black outlines. Simple cel-shaded highlight on the upper left
of the head and a soft flat shadow on the lower right. Clean and uncluttered, and instantly
readable when shrunk to 24 pixels.
```

### 🅐 A안 — 웃는 얼굴 단독 **(추천)**

가장 안전하다. 24px에서도 「웃는 얼굴」로 읽힌다. 소품이 없어 얼룩질 여지가 없다.

```
[공통 블록]

EXPRESSION: the thick black eyebrows are drawn raised in a relaxed friendly arch, and the mouth
is drawn as a wide upward-curving smile. The face reads as calm and welcoming.

BACKGROUND: one flat warm gold colour with a soft radial glow directly behind the head. No props,
no scenery, no objects of any kind.
```

### 🅑 B안 — 손 인사

친근함이 가장 강하다. 채널 홈(80~144px)에서 좋지만 **24px에서는 손이 얼룩으로 보일 수 있다.**

```
[공통 블록]

EXPRESSION: the thick black eyebrows are drawn raised in a relaxed friendly arch, and the mouth
is drawn as a wide upward-curving smile.

POSE: one simple mitten-shaped cartoon hand is raised beside the head in a small friendly wave,
palm toward the viewer, kept clear of the face and well inside the circular crop area.

BACKGROUND: one flat warm gold colour with a soft radial glow directly behind the head. No props,
no scenery.
```

### 🅒 C안 — 얼굴 + 금화 한 닢

**경제 채널이라는 정체성을 아이콘 하나로 말한다.** 셋 중 정체성이 가장 선명하지만 24px 리스크가 가장 크다.

```
[공통 블록]

EXPRESSION: the thick black eyebrows are drawn raised in a relaxed friendly arch, and the mouth
is drawn as a wide upward-curving smile.

PROP: exactly one large flat round gold coin, blank and without any lettering, held up beside the
head by a simple mitten-shaped cartoon hand. The coin is big and simple enough to read as a plain
gold circle at 24 pixels. There is nothing else in the frame.

BACKGROUND: one flat deep-navy colour with a soft warm golden glow directly behind the head, so
that the gold coin and the off-white face both stand out.
```

### 🚨 2차 실패 (2026-08-21) — 그림은 나왔는데 아이덴티티가 없었다

1차 프롬프트를 고쳐 **일러스트는 제대로 나왔다.** 그런데 결과물이 **그냥 웃는 민머리 캐릭터**였다.
정호님: *"너무 아이덴티티도 없고 의미도 없잖아. 방구석 경제라는 느낌이 들도록 만들어보라는거야."*

### 🔴 벤치 분석 — [경제해적단 프로필](https://www.youtube.com/@경제해적단-t5m)이 하는 것

| | 경제해적단 | 우리 2차 결과물 |
|---|---|---|
| **채널명이 그림이 됐나** | ⭕ "해적단" → **두건 · 갈고리 손 · 해골 금화** | ❌ "방구석"이 아무 데도 없다 |
| 구성 | **전신 + 포즈 + 배경** — 이야기가 있다 | 얼굴만 — 이야기가 없다 |
| 등신 | 2.5등신(머리가 전체의 약 35%) | 얼굴이 65% |
| 정체성 소품 | 두건·갈고리·해골금화·흩날리는 금화 | 금화 하나 |
| 배경 | 진한 네이비 + 금색 반짝임 입자 | 단색 그라데이션 |

> 🔴 **핵심 원리: 채널명을 캐릭터로 만든다.**
> 해적단이 해적을 그렸듯 우리는 **방구석**을 그려야 한다.
> ⛔ **정장은 채널명과 정반대다.** 「방구석」에 정장을 입힌 것이 2차 실패의 본질이다.

### 🏠 확정 컨셉 — 「방바닥에 앉아 내 돈 굴리는 사람」

| 요소 | 방구석(정체성) | 경제(장르) |
|---|---|---|
| 옷 | **후드티** ⛔ 정장 금지 | — |
| 자세 | **방바닥에 책상다리 / 이불 두름** | — |
| 소품 | 방석 · 이불 · 머그컵 | **노트북·폰의 초록 상승 차트 · 금화** |
| 배경 | 따뜻한 방 안 조명 | 진한 네이비 + 금색 반짝임 입자 |

**얼굴 사양은 [thumbnail-illustration.md](thumbnail-illustration.md) §3 마스코트 그대로 두고, 몸과 장면으로 아이덴티티를 만든다.**
등신도 얼굴 65% → **2.5등신(머리 약 35%)** 으로 바꾼다. 전신이라야 이야기가 생긴다.

### 🔴 4차 개정 (2026-08-21) — 「널브러짐」이 빠져 있었다

3차안은 셋 다 **바르게 앉아** 있었다. 「방구석」의 핵심은 자세가 아니라 **널브러짐**이다.
정호님: *"소파에서 테이블 위에 다리 꼬고 앉아서 집에서 편하게 널브러져 있는 느낌… 말 그대로 방구석에 널브러져서 경제를 배운다는 느낌."*

그리고 **경제해적단 스타일을 복제하지 않는다.** 금색 반짝임 입자·원형 네이비 배경은 그 채널 문법이다.
→ **우리 스타일은 [thumbnail-illustration.md](thumbnail-illustration.md) §2** — 볼류메트릭 semi-3D · 황금빛 역광 · 거의 검은 그림자와 밝은 하이라이트가 한 화면에.

#### 컨셉 축

| | |
|---|---|
| **자세** | **널브러짐.** 다리 꼬아 테이블에 올리기 · 소파에 파묻히기 · 바닥에 엎드리기 · 대자로 눕기 |
| **옷** | 후드티·트레이닝복 ⛔ 정장 금지 |
| **경제** | 화면 속 초록 상승 차트 · 금화 — **소품 하나면 충분하다** |
| **각도** | 시안마다 다르게 — 정면 / 3/4 측면 / 살짝 위 / 탑뷰 |

### 📋 복사용 — 4안 한 줄씩 (🔴 4차 · 널브러짐 + 우리 스타일)

> 🅐 소파+테이블 다리 꼬기(정호님 지정) / 🅑 소파에 파묻힘 / 🅒 바닥에 엎드림 / 🅓 대자로 누움(탑뷰)

```
A volumetric semi-3D digital illustration of a cartoon mascot, drawn in the visual language of Korean finance-explainer YouTube channels, for a square YouTube channel avatar. This is an ILLUSTRATION, not a photo. Square 1:1 aspect ratio. NEGATIVE — no photography, no photorealism, no real human skin or pores, no individual hair strands, no real person's face, no camera bokeh, and absolutely no suit and no necktie. CHARACTER: a chibi figure about 2.5 heads tall with a thick clean BLACK OUTLINE around every form; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair and NO nose, dimensional and glossy, and it is the brightest thing in the frame and takes about 35% of the frame height; two big round WHITE eyes with solid round black pupils and drawn eyelids; thick solid BLACK eyebrows raised in a relaxed contented arch; a mouth drawn as a lazy satisfied half-smile; hands as simple rounded mitten shapes. He wears a soft DEEP-NAVY HOODIE and loose grey sweatpants. POSE — he is thoroughly SLOUCHED AND RELAXED, not sitting up straight: he sags deep into a fabric sofa with his shoulders low, his ANKLES CROSSED AND PROPPED UP ON THE COFFEE TABLE in front of him, one arm draped along the back of the sofa and the other holding a tablet resting against his knees, and on the tablet screen a bright GREEN rising chart line glows. A mug and two flat gold coins sit on the coffee table beside his feet. CAMERA: straight-on eye level, facing him. COMPOSITION: the whole slouched figure is compact and centred inside the square with generous empty margin on all four sides, because the square is cropped into a circle and every corner is discarded; nothing important touches the outer edge; no lettering anywhere. LIGHT AND COLOUR: a warm golden light burns in from the left side of the room and floods the scene with orange and gold while the right side falls into deep near-black shadow, so the tonal range runs from almost pure black to bright highlight in one frame; materials have real weight and thickness — soft sofa fabric, wood table, glossy tablet, solid gold coins; deep navy hoodie, off-white face, warm gold coins, bright green chart line.
A volumetric semi-3D digital illustration of a cartoon mascot, drawn in the visual language of Korean finance-explainer YouTube channels, for a square YouTube channel avatar. This is an ILLUSTRATION, not a photo. Square 1:1 aspect ratio. NEGATIVE — no photography, no photorealism, no real human skin or pores, no individual hair strands, no real person's face, no camera bokeh, and absolutely no suit and no necktie. CHARACTER: a chibi figure about 2.5 heads tall with a thick clean BLACK OUTLINE around every form; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair and NO nose, dimensional and glossy, and it is the brightest thing in the frame and takes about 35% of the frame height; two big round WHITE eyes with solid round black pupils and drawn eyelids; thick solid BLACK eyebrows raised in a relaxed contented arch; a mouth drawn as a lazy satisfied half-smile; hands as simple rounded mitten shapes. He wears a soft DEEP-NAVY HOODIE and loose grey sweatpants. POSE — he has COLLAPSED SIDEWAYS INTO THE CORNER OF A DEEP SOFA and is half-buried in cushions, one leg folded under him and the other hanging loosely off the seat, a soft blanket sliding off his shoulder, an open laptop balanced on a cushion beside him with a bright GREEN rising chart line glowing on the screen, and one mitten hand lazily reaching toward it. A mug sits on the floor by the sofa next to two flat gold coins. CAMERA: a three-quarter side view, slightly above his eye level. COMPOSITION: the whole slouched figure is compact and centred inside the square with generous empty margin on all four sides, because the square is cropped into a circle and every corner is discarded; nothing important touches the outer edge; no lettering anywhere. LIGHT AND COLOUR: a warm golden light burns in from a window behind the sofa and floods the scene with orange and gold while the foreground falls into deep near-black shadow, so the tonal range runs from almost pure black to bright highlight in one frame; materials have real weight and thickness — soft sofa fabric, knitted blanket, glossy laptop, solid gold coins; deep navy hoodie, off-white face, warm gold coins, bright green chart line.
A volumetric semi-3D digital illustration of a cartoon mascot, drawn in the visual language of Korean finance-explainer YouTube channels, for a square YouTube channel avatar. This is an ILLUSTRATION, not a photo. Square 1:1 aspect ratio. NEGATIVE — no photography, no photorealism, no real human skin or pores, no individual hair strands, no real person's face, no camera bokeh, and absolutely no suit and no necktie. CHARACTER: a chibi figure about 2.5 heads tall with a thick clean BLACK OUTLINE around every form; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair and NO nose, dimensional and glossy, and it is the brightest thing in the frame and takes about 35% of the frame height; two big round WHITE eyes with solid round black pupils and drawn eyelids; thick solid BLACK eyebrows raised in a relaxed contented arch; a mouth drawn as a lazy satisfied half-smile; hands as simple rounded mitten shapes. He wears a soft DEEP-NAVY HOODIE and loose grey sweatpants. POSE — he LIES FLAT ON HIS STOMACH ON THE FLOOR of his own room on a rug, propped up on both elbows with his chin resting in his mitten hands, his lower legs bent up in the air behind him and crossed lazily at the ankles, and a smartphone lies on the rug in front of his face with a bright GREEN rising chart line glowing on its screen. Two flat gold coins and a mug sit on the rug beside the phone. CAMERA: viewed from slightly above and in front, looking down at him. COMPOSITION: the whole sprawled figure is compact and centred inside the square with generous empty margin on all four sides, because the square is cropped into a circle and every corner is discarded; nothing important touches the outer edge; no lettering anywhere. LIGHT AND COLOUR: a warm golden light burns in low from one side of the room and floods the rug with orange and gold while the far side of the floor falls into deep near-black shadow, so the tonal range runs from almost pure black to bright highlight in one frame; materials have real weight and thickness — woven rug, glossy phone, solid gold coins; deep navy hoodie, off-white face, warm gold coins, bright green chart line.
A volumetric semi-3D digital illustration of a cartoon mascot, drawn in the visual language of Korean finance-explainer YouTube channels, for a square YouTube channel avatar. This is an ILLUSTRATION, not a photo. Square 1:1 aspect ratio. NEGATIVE — no photography, no photorealism, no real human skin or pores, no individual hair strands, no real person's face, no camera bokeh, and absolutely no suit and no necktie. CHARACTER: a chibi figure about 2.5 heads tall with a thick clean BLACK OUTLINE around every form; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair and NO nose, dimensional and glossy, and it is the brightest thing in the frame and takes about 35% of the frame height; two big round WHITE eyes with solid round black pupils and drawn eyelids; thick solid BLACK eyebrows raised in a relaxed contented arch; a mouth drawn as a lazy satisfied half-smile; hands as simple rounded mitten shapes. He wears a soft DEEP-NAVY HOODIE and loose grey sweatpants. POSE — he is SPRAWLED FLAT ON HIS BACK on a floor mattress with a rumpled duvet half over his legs, arms and legs thrown out loosely, holding a tablet up above his face with both mitten hands, and on the tablet screen a bright GREEN rising chart line glows down onto him. Several flat gold coins are scattered on the duvet around him and a mug sits on the floor by his head. CAMERA: a TOP-DOWN view looking straight down at him from the ceiling. COMPOSITION: the whole sprawled figure is compact and centred inside the square with generous empty margin on all four sides, because the square is cropped into a circle and every corner is discarded; nothing important touches the outer edge; no lettering anywhere. LIGHT AND COLOUR: a warm golden light burns in from one side and floods the bedding with orange and gold while the opposite side falls into deep near-black shadow, so the tonal range runs from almost pure black to bright highlight in one frame; materials have real weight and thickness — rumpled duvet fabric, glossy tablet, solid gold coins; deep navy hoodie, off-white face, warm gold coins, bright green chart line.
```

### 4차 판정 기준

- [ ] 🔴 **널브러져 있는가.** 바르게 앉아 있으면 실패 — 어깨가 처지고 팔다리가 늘어져 있어야 한다
- [ ] **후드티·트레이닝복인가.** 정장·넥타이가 보이면 즉시 폐기
- [ ] 초록 상승 차트가 화면에서 읽히는가
- [ ] 한쪽은 황금빛으로 밝고 반대쪽은 거의 검은가 (우리 스타일 명암 대비)
- [ ] ⛔ **경제해적단 문법이 섞이지 않았는가** — 금색 반짝임 입자, 원형 테두리
- [ ] 원형으로 잘랐을 때 팔다리가 잘리지 않는가
- [ ] 24×24로 줄였을 때 덩어리로 구분되는가

### 🗄️ 폐기 — 3차 프롬프트 (바르게 앉은 자세)

아래는 **널브러짐 부재 + 경제해적단 문법 혼입**으로 폐기했다. 기록으로만 남긴다.

### 📋 폐기 — 3차 복사용

> 각 줄이 완결된 프롬프트다. 한 줄씩 복사해 넣는다.
> 🅐 방바닥+노트북 / 🅑 이불+스마트폰 / 🅒 금화 더미+노트북

```
A flat cartoon mascot character illustration for a YouTube channel avatar, hand-drawn digital art in the style of Korean finance-explainer YouTube channels. This is a DRAWING, not a photo. Square 1:1 aspect ratio. NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh, studio photo lighting, any suit or formal business clothing. CHARACTER: a chibi cartoon figure about 2.5 heads tall, drawn with thick clean BLACK OUTLINES and flat cel shading; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair whatsoever and NO nose, and it is the brightest thing in the picture and takes up about 35% of the frame height; two big round WHITE eyes with solid round black pupils and simple drawn eyelids; thick solid BLACK eyebrows drawn as two bold shapes, raised in a relaxed friendly arch; a mouth drawn as a warm upward-curving smile; hands drawn as simple rounded mitten shapes. He wears a soft flat DEEP-NAVY HOODIE and comfortable home clothes — absolutely no suit and no necktie. SCENE: he sits cross-legged on the floor of his own room on a small round cushion, an open laptop resting on his lap, and on the laptop screen a bright GREEN rising chart line glows clearly; three or four flat round gold coins lie scattered on the floor beside him and one small warm mug sits next to them. COMPOSITION: the whole seated figure sits exactly in the centre of the square and is fully contained with generous empty margin on all four sides, because the square will be cropped into a circle and every corner will be discarded; nothing important may touch the outer edge; there is no lettering anywhere in the image. COLOUR AND LIGHT: a deep navy-blue background with a warm golden glow radiating from behind the figure and a scattering of tiny gold sparkle dots floating in the dark background; bold flat poster colours — off-white face, deep navy hoodie, warm gold coins, bright green chart line, black outlines. Clean and uncluttered, and instantly readable when shrunk to 24 pixels.
A flat cartoon mascot character illustration for a YouTube channel avatar, hand-drawn digital art in the style of Korean finance-explainer YouTube channels. This is a DRAWING, not a photo. Square 1:1 aspect ratio. NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh, studio photo lighting, any suit or formal business clothing. CHARACTER: a chibi cartoon figure about 2.5 heads tall, drawn with thick clean BLACK OUTLINES and flat cel shading; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair whatsoever and NO nose, and it is the brightest thing in the picture and takes up about 35% of the frame height; two big round WHITE eyes with solid round black pupils and simple drawn eyelids; thick solid BLACK eyebrows drawn as two bold shapes, raised in a relaxed friendly arch; a mouth drawn as a warm upward-curving smile; hands drawn as simple rounded mitten shapes. He wears a soft flat DEEP-NAVY HOODIE and comfortable home clothes — absolutely no suit and no necktie. SCENE: he sits on the floor of his own room with a thick soft blanket pulled up around his shoulders like a cocoon, holding up a smartphone with both mitten hands, and on the phone screen a bright GREEN rising chart line glows clearly; a warm mug sits on the floor beside him and two flat round gold coins lie next to it. COMPOSITION: the whole seated figure sits exactly in the centre of the square and is fully contained with generous empty margin on all four sides, because the square will be cropped into a circle and every corner will be discarded; nothing important may touch the outer edge; there is no lettering anywhere in the image. COLOUR AND LIGHT: a deep navy-blue background with a warm golden glow radiating from behind the figure and a scattering of tiny gold sparkle dots floating in the dark background; bold flat poster colours — off-white face, deep navy hoodie, warm gold coins, bright green chart line, black outlines. Clean and uncluttered, and instantly readable when shrunk to 24 pixels.
A flat cartoon mascot character illustration for a YouTube channel avatar, hand-drawn digital art in the style of Korean finance-explainer YouTube channels. This is a DRAWING, not a photo. Square 1:1 aspect ratio. NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh, studio photo lighting, any suit or formal business clothing. CHARACTER: a chibi cartoon figure about 2.5 heads tall, drawn with thick clean BLACK OUTLINES and flat cel shading; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair whatsoever and NO nose, and it is the brightest thing in the picture and takes up about 35% of the frame height; two big round WHITE eyes with solid round black pupils and simple drawn eyelids; thick solid BLACK eyebrows drawn as two bold shapes, raised in a delighted arch; a mouth drawn as a wide happy open smile; hands drawn as simple rounded mitten shapes. He wears a soft flat DEEP-NAVY HOODIE and comfortable home clothes — absolutely no suit and no necktie. SCENE: he sits cross-legged on the floor of his own room on a small round cushion with an open laptop on his lap showing a bright GREEN rising chart line, and a generous pile of flat round gold coins is heaped on the floor around him, with a few coins tumbling down the side of the pile. COMPOSITION: the whole seated figure sits exactly in the centre of the square and is fully contained with generous empty margin on all four sides, because the square will be cropped into a circle and every corner will be discarded; nothing important may touch the outer edge; there is no lettering anywhere in the image. COLOUR AND LIGHT: a deep navy-blue background with a warm golden glow radiating from behind the figure and a scattering of tiny gold sparkle dots floating in the dark background; bold flat poster colours — off-white face, deep navy hoodie, warm gold coins, bright green chart line, black outlines. Clean and uncluttered, and instantly readable when shrunk to 24 pixels.
```

### 3차 판정 기준

- [ ] **후드티인가.** 정장·넥타이가 보이면 즉시 폐기
- [ ] **바닥에 앉아 있는가.** 서 있으면 「방구석」이 아니다
- [ ] 초록 상승 차트가 화면에서 읽히는가 (경제 신호)
- [ ] 금화가 있는가
- [ ] 얼굴이 썸네일 마스코트와 같은가 (민머리·코 없음·큰 흰자 눈·굵은 검정 눈썹)
- [ ] 24×24로 줄였을 때 **네이비 덩어리 + 초록 점 + 금색 점**으로 구분되는가

### 🗄️ 폐기 — 2차 프롬프트 (얼굴 단독형)

아래는 **아이덴티티 부재로 폐기**했다. 기록으로만 남긴다.

```
A flat cartoon mascot character illustration, hand-drawn digital art in the style of Korean finance-explainer YouTube thumbnails. This is a DRAWING, not a photo. Square 1:1 aspect ratio. NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh, studio photo lighting. CHARACTER — draw exactly this and nothing else: a large smooth round OFF-WHITE head shaped like a simple ball, completely BALD with NO hair whatsoever and NO nose, drawn with a thick clean BLACK OUTLINE around the whole head and flat cel shading inside, and it is the brightest thing in the picture; two big round WHITE eyes with solid round black pupils and simple drawn eyelids, looking straight at the viewer; thick solid BLACK eyebrows drawn as two bold shapes above the eyes, raised in a relaxed friendly arch; a mouth drawn as a wide upward-curving smile; a small simple cartoon body in a flat deep-navy suit jacket over a white collar, only the shoulders visible along the bottom edge, hands drawn as simple rounded mitten shapes. COMPOSITION: the head sits exactly in the centre of the square and fills about 65% of the frame height, with generous empty margin on all four sides, because the square will be cropped into a circle and every corner will be discarded; nothing important may touch the outer edge; there is no lettering anywhere in the image. BACKGROUND: one flat warm gold colour with a soft radial glow directly behind the head, with no props, no scenery and no objects of any kind. COLOUR: bold flat poster colours with a warm golden glow — warm gold and orange background, off-white face, deep navy clothing, black outlines; a simple cel-shaded highlight on the upper left of the head and a soft flat shadow on the lower right; clean and uncluttered, and instantly readable when shrunk to 24 pixels.
A flat cartoon mascot character illustration, hand-drawn digital art in the style of Korean finance-explainer YouTube thumbnails. This is a DRAWING, not a photo. Square 1:1 aspect ratio. NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh, studio photo lighting. CHARACTER — draw exactly this and nothing else: a large smooth round OFF-WHITE head shaped like a simple ball, completely BALD with NO hair whatsoever and NO nose, drawn with a thick clean BLACK OUTLINE around the whole head and flat cel shading inside, and it is the brightest thing in the picture; two big round WHITE eyes with solid round black pupils and simple drawn eyelids, looking straight at the viewer; thick solid BLACK eyebrows drawn as two bold shapes above the eyes, raised in a relaxed friendly arch; a mouth drawn as a wide upward-curving smile; a small simple cartoon body in a flat deep-navy suit jacket over a white collar, only the shoulders visible along the bottom edge, hands drawn as simple rounded mitten shapes. POSE: one simple mitten-shaped cartoon hand is raised beside the head in a small friendly wave, palm toward the viewer, kept clear of the face and well inside the circular crop area. COMPOSITION: the head sits exactly in the centre of the square and fills about 65% of the frame height, with generous empty margin on all four sides, because the square will be cropped into a circle and every corner will be discarded; nothing important may touch the outer edge; there is no lettering anywhere in the image. BACKGROUND: one flat warm gold colour with a soft radial glow directly behind the head, with no props and no scenery. COLOUR: bold flat poster colours with a warm golden glow — warm gold and orange background, off-white face, deep navy clothing, black outlines; a simple cel-shaded highlight on the upper left of the head and a soft flat shadow on the lower right; clean and uncluttered, and instantly readable when shrunk to 24 pixels.
A flat cartoon mascot character illustration, hand-drawn digital art in the style of Korean finance-explainer YouTube thumbnails. This is a DRAWING, not a photo. Square 1:1 aspect ratio. NEGATIVE — none of the following may appear: photography, photorealism, real human skin, skin pores or texture, individual hair strands, a real person's face, camera depth-of-field or bokeh, studio photo lighting. CHARACTER — draw exactly this and nothing else: a large smooth round OFF-WHITE head shaped like a simple ball, completely BALD with NO hair whatsoever and NO nose, drawn with a thick clean BLACK OUTLINE around the whole head and flat cel shading inside, and it is the brightest thing in the picture; two big round WHITE eyes with solid round black pupils and simple drawn eyelids, looking straight at the viewer; thick solid BLACK eyebrows drawn as two bold shapes above the eyes, raised in a relaxed friendly arch; a mouth drawn as a wide upward-curving smile; a small simple cartoon body in a flat deep-navy suit jacket over a white collar, only the shoulders visible along the bottom edge, hands drawn as simple rounded mitten shapes. PROP: exactly one large flat round gold coin, blank and without any lettering, held up beside the head by a simple mitten-shaped cartoon hand, big and simple enough to read as a plain gold circle at 24 pixels, and there is nothing else in the frame. COMPOSITION: the head sits exactly in the centre of the square and fills about 65% of the frame height, with generous empty margin on all four sides, because the square will be cropped into a circle and every corner will be discarded; nothing important may touch the outer edge; there is no lettering anywhere in the image. BACKGROUND: one flat deep-navy colour with a soft warm golden glow directly behind the head, so that the gold coin and the off-white face both stand out. COLOUR: bold flat poster colours — deep navy background, off-white face, gold coin, black outlines; a simple cel-shaded highlight on the upper left of the head and a soft flat shadow on the lower right; clean and uncluttered, and instantly readable when shrunk to 24 pixels.
```

### 재생성 판정 (나노바나나 결과를 받고 즉시)

- [ ] **사진처럼 보이면 즉시 폐기한다.** 머리카락 한 올, 피부 질감, 코가 있으면 실패다
- [ ] 머리가 **민머리 미색 공 + 굵은 검정 외곽선**인가
- [ ] 눈이 **큰 흰자 + 검은 원형 눈동자**인가 (작은 점 눈이면 실패)
- [ ] **눈썹이 굵은 검정 두 덩어리**로 있는가
- [ ] 24×24로 줄여서 웃는 얼굴로 읽히는가
- [ ] 글자가 한 개도 없는가

> 실패하면 **공통 블록의 NEGATIVE 줄을 프롬프트 맨 앞으로 올려** 다시 돌린다.

### 시안 비교

| | 24px 가독 | 친근함 | 정체성 | 위험 |
|---|---|---|---|---|
| 🅐 얼굴 단독 | **최상** | 상 | 중 | 없음 |
| 🅑 손 인사 | 중 | **최상** | 중 | 손이 얼룩질 수 있음 |
| 🅒 금화 | 중하 | 상 | **최상** | 소품이 노이즈가 될 수 있음 |

> **추천은 🅐다.** 프로필의 1차 역할은 **추천 피드 36px에서 "친근한 사람 채널"로 읽히는 것**이지 정보 전달이 아니다.
> 정체성은 배너·소개글·썸네일이 맡는다.

### 자가 점검 (생성 후 반드시)

- [ ] **1024px 원본을 24×24로 줄여 본다.** 웃는 얼굴로 읽히면 통과, 회색 덩어리면 재생성
- [ ] 정사각을 **원형으로 잘랐을 때** 머리 위·턱 아래가 잘리지 않는가
- [ ] 얼굴이 [thumbnail-illustration.md](thumbnail-illustration.md) §3 마스코트와 **같은 얼굴**로 보이는가 (눈·눈썹·코 없음·외곽선)
- [ ] 글자가 한 개도 없는가

---

## 3. 배너

**규격**: 업로드 2560×1440 · **모든 기기 공통 안전영역 1546×423(중앙)**. 중요한 것은 전부 안전영역 안에 넣는다.

### ✅ 확정 프로필 (2026-08-21) — 4차 🅑안

**「소파 구석에 옆으로 무너져 파묻힌」 안으로 확정.** 아래 요소가 채널 비주얼 아이덴티티의 기준이 된다.

| 요소 | 확정값 |
|---|---|
| 캐릭터 | 민머리 미색 공 머리 · 코 없음 · 굵은 검정 외곽선 · 큰 흰자 눈 + **처진 눈꺼풀** · 굵은 검정 눈썹 · **나른한 반쪽 미소** |
| 복장 | **진한 네이비 후드티 + 회색 트레이닝 팬츠** · 흰 미튼 손발 |
| 가구 | **진한 네이비 패브릭 소파**(팔걸이·쿠션) · 팔걸이에 걸친 **주황·갈색 체크 담요** |
| 소품 | 쿠션 위 **노트북**(초록 상승 차트가 광원처럼 빛남) · 기하학 무늬 **머그컵** · **$ 각인 금화 2~3닢** |
| 배경 | 어두운 방 · 왼쪽 **주황빛 커튼/창문** · 나무 바닥 · 러그 |
| 조명 | 창에서 오는 **따뜻한 주황 역광** + 노트북의 **초록 글로우** · 반대쪽은 거의 검정 |

> 🔴 **배너·썸네일·향후 모든 캐릭터 등장물은 이 사양을 따른다.**

### 배너 생성 프롬프트 (🔴 2026-08-21 확정 프로필에 맞춤)

> ⛔ 초판(정장)·2판(바르게 앉음) 폐기. **프로필과 같은 캐릭터·같은 방·같은 색**이어야 한 세트로 읽힌다.

```
A volumetric semi-3D digital illustration for a wide YouTube channel banner, 2560 x 1440, drawn in the visual language of Korean finance-explainer YouTube channels. This is an ILLUSTRATION, not a photo. NEGATIVE — no photography, no photorealism, no real human skin or pores, no individual hair strands, no real person's face, no camera bokeh, and absolutely no suit and no necktie. EVERY IMPORTANT ELEMENT must sit inside the central safe area of 1546 x 423 pixels, because the far left and far right of the canvas are cropped away on phones. CHARACTER — exactly the same mascot as the channel avatar: a chibi figure about 2.5 heads tall with a thick clean BLACK OUTLINE around every form; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair and NO nose, dimensional and glossy, and it is the brightest thing in the frame; two big round WHITE eyes with solid round black pupils and HEAVY DROOPING EYELIDS; thick solid BLACK eyebrows in a relaxed contented arch; a lazy satisfied half-smile; hands and feet as simple rounded off-white mitten shapes. He wears a DEEP-NAVY HOODIE and loose GREY SWEATPANTS. SCENE — in the LEFT HALF of the safe area he has COLLAPSED SIDEWAYS INTO THE CORNER OF A DEEP NAVY FABRIC SOFA, thoroughly slouched and half-buried in cushions with one leg folded under him and the other hanging loosely, an ORANGE AND BROWN PLAID BLANKET draped over the sofa arm behind him, and an open LAPTOP resting on a cushion beside him whose screen glows with a bright GREEN RISING CHART LINE that spills green light onto his hand. On the wooden floor and rug below sit a patterned ceramic MUG and two or three flat GOLD COINS. TEXT: render the Korean words "내 돈이 어떻게 되는지, 쉬운 말로" in large bold Korean Hangul in the RIGHT HALF of the safe area, in warm off-white with a soft dark edge so it stays readable against the dark room. Render no other lettering anywhere. LIGHT AND COLOUR: a warm orange glow burns in through a curtained window on the far left and floods that side of the room with orange and gold, while the right side of the room falls away into deep near-black shadow so the tonal range runs from almost pure black to bright highlight in one frame; materials have real weight and thickness — soft sofa fabric, woollen plaid blanket, glossy laptop, ceramic mug, solid gold coins. The far left and far right thirds of the 2560-wide canvas are a plain continuation of the dark room with nothing important in them. Unlike a thumbnail, this frame is NOT crowded.
```

```
A wide YouTube channel banner illustration, 2560 x 1440. This is a DRAWING, not a photo. NEGATIVE — no photography, no photorealism, no real human skin or hair strands, no camera bokeh, and absolutely no suit or necktie. EVERY IMPORTANT ELEMENT must sit inside the central safe area of 1546 x 423 pixels, because the far left and far right of the canvas are cropped away on phones. CHARACTER: a chibi cartoon figure about 2.5 heads tall, drawn with thick clean BLACK OUTLINES and flat cel shading; his head is a large smooth round OFF-WHITE ball, completely BALD with NO hair and NO nose, and it is the brightest thing in the picture; two big round WHITE eyes with solid round black pupils and simple drawn eyelids; thick solid BLACK eyebrows raised in a relaxed friendly arch; a mouth drawn as a warm upward-curving smile; hands drawn as simple rounded mitten shapes. He wears a soft flat DEEP-NAVY HOODIE and comfortable home clothes. SCENE: he sits cross-legged on the floor of his own room on a small round cushion in the LEFT HALF of the safe area, an open laptop on his lap showing a bright GREEN rising chart line, with a few flat round gold coins and a warm mug on the floor beside him; behind him the room is suggested simply with a warm window glow and a floor lamp. TEXT: render the Korean words "내 돈이 어떻게 되는지, 쉬운 말로" in large bold Korean Hangul in the RIGHT HALF of the safe area, in warm off-white with a soft dark edge so it stays readable. Render no other lettering anywhere. COLOUR AND LIGHT: a deep navy-blue background with a warm golden glow radiating from the window and a scattering of tiny gold sparkle dots; bold flat poster colours — off-white face, deep navy hoodie, warm gold coins, bright green chart line, black outlines. The far left and far right thirds of the canvas are a plain continuation of the navy background with nothing important in them. Clean and open — unlike a thumbnail, this frame is NOT crowded.
```

### 배너 문구 후보

| # | 문구 | 성격 |
|---|---|---|
| **1 (추천)** | **내 돈이 어떻게 되는지, 쉬운 말로** | 축을 정확히 말한다. 소재를 좁히지 않는다 |
| 2 | 10억까지, 내 돈 이야기 | **P0 축을 정면으로 건다.** 정체성 신호가 가장 강하지만 채널을 한 소재로 좁힌다 |
| 3 | 어려운 경제 말고, 내 계좌 이야기 | 차별화가 선명하나 길다 |

> 🔴 **1번을 추천한다.** 2번은 [direction.md](../direction.md) 공식 ⑥과 완벽히 맞지만, **배너에 금액을 박으면 다른 소재를 얹을 때 어긋난다.** 지금은 소재를 넓게 열어 둘 때다.

---

## 4. 채널 소개글

```
내 돈이 앞으로 어떻게 되는지, 쉬운 말로 풀어드립니다.

10억이 생기면 실제로 무슨 일이 벌어지는지,
내 계좌는 지금 어디쯤 와 있는지,
남들은 어디서 돈을 잃고 어디서 불리는지.

어려운 용어와 숫자 놀음 없이,
방구석에서 편하게 보실 수 있게 만듭니다.
```

- ⛔ **채널명·핸들을 소개글에 넣지 않는다** ([[feedback_youtube_no_channel_name]] 취지 — 장르만 서술한다). 「방구석」은 일반명사로만 쓴다
- ⛔ 「역사」·「전쟁」·「세계」·「국제정세」를 한 번도 쓰지 않는다. 1기 잔재를 지운다
- ⭕ **「10억」을 소개글에 넣는다** — 배너와 달리 소개글은 소재를 좁히지 않고 축만 알린다

---

## 5. 재생목록·홈 정리 원칙

| 하는 것 | 안 하는 것 |
|---|---|
| 홈 상단 추천 섹션을 **[08-10](https://www.youtube.com/watch?v=CKEBf-52HBo)·[08-16](https://www.youtube.com/watch?v=TxSTmhN8PaQ)·[08-09](https://www.youtube.com/watch?v=EfzrxJzqExk)** 세 편으로 구성 | 8월 경제 편을 비공개로 돌리지 않는다([direction.md](../direction.md) 9-1절) |
| **[08-10](https://www.youtube.com/watch?v=CKEBf-52HBo)의 최종화면·카드·고정댓글을 신작으로 연결** — 하루 +437회가 여기서 나온다 | 죽은 8월 편을 지우지 않는다. **썸네일·제목만 교체** |
| 역사 재생목록을 홈에서 내린다 | — |

> 🔴 **[08-10](https://www.youtube.com/watch?v=CKEBf-52HBo) 연결이 지금 가장 값싼 노출 공급책이다.** 신작 노출이 293인 상태에서 유일하게 살아 있는 파이프다.
