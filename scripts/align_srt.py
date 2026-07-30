# -*- coding: utf-8 -*-
"""
인트로 대본(자막 덩어리) + TTS 오디오 → 강제 정렬 SRT 생성.

대본이 정답 텍스트이므로 오디오에서는 '타이밍'만 가져온다.

엔진 2종:
  - ctc     (기본, 권장): ONNX MMS wav2vec2 CTC 강제정렬. torch 불필요.
             정답 텍스트를 프레임 단위(20ms)로 정렬 → ASR·보간 없음 → 오차 최소.
  - whisper (폴백): faster-whisper ASR 단어 타임스탬프 + difflib 정렬. 근사치.

--chunks 파일: 자막 한 줄에 표시할 덩어리를 한 줄씩 (빈 줄 무시).
줄 순서 = 자막 순서. 텍스트는 대본 원문 철자 그대로 유지할 것.

사용:
  .venv/bin/python scripts/align_srt.py \
      --audio "channels/{ch}/projects/{proj}/_compilation/intro.mp3" \
      --chunks "channels/{ch}/projects/{proj}/_compilation/intro_chunks.txt" \
      --out "channels/{ch}/projects/{proj}/_compilation/intro.srt"
  # Windows: .venv\\Scripts\\python scripts\\align_srt.py --audio ... --chunks ... --out ...

옵션:
  --engine ctc|whisper   (기본 ctc)
  --keep-gaps            자막 사이 자연 쉼(텀)을 그대로 둔다 (기본은 텀 제거)
  --lead 0.12            모든 자막을 N초 앞당김 (자막이 늦게 뜰 때)
"""
import re, sys, os, argparse, difflib


def fmt(t):
    if t < 0:
        t = 0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        ms = 0
        s += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def read_chunks(path):
    with open(path, encoding="utf-8") as f:
        chunks = [ln.strip() for ln in f if ln.strip()]
    if not chunks:
        print("ERROR: 자막 덩어리 파일이 비어 있습니다.", file=sys.stderr)
        sys.exit(1)
    return chunks


# ---------------------------------------------------------------------------
# 엔진 1: CTC 강제정렬 (ONNX MMS) — 기본
# ---------------------------------------------------------------------------
def align_ctc(audio, chunks, lang="kor"):
    import onnxruntime  # noqa
    from ctc_forced_aligner import (
        load_audio, generate_emissions, preprocess_text,
        get_alignments, get_spans, postprocess_results,
        ensure_onnx_model, Tokenizer, MODEL_URL,
    )
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".models")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "ctc_forced_aligner.onnx")
    ensure_onnx_model(model_path, MODEL_URL)

    import onnxruntime
    session = onnxruntime.InferenceSession(model_path)
    tokenizer = Tokenizer()

    waveform = load_audio(audio)
    emissions, stride = generate_emissions(session, waveform, batch_size=4)

    text = " ".join(chunks)
    tokens_starred, text_starred = preprocess_text(text, romanize=True, language=lang)
    segments, scores, blank = get_alignments(emissions, tokens_starred, tokenizer)
    spans = get_spans(tokens_starred, segments, blank)
    word_ts = postprocess_results(text_starred, spans, stride, scores)  # [{start,end,text}]

    total_dur = word_ts[-1]["end"] if word_ts else 0.0

    # 단어를 순서대로 소비하며 chunk에 배정 (CTC는 단어당 1개 결과 = 정확 매칭)
    chunk_word_counts = [len(c.split()) for c in chunks]
    if sum(chunk_word_counts) != len(word_ts):
        # 안전장치: 개수 불일치 시 whisper 폴백
        print(f"WARN: CTC 단어 수 불일치(정렬 {len(word_ts)} vs 대본 {sum(chunk_word_counts)}). whisper 폴백.", file=sys.stderr)
        return None
    chunk_times = []
    idx = 0
    for cnt in chunk_word_counts:
        ws = word_ts[idx:idx + cnt]
        idx += cnt
        chunk_times.append((ws[0]["start"], ws[-1]["end"]))
    return chunk_times, total_dur


