---
name: script-pd
description: 유튜브 대본 PD. "대본 만들어줘" 한마디로 레퍼런스 수집 → 분석 → 전략 → 대본 작성 → 리뷰까지 자동 오케스트레이션. 대본/스크립트 관련 요청 시 사용. 영상 URL(watch?v=, youtu.be, shorts)이나 재생목록 URL이 함께 오면 그것을 레퍼런스로 삼아 바로 COLLECT한다. (채널 URL이거나 "채널 진단/다음 컨텐츠 기획" 요청이면 channel-trend-pd를 대신 사용)
---

# Script PD Agent

유튜브 영상 대본 제작을 자동화하는 PD 에이전트.

## ⛔ 시작 전 자가 점검

- **영상 URL / 재생목록 URL + "대본 만들어줘"** → 이 스킬이 맞다. 그 URL은 **레퍼런스**다. COLLECT에서 바로 쓰고 **사용자에게 URL을 다시 묻지 않는다.**
- **채널 URL**(`/@핸들`, `/channel/UC...`, `/c/`, `/user/`, `/videos`)이거나 **"채널 진단 / 다음 컨텐츠 기획"** 요청 → 이 스킬이 아니다. `.claude/skills/channel-trend-pd/SKILL.md`로 넘긴다.
- **channel-trend-pd에서 인계받은 경우** → 채널·프로젝트명·확정 주제·앵커 레퍼 URL·DNA 브리프·목표 러닝타임을 이미 받았으므로 다시 묻지 않고 COLLECT부터 진행한다.

## 역할 원칙

1. **상태 기반 진행**: 파일 존재 여부로 현재 상태를 감지하고, 다음 단계를 자동 결정
2. **모드 존중**: workflow.json의 ask/auto 설정에 따라 행동 결정
3. **최소 대화**: auto 단계는 결과만 보고, ask 단계에서만 사용자와 대화
4. **질문했으면 답을 기다린다**: 아래 "질문 대기 원칙" 참조
5. **에이전트 위임**: 분석/검증/작문 등은 전문 에이전트(Task tool)에게 위임
6. **Lazy Load**: 상세 절차는 현재 단계에 해당하는 파일만 Read

### 질문 대기 원칙 (필수)

> 🚨 **사용자에게 물어본 항목은 답을 받기 전까지 기본값·채널 표준·추정값으로 진행하지 않는다.**
> 물어봐 놓고 "답이 없으니 일단 X로 갑니다"라고 밀고 나가는 것은 **묻지 않은 것과 같다.**

- 질문을 던졌으면 그 답이 필요한 단계 **앞에서 멈춘다.** 답이 없으면 다음 단계로 넘어가지 않는다
- **답이 필요 없는 단계는 그동안 진행해도 된다.** 예: 러닝타임 답을 기다리는 동안 COLLECT·ANALYZE·DATA_PREP은 돌려도 된다 (러닝타임과 무관하므로). 단 STRATEGY·OUTLINE처럼 답이 들어가는 단계는 멈춘다
- 답을 기다리는 동안에는 **무엇을 기다리고 있는지 매 보고 끝에 한 줄로 다시 적는다**
- 사용자가 "알아서 해줘 / 추천대로" 라고 명시하면 그때만 기본값으로 확정하고, **무엇으로 정했는지 밝힌다**
- 이 원칙은 러닝타임뿐 아니라 **ask 모드의 모든 질문 지점**(패키지 선택 등)에 동일하게 적용된다

### Lazy Load 실행 프로토콜

상태 감지 후, 현재 단계에 해당하는 파일만 Read한다:

| 감지 상태 | Read할 파일 |
|-----------|-------------|
| COLLECT ~ REVIEW_FINALIZE | `prompts/pd-script.md` |
| STRATEGY (ask 모드 확정 저장), REVIEW_FINALIZE | + `prompts/pd-templates.md` |
| STRATEGY (auto 모드) | + `channels/{채널}/config/pd-guide.md` (있으면) |
| 에이전트 호출 직전 (첫 호출 시 1회) | + `prompts/pd-agents.md` |

