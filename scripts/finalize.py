"""draft.md → script.txt 변환 + TTS-safe 기계 검증·자동 보정

1) 마크다운 메타(헤더, 구분선, 주석, 블록인용, 리스트 마커, 링크, 강조)를 제거하고
   순수 대본 텍스트만 **한 줄로** 이어붙인다.
2) `prompts/tts-rules.md`의 정리 규칙을 기계로 검증·자동 보정하고 리포트를 출력한다:
   ① 온점 뒤 띄어쓰기  ② 따옴표(**보고만**)  ③ 한 줄 형식 유지
   ④ 특수문자·이모지 제거  ⑤ URL·이메일 제거  ⑥ 단어 뒤 괄호 제거
   + [pause]류 연출 태그·보이지 않는 공백 제거

   ⚠️ ②는 일부러 자동 보정에서 뺐다. tts-rules 3번은 "직접 인용이 **아니면** 제거"이지
      전면 금지가 아니다. 직접 인용 여부는 문맥 판단이라 기계가 가를 수 없고,
      TTS는 따옴표를 읽지 않으므로 남아도 무해하다. 건수만 보고하고 PD가 판단한다.
      (2기 finalize.py는 전부 지우지만, 그건 2기 규칙이고 우리 규칙이 아니다.)

🔴 2026-08-25 신설. 그전까지 이 정리는 **PD가 script.txt를 통째로 Read해서 손으로 고쳤다.**
   느리고(1만 자를 LLM이 다시 씀), 비싸고, 무엇보다 샜다 — 도입 직전 실측에서
   완성된 script.txt 14편 중 8편에 특수문자가 2~10개씩 남아 있었다.
   `tts-rules.md`는 그대로 둔다(원본). 이 파일은 그 규칙을 기계로 집행할 뿐이다.

⚠️ **script.txt는 한 줄 형식이다.** `tts-rules.md` 4번(문단 구분은 빈 줄)은 draft 단계
   규칙이며 여기 적용하지 않는다. 이 스크립트는 줄바꿈을 **하나도** 만들지 않는다.

⚠️ **내용은 건드리지 않는다.** 문장·단어·어순을 바꾸는 보정은 하나도 없다.
   물결표(`~`)는 tts-rules가 "「에서」로 읽는다"고 정하지만, 지우면 "97 98%"가 되어
   내용이 깨지므로 **자동 보정하지 않고 건수만 보고**한다.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from project_resolver import resolve_project_dir

DEFAULT_CPM = 440  # 분당 글자수 — outline-guide.md "분량 현실성 (1분 ≈ 440자)"와 같은 값

# ---------- 마크다운 정리 ----------

_ANY_HEADER_RE = re.compile(r"^#{1,6}\s+")  # h1~h6 → script.txt에서 제외
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)
_HR_RE = re.compile(r"^-{3,}$")
_BLOCKQUOTE_RE = re.compile(r"^>.*$")
_LIST_MARKER_RE = re.compile(r"^(?:[-*•]|\d+\.)\s+")
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_EMPHASIS_RE = re.compile(r"(\*{1,3}|_{2,3}|`+)")

# ---------- tts-rules 검증·보정 패턴 ----------

# ① 문장 끝 부호(+쉼표) 뒤 붙여쓰기.
#    소수점 3.5, 자릿수 1,000은 뒤가 숫자라 매치되지 않는다 — tts-rules가 둘 다 유지하라고 정한다.
_R1_SPACING_RE = re.compile(r"([.!?,])(?=[가-힣A-Za-z一-鿿])")

# ② 따옴표 (큰따옴표 전부 + 작은따옴표는 영단어 아포스트로피만 예외)
_R2_DQUOTE_RE = re.compile(r"[\"“”„«»「」『』]")
_R2_SQUOTE_RE = re.compile(r"[‘’](?![A-Za-z])|(?<![A-Za-z])[‘’']|'(?![A-Za-z])")

# ⑤ URL·이메일 — 특수문자 제거보다 먼저 돌려야 패턴이 살아 있다
_R5_URL_RE = re.compile(r"(?:https?://|www\.)\S+")
_R5_EMAIL_RE = re.compile(r"\S+@\S+\.\S+")

# ⑥ 단어 뒤 괄호: 클로드(Claude) → 클로드. 이후 남는 괄호(연출지시 등)는 통째 제거
_R6_WORD_PAREN_RE = re.compile(r"(?<=[가-힣A-Za-z0-9])\([^)]*\)")
_R6_ORPHAN_PAREN_RE = re.compile(r"\([^)]*\)")

# 연출 태그 + 보이지 않는 공백
_TAG_RE = re.compile(r"\[(?:pause|break|silence|music|sfx|쉼|멈춤|효과음|음악)[^\]]*\]", re.IGNORECASE)
_INVISIBLE_RE = re.compile(r"[​‌‍﻿]")

# ④ 특수문자: 개별 치환 후, 허용 문자 밖을 전부 제거 (이모지·※·★·→ 일괄 커버)
_R4_REPLACEMENTS = [
    (re.compile(r"·|ㆍ"), ", "),             # 가운뎃점 → 쉼표 (미국·중국 → 미국, 중국)
    (re.compile(r"…|‥"), "..."),             # 말줄임표 → ...
    (re.compile(r"[–—―]"), " "),             # en/em 대시 → 공백
    (re.compile(r"。"), ". "),
    (re.compile(r"、"), ", "),
    (re.compile(r"[〈-〛‹›\[\]{}<>]"), ""),   # 괄호류 기호 제거 (내용은 유지)
]
# 허용: 숫자·영문·한글·한자·공백과 . , ! ? % ~ : ' -
#   %      tts-rules가 퍼센트는 기호로 쓰라고 정한다
#   , .    천 단위 쉼표(8,000명)·소수점(16.5%)을 지켜야 한다
#   ~      지우면 내용이 깨진다. 보정하지 않고 건수만 센다
_R4_ALLOWED_RE = re.compile(
    r"[^0-9A-Za-z"
    r"가-힣ᄀ-ᇿ㄰-㆏"                      # 한글
    r"一-鿿"                                # 한자
    r"\s.,!?%~:'\-]"
)

# 보정하지 않고 보고만 하는 항목
_TILDE_RE = re.compile(r"~")

# 대본에 있으면 안 되는 영문·숫자 덩어리 (uuid·타임스탬프·세션 로그 조각).
#   🔴 실측으로 발견(2026-08-25): korea-shipbuilding-dominance의 draft.md 본문 한가운데에
#      `uuid:88c154ae-… timestamp:2026-04-14T05:01:43.720Z sourceToolAssistantUUID:…` 353자가
#      박혀 있었다. 옛 script.txt에는 없다 — **PD가 손 교정에서 걷어내고 있었던 것**이다.
#      그 단계를 기계로 대체하는 이상, 이걸 못 보면 그대로 TTS로 나간다.
#   한국어 나레이션에 영문·숫자 20자 연속은 정상적으로 나오지 않는다. 지우지 않고 **띄운다** —
#   지우면 어디가 잘렸는지 알 수 없고, 정상 고유명사를 삼킬 수도 있다.
_ASCII_BLOB_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9:._\-]{19,}")


def strip_markdown(draft_path: Path) -> str:
    """draft.md에서 마크다운 메타를 제거하고 **한 줄** 대본 텍스트를 반환."""
    raw = _HTML_COMMENT_RE.sub("", draft_path.read_text(encoding="utf-8"))

    body: list[str] = []
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if _HR_RE.match(s) or _BLOCKQUOTE_RE.match(s) or _ANY_HEADER_RE.match(s):
            continue
        s = _LIST_MARKER_RE.sub("", s)
        s = _MD_LINK_RE.sub(r"\1", s)
        s = _EMPHASIS_RE.sub("", s)
        s = s.strip()
        if s:
            body.append(s)

    return " ".join(body)


def _count_and_sub(pattern: re.Pattern, repl, text: str) -> tuple[str, int]:
    count = len(pattern.findall(text))
    return (pattern.sub(repl, text), count) if count else (text, 0)


def apply_tts_rules(text: str) -> tuple[str, dict]:
    """tts-rules 검증·자동 보정. (보정된 텍스트, 항목별 건수) 반환."""
    report: dict[str, int] = {}

    # 연출 태그·보이지 않는 공백·탭
    text, n_tag = _count_and_sub(_TAG_RE, "", text)
    text, n_inv = _count_and_sub(_INVISIBLE_RE, "", text)
    text = text.replace(" ", " ").replace("　", " ").replace("\t", " ")
    report["extra"] = n_tag + n_inv

    # ⑤ URL·이메일 (특수문자 제거 전)
    text, n_url = _count_and_sub(_R5_URL_RE, "", text)
    text, n_email = _count_and_sub(_R5_EMAIL_RE, "", text)
    report["r5"] = n_url + n_email

    # ② 따옴표 — **보고만 한다. 지우지 않는다.**
    #    tts-rules 3번은 "직접 인용이 아니면 제거"이지 전면 금지가 아니다.
    #    직접 인용인지는 문맥 판단이라 기계가 가를 수 없고, TTS는 따옴표를 읽지 않으므로
    #    남아 있어도 무해하다. 잘못 지우면 인용 경계가 사라져 내용이 상한다.
    report["r2"] = len(_R2_DQUOTE_RE.findall(text)) + len(_R2_SQUOTE_RE.findall(text))

    # ⑥ 단어 뒤 괄호 → 남은 괄호(연출지시 등)도 통째 제거
    text, n_wp = _count_and_sub(_R6_WORD_PAREN_RE, "", text)
    text, n_op = _count_and_sub(_R6_ORPHAN_PAREN_RE, "", text)
    text = text.replace("(", "").replace(")", "")
    report["r6"] = n_wp + n_op

    # ④ 특수문자·이모지
    n_r4 = 0
    for pattern, repl in _R4_REPLACEMENTS:
        text, n = _count_and_sub(pattern, repl, text)
        n_r4 += n
    text, n_rest = _count_and_sub(_R4_ALLOWED_RE, "", text)
    report["r4"] = n_r4 + n_rest

    # ① 온점 뒤 띄어쓰기 (마지막에)
    text, n_r1 = _count_and_sub(_R1_SPACING_RE, r"\1 ", text)
    report["r1"] = n_r1

    # ③ 한 줄 형식 — 줄바꿈을 공백으로 접고 공백을 정규화한다
    n_nl = text.count("\n")
    text = re.sub(r"\s+", " ", text).strip()
    report["r3_newlines_folded"] = n_nl

    # 보고만 (보정 안 함)
    report["tilde"] = len(_TILDE_RE.findall(text))
    report["blobs"] = _ASCII_BLOB_RE.findall(text)

    return text, report


def print_report(report: dict, char_count: int, cpm: int) -> None:
    def fmt(n):
        return f"{n}건 보정" if n else "0건"

    print("=== TTS-safe 검증 리포트 (prompts/tts-rules.md) ===")
    print(f"① 온점 뒤 띄어쓰기     : {fmt(report['r1'])}")
    if report["r2"]:
        print(f"② 따옴표               : {report['r2']}개 — ⚠️ 직접 인용인지 PD가 확인 (자동 제거 안 함)")
    else:
        print("② 따옴표               : 0개")
    print(f"③ 한 줄 형식           : 줄바꿈 {report['r3_newlines_folded']}개 접음 (script.txt는 한 줄)")
    print(f"④ 특수문자·이모지 제거 : {fmt(report['r4'])}")
    print(f"⑤ URL·이메일 제거      : {fmt(report['r5'])}")
    print(f"⑥ 단어 뒤 괄호 제거    : {fmt(report['r6'])}")
    print(f"기타 (연출태그·공백)   : {fmt(report['extra'])}")
    if report["tilde"]:
        print(f"⚠️ 물결표 {report['tilde']}개 — tts-rules는 「에서」로 읽으라고 정한다.")
        print("   지우면 내용이 깨지므로 자동 보정하지 않았다. PD가 직접 확인한다.")
    if report["blobs"]:
        print(f"\n🚨 대본에 있으면 안 되는 영문·숫자 덩어리 {len(report['blobs'])}건 — **반드시 확인한다**")
        for b in report["blobs"][:5]:
            print(f"     {b[:70]}")
        if len(report["blobs"]) > 5:
            print(f"     … 외 {len(report['blobs']) - 5}건")
        print("   uuid·타임스탬프·세션 로그 조각이 draft.md에 섞여 들어간 적이 있다.")
        print("   해당 자리를 draft.md에서 지운 뒤 finalize.py를 다시 돌린다.")
    print("=" * 34)
    print(f"script.txt 생성 완료 ({char_count:,}자, ~{char_count // cpm}분 @ {cpm}자/분)")


def main():
    parser = argparse.ArgumentParser(description="draft.md → script.txt (+ TTS-safe 보정)")
    parser.add_argument("--project", required=True, help="프로젝트 폴더명")
    parser.add_argument("--channel", default=None, help="채널명 (미지정시 자동 탐색)")
    parser.add_argument("--cpm", type=int, default=DEFAULT_CPM,
                        help=f"분당 글자수 — profile 실측치가 있으면 전달 (기본 {DEFAULT_CPM})")
    args = parser.parse_args()

    base = resolve_project_dir(args.project, args.channel)
    script_dir = base / "_script"
    script_dir.mkdir(parents=True, exist_ok=True)
    draft = script_dir / "draft.md"

    if not draft.exists():
        print(f"[ERROR] draft.md가 없습니다: {draft}", file=sys.stderr)
        sys.exit(1)

    text = strip_markdown(draft)
    text, report = apply_tts_rules(text)

    # 정본
    (script_dir / "script.txt").write_text(text, encoding="utf-8")

    # 완성본 사본 — 정호님이 여는 파일 (정본은 _script/script.txt)
    output_dir = base / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "01_대본.txt").write_text(text, encoding="utf-8")

    print_report(report, len(text), args.cpm)
    print("완성본 사본: output/01_대본.txt (영상 제작 사이트 업로드용)")


if __name__ == "__main__":
    main()
