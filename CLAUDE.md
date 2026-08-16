# autoworkers

유튜브 영상 대본 자동 제작 파이프라인. 레퍼런스 수집 → 분석 → 전략 → 대본 작성 → 리뷰까지.

## 요청 라우팅 (분기 규칙) — 작업 시작 전 반드시 먼저 판별

**URL "유무"로 분기하지 않는다. URL의 "종류"와 "요청 의도"로 분기한다.**

### 1단계 — URL 종류 판별

| 패턴 | 종류 |
|------|------|
| `youtube.com/watch?v=...`, `youtu.be/...`, `youtube.com/shorts/...` | **영상 URL** |
| `youtube.com/@핸들`, `/channel/UC...`, `/c/...`, `/user/...`, 끝에 `/videos` | **채널 URL** |
| `youtube.com/playlist?list=...` | **재생목록 URL** |

### 2단계 — 라우팅 표

| 입력 | 라우팅 | 이유 |
|------|--------|------|
| **영상 URL** + "대본 만들어줘" | `script-pd` — 그 영상을 **레퍼런스**로 COLLECT (URL 다시 묻지 않음) | 영상 1개는 레퍼지 진단 대상이 아니다 |
| **영상 URL 여러 개** + "대본 만들어줘" | `script-pd` — 전부 레퍼런스로 COLLECT | 동일 |
| **재생목록 URL** + "대본 만들어줘" | `script-pd` — 레퍼런스로 COLLECT | 동일 |
| **채널 URL** (+ 대본/기획/진단 무엇이든) | `channel-trend-pd` | 채널 전체 스캔이 필요 |
| **URL 없음** + "대본 만들어줘 / **이어서 해줘 / 계속해줘** / 다시 써줘" | `script-pd` (로컬 프로젝트 재개) | 「이어서·계속」은 **하던 작업**이다 — 아래 「다음」과 헷갈리지 말 것 |
| **URL 없음** + "{주제}로 대본 만들어줘" | `script-pd` — 주제가 있으므로 레퍼를 찾아 COLLECT | 무엇을 만들지가 정해져 있다 |
| **URL 없음** + "다음 컨텐츠 기획 / 채널 진단" | `channel-trend-pd` (채널 URL 물어봄) | |
| **「다음」이 들어간 제작 요청** — "다음 거 / 다음 대본 / 다음 편 / 다음 소재로 / 그다음 거 / 순서대로 다음 거 / 다음 순번 / 대기열 다음 거 / 큐에서 다음 소재로" | `channel-trend-pd` **빠른 경로(Phase 0-A)** — **어느 채널인지 먼저 묻고**, `production-queue.md`의 미제작 1순위를 꺼내 배율만 재확인하고 곧장 `script-pd` 인계 | **이미 검증된 소재다. 전체 스캔을 다시 돌리지 않는다** |
| **레퍼도 주제도 없음** + "오늘 소재 추천해줘 / 오늘 뭐 올리지 / 주제 알아서 정해줘" | `channel-trend-pd` **전체 스캔** | **무엇을 만들지부터 정해야 한다** |
| **영상 URL** + "이 채널 진단해줘 / 다음 컨텐츠 기획해보자" | `channel-trend-pd` (영상 → 소속 채널 역추적) | **의도 문구가 URL 종류보다 우선** |
| **여러 영상 URL** + "통합본 / 영상 합쳐줘" | `compilation` | |

### 우선순위

1. **의도 문구가 명시적이면 그것이 최우선** ("진단", "채널 분석", "다음 컨텐츠 기획", "소재 추천" → channel-trend-pd / "통합본" → compilation)
2. 의도 문구가 없으면 **URL 종류**로 판별
3. **애매하면 작업을 시작하지 말고 사용자에게 먼저 확인한다.** 잘못된 스킬로 수집·스캔을 돌리면 시간과 API 호출이 낭비된다.

> **가장 직관적인 판별 기준 — 「무엇을 만들지가 정해져 있는가」**
> 주제나 레퍼런스가 **있으면** → `script-pd` (만들기만 하면 된다)
> 주제도 레퍼런스도 **없으면** → `channel-trend-pd` (무엇을 만들지부터 정해야 한다)

> ⚠️ 흔한 오류: `watch?v=` 영상 URL을 보고 "URL이 있으니 channel-trend-pd"로 가는 것. **영상 URL 단독은 script-pd다.**

## 사용법

### 채널 만들기
채널 생성 요청 시 **반드시 `.claude/skills/channel-setup/SKILL.md`를 먼저 읽고** 그대로 따를 것.
```
"채널 만들어줘"        → channel-setup 스킬 로드 → 대화형 채널 생성
```

### 대본 만들기
대본 제작 관련 요청 시 **반드시 `.claude/skills/script-pd/SKILL.md`를 먼저 읽고** 그대로 따를 것.
```
"대본 만들어줘"                    → SKILL.md 로드 → 상태 감지 → 자동 진행
"{영상 URL} 대본 만들어줘"          → SKILL.md 로드 → 그 영상을 레퍼런스로 COLLECT
"이어서 해줘"                      → 마지막 상태에서 재개
"대본 다시 써줘"                   → 해당 단계만 재실행
"산출물 다시 줘 / 산출물 정리해줘"   → 파일 확인 + 누락된 복사용 txt만 생성 → 5줄 형식 보고
```
> "산출물 다시 줘"는 **아무것도 새로 만들지 않는다.** 대본·컨셉·프롬프트를 건드리지 않고, 완료된 옛 프로젝트에도 쓸 수 있다.

