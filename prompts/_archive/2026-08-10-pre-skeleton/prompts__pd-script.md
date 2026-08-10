# 대본 제작 — 상세 절차

`{P}` = `channels/{채널}/projects/{프로젝트}`
`{S}` = `{P}/_script` (대본 단계 산출물 디렉토리)
`{VENV_PYTHON}` = macOS/Linux: `.venv/bin/python` | Windows: `.venv\Scripts\python`

> ⚠️ 파이썬은 항상 `{VENV_PYTHON}`으로 부른다. `python`·`python3`을 그대로 쓰지 않는다 (Windows에 `python3`이 없다).

---

## COLLECT

**YouTube 레퍼런스 수집.**

1. YouTube URL 확보
   - **사용자 메시지에 이미 영상 URL(`watch?v=`, `youtu.be/`, `/shorts/`)이나 재생목록 URL이 있으면 그것이 레퍼런스다. 다시 묻지 말고 바로 수집한다.**
   - channel-trend-pd에서 앵커 레퍼 URL을 인계받았으면 그것을 쓴다. 역시 다시 묻지 않는다.
   - URL이 전혀 없을 때만 사용자에게 요청한다.
2. 실행:
```bash
{VENV_PYTHON} scripts/collect.py --project {프로젝트} --channel "{채널}" URL1 URL2 ...
```
3. 결과: `_refs/{NNN}/` 에 meta.md, transcript.txt, thumbnail.webp

### collect.py 실패 시 — 수동 수집 폴백

collect.py가 실패하면 (429 에러, 네트워크 문제 등) 사용자에게 대본을 직접 붙여넣도록 안내한다.

**흐름 — 한 번에 하나씩, 제목과 대본을 분리해서 받는다:**

```
1. 안내: "YouTube에서 직접 가져오지 못했습니다. 대본을 직접 붙여넣어 주세요."
2. 요청: "첫 번째 레퍼런스 영상의 제목을 알려주세요."
3. 사용자가 제목 입력
4. 요청: "이제 그 영상의 대본을 붙여넣어 주세요."
5. 사용자가 대본 붙여넣기
6. _refs/001/ 생성 (transcript.txt + meta.md)
7. 질문: "두 번째 레퍼런스 영상도 있나요?"
8. 있으면 → "제목을 알려주세요." → "대본을 붙여넣어 주세요." → _refs/002/ 생성
9. 반복 (최대 4~5개)
10. 없으면 → ANALYZE 진행
```

**파일 생성 규칙:**
- `_refs/{NNN}/transcript.txt` — 사용자가 붙여넣은 대본 텍스트 그대로 저장
- `_refs/{NNN}/meta.md` — 최소 정보로 생성:
  ```markdown
  # {영상 제목}

  ## 기본 정보
  - **URL**: {있으면 URL, 없으면 "(직접 입력)"}
  - **수집 방식**: 수동 입력
  ```
- `thumbnail.webp` — 없음 (수동 수집이므로 썸네일 없이 진행)

---

## ANALYZE

**레퍼런스 영상 분석. 에이전트: video-analyst**

1. `_refs/*/analysis.md`가 없는 영상 목록 확인
2. **전체 동시 병렬 실행** (run_in_background: true, **TaskOutput 사용 금지** → Glob으로 확인)
3. 각 에이전트에게 전달:
   - 채널 프로필 (`channels/{채널}/config/profile.md`)
   - 분석 프롬프트 (`prompts/reference-analyze.md`)
   - 영상 데이터 (meta.md + transcript.txt + thumbnail.webp)
4. 출력: 각 `_refs/{NNN}/analysis.md`
5. 완료 후 요약 보고

---

## DATA_PREP

**패턴 추출 + 데이터 검증/리서치. 2 에이전트 완전 병렬.**

### pattern-extractor 에이전트

1. 최소 2개 analysis.md 필요 (부족하면 알림)
2. 에이전트 1개 호출 (run_in_background: true)
3. 전달: 채널 프로필 + `prompts/reference-patterns.md` + 모든 analysis.md + meta.md
4. 출력: `{P}/_script/patterns.md`

### data-researcher 에이전트

1. 에이전트 1개 호출 (run_in_background: true, WebSearch 사용)
2. 전달: 채널 프로필 + `prompts/data-research.md` + 모든 transcript.txt + 모든 **meta.md** + **아래 「앵글 축 후보」**
3. 출력: `{P}/_script/factcheck.md` + `{P}/_script/verified-data.md` (추가 리서치 포함)

> 🚨 **`analysis.md`는 전달하지 않는다.** 리서치에 필요한 "레퍼가 무슨 내용을 다뤘나"는 원본인 `transcript.txt`에 전부 있다. `analysis.md`는 그걸 해석한 2차 자료(2편 합 약 2.8만 자)라서, 원본과 함께 주면 같은 내용을 두 번 읽는다. 구조·썸네일 분석은 리서치 방향과 무관하고, 그건 pattern-extractor가 쓴다.

#### 🚨 앵글 축 후보를 함께 준다 — 2차 리서치를 막는 유일한 방법

**DATA_PREP은 STRATEGY보다 먼저 온다. 즉 리서치 시점에는 앵글이 아직 없다.** 그래서 아무 대비 없이 조사하면, 나중에 확정된 앵글이 새 축을 요구할 때 **리서치를 한 번 더 돌리게 된다.**

> **실측(2026-08-08, china-broke-reality)**: 1차 리서치는 경제 축(부동산·수출·한국 피해)만 팠는데, 확정 앵글이 군사·해상 봉쇄 축을 요구해 2차를 추가로 돌렸다. **108,342토큰**이 더 들었다.

그래서 호출 전에 PD가 **앵글 축 후보 2~4개를 뽑아 리서치 범위에 넣는다.**

