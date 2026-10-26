# 4단계: 문장 단위 장면 계획 (자동 점검 오류 0)

**누가:** 클라우드. **Template:** `episodes/ep08/plan/plan_v2.py` (latest) or `skills/cheezon-production/tools/plan_template.py`.
**Results:** `plan/shot_list_vN.json` (used by the edit script) and `plan/shot_table_vN.md` (for people to read).

## 계획 스크립트 구성
- `T = narr_timing.json`, the measured timings. `VEND` = narration end + `TAIL` (1.0 s).
- `USE = {id: (start, end)}`: the usable range of each video.
  - At planning time assume `(0, CEND)`, with `CEND = clip length - 0.05` (episode 8: 9.95).
  - Update it with the measured values after the video review.
- `FILE = {id: path}`: exceptions, such as a case-clash filename or a composite (`V09_fill.mp4`).
- `VID = {id: (file, [usable ranges], role)}`. Roles: 도입 (opening), 원리 (principle), 무빙 (camera move), 동작 (action).
- `IMG = {id: filename}`, `PICK_N = {id: chosen number}`.
- `SEG = [(start s, source id, 'v'/'i', source start s, option), ...]`. Each cut ends where the next row starts.
- **Options:** `flow_wm`, `bright`, `blur_plate`, `hflip`, `haze`, `x5 표기` (edit label).
- `PRINCIPLE_SENT`: the ids of the principle sentences.

## 자동 점검 (전부 통과해야 다음 단계)
- Length of every cut > 0.
- Video: inside its usable range. No overlapping source ranges.
- Image: exists, **no reuse**, **4.5 s or less**.
- Total length = narration end + TAIL (within 0.04 s).
- No sources unused by the plan.
- **Principle sentence:** at least 60% of its time is video.
- **Opening 0–30 s:** **3–5 videos**, all of them video.
- **Non-principle video share: 10–20%.**
- Errors = 0 → `shot_table` reads "점검: 통과".

## 장면 배정 원칙
- Principles go on 3D principle videos (fixed camera). Hooks, scale and places go on realistic images or camera-move videos.
- Long sentences are split with extra reaction, close-up or reversal images so that images change every 2–4 s.
- **Image effects:** slow zoom in or out of about 6%, alternating left, centre and right pans (`effect` = `in_c`, `out_l`, …).
- Do not repeat the same direction of move twice in a row.

## 금지
- Estimated times.
- Slow motion, freezes, repeats, reversed playback.
- A video range ending past CEND.
- Moving to the next step with errors.