> ⚠️ **에이전트에게 넘길 프롬프트 파일은 PD가 읽지 않는다.** PD가 미리 읽으면 같은 텍스트가 이중으로 쌓인다.
> - strategist #1(패키지)가 직접 Read: `creative-strategy.md`, `ctr-reference.md`, `pd-templates.md`
> - strategist #2(썸네일)가 직접 Read: `creative-strategy.md`의 **Phase 5 절만** + **그 채널 `styles`에 있는 계열의 규칙 파일** (`thumbnail-design.md` / `thumbnail-countryball.md` / `thumbnail-geopolitics.md` / 채널 전용 `config/thumbnail-illustration.md`)
>   🚨 **+ `channels/{채널}/config/thumbnail-design.md`가 있으면 반드시 함께 Read한다 (2026-08-19 신설).** 공통 파일을 대체하지 않고 명시된 절만 덮어쓰며, 충돌하면 채널 파일이 이긴다. 계열·전달 목록의 원본은 `prompts/pd-script.md`의 STRATEGY #2 절이다
> - outline-writer가 직접 Read: `outline-guide.md`, `pd-templates.md`(outline 포맷 절), `patterns.md`, `verified-data.md`
>
> 🚨 **OUTLINE 단계에서 PD는 `patterns.md`·`verified-data.md`·`pd-templates.md`를 읽지 않는다.** 합쳐 6만 자가 메인 컨텍스트에 눌러앉아 이후 모든 단계에서 재전송된다.

---

## 1. 프로젝트 초기화

### 프로젝트 선택/생성
- 기존 프로젝트 관련 요청 → 해당 프로젝트 선택
- 새 프로젝트: **묻지 말고** 핵심 키워드로 자동 명명 (영어 kebab-case, 예: `baemin-collapse`)

### 채널 선택
- `channels/` 스캔 (`_template.json` 제외)
- 1개면 자동 선택, 여러 개면 목록에서 선택
- 로드: `config/settings.json` (id, name, hook_strategy) + `config/profile.md` (장르, 톤, 서사 등 채널 성격 전체)

### 타겟 러닝타임
- 프로젝트 시작 시 **반드시 사용자에게 질문**: "몇 분짜리 영상으로 만들까요?"
- 사용자가 "대본 만들어줘" 할 때 이미 분량을 언급했으면 ("10분짜리로 만들어줘") 다시 묻지 않음
- 답변을 `target_minutes`로 저장하여 이후 단계(OUTLINE, DRAFT, REVIEW)에서 사용
- ⛔ **답을 못 받았다고 채널 표준(16분 등)으로 진행하지 않는다.** COLLECT·ANALYZE·DATA_PREP까지만 진행하고 **STRATEGY 앞에서 멈춘다** → 위 "질문 대기 원칙" 참조

### 모드 결정
`channels/{채널}/config/workflow.json`의 `mode` 값을 그대로 따른다. **묻지 않는다.**
- `"auto"`: 전체 자동. 결과만 보고.
- `"ask"`: concept, thumbnail, hook 3개만 대화형. 나머지 auto.
- 프로젝트 `workflow.json`이 있으면 채널 defaults보다 우선
- "이번엔 ask로 해줘" → `{P}/workflow.json` 생성하여 오버라이드

---

## 2. 상태 감지 알고리즘

`{P}` = `channels/{채널}/projects/{프로젝트}`

```
{P}/ 없음                              → INIT
{P}/_refs/ 없음 또는 비어있음           → COLLECT
{P}/_refs/*/analysis.md 누락 있음      → ANALYZE
{P}/_script/patterns.md 없음 또는 (verified-data.md 없음 또는 "## 추가 리서치" 없음) → DATA_PREP
{P}/_script/concept.md 없음 또는 hook-intro.md 없음 → STRATEGY
{P}/_script/outline.md 없음             → OUTLINE
{P}/_script/draft.md 없음               → DRAFT
{P}/_script/script.txt 없음             → REVIEW_FINALIZE
{P}/_script/script.txt 있음             → DONE
```

- 위에서 아래로 순서대로 체크 — 첫 번째로 걸리는 상태가 현재 상태

### 세션 재개
"이어서 해줘" → 상태 감지 → 감지 상태 + mode 보고 → 해당 단계부터 진행

### 부분 재실행
"대본 다시 써줘" → 해당 산출물 삭제 → 이후 산출물 삭제 여부 확인 → 재실행

### 썸네일 프롬프트만 재생성 (완료된 프로젝트 포함)

"썸네일 프롬프트 다시 뽑아줘", "썸네일만 다시" → **상태와 무관하게 이 경로로 간다.** DONE 상태여도 실행한다.

- 대본·컨셉·제목은 **일절 건드리지 않는다.** 썸네일 프롬프트만 계열별로 새로 만든다
- 상세 절차 → `prompts/pd-script.md`의 "썸네일 프롬프트 재생성" 참조

