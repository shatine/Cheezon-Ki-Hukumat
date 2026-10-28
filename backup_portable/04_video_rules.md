# 04. 영상 생성·검수 규칙 (Muse / Flow 영상)

## 1. 언제 영상인가 (계획 기준)
- **Principle sentences must be video.** Examples: forces, flows, heat, wind, the order of construction.
- **Non-principle shots:** only **10–20%** are video. Use them for camera moves, or where people or vehicles moving is the point. Episode 8: 13.8%.
- **The 30 s opening:** **3–5** long, natural videos (5–10 s each). No 1 s montages.
- Everything else is images with effects: slow zoom in or out, alternating with left, centre and right pans.

## 2. 생성 설정
- **Muse (default):** Chrome on debug port 9227.
  - Image-to-video, 16:9, the longest length. Episode 8: 10.0 s, 1216×672, 24 fps.
  - **Generate only with user approval.** Record the approval (date and the user's words) in HANDOFF.
- **Flow video (exception):** Omni 1.1 Flash, 1280×720, **15 credits each (paid)**.
  - **Only on the user's instruction.** Use it when Muse keeps failing.
  - There is a star watermark at the bottom right. Remove it in editing: `delogo=x=1132:y=572:w=58:h=58`, plan option `flow_wm`.
- **One clip at a time:** submit → wait 30–60 s and check once → download → next.
- **First frame:** exactly the `image` from the JSON, an image confirmed in the strict image review.
  - If Muse refuses the image, retry once with the same image. If it still refuses, **do not generate from text alone**. Write "거부" in the report.
- **Save:** `CB\clips_v1\{id}.mp4`. If you retry, keep only the last attempt.
  - Earlier versions go to `clips_v1\old\`.

## 3. 프롬프트 틀 (`video/make_vprompts_v1.py` → `vprompts_v1.json`)
`[scene action]. [camera tag]. Movement: … Speed: … Framing: … End: …` + brightness phrase + suffix.

**Fixed camera (default; principle videos always use it)**
```
[locked-off static shot]. Movement: camera completely still, no zoom, no pan. Speed: none. Framing: exactly the composition of the image. End: same frame.
```
**Brightness phrase (every clip)**
```
The lighting stays the same bright light for the whole shot, no darkening, no fade.
```
**Realistic suffix**
```
Photorealistic, bright midday daylight, vivid colours. Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark.
```
**3D suffix**
```
Clean bright 3D educational render, white-grey studio background. Keep the exact same [subject], shape, colours and layout as the image. No new objects, no text, no labels. Ambient sound only. No dialogue, no music, no watermark.
```

### ★ 8편 핵심 교훈: Muse는 동작 동사를 과장한다
- "Slides, flows into, shakes, expands, fills" and the like are **exaggerated a lot**.
  - Cement spilled over and covered the block.
  - The deck lifted off its bearings.
  - The bridge tipped like a see-saw.
  - A rail disappeared.
  - Retrying the same prompt failed the same way every time.
- On the other hand, **every clip where the objects stayed still and only light and arrows moved passed.** Write principle videos like this from the start:
```
Every solid object stays completely still and keeps its exact shape and position for the whole shot: nothing slides, lifts, tilts, melts, disappears or leaks. Only light, colour and glowing arrows change.
```
- **Show the principle with light, colour and arrows:**
  | 원리 | 보여 주는 방법 (8편) |
  |---|---|
  | Bearings can move | Blue arrows on the deck blink left and right; the bearings glow blue |
  | Bearings absorb shaking | White shake lines blink at the base; the bearings on each pier glow in turn |
  | Rails can slide | The rails stay put; orange arrows beside the rails blink towards the joint |
  | The arch pushes on the mountain | Orange arrows run along the arch into the rock |
  | Heat | Only the side the sun hits turns red |
- **If it still fails, use a local composite instead.** Episode 8 V09 "cement fills the cracks":
  - A crack-only mask was made from frame 0 of a still clip (`v09_crack_mask.png`).
  - `v09_fill.py` paints the cracks grey from the pipe tip outward.
  - This is free and its result is certain.

## 4. 카메라 규칙
- **Only about 2/10 of video clips have camera moves.** Episode 8: 4 of 24 (o02 tilt up, o03 drone forward, v12 slider, v23 drone pull back).
- **One move per clip**, very slow, ending on a still composition.
- Do not use the same direction of move twice in a row.
- **Do not dolly in towards people.** Faces get large.
  - Episode 7 o1: the camera pushed in fast after 5 s, so only 0–5.4 s was usable.
- **Never use the phrase "One single continuous camera movement…".** It causes motion sickness.
- **Moves to use:**
  - slow dolly in;
  - slider left/right;
  - drone pull back (endings);
  - tilt up (reveal);
  - macro slow zoom in.

## 5. 검수 (생성 목록을 다 만든 뒤, 같은 세션에서)
**Preparation:** `python episodes\epNN\video\cloud_review_clips_v1.py "CB\review\clips_vN" "CB\clips_v1"` (full paths). It produces:
- a table: size, fps, length, **mean brightness every 0.5 s**, first-to-last change (a fall of 15 or more is flagged **어두워짐**);
- a sheet of frames every **1 s** for each clip.

**Look at every sheet frame by frame:**
| 항목 | 탈락 / 구간 제한 |
|---|---|
| Shape | The subject changes shape, or parts appear or disappear (a rail vanishing, a deck lifting) |
| Principle direction | Arrows or flows in the wrong direction, exaggerated motion (overflow, collapse) |
| Camera | Spinning, a sudden push-in, a face growing large |
| Brightness | Going dark → use only up to that point, or correct it in the edit (`bright`) |
| Text | Text or a watermark appears |
| Consistency | Different from the first frame (realistic/3D swapped, colours changed) |

- **Usable range (USE):** the measured range you can use, for example `V20a 0–7.0` or `V16b 0–8.5`.
  - **The end must be at or before length − 0.05 s** (episode 8 `CEND = 9.95`).
- **Record:** `video/review_clips_v1.md`, one row per id: result, usable range, note. Write the cause and the new method too.
- **Remakes:** set the `retake_vN` flag on those ids in `make_vprompts_v1.py`, run it again, and regenerate those ids only (Muse approval covers the remakes of an approved batch; ask again for new ids).
  - Episode 8 went through v1 → v2 (6 clips) → v3 (4 clips), with 2 made in Flow video and 1 composite.
- **Flow clips** are 1280×720, so the edit scales them to 1920×1080. Keep the watermark-removal option.
- **Cost record:** write the paid Flow clips in the review file, for example "Flow 영상 3개 × 15크레딧 = 45크레딧 (사용자 지시)".
