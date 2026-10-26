# 8편 작업 지시서: 업로드본 v1 렌더 → push (2026-10-26)

**Purpose:** render the episode-8 YouTube upload version.
- One line of Hindi subtitles, background music with ducking, -14 LUFS.
- It is the same method as episode 7 (`edit_v9_upload.py`).
- **Nothing here costs money.** Local rendering only. Follow the 상시 허락 in `CLAUDE.md` and do not ask.
- **Cloud review v1** (`episodes\ep08\review_edit\review_v1.md`) passed the review cut, with one fix: the V02 label timing. The script already carries that fix.

## 0. 먼저 읽기 (짧게)
1. `D:\youtube\Cheezon-Ki-Hukumat\guidelines\CLAUDE.md` (상시 허락)
2. This work order
- **Do not edit the script.** If something breaks, report the last 20 lines of output as they are.

## 1단계: 동기화와 확인
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main
$CB = "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge"
Test-Path "D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\music\bgm.mp3"
(Get-ChildItem "$CB\out\v1_hi_seg" -Filter *.mp4).Count
Select-String -Path "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\review_edit\edit_v1.py" -Pattern '"×5", 1185, 430, 5.1'
```
- **Expected:** `True`, then `72`, then one matching line.
- If the third command prints nothing, the pull did not work. Pull again.
- If the background music file is `False`, set its path before step 2: `$env:BGM = "<bgm.mp3 경로>"`. This is the same music as episodes 6 and 7.

## 2단계: 업로드본 렌더
```powershell
cd "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\review_edit"
python edit_v1.py --upload
```
- **Speed:** the 71 review-cut segments are reused. Only V02 is rendered again, because of the labels. So it is much faster than the review cut.
- **Pass:** the report at the end shows:
  - `total_sec` of about 335.3;
  - `lufs` between -14.5 and -13.5;
  - `true_peak_dbfs` of -1.5 or lower;
  - a `small:` line.
- **Outputs:**
  - `CB\out\v1_upload_hi.mp4`: the file to upload, 1920x1080.
  - `CB\out\v1_upload_subs_hi.srt`: subtitles to attach on YouTube if needed.
  - `CB\out\v1_upload_small.mp4`: for the cloud check.

## 3단계: 클라우드로 보내기
```powershell
$repo = "D:\youtube\Cheezon-Ki-Hukumat"
$dst  = "$repo\episodes\ep08\review_edit\v1"
git -C $repo pull origin main
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item "$CB\out\v1_upload_small.mp4" $dst
(Get-Item "$dst\v1_upload_small.mp4").Length / 1MB
git -C $repo add episodes/ep08/review_edit
git -C $repo commit -m "EP8: upload cut v1 (small) + upload subtitles and report"
git -C $repo push origin main
```
- If the size exceeds 95 MB, report it without pushing.
- `subs_upload.ass` and `edit_report_v1_upload.json` are generated in the repository's `review_edit\` and are pushed together.
- If the push is rejected, run `git -C $repo pull --no-rebase origin main` and push again. Check that the last line shows `main -> main`.

## 4단계: 보고
- The contents of `edit_report_v1_upload.json`.
- Whether the push succeeded (`main -> main`).
- **Do not upload to YouTube yet.** The cloud first checks the sound and the V02 labels, then writes the upload text (titles, descriptions, keywords).