- **뽑는 곳**: `_refs/*/analysis.md`의 「우리 영상에서 반드시 다뤄야 할 포인트」·「댓글 반응」 + 레퍼 제목/썸네일이 판 축. 새로 검색하지 않는다
- **형식**: "이 주제에서 우리가 잡을 수 있는 축은 ①경제(부동산·수출) ②군사·안보 ③기술·산업 ④한국 체감이다. **네 축 모두 조사 항목에 포함하라**"
- ⛔ **범위를 넓히되 항목당 검증 강도는 낮추지 않는다.** 축이 늘었다고 "각 축 대충 훑기"로 가면 2차를 안 돌리는 대신 대본이 부실해진다. 1차 출처 확인, 수치 교차검증, ❌/❓ 판정은 축이 몇 개든 그대로 한다
- 축이 4개를 넘어가면 **주제와 가장 먼 것부터 자른다.** 무한정 넓히는 게 목적이 아니라 "확정 앵글이 요구할 법한 축"을 미리 덮는 게 목적이다

### 완료 확인

- `_script/patterns.md` 존재 확인
- `_script/verified-data.md`에 "## 추가 리서치" 존재 확인

---

## STRATEGY

**크리에이티브 전략 설계 + 썸네일 프롬프트. strategist 에이전트를 2회로 나눠 호출한다.**

입력: `_script/patterns.md` + `_script/verified-data.md` + 채널 프로필

> 🚨 **한 번에 몰아 부르지 않는다. 모드(auto/ask)와 무관하게 항상 2회로 쪼갠다.**
> - **#1 패키지 설계** (Phase 1~4.5) — 앵글·제목·카피·Hook. **썸네일 계열 규칙 파일 3종을 읽지 않는다.**
> - **#2 썸네일 프롬프트** (Phase 5) — 계열별 9장. **`creative-strategy.md`는 Phase 5 절만 읽는다.**
>
> 합쳐 부르면 #1이 쓰지도 않을 계열 규칙 3종(약 4.4만 자)을 읽고, #2가 이미 끝난 설계 절차(약 2.1만 자)를 다시 읽는다.
> 계열을 무엇으로 할지 판정하는 표는 `creative-strategy.md` Phase 5 안에 있으므로 #1도 판정만은 할 수 있다.

### 사전 준비

```bash
{VENV_PYTHON} -c "import os; os.makedirs('{P}/output/thumbnails', exist_ok=True)"
```

### strategist #1 — 패키지 설계

> 🚨 **프롬프트 파일은 "내용"이 아니라 "경로"로 전달한다.** strategist는 Read 툴이 있어 스스로 읽는다.
> PD가 대신 읽어서 프롬프트에 붙여넣으면 같은 텍스트가 PD와 에이전트 양쪽에 이중으로 쌓인다.
> 대신 호출 프롬프트 **첫 지시로 "아래 파일들을 작업 시작 전에 모두 Read하라"를 명시**한다. 안 읽으면 규칙이 통째로 빠진다.

1. strategist 에이전트 호출:
   - **경로로 전달** (내용 임베드 금지):
     - `prompts/creative-strategy.md` — 5.5-Phase 설계 절차
     - `prompts/ctr-reference.md` — CTR 이론
     - `prompts/pd-templates.md` — 후보 표 형식
     - `channels/{채널}/config/profile.md`
     - `channels/{채널}/config/settings.json` (hook_strategy)
     - `channels/{채널}/config/pd-guide.md` (있으면)
     - `channels/{채널}/config/thumbnail-strategy.json` (있으면)
     - `{P}/_script/patterns.md` + `{P}/_script/verified-data.md`
     - `{P}/_refs/` (analysis.md, meta.md, thumbnail.webp — 앵커 선정·계승용)
   - ⛔ **`thumbnail-design.md` · `thumbnail-countryball.md` · `thumbnail-geopolitics.md`를 전달하지 않는다.** 이 셋은 #2 전용이다. #1이 낼 것은 **이미지 컨셉 2줄과 계열 판정**뿐이고, 그 근거는 `creative-strategy.md` Phase 5의 계열 판정 표에 있다
   - 함께 전달: 모드(auto/ask) + 출력 파일 경로 + 목표 러닝타임
   - auto 출력: `concept.md` + `hook-intro.md`
   - ask 출력: `_strategy_candidates.md` (전문) + **`_strategy_summary.md` (비교표만, 2,000자 이내)**

### strategist #2 — 썸네일 프롬프트 (Phase 5)

패키지가 확정되고 `concept.md`가 저장된 뒤에 부른다.

1. **먼저 PD가 Phase 5의 시작 줄 번호를 잡는다** (파일이 수정돼도 안 깨지게 매번 새로 잡는다):
```bash
grep -n '^## Phase 5' prompts/creative-strategy.md
```
2. strategist 에이전트 호출 — **경로로 전달**:
   - `prompts/creative-strategy.md` — **위에서 얻은 줄 번호를 offset으로 주고 "그 줄부터 끝까지만 Read하라"고 지시한다.** 전문을 읽히지 않는다
   - `prompts/thumbnail-design.md` — 실사형 (항상)
   - `prompts/thumbnail-countryball.md` — 국기볼형 (항상)
   - `prompts/thumbnail-geopolitics.md` — 정세형 (**국가·안보 소재일 때만.** 아니면 전달하지 않는다)
   - `channels/{채널}/config/thumbnail-strategy.json` + `profile.md`
   - `{P}/_script/concept.md` (확정 컨셉·계승 정보) + `{P}/_script/verified-data.md`
   - `{P}/_refs/{앵커}/thumbnail.webp` + `analysis.md` — 계승 3장 근거
   - ⛔ `patterns.md` · `_strategy_candidates.md` · `ctr-reference.md`를 전달하지 않는다. Phase 5는 확정된 `concept.md`만 있으면 된다
3. 출력: `prompts.json` + `prompts-countryball.json` (+ 해당 시 `prompts-geopolitics.json`)

### auto 모드

1. #1이 낸 concept.md + hook-intro.md 존재 확인 → 곧바로 **strategist #2** 호출 → prompts.json + prompts-countryball.json (+ 국가·안보 소재면 prompts-geopolitics.json) 존재 확인
2. 결과 요약 보고 — 확정 패키지(A~D 중 어느 것인지) + 확정 제목
3. **복사용 통합본 .txt 생성** (아래 "복사용 통합본(.txt) 생성" 참조) — 필수
4. **썸네일 목록 표 + txt 링크 출력** (아래 "썸네일 프롬프트 채팅 출력 — 목록 표만" 참조. 영문 프롬프트 원문은 출력하지 않는다)
5. OUTLINE 진행

