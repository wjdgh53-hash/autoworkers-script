# 대본 제작 — 상세 절차

`{P}` = `channels/{채널}/projects/{프로젝트}`
`{VENV_PYTHON}` = macOS/Linux: `.venv/bin/python` | Windows: `.venv\Scripts\python`

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
2. 전달: 채널 프로필 + `prompts/data-research.md` + 모든 transcript.txt + 모든 **meta.md**
3. 출력: `{P}/_script/factcheck.md` + `{P}/_script/verified-data.md` (추가 리서치 포함)

> 🚨 **`analysis.md`는 전달하지 않는다.** 리서치에 필요한 "레퍼가 무슨 내용을 다뤘나"는 원본인 `transcript.txt`에 전부 있다. `analysis.md`는 그걸 해석한 2차 자료(2편 합 약 2.8만 자)라서, 원본과 함께 주면 같은 내용을 두 번 읽는다. 구조·썸네일 분석은 리서치 방향과 무관하고, 그건 pattern-extractor가 쓴다.

### 완료 확인

- `_script/patterns.md` 존재 확인
- `_script/verified-data.md`에 "## 추가 리서치" 존재 확인

---

## STRATEGY

**크리에이티브 전략 통합 설계 + 썸네일 프롬프트. strategist 에이전트 1회.**

입력: `_script/patterns.md` + `_script/verified-data.md` + 채널 프로필

### 사전 준비

```bash
python -c "import os; os.makedirs('{P}/output/thumbnails', exist_ok=True)"
```

### strategist 에이전트 호출

> 🚨 **프롬프트 파일은 "내용"이 아니라 "경로"로 전달한다.** strategist는 Read 툴이 있어 스스로 읽는다.
> PD가 대신 읽어서 프롬프트에 붙여넣으면 같은 텍스트(약 3.3만 자)가 PD와 에이전트 양쪽에 이중으로 쌓인다.
> 대신 호출 프롬프트 **첫 지시로 "아래 파일들을 작업 시작 전에 모두 Read하라"를 명시**한다. 안 읽으면 규칙이 통째로 빠진다.

1. strategist 에이전트 호출:
   - **경로로 전달** (내용 임베드 금지):
     - `prompts/creative-strategy.md` — 5.5-Phase 설계 절차
     - `prompts/ctr-reference.md` — CTR 이론
     - `prompts/thumbnail-design.md` — 실사형 썸네일 규칙
     - `prompts/thumbnail-countryball.md` — 국기볼형 썸네일 규칙
     - `prompts/thumbnail-geopolitics.md` — 정세형 썸네일 규칙
     - `channels/{채널}/config/profile.md`
     - `channels/{채널}/config/settings.json` (hook_strategy)
     - `channels/{채널}/config/pd-guide.md` (있으면)
     - `channels/{채널}/config/thumbnail-strategy.json` (있으면)
     - `{P}/_script/patterns.md` + `{P}/_script/verified-data.md`
     - `{P}/_refs/` (analysis.md, meta.md, thumbnail.webp — 앵커 선정·계승용)
   - 함께 전달: 모드(auto/ask) + 출력 파일 경로 + 목표 러닝타임
   - auto 출력: `concept.md` + `hook-intro.md` + `prompts.json` + `prompts-countryball.json` (+ 국가·안보 소재면 `prompts-geopolitics.json`)
   - ask 출력: `_strategy_candidates.md` (전문) + **`_strategy_summary.md` (비교표만, 2,000자 이내)**

### auto 모드

1. concept.md + hook-intro.md + prompts.json + prompts-countryball.json (+ 국가·안보 소재면 prompts-geopolitics.json) 존재 확인
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
5. 썸네일 프롬프트 생성 (strategist Phase 5 재호출 또는 PD 직접) — 계열마다 파일 분리:
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
python3 -c "
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
   - `prompts/outline-guide.md` — outline 작성 규칙 전체 (셀프체크 9항목 포함)
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

**대본 초안 작성. 에이전트: script-writer (파트당 1개, 병렬)**

입력: `_script/outline.md` + `_script/verified-data.md` + 채널 프로필 + `prompts/script-review-checklist.md`

### 파트별 병렬 에이전트

1. outline.md `## 3. 본문 구조`에서 `### ` 파트 헤더 추출 → 파트 목록 확인
2. **Hook & Intro는 에이전트 범위에서 제외** — merge_draft.py가 자동 삽입
3. 파트당 에이전트 1개 병렬 호출:
   - 각 에이전트 → `_script/_draft_part{N}.md` 저장 (N = 파트 순서, 클로징 포함)
4. 각 에이전트에게 전달: outline.md(**`## 1. 기획 뼈대` + 담당 파트 섹션**) + verified-data.md + 채널 프로필 + script-review-checklist.md + 담당 파트명 + 출력 경로 + **목표 글자수 범위**(하한 90% ~ 상한 110%, 절대 상한 130%를 숫자로 명시)
5. 완료 확인: `ls {S}/_draft_part*.md`로 파일 수 == 파트 수

