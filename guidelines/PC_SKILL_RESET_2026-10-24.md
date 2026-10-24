# PC를 깃(main)에 맞추기: 실행 계획 (2026-10-24 개정)

The PC currently has no `cheezon-production` and still has 14 old skills, so nothing has been applied yet.
This plan makes **git the single source of truth**. From now on, running one script keeps the PC up to date.

## 준비물 위치
- Repository clone: `D:\youtube\Cheezon-Ki-Hukumat`
- Channel folder: `D:\youtube\7. Cheezon Ki Hukumat`
- Sync script: `D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1`

## 1단계: TTS 파일 2개를 먼저 깃에 올리기 (딱 한 번)
The sync makes the skill folder **identical** to git. Files that are not in git (`tts_vs.py`, `junk_check.py`) would be wiped, so put them into git first.
```powershell
cd "D:\youtube\Cheezon-Ki-Hukumat"
git checkout -- .
git pull origin main
Copy-Item "D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\tts_vs.py"   "D:\youtube\Cheezon-Ki-Hukumat\skills\cheezon-production\tools\tts_vs.py"
Copy-Item "D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\junk_check.py" "D:\youtube\Cheezon-Ki-Hukumat\skills\cheezon-production\tools\junk_check.py"
Select-String -Path "D:\youtube\Cheezon-Ki-Hukumat\skills\cheezon-production\tools\tts_vs.py" -Pattern '\.wav|\.json|\.txt|Path\(' | Select-Object LineNumber, Line
```
- If the last command shows other files that `tts_vs.py` reads (a voice reference wav, a ref_text file and so on), copy each into the same `tools` folder too.
- Ask a PC session: "tts_vs.py가 tools 폴더 안 파일만 쓰도록 경로를 고쳐줘."

Then commit:
```powershell
git add skills/cheezon-production/tools
git commit -m "cheezon-production: add TTS dependencies (tts_vs.py, junk_check.py)"
git push origin main
```

## 2단계: 미리보기 (아무것도 안 바꿈)
```powershell
powershell -ExecutionPolicy Bypass -File "D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1"
```
Check the output:
- In step 2, only the 14 old skills are marked "삭제".
- In step 4, only the old copy and lesson folders are marked "삭제".

## 3단계: 실제 실행
```powershell
powershell -ExecutionPolicy Bypass -File "D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1" -Apply
```
What the script does:
1. `git pull`.
2. Makes `D:\youtube\7. Cheezon Ki Hukumat\.claude\skills` identical to `skills/` in git.
   - The 14 old skills are deleted and `cheezon-production` is added.
3. Replaces `CLAUDE.md` and `CHANNEL.md` in the channel folder.
4. Deletes the old skill copies and lesson folders:
   - `skills_copy`, `스킬_원문`, `skill_upgrade`
   - The three Codex skills.

Check the final output:
- `.claude\skills` contains only `cheezon-production`.
- `tts_vs.py` and `junk_check.py` are listed as "있음".
- If an `AGENTS.md` turns up, open it. If it points to old skills, change it to "`.claude\skills\cheezon-production`을 따른다" or delete it.
- If `C:\Users\developer1\.codex\skills` gives an access error, delete it in File Explorer instead.

## 4단계: 확인
1. Fully quit the Claude desktop app and start it again.
2. Open a new **local (this computer)** session with the folder `D:\youtube\7. Cheezon Ki Hukumat`.
3. Ask: "cheezon-production 스킬을 읽고 공정 단계와 7편 실수 목록을 요약해."
   - It must not mention old skill names such as cheezon-video or video-camera.

## 앞으로 (계속 최신 유지)
- **When to sync:** whenever the cloud changes a skill or guideline, and **before starting work on the PC**, run the step 3 command once more. It pulls and mirrors in one go.
- **Changing a skill on the PC:** edit it in the repository (`D:\youtube\Cheezon-Ki-Hukumat\skills\...`), commit and push, then sync.
  - Do not edit `.claude\skills` directly. The next sync overwrites it.

## 수정 (2026-10-25)
- **동기화 스크립트가 더 이상 로컬 변경을 지우지 않는다.**
  - The old version ran `git checkout -- .` and reverted EP7 changes that had not been committed (`plan_v9.py`, `shot_list_v9.json`).
  - It now **stops** if there are uncommitted changes, and lists them. Commit and push first, then sync.
- **TTS 파일:** `skills/cheezon-production/tools/` now holds all of them (982544a):
  - `tts_vs.py`, `junk_check.py`, `asr_check.py`, `fw_local.py`, `voice_ref_male_charonclone.wav`, `ref_text.txt`
