"""통합본 인트로 intro.md → intro_script.txt (TTS 업로드용 한 줄 대본)

`finalize.py`가 본편 대본에 하는 일을 통합본 인트로에 똑같이 해 준다.
**정리 규칙은 이 파일에 다시 쓰지 않는다** — `finalize.py`의 함수를 그대로 import한다.
규칙 원본은 `prompts/tts-rules.md` 한 곳이고, 그 집행자는 `finalize.py` 한 곳이다.

본편과 다른 점은 두 가지뿐이다:
1. 입력이 `_script/draft.md`가 아니라 `_compilation/intro.md`다.
   (compilation 스킬은 `_script/`를 절대 만들지 않는다 — script-pd 영역이라 상태 감지가 꼬인다)
2. intro.md 아래쪽의 「검수 체크」 절은 대본이 아니므로 잘라낸다.
   첫 수평선(`---`) **앞까지**가 낭독 대상이다.

사용:
    python scripts/finalize_intro.py --dir channels/{ch}/projects/{proj}/_compilation
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from finalize import apply_tts_rules, print_report, strip_markdown_text, DEFAULT_CPM

_HR_SPLIT_RE = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def extract_narration(md: str) -> str:
    """intro.md에서 낭독 대상만 잘라낸다 — 첫 수평선 앞까지."""
    return _HR_SPLIT_RE.split(md, maxsplit=1)[0]


def main():
    parser = argparse.ArgumentParser(description="intro.md → intro_script.txt (+ TTS-safe 보정)")
    parser.add_argument("--dir", required=True, help="_compilation 폴더 경로")
    parser.add_argument("--cpm", type=int, default=DEFAULT_CPM,
                        help=f"분당 글자수 (기본 {DEFAULT_CPM})")
    args = parser.parse_args()

    comp_dir = Path(args.dir)
    intro = comp_dir / "intro.md"
    if not intro.exists():
        print(f"[ERROR] intro.md가 없습니다: {intro}", file=sys.stderr)
        sys.exit(1)

    narration = extract_narration(intro.read_text(encoding="utf-8"))
    text = strip_markdown_text(narration)
    text, report = apply_tts_rules(text)

    out = comp_dir / "intro_script.txt"
    out.write_text(text, encoding="utf-8")

    print_report(report, len(text), args.cpm)
    print(f"인트로 대본: {out}")
    print(f"예상 낭독 시간: 약 {round(len(text) / args.cpm * 60)}초")


if __name__ == "__main__":
    main()