### ask 모드

1. **`_strategy_summary.md`만 읽는다** (2,000자). `_strategy_candidates.md` 전문(1.6~2.4만 자)은 읽지 않는다 — 채팅에 낼 건 비교표뿐이고, 그건 요약본에 다 있다
2. **4개 패키지를 "한눈에 비교" 표로 제시** (A·B·C·D). 채팅에 전문을 늘어놓지 않는다 — 표 + 상세는 파일 링크
   - 🚨 **사용자에게 묻는 것은 패키지 하나뿐이다.** 패키지가 정해지면 **제목과 썸네일 카피는 묻지 않고 바로 다음 단계로 간다.**
   - 제목 3안 / 썸네일 카피 3안은 **채팅으로 고르게 하지 않고 산출물에 전부 수록**한다 — `concept.md`와 `output/youtube.md` 양쪽에 표로 넣고, 1순위를 잠정 확정으로 삼아 대본을 진행한다. 사용자는 완료 후 산출물에서 직접 고른다
   - 형식은 `prompts/pd-templates.md`의 **「★ 후보 표 형식 — 산출물에 이 형태로 수록」** 그대로. 1줄·2줄·리액션을 각각 다른 칸에 넣고 글자수를 매 칸에 표기한다
3. 사용자 선택/수정/혼합 (패키지 단위로만):
   - "B로 해줘" → B 그대로 채택
   - "A 앵글에 B 제목으로" → 혼합
   - "A 좋은데 Hook 좀 바꿔줘" → 수정
   - 사용자가 **먼저** 특정 제목·카피를 지목하면 그것을 1순위로 올린다. 지목이 없으면 묻지 말고 strategist 1순위로 진행
4. 확정 → `_script/concept.md` + `_script/hook-intro.md` 저장
   - **선택된 패키지 1개의 절만** `_strategy_candidates.md`에서 부분 Read한다 (`grep -n '^## 패키지'`로 줄 번호를 잡고 그 구간만 offset/limit로 읽는다). 4개 패키지 전문을 통째로 읽지 않는다 — 나머지 3개는 버려질 안이다

   **⛔ 새 설계가 필요한 경우 strategist를 새로 띄우지 않는다 — `SendMessage`로 #1을 이어 쓴다.**

   | 사용자 응답 | 처리 |
   |---|---|
   | "B로 해줘" (그대로 채택) | **PD가 직접** 부분 Read → `concept.md` 작성. 에이전트 호출 없음 |
   | "A인데 제목은 ②번으로" (후보 안에서 교체) | **PD가 직접** — 후보가 이미 candidates에 있다 |
   | **"A 앵글에 B 제목 골격으로"** / "A인데 Hook 다시" / **레퍼 계승 골격을 새로 짜야 함** | **`SendMessage`로 strategist #1에게** — "X안 확정. {요구사항}으로 `concept.md`·`hook-intro.md` 본문을 작성해 반환하라" |

   > 🚨 **혼합·수정을 새 Task로 띄우면 #1이 이미 읽은 파일을 통째로 다시 읽는다.** `creative-strategy.md`·`ctr-reference.md`·`pd-templates.md`·`patterns.md`·`verified-data.md`·`_refs`가 전부 재Read된다.
   > `SendMessage`는 그 에이전트의 컨텍스트를 그대로 이어받으므로 **재Read가 0**이다. 설계 밀도는 그대로고 비용만 빠진다.
   > **실측(2026-08-08, china-broke-reality)**: 혼합안(A 앵글 + 레퍼 제목 골격)을 새 Task로 띄워 **183,441토큰**을 썼다. SendMessage였으면 약 3만이었다.
   > PD가 조립하지 않는 이유: 계승 골격을 새로 짜려면 어휘 대조표·[모순]/[남김]/[바꿈] 판정·텐션 트라이앵글을 다시 설계해야 하고, 그건 부분 Read로 조립되지 않는다. **품질을 지키면서 비용만 없애는 길이 SendMessage다.**
5. **strategist #2 호출** (위 「strategist #2 — 썸네일 프롬프트」 절차 그대로) — 계열마다 파일 분리:
   - `{P}/output/thumbnails/prompts.json` — 실사형 9개 (항상)
   - `{P}/output/thumbnails/prompts-countryball.json` — 국기볼형 9개 (항상)
   - `{P}/output/thumbnails/prompts-geopolitics.json` — 정세형 9개 (국가·안보 소재일 때만)
6. **복사용 통합본 .txt 생성** (아래 참조) — 필수
7. **썸네일 목록 표 + txt 링크 출력** (아래 참조. 영문 프롬프트 원문은 출력하지 않는다)
8. OUTLINE 진행

### 복사용 통합본(.txt) 생성 — 필수

> 🚨 **JSON을 만들었으면 반드시 같은 폴더에 계열별 `.txt`를 같이 만든다.** 사용자가 실제로 복사해 쓰는 건 이 txt다.
> JSON은 `generate_thumbnails.py`와 파이프라인 문서가 참조하는 구조 파일이라 **표시용 필드를 끼워 넣지 않는다.** JSON 문자열은 줄바꿈이 `\n`으로 이스케이프되므로 그 안에 통합본을 넣으면 복사 시 이스케이프가 그대로 딸려가 프롬프트가 뭉개진다.

생성한 JSON마다 1개씩, 같은 이름의 `.txt`를 만든다.

```bash
{VENV_PYTHON} -c "
import json, sys, os
d = os.path.join('{P}', 'output', 'thumbnails')
for src in ['prompts', 'prompts-countryball', 'prompts-geopolitics']:
    p = os.path.join(d, src + '.json')
    if not os.path.exists(p): continue
    data = json.load(open(p, encoding='utf-8'))
    body = '\n\n'.join(t['prompt_en'] for t in data['thumbnails'])
    open(os.path.join(d, src + '.txt'), 'w', encoding='utf-8').write(body + '\n')
    print(src + '.txt 생성')
"
```