> 🚨 **`concept.md`는 전달하지 않는다.** 작가가 필요한 확정 제목·핵심 약속·타겟 시청자·톤은 `outline.md`의 `## 1. 기획 뼈대`(약 800자)에 전부 들어 있다.
> `concept.md`(약 1만 자)의 나머지는 제목 후보 3안·썸네일 카피 후보 3안·썸네일 이미지 컨셉·텐션 트라이앵글·정보갭 변형안·선택 근거인데, **작가가 하나도 쓰지 않는다.** 썸네일은 작가 일이 아니다.
> 파트당 1개씩 병렬 호출하므로 이 중복은 **파트 수만큼 곱해진다** — 6파트면 5.4만 자, 10파트면 9만 자다.

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
3. **실사형 5번 장(레퍼 계승)을 쓸 수 있는지 판정한다.**

   > ⚠️ **계승은 제목과 썸네일을 같은 앵커에서 함께 가져왔을 때 성립한다.**
   > 패키지 D는 제목 골격과 썸네일 구도를 한 앵커에서 같이 물려받아 둘이 한 몸으로 작동한다.
   > 구형 프로젝트는 **제목이 독자적으로 설계됐으므로 그 짝이 없다.** 검증된 구도라는 이유만으로 무관한 제목에 얹으면 텐션 트라이앵글이 깨진다.

   **(a) concept.md에 "계승 정보"가 있는 경우** (패키지 D로 만든 프로젝트)
   → 그 앵커를 그대로 쓴다. 5번은 예정대로 **레퍼 계승**.

   **(b) 계승 정보가 없는 경우** (A·B·C 확정, 또는 구형 프로젝트)
   1. 볼 레퍼를 정한다 — **짝의 근접성이 조회수보다 우선한다**
      - `concept.md`에 "참고 레퍼 → 썸네일 계승 후보"가 있으면 **그 레퍼**를 쓴다
      - 없으면(구형 프로젝트 등) `_refs/*/meta.md`의 조회수 ÷ 경과일 1위를 전역 앵커로 쓴다
   2. 해당 `analysis.md`의 썸네일 비주얼 분석을 읽고, **그 구도가 이 프로젝트의 확정 제목이 한 약속을 시각적으로 이행할 수 있는지** 판정한다
      - ⭕ **이행 가능** → 5번을 레퍼 계승으로 만든다. 단 "반드시 다르게 할 것 3개" 규칙은 그대로 적용
      - ❌ **상충하거나 무관** → **레퍼 계승을 쓰지 않는다.** 5번을 **감정 클로즈업**(인물/핵심 대상의 표정·상태를 크게 잡아 표정만으로 승부)으로 대체한다
   3. `_refs`가 비어 있거나 `thumbnail.webp`가 없으면 판정 불가 → 감정 클로즈업으로 대체

   **어느 쪽을 골랐든 그 판정과 근거를 보고한다.** 대체한 경우 "앵커 구도가 확정 제목과 맞지 않아 감정 클로즈업으로 대체했다"고 명시한다.
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
   - 전달: `_script/draft.md` + `_script/outline.md` + `_script/concept.md` + `_script/verified-data.md` + `prompts/script-review-checklist.md` + `prompts/draft-verify.md` + `_refs/*/analysis.md` (독창성 검수 — 레퍼런스 고유 표현 대조용)
   - 출력: `{P}/_script/review.md` (체크리스트 + 심각도 분류 + 신규 주장 검증 결과 + verdict)
   - reviewer가 신규 주장을 식별하면 즉시 WebSearch로 검증하여 review.md에 포함

2. **verdict 확인:**
   - review.md의 `verdict:` 확인
   - `verdict: 통과` → finalize.py 실행
   - `verdict: 수정` → 리비전 1회

3. **리비전 (최대 1회):**
   - review.md 치명적 항목 (신규 주장 ❌/⚠️ 포함) 정리
   - script-writer 재호출 → draft.md 덮어쓰기
   - finalize.py 실행 (재검수 없이 확정)

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
   - `pd-guide.md`에 크리에이터 분석 섹션 가이드가 있는 채널만 해당
   - 대본(`script.txt`)의 크리에이터 분석 구간에서 핵심 인사이트를 추출
   - youtube.md 하단에 `## 고정 댓글` 섹션으로 추가
   - 포맷:
     ```
     📌 {채널명}의 분석

     {대본 크리에이터 분석 섹션의 핵심 내용을 2~4개 불릿으로 요약}

     이 분석은 저의 개인적인 견해이며, 실제 상황은 달라질 수 있습니다.
     여러분은 어떻게 생각하시나요?
     ```