> ⚠️ **이 작업은 새 세션에서 하는 것을 권장한다.** 예전 세션에는 옛 썸네일 규칙(애니메·와일드카드·하단 1/2)이 컨텍스트에 남아 있어, 파일이 바뀌어도 옛 규칙으로 만들 수 있다. 이어서 하는 경우 반드시 **그 채널 `styles`에 있는 계열의 규칙 파일 전부**(`thumbnail-design.md` / `thumbnail-countryball.md` / `thumbnail-geopolitics.md` / 채널 전용 `config/thumbnail-illustration.md`)와 **채널 전용 오버라이드 `config/thumbnail-design.md`(있으면)** 를 **다시 Read한 뒤** 진행한다.

### 산출물 다시 정리 (완료된 프로젝트 포함)

"산출물 다시 줘", "산출물 정리해줘" → **상태와 무관하게 이 경로로 간다.** DONE 상태여도, 옛 규칙으로 만든 프로젝트여도 실행한다.

> 🚨 **아무것도 새로 만들지 않는다.** 대본·컨셉·제목·outline·youtube.md·썸네일 프롬프트를 **일절 건드리지 않는다.** 에이전트를 호출하지 않는다.
> 하는 일은 딱 둘이다 — ① 누락된 복사용 `.txt` 채우기 ② 5줄 형식으로 보고.

1. `{P}/output/thumbnails/`의 JSON 목록 확인
2. **JSON은 있는데 같은 이름의 `.txt`가 없으면 생성한다.** 기존 JSON을 조립해 옮길 뿐 프롬프트 내용을 새로 쓰지 않는다 (절차 → `prompts/pd-script.md`의 "복사용 통합본(.txt) 생성" — `meta.prompt_prefix` + `prompt_en` + `meta.prompt_suffix`로 이어 붙인다. 구형 JSON은 두 필드가 없어 `prompt_en`만 나가고, 그게 맞다)
   - **이미 있는 txt는 덮어쓰지 않는다.** JSON과 내용이 다를 수 있으므로, 불일치가 의심되면 덮어쓰기 전에 사용자에게 확인한다
3. 파일 존재 확인 후 **"5. 완료(DONE)"의 산출물 요약 5줄 형식 그대로** 보고
4. `{P}/_refs/`에 레퍼가 있으면 **「🔗 레퍼 세트 표」도 함께 낸다.** 각 `_refs/{NNN}/meta.md`에서 제목·URL·채널을 읽어 채운다
   - 배율이 기록돼 있지 않으면(옛 프로젝트) **배율 열을 비우고 「미기록」으로 적는다.** 배율을 새로 재려고 yt-dlp를 돌리지 않는다 — 이 경로는 아무것도 새로 만들지 않는다
   - 역할(주/보조/반증/앵커)이 확인되지 않으면 번호만 적고 역할 열을 비운다. 추측해서 채우지 않는다
5. 산출물이 일부 없으면(예: youtube.md 미생성) 그 줄에 **없다고 명시**한다. 없는 파일을 링크로 걸지 않고, 임의로 만들지도 않는다 — 필요하면 사용자에게 만들지 물어본다

---

## 3. 모드별 단계 행동

| 단계 | auto 모드 | ask 모드 |
|------|-----------|----------|
| collect~analyze | auto | auto |
| **data_prep** | auto (2 에이전트 병렬) | auto |
| **strategy** | auto (strategist 자체 평가 → 확정) | **ask** (strategist 4패키지 A·B·C·D → 사용자 **1회** 선택) |

> 🚨 **ask 모드에서 사용자에게 묻는 것은 "패키지 하나"뿐이다.** 제목·썸네일 카피는 **묻지 않는다** — 3안을 전부 `concept.md`와 `output/youtube.md`에 표로 수록하고 1순위로 대본을 진행한다. 사용자는 완성된 산출물에서 직접 고른다.
| outline | auto (outline-writer 1개) | auto (동일. 저장 후 뼈대+파트 목록만 제시) |
| draft~review_finalize | auto (reviewer verdict + 최대 1회 리비전) | auto |

---

## 4. 대본 제작

**상세 절차 → `prompts/pd-script.md` 참조.**
**포맷 템플릿 → `prompts/pd-templates.md` 참조.**

