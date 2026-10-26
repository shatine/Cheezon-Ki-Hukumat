# 8편 검수본 v1 클라우드 검수 (2026-10-26)

**Material reviewed:** `v1_review_small.mp4` (960x540, 30 fps, 335.34 s, 21 MB), which is the original `CB\out\v1_review_hi.mp4` scaled down.
- The original is on the PC, so the cloud checked this downscaled copy.
- **Method:**
  - Frames every 1 s from 0 s to the end (336 frames, 14 sheets).
  - Brightness and change between frames every 0.5 s.
  - Suspect spots enlarged at 960x540.
  - Loudness and silence measured.

## 판정: **합격, 1건 수정** → 업로드본 렌더로 진행

| 항목 | 결과 |
|---|---|
| Length, cuts | 335.33 s, 72 cuts (24 video, 48 images), matches the plan v2. Shortest 1.7 s, longest 9.93 s |
| Cut boundaries | All 72 boundaries fall where `cuts_v1.json` puts them. No black frames, no duplicated cuts, no reversed playback |
| Brightness | Lowest mean 84 (i11a). Nothing below 60. Brightness corrections on v12, i23b and i24 are applied |
| Freezes | Change between frames is below 0.3 at V10a at 132, 136.5 and 137 s, and V16a at 236.5 s. Both are principle shots where motion is small. Within tolerance |
| Flow watermark | V05 (70 s), V09 (128 s), V20b (300 s): no trace in the lower right |
| V09 composite | 125.5–131.3 s: grey cement spreads into the cracks from the pipe tip. Pass |
| Blur | i19a2 (267 s): the equipment display reads only as a green bar, no text. i20a (288 s): the jeep's number plate is blurred. Pass |
| Hindi subtitles | 102 lines, all one line, no clipping at the edges. They match the narration |
| Korean subtitles | 70 lines (review only). 9 long lines are reduced to 32–42 px, which is fine because they are not used in the upload version |
| Sound | -16.6 LUFS, peak -2.6 dB, narration only. Silence only in the last 1.0 s (334.3–335.3 s) |

## 수정 1건 (클라우드가 스크립트에서 고침)

- **The V02 labels appear in the wrong order.**
  - **Before:** "×5" appeared at 16.5 s, but the Qutub line starts at 20.8 s. "359 m" appeared at 20.7 s, after the 359 m line (15.1–18.3 s) had already ended.
  - **Fix:** in `edit_v1.py`, `LABEL` now shows "359 m" 0.8 s into the cut (16.5 s) and "×5" 5.1 s into the cut (20.8 s). Only the V02 cut is re-rendered.

## 참고 (고치지 않음)
- **V17 (244.4–252.5 s):** the red pier glows only about 2 s, during the line "even if one pier breaks". Then the train crosses. The meaning holds.
- **V10a, 139–140 s:** the black rope looks slightly thicker for a moment. Not visible at playback speed.
- **v23 (319–328 s):** the bridge is small in the frame, but it is the ending wide shot, so this is intended.
