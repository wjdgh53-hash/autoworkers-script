# 실사형 썸네일 프롬프트 규칙

creative-strategy.md Phase 5에서 참조하는 **실사형 계열** 프롬프트 작성 규칙.
사용자가 텍스트를 직접 얹으므로 **이미지에 텍스트를 절대 넣지 않는다.**

> 🚨 이 파일은 **실사형 전용**이다. 국기볼형은 `prompts/thumbnail-countryball.md`를 따르며 **규칙이 정반대다**(실사형=실존 인물 실명 필수 / 국기볼형=실존 인물 절대 금지). 두 계열의 규칙을 섞지 않는다.

---

## 스타일 — 레퍼런스 썸네일을 그대로 베낀다

**이 스타일 하나만 쓴다.** 애니메, 일러스트, 3D 렌더, 카툰 등 다른 아트 스타일은 생성하지 않는다.

> 🚨 **추상적 형용사로 스타일을 지시하지 않는다.** `cinematic`, `commercial style`, `dramatic` 같은 말만 늘어놓으면 레퍼와 전혀 다른 그림이 나온다. 아래 **구성 요소를 장면에 직접 배치**해야 그 스타일이 나온다.

### 레퍼런스 썸네일 해부 — 반복되는 7개 요소

목표하는 스타일은 아래 요소들이 한 화면에 겹쳐 쌓인 **정보 밀도 높은 광고 합성물**이다. 매 장에서 서사에 맞는 것을 **최소 3개 이상** 골라 넣는다.

| # | 요소 | 프롬프트에 쓰는 법 |
|---|------|------------------|
| 1 | **실물 브랜드 제품·간판을 라벨까지 선명하게** | 냉장고·세탁기·TV·주류병·트럭·간판을 실제 브랜드로 배치. `a Samsung refrigerator and an LG washing machine with their logos clearly visible`, `a green delivery truck with the NAVER logo on its side` |
| 2 | **실존 인물 얼굴을 크게, 표정을 극단으로** | 화면 중앙~한쪽에 상반신 컷아웃. 입 가림·경악·환희 등 한 감정을 과장. 밝은 스튜디오 조명으로 얼굴을 띄운다 |
| 3 | **국기를 실물 천 재질로, 승패에 따라 상태를 다르게** | 승자 `a clean crisp flag waving brightly` / 패자 `a torn, scorched, weathered flag` |
| 4 | **초록 상승 / 빨강 하강 화살표를 좌우 대칭으로** | 승패가 갈리는 서사면 두 개를 대칭 위치에 하나씩. 글자를 읽기 전에 승패가 전달된다 |
| 5 | **삽입 액자 패널** | 국기·인물·제품을 별도 사진 패널로 끼워 넣고 흰 테두리를 두른다. `an inset photo panel with a clean white border showing {대상}` |
| 6 | **파손·스파크·균열 이펙트** | 패자 쪽에 배치. 깨진 화면, 스파크 튀는 콘센트, 갈라진 간판, 무너지는 건물 |
| 7 | **사물 표면의 한글 라벨** | 트럭·상자·간판에 한글이 그대로 박혀 있어도 된다. `boxes printed with "네이버배송"`. 단 화면을 가로지르는 제목 오버레이는 금지 |

**프롬프트 앞부분에 항상 명시한다:**

```
photorealistic advertising composite, intense neon glow lighting, emissive brand colors
spilling onto surrounding surfaces, extreme color contrast, the upper three-fifths densely
packed with elements, exaggerated wide-angle perspective, hyper-saturated and eye-catching
```

> 이 문구는 톤만 잡는다. **위 7개 요소를 장면 묘사에 직접 넣지 않으면 스타일이 재현되지 않는다.**

### 눈에 띄게 만드는 것 — 발광과 밀도

> 🚨 **핵심은 배경 밝기가 아니라 "요소가 스스로 빛나는가"다.**
> 레퍼런스는 야간 도시의 어두운 배경인데도 가장 눈에 띈다. NAVER 간판이 형광 초록으로 발광하고, 창고 선반이 네온 라인이고, 박스에까지 초록 반사광이 깔리기 때문이다. 어두운 배경은 그 발광을 튀게 하는 **무대**다.
>
> ⛔ 배경을 하얗게 깔고 요소를 평범하게 배치하면 **광고 카탈로그**가 되고 썸네일로서 죽는다. 실제로 그렇게 만들어 실패했다.

**필수 4요소 — 매 장에 전부 넣는다.**

