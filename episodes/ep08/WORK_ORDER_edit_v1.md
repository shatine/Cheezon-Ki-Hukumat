# 8편 작업 지시서: 편집 검수본 v1 렌더 → push (2026-10-26)

**Purpose:** render the episode-8 review cut (Hindi and Korean subtitles, narration only) and send it to the cloud for review.
- After the cloud reviews it from 0 s to the end, an upload version (one line of Hindi subtitles, background music, -14 LUFS) follows in a separate work order.
- **Nothing here costs money.** Only local rendering. Follow the 상시 허락 in `CLAUDE.md` and do not ask.

## 0. 먼저 읽기 (짧게)
1. `D:\youtube\Cheezon-Ki-Hukumat\guidelines\CLAUDE.md` (상시 허락)
2. This work order
- The scripts are already written by the cloud. **Do not edit them.** If something breaks, report the error message as it is.

## 경로
| 이름 | 경로 |
|---|---|
| Repository (scripts and plan) | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\` |
| Edit script | `...\ep08\review_edit\edit_v1.py`, which reads `...\ep08\plan\shot_list_v2.json` |
| Media folder (CB) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\` |
| Narration | `CB\review_edit\narration_hi.wav`, `CB\review_edit\narr\{id}.wav` (the step 1 TTS result) |
| Clips and images | `CB\clips_v1\*.mp4`, `CB\img\v1_*.png` |
| Output | `CB\out\v1_review_hi.mp4` (original), `CB\out\v1_review_small.mp4` (for the cloud) |

## 1단계: 동기화와 확인
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main
$CB = "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge"
Test-Path "$CB\review_edit\narration_hi.wav"; (Get-ChildItem "$CB\review_edit\narr" -Filter *.wav).Count
Test-Path "$CB\clips_v1\v14_real.mp4"; Test-Path "$CB\img\v1_V02_6.png"
python -c "import numpy, soundfile, PIL; print('ok')"
```
- **Expected:** True, 70 (number of TTS lines), True, True, ok.
- If the module check fails: `pip install numpy soundfile pillow`.
- If `narr` has fewer than 70 files, check the line-by-line wav from the step 1 TTS.
- Check the files the clips need. `V09.mp4`, `V20b.mp4` and `V05.mp4` must be the latest **Flow** versions. The earlier Muse versions are in `old\`.

## 2단계: V09 시멘트 합성 (클라우드가 만든 마스크 사용)
```powershell
python "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\review_edit\v09_fill.py" "$CB\clips_v1\V09.mp4" "$CB\clips_v1\V09_fill.mp4"
```
- **Pass:** the last line is `frames 240 -> ...V09_fill.mp4`. When played, the cracks turn grey one by one from the pipe tip outward.

## 3단계: 렌더 (한 번에)
```powershell
cd "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\review_edit"
python edit_v1.py
```
- **This takes some time** (72 cuts at 1920x1080). One line is printed per cut.
- **Pass:** the report at the end shows `total_sec` of about 335.3, and a line starting `small:` (the file size in MB).
- **If it stops:**
  - `없음` or `짧음` + `소스 문제 → 렌더 중단`: a source file is missing or too short. Report the printed list as it is.
  - Any other error (for example, the font path in the V02 `drawtext` line): report the last 20 lines of output as they are. **Do not edit the script.** The cloud fixes it.
- Automatic options (the PC does nothing):
  - Watermark removal on the Flow clips.
  - Gradual brightness correction on v12.
  - Brightness correction on i23b and i24.
  - Blur on the i19a2 nameplate and the i20a number plate.
  - The numbers "359 m" and "×5" on V02.

## 4단계: 클라우드로 보내기
```powershell
$repo = "D:\youtube\Cheezon-Ki-Hukumat"
$dst  = "$repo\episodes\ep08\review_edit\v1"
git -C $repo pull origin main
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item "$CB\out\v1_review_small.mp4" $dst
(Get-Item "$dst\v1_review_small.mp4").Length / 1MB
git -C $repo add episodes/ep08/review_edit
git -C $repo commit -m "EP8: review cut v1 (small) + subtitles and edit report"
git -C $repo push origin main
```
- If the size exceeds 95 MB, report it without pushing.
- `subs_hi.srt`, `subs_ko.srt`, `subs.ass`, `cuts_v1.json` and `edit_report_v1.json` are generated in the repository's `review_edit\` and are pushed together.
- If the push is rejected, run `git -C $repo pull --no-rebase origin main` and push again.

## 5단계: 보고
- The contents of `edit_report_v1.json`, which include the total length, the number of cuts and the subtitle counts.
- Whether the push succeeded.
- The user should watch `CB\out\v1_review_hi.mp4` from start to end. The cloud reviews the frames and the subtitle timing.
