# 8편 작업 지시서: Muse 영상 다시 만들기 6개 → push (2026-10-26)

- **허락:** Muse generation was approved by the user on 2026-10-25. This is a remake of the same 24 clips, so do not ask again.
- **PC: generate and save only. The cloud does the strict review.** Make all 6 in one go, then push once.
- **Reason:** `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\video\review_clips_v1.md` (cloud review). The other 18 clips are final; do not touch them.

## 1. 준비
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main
```
- In `episodes\ep08\video\vprompts_v1.json`, use only the 6 clips where **`retake_v2` is `true`**: V09, V16a, V16b, V20a, V20b, v23.
- The prompts have changed. Paste each clip's `prompt` **as it is**. The first frame is the `image` filename (in `08_chenab_bridge\img\`).

## 2. 생성 (Muse 9227, one at a time, a new side chat for each)
- A retry in the same chat can return the old clip as it is. Make each clip in **a new side chat**.
- **Save:** move the old file to `clips_v1\old\{id}.mp4` (keep it, do not delete), then save the new clip as `clips_v1\{id}.mp4`.
- **간단 확인 (one look; at most 2 retries per clip):**
  | id | 확인할 것 |
  |---|---|
  | V09 | Cement does not flow out of the block onto the table |
  | V16a | The deck pieces do not lift into the air |
  | V16b | The terrain does not melt and change shape |
  | V20a | The bridge does not ripple and collapse |
  | V20b | The rails do not disappear |
  | v23 | There is no scene cut in the middle, and the bridge stays in the centre |
- If Muse refuses, try once more. If it still refuses, do not make it from text only. Report it and move on. Making it in Flow (which costs credits) needs the user's instruction.

## 3. 보내기
```powershell
$src  = "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\clips_v1"
$repo = "D:\youtube\Cheezon-Ki-Hukumat"
$dst  = "$repo\episodes\ep08\video\v1"
git -C $repo pull origin main
New-Item -ItemType Directory -Force $dst | Out-Null
foreach ($i in "V09","V16a","V16b","V20a","V20b","v23") { Copy-Item "$src\$i.mp4" $dst }
git -C $repo add episodes/ep08/video/v1
git -C $repo commit -m "EP8: Muse retakes v2 (6) for cloud review"
git -C $repo push origin main
```
- If the push is rejected, run `git -C $repo pull --no-rebase origin main` and push again.

## 4. 보고
- The count made (out of 6), the retried ids and the reason for each retry, any ids Muse refused, and whether the push succeeded.