| # | 요소 | 프롬프트에 쓰는 법 |
|---|------|------------------|
| 1 | **브랜드 컬러가 조명처럼 발광** | `glowing neon green`, `emissive glow`, `light spilling onto surrounding surfaces`, `bloom`. 로고·간판·차량·설비가 스스로 빛나고 그 빛이 주변 사물에 반사되게 한다 |
| 2 | **극단 2색 대비** | 승자색 대 패자색 **단 두 색**으로 화면을 지배한다. 중간색·파스텔을 섞지 않는다. `the entire left half saturated in glowing green, the entire right half in deep glowing red` |
| 3 | **여백 없는 밀도 (상단에 한정)** | **상단 3/5 안에서만** 요소로 꽉 채운다. 컨베이어에 박스 수십 개, 설비, 차량, 화살표, 건물이 동시에. `the upper three-fifths densely packed with` — ⛔ 그냥 `densely packed frame with no empty space`라고 쓰면 하단 세이프존과 정면 충돌해 세이프존이 깨진다 |
| 4 | **원근 과장 + 진행 중인 액션** | 컨베이어나 도로가 화면 밖으로 뻗는 광각. 정적인 진열이 아니라 충돌·수거·붕괴가 **일어나는 중**의 한 순간 |

**배경 톤 선택** — 서사에 따라 고르되, 어느 쪽이든 위 4요소는 지킨다.

- **대결·위기·야간 소재** → 어두운 배경 (`dark night city skyline`, `deep navy sky`). 네온 발광이 가장 강하게 살아난다. **기본으로 쓸 만한 선택**
- **일상·소비·희망 소재** → 밝은 배경. 단 그때도 브랜드 컬러는 발광시키고 밀도를 채운다
- 배경이 어둡다고 피사체까지 어둡게 두지 않는다. 피사체는 항상 강하게 빛난다

**굵기** — 화살표·강조 원은 얇은 그래픽이 아니라 **두껍고 발광하는** 것으로. `thick glowing neon arrow`, `bold red neon ring`

### 브랜드 — 로고와 상호를 전면에 쓴다

> 🚨 **대본에 기업·브랜드가 등장하면, 그 로고와 상호가 썸네일의 1차 후킹 장치다.** 시청자는 로고를 보고 0.3초 만에 "내가 쓰는 그 서비스 얘기구나"를 안다. 이걸 추상 상징으로 바꾸면 후킹이 통째로 죽는다.

- **실제 로고를 실명으로 지정한다.** `the Coupang logo`, `the NAVER green logo`, `the Samsung logo`
  - ❌ `a red corporate logo panel`, `a generic delivery company sign` — 익명화 금지
- **로고를 화면에서 즉시 읽히는 크기로** 배치한다. 구석에 작게 넣지 않는다
- **물건에 브랜드를 입힌다** — 배송 트럭 측면, 택배 상자, 창고 간판, 유니폼, 앱 화면, 제품 실물
  - 예: `a delivery truck with the Coupang logo on its side`, `a warehouse with a large illuminated NAVER sign`
- **두 브랜드가 대결하는 서사면 양쪽 로고를 좌우에 대칭으로** 세워 한눈에 대진표가 보이게 한다
- 제품·모델명도 그대로 보존한다: `Samsung HBM4 memory chip` (O) / `semiconductor chip` (X)
- 브랜드가 없는 주제(국가·산업·사회 현상)에서만 상징물로 간다

### 후처리 요소

서사에 맞을 때만 쓴다. 습관적으로 전부 붙이지 않는다.

| 요소 | 영어 표현 | 쓰는 상황 |
|------|----------|----------|
| 상승/하락 화살표 | `large glowing green upward arrow` / `large glowing red downward arrow` | 성장·추락, 승패 대비 |
| 강조 원 | `bright red neon circle highlighting {대상}` | 한 지점에 시선을 몰 때 |
| 균열 | `deep cracks spreading across {대상}` | 붕괴·와해 |
| 스파크·불꽃 | `bright sparks and embers flying` | 충돌·파손 |
| 연기 | `dark smoke rising` | 위기·화재 |

---

## 구도 — 고정 기본값 없음

**대본의 서사가 구도를 결정한다.** 특정 구도를 기본값으로 두지 않는다.

아래는 후보 목록이다. 서사에 맞는 것을 고르고, **왜 골랐는지 `concept_ko`에 한 줄 적는다.**

