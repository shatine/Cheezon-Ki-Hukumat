# 00. 전체 지침

## 1. 채널
- **Channel:** Cheezon Ki Hukumat (@CheezonKiHukumat).
- **Format:** an explainer channel on the principles behind Indian infrastructure, technology and everyday life.
- **Viewers:** Indian adults.
- **Story shape:** start from a contradiction, inconvenience or risk in the subject, as a question. Give partial answers with principles and evidence, and at the end come back to the first question with the answer.
- **Episodes done:**
  - Episode 7: "버스에서 살 수 있을까요?" (KSRTC bus).
  - Episode 8: "체납 철교: 지진이 오면 이 다리는 어떻게 될까?" (uploaded 2026-10-26).
- **Languages:**
  | 용도 | 언어 |
  |---|---|
  | Conversation with the user, reviews, reports, work orders | **Korean** |
  | Narration, subtitles, thumbnail text | **Hindi** |
  | Upload titles and descriptions | **English and Hindi, in separate files** |
- **Delivery spec:**
  - 1920×1080, 30 fps, H.264.
  - Audio: -14 LUFS, true peak -1.5 dBTP.
  - One line of Hindi subtitles burned into the picture.
  - Quiet background music with ducking.

## 2. 역할 분담 (두 개의 에이전트 세션)
| 세션 | 위치 | 하는 일 | 하지 않는 일 |
|---|---|---|---|
| **Cloud (planning and review)** | Remote container with a clone of the git repository | Topic, script, evidence, plan scripts, image and video prompts, **strict review**, edit scripts, PC work orders, upload text, thumbnail text layout | It cannot control the browser on the user's PC (Flow, Muse) |
| **PC (generation)** | User's Windows PC, local agent | Flow image generation, Muse/Flow video generation, TTS, final render, git push | **No strict review** (to save tokens). Only generate, save and do a quick check |

- **Credits:** use the cloud session's credits first. Keep PC session tokens to a minimum.
- **PC quick check:** look at each result once.
  - Regenerate right away if the subject is wrong, realistic and 3D are swapped, text is visible, or it is dark.
  - Zooming in, comparing and detailed records are the cloud's job.
- **PC working style:**
  - Make the whole list in a work order **in one go**, then push once.
  - If the PC hits its limit, push what is finished and continue in a new session.
  - Take screenshots only when needed. Check completion by waiting **once**, 30–60 s after submitting.

## 3. 파일 주고받기 (git)
- **Repository:** https://github.com/shatine/Cheezon-Ki-Hukumat. The exchange branch is **`main`**.
- **Order of exchange:**
  1. **Cloud:** writes scripts, prompts and a work order → commits and pushes to `main`.
  2. **PC:** `git pull origin main` → runs the work order → copies results into the repository's send folder (for example `episodes/epNN/images/v1/`) → commits and pushes.
  3. **Cloud:** pulls → copies the media to a scratch folder → **removes the media from git right away** (`git rm -r …`, commit message "remove … after cloud download (kept on PC)") → pushes.
  4. **Cloud:** reviews strictly → adds the result to `picks_*.md` / `review_*.md` → gives the PC a remake list or the next work order.
- **If a push is rejected** (fetch first): run `git pull --no-rebase origin main`, then push again.
- **Size limit:** git rejects files over 100 MB. Videos for the cloud are sent as a small copy at 960×540, crf 30.
- **Case clash:** Windows does not tell `v14` from `V14`. Name the file differently (for example `v14_real.mp4`) and map it in the plan's `FILE`.

## 4. PC 폴더 구조
| 이름 | 경로 |
|---|---|
| Repository clone | `D:\youtube\Cheezon-Ki-Hukumat\` |
| Channel folder | `D:\youtube\7. Cheezon Ki Hukumat\` |
| Episode media folder (CB) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\NN_name\` (e.g. `08_chenab_bridge`) |
| ├ Images (watermark removed) / originals | `CB\img\`, `CB\img_raw\` |
| ├ Video clips | `CB\clips_v1\` (old versions in `clips_v1\old\`) |
| ├ TTS | `CB\review_edit\narration_hi.wav`, `CB\review_edit\narr\{id}.wav` |
| └ Render output | `CB\out\` (`v1_review_hi.mp4`, `v1_upload_hi.mp4`, small copies) |
| Background music (episodes 6–8) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\music\bgm.mp3` |
| Skill sync | `guidelines\sync_pc.ps1 -Apply` (keeps the PC skill folder identical to git) |

