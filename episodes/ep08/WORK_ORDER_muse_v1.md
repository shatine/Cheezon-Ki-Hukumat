# 8편 작업 지시서: Muse 영상 24개 생성 → push (사용자 허락 2026-10-25)

**Purpose:** generate the 24 episode-8 video clips in Muse and send them to the cloud for review.
- **The user has approved Muse video generation** (2026-10-25, the "시작" reply). This work order allows Muse generation, so do not ask again.
- **PC: generate and save only. The cloud does the strict review.** Make the whole list in one go, then push once.
- If the limit hits, push what is finished and carry on in a new session.

## 0. 먼저 읽기 (짧게)
1. `D:\youtube\Cheezon-Ki-Hukumat\guidelines\CLAUDE.md` (상시 허락)
2. This work order
3. `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\video\vprompts_v1.json`: 24 clips, each with `id`, `image` (first frame), `prompt` and `save`.
- The skill folder is needed only if you have not read it before. `references\prompts.md` has the video section.

## 경로
| 이름 | 경로 |
|---|---|
| First-frame images | `D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\img\` (the `image` filename from the JSON) |
| Where to save clips (permanent) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\clips_v1\{id}.mp4` |
| Folder for sending to the cloud | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\video\v1\{id}.mp4` |

## 1단계: 동기화와 준비
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main
New-Item -ItemType Directory -Force "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\clips_v1" | Out-Null
Test-Path "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\img\v1_V14_1.png"
```
- If the last line is `False`, copy `img\v1_v14_2.png` to `img\v1_V14_1.png` first. It is V14's first frame.

## 2단계: Muse 생성 (24개, JSON 순서대로)
- **Tool:** Muse (Chrome 9227). **One at a time:** submit → wait for it to finish (one check after 30–60 s) → download → next. No rapid repeated clicks (bot detection).
- **Settings:** image to video, 16:9, the longest length (normally 10 s).
  - Write the actual length and resolution once in the report. In episode 7 it was 10 s at 1216x672.
- **Input for each clip:**
  1. First frame = `img\{image}`, exactly the `image` value in the JSON. Example: V02 uses `v1_V02_6.png`.
  2. Prompt = the `prompt` value in the JSON, pasted **as it is** (do not edit).
- **Save:** `clips_v1\{id}.mp4`. If you retry, keep only the last attempt under the same name.
- **간단 확인 (one look):** play it once. Retry right away **only** in these cases (at most 2 retries per clip):
  - it is a different scene from the first frame;
  - realistic and 3D are swapped;
  - large text or a watermark appears;
  - it turns dark;
  - the camera spins (only o02, o03, v12 and v23 move; everything else is a fixed camera).
  - Leave the finer checks (frames, brightness, principle direction) to the cloud.
- **If Muse refuses the first frame** (an image upload error or rejection):
  - Try once more with the same image.
  - If it still fails, **do not generate from the text alone**. In episode 7 that made the bus look different. Note "거부" for that id in the report and move on.
- **Do not change the order:** o01, o02, V02, o03, V04, V05, V06, V07a, V07b, V09, V10a, V10b, v12, V13, v14, V14, V16a, V16b, V17, V18, V20a, V20b, V22, v23

## 3단계: 클라우드로 보내기 (한 번에)
```powershell
$src  = "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\clips_v1"
$repo = "D:\youtube\Cheezon-Ki-Hukumat"
$dst  = "$repo\episodes\ep08\video\v1"
git -C $repo pull origin main
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item "$src\*.mp4" $dst
Write-Host "복사:" (Get-ChildItem $dst -Filter *.mp4).Count "개"
git -C $repo add episodes/ep08/video/v1
git -C $repo commit -m "EP8: Muse clips v1 for cloud review"
git -C $repo push origin main
```
- If the push is rejected (fetch first): run `git -C $repo pull --no-rebase origin main`, then push again.
- If a single file exceeds 100 MB, GitHub rejects it. Write its size in the report and leave it out.
- The cloud removes `video\v1\` from git after downloading. The originals stay in `clips_v1\`.

## 4단계: 보고
- The count made (out of 24), the actual clip length and resolution, the ids that were retried, and any ids Muse refused.
- Whether the push succeeded (`main -> main`).

## 금지
- Changing the script, numbers, order or prompts.
- Using a first frame other than the one in the JSON.
- Generating from text only.
- Several submissions in a row.
- Editing `.claude\skills` directly.
