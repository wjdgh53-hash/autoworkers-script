# 일러스트형 썸네일 규칙 — 방구석 경제 전용 (신설 2026-08-19)

> 국기볼형을 제거하고 그 자리에 신설한 계열. 근거 [_benchmarks/thumbnail-patterns.md](_benchmarks/thumbnail-patterns.md) 8절
> 벤치 3곳에서 역추출: [경제해적단](https://www.youtube.com/@경제해적단-t5m)(구독 101,000·최고 13.8배) · [야무진 경제학](https://www.youtube.com/channel/UCdu6FZYHrnBKdyzRawLabmg)(13.9배) · [유치한경제학](https://www.youtube.com/channel/UC7cf7eZIucAAzkm_rwoawZw)(7.4·5.3배)
>
> 🔴 **게이트 A~D와 텍스트 규칙은 [thumbnail-design.md](thumbnail-design.md)가 유일한 원본이다.** 여기에 다시 적지 않는다.
> 이 파일은 **그 게이트를 일러스트로 구현하는 방법**만 정의한다.
> ⛔ 탐정경제학에는 존재하지 않는 계열이다.

---

## §1. 왜 신설하나 — 게이트가 실사와 부딪힌다

[thumbnail-design.md](thumbnail-design.md)의 게이트를 세우고 보니 **실사로는 구현이 어려운 항목이 셋** 있다.

| 게이트 | 실사의 문제 | 일러스트의 해법 | 실측 |
|---|---|---|---|
| **A 얼굴 — 「나 같은 사람」** | 실사는 **나이·성별·직업이 반드시 찍힌다.** 특정하는 순간 나머지가 배제된다 | 마스코트는 **무연령·무성·무직업**이라 전원이 자기를 대입한다 | 우리 [08-18](https://www.youtube.com/watch?v=33l7widZdTs) 0.75배가 「백발 노인=다른 세대」로 죽었다 |
| **C 사건 진행 중** | 「구멍에서 물이 쏟아지는 침몰선」을 사진으로 못 만든다 | 은유를 물리적 장면으로 그릴 수 있다 | 야무진 [13.9배](https://www.youtube.com/watch?v=LjHlXKeRH5s) |
| **1순위 구도 — 좌우 대비** | **같은 인물을 두 번** 일관되게 생성하기 어렵다 | 같은 마스코트를 양쪽에 두면 끝 | 경제해적단 [채널 1위 13.8배](https://www.youtube.com/watch?v=JREdVuRBv9U)·[3.2배](https://www.youtube.com/watch?v=1-M2uIaVoKs) |

> ⚠️ **실사를 대체하는 게 아니다.** 실사는 A-1(머스크·실존 유명인)에서 검증된 자산이다([26.6배](https://www.youtube.com/watch?v=TxSTmhN8PaQ)·[18.5배](https://www.youtube.com/watch?v=CKEBf-52HBo)).
> 그리고 실사 무명으로도 [20.7배](https://www.youtube.com/watch?v=Uwfjww9_yKk)가 나온다. **둘 다 만들어 A/B로 실측한다**(§7).

---

## §2. 스타일 — 경제해적단을 그대로 베낀다

> 🔴 **2026-08-20 전면 개정.** 첫 회차(`semiconductor-stock-halved`) 결과물이 **회색·저채도·무표정**으로 나왔다.
> 원인은 아래 옛 문구였다 — `believable perspective, materials and lighting`이 모델에게 **사진 렌더링**으로 읽혀
> 다큐 사진 톤(저채도·저대비)이 나왔고, 색·표정 규정이 아예 없어서 모델 기본값이 그대로 갔다.
> 정호님 지시: **"완전히 벤치마킹한다고 생각하고 똑같이 베껴도 된다."**

### 실측 — 경제해적단 상위 6편 (2026-08-20, 160×90 축소 후 HSV)

| | 채도 | 밝기 | 대비(상위5%−하위5%) |
|---|---|---|---|
| [S&P500 9.7 vs 3,700만](https://www.youtube.com/watch?v=JREdVuRBv9U) 채널 1위 | 0.37 | 0.29 | 0.96 |
| [달러 패권](https://www.youtube.com/watch?v=NID7VESSER8) 157,000 | 0.36 | 0.33 | 0.96 |
| [부자들은 주식을 팔지 않습니다](https://www.youtube.com/watch?v=aepM7E3vsTs) | 0.47 | 0.34 | 0.98 |
| [조용히 부자되는 3가지](https://www.youtube.com/watch?v=1-M2uIaVoKs) | 0.40 | 0.35 | 0.97 |
| [월배당 ETF 베스트 5](https://www.youtube.com/watch?v=81c1g3RiDE8) | 0.34 | 0.44 | 1.00 |
| [배당주로 노후 끝내기](https://www.youtube.com/watch?v=vrZKuTGJsQU) | 0.54 | 0.37 | 1.00 |

**채도 0.34~0.54 · 대비 0.96~1.00.** 대비가 거의 1.00이라는 건 **순검정 그림자와 밝은 하이라이트가 한 화면에 같이 있다**는 뜻이다.
회색 중간톤으로 채우면 이 값이 안 나온다.

### 규격

| 요소 | 규격 |
|---|---|
| **매체** | **2D 디지털 일러스트.** 사진이 아니다 — 붓·셀 음영이 보이는 그림 |
| **캐릭터** | 극단적으로 단순. 선 몇 개로 된 얼굴 |
| **배경** | 정교하되 **명백한 그림.** 건물·거리·실내가 사실적 비례로 그려지되 사진 질감이 아니다 |
| **채도** | **높다.** 황금빛 주황이 기본 광원. 빨강(손실)·초록(이익)·금색(성공)을 원색으로 쓴다 |
| **대비** | **극단적.** 순검정에 가까운 그림자와 밝은 하이라이트를 한 화면에 |
| **왜** | 정보량 대비가 시선을 캐릭터로 몰고, 색·대비가 160×90에서 살아남게 한다 |

```
Style: a bold, high-saturation 2D digital illustration with cel shading and visible brush work —
clearly a drawing, never a photograph. Warm golden-hour light floods the scene from one side,
pushing deep near-black shadows on the other; the tonal range runs from almost pure black to bright
highlight in the same frame. Colours are vivid and unmixed — warm gold and orange for the winning
side, saturated red for loss and danger, saturated green and gold for gain. The environment is
drawn in rich detail with solid perspective, but stays an illustration. The characters standing in
it are drawn in a deliberately flat, minimal style, and this contrast is intentional.
```

- ⛔ **`believable lighting`·`photorealistic`·`documentary`·`muted`·`desaturated`·`overcast` 계열 단어를 쓰지 않는다.** 이 단어들이 첫 회차를 회색으로 만들었다
- ⛔ **회색 중간톤으로 화면을 채우지 않는다.** 어두운 곳은 검게, 밝은 곳은 밝게
- ⛔ 아메리칸 카툰·치비·3D 픽사 렌더는 아니다
- ⛔ **국기볼형과 다르다.** 국기볼은 국가를 의인화한 구체이고, 이건 **시청자 본인의 아바타**다

### 좌우 대비일 때의 색 배분 (벤치 주력 구도)

```
왼쪽 (잃는 쪽)   차갑고 어둡다 — 회청색·먹구름·비, 빨강 경고, 검은 그림자
      ↕ 가운데 경계는 물리적으로 (능선·유리·문틀·빛의 경계)
오른쪽 (얻는 쪽) 따뜻하고 밝다 — 황금빛 노을, 초록, 금색
```

> 실측: [채널 1위 13.8배](https://www.youtube.com/watch?v=JREdVuRBv9U)가 정확히 이 배분이다 —
> 좌측 비 내리는 잿빛 산길, 우측 황금빛 도시와 저택. 가운데 능선이 경계다.

## §3. 마스코트 규격 — 「나」의 아바타

**매 편 같은 캐릭터가 나온다.** 벤치 최상위 4곳 전부가 고정 얼굴을 갖고 있다([thumbnail-patterns.md](_benchmarks/thumbnail-patterns.md) 8-3).

### 고정 사양 (9장 전부 동일하게 유지)

```
a smooth rounded off-white head with no hair, no nose and no rendered skin texture,
two solid black eyes and a drawn mouth; thick black eyebrows carry most of the emotion,
and the mouth, sweat drops, tears, hands and props carry the rest
```

| 항목 | 규격 | 이유 |
|---|---|---|
| **머리** | 매끈한 미색(off-white) 원형. 머리카락 없음 | 머리카락이 붙는 순간 **성별·연령**이 생긴다 |
| **눈** | 검은 점 두 개. **감정이 클 때는 크게 뜬 흰자 + 검은 눈동자**로 키운다 | 단순할수록 이입이 넓다 |
| **코** | **없음** | 인종·나이 신호를 지운다 |
| **입** | 담담할 땐 짧은 선. **놀람·낭패는 크게 벌린 입**으로 연다 | |
| **눈썹** | 굵은 검정 — V자(경고·분노) / 八자(불안·낭패) / 평평(담담) / 아치(놀람) | |
| **🔴 표정 부속** | **땀방울 · 눈물 · 벌린 입 · 손동작(머리 감싸기·이마 짚기·가리키기) · 소품(선글라스·커피잔)을 적극 쓴다** | 아래 실측 참조 |
| **몸** | 상황에 맞는 복장(정장·작업복·등산복 등). **몸은 바뀌고 머리는 안 바뀐다** | 처지는 바뀌어도 「나」는 같다 |
| **크기** | 머리가 화면 높이의 **30~40%** | 실사형(55~60%)보다 작다 — 배경 장면을 함께 읽혀야 하기 때문 |

> ⚠️ **차별화**: 경제해적단은 흰 동그라미 + 검은 점, 야무진은 노란 계란 + 안경이다.
> 우리는 **안경 없음 + 미색**으로 간다. 안경을 붙이면 야무진과 겹치고 「해설자」 인상이 생겨 **「나」가 아니라 「선생」**이 된다.

> 🔴 **2026-08-20 개정 — 「감정을 책임지는 유일한 요소는 눈썹」을 삭제했다.**
> 첫 회차가 **9장 전부 무표정**으로 나왔다. 눈썹만 허용하면 그 이상을 못 그린다.
> 벤치 실측: [부자들은 주식을 팔지 않습니다](https://www.youtube.com/watch?v=aepM7E3vsTs)는 **땀방울 + 머리 감싼 손 + 벌린 입**을 한 얼굴에 다 쓰고,
> 옆 캐릭터는 **선글라스 + 커피잔**으로 여유를 표현한다. [달러 패권 157,000회](https://www.youtube.com/watch?v=NID7VESSER8)는 **크게 뜬 눈 + 벌린 입 + 손바닥을 편 제지 동작**이다.
> **표정 강도는 대본 내용을 유추할 수 있을 만큼 올린다**([[feedback_thumbnail_face_expression]]).

> 🔶 **이 사양은 교체 가능하다.** 다만 **한 프로젝트 안 9장은 반드시 동일**해야 한다.

---

## §4. 구도 — 좌우 대비가 이 계열의 주력

[thumbnail-design.md](thumbnail-design.md) §3-A의 우선순위를 따르되, **이 계열은 1순위(좌우 대비) 비중을 더 높인다 — 9장 중 4~5장.**

### 좌우 대비 표준형 — 「같은 나, 갈라진 두 결말」

```
같은 마스코트를 좌우에 하나씩 둔다. 머리는 완전히 같고, 아래 셋만 다르다.
  ① 눈썹        좌: 八자(낭패)        우: 평평하거나 아치(여유)
  ② 복장·소지품  좌: 낡음·무거움       우: 정돈됨·가벼움
  ③ 배경 세계    좌: 어둡고 찬 색       우: 밝고 따뜻한 색
경계는 물리적 사물로 만든다 — 갈라진 지면, 갈림길 표지판, 벽, 빛의 경계.
⛔ 그래픽 분할선을 긋지 않는다.
```

> 실측: [289,154회 채널 1위](https://www.youtube.com/watch?v=JREdVuRBv9U) — 좌(어두운 돌산·쇠사슬 족쇄·땀) vs 우(황금길·저택·금화). 가운데 나무 갈림길 표지판.
> [67,369회](https://www.youtube.com/watch?v=1-M2uIaVoKs) — 좌(청소하는 아저씨) vs 우(고급 저택 문 여는 사람). 가운데 금색 균열.

### 나머지 구도

| 구도 | 장수 | 예 |
|---|---|---|
| **좌우 대비** | 4~5 | 위 표준형 |
| **은유 장면**(게이트 C 전담) | 2~3 | 구멍에서 물이 쏟아지는 배 · 무너지는 계단 · 새는 양동이 |
| **현장 + 정보 패널** | 1~2 | 마스코트 우측 + 좌측에 증권앱·전광판·칠판 |

---

## §5. 금액을 그리는 법 (게이트 B)

일러스트는 실사보다 **금액을 크고 정확하게** 넣기 쉽다. 이 계열의 이점을 살린다.

| 자리 | 프롬프트 예 |
|---|---|
| 증권앱 패널 | `a phone screen panel showing "총손익" in Korean Hangul on the left and "-52,466,430" in large red digits on the right` |
| 칠판·현수막 | `a wooden signboard: top line "970만원" and next to it "3,700만원" in Korean Hangul, with a "vs" between them` |
| 전광판 | `a board reading "삼성전자" in Korean Hangul with "-18.30%" and "-4,580,000원" below it in red` |

- 표기 규칙(큰따옴표 지정 + `in Korean Hangul`)은 [prompts/thumbnail-design.md](../../../prompts/thumbnail-design.md)의 「글자가 딸린 사물」 절을 그대로 따른다
- **한글+영문 2단 간판**은 [thumbnail-design.md](thumbnail-design.md) §5-C를 따른다 (9장 중 2~3장)

---

## §6. 세이프존·텍스트·출력

전부 기존 규칙 그대로다. **이 계열에서 새로 정하는 것은 없다.**

| 항목 | 원본 |
|---|---|
| 세이프존 하단 3/8 | [prompts/thumbnail-design.md](../../../prompts/thumbnail-design.md) |
| 9장 배분(내용3·제목3·계승3) | 동일 |
| 텍스트 2줄·색 대비·제목 복사 금지 | [thumbnail-design.md](thumbnail-design.md) §5 |
| 자가 점검 6칸 | [thumbnail-design.md](thumbnail-design.md) §7 |
| 공통 블록 1회 작성 | [prompts/thumbnail-design.md](../../../prompts/thumbnail-design.md) |

**출력 파일**: `{P}/output/thumbnails/prompts-illustration.json` · `meta.style = "illustration"`

> ⚠️ 인물 크기만 다르다 — 실사형은 얼굴 55~60%, **이 계열은 머리 30~40%**(§3). 실사형의 `SCALE, EQUALLY IMPORTANT:` 문장을 그대로 쓰지 않는다.

### 🔴 세이프존은 그대로 두되, 어두움이 위로 번지지 않게 한다 (2026-08-20)

**세이프존은 유지한다.** 벤치도 하단 35~45%가 텍스트 자리이고 어둡다 — 우리와 같은 구조다.
차이는 **그 위**다. 벤치는 상단이 황금빛으로 밝은데, 첫 회차 우리 결과물은 **화면 전체가 회색**이었다.

세이프존 문장이 프롬프트 맨 앞(`HIGHEST PRIORITY`)에서 `dark`를 세 번 말하는데
그 뒤에 색 지정이 없으면, 모델이 그 톤을 **화면 전체로 끌고 간다.**

- ⭕ **세이프존 문장 바로 뒤에 상단 톤을 명시한다** — `the upper five-eighths is bright, warm and high-contrast`
- ⛔ 세이프존 문장만 두고 상단 색을 안 정하지 않는다
- 판정: 완성 이미지를 **160×90으로 줄여 보고**, 상단 5/8이 회색 덩어리면 다시 만든다

---

## §7. 🧪 A/B 실측 설계 (첫 회차 = [production-queue.md](../production-queue.md) 3번)

**이 계열은 우리 채널 미검증이다. 첫 편은 반드시 통제 실험으로 돌린다.**

1. 같은 프로젝트에서 **실사형 9장 + 일러스트형 9장**을 둘 다 생성한다
2. 정호님이 최종 1장을 고른다
3. **어느 계열을 썼는지 [production-queue.md](../production-queue.md) 해당 항목에 기록한다** — 이걸 안 적으면 실험이 무의미하다
4. 업로드 후 **48시간·7일 조회수·일**을 같은 항목에 기록한다
5. 판정 기준
   - 창 중앙값(현재 28.2회·일) **3배 이상** → 그 계열 유효
   - **1배 미만** → 그 계열 보류, 다른 계열로 다음 편
   - ⚠️ **1편으로 계열을 확정하지 않는다.** 소재·제목이 교란 변수다. 최소 3편을 쌓고 판단한다

> 🔴 **기록하지 않으면 [08-18](https://www.youtube.com/watch?v=33l7widZdTs) 때와 같아진다** — 그때도 「머스크 의존도 실험」이라 적어 뒀기 때문에 하루 만에 원인을 특정할 수 있었다.
