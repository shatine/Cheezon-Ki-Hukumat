# 3단계: 힌디어 문장 대응 → TTS → 실측 시간표

**누가:** the cloud translates, the PC runs the TTS. **Results:** `script/lines_hi_ko.tsv`, `review_edit/narr_timing.json`; PC: `CB\review_edit\narr\*.wav`, `narration_hi.wav`.

## 클라우드
1. **Sentence-matched Hindi:** one row per line, `S01a \t Hindi \t Korean literal translation` (episode 8: 70 lines).
   - Split long sentences into lines at commas. Lines must not break the paragraph structure.
   - Write numbers out in Hindi words. Write proper nouns in Devanagari.
   - The opening line is the same as the thumbnail text.
2. Write the PC work order (step 9 template): TTS, then the `narr_timing.json` push.

## PC (작업 지시서대로)
1. Copy `skills/cheezon-production/tools/tts_template.py` into the new episode's `review_edit\`. Put `lines.tsv` (= `lines_hi_ko.tsv`) next to it.
2. **Settings:** Voice Studio (free), voice `charonclone`, **seed 7 fixed**, speed 1.0, one sentence at a time, -16 LUFS.
3. **Strict defect check** (`junk_check`, `asr_check`). If a line fails:
   - regenerate it with the same seed, changing the commas;
   - if it still fails, split it at a comma;
   - if it still fails, split it in half.
4. **Pauses:** 0.35 s between sentences, 0.8 s between paragraphs.
5. Results: `narr\{id}.wav`, `narration_hi.wav`, `narr_timing.json` (start and end of each line), and `narr_check.json` (check results).
6. Push only `narr_timing.json` and `narr_check.json` to the repository. **The audio stays on the PC.**

## 클라우드 확인
- Total length (episode 8: 334.3 s); line count = number of tsv lines; failed lines in `narr_check.json`.
- Report the automatic results separately from what the user heard.

## 금지
- Estimating times from sentence length.
- Speeding up or cutting the narration to fit the picture.
- Changing the seed.
