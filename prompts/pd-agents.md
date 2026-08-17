# PD 에이전트 호출 사양

---

## 에이전트별 스펙

| 에이전트 | model | 실행 방식 | 참조 프롬프트 |
|----------|-------|-----------|-------------|
| video-analyst | **sonnet** | 전체 동시 병렬 | prompts/reference-analyze.md |
| pattern-extractor | **sonnet** | 1개 (data-researcher와 병렬) | prompts/reference-patterns.md + config/settings.json (hook_strategy) |
| data-researcher | opus | 1개 (pattern-extractor와 병렬, WebSearch) | prompts/data-research.md |

### 🚨 모델 배정 원칙 — 「추출은 sonnet, 창작·검증은 opus」

정해진 템플릿을 채우는 **추출·요약** 작업은 sonnet, 없던 것을 만들거나 사실을 판정하는 작업은 opus다.

| 구분 | 에이전트 | 이유 |
|---|---|---|
| **sonnet** | video-analyst, pattern-extractor | 레퍼 대본을 정해진 항목표에 옮기는 일이다. 창작이 아니다 |
| **opus 유지** | strategist, outline-writer, script-writer, script-reviewer | 대본 품질이 여기서 결정된다 |
| **opus 유지** | data-researcher | ⛔ **sonnet으로 내리지 않는다.** 팩트 검증이고, 틀리면 허위 컨텐츠 제재로 채널이 죽는다. script-reviewer가 뒤에서 재검증하지만 **「신규 주장」만** 본다 — `verified-data.md`에 이미 검증됐다고 적혀 들어온 틀린 수치는 신규 주장이 아니어서 그냥 통과한다 |

> 이 배정은 1차 버전(`autoworkers-1st`)의 원설계다. 중간에 전부 opus로 바뀌면서 비용이 뛰었고, 2026-08-17에 되돌렸다.
> ⛔ **에이전트를 새로 추가할 때 기본값을 opus로 두지 않는다.** 위 표의 구분으로 먼저 판정한다.
| strategist **#1** | opus | 1개 (STRATEGY 전반) | prompts/creative-strategy.md + prompts/ctr-reference.md + prompts/pd-templates.md + config/settings.json (hook_strategy) + config/thumbnail-strategy.json (있으면) — **썸네일 계열 규칙 3종은 주지 않는다** |
| strategist **#2** | opus | 1개 (STRATEGY 후반, 패키지 확정 후) | prompts/creative-strategy.md **Phase 5 절만**(PD가 `grep -n '^## Phase 5'`로 줄 번호를 잡아 offset 전달) + prompts/thumbnail-design.md + prompts/thumbnail-countryball.md + (국가·안보 소재면) prompts/thumbnail-geopolitics.md |
| outline-writer | opus | 1개 (OUTLINE) | prompts/outline-guide.md + prompts/pd-templates.md (outline.md 포맷 절) |
| script-writer | opus | **인접 파트 2개씩 묶어 1개** 병렬 (6파트 → 3개) | outline.md + prompts/script-review-checklist.md |
| script-reviewer | opus | 1개 (verdict 권한, WebSearch) | prompts/script-review-checklist.md + prompts/draft-verify.md |

---

## 병렬 호출 패턴

독립적인 에이전트 N개를 동시에 실행:
1. 전체 대상 목록에 대해 Agent tool 동시 호출 (run_in_background: true)
2. 출력 파일 존재 여부를 Glob으로 확인
3. 모든 파일 생성 확인 후 다음 단계

**배치 분할 하지 않는다** — 에이전트들이 독립적이고 TaskOutput을 사용하지 않으므로 PD 컨텍스트 부하 없음.

---

## Task tool 호출 시 전달 내용

에이전트에게 항상 전달:
1. **역할** (agents/*.md에 정의된 역할 설명)
2. **도메인 프롬프트** (prompts/*.md — **파일 경로로 전달**)
3. **프로젝트 데이터** (파일 경로 — 에이전트가 직접 Read)
4. **출력 경로** (결과 파일 절대 경로)

> 🚨 **파일 내용을 prompt에 임베드하지 않는다. 경로만 전달한다.**
> PD가 대신 읽어서 붙여넣으면 같은 텍스트가 PD 컨텍스트와 에이전트 프롬프트에 **이중으로 쌓인다.**
> (STRATEGY 단계 기준 약 3.3만 자 중복)
>
> 대신 호출 프롬프트의 **첫 지시로 "아래 파일들을 작업 시작 전에 모두 Read하라"를 명시**한다.
> 경로만 던지고 읽으라는 말을 빠뜨리면 에이전트가 안 읽고 진행해 규칙이 통째로 빠진다.

---

## 결과 확인 규칙 (필수)

- **TaskOutput 절대 사용 금지**: 에이전트 전체 transcript(base64 이미지 포함)가 PD 컨텍스트에 덤프되어 컨텍스트 폭발을 일으킴
- **대신**: 출력 파일 존재 여부를 Glob으로 확인 → 필요한 부분만 Read
- 에이전트가 파일을 잘 생성했는지만 확인하면 충분
- 에이전트 실패 시: 해당 에이전트만 재실행 (파일 미생성으로 감지)