**txt 내용 규칙** (사용자가 실제로 복사하는 파일이다):
- **영어 프롬프트 원문만** 넣는다. 번호·제목·한국어 설명·구분선을 넣지 않는다
- 프롬프트 사이는 **빈 줄 하나**로만 구분한다
- 계열을 한 파일에 섞지 않는다 — 계열마다 따로 돌리기 때문이다
- 완료 보고 시 **txt 경로도 클릭 가능한 링크로 함께 안내**한다

### 썸네일 프롬프트 채팅 출력 — 목록 표만

> 🚨 **영어 프롬프트 원문을 채팅에 출력하지 않는다.** 원문은 이미 계열별 `.txt`에 들어 있고, 사용자는 그 파일을 열어 통째로 복사한다.
> 채팅에 27개(3계열 × 9장)를 다시 쓰면 **약 5만 자를 그대로 중복 출력**하게 된다. 코드 블록도 만들지 않는다.

계열을 **완전히 분리해서**, 계열마다 **① 목록 표 + ② 복사용 txt 링크 한 줄**만 낸다.

출력 계열: **실사형 → 국기볼형 → 정세형**(국가·안보 소재일 때만) 순서. 정세형을 생성하지 않았으면 그 사실과 이유를 한 줄 적는다.

### 표 행은 python으로 뽑는다 — json을 Read하지 않는다

> 🚨 **썸네일 json을 Read 툴로 열지 않는다.** 표에 필요한 건 `composition`(6자) + `concept_ko`(151자)뿐인데 `prompt_en`이 파일의 **78%**(장당 약 1,600자)다. 표 하나 만들자고 3계열 6만 자를 읽고 버리게 된다.

```bash
{VENV_PYTHON} -c "
import json, os, sys
d = os.path.join(sys.argv[1], 'output', 'thumbnails')
for src in ['prompts', 'prompts-countryball', 'prompts-geopolitics']:
    p = os.path.join(d, src + '.json')
    if not os.path.exists(p): continue
    print('###', src)
    for t in json.load(open(p, encoding='utf-8'))['thumbnails']:
        print('|', t['id'], '|', t.get('purpose',''), '|', t.get('composition',''), '|', t.get('concept_ko','').replace('\n',' '), '|')
" {P}
```

출력된 행을 그대로 표에 옮긴다. 출력 형식은 정확히 이렇게 한다.

```
## 실사형 9개 — [복사용 txt](…/output/thumbnails/prompts.txt)

| # | 목적 | 구도 | 내용 |
|---|------|------|------|
| 1 | 내용 대표 | {composition} | {concept_ko} |
| … | … | … | … |
| 9 | {감정 클로즈업} | {composition} | {concept_ko} |

## 국기볼형 9개 — [복사용 txt](…/output/thumbnails/prompts-countryball.txt)

(동일 구조 — 목록 표 + 링크)

## 정세형 9개 — [복사용 txt](…/output/thumbnails/prompts-geopolitics.txt)

(동일 구조. 국가·안보 소재가 아니면 이 절을 생략하고 사유를 한 줄 적는다)
```

**표 규칙:**
- 1번부터 9번까지 **한 줄씩 9행**으로 낸다. "1~3", "4~6" 같은 묶음 표기는 쓰지 않는다
- `내용` 칸은 `concept_ko`를 **한 줄로** 적는다. 영어 프롬프트를 여기에 넣지 않는다
- 헤더의 txt 링크는 **워크스페이스 상대경로**로 걸어 클릭하면 파일이 열리게 한다

> ⛔ **이미지 자동 생성은 하지 않는다.** `generate_thumbnails.py`를 파이프라인에서 호출하지 않는다.
> 사용자가 명시적으로 요청할 때만 실행하며, 그때 `google-genai`·`Pillow` 설치가 필요하다.

---

## OUTLINE

**통합 기획서 작성. 에이전트: outline-writer 1개.**

> 🚨 **PD가 직접 쓰지 않는다.** outline을 쓰려면 `patterns.md`(최대 4만 자) + `verified-data.md`(최대 2만 자) + `concept.md`를 전부 읽어야 하는데, PD가 읽으면 그 6만 자가 메인 컨텍스트에 남아 이후 모든 단계에서 계속 재전송된다. 에이전트 안에서 읽고 버린다.
> **작성 규칙·포맷 파일도 PD가 읽지 않는다.** `outline-guide.md`, `pd-templates.md`는 outline-writer가 직접 Read한다.

### 에이전트 호출

1. outline-writer 에이전트 호출 (run_in_background: true)
2. **경로로 전달** (내용 임베드 금지). 호출 프롬프트 첫 지시로 "아래 파일들을 작업 시작 전에 모두 Read하라"를 명시한다:
   - `prompts/outline-guide.md` — outline 작성 규칙 전체 (셀프체크 10항목 포함. **결과는 파일이 아니라 응답으로만 온다**)
   - `prompts/tone-guide.md` — 문체 기준. **파트별 수치 배정 상한(2~3개)과 살림 비유 착지 설계용**
   - `prompts/pd-templates.md` — `## outline.md 포맷` 절
   - `{P}/_script/concept.md` + `hook-intro.md` + `patterns.md` + `verified-data.md`
   - `channels/{채널}/config/profile.md` + `pd-guide.md` (있으면)
3. 함께 전달: **target_minutes**(사용자가 지정한 목표 분량) + 출력 경로 `{P}/_script/outline.md`
4. 완료 확인: `{P}/_script/outline.md` 존재 확인 (Glob). **파일 전문을 Read하지 않는다** — 아래 헤더 검증에 필요한 `### ` 줄만 확인한다

### 완료 후 헤더 검증 (PD 직접, 필수)

`grep '^### ' {P}/_script/outline.md`로 파트 헤더만 뽑아 **모든 줄의 괄호 안에 `~N분, ~N자`가 있는지** 확인한다. 클로징도 예외가 아니다.

