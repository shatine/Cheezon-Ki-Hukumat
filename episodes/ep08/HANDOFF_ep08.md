# 8편 인계: 체납 철교 (2026-10-25, 클라우드 세션 종료 시점)

The new cloud session reads this file first.
- Then it reads `guidelines/CLAUDE.md` (including the **상시 허락** section) and all of `skills/cheezon-production/`.
- Work on the cloud and PC, and on credits, uses the rules in those files.

## 채널·역할 요약
- **채널:** Cheezon Ki Hukumat, a Hindi explainer channel for Indian adults.
- **Conversation language:** Korean. Narration: Hindi.
- **Cloud session:** script, plan, prompts, review, upload text. The user wants **cloud session credits used first**.
- **PC session** (Claude desktop app, local, folder `D:\youtube\7. Cheezon Ki Hukumat`): Flow images, Muse videos, TTS, final render.
- **Exchange:** GitHub https://github.com/shatine/Cheezon-Ki-Hukumat `main`.
  - Media the PC uploads (images, videos) is downloaded by the cloud for review, then **removed from git right away** (space).
- **PC sync:** `guidelines/sync_pc.ps1 -Apply`. It keeps the PC's `.claude\skills` identical to git; skill = `cheezon-production` only.

## 8편 확정 사항
- **Topic:** Chenab Rail Bridge. Candidates and reasoning: `topic_candidates.md`.
- **Reference videos** (three with 1M+ views):
  - Views are in `opening_candidates.md`.
  - Transcripts are in `refs/*.txt`.
  - Analysis is in `refs_analysis.md`.
- **Opening line (confirmed by the user):** "지진이 오면 이 다리는 어떻게 될까? 359m 위 기차, 강바닥엔 기둥 하나 없다! 기둥 하나 못 세우는데, 다리는 어떻게 놓았나?"
- **Thumbnail text:**
  - Red: `भूकंप आया तो`
  - Yellow: `इस पुल का क्या होगा?`
  - Green: `359 मीटर` with a **vertical** arrow (height).
  - Draft: `thumbnail/thumb_v2_1280x720.jpg`. Prompts: `upload_thumbnail_prompt.md`. The user has not yet chosen a final version.
- **Script (confirmed, no changes):** `script/script_ko_final.md`, with evidence table.
  - Number rule: where sources disagree, use the **highest** figure. Government claims are attributed in the sentence.
  - The 90 km/h stop rule could not be confirmed, so it was removed. It was replaced with 120 sensors and a red signal plus alarm.
- **Hindi:** `script/lines_hi_ko.tsv`, 70 lines.

## PC 진행 상황 (작업 지시서 `WORK_ORDER_tts_to_images.md`)
| 단계 | 상태 | 결과 |
|---|---|---|
| 0 동기화 | 완료 | — |
| 1 TTS | 완료 | 334.3 s, 70 lines. `review_edit/narr_timing.json` (audio only on the PC) |
| 2 장면 계획 | 완료 | `plan/plan_v1.py` → 72 cuts, 0 errors. Video 24 cuts (principle 139.9 s), images 48 cuts (max 4.5 s), opening 4 videos, non-principle video share 13.8% |
| 3 이미지 프롬프트 | 완료 | `images/prompts_v1.json` (2 masters CB and G3D + 48 images + 24 video first frames) |
| 4 Flow 생성·검수 | **진행 중** | `images/picks_v1.md`, 33 of 74 ids. Cloud pre-checked the remaining 41 prompts and revised 6 (V02 retry, i15c, i19c, i19c2, i21, i24) |
| 5 영상 프롬프트 | 완료 | `video/vprompts_v1.json` (24 clips, not generated) |
| 6 클라우드 검수 | **2차 완료**: v1 41 pass + v2 16 pass = 57. Left: 7 remakes + 10 new (`picks_v1.md` 클라우드 검수 v2, top of `WORK_ORDER_flow_round2.md`) | — |

## 다음 클라우드 세션이 할 일
- PC work order for now: `WORK_ORDER_flow_round2.md` (11 remakes + 22 new). When the PC pushes to `images/v1/`, review with `cloud_review_v1.py` and at full size, then remove from git.
0. Review tool: `python3 episodes/ep08/images/cloud_review_v1.py <scratch dir>` copies `images/v1/*.png`, writes `auto_report.md` (size, brightness, neighbour similarity, missing ids) and contact sheets. Then `git rm -r episodes/ep08/images/v1`. Still look at every image at full size.
1. `git pull` → read this file, `WORK_ORDER_tts_to_images.md`, `images/picks_v1.md` and `plan/shot_table_v1.md`.
2. When the PC finishes step 4 and pushes the images:
   - Copy them to the scratchpad, then remove them from git.
   - Review every image at original size: same bridge and orientation, principle direction, faces, text, duplicates, brightness.
   - Add the results to `picks_v1.md`, and send the remake list to the PC.
3. Then: Muse video generation (PC) → edit and review → upload text (titles and descriptions in English and Hindi separately, keywords 8+8; 7편 example: `episodes/ep07_bus/upload/`).

## 사용자 성향 (반드시 지킬 것)
- Do not make the user answer questions you can resolve yourself. Do it, then report the result.
- Strict image review. Free images can be remade as often as needed.
- Bigger numbers hook harder. The thumbnail text should be large and bold.
- Write full paths in instructions. Give PC instructions step by step.
