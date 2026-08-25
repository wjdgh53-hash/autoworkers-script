# 벤치마크 후보 풀 + 히트 패턴 — 방구석 경제

> 최초 작성 **2026-08-21** · 근거 [_diagnosis/2026-08-21_방구석economy.md](../../_diagnosis/2026-08-21_방구석economy.md)
> 판정 완료 채널은 [channels.md](channels.md)에 있다. **이 파일은 미판정 발굴 후보 + 히트 패턴 분석이다.**
>
> 🎯 **방침 (2026-08-21 정호님)**
> 「같은 결 채널을 **많이** 찾아 → 각 채널 **인기순 상위**를 뽑고 → **배수**로 정렬해 고배수 소재를 캐낸다.
> 그리고 **터지는 소재들의 공통 패턴을 뽑는다.**」
> **배수 = 그 영상이 나올 당시 채널력 대비 성과.** 배수가 높다 = 채널이 작아도 소재가 끌어올렸다
> = **구독 6,370인 우리가 들어가도 재현 가능하다.** 절대 조회수가 아니라 이 배수로 줄을 세운다.
>
> 🔗 모든 항목에 영상 URL을 병기한다. ⛔ **ID를 확인하지 못한 영상은 링크를 만들지 않는다**(2026-08-21 자체 오류 재발 방지).

---

# 1부 — 🔴 터지는 소재의 공통 패턴 (2026-08-21 1차 추출)

