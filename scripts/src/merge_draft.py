"""hook-intro.md + _draft_part*.md → draft.md 병합."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_H2_RE = re.compile(r"^#{2,3}\s+(.+)$", re.MULTILINE)
_PART_NUM_RE = re.compile(r"_draft_part(\d+)\.md$")


def extract_hook_intro(path: Path) -> tuple[str, str]:
    """hook-intro.md에서 ## Hook / ## Intro 본문만 추출."""
    text = path.read_text(encoding="utf-8")
    headers = [(m.start(), m.end(), m.group(1).strip()) for m in _H2_RE.finditer(text)]

    hook_text = None
    intro_text = None

    for i, (start, end, title) in enumerate(headers):
        next_start = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        body = text[end:next_start].strip()

        if re.match(r"Hook(\s*\(|$)", title):
            hook_text = body
        elif re.match(r"Intro(\s*\(|$)", title):
            intro_text = body

    if hook_text is None:
        raise ValueError(f"## Hook 헤더를 찾을 수 없습니다: {path}")
    if intro_text is None:
        raise ValueError(f"## Intro 헤더를 찾을 수 없습니다: {path}")

    return hook_text, intro_text


def collect_parts(parts_dir: Path) -> list[Path]:
    """_draft_part*.md를 숫자 순으로 정렬하여 반환."""
    parts = list(parts_dir.glob("_draft_part*.md"))
    if not parts:
        raise FileNotFoundError(f"_draft_part*.md 파일을 찾을 수 없습니다: {parts_dir}")

    def sort_key(p: Path) -> int:
        m = _PART_NUM_RE.search(p.name)
        return int(m.group(1)) if m else 999

    parts.sort(key=sort_key)
    return parts


def merge_draft(
    hook_intro_path: Path,
    parts_dir: Path,
    output_path: Path,
) -> int:
    """draft.md 병합. 0=성공, 1=오류."""
    try:
        hook_text, intro_text = extract_hook_intro(hook_intro_path)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        parts = collect_parts(parts_dir)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    sections = [f"## Hook & Intro\n\n{hook_text}\n\n{intro_text}"]

    # 파트 파일은 `## ` h2 한 줄로 시작해야 한다 (validate_draft.py의 계약).
    # 헤더가 없으면 이 파일이 앞 섹션에 통째로 흡수되고, 병합은 성공한 것처럼 끝난 뒤
    # validate 단계에서 개수 불일치로 exit 2가 난다. 원인이 여기라는 걸 알 수 없으므로
    # 여기서 미리 짚어 준다.
    header_problems: list[str] = []
    for part_path in parts:
        content = part_path.read_text(encoding="utf-8").strip()
        lines = content.splitlines()
        if not lines or not lines[0].startswith("## "):
            header_problems.append(f"{part_path.name}: 첫 줄이 `## ` 헤더가 아니다")
        extra = sum(1 for ln in lines[1:] if re.match(r"^#{2,3}\s+", ln))
        if extra:
            header_problems.append(f"{part_path.name}: 본문 안에 소제목 {extra}개 (##/### 금지)")
        sections.append(content)

    draft = "\n\n".join(sections) + "\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(draft, encoding="utf-8")

    print(f"draft.md 생성 완료: {output_path}")
    print(f"  Hook & Intro + {len(parts)}개 파트 병합")
    print(f"  총 {len(draft):,}자")

    if header_problems:
        print("\n[WARN] 파트 헤더 계약 위반 — validate_draft.py가 exit 2로 떨어진다:", file=sys.stderr)
        for p in header_problems:
            print(f"  · {p}", file=sys.stderr)
        print("  → 해당 파트 파일을 고친 뒤 merge를 다시 돌린다.", file=sys.stderr)

    _report_distant_repeats(output_path)
    return 0


def _report_distant_repeats(draft_path: Path) -> None:
    """병합 직후 원거리 반복을 파트 귀속과 함께 알려준다 (WARN, 종료코드 영향 없음).

    병합 시점은 전체 파트가 처음 한자리에 모이면서 **파트 경계 정보가 아직 살아 있는**
    유일한 지점이다. 작가들은 서로 뭘 썼는지 모르므로 여기서 한 번 훑어 준다.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from check_tone import find_distant_repeats, load_body_with_parts
    except Exception:
        return

    try:
        body, parts = load_body_with_parts(draft_path)
        hits = find_distant_repeats(body, parts)
    except Exception:
        return

    if not hits:
        return

    print(f"\n[WARN] 30초 밖에서 같은 말이 다시 나옴 — {len(hits)}건", file=sys.stderr)
    for d in hits[:5]:
        where = f"{d['first_part'] or '?'} → {d['second_part'] or '?'}"
        print(f"  · {where} (간격 {d['seconds']}초): {d['first'][:48]}…", file=sys.stderr)
    if len(hits) > 5:
        print(f"  … 외 {len(hits) - 5}건", file=sys.stderr)
    print("  → outline에 [회수]로 설계된 오픈루프면 정상. 아니면 뒤쪽을 새로 쓴다.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="hook-intro.md + _draft_part*.md → draft.md 병합",
    )
    parser.add_argument("--hook-intro", required=True, type=Path, help="hook-intro.md 경로")
    parser.add_argument("--parts-dir", required=True, type=Path, help="_draft_part*.md 디렉토리")
    parser.add_argument("--output", required=True, type=Path, help="출력 경로 (draft.md)")
    args = parser.parse_args()

    if not args.hook_intro.exists():
        print(f"ERROR: hook-intro.md를 찾을 수 없습니다: {args.hook_intro}", file=sys.stderr)
        sys.exit(1)
    if not args.parts_dir.is_dir():
        print(f"ERROR: parts 디렉토리를 찾을 수 없습니다: {args.parts_dir}", file=sys.stderr)
        sys.exit(1)

    sys.exit(merge_draft(args.hook_intro, args.parts_dir, args.output))


if __name__ == "__main__":
    main()