### 통합본 만들기
통합본 제작 관련 요청 시 **반드시 `.claude/skills/compilation/SKILL.md`를 먼저 읽고** 그대로 따를 것.
```
"통합본 만들어줘"      → compilation 스킬 로드 → 메타데이터 수집 → 조합 추천 → 인트로 작성
"영상 합쳐줘"          → compilation 스킬 로드
```

### 다음 컨텐츠 기획 (채널 진단 → 트렌드 결합)
**메시지에 유튜브 "채널" URL(`/@핸들`, `/channel/UC...`, `/c/`, `/user/`, `/videos`)이 있거나**, 또는 **"진단/기획" 의도 문구가 있으면** 반드시 `.claude/skills/channel-trend-pd/SKILL.md`를 먼저 읽고 그대로 따를 것.
채널 진단 → 히트작 DNA(제목 공식·썸네일 프레임·구조) 계승 → 최신 트렌드 결합 → 주제 확정 → script-pd 인계.
```
"{채널 URL} 대본 만들어줘"        → channel-trend-pd 로드 → 진단 → DNA 추출 → 트렌드 결합 → script-pd
"다음 컨텐츠 기획해보자"           → channel-trend-pd 로드 (채널 URL 있으면 그 채널, 없으면 물어봄)
"채널 진단해줘"                   → channel-trend-pd 로드 → 진단만/기획까지
"{영상 URL} 이 채널 진단해줘"      → channel-trend-pd 로드 (영상 → 소속 채널 역추적)
```
> ⚠️ **`watch?v=` 영상 URL + "대본 만들어줘"는 channel-trend-pd가 아니다 → script-pd(레퍼런스 수집).**
> 채널 전체를 스캔·진단해야 할 이유(채널 URL 또는 명시적 진단/기획 요청)가 있을 때만 이 스킬로 온다. 전체 분기 규칙은 위 "요청 라우팅" 표 참조.

## 프로젝트 구조

```
autoworkers/
├── .claude/
│   ├── skills/script-pd/SKILL.md         # PD 두뇌 (상태머신)
│   ├── skills/channel-setup/SKILL.md     # 채널 생성 스킬
│   ├── skills/compilation/SKILL.md       # 통합본 기획 스킬
│   ├── skills/channel-trend-pd/SKILL.md  # 채널 진단→히트 DNA 계승→트렌드 결합→script-pd 인계
│   └── agents/                            # 역할별 에이전트 정의
├── channels/{channel-name}/            # 채널별 설정 + 프로젝트
│   ├── config/                        # 채널 설정 파일
│   │   ├── settings.json              # 채널 식별 (id, name)
│   │   └── profile.md                 # 채널 성격 전체 (장르, 톤, 서사, 관점 등)
│   └── projects/                      # 영상별 작업 폴더
│       └── {project-name}/
│           ├── _refs/                  # 레퍼런스 수집 결과 (script-pd 전용)
│           ├── _script/               # 대본 단계 산출물 (script-pd 전용)
│           ├── _compilation/          # 통합본 기획 산출물 (compilation 전용)
│           └── output/                # 최종 산출물 (youtube.md, thumbnails/)
├── prompts/                           # 에이전트용 프롬프트
├── scripts/                           # Python 코드
│   ├── collect.py                     # yt-dlp 수집
│   ├── finalize.py                    # draft → script.txt
│   └── src/                           # 유틸리티
└── requirements.txt                   # Python 의존성
```

## 크로스 플랫폼 규칙 (필수)

이 프로젝트는 macOS와 Windows 사용자가 함께 사용한다. **모든 명령어 실행 시 OS를 자동 감지하여 적절한 명령어를 사용할 것.**

### Python 실행
- macOS/Linux: `.venv/bin/python scripts/...`
- Windows: `.venv\Scripts\python scripts/...`

```bash
# macOS/Linux
.venv/bin/python scripts/collect.py --project {project} --channel "{channel}" URL1 URL2

# Windows (cmd/PowerShell)
.venv\Scripts\python scripts/collect.py --project {project} --channel "{channel}" URL1 URL2
```

### pip 실행
- macOS/Linux: `.venv/bin/pip install -U yt-dlp`
- Windows: `.venv\Scripts\pip install -U yt-dlp`

### 파일/디렉토리 조작 — 셸 명령 대신 Python 사용
OS별 셸 명령(`mv`, `rm -r`, `mkdir -p` 등)은 크로스 플랫폼 호환이 안 되므로, **Python으로 대체**한다:

```bash
# mkdir -p 대신
python -c "import os; os.makedirs('path/to/dir', exist_ok=True)"

# mv 대신
python -c "import shutil; shutil.move('src', 'dst')"

# rm -r 대신
python -c "import shutil; shutil.rmtree('path/to/dir')"
```

> **프롬프트/스킬의 셸 명령은 예시일 뿐이다.** 실행 시 반드시 현재 OS에 맞는 명령어를 사용할 것.

## 산출물

최종 산출물은 `_script/script.txt`. 이 파일을 영상 제작 사이트에 업로드하면 TTS → 영상 제작이 자동 진행됨.
부가 산출물: `output/youtube.md` (제목/설명/태그), `output/thumbnails/prompts.json` (썸네일 프롬프트).
