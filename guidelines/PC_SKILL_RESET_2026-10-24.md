# PC 스킬 정리 — 이전 것 전부 삭제, 7편(폐버스) 것만 남기기 (2026-10-24)

The GitHub repository already has only `skills/cheezon-production/` left. These are the steps to make the PC the same.
Run them in Windows **PowerShell**, in order. **Steps 1–3 must come before the deletion in step 4.** If you delete first, Hindi TTS stops working.

Paths used below:
- Channel folder: `D:\youtube\7. Cheezon Ki Hukumat`
- Episode 7 working folder: `D:\youtube\7. Cheezon Ki Hukumat\폐버스가집이 될수없는 이유`
- Local copy of the GitHub repository: `D:\youtube\Cheezon-Ki-Hukumat` (if you already have a clone somewhere else, swap in that path)

## 1단계: 저장소 최신으로 받기
```powershell
if (Test-Path "D:\youtube\Cheezon-Ki-Hukumat\.git") { git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main } else { git clone https://github.com/shatine/Cheezon-Ki-Hukumat.git "D:\youtube\Cheezon-Ki-Hukumat" }
Get-ChildItem "D:\youtube\Cheezon-Ki-Hukumat\skills"
```
The listing must show only the `cheezon-production` folder.

## 2단계: 새 스킬 복사
```powershell
New-Item -ItemType Directory -Force "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills" | Out-Null
Copy-Item -Recurse -Force "D:\youtube\Cheezon-Ki-Hukumat\skills\cheezon-production" "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production"
```

## 3단계: TTS가 쓰는 파일 2개를 새 스킬로 옮기기 (삭제 전에 꼭)
Episode 7's TTS (`tts_template.py`) reads two files from the episode 5 folder.
```powershell
Copy-Item "D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\tts_vs.py" "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools\tts_vs.py"
Copy-Item "D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\junk_check.py" "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools\junk_check.py"
Select-String -Path "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools\tts_vs.py" -Pattern '\.wav|\.json|\.txt|Path\(' | Select-Object LineNumber, Line
```
If the last command shows other files that `tts_vs.py` reads (a voice reference wav, a ref_text file and so on), copy each of them into the same `tools` folder too. Then ask a PC session: "tts_vs.py가 tools 폴더 안 파일만 쓰도록 경로를 고쳐줘."

## 4단계: 이전 스킬·교훈 삭제
First list everything to be deleted with the command below and check it. If it looks right, run the deletion block.
```powershell
$old = @(
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\channel-setup",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\channel-video-style",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-claude-review",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-script",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-video",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\encyclopedia-script",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\encyclopedia-video",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\episode-pipeline",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-camera",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-edit",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-screen",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-sound",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-story",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-text",
  "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\video-verify",
  "D:\youtube\7. Cheezon Ki Hukumat\폐버스가집이 될수없는 이유\skills_copy",
  "D:\youtube\7. Cheezon Ki Hukumat\폐버스가집이 될수없는 이유\제작_인계가이드\스킬_원문",
  "D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge_CODEX\outputs\channel_benchmark_20261015\skill_upgrade",
  "C:\Users\developer1\.codex\skills\cheezon-video",
  "C:\Users\developer1\.codex\skills\cheezon-script",
  "C:\Users\developer1\.codex\skills\cheezon-claude-review"
)
$old | ForEach-Object { "{0}  {1}" -f (Test-Path $_), $_ }
Get-ChildItem "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills"
```
- Anything in the `.claude\skills` listing other than `cheezon-production` that is **not in the list above** is also an old skill. Add it to `$old`.
- If it shows False, the folder is already gone. Leave it.
- `C:\Users\developer1\.codex\skills` was previously blocked from being opened. If it still gives an error, delete it in File Explorer instead.

Deletion:
```powershell
$old | Where-Object { Test-Path $_ } | ForEach-Object { Remove-Item -Recurse -Force $_ }
Get-ChildItem "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills"
```
Only `cheezon-production` should remain.

## 5단계: 채널 지침 파일 교체
```powershell
Copy-Item -Force "D:\youtube\Cheezon-Ki-Hukumat\guidelines\CLAUDE.md" "D:\youtube\7. Cheezon Ki Hukumat\CLAUDE.md"
Copy-Item -Force "D:\youtube\Cheezon-Ki-Hukumat\guidelines\CHANNEL.md" "D:\youtube\7. Cheezon Ki Hukumat\CHANNEL.md"
Get-ChildItem "D:\youtube\7. Cheezon Ki Hukumat" -Filter "AGENTS.md" -Recurse -Depth 2 | Select-Object FullName
```
- The last command finds `AGENTS.md`, the Codex instruction file.
- If it points to old skills, open it and change the contents to "새 편 제작은 `.claude\skills\cheezon-production`을 따른다", or delete it.
- The `AGENTS.md` in the episode 7 working folder is also covered by this.

## 6단계: 확인
1. Fully quit the Claude desktop app and start it again. That reloads the skills.
2. Open a new **local (this computer)** session with the folder `D:\youtube\7. Cheezon Ki Hukumat`.
3. Ask: "cheezon-production 스킬을 읽고 공정 9단계와 7편 실수 목록을 요약해."
   - Check that it summarises from the new skill only.
   - It must not mention old skill names such as cheezon-video or video-camera.

## 남기는 것 (지우지 않음)
- Episode 7 working folder: `D:\youtube\7. Cheezon Ki Hukumat\폐버스가집이 될수없는 이유\`, everything except `skills_copy` and `제작_인계가이드\스킬_원문`.
  - This includes the images, videos, narration and `ep07_img3d\flow_recv.py`.
- Folders for already-published episodes, e.g. `D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\`.
  - Only the `tts_vs.py` and `junk_check.py` there are used by the new skill; they were copied in step 3.
  - Whether to delete the rest of each episode's videos is a separate decision.