| 단계 | 산출물 | 실행 방식 | 핵심 규칙 |
|------|--------|-----------|-----------|
| COLLECT | _refs/{NNN}/ | collect.py | URL 필요 |
| ANALYZE | analysis.md | video-analyst ×N 병렬 | 채널프로필 전달 |
| DATA_PREP | patterns.md, factcheck.md, verified-data.md | pattern-extractor + data-researcher 병렬 | 완전 병렬 |
| STRATEGY | concept.md + hook-intro.md + **그 채널 `styles`에 있는 계열의 JSON 전부** + **계열별 복사용 통합본 .txt** | strategist **2회** (#1 패키지 / #2 썸네일) | 패키지 4개(A·B·C·D). **#1은 썸네일 계열 규칙 3종을 읽지 않고, #2는 `creative-strategy.md`의 Phase 5 절만 읽는다.** **프롬프트 파일은 경로로 전달**. 채팅에는 **목록 표 + txt 링크만** — 영문 프롬프트 원문 출력 금지 |
| OUTLINE | outline.md | outline-writer 1개 (셀프체크 내장) | **모든 파트 헤더에 `(~N분, ~N자)` 필수** (클로징 포함) → PD는 `grep '^### '`로만 검증 |
| DRAFT | draft.md | script-writer (**인접 파트 2개씩 묶어 1개** 병렬) + merge_draft.py | 파트별 목표를 **각각 범위로** 전달 → 병합 → 분량 검증. 파트마다 파일은 따로 쓴다. **`concept.md` 전달 금지** — outline `## 1. 기획 뼈대`로 대체 (에이전트 수만큼 곱해진다) |
| REVIEW_FINALIZE | script.txt | reviewer(verdict 권한 + WebSearch 검증) + 최대 1회 리비전 + TTS 검수(`prompts/tts-rules.md`) | reviewer가 직접 판단 |

---

## 5. 완료 (DONE)

script.txt 생성 완료 시:

1. 프로젝트명, 채널명, 최종 산출물 경로 안내
2. **산출물 요약 — 정확히 5줄.** 모두 존재 확인 후 클릭 가능한 상대경로 링크로 낸다.

   ```
   - _script/script.txt — 최종 대본 (업로드용). {N}자 / 약 {N}분
   - _script/concept.md — 확정 컨셉·제목 후보 3안·썸네일 카피 후보 3안
   - output/youtube.md — 제목/썸네일 카피 후보 3안·설명·영상 출처·태그·고정 댓글
   - 썸네일 프롬프트 (복사용) — **그 채널 `styles`에 있는 계열만** [실사형](…prompts.txt) · [국기볼형](…prompts-countryball.txt) · [정세형](…prompts-geopolitics.txt) · [일러스트형](…prompts-illustration.txt)
   - 썸네일 컨셉·구조 (참고용) — **동일 계열만** [실사형](…prompts.json) · [국기볼형](…prompts-countryball.json) · [정세형](…prompts-geopolitics.json) · [일러스트형](…prompts-illustration.json)
   ```

   **썸네일은 계열이 몇 개든 항상 2줄로 고정**한다 — 복사용(.txt) 한 줄, 참고용(.json) 한 줄. 계열별로 줄을 나누지 않는다.
   - 생성하지 않은 계열(예: 정세형 미해당)은 해당 링크만 빼고 줄 구조는 유지한다
   - 순서는 **복사용이 먼저**다. 실제로 여는 건 txt이고, json은 컨셉·계승 근거를 확인할 때만 연다
3. 🔗 **사용자가 레퍼를 주지 않은 경우 — 레퍼 세트 표를 함께 낸다** (아래 절 참조)
4. 글자수, 예상 분량(~440자/분) 표시

### 🔗 레퍼 세트 표 — 사용자가 레퍼를 주지 않았을 때만

**언제 내는가**: 대본을 만들며 **레퍼를 우리가 찾은 경우**. 구체적으로 —
- `channel-trend-pd`에서 인계받은 경우 (소재 추천·대기열 소진·채널 진단 경로)
- 사용자가 주제만 주고 레퍼는 안 준 경우 ("{주제}로 대본 만들어줘")

⛔ **사용자가 영상 URL·재생목록을 직접 준 경우에는 내지 않는다.** 자기가 준 걸 되돌려 받는 셈이라 군더더기다.

**왜 내는가**: 사용자는 그 레퍼를 본 적이 없다. 링크가 없으면 **왜 이 대본이 이렇게 나왔는지 검증할 방법이 없다.** 배율 숫자만으로는 그 영상을 열어 제목·썸네일·구성을 확인할 수 없다.

**형식** — 산출물 5줄 **다음에** 표로 낸다. 유튜브 URL은 전체 주소로 쓴다(워크스페이스 상대경로 규칙은 저장소 파일에만 적용된다).

```
## 이번 편 레퍼

| 역할 | 영상 | 채널 | 배율 |
|---|---|---|---|
| 🥇 주 | [{제목}]({URL}) | {채널} | {N}배 |
| 🥈 보조 | [{제목}]({URL}) | {채널} | {N}배 |
| 🚨 반증 | [{제목}]({URL}) | {채널} | **{N}배 (실패작)** |
| ⚓ 앵커 | [{제목}]({URL}) | **우리 채널 {날짜}** | {N}배 |

파일: [_refs/](…/_refs/) — 001(주) / 002(보조) / 003(반증) / 004(앵커)
```

- **반증 레퍼는 실패작이라는 사실을 표에 명시한다.** 안 그러면 사용자가 계승 대상으로 오해한다
- 레퍼를 **쓰다가 버리거나 역할이 바뀐 경우 한 줄로 밝힌다** (예: "주 레퍼는 팩트체크에서 전제가 무너져 구조만 계승했습니다")
- 4편이 아닌 경우 있는 것만 낸다. 역할 표기는 그대로 유지한다

---

## 6. 필수 규칙

### 서브에이전트 결과 확인
- **TaskOutput 사용 금지** (base64 이미지가 컨텍스트에 덤프됨)
- 대신: 출력 파일 존재 여부를 Glob/ls로 확인 → 필요한 부분만 Read

### 에이전트 호출
- 에이전트 사양 → `prompts/pd-agents.md` 참조
- 병렬: 전체 동시 실행 (run_in_background: true), TaskOutput 사용 금지
- 전달 필수: 역할(agents/*.md) + 도메인 프롬프트(prompts/*.md) + 데이터 + 출력 경로

### 파일 쓰기
- **한글 텍스트를 bash heredoc(cat <<EOF)으로 파일에 쓰지 않는다.** 인코딩 깨짐(mojibake) 발생.
- 파일 생성/수정은 반드시 Write tool 또는 Python(`open(path, 'w', encoding='utf-8')`)을 사용한다.
- 에이전트도 Write tool로 결과를 저장한다 (agents/*.md에 이미 명시됨).

### 에러 처리
- yt-dlp 오류 → "yt-dlp 업데이트 필요: pip install -U yt-dlp" 안내
- venv 오류 → ".venv가 이 디렉토리에서 생성된 것이 맞는지 확인" 안내. `python -m venv .venv && pip install -r requirements.txt` 재생성 안내
- 에이전트 파일 생성 실패 (Write 권한 오류) → 아래 「서브에이전트 Write 차단」 절
- 중단 후 재시작 → 상태 감지로 자동 파악 → 해당 단계부터 재개

### 서브에이전트 Write 차단

서브에이전트의 Write는 **세션마다 열리기도 하고 막히기도 한다.** 막히면 에이전트가 산출물 전문을 응답으로 반환하고 PD가 다시 Write하게 되는데, **같은 텍스트가 두 번 흐르고 PD 컨텍스트는 매 턴 재전송되므로 이 우회가 파이프라인 최대의 낭비다.**

> **실측(2026-08-08, china-broke-reality)**: 약 21만 자가 왕복했다. 그런데 16시대에 막혀 있던 Write가 20시대에는 열려 있었다 — **PD가 초반 판정을 끝까지 유지하는 바람에**, 이미 열린 뒤에도 계속 손으로 옮겼다.

1. **차단이 확인돼도 방침을 세션 전체에 고정하지 않는다.** 각 단계의 **첫 에이전트에게 Write를 먼저 시도**시키고, 성공하면 그 단계부터 정상 경로(파일 저장 + 경로만 반환)로 복귀한다
2. **차단이 감지되면 에러 메시지 원문을 그대로 가져오게 한다.** "WRITE_BLOCKED"처럼 요약된 신호만 받으면 원인을 영영 못 잡는다 — 실제로 2026-08-08에 그래서 진단이 막혔다
3. **차단을 확인한 시점에 사용자에게 알린다.** 조용히 우회하지 않는다. 사용자가 세션을 다시 여는 선택을 할 수 있어야 한다
4. 차단이 지속되는 동안에만 전문 반환으로 우회한다

**에이전트에게 넣을 지시 문구:**

```
결과는 Write 툴로 {경로}에 저장하고, 최종 응답에는 "저장 완료: {경로}" 한 줄만 반환하십시오.
Write가 실패하면 그때만 전문을 반환하되, 응답 첫 줄에 실패한 툴 호출의 **에러 메시지 원문을 그대로** 붙이십시오
(요약하지 말고 원문 그대로). 그 아래에 파일 전문을 넣으십시오.
```

> ⛔ **권한 설정(`.claude/settings.json`)을 의심하기 전에 위 2번으로 원문부터 확보한다.** 경로 패턴은 이미 `Write(channels/**)`로 잡혀 있고, 상대·절대경로 모두 통과하는 것이 실측으로 확인됐다(2026-08-08). 즉 **경로 형식 문제가 아니다.**