| 구도 | 적합한 서사 |
|------|------------|
| 인물 감정 클로즈업 | 한 인물의 반응이 이야기의 핵심일 때 |
| 좌우 대비 | 두 진영·국가·기업의 대립, 승패가 갈릴 때 |
| 중앙 집중 | 하나의 대상에 시선을 몰아야 할 때 |
| 스케일 대비 | 규모 차이 자체가 메시지일 때 |
| 붕괴·균열 | 무너짐·와해가 주제일 때 |
| 그래프·화살표 | 수치 변화가 핵심일 때 |
| 현장 장면 | 사건의 무대를 보여줘야 할 때 |
| 전후 대비 | 과거와 현재의 격차가 핵심일 때 |

> ⚠️ **좌우 대비는 여러 후보 중 하나일 뿐이다.** 대립 구조가 아닌 주제에 억지로 좌우 대비를 씌우지 않는다.

---

## 피사체 — 실명·실물로 특정한다

일반화가 가장 큰 실패다. `an Asian man in a suit`, `a semiconductor chip` 같은 표현은 아무것도 전달하지 못한다.

### 국가 원수 — 현직 실명으로 지정

대본 서사에 국가가 등장하면 **그 나라의 현 국가원수를 실명으로** 넣는다.

| 국가 | 프롬프트 표기 |
|------|--------------|
| 일본 | `Takaichi Sanae (Prime Minister of Japan)` |
| 미국 | `Donald Trump (US President)` |
| 중국 | `Xi Jinping (President of China)` |
| 북한 | `Kim Jong Un (leader of North Korea)` |
| 러시아 | `Vladimir Putin (President of Russia)` |
| 한국 | 현직 대통령 실명 + `(President of South Korea)` |

- 그 외 국가는 리서치로 확인된 현직 지도자를 실명+직함으로 쓴다
- 확인이 안 되면 지도자 대신 **국기·상징물·산업 현장**으로 대체한다. 틀린 이름을 넣지 않는다

### 기업 — 로고를 크게, 총수는 있으면 함께

기업이 주체면 **실제 로고를 화면에서 즉시 읽히는 크기로** 배치한다. 위 "브랜드" 절이 이 계열의 핵심 규칙이다.

- 로고: `the Coupang logo`, `the NAVER green logo`, `the Samsung logo`
- 총수가 서사에 등장하면 실명 병기: `Lee Jae-yong (Samsung Electronics chairman)`, `Jensen Huang (NVIDIA CEO)`
- **총수가 없거나 서사와 무관해도 로고는 반드시 들어간다.** 로고 없이 인물만 세우면 무슨 회사 얘기인지 알 수 없다
- 국내 기업 간 대결이면 **국기가 아니라 로고**로 진영을 나눈다. 한국 회사끼리의 경쟁을 국가 대결처럼 그리면 대본과 어긋난다

### 제품·브랜드 — 고유명사 보존

`HBM4 칩` → `Samsung HBM4 memory chip` (O) / `semiconductor chip` (X)
`참이슬` → `Chamisul soju bottles with green glass` (O) / `soju bottles` (X)

### 국기 — 맥락상 필요할 때만

국가 간 서사라고 해서 자동으로 넣지 않는다. **국기가 그 장면의 의미를 더할 때만** 쓴다.

- 승자 측: `a clean crisp {국가} national flag waving`
- 패자 측: `a torn, scorched, weathered {국가} flag`
- ⛔ **일본 국기는 반드시 일반 국기만**: `Japanese national flag (plain white field with one solid red circle in the center)`. 전범기(旭日旗)는 절대 금지 — `rising sun`, `rays`, `imperial` 등 연상 표현을 쓰지 않는다
- 한국: `South Korean flag (white field with a red-and-blue taeguk circle and four black trigrams)`

---

## 대립 구도 소재 — 우리 쪽 인물을 반드시 세운다

침해·탈취 서사(문화공정·기술 유출·상표 선점 등)에서 **가장 흔한 실패는 화면에 상대만 있는 것**이다. 상대 혼자 곤란해하는 그림은 조소까지만 나오고 분노가 붙지 않는다. 감정을 받아줄 얼굴이 없기 때문이다.