- 하나라도 글자수 표기가 빠지면 `validate_draft.py`가 **exit 2를 내고 DRAFT에서 파이프라인이 멈춘다** → 빠진 줄만 Edit으로 채운다
- Hook/Intro는 `## 2. Hook & Intro` 아래에 있어야 하고 `### ` 파트 헤더가 아니다 (`### Hook (~10초)` 형태는 목표 대상에서 자동 제외됨)
- 상세 규칙 → `prompts/outline-guide.md`의 "⛔ 파트 헤더 형식"

### ask 모드

1. outline-writer 호출은 동일
2. 저장된 outline.md의 **`## 1. 기획 뼈대` + 파트 헤더 목록만** 사용자에게 제시 (전문 출력 금지 — 파일 링크로 대체)
3. 피드백이 있으면 해당 부분만 Edit으로 수정 → 확정

**확인 후: 사용자 확인 없이 바로 DRAFT 단계로 자동 진행한다** (auto 모드).

---

## DRAFT

**대본 초안 작성. 에이전트: script-writer (인접 파트 2개씩 묶어 1개, 병렬)**

입력: `_script/outline.md` + `_script/verified-data.md` + 채널 프로필 + **`prompts/tone-guide.md`** + `prompts/script-review-checklist.md`

### 파트 묶음 병렬 에이전트

1. outline.md `## 3. 본문 구조`에서 `### ` 파트 헤더 추출 → 파트 목록 확인
2. **Hook & Intro는 에이전트 범위에서 제외** — merge_draft.py가 자동 삽입
3. **인접 파트 2개씩 묶어 에이전트 1개에 배정한다.** 파트가 홀수면 마지막 에이전트가 1개를 맡는다:
   - 6파트 → 에이전트 3개 (1·2 / 3·4 / 5·6) · 5파트 → 3개 (1·2 / 3·4 / 5) · 7파트 → 4개
   - 각 에이전트는 담당 파트마다 **파일을 따로** 쓴다 → `_script/_draft_part{N}.md` (N = 파트 순서, 클로징 포함). 두 파트를 한 파일에 합치지 않는다 — `merge_draft.py`와 `validate_draft.py`가 파일 단위로 센다
   - **파트별 목표 글자수 범위를 각각 따로 명시한다.** 한 작가가 두 파트를 쓰면 분량이 한쪽으로 쏠리기 쉽다
4. 각 에이전트에게 전달:
   - outline.md의 **`## 1. 기획 뼈대` + 담당 파트 섹션(2개면 2개 다)**
   - **형제 파트 목록** — `## 3. 본문 구조`의 전 파트 헤더 + 각 파트 `핵심 내용` 첫 줄만 1줄씩 (아래 🚨 참조)
   - **Hook & Intro 원문** (`hook-intro.md`)
   - **verified-data.md는 「장면·일화」 계열 절만 발췌해 넣는다** (아래 🚨 참조)
   - 채널 프로필 + **tone-guide.md 전문** + script-review-checklist.md
   - 담당 파트명 + 출력 경로 + **파트별 목표 글자수 범위**(하한 90% ~ 상한 110%, 절대 상한 130%를 숫자로 명시)
   - **출력 형식 지시**: 파일은 반드시 `## {파트명}` **h2 헤더 한 줄로 시작**하고, 본문 안에는 `##`·`###` 소제목을 **하나도 넣지 않는다**

> 🚨 **형제 파트 목록과 Hook 원문을 반드시 넣는다.** 이걸 빼면 작가는 자기 파트만 보고 쓰게 되는데,
> 「장면·일화」는 전원이 같은 것을 받으므로 같은 장면을 두 작가가 각자 집는다. 실제로 그렇게 반복이 났다.
> 함께 넣을 지시 한 줄: **"내 파트 밖에 배정된 소재·문장·수치는 내가 쓰지 않는다. Hook에 이미 나온 사실을 다시 설명하지 않는다."**
> 추가되는 분량은 파트당 300~500자로, concept.md를 뺀 효과를 해치지 않는다.

> 🚨 **`verified-data.md` 전문을 넣지 않는다. 「장면·일화」 계열 절만 발췌한다.**
> 작가가 쓸 **수치는 이미 outline 파트 섹션의 「배정 수치 3개」 표에 대본 표기·살림 착지까지 적혀 있다.** 전문을 또 주면 같은 숫자를 두 번 주는 것이고,
> 파트 섹션에는 **⛔ 쓰지 않을 숫자 목록**까지 있어서 작가는 어차피 배정 밖 숫자를 못 쓴다 (2026-08-08 실측: 배정 밖 숫자 유입 0건).
> 반면 **장면·일화는 outline이 제목만 적어 두므로 원문이 필요하다** — "포항 화물차 기사 김성민 씨(55)"의 발언, 셔터에 붙은 임대 고지 같은 것들이다. 이게 빠지면 파트가 숫자만 남고 그림이 사라진다.
> 발췌 대상: `## 장면·일화`, `### 장면·일화 (대본의 그림 재료)`, `### 시청자 일상으로 닿는 지점` 등 **사람·현장 묘사가 들어 있는 절 전부.** 통계 나열 절은 넣지 않는다.
> 절 제목이 프로젝트마다 다르므로 `grep -n '^##' {S}/verified-data.md`로 목록을 먼저 뽑아 판단한다. **애매하면 넣는다** — 빠뜨려서 그림을 잃는 쪽이 더 나쁘다.

> 🚨 **`tone-guide.md`는 반드시 전문을 넣는다.** 경로만 알려주고 "읽어라"로 넘기지 않는다.
> 대조쌍이 규칙 문장보다 강하게 작동하는데, 안 읽으면 아무 효과가 없다.
> 다만 **약 8,100자**로 작지 않다. **파트 2개씩 묶는 이유가 여기에도 있다** — 6파트를 6명에게 주면 4.9만 자, 3명이면 2.4만 자다.
> 같은 이유로 `concept.md`는 절대 함께 넣지 않는다.