# ---------------------------------------------------------------------------
# 엔진 2: faster-whisper ASR + difflib (폴백)
# ---------------------------------------------------------------------------
def align_whisper(audio, chunks, model="medium", lang="ko"):
    def norm(s):
        return re.sub(r'[^0-9A-Za-z가-힣%]', '', s)

    my_words = []
    for ci, ch in enumerate(chunks):
        for w in ch.split():
            nw = norm(w)
            if nw:
                my_words.append((nw, ci))
    my_norm = [w for w, _ in my_words]

    from faster_whisper import WhisperModel
    print(f"[whisper] 모델({model}) 로딩 + 전사...", file=sys.stderr)
    wm = WhisperModel(model, device="cpu", compute_type="int8")
    segments, _ = wm.transcribe(audio, language=lang, word_timestamps=True, beam_size=5)
    rec = []
    for seg in segments:
        if seg.words:
            for w in seg.words:
                nw = norm(w.word)
                if nw:
                    rec.append((nw, w.start, w.end))
    if not rec:
        print("ERROR: 오디오에서 단어를 인식하지 못했습니다.", file=sys.stderr)
        sys.exit(1)
    total_dur = rec[-1][2]
    rec_norm = [w for w, _, _ in rec]

    sm = difflib.SequenceMatcher(a=my_norm, b=rec_norm, autojunk=False)
    my_time = [None] * len(my_words)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                r = rec[j1 + k]
                my_time[i1 + k] = (r[1], r[2])
    n = len(my_time)
    first = next((i for i in range(n) if my_time[i]), None)
    if first is None:
        print("ERROR: 대본과 오디오가 정렬되지 않습니다.", file=sys.stderr)
        sys.exit(1)
    for i in range(first):
        my_time[i] = (my_time[first][0], my_time[first][0])
    last = max(i for i in range(n) if my_time[i])
    for i in range(last + 1, n):
        my_time[i] = (my_time[last][1], my_time[last][1])
    i = 0
    while i < n:
        if my_time[i] is None:
            j = i
            while j < n and my_time[j] is None:
                j += 1
            s = my_time[i - 1][1]
            e = my_time[j][0]
            span = (e - s) / (j - i + 1)
            for k in range(i, j):
                my_time[k] = (s + span * (k - i), s + span * (k - i + 1))
            i = j
        else:
            i += 1
    ct = {}
    for (w, ci), t in zip(my_words, my_time):
        st, en = t
        if ci not in ct:
            ct[ci] = [st, en]
        else:
            ct[ci][0] = min(ct[ci][0], st)
            ct[ci][1] = max(ct[ci][1], en)
    return [tuple(ct[ci]) for ci in range(len(chunks))], total_dur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--chunks", required=True, help="자막 덩어리 파일 (한 줄에 하나)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--engine", choices=["ctc", "whisper"], default="ctc")
    ap.add_argument("--model", default="medium", help="whisper 엔진 모델")
    ap.add_argument("--ctc-lang", default="kor", help="CTC 언어 (ISO 639-3, 한국어 kor)")
    ap.add_argument("--wh-lang", default="ko", help="whisper 언어")
    ap.add_argument("--keep-gaps", dest="close_gaps", action="store_false", default=True,
                    help="자연 쉼(텀)을 그대로 둔다 (기본은 텀 제거)")
    ap.add_argument("--lead", type=float, default=0.0,
                    help="모든 자막을 N초 앞당김 (예: 0.12)")
    args = ap.parse_args()

    chunks = read_chunks(args.chunks)

    result = None
    if args.engine == "ctc":
        print("[1/2] CTC 강제정렬(ONNX MMS)...", file=sys.stderr)
        try:
            result = align_ctc(args.audio, chunks, lang=args.ctc_lang)
        except Exception as e:
            print(f"WARN: CTC 실패({e}). whisper 폴백.", file=sys.stderr)
            result = None
    if result is None:
        chunk_times, total_dur = align_whisper(args.audio, chunks, model=args.model, lang=args.wh_lang)
    else:
        chunk_times, total_dur = result

    # 순서 정리 + 리드 오프셋
    seq = []
    prev_end = 0.0
    for ci in range(len(chunks)):
        st, en = chunk_times[ci]
        st = max(st - args.lead, 0.0, prev_end)
        en = max(en - args.lead, st + 0.3)
        seq.append([st, en])
        prev_end = en

    # 텀 제거: 각 자막을 다음 자막 시작까지 유지
    if args.close_gaps:
        for k in range(len(seq) - 1):
            seq[k][1] = seq[k + 1][0]
        seq[-1][1] = max(seq[-1][1], total_dur)

    with open(args.out, "w", encoding="utf-8") as f:
        for ci in range(len(chunks)):
            st, en = seq[ci]
            f.write(f"{ci + 1}\n{fmt(st)} --> {fmt(en)}\n{chunks[ci]}\n\n")

    print(f"[2/2] 저장 완료: {args.out}  (엔진 {args.engine}, 총 약 {total_dur:.1f}초)", file=sys.stderr)
    for ci in range(len(chunks)):
        st, en = seq[ci]
        print(f"{ci + 1:2d}  {fmt(st)} --> {fmt(en)}  {chunks[ci]}")


if __name__ == "__main__":
    main()