| 규칙 | 내용 |
|------|------|
| **우리 쪽 인물 배치** | 9장 중 최소 5장에 우리 측 인물(장인·근로자·소비자 등)을 세운다. 상대 단독 장면만으로 세트를 채우지 않는다 |
| **손이 닿게 한다** | 상대의 손이 허공에서 멈추면 "못 가졌다"까지만 읽힌다. **가격표 부착·라벨 교체·물건을 안고 걸어감** 등 실제 접촉 동작을 넣어야 침해가 보인다 |
| **표정 온도를 가른다** | 상대 = 능청·무심·계산 / 우리 = **분노**(동공 축소, 눈썹 V자, 벌린 입) 또는 **경멸**(반쯤 감은 눈, 내려간 입꼬리). 둘을 같은 온도로 두지 않는다 |
| **감정 클로즈업 장은 우리 쪽으로** | 7~9번을 상대 얼굴로만 채우면 세트 전체가 상대 시점이 된다. **최소 2장은 우리 쪽 얼굴 클로즈업**으로 — 시청자 이입점이다 |

> 온도 설계의 상위 원칙은 `prompts/ctr-reference.md`의 "대립 구도 소재의 온도 규칙"을 따른다.
> 이 규칙은 **국기볼형에도 그대로 적용**한다.

## 표정 — 대본이 얼굴에서 읽히게

**이 계열의 핵심 규칙이다.** 텍스트는 사용자가 따로 얹으므로, 이미지만으로 전달되는 정보의 대부분이 인물 표정이다. 표정이 밋밋하면 어떤 대본이든 똑같아 보인다.

`shocked` 한 단어로 끝내지 않는다. **눈·입·손동작·부수 요소로 분해해서** 쓴다.

| 요소 | 영어 표현 예 |
|------|-------------|
| 눈 | `eyes wide open showing whites`, `narrowed confident eyes`, `eyes squeezed shut` |
| 입 | `mouth agape`, `lips pressed tight`, `broad triumphant grin` |
| 손 | `hand covering the mouth`, `palm pressed to forehead`, `clenched fist raised`, `pointing finger` |
| 부수 | `beads of sweat on the forehead`, `flushed cheeks`, `pale drained face` |

**서사에 따라 표정을 갈라 쓴다.**
- 패자·당하는 쪽: 경악, 낭패, 당혹 — `eyes wide, hand covering the mouth, beads of sweat`
- 승자·이기는 쪽: 확신, 환희, 여유 — `confident narrowed eyes, broad grin, arms open`

인물이 둘 이상이면 **표정을 반드시 대비**시킨다. 둘 다 같은 표정이면 서사가 전달되지 않는다.

> 징그럽거나 혐오를 유발하는 과장은 금지한다.

---

## 하단 세이프존 — 하단 2/5

화면 **하단 5분의 2는 제목 문구 오버레이 자리**다. 레퍼런스 썸네일도 텍스트가 전체 면적의 35~40%를 쓴다.

- 이 영역에 인물, 로고, 핵심 오브젝트, 손, 실루엣을 배치하지 않는다
- 흐림·어두운 그라데이션·반투명 패널 같은 별도 처리도 넣지 않는다
- 모든 인물과 핵심 피사체는 **상단 5분의 3 안에** 완결적으로 담는다. 인물은 가슴 위 또는 허리 위 구도로 잡고 머리가 잘리지 않게 한다

### 지켜지게 만드는 3가지 (이게 핵심이다)

이미지 모델은 공간 제약을 잘 안 지킨다. 아래를 지키지 않으면 9장 중 절반이 깨진다.

**1. 세이프존 문장을 프롬프트 맨 앞에 둔다.** 장면 묘사 뒤에 붙이면 가중치가 낮아 무시된다.

**2. 부정형이 아니라 긍정형으로 쓴다.** "비워라"라고 하면 모델은 지시를 흘리고, 나열한 명사(characters, objects…)를 오히려 그려 넣는다. **그 자리에 무엇을 그릴지** 지정한다 — 매끈한 아스팔트, 평평한 바닥, 열린 하늘, 단색 벽 중 장면에 맞는 것.

**3. 밀도 지시를 상단으로 한정한다.** `densely packed frame with no empty space`는 세이프존과 정면 충돌한다. 반드시 `the upper three-fifths densely packed`로 범위를 묶는다.

**영어 프롬프트의 첫 문장으로 아래를 넣는다:**

```
COMPOSITION RULE, HIGHEST PRIORITY: the lower two-fifths of this image is one clean continuous
surface — {smooth asphalt / plain floor / open sky / flat wall} — rendered simply and evenly with
nothing on it, and every subject, character, object, effect and action is composed entirely within
the upper three-fifths above it.
```