> 🚨 **`## ` 헤더는 계약이다.** `validate_draft.py`는 draft.md의 `^## ` 섹션 수가 outline 목표 수와 정확히 일치해야 통과시킨다.
> `merge_draft.py`는 헤더가 없어도 **조용히 exit 0**으로 끝나고, 모든 파트가 Hook 섹션 하나에 흡수된 뒤 validate에서 exit 2가 난다.
> 즉 **증상은 merge 다음에 나타나지만 원인은 작가 프롬프트에 있다.** exit 2가 나면 파트 파일의 첫 줄부터 확인한다.

5. 완료 확인: `ls {S}/_draft_part*.md`로 파일 수 == 파트 수
   - ⚠️ 재실행 전에 **`_draft_part*.md`를 먼저 지운다.** 이전 회차의 파트 파일이 남아 있으면 glob에 걸려 섹션 수가 초과되고 validate가 exit 2로 떨어진다

> 🚨 **`concept.md`는 전달하지 않는다.** 작가가 필요한 확정 제목·핵심 약속·타겟 시청자·톤은 `outline.md`의 `## 1. 기획 뼈대`(약 800자)에 전부 들어 있다.
> `concept.md`(약 1만 자)의 나머지는 제목 후보 3안·썸네일 카피 후보 3안·썸네일 이미지 컨셉·텐션 트라이앵글·정보갭 변형안·선택 근거인데, **작가가 하나도 쓰지 않는다.** 썸네일은 작가 일이 아니다.
> 에이전트 수만큼 곱해지므로 6파트·작가 3명이면 3만 자, 10파트·5명이면 5만 자다.

### draft.md 병합

```bash
{VENV_PYTHON} scripts/src/merge_draft.py \
  --hook-intro {S}/hook-intro.md \
  --parts-dir {S} \
  --output {S}/draft.md
```

### 분량 검증 게이트 (REVIEW 전 필수)

```bash
{VENV_PYTHON} scripts/src/validate_draft.py {S}/outline.md {S}/draft.md
```

기본값(파트 하한 90% / 파트 상한 130% / 본문 총합 상한 120%)을 쓴다. **임계값을 임의로 완화하지 않는다.**

세 가지를 본다:
1. **파트 하한** — 내용이 빠졌는지
2. **파트 상한** — 한 파트가 폭주했는지
3. **본문 총합 상한** — 파트가 골고루 부풀어 러닝타임을 넘겼는지 (파트별로는 다 통과해도 합치면 넘칠 수 있다)

- **exit 0** → REVIEW 진행
- **exit 2 (구조 오류)** → **재시도하지 말고 원인부터 고친다.** 목표 수 ≠ 섹션 수라는 뜻이다:
  - outline 파트 헤더에 글자수 표기가 빠졌는지 확인 → 채운다
  - draft에 outline에 없는 파트가 있는지 확인 → outline에 맞춘다
  - 고친 뒤 재실행. **이 오류를 무시하고 넘어가면 엉뚱한 파트끼리 비교된 허수로 통과한다**
- **exit 1, FAIL(부족)** → 보충 2-pass:
  1. FAIL 파트 번호(N) 확인
  2. outline.md에서 빠진 내용(비유/사례/데이터) 식별
  3. script-writer 재호출 → `_draft_part{N}.md` 덮어쓰기
  4. merge_draft.py 재실행 → draft.md 재생성
  5. validate_draft.py 재실행 (1회)
- **exit 1, FAIL(초과) 또는 FAIL(총합 초과)** → 압축 2-pass:
  1. 초과 파트만 골라 압축 에이전트 호출 (새로 쓰지 말고 **기존 문장을 합치거나 지우게** 한다)
  2. 삭제 우선순위 지시: 반복 설명 → 부연 비유 → 수사·강조 표현 순
  3. **사실·숫자·고유명사·파트 전환 문구는 전량 유지** 지시
  4. 총합만 초과한 경우 → 비율이 높은 파트부터 균등하게 덜어낸다
  5. merge_draft.py → validate_draft.py 재실행 (1회)

> ⛔ **사후 패딩·사후 삭제로 숫자만 맞추지 않는다.** 분량을 채우려고 의미 없는 문장을 덧대거나, 줄이려고 검증된 수치를 빼는 것은 금지다.

> 작가 에이전트 프롬프트에 목표 글자수를 **범위로** 준다. "1,050자 이상"이 아니라 "**1,050~1,280자 (하한 90%, 상한 110%, 절대 상한 130%)**". 하한만 주면 초과분이 그대로 쌓인다.

### 문체 검증 게이트 (REVIEW 전 필수)

분량 게이트를 통과한 뒤 곧바로 돌린다.

```bash
{VENV_PYTHON} scripts/src/check_tone.py {S}/draft.md
```

- **exit 0** → REVIEW 진행 (하한 미달 WARN은 차단하지 않는다. 다만 REVIEW에 그대로 넘긴다)
- **exit 1** → 문체 2-pass (**최대 2회**):
  1. 출력에서 FAIL 항목과 지적된 문장·구간을 확인한다
  2. 해당 파트의 script-writer를 재호출한다. 프롬프트에 **`prompts/tone-guide.md` 전문 + check_tone.py 출력 전문**을 넣는다
  3. 지시: 숫자는 반올림, 퍼센트는 '몇 중에 몇'으로, 전문용어는 치환표대로. **검증된 사실은 하나도 빼지 않는다**
  4. merge_draft.py → validate_draft.py → check_tone.py 재실행
- **2회 재작성 후에도 exit 1** → **파이프라인을 멈추고 사용자에게 보고한다.** 임의로 통과시키지 않는다
  - 보고 내용: 어느 항목이 몇 대 몇으로 걸렸는지 + 두 번의 재작성에서 얼마나 내려갔는지 + 남은 걸림돌 문장
  - 소재 특성상(법령·공시 중심) 물리적으로 못 맞추는 경우가 있다. 그 판단은 사용자가 한다

