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
4. **에이전트 위임**: 분석/검증/작문 등은 전문 에이전트(Task tool)에게 위임
5. **Lazy Load**: 상세 절차는 현재 단계에 해당하는 파일만 Read

### Lazy Load 실행 프로토콜

상태 감지 후, 현재 단계에 해당하는 파일만 Read한다:

| 감지 상태 | Read할 파일 |
|-----------|-------------|
| COLLECT ~ REVIEW_FINALIZE | `prompts/pd-script.md` |
| STRATEGY (ask 모드 확정 저장), REVIEW_FINALIZE | + `prompts/pd-templates.md` |
| STRATEGY (auto 모드) | + `channels/{채널}/config/pd-guide.md` (있으면) |
| 에이전트 호출 직전 (첫 호출 시 1회) | + `prompts/pd-agents.md` |

> ⚠️ **에이전트에게 넘길 프롬프트 파일은 PD가 읽지 않는다.** PD가 미리 읽으면 같은 텍스트가 이중으로 쌓인다.
> - strategist가 직접 Read: `creative-strategy.md`, `ctr-reference.md`, `thumbnail-design.md`, `thumbnail-countryball.md`, `thumbnail-geopolitics.md`
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

> ⚠️ **이 작업은 새 세션에서 하는 것을 권장한다.** 예전 세션에는 옛 썸네일 규칙(애니메·와일드카드·하단 1/2)이 컨텍스트에 남아 있어, 파일이 바뀌어도 옛 규칙으로 만들 수 있다. 이어서 하는 경우 반드시 계열별 규칙 파일 3종(`thumbnail-design.md`, `thumbnail-countryball.md`, `thumbnail-geopolitics.md`)을 **다시 Read한 뒤** 진행한다.

### 산출물 다시 정리 (완료된 프로젝트 포함)

"산출물 다시 줘", "산출물 정리해줘" → **상태와 무관하게 이 경로로 간다.** DONE 상태여도, 옛 규칙으로 만든 프로젝트여도 실행한다.

> 🚨 **아무것도 새로 만들지 않는다.** 대본·컨셉·제목·outline·youtube.md·썸네일 프롬프트를 **일절 건드리지 않는다.** 에이전트를 호출하지 않는다.
> 하는 일은 딱 둘이다 — ① 누락된 복사용 `.txt` 채우기 ② 5줄 형식으로 보고.

1. `{P}/output/thumbnails/`의 JSON 목록 확인
2. **JSON은 있는데 같은 이름의 `.txt`가 없으면 생성한다.** 기존 JSON의 `prompt_en`을 그대로 옮길 뿐 프롬프트 내용을 새로 쓰지 않는다 (절차 → `prompts/pd-script.md`의 "복사용 통합본(.txt) 생성")
   - **이미 있는 txt는 덮어쓰지 않는다.** JSON과 내용이 다를 수 있으므로, 불일치가 의심되면 덮어쓰기 전에 사용자에게 확인한다
3. 파일 존재 확인 후 **"5. 완료(DONE)"의 산출물 요약 5줄 형식 그대로** 보고
4. 산출물이 일부 없으면(예: youtube.md 미생성) 그 줄에 **없다고 명시**한다. 없는 파일을 링크로 걸지 않고, 임의로 만들지도 않는다 — 필요하면 사용자에게 만들지 물어본다

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
| STRATEGY | concept.md + hook-intro.md + prompts.json + prompts-countryball.json (+ prompts-geopolitics.json) + **계열별 복사용 통합본 .txt** | strategist 1회 | 패키지 4개(A·B·C·D). 썸네일 프롬프트 계열별 9개씩, 파일 분리. **프롬프트 파일은 경로로 전달**. 채팅에는 **목록 표 + txt 링크만** — 영문 프롬프트 원문 출력 금지 |
| OUTLINE | outline.md | outline-writer 1개 (셀프체크 내장) | **모든 파트 헤더에 `(~N분, ~N자)` 필수** (클로징 포함) → PD는 `grep '^### '`로만 검증 |
| DRAFT | draft.md | script-writer (파트당 1개 병렬) + merge_draft.py | 목표를 **범위로** 전달 → 병합 → 분량 검증. **`concept.md` 전달 금지** — outline `## 1. 기획 뼈대`로 대체 (파트 수만큼 곱해진다) |
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
   - 썸네일 프롬프트 (복사용) — [실사형](…prompts.txt) · [국기볼형](…prompts-countryball.txt) · [정세형](…prompts-geopolitics.txt)
   - 썸네일 컨셉·구조 (참고용) — [실사형](…prompts.json) · [국기볼형](…prompts-countryball.json) · [정세형](…prompts-geopolitics.json)
   ```

   **썸네일은 계열이 몇 개든 항상 2줄로 고정**한다 — 복사용(.txt) 한 줄, 참고용(.json) 한 줄. 계열별로 줄을 나누지 않는다.
   - 생성하지 않은 계열(예: 정세형 미해당)은 해당 링크만 빼고 줄 구조는 유지한다
   - 순서는 **복사용이 먼저**다. 실제로 여는 건 txt이고, json은 컨셉·계승 근거를 확인할 때만 연다
3. 글자수, 예상 분량(~440자/분) 표시

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
- 에이전트 파일 생성 실패 (Write 권한 오류) → 해당 에이전트를 1회 재호출. 재실패 시 PD가 직접 해당 파일을 생성 (에이전트 출력에서 내용을 추출하여 PD가 Write tool로 저장)
- 중단 후 재시작 → 상태 감지로 자동 파악 → 해당 단계부터 재개
