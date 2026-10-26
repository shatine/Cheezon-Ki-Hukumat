# 7단계: 편집 — 검수본 렌더 → 0초~끝 검수 → 업로드본 렌더 → 확인

**Template:** `episodes/ep08/review_edit/edit_v1.py`. It runs on the PC; the cloud writes and tests it.

## 편집 스크립트 (클라우드 작성)
- **Inputs:**
  - `CB\review_edit\narration_hi.wav`, `narr\{id}.wav`
  - `episodes/epNN/review_edit/narr_timing.json`
  - `plan/shot_list_vN.json`
  - `CB\clips_v1\*.mp4`, `CB\img\*.png`
  - Paths can be overridden with the environment variables `CB`, `BGM`, `LABEL_FONT`, `HI_FONT` and `KO_FONT`.
- **Checks before rendering:** stop if a source is missing or too short (`src_end > dur - 0.03`).
- **Cut rendering (one segment per cut, `CB\out\v1_hi_seg\NNN.mp4`):**
  - Video: trim from the source start, 1.0× speed, fps 30, scale and crop to 1920×1080.
  - Image: slow zoom of about 6% (`zoompan`), alternating left, centre and right pans.
  - Options:
    - `flow_wm`: `delogo`.
    - `bright`: video gradually corrected over the cut; images by gamma.
    - `blur_plate`: `gblur` on BLUR ratio coordinates.
    - `hflip`.
    - `LABEL`: `drawtext`, green 0x33FF33, black border. **Show each number at the moment its narration line starts.**
  - Check the frame count of each segment.
- **Review cut** (`python edit_v1.py`):
  - Hindi subtitles: Nirmala UI 58, white, black border, bottom margin 104. Long lines are split at commas, timed to the nearest pause.
  - Korean literal translation: Malgun Gothic 44, yellow; shrunk when it does not fit.
  - Narration only.
  - Output `CB\out\v1_review_hi.mp4`, plus the small copy for the cloud `v1_review_small.mp4` (960×540, crf 30).
  - Also produces `subs_hi.srt`, `subs_ko.srt`, `subs.ass`, `cuts_v1.json` and `edit_report_v1.json`.
- **Upload cut** (`python edit_v1.py --upload`):
  - Reuses the review-cut segments; only the LABEL cuts are rendered again.
  - **One line of Hindi only:** Nirmala UI 60, margin 64. No Korean.
  - Background music `bgm.mp3` at -21 dB, sidechain ducking under the narration (threshold 0.03, ratio 6, attack 20, release 400).
  - Fade out over the last 2 s. `loudnorm I=-14:TP=-1.5:LRA=11`.
  - Output `CB\out\v1_upload_hi.mp4`, `v1_upload_subs_hi.srt`, `v1_upload_small.mp4`, `edit_report_v1_upload.json`.
- **Test in the cloud before handing it over:** render once with fake media (coloured clips and images, a sine-wave BGM, Linux fonts). Check the length, cut count, labels and LUFS.

## 검수본 검수 (클라우드, 0초~끝 전부)
1. Pull → copy the small copy to scratch → `git rm` → push.
2. Read the report: total length = plan, cut count, subtitle count.
3. Make **sheets of frames every 1 s** (all 336 or so, 24 per sheet). **Look at every sheet.**
4. **Brightness every 0.5 s** (nothing below 60), **change between frames** (below 0.3 = suspected freeze; principle shots can be an exception).
5. **Enlarge the suspect spots:** label timing, watermark positions, blurred areas, composites, subtitle clipping.
6. **Sound:** `ebur128` (review cut is narration only, about -16 LUFS), `silencedetect` (only the end may be silent).
7. Record in `review_edit/review_v1.md`:
   - a table (pass or fail per item);
   - fixes (what changed in the script);
   - notes (left unfixed, with the reason).
8. Fix the script → test in the cloud → write the upload work order.

## 업로드본 확인
- LUFS -14 ±0.5, TP ≤ -1.5, BGM about 15–20 dB below the narration in the pauses, the fade-out at the end.
- One line of subtitles, no overlaps, no Korean.
- Any fixed spots (labels and so on) are now correct.
- Add an "업로드본 v1 확인" section to `review_v1.md`, and write in HANDOFF that it can be uploaded.