## 5. 저장소 구조 (한 편 = `episodes/epNN_name/`)
```
HANDOFF_epNN.md             인계: 확정 사항, 단계별 상태 표, 다음 할 일, 사용자 성향
topic_candidates.md         소재 후보와 선정 이유
opening_candidates.md       참고 영상(100만+ 조회) 후보
refs/*.txt, refs_analysis.md  참고 영상 대본과 분석
script/script_ko_final.md   확정 한국어 대본 + 근거표 (확정 후 수정 금지)
script/lines_hi_ko.tsv      id \t 힌디어 \t 한국어 직역
review_edit/narr_timing.json  TTS 실측 시간표 (줄별 start/end)
plan/plan_vN.py → shot_list_vN.json, shot_table_vN.md   컷 계획 + 자동 점검
images/make_prompts_v1.py → prompts_v1.json, picks_v1.md, cloud_review_v1.py
video/make_vprompts_v1.py → vprompts_v1.json, review_clips_v1.md, cloud_review_clips_v1.py
review_edit/edit_v1.py      검수본·업로드본 렌더, review_v1.md
thumbnail/                  썸네일
upload/                     upload_titles_keywords.md, upload_description_en.txt, upload_description_hi.txt
WORK_ORDER_*.md             PC 작업 지시서
```

## 6. 도구
| 용도 | 도구 | 설정 |
|---|---|---|
| Images | Google **Flow** (Nano Banana 2.1) | 16:9, x1. One project per episode (episode 8: `baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd`). **Free**, so regenerate as often as needed. One image at a time |
| Video (default) | **Muse** (Chrome, debug port 9227) | Image-to-video, 16:9, 10.0 s, 1216×672, 24 fps. **Generate only with user approval** |
| Video (exception) | Flow video (Omni 1.1 Flash) | 1280×720, **15 credits each (paid)**. **Only on the user's instruction.** Star watermark at bottom right (x1132–1190, y572–630) is removed in editing with `delogo` |
| TTS | Voice Studio (free) | voice charonclone, seed 7, speed 1.0, each sentence -16 LUFS |
| Editing | Python + ffmpeg (numpy, soundfile, PIL) | `edit_v1.py` |
| Review | ffmpeg/ffprobe, PIL, numpy, OpenCV | Frame sheets, brightness, dhash similarity |

- **One at a time:** in both Flow and Muse, submit → check it finished → next. Rapid repeated submissions trigger bot detection.
- **Browser:** Muse uses Chrome on port 9227. Do not use the port-9222 Chrome.

## 7. 공정 한눈에 (각 단계 = `skills/stepN_*.md`)
1. **Topic and opening line:** pick the topic, analyse 3 reference videos, fix the opening line (central question). Thumbnail text = opening line.
2. **Script:** Korean script and evidence table → user review → freeze.
3. **Hindi and TTS:** sentence-matched Hindi → TTS → measured timing table `narr_timing.json`.
4. **Plan:** sentence-level cut plan script. Zero automatic-check errors.
5. **Images:** prompt JSON → the PC generates in Flow → strict cloud review → remakes → all confirmed.
6. **Video:** video prompt JSON → the PC generates in Muse (after user approval) → cloud frame review → usable ranges entered in the plan.
7. **Edit:** review-cut render → cloud review from 0 s to the end → fixes → upload-cut render (background music, -14 LUFS) → check.
8. **Upload text and thumbnail:** EN/HI titles, descriptions, chapters, sources, keywords 8+8, thumbnail.
9. **Hand-off:** update HANDOFF. Once a new version is confirmed, delete the one it replaced.

At every step, the cloud keeps these up to date:
- the HANDOFF status table;
- the "다음 클라우드 세션이 할 일" section;
- the PC work order (`WORK_ORDER_*.md`).

## 8. 사용자 성향 (반드시)
- **Communication:**
  - Do not make the user answer questions you can resolve yourself. Do the work, then report the result.
  - When something is long-running, say in one or two lines what you are doing, then carry on.
  - Report in Korean, briefly, with a table and the key numbers.
- **Instructions for the user and the PC:**
  - **Full paths.** Steps in order. Commands that can be pasted as they are.
- **Review:**
  - The user wants **strict review**. Images are free, so they can be remade as often as needed.
- **Hooks:**
  - **Bigger numbers hook harder.** Where sources disagree, use the highest figure (see `02_script_rules.md`).
  - Thumbnail text **very large, bold, thick black outline**, with margins at the top and bottom.
- **Speed:**
  - Cutting the work into small chunks (for example "push every 10 images") is too slow, so do not do it. Make the whole list, then push once.