중괄호는 장면에 맞는 표면 하나로 채운다. 야외 도로면 `smooth asphalt`, 실내면 `plain polished floor`, 하늘이 보이면 `open sky`.

> 그래도 100% 지켜지지는 않는다. **9장 중 2~3장은 깨질 수 있으므로 골라 쓰는 것을 전제로 한다.**

---

## 9장 배분

| # | 목적 | 내용 |
|---|------|------|
| 1~3 | **내용 대표** | 대본의 핵심 장면·데이터를 가장 잘 보여주는 그림 |
| 4~6 | **제목 대표** | 확정 제목이 약속한 것을 시각적으로 가장 잘 이행하는 그림 |
| 7~9 | **레퍼 계승 / 감정 클로즈업** | 아래 성립 조건에 따라 갈린다 |

- **같은 그룹 안의 3장은 서로 완전히 다른 그림**이어야 한다. 같은 장면의 색·앵글만 바꾼 변형은 금지 — 선택지를 넓히려고 9장으로 늘린 것이므로 유사 컷이 섞이면 목적이 사라진다
- 그룹마다 **구도 패턴을 3개 다르게** 고른다 (예: 내용 대표 = 스케일 대비 / 현장 장면 / 감정 투샷)
- **9장 전부 표정이 달라야 한다.** 인물이 겹치더라도 감정·시선·손동작 중 최소 2개는 달리한다

### 7~9번 장 — 계승이 성립하는 경우에만 계승한다

3장을 같은 계승 구도로 채우면 서로 비슷해진다. **계승이 성립해도 최소 1장은 감정 클로즈업으로** 둔다.

| 상황 | 7~9번 구성 |
|------|-----------|
| 계승 성립 | 계승 1~2장 + 감정 클로즈업 1~2장 |
| 계승 불성립 | 감정 클로즈업 3장 — **인물·감정·앵글을 각각 다르게** (예: 분노 / 경멸 / 헛웃음) |

> **계승은 제목과 썸네일을 같은 앵커에서 함께 가져왔을 때 성립한다.**
> 패키지 D는 제목 골격과 썸네일 구도를 한 앵커에서 같이 물려받아 둘이 한 몸으로 작동한다.
> 제목이 독자적으로 설계된 프로젝트(패키지 A·B·C 확정, 또는 구형 프로젝트)에는 **그 짝이 없다.**
> 검증된 구도라는 이유만으로 무관한 제목에 얹으면 텐션 트라이앵글이 깨진다.

**어느 레퍼의 구도를 볼 것인가 — 짝의 근접성이 조회수보다 우선한다.**

concept.md의 "참고 레퍼 → 썸네일 계승 후보"를 먼저 본다. 확정된 패키지가 실제로 참고한 레퍼가 있으면 **그 레퍼**를 쓴다. 전역 앵커(조회수/일 1위)보다 우선한다.

확정 제목이 레퍼3을 참고해 만들어졌다면 레퍼3의 구도가 그 제목과 훨씬 잘 붙는다. 조회수 1위라는 이유만으로 무관한 레퍼를 끌어오면 5번 장의 존재 이유가 사라진다.

| 상황 | 볼 레퍼 | 5번 장 |
|------|---------|--------|
| **패키지 D 확정** | 앵커 (제목도 여기서 계승) | **레퍼 계승**. 짝이 맞으므로 그대로 진행 |
| **A·B·C 확정 + 참고 레퍼 있음** | **그 참고 레퍼** | 구도가 **확정 제목의 약속을 이행할 수 있으면** 계승, 아니면 **감정 클로즈업** |
| **A·B·C 확정 + 참고 레퍼 없음** (완전 독자 설계) | 전역 앵커 | 위와 동일 판정 |
| `_refs` 없음 / `thumbnail.webp` 없음 | — | 판정 불가 → **감정 클로즈업** |

- **감정 클로즈업**: 인물 또는 핵심 대상을 크게 잡아 표정·상태만으로 승부한다. 배경과 부수 요소는 물러난다
- 계승을 쓰기로 했으면 `_refs/{앵커}/analysis.md`의 비주얼 분석과 `thumbnail.webp`를 근거로 삼는다
- 어느 쪽을 골랐든 `concept_ko`에 판정 근거를 적는다

