# 8편 작업 지시서: Muse 영상 다시 만들기 v3, 4개 → push (2026-10-26)

- **허락:** a remake of clips already approved (2026-10-25). Do not ask again.
- **PC: generate and save only. The cloud does the strict review.** Make all 4 in one go, then push once.
- **Why:** see "다시 만든 v2 6개 검수" in `episodes\ep08\video\review_clips_v1.md`.
  - V20a and v23 passed. Keep the v2 versions now in `clips_v1\`.
- **The prompts have changed completely.** Objects now stay still, and only light and arrows move.

## 1. 준비
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main
```
- In `episodes\ep08\video\vprompts_v1.json`, use only the 4 clips where **`retake_v3` is `true`**: V09, V16a, V16b, V20b.
- Paste each `prompt` **as it is**. The first frame is the `image` filename (in `08_chenab_bridge\img\`).

## 2. 생성 (Muse 9227, one at a time, a new side chat for each)
- **Save:** move the current file to `clips_v1\old\{id}_v2.mp4`, then save the new clip as `clips_v1\{id}.mp4`.
- **간단 확인 (one look; at most 2 retries per clip):** the object's shape and position stay the same, and only light and arrows move. If something moves, melts, disappears or leaks, retry.
- If Muse refuses, try once more. If it still refuses, report it. Do not make it from text only, and do not make it in Flow (which costs credits).

## 3. 보내기
```powershell
$src  = "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\clips_v1"
$repo = "D:\youtube\Cheezon-Ki-Hukumat"
$dst  = "$repo\episodes\ep08\video\v1"
git -C $repo pull origin main
New-Item -ItemType Directory -Force $dst | Out-Null
foreach ($i in "V09","V16a","V16b","V20b") { Copy-Item "$src\$i.mp4" $dst }
git -C $repo add episodes/ep08/video/v1
git -C $repo commit -m "EP8: Muse retakes v3 (4) for cloud review"
git -C $repo push origin main
```
- If the push is rejected, run `git -C $repo pull --no-rebase origin main` and push again.

## 4. 보고
- Write it in `episodes\ep08\video\muse_v3_pc_report.md` and push it together with the clips: the count made, retries and reasons, and any ids Muse refused.
