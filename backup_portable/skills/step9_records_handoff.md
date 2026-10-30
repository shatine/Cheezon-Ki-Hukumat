# 9단계: 기록, git 백업, 검수 보고, HANDOFF (매 단계 끝에)

Every step ends with the same three things: **records → report → HANDOFF**, then a git backup of the text files.

## 단계별 기록 파일
| 단계 | 기록 |
|---|---|
| 1 | `hook_thumbnail.md` (opening line candidates → confirmed, thumbnail drafts → confirmed), `topic_candidates.md`, `refs_analysis.md` |
| 2 | `script/script_ko_final.md` (with the evidence table) |
| 3 | `script/lines_hi_ko.tsv`, `review_edit/narr_timing.json`, `narr_check.json` |
| 4 | `plan/plan_vN.py`, `shot_table_vN.md` ("점검: 통과") |
| 5 | `images/prompts_v1.json`, `picks_v1.md` (one section per review round) |
| 6 | `video/vprompts_v1.json`, `muse_vN_report.md`, `review_clips_v1.md` |
| 7 | `review_edit/edit_report_*.json`, `review_v1.md` |
| 8 | `upload/*`, `thumbnail/make_thumb_vN.py`, `thumb_vN_1280x720.jpg` |

## git 백업 (텍스트만)
```
cd D:\youtube\Cheezon-Ki-Hukumat
git add episodes\epNN
git status          # 미디어(png/jpg 배경/mp4/wav)가 없는지 확인. 있으면 빼고 .gitignore에 추가
git commit -m "epNN: <단계> <무엇>"
git push origin main
```
- If the push is rejected: `git pull --no-rebase origin main`, then push again. Check the last line says `main -> main`.
- Only the final thumbnail JPG (under 2 MB) may be committed. Backgrounds and all other media stay in CB.

## 검수 보고 형식 (사용자에게, 한국어)
- **First line:** the verdict (pass / N fixes / N remakes).
- **Table:** item | result, with the key numbers.
- **What was fixed:** before → after.
- **Left as is:** with the reason.
- **What happens next.**
- Keep what was seen by eye separate from what was measured automatically. Do not claim to have reviewed what you have not looked at.
- When the user has to do something (approve Muse, listen to TTS, upload), give full paths and steps in order.

## HANDOFF 갱신 (매 단계)
- **Confirmed items at the top:** the opening line, the thumbnail (file path), the title direction, the script, the number rules.
- Status table: step | state | result (file paths).
- User approvals: date and words (Muse batches, Flow video, paid items).
- "다음 세션이 할 일": exactly where to pick up if the session ends.
- The user's preferences.
- Once a new version is confirmed, delete the one it replaced (git history keeps it).