표본: [경제해적단](https://www.youtube.com/@경제해적단-t5m) 히트 9편(15만 이상) vs 부진 8편(1만 미만).
**같은 채널·같은 포맷·같은 길이대(13~23분)라 사실상 통제 실험이다.**

## 히트군 (15만 이상)

| 영상 | 조회 | 길이 |
|---|---|---|
| [국민성장펀드 vs 반도체 ETF \| **같은 3000만원**, 5년 뒤 손에 쥐는 돈이 다릅니다](https://www.youtube.com/watch?v=yysVN041wz8) | **637,163** | 16:08 |
| [**금융자산 10억** 생기면 실제로 벌어지는 일 **6가지** (세금·심리·현금흐름 전부)](https://www.youtube.com/watch?v=QdtKu0Zfw14) | **633,252** | 20:22 |
| [주식으로 돈 잃는 **4가지 패턴** \| 추격매수→물타기→손절못하기→원금대기의 끝](https://www.youtube.com/watch?v=-27Dlgpfr60) | **386,711** | 16:55 |
| ["주식으로 조용히 부자 된 사람들" 이 10년간 딱 지킨 **5가지 원칙**](https://www.youtube.com/watch?v=IinIFTY18jk) | **362,029** | 22:36 |
| [**1억을 20억**으로 만드는 **4가지 전략** \| **99%가 모르는** 부자의 비밀](https://www.youtube.com/watch?v=OzboXb0oVKY) | **344,763** | 16:20 |
| [**-30% 물린 종목**, 팔아야 할까 버텨야 할까 \| 손절 기준 **3가지**](https://www.youtube.com/watch?v=dVSpaWB1IZs) | **307,957** | 13:34 |
| [**같은 S&P500**인데 세금 **970만 vs 3700만원**…**종목 아니라 '이것'** 때문입니다](https://www.youtube.com/watch?v=JREdVuRBv9U) | **289,881** | 23:08 |
| [돈이 스스로 일하기 시작하는 시작점](https://www.youtube.com/watch?v=PEnNxbBd5eY) | **217,191** | 22:36 |
| [달러 패권의 **진짜 전략**, 한국 투자자가 놓치면 안 될 것](https://www.youtube.com/watch?v=NID7VESSER8) | **161,067** | 22:33 |

## 부진군 (1만 미만)

| 영상 | 조회 | 왜 죽었나 |
|---|---|---|
| [**"2배 벌려다 4배 잃었다" 레버리지 절대 하면 안 되는 5가지**](https://www.youtube.com/watch?v=rHKJbvIGft8) | **2,201** | 내가 안 하는 일 |
| [의외로 잘 모르는 **엔화 약세**의 진짜 이유](https://www.youtube.com/watch?v=ztlNzqArChw) | 5,287 | **시의성**·해설 |
| [**연금저축**은 이렇게 활용해야 돈이 쌓입니다](https://www.youtube.com/watch?v=g45m3De3D-M) | 5,922 | 실무 절차 |
| [**현시점** 삼전, 하이닉스 지금 사면 "역대급 세일일까?"](https://www.youtube.com/watch?v=U4lEeRDKZD0) | 6,426 | **시의성**·종목 |
| ["계란 나눠 담지 마라" **시드머니 1억 미만**일때](https://www.youtube.com/watch?v=xtKgPnxXenA) | 7,110 | 조언형 |
| [월급 250만원으로 20억 만드는 법](https://www.youtube.com/watch?v=_5H7MVsb1Rk) | 8,751 | 조건이 남 얘기 |
| ["부자들이 더 부자되는 시기"](https://www.youtube.com/watch?v=I3-Up8QGbcU) | 9,210 | 금액 없음·추상 |
| ["빚도 자산이 된다?" 부자들이 레버리지를 쓰는 진짜 이유](https://www.youtube.com/watch?v=WuQx7h9EYaQ) | 9,923 | 내가 안 하는 일 |

---

## 🔴🔴 11채널 전수 스캔 (2026-08-21) — 전편 + 시점 보정 배수

> 도구: `scan_channel.py`(스크래치패드). 채널 전편을 받아 **업로드일 ±3주 이웃 편들의 중앙값**을 분모로 배수를 계산한다.
> 자기 자신은 분모에서 제외한다. 이웃이 3편 미만이면 창을 2배로 넓힌다. 채널당 45~50편.

| 채널 | 구독 | 중앙값 | **최고배수** | 최고작 유형 | 판정 |
|---|---|---|---|---|---|
| ⭐ [자본의 기록](https://www.youtube.com/channel/UCa0pvW8gytqAeijDDzXN8aQ) | **3,080** | 254 | **36.7배** | **P0** 10억 달성 후 | 패턴 근거 (⚠️06-25 중단) |
| ⭐⭐ [차윤호 스플릿](https://www.youtube.com/channel/UCnE_A6f34Dx2hemI4QeBkOg) | **13,900** | 3,858 | **41.0배** | **P0** 1억 상위 몇% | **체급 적합 1순위** |
| ⭕ [부자아빠의 경제학](https://www.youtube.com/channel/UChUIo6kavReZaRCIj_reZvg) | 54,900 | 5,205 | 28.0배 | 시사 / **2위가 P0** 15.8배 | 유효 |
| ⚠️ [어니스트와 투자 빌드업](https://www.youtube.com/channel/UCHWFdDG50K-k8btmLG_2Lcg) | 81,200 | 2,090 | 12.2배 | 망하는 **과정**(P6) | ⚠️ 06-02 중단 |
| ⭐ [경제해적단](https://www.youtube.com/@경제해적단-t5m) | 101,000 | 8,981 | 92.8x* | **P0** 10억 | **주 벤치** |
| ⛔ [위즈덤투스](https://www.youtube.com/channel/UCiAM9aJjVTmhtYgj0cyTPzA) | 114,000 | 29,970 | **2.6배** | 시황·종목 | **이상치 없음 → 제외** |
| ⭕ [집구석 경제학](https://www.youtube.com/channel/UCdA_ovMcYiNgbkf4624Tbxw) | 133,000 | 4,882 | 7.8배 | **P0** 연령별 순자산 등수 | 시황 채널인데 P0만 튐 |
| ⛔ [머니버디](https://www.youtube.com/channel/UCAi37F2UKYDcB40Hq13NJ3w) | 149,000 | 10,311 | **2.6배** | 매매 기법 | **이상치 없음 + 25-02 중단** |
| ⭕ [쩐문가](https://www.youtube.com/channel/UCuE1ykAWttKJZIVS7nMzKvw) | 162,000 | 8,474 | **30.9배** | **P0** 통장에 10억 | 인터뷰 포맷(소재만) |
| ⭕ [똑재TV](https://www.youtube.com/channel/UCmshc9VpICv4oPyjMK3Vk_w) | 165,000 | 37,117 | 12.6배 | **P0** 10억 도달 | ETF 실무 |
| ⭕ [경제학 똑똑](https://www.youtube.com/channel/UC2aLhOkPPZEfxTGV7OqffbQ) | 256,000 | 7,743 | **33.2배** | 도달 경로(100만→1억) | 유효 |
| ⛔ [떠먹여주는TV](https://www.youtube.com/channel/UC5dEgOV_mGqMHXizL1drtvA) | 719,000 | 3,383 | 9.2배 | **정치·시사·군사** | **결 불일치 → 제외** |

*경제해적단만 vidIQ 값(정호님 화면). 나머지는 자체 시점 보정 계산.

> ⚠️ **떠먹여주는TV는 제 오판이었다.** 검색에서 「금융자산 10억」 편 하나를 보고 후보에 올렸는데, 실제로는 **진재일 교수·이철재 기자 인터뷰를 하루 11편씩 올리는 정치·시사 채널**이었다. 그 1편이 예외였다.

### ⭐ 발견 1 — 우리 체급 채널에서 41배가 나왔다

[차윤호 스플릿](https://www.youtube.com/channel/UCnE_A6f34Dx2hemI4QeBkOg)은 **구독 13,900 = 우리(6,370)의 2.2배**로, 체급 기준(0.5~4배)에 정확히 들어오는 유일한 채널이다.

| 배수 | 영상 | 조회 | 길이 |
|---|---|---|---|
| **41.0배** | [주식에 **1억 투자**하면 대한민국 **상위 몇%**일까? (데이터 보고 충격받았습니다)](https://www.youtube.com/watch?v=HiWkdp35UbQ) | 179,070 | **8:05** |
| 6.0배 | [**연령별 평균 자산** 현실? 데이터 보고 충격받았습니다](https://www.youtube.com/watch?v=NuEzO-4r4Zo) | 33,140 | 21:43 |
| 3.6배 | [개미투자자가 주식으로 살아남는법? 그냥 이렇게만 하세요](https://www.youtube.com/watch?v=IZsqM0ifWXo) | 37,996 | 17:44 |
| 3.5배 | [주식으로 인생 망하는 사람들의 공통점](https://www.youtube.com/watch?v=vTj9mTDJ_GI) | 16,112 | 16:00 |

**1·2위가 같은 구조다 — 「내가 어디쯤인가」를 돈 액수로 알려준다.**

### ⛔ 발견 2 — 시의성 채널은 배수가 아예 안 터진다

[위즈덤투스](https://www.youtube.com/channel/UCiAM9aJjVTmhtYgj0cyTPzA)는 45편 **전부 1~2배대**이고 최고가 2.6배다. 매일 시황·종목을 올리는 채널이라 **모든 편이 비슷하게 소비되고 이상치가 생기지 않는다.**

> 🔴 **이게 우리에게 결정적이다.** 구독 6,370에서 노출 293을 뚫으려면 **이상치가 필요하다.** 안정적 1~2배로는 못 뚫는다.
> ⛔ **위즈덤투스는 벤치 대상이 아니다.** 「시의성으로 가면 이렇게 된다」는 **반증 사례**로만 등재한다.
> 근거 보강: 같은 [물타기 vs 손절 소재](https://www.youtube.com/watch?v=mVpZc_HKBvU)가 위즈덤투스에선 **1.1배**(19,907)인데 경제해적단에선 [28.5배](https://www.youtube.com/watch?v=dVSpaWB1IZs)(307,957)다. **채널 성격이 다르면 같은 소재도 안 터진다.**

### 🚨 발견 3 — 패턴 P3이 반례로 깨졌다

똑재TV에서 **시의성인데 크게 터진 편**이 나왔다.

| 영상 | 조회 | 배수 | 성격 |
|---|---|---|---|
| [국민성장펀드 가입방법 \| 추천 VS 비추천, 유의사항](https://www.youtube.com/watch?v=PxYkrA9kBAg) | 566,586 | **8.4배** | **신상품 = 시의성** |
| [ISA 개정안 개편 총정리 \| 불리해진 기존 ISA계좌 당장 이것부터](https://www.youtube.com/watch?v=06TR8uFsbkk) | 279,859 | **3.6배** | **제도 변경 = 시의성** |

vs 경제해적단에서 죽은 시의성 편 — [엔화 약세](https://www.youtube.com/watch?v=ztlNzqArChw) 5,287 · [현시점 삼전·하이닉스](https://www.youtube.com/watch?v=U4lEeRDKZD0) 6,426.

> **갈린 건 「날짜가 붙었나」가 아니라 「내 계좌가 바뀌나」다.**
> ISA 개정·국민성장펀드는 **내 계좌에 직접 손대야 하는 일**이고, 엔화 약세는 **읽고 끝나는 뉴스**다.
> → **P3은 독립 패턴이 아니었다. P4(내 상태)의 파생이다.** 아래에서 수정한다.

### 🔴🔴 발견 5 — **「10억」이 최적 금액이다. 같은 채널에서 27배 갈렸다**

[부자아빠의 경제학](https://www.youtube.com/channel/UChUIo6kavReZaRCIj_reZvg)에 **완벽한 통제 실험**이 있다.
같은 채널 · 같은 제목 골격 · 같은 포맷 · 3개월 차이. **다른 건 금액 하나뿐이다.**

| 영상 | 조회 | 배수 |
|---|---|---|
| [금융자산 **10억**이 생기면 당신에게 일어나는 변화들](https://www.youtube.com/watch?v=iUV_Dr-2ecI) | **84,377** | **15.8배** |
| [금융자산 **20억**이 생기면 당신에게 일어나는 변화들 (10억과 비교)](https://www.youtube.com/watch?v=OQcQzXSXCAg) | **3,111** | **1.6배** |

**조회수 27배. 배수 10배.** 금액을 20억으로 올리자 죽었다.

#### 「10억」이 5개 채널 전부에서 최상위다

| 채널 | 구독 | 영상 | 조회 | 배수 |
|---|---|---|---|---|
| 자본의 기록 | 3,080 | [부자들이 죽어도 지키는 철칙 "**10억 달성 후**…"](https://www.youtube.com/watch?v=j_m6PEB61fY) | 20,673 | **36.7배** (1위) |
| 쩐문가 | 162,000 | [**통장에 10억이 쌓이면** 그때서야 알게되는 현실](https://www.youtube.com/watch?v=7BIXcCsBb1s) | 143,419 | **30.9배** (1위) |
| 똑재TV | 165,000 | [**금융자산 10억 도달**하면 반드시 겪게 됩니다](https://www.youtube.com/watch?v=w0tGUgRg9mM) | 730,756 | **12.6배** (1위) |
| 부자아빠의 경제학 | 54,900 | [**금융자산 10억**이 생기면](https://www.youtube.com/watch?v=iUV_Dr-2ecI) | 84,377 | **15.8배** (2위) |
| 경제해적단 | 101,000 | [**금융자산 10억** 생기면 실제로 벌어지는 일 6가지](https://www.youtube.com/watch?v=QdtKu0Zfw14) | 633,252 | **92.8x** |

> **「10억」은 한국에서 「부자의 기준선」으로 사회적 합의가 된 숫자다.**
> 5억은 아직 아니고, 20억·30억·50억은 **내 얘기가 아니게 된다.** 모수가 급격히 줄어든다.
> ⛔ **금액을 키우고 싶은 유혹을 이겨야 한다.** 20억으로 올리면 27배가 날아간다.

### 🔴🔴 발견 6 — **채널 유형이 배수 상한을 정한다**

11곳을 유형별로 묶으면 **최고 배수가 유형별로 갈린다.**

| 유형 | 채널 (최고 배수) | 배수 대역 |
|---|---|---|
| **상태·위치형** | 차윤호 **41.0** · 자본의 기록 **36.7** · 경제학 똑똑 **33.2** · 쩐문가 **30.9** · 경제해적단 **92.8** | **30~92배** |
| 실무·제도형 | 똑재TV 12.6 · 부자아빠 15.8(P0편) | 12~16배 |
| ⛔ **기법·시황형** | 위즈덤투스 **2.6** · 머니버디 **2.6** | **2~3배** |

> 🔴 **이게 우리에게 가장 중요한 발견이다.**
> [위즈덤투스](https://www.youtube.com/channel/UCiAM9aJjVTmhtYgj0cyTPzA)(114,000)와 [머니버디](https://www.youtube.com/channel/UCAi37F2UKYDcB40Hq13NJ3w)(149,000)는 **구독이 우리의 18~23배인데 최고 배수가 2.6배**다. 매일 시황·기법을 올려 **모든 편이 비슷하게 소비되고 이상치가 생기지 않는다.**
> 반면 **구독 3,080인 [자본의 기록](https://www.youtube.com/channel/UCa0pvW8gytqAeijDDzXN8aQ)이 36.7배를 냈다.**
>
> **구독 6,370에서 노출 293을 뚫으려면 이상치가 필요하다. 안정적 2배로는 못 뚫는다.**
> → **소재축을 「상태·위치형」으로 고정한다.** 기법·시황은 하지 않는다.
>
> 🧪 **교차 증거**: [집구석 경제학](https://www.youtube.com/channel/UCdA_ovMcYiNgbkf4624Tbxw)(133,000)은 시황 채널이라 45편이 2.1~3.3배인데, **P0 편 하나만 7.8배**로 튀었다 — [연령별 평균 순자산… (내 자산의 등수는) 자산별 8계급, 여러분은 몇 층에 계신가요?](https://www.youtube.com/watch?v=vgAG-Ri7-6M) 37,844회.
> **시황 채널 안에서도 P0만 튄다.**

### 📏 발견 4 — 길이는 변수가 아닐 수 있다

41배 편이 **8분 5초**다. 똑재TV 히트작도 13~19분, 경제해적단은 13~23분으로 흩어져 있다.
⚠️ 다만 **우리 자체 데이터로는** 히트 2편이 17~18분이라 지금 [direction.md](../../direction.md) 8절(16~20분)을 바꿀 근거는 부족하다. **관찰로만 남긴다.**

---

## 🔴 추출된 패턴

### ⭐⭐⭐ P0. **「자산 총액으로 내 위치를 확인시켜준다」 — 구독 3,080~165,000 전 구간에서 최상위. 체급을 타지 않는다 (2026-08-21 확정)**

> **이 장르의 단일 최강 골격이다.** 체급이 **54배 차이 나는 4개 채널에서 전부 1위 또는 최상위**가 이 구조다.

#### 체급별 검증표 — 이게 P0의 근거다

| 구독 | 채널 | 대표작 | 조회 | **배수** | 채널 내 순위 |
|---|---|---|---|---|---|
| **3,080** | [자본의 기록](https://www.youtube.com/channel/UCa0pvW8gytqAeijDDzXN8aQ) | [부자들이 죽어도 지키는 철칙, "**10억 달성 후** 3년은 죽은 듯이 지내라"](https://www.youtube.com/watch?v=j_m6PEB61fY) | 20,673 | **36.7배** | **1위** |
| **13,900** | [차윤호 스플릿](https://www.youtube.com/channel/UCnE_A6f34Dx2hemI4QeBkOg) | [주식에 **1억 투자**하면 대한민국 **상위 몇%**일까?](https://www.youtube.com/watch?v=HiWkdp35UbQ) | 179,070 | **41.0배** | **1위** |
| 101,000 | [경제해적단](https://www.youtube.com/@경제해적단-t5m) | [**금융자산 10억** 생기면 실제로 벌어지는 일 6가지](https://www.youtube.com/watch?v=QdtKu0Zfw14) | 633,252 | **92.8x**(vidIQ) | 최상위 |
| 165,000 | [똑재TV](https://www.youtube.com/channel/UCmshc9VpICv4oPyjMK3Vk_w) | [**금융자산 10억 도달**하면 반드시 겪게 됩니다](https://www.youtube.com/watch?v=w0tGUgRg9mM) | 730,756 | **12.6배** | **1위** |

> 🔴 **구독 3,080은 우리(6,370)보다 작다.** 「이미 커서 되는 것」이라는 반론이 여기서 완전히 막힌다.

#### 🚨 자본의 기록 — 상위 15편 중 13편이 P0다 (구독 3,080 · 전체 중앙값 254)

| 배수 | 영상 | 조회 |
|---|---|---|
| **36.7배** | [부자들이 죽어도 지키는 철칙, "**10억 달성 후** 3년은 죽은 듯이 지내라"](https://www.youtube.com/watch?v=j_m6PEB61fY) | 20,673 |
| **21.8배** | [**30억 자산가**는 돈을 이렇게 봅니다 ｜ 진짜 기준 5가지](https://www.youtube.com/watch?v=wRPHWu-oPxA) | 7,576 |
| **20.3배** | ["**30억 넘어가니** 세상이 다르게 보입니다"](https://www.youtube.com/watch?v=86ueOSQRrD8) | 8,016 |
| **14.0배** | [**자산 20억 자산가**가 말하는 "돈이 돈을 버는" 진짜 의미](https://www.youtube.com/watch?v=Wli8W-PMq5g) | 3,510 |
| 5.1배 | [**1억, 5억, 10억, 30억**, 자산별 돈 관리법이 다릅니다](https://www.youtube.com/watch?v=aWEb3jVban8) | 1,363 |
| 5.0배 | ["**10억은 이제 큰 돈이 아닙니다**"](https://www.youtube.com/watch?v=LwmvudYj3TQ) | 1,146 |
| 3.7배 | [**자산 5억 달성 후**, 다음 목표는 10억이 아닙니다](https://www.youtube.com/watch?v=XWDKrydLUlg) | 866 |
| 3.5배 | [**1억, 5억, 10억.** 자산별로 다른 투자법](https://www.youtube.com/watch?v=iSkxnAz_ucc) | 887 |
| 3.4배 | [**50억 부자**가 끝까지 지키는 투자 원칙](https://www.youtube.com/watch?v=iqrPmWjiopc) | 1,172 |
| 3.1배 | [**자산 50억 슈퍼리치**들이 자녀에게만 몰래 가르치는 '돈의 조기교육'](https://www.youtube.com/watch?v=_X4iYE0Iop4) | 798 |
| 3.0배 | [**10억 금융자산가**는 이렇게 합니다](https://www.youtube.com/watch?v=0_Rqp4a6DDA) | 1,044 |
| 2.9배 | [부자들의 '**10억의 벽**'을 뚫은 3가지 비밀](https://www.youtube.com/watch?v=x5STyxhYt7I) | 1,131 |
| 2.8배 | [**10억 없어도** 가능합니다. **단돈 2억대**로 **월 배당 300만 원**](https://www.youtube.com/watch?v=bPbudYhsRpA) | 489 |

⚠️ **건전성**: 자본의 기록은 **06-25 이후 업로드 중단**(2개월). 채널 계승 대상은 아니고 **패턴 근거로만 쓴다.**

#### 🔴 P0의 경계 — 「자산 총액」이어야 한다. 「월 현금흐름」은 아니다

같은 채널에서 **금액이 있는데도 죽은 편**이 P0의 정확한 범위를 알려준다.

| 산다 (자산 총액 = 내 위치) | 죽는다 (월 현금흐름 = 방법론) |
|---|---|
| **10억 달성 후** 36.7배 · **30억 자산가** 21.8배 | [**월 400만 원** 현금흐름 만든 사람들은 결국 이것부터 바꿨습니다](https://www.youtube.com/watch?v=rRkbQAeJsF4) **0.5배**(348회) |
| **자산 20억** 14.0배 · **자산 5억 달성 후** 3.7배 | [**월 400만 원** 현금흐름을 못 만드는 사람들의 가장 큰 착각](https://www.youtube.com/watch?v=EXrAAUlUxB8) **0.9배**(666회) |
| | [50대 이후 돈이 줄어드는 사람들의 공통점 7가지](https://www.youtube.com/watch?v=gOGDF9A9kOA) *(금액 없음)* **0.3배**(177회) |

> **총액은 「나는 어디쯤인가」를 묻고, 월 얼마는 「어떻게 하면 되나」를 묻는다.**
> **전자만 터진다.** 시청자는 자기 위치를 확인하려고 들어온다.

**골격**: `[자산 총액]을 가지면 / 도달하면 / 넘어가면` + `내가 어디쯤인가(상위 몇% / 무슨 일이 벌어지나 / 뭐가 달라지나)`

시청자가 답을 확인하려면 **자기 숫자를 대입해야 한다.** 그래서 클릭에서 끝나지 않고 **시청 지속**까지 끌고 간다.

---

### P1. 제목에 **원 단위 구체 금액**이 박힌다

히트 9편 중 **6편**: `3000만원` · `10억` · `1억→20억` · `-30%` · `970만 vs 3700만`
부진군에서 금액이 있는 2편(`시드머니 1억`·`월급 250만원`)은 **금액이 조건절**이라 시청자를 걸러낸다.

> **금액은 「내가 가진/잃은 액수」로 써야 한다. 「이 금액이 있는 사람만」으로 쓰면 죽는다.**

### P2. ⭐ **「같은 조건인데 갈렸다」 대비 구조** — 가장 강한 골격

| 영상 | 조회 |
|---|---|
| [**같은 3000만원**, 5년 뒤 손에 쥐는 돈이 **다릅니다**](https://www.youtube.com/watch?v=yysVN041wz8) | **637,163** (채널 1위) |
| [**같은 S&P500**인데 세금 **970만 vs 3700만원**](https://www.youtube.com/watch?v=JREdVuRBv9U) | 289,881 |

같은 조건에서 결과가 갈리면 **"나는 어느 쪽인가"** 가 즉시 발동한다.
🔗 이건 [config/pd-guide.md](../pd-guide.md) 오프닝 5단 공식의 「두 사람 대비+금액」과 **같은 장치**다. 제목·썸네일·오프닝에 동시에 세운다.

### 🔴 P3. ~~날짜가 붙으면 죽는다~~ → **「읽고 끝나는 뉴스」가 죽는다** (2026-08-21 반례로 수정)

**최초 판정은 틀렸다.** 똑재TV에 시의성인데 크게 터진 편이 있다(위 발견 3).

| 시의성인데 **산다** | 시의성이라 **죽는다** |
|---|---|
| [국민성장펀드 가입방법](https://www.youtube.com/watch?v=PxYkrA9kBAg) 566,586 (**8.4배**) | [엔화 약세의 진짜 이유](https://www.youtube.com/watch?v=ztlNzqArChw) 5,287 |
| [ISA 개정안 개편 총정리](https://www.youtube.com/watch?v=06TR8uFsbkk) 279,859 (**3.6배**) | [현시점 삼전·하이닉스](https://www.youtube.com/watch?v=U4lEeRDKZD0) 6,426 |
| → **내 계좌에 직접 손대야 하는 일** | → **읽고 끝나는 뉴스** |

> **수정된 규칙: 「내 계좌가 바뀌는가」가 기준이다. 날짜는 기준이 아니다.**
> ⚠️ **P3은 독립 패턴이 아니라 P4(내 상태)의 파생이다.** 다음 회차에 두 항목을 통합할지 검토한다.
> ⭕ 다만 **에버그린이 롱테일을 만든다는 사실은 그대로다** — 경제해적단 히트 9편이 1~4개월 뒤에도 VPH 12~135로 돌고 있다. 우리 [08-10](https://www.youtube.com/watch?v=CKEBf-52HBo)도 11일 차 +437회/일이다.
> 🔗 원본 규칙은 [direction.md](../../direction.md) **1-2절**이다. **그 절의 「날짜가 없다」 조건도 함께 고쳐야 한다.**

### P4. **내가 지금 그 상태여야 한다** (명명 테스트)

| 산다 | 죽는다 |
|---|---|
| [**-30% 물린 종목**](https://www.youtube.com/watch?v=dVSpaWB1IZs) — 나 지금 물려 있다 | [**레버리지** 하지 마라](https://www.youtube.com/watch?v=rHKJbvIGft8) — 나 안 한다 |
| [**돈 잃는 4가지 패턴**](https://www.youtube.com/watch?v=-27Dlgpfr60) — 내가 그중 하나다 | [**부자들이** 레버리지 쓰는 법](https://www.youtube.com/watch?v=WuQx7h9EYaQ) — 부자 얘기 |
| [**10억 생기면**](https://www.youtube.com/watch?v=QdtKu0Zfw14) — 내 미래 상태 | 예순 부부의 2억 — 남 얘기 |

🔗 원본 규칙은 [direction.md](../../direction.md) **1-1절 「내 상태 명명 테스트」**다.

### P5. **원인이 뻔한 게 아니라고 못 박는다**

`종목 아니라 '이것' 때문` · `99%가 모르는` · `진짜 전략` · `아무도 알려주지 않는` · `진짜 이유`
→ 시청자가 이미 안다고 생각하는 답을 **선제적으로 부정**해 클릭 이유를 만든다.

### P6. **여정을 화살표로 그려 자기 위치를 찾게 한다** 🆕

[`추격매수→물타기→손절못하기→원금대기의 끝`](https://www.youtube.com/watch?v=-27Dlgpfr60) **386,711회**
4단계를 제목에 나열하니 시청자가 **"나는 2단계에 있다"** 를 즉시 찾는다. P4의 가장 강한 구현이다.

---

## 🚨 소재는 필요조건이지 충분조건이 아니다 — 같은 소재 다채널 실측

**같은 소재를 여러 채널이 했을 때 성적이 극단으로 갈린다.**

| 소재 | 채널별 성적 | 최대 격차 |
|---|---|---|
| 국민성장펀드 vs 반도체 ETF | [경제해적단 **637,163**](https://www.youtube.com/watch?v=yysVN041wz8) · [손안의 경제학 5,251](https://www.youtube.com/watch?v=V8STbNx0uyk) · [경제나침반 343](https://www.youtube.com/watch?v=HhuqmZIj4Kw) · [경제잡스 67](https://www.youtube.com/watch?v=2cWddrudJmE) · [한국경제 46](https://www.youtube.com/watch?v=1kGERS2c2KY) | **13,851배** |
| 조용히 부자 된 5가지 원칙 | [경제해적단 **362,029**](https://www.youtube.com/watch?v=IinIFTY18jk) · [만화 경제학 1,703](https://www.youtube.com/watch?v=YMV9qxPlsRU) · [부자코드 47](https://www.youtube.com/watch?v=boeg2NRCNvw) · [차유진의 돈 공부 32](https://www.youtube.com/watch?v=T68oJIBoaGo) · [한발빠른경제학 3](https://www.youtube.com/watch?v=LcAH1g2aMbQ) | **120,676배** |
| 금융자산 10억 생기면 | [**똑재TV 730,748**](https://www.youtube.com/watch?v=w0tGUgRg9mM) · [경제해적단 633,252](https://www.youtube.com/watch?v=QdtKu0Zfw14) · [머니탐험대 25,684](https://www.youtube.com/watch?v=luNO-jAetV8) · [떠먹여주는TV 5,217](https://www.youtube.com/watch?v=8AzqHhKJccQ) · [라이프 빌드업 372](https://www.youtube.com/watch?v=ZG4bat-nwsk) | **1,964배** |
| 1억을 20억으로 | [경제해적단 344,763](https://www.youtube.com/watch?v=OzboXb0oVKY) · [만약에 머니 216,369](https://www.youtube.com/watch?v=hbBABRmu93Q) · [머니탐험대 31,706](https://www.youtube.com/watch?v=bHT9AsrEXEM) · [집구석 경제학 14,309](https://www.youtube.com/watch?v=yGY3vhtBEM8) · [경제만담 559](https://www.youtube.com/watch?v=3lEdXO6J1oY) · [경제탐사대 76](https://www.youtube.com/watch?v=5UgSLaee3pA) | **4,536배** |

> 🔴 **결론: 고배수 소재를 찾는 것은 출발선이지 결승선이 아니다. 같은 소재에서 만듦새가 수천 배를 가른다.**
> ⭕ 이건 우리에게 유리한 소식이다 — [08-10](https://www.youtube.com/watch?v=CKEBf-52HBo)이 같은 머스크 소재에서 구독 46,700 [속전속보](https://www.youtube.com/watch?v=9kVGwQihqlE)(3,141회) 포함 8곳을 전부 이긴 것과 같은 구조다.
> ⛔ **포화를 피하지 않는다. 밀도로 이긴다**([direction.md](../../direction.md) 1-2절).

---

# 2부 — 발굴 후보 채널

## 📐 배수 계산 방법 (2026-08-21 확정)

| | |
|---|---|
| **정호님 화면(vidIQ)의 배수** | 그 툴이 **업로드 당시** 채널력을 기록해 계산한 값. 우리가 접근할 수 없다 |
| **우리가 계산하는 배수** | `조회수 ÷ 분모` |
| 🔴 **분모 — 시점 보정 필수** | **그 영상 업로드 ±3주에 같은 채널이 올린 편들의 중앙값.** ⛔ 「현재 중앙값」으로 나누면 오차가 크다 |

### 실측 대조 — 현재 중앙값(8,981)으로 나눈 경우의 오차

| 영상 | 조회 | 현재 중앙값 기준 | vidIQ 화면 | 일치 |
|---|---|---|---|---|
| [국민성장펀드 vs 반도체 ETF](https://www.youtube.com/watch?v=yysVN041wz8) | 637,163 | 70.9배 | 68.7x | ✅ |
| [-30% 물린 종목](https://www.youtube.com/watch?v=dVSpaWB1IZs) | 307,957 | 34.3배 | 28.5x | ✅ |
| [금융자산 10억 생기면](https://www.youtube.com/watch?v=QdtKu0Zfw14) | 633,252 | 70.5배 | 92.8x | 근접 |
| [주식으로 돈 잃는 4가지 패턴](https://www.youtube.com/watch?v=-27Dlgpfr60) | 386,711 | 43.1배 | >100x | 과소 |
| [1억을 20억으로](https://www.youtube.com/watch?v=OzboXb0oVKY) | 344,763 | 38.4배 | 78.7x | 과소 |
| [조용히 부자 된 5가지 원칙](https://www.youtube.com/watch?v=IinIFTY18jk) | 362,029 | 40.3배 | **4.7x** | ❌ 크게 어긋남 |

> **결론: 현재 중앙값 분모는 못 쓴다. 반드시 시점 보정한다.**
> ⚠️ **유튜브 인기순 정렬은 yt-dlp가 무시한다**(`?sort=p` 무효). **채널 전편을 받아 조회수로 직접 정렬**한다.

---

## ⭐ 1순위 후보 — 나레이션 롱폼 · 재테크 에버그린 · 미스캔

| 채널 | 발견 근거 영상 | 조회 | 길이 | 우선순위 사유 |
|---|---|---|---|---|
| **똑재TV** | [금융자산 10억 도달하면 반드시 겪게 됩니다. 아무도 미리 알려주지 않는](https://www.youtube.com/watch?v=w0tGUgRg9mM) | **730,748** | — | **같은 소재에서 경제해적단을 이겼다.** 최우선 |
| **어니스트와 투자 빌드업** | [고수의 물린 주식 관리방법 (손절, 물타기, 존버보다 유리한 이유)](https://www.youtube.com/watch?v=DXJTMR388eU) | **277,765** | — | P4 명명형 |
| **머니버디** | [물렸을 때 손절하면 안되는 이유](https://www.youtube.com/watch?v=uTP6pWq3r8A) | **185,280** | — | P4 명명형 |
| **차윤호 스플릿** | [주식투자에서 개미투자자 99%가 결국 손실나는 이유 7가지](https://www.youtube.com/watch?v=HoHCkeTfqSQ) 105,174 · [주식으로 돈 벌어도 결국 전재산을 잃는 이유](https://www.youtube.com/watch?v=RXft-lAkSqU) **161,702** | 16.7만 | 20분 | 히트 2편·나레이션 롱폼 |
| **쩐문가** | [10억이 생기면 그때서야 겪게되는 일들](https://www.youtube.com/watch?v=MxZ4SgJ1EZ4) | **144,151** | 16분 | P4 명명형 |
| **부자아빠의 경제학** | [금융자산 10억이 생기면 당신에게 일어나는 변화들](https://www.youtube.com/watch?v=iUV_Dr-2ecI) | 84,377 | 31분 | 체급 근접 가능성 |
| **위즈덤투스** | [물타기 vs 손절 "무작정 물타다 계좌 완전히 망가집니다"](https://www.youtube.com/watch?v=mVpZc_HKBvU) | 19,898 | 18분 | **08-18 활동 중** |
| **경제학 똑똑** | [주식으로 돈 벌고도 결국 망하는 사람들의 공통점](https://www.youtube.com/watch?v=z_UO_bcY498) | 19,086 | 19분 | 체급 근접 |
| **자본의 기록** | ["1억·3억과는 다르다, 5억부터 펼쳐지는 세계"](https://www.youtube.com/watch?v=DIWHUuKJSiQ) | 15,706 | — | P1+P4 |
| **집구석 경제학** | [첫 1억이 10억이 되는 진짜 이유? 10억을 20억으로](https://www.youtube.com/watch?v=yGY3vhtBEM8) | 14,309 | 28분 | 체급 근접 |
| **떠먹여주는TV** | [금융자산 10억을 모으면 생기는 변화](https://www.youtube.com/watch?v=8AzqHhKJccQ) | 5,217 | 35분 | **08-17 활동 중** |

> ⚠️ **스캔 시 판정 순서를 지킨다** — ⓪복제 네트워크 → ①시청자 연령대 → ②세분축 → ③체급·포맷·건전성 → ④배수([channels.md](channels.md)).
> ⚠️ **구독 3,000~25,000 채널을 우선**한다. 체급이 크게 벌어지면 소재 계승 근거가 약해진다.
> ⚠️ 위 조회수는 **검색으로 발견한 1편**일 뿐이다. **채널 중앙값·구독·건전성은 아직 안 쟀다.**

---

## 🔁 재확인 대상 — 기존 3군인데 이 결에서 큰 성과가 있다

| 채널 | 근거 영상 | 조회 | 기존 판정 | 재확인 사유 |
|---|---|---|---|---|
| [만약에 머니](https://www.youtube.com/channel/UCSqFJxc0zYKLTr2IwFth2pA) | [50대 노후준비 1억을 20억으로 만드는 3가지 전략](https://www.youtube.com/watch?v=hbBABRmu93Q) | **216,369** | ⛔ 실무 정보축 · 06-15 중단 | 21만 편이 있다. 중단이면 소재만 참고, 재개면 재판정 |
| [똑똑하게 돈 벌기](https://www.youtube.com/channel/UCEDbet_4cQqo5_8Yw2ermKg) | [개인투자자가 매수하는데 주가는 왜 안 오를까(세력)](https://www.youtube.com/watch?v=4B0Hxwwv2WQ) **552,602** · [주식투자를 실패했다면 이 이유](https://www.youtube.com/watch?v=sZfKCXTBAHI) 277,588 | ⛔ 100배 급락 = **제재 정황** | 제재 전 소재는 유효할 수 있다. **소재만 참고, 채널 계승 금지** |

---

## ⛔ 복제 네트워크 — 판정 0순위 탈락 (회피 명단)

| 채널 | 복제 증거 | 원본 |
|---|---|---|
| **머니탐험대** | [금융자산 10억 생기면… 6가지](https://www.youtube.com/watch?v=luNO-jAetV8) 25,684 · [1억을 20억으로 만드는 4가지 전략](https://www.youtube.com/watch?v=bHT9AsrEXEM) 31,706 | 경제해적단 **동일 제목·동일 길이**(1,221초 / 979초) |
| **은빛사연** · **인생의 경고장** | [4,716회](https://www.youtube.com/watch?v=r4GY_dvIP1E) · [**0회**](https://www.youtube.com/watch?v=ivdSTp-cCi4) — 둘 다 **2,792초** | [은빛시나리오 11,065회](https://www.youtube.com/watch?v=HLesWEWxzNo) |
| [만화 경제학](https://www.youtube.com/channel/UCOrRuK7IJq1a7scuEPYIm3w) | [조용히 부자 된 5가지 원칙](https://www.youtube.com/watch?v=YMV9qxPlsRU) 1,703 · [50대 주식투자 실패 3가지](https://www.youtube.com/watch?v=ry3xKOCcfCo) 2,891 | 경제해적단 / 만약에 머니 |
| **부자코드** · **경제만담** · **경제탐사대** · **한발빠른경제학** · **차유진의 돈 공부** · **라이프 빌드업** · **경제수비수** · **이성진 주식투자의 정석** | [47](https://www.youtube.com/watch?v=boeg2NRCNvw) · [559](https://www.youtube.com/watch?v=3lEdXO6J1oY) · [76](https://www.youtube.com/watch?v=5UgSLaee3pA) · [3](https://www.youtube.com/watch?v=LcAH1g2aMbQ) · [32](https://www.youtube.com/watch?v=T68oJIBoaGo) · [372](https://www.youtube.com/watch?v=ZG4bat-nwsk) · [15](https://www.youtube.com/watch?v=0BGLDqh9GBw) · [559](https://www.youtube.com/watch?v=hGKQZr5TIn0) | 전부 경제해적단 계열 복제 |

> 🔴 **이 명단은 「소재의 힘」에 대한 증거이기도 하다** — 머니탐험대는 복제본만으로 25,684·31,706회를 냈다.
> ⛔ 그러나 **복제는 하지 않는다.** 가져오는 건 **소재와 골격**이고 문장·구성은 새로 만든다([[feedback_reference_originality]]).
> ⚠️ 동시에 **복제본 대부분이 0~559회다.** 소재만 베끼면 죽는다는 증거이기도 하다(위 「필요조건」 절).

---

## ❌ 포맷 불일치 — 소재 수요 확인용으로만

| 채널 | 근거 영상 | 조회 | 제외 사유 |
|---|---|---|---|
| **상승효과TV** | [주식투자로 반드시 부자 되는 10가지 비밀](https://www.youtube.com/watch?v=tcU5XihZAUk) | 826,305 | 13분·2021년 |
| **슈퍼개미 이주영TV** | [개미가 망하는 이유 10가지](https://www.youtube.com/watch?v=kolTNy0njsE) | 235,846 | 8분·2022년 |
| **주식단테_20년차트고수** | [물린 계좌를 효과적으로 탈출하자](https://www.youtube.com/watch?v=xpqU-ZEvCY0) | 160,150 | **2.5분** 차트 강의 |
| **TQQQ미친놈** | [금융자산 10억이 가지는 의미](https://www.youtube.com/watch?v=1ToegNDTKw8) | 144,988 | **6분** |
| **장영한 주식TV** | [개미투자자의 95%가 돈을 잃는 이유](https://www.youtube.com/watch?v=qnIU15-Wp4Y) | 127,919 | **인터뷰** |
| **개천에서 용재난다** · **시윤주식** · **김작가 TV** · **MKTV 김미경TV** | [109,837](https://www.youtube.com/watch?v=azKjaueHi1A) · [89,110](https://www.youtube.com/watch?v=IsT_1WBFRGM) · [86,362](https://www.youtube.com/watch?v=WohBzLRrZi8) · [43,187](https://www.youtube.com/watch?v=X5mBzsmUn9Q) | — | 상담·인터뷰·게스트 클립 |

---

# 3부 — 확보된 고배수 소재 (정호님 vidIQ 화면 · 2026-08-21)

| 소재 | 조회 | **배수** | 길이 | 경과 | 해당 패턴 |
|---|---|---|---|---|---|
| [주식으로 돈 잃는 4가지 패턴 \| 추격매수→물타기→손절못하기→원금대기](https://www.youtube.com/watch?v=-27Dlgpfr60) | 38만 | **>100x** | 16:55 | 3개월 | P4·**P6** |
| [금융자산 10억 생기면 실제로 벌어지는 일 6가지](https://www.youtube.com/watch?v=QdtKu0Zfw14) | 63만 | **92.8x** | 20:22 | 2개월 | P1·P4 |
| [1억을 20억으로 만드는 4가지 전략 \| 99%가 모르는 부자의 비밀](https://www.youtube.com/watch?v=OzboXb0oVKY) | 34만 | **78.7x** | 16:20 | 4개월 | P1·P5 |
| [국민성장펀드 vs 반도체 ETF \| 같은 3000만원, 5년 뒤](https://www.youtube.com/watch?v=yysVN041wz8) | 63만 | **68.7x** | 16:08 | 3개월 | P1·**P2** |
| [-30% 물린 종목, 팔아야 할까 버텨야 할까 \| 손절 기준 3가지](https://www.youtube.com/watch?v=dVSpaWB1IZs) | 30만 | **28.5x** | 13:34 | 2개월 | P1·**P4** |
| ["주식으로 조용히 부자 된 사람들" 10년간 딱 지킨 5가지 원칙](https://www.youtube.com/watch?v=IinIFTY18jk) | 36만 | 4.7x | 22:36 | 1개월 | P5 |

> ⭕ **길이 13~22분으로 우리 대역(16~20분)과 겹친다.** 포맷 이식 부담이 없다.
> ⭕ **1~4개월 지난 지금도 VPH 12~135로 돈다** — 에버그린이라 롱테일이 산다(P3).

---

## 📋 다음 작업 (미착수)

1. 1순위 후보 **11곳 전편 스캔** → 구독·중앙값·건전성 판정 → 조회수 정렬 → **시점 보정 배수** 계산
2. 배수 상위 소재를 3부에 누적하고 **패턴 P1~P6을 재검증**(표본이 경제해적단 1곳뿐인 게 현재 한계다)
3. 판정 통과 채널은 [channels.md](channels.md)로 승격 이관
4. 확정 소재를 [production-queue.md](../../production-queue.md)에 편성
