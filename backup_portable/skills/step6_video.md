# 6단계: 영상 프롬프트 → PC 생성 → 프레임 검수 → 쓸 구간

**규칙:** `../04_video_rules.md` (all of it). **Muse video generation needs user approval. Flow video costs money and is made only on the user's instruction.**

## 클라우드: 프롬프트
1. Copy `episodes/ep08/video/make_vprompts_v1.py`.
   - `S` = (id, sentence, move, action, camera). `PICK` = the confirmed first-frame image for each id.
   - Principle videos: `LOCK` + **the "Every solid object stays completely still … Only light, colour and glowing arrows change." sentence** + light and arrows only.
   - Camera moves on about 2/10 of clips. The rest use `LOCK`. Every clip gets the `LIGHT` brightness phrase. Suffix = realistic `REAL` or 3D `D3`.
2. Running it produces `vprompts_v1.json`: `id`, `image`, `script`, `move`, `prompt`, `save`.
3. After the user approves ("시작" and so on), write the PC work order. Record the approval date at the top.
   - **Order:** one at a time, in JSON order.
   - **Settings:** image-to-video, 16:9, the longest length. Record the actual length and resolution once.
   - **Retake only when** the scene differs, realistic/3D is swapped, text or a watermark appears, it goes dark, or the camera spins. At most 2 retakes.
   - **Refused:** retry once; if still refused, write "거부". Never generate from text only.
   - **Send:** copy `clips_v1\*.mp4` to `episodes/epNN/video/v1/` and push once. Write the report to `video/muse_vN_pc_report.md`.

## 클라우드: 검수
1. `git pull` → copy to scratch → `git rm -r episodes/epNN/video/v1` → push.
2. Run `python3 episodes/epNN/video/cloud_review_clips_v1.py <scratch>/out <scratch>/src` → brightness table + 1 s frame sheets.
3. Look at every sheet: shape changes, principle direction, exaggerated motion, camera, darkening, text.
4. In `video/review_clips_v1.md`, record each id: pass and usable range / fail with cause → new method.
5. **For failures, change the method:**
   - First rewrite with light and arrows.
   - If it still fails, suggest Flow video (paid, needs user instruction) or a composite made in the cloud (free; the V09 crack-fill example).
6. Once confirmed, copy the measured ranges into the plan `USE` → create `plan_v(N+1).py` → automatic-check errors must be 0.

## 완료 기준
- Every clip is confirmed, the plan reflects the measured usable ranges, and the errors are 0.