> ⚠️ **5번은 구도만 계승한다. 그림을 통째로 옮기지 않는다.**
> 계승하는 것: **화면 분할 방식, 시선 흐름, 요소의 상대적 크기·위치 관계**
> **반드시 다르게 할 것 — 아래 중 최소 3개:**
> 1. 피사체 (필수)
> 2. 색 팔레트 또는 전체 톤
> 3. 카메라 시점·앵글
> 4. 강조 요소 (화살표·균열·스파크 등의 종류와 위치)
> 5. 인물 표정의 감정 방향
>
> `concept_ko`에 **무엇을 계승했고 무엇을 다르게 했는지** 항목으로 적는다. 같은 주제를 다룰 때 특히 닮기 쉬우니 주의한다.

---

## 프롬프트 작성 규칙

1. **영어로 작성** — AI 이미지 생성 모델에 최적화
2. **3~5문장** — 구체적이고 생생하게, 과도하게 길지 않게
3. **스타일 문구를 앞부분에 명시** — 위 "스타일" 섹션의 고정 문구
4. **구도를 구체적으로 서술** — 좌우 배치, 중앙 집중, 원근, 카메라 각도
5. **모바일 주목성** — 160×90px로 줄여도 핵심이 인지되게 피사체를 크고 명확하게
6. **텍스트 절대 금지** — `no text, no letters, no words, no numbers, no watermark`를 항상 포함
7. **실존 인물이 아닌 일반 인물**이 등장할 경우 호감형으로: `attractive person with a warm likeable face`

---

## 채널 설정 반영 (`config/thumbnail-strategy.json`)

없으면 기본값을 쓴다.

| 필드 | 반영 방식 | 기본값 |
|------|----------|--------|
| `count` | 생성 장수 | 5 |
| `color_palette` | `auto`=**주제에 따라 판단**(기본) / `bright`=`bright vibrant colors, clean high-key background` / `dark`=`dark cinematic atmosphere, deep shadows` / `neon`=`neon glow, vivid fluorescent accents` | `auto` |
| `emotions` | `shock`=표정 과장 극대화 / `tension`=`ominous atmosphere, cracks, dark shadows` / `curiosity`=`partially revealed, intriguing` | `["shock","tension"]` |
| `text_space` | `bottom-third` 고정 (위 세이프존 규칙) | `bottom-third` |
| `brand.colors` | 지정된 색을 포인트 컬러로 반영 | 없음 |

> `art_styles`는 더 이상 쓰지 않는다. 실사형은 단일 스타일이다.
>
> ⚠️ `color_palette`가 `dark`로 지정돼 있어도 **모든 장을 어둡게 만들지 않는다.** 위 "밝기" 절이 우선한다 — 어둠은 서사가 어두울 때만 쓰고, 그때도 피사체는 밝게 분리한다.

---

## 출력 형식

`{P}/output/thumbnails/prompts.json`

```json
{
  "meta": {
    "project": "{프로젝트명}",
    "style": "photorealistic",
    "titles": ["{확정 제목}", "{제목 후보 2}", "{제목 후보 3}"],
    "thumbnail_texts": ["{텍스트 세트 1}", "{텍스트 세트 2}", "{텍스트 세트 3}"],
    "anchor_ref": "{앵커 레퍼 번호} — {앵커 제목}"
  },
  "thumbnails": [
    {
      "id": 1,
      "purpose": "content",
      "composition": "인물 감정 클로즈업",
      "concept_ko": "다카이치가 220V 전환 발표를 듣고 경악하는 순간. 대본 파트 3의 '일본 가전이 한국 규격에 밀렸다' 장면이 근거.",
      "prompt_en": "..."
    },
    { "id": 2, "purpose": "content", "...": "..." },
    { "id": 3, "purpose": "title", "...": "..." },
    { "id": 4, "purpose": "title", "...": "..." },
    {
      "id": 5,
      "purpose": "reference-inherit",
      "composition": "{앵커 구도 패턴}",
      "concept_ko": "앵커 003의 좌우 대비 + 우측 붕괴 건물 구도를 계승. 피사체만 교체.",
      "prompt_en": "..."
    }
  ]
}
```

| 필드 | 설명 |
|------|------|
| `meta.style` | 항상 `"photorealistic"` |
| `purpose` | `content`(1~2) / `title`(3~4) / `reference-inherit` 또는 `emotion-closeup`(5) |
| `composition` | 이 장에서 고른 구도 패턴명 |
| `concept_ko` | 무엇을 보여주는지 + **왜 이 구도인지 대본 근거** 1~2문장 |
| `prompt_en` | 영어 프롬프트 (3~5문장, 스타일 문구 + 세이프존 문장 + 텍스트 금지 문구 포함) |