> 📌 **초기에는 재작성이 자주 발동한다.** 기존 70편을 이 게이트에 넣으면 63편이 실패한다(2026-08-04 실측).
> 옛 규칙으로 쓴 대본이라 당연한 결과다. 새 파이프라인(장면 수집 → outline 수치 배정 → tone-guide 전문 전달)을
> 거친 대본은 작성 단계에서 이미 기준 안으로 들어와야 정상이다. **재작성이 계속 2회씩 발동하면 게이트가 아니라
> 앞단(DATA_PREP·OUTLINE)이 잘못된 것이므로 그쪽을 고친다.**

> ⛔ **수치를 통째로 삭제해서 밀도를 맞추지 않는다.** 반올림·비유 치환·중복 제거로 줄인다.
> 사실 근거가 빠지면 독창성·팩트 검수에서 다시 걸린다.
> ⛔ **기준값을 임의로 완화하지 않는다.** 상한은 레퍼 히트작 실측으로 교정된 값이다 (`check_tone.py` docstring 참조).

---

## 썸네일 프롬프트 재생성 (단독 실행)

**트리거**: "썸네일 프롬프트 다시 뽑아줘", "썸네일만 다시 만들어줘"
**전제**: `concept.md`가 있는 프로젝트. `script.txt`가 이미 있는 완료 프로젝트도 대상이다.

> 🚨 **대본·컨셉·제목을 수정하지 않는다.** 이 경로는 썸네일 프롬프트만 계열별로 새로 만든다.
> `concept.md`, `outline.md`, `draft.md`, `script.txt`, `youtube.md`는 읽기만 하고 쓰지 않는다.

### 절차

1. **규칙 파일을 지금 다시 Read한다** — `prompts/thumbnail-design.md` + `prompts/thumbnail-countryball.md` + `prompts/thumbnail-geopolitics.md`
   - 이어서 진행 중인 세션이면 옛 규칙이 컨텍스트에 남아 있을 수 있다. 반드시 다시 읽는다
2. **재료 확인**:
   - `{P}/_script/concept.md` — 확정 제목, 썸네일 텍스트, 이미지 컨셉
   - `{P}/_script/script.txt` 또는 `draft.md` — **대본 내용 대표 2장의 근거**. 있으면 이쪽을 쓴다 (patterns.md보다 정확하다)
   - `{P}/_refs/*/meta.md` + `analysis.md` — 앵커 선정·계승용
3. **7~9번 계승 3장의 앵커를 정한다.** (계승할지 말지는 판정하지 않는다 — 3장 고정이다)

   > 🚨 **확정 패키지가 무엇이든(A·B·C·D) 7~9번은 3계열 모두 레퍼 계승 3장이다.**
   > 계승 절차와 판정 기준은 `prompts/thumbnail-design.md`의 「7~9번 장 — 무조건 3장 전부 레퍼 계승」 절이 **유일한 원본**이다. 여기에 다시 적지 않는다.

   **볼 레퍼만 여기서 정한다 — 짝의 근접성이 조회수보다 우선한다.**
   - `concept.md`에 "참고 레퍼 → 썸네일 계승 후보"가 있으면 **그 레퍼**를 쓴다
   - 없으면(구형 프로젝트 등) `_refs/*/meta.md`의 조회수 ÷ 경과일 1위를 전역 앵커로 쓴다
   - `_refs`가 비어 있거나 `thumbnail.webp`가 없으면 **그때만** 계승 불가 → 감정 클로즈업 3장으로 대체하고 사유를 `concept_ko`에 적는다

   앵커를 정했으면 그 `analysis.md`의 비주얼 분석과 `thumbnail.webp`를 근거로 **[모순] 한 줄을 뽑아** `concept_ko` 맨 앞에 적는다.
4. **해당하는 계열을 모두 생성한다. 어느 계열을 만들지 묻지 않는다.**
   - 기존 파일이 있으면 `{파일명}.bak`으로 옮긴 뒤 새로 쓴다 (덮어쓰기 전에 보존 — 그래서 확인을 받을 필요가 없다)
   - `{P}/output/thumbnails/prompts.json` — 실사형 9개 (항상)
   - `{P}/output/thumbnails/prompts-countryball.json` — 국기볼형 9개 (항상)
   - `{P}/output/thumbnails/prompts-geopolitics.json` — 정세형 9개 (**국가·안보·전쟁·정권 소재일 때만**. 아니면 생성하지 않고 사유 보고)
   - **예외**: 사용자가 "국기볼만", "정세형만"처럼 계열을 직접 지정했을 때만 그 계열만 만든다
5. **복사용 통합본 .txt 재생성** — 위 "복사용 통합본(.txt) 생성" 절차 그대로. JSON을 새로 썼으면 txt도 반드시 갱신한다 (기존 txt가 남아 있으면 옛 프롬프트를 복사하게 된다)
6. **채팅으로 계열을 분리 출력** — 위 "썸네일 프롬프트 채팅 출력 — 목록 표만" 형식 그대로 (목록 표 + txt 링크. 영문 원문 출력 금지)
7. 보고: 무엇이 바뀌었는지 1~2줄 (예: 애니메 → 실사 합성 단일, 국기볼형 9개 신규, 세이프존 1/2 → 1/3)

### 실행 방식

strategist Phase 5만 호출하거나 PD가 직접 작성한다. 어느 쪽이든 위 규칙 파일 2개를 읽고 시작한다.

---

## REVIEW_FINALIZE

**검수 + 확정. 에이전트: script-reviewer(verdict 권한 + 신규 주장 WebSearch 검증)**

1. **script-reviewer 에이전트 호출:**
   - 전달: `_script/draft.md` + `_script/outline.md` + `_script/concept.md` + `_script/verified-data.md` + **`prompts/tone-guide.md`** + `prompts/script-review-checklist.md` + `prompts/draft-verify.md` + `_refs/*/analysis.md` (독창성 검수 — 레퍼런스 고유 표현 대조용)
   - **문체 게이트에서 돌린 `check_tone.py` 출력 전문**을 함께 전달한다. reviewer는 이걸 review.md `## 0. 기계 검증`에 그대로 붙인다 (reviewer에게는 Bash 툴이 없다)
   - 출력: `{P}/_script/review.md` (체크리스트 + 심각도 분류 + 신규 주장 검증 결과 + verdict)
   - reviewer가 신규 주장을 식별하면 즉시 WebSearch로 검증하여 review.md에 포함

2. **verdict 확인:**
   - review.md의 `verdict:` 확인
   - `verdict: 통과` → finalize.py 실행
   - `verdict: 수정` → 리비전 1회

3. **리비전 (최대 1회):**
   - review.md 치명적 항목 (신규 주장 ❌/⚠️ 포함) 정리
   - script-writer 재호출 → draft.md 덮어쓰기
   - **재호출 프롬프트에 반드시 넣는다** (아래 "리비전 지시 필수 문구" 참조)
   - **리비전 후 기계 검증 재실행** (아래 참조) → finalize.py 실행

### 리비전 지시 필수 문구

> 🚨 **복제된 표현을 지운 자리는 "새 비유"로 채운다. 숫자로 대체하지 않는다.**
> 레퍼와 겹치는 비유를 삭제하고 그 자리에 사실·수치를 그대로 넣는 것이 가장 흔한 도피처인데,
> 그러면 독창성은 고쳐지고 숫자 밀도가 망가진다. **실측: `bar-karaoke-collapse`에서 리비전 전후로
> 숫자 밀도가 2.0 → 5.5로 뛰었다.** 기준 안이라 넘어갔지만 같은 일이 더 크게 벌어질 수 있다.
> `prompts/tone-guide.md`를 함께 전달하고, 대체 표현은 그 문서의 대조쌍대로 만들게 한다.

### 리비전 후 기계 검증 (finalize 전 필수)

```bash
{VENV_PYTHON} scripts/src/validate_draft.py {S}/outline.md {S}/draft.md
{VENV_PYTHON} scripts/src/check_tone.py {S}/draft.md
```

**검사만 한다. 자동 재수정하지 않는다.** 리비전은 1회로 끝이다.

> **왜 자동 루프를 안 도는가:** 독창성과 숫자 밀도는 서로 잡아당긴다(비유를 지우면 숫자가 늘고,
> 숫자를 줄이려 새 비유를 지으면 또 레퍼와 겹칠 수 있다). 그런데 숫자는 파이썬이 몇 초에 재는 반면
> **독창성은 에이전트가 레퍼 원문과 대조해야 안다.** 자동으로 계속 고치면 "숫자를 고치다 독창성이
> 다시 깨졌는지"를 확인할 방법이 없다. 그래서 검사만 하고 아래 규칙으로 처리한다.

**충돌 시 우선순위 — 독창성을 지키고 숫자를 양보한다.**

독창성 위반은 있냐 없냐의 문제이고 되돌릴 수 없다(올라간 영상은 못 고친다).
숫자 밀도는 정도의 문제이고 다음 편에서 고칠 수 있다. 그래서:

| 리비전 후 숫자 밀도 | 처리 |
|---|---|
| ~10.0 (차단선 이하) | 그대로 finalize |
| 10.0 ~ 13.0 | **finalize 진행.** 단 완료 보고에 `⚠️ 리비전 후 숫자 밀도 {값} (기준 8, 차단선 10)` 한 줄을 반드시 넣는다 |
| 13.0 초과 | **멈추고 사용자에게 보고.** 이건 양보 범위가 아니라 리비전이 대본을 망가뜨린 것이다 |

- **복제 표현을 되살려서 숫자를 맞추는 것은 어떤 경우에도 금지**다
- `validate_draft.py`가 exit 1/2면 분량이 깨진 것이므로 숫자 밀도와 무관하게 멈추고 보고한다

4. 확정 후 finalize:
```bash
{VENV_PYTHON} scripts/finalize.py --project {프로젝트} --channel "{채널}"
```
5. 결과: `{P}/_script/script.txt` (순수 텍스트, 한 줄 형태)

6. **TTS 검수:**
   - `{P}/_script/script.txt` 읽기
   - `prompts/tts-rules.md` 규칙에 따라 형식만 정리 (내용 변경 금지)
   - 정리된 텍스트를 `{P}/_script/script.txt`에 덮어쓰기

7. **youtube.md 생성:**
   - `{P}/_script/concept.md`에서 "확정 제목" 추출
   - `{P}/_script/concept.md`의 "핵심 약속" + "앵글" 기반으로 설명 작성
   - 채널 프로필(`profile.md`)의 장르 정보로 영상 장르/성격 소개 문구 생성 (**채널명·핸들은 설명·태그·해시태그 어디에도 넣지 않는다** — 업로드 채널이 달라질 수 있음)
   - `concept.md` + `outline.md` 키워드 기반으로 태그/해시태그 선정
   - **영상 출처**: `{P}/_script/factcheck.md`(출처 컬럼) + `{P}/_script/verified-data.md`("추가 리서치" 출처)에서 핵심 근거 출처 3~7개를 추출해 설명 다음 `## 영상 출처` 섹션에 정리 (새 검색 금지, 중복 병합, 출처 없으면 섹션 생략 — `pd-templates.md`의 "영상 출처 작성 규칙" 참조)
   - 포맷: `prompts/pd-templates.md`의 "youtube.md 포맷" + 설명/출처/태그 작성 규칙 참조
   - 출력: `{P}/output/youtube.md`

8. **고정 댓글 생성 (youtube.md에 포함):**
   - `pd-guide.md`에 크리에이터 리액션 가이드가 있는 채널만 해당
   - 대본(`script.txt`)의 크리에이터 리액션 구간에서 핵심 인사이트를 추출
   - youtube.md 하단에 `## 고정 댓글` 섹션으로 추가
   - 포맷:
     ```
     📌 이 영상을 만들며 든 생각

     {대본 크리에이터 리액션 구간의 핵심 내용을 2~4개 불릿으로 요약}

     이 분석은 저의 개인적인 견해이며, 실제 상황은 달라질 수 있습니다.
     여러분은 어떻게 생각하시나요?
     ```
