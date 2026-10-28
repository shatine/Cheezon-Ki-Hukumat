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
  | Conversation with the user, reviews, reports | **Korean** |
  | Narration, subtitles, thumbnail text | **Hindi** |
  | Upload titles and descriptions | **English and Hindi, in separate files** |
- **Delivery spec:**
  - 1920×1080, 30 fps, H.264.
  - Audio: -14 LUFS, true peak -1.5 dBTP.
  - One line of Hindi subtitles burned into the picture.
  - Quiet background music with ducking.

## 2. ★ 제작의 출발점: 후킹 도입부 문구 + 썸네일
**Every episode starts with two things, and nothing else starts before both are confirmed by the user:**
1. **A strong hook opening line.** The central question of the whole video, said in the first seconds.
2. **A thumbnail that grabs attention with that line.** The same words, very large, on a picture that shows the contradiction.

- **Opening line = central question = thumbnail text = what the title points to.** One idea, used four times.
- The topic is chosen *for* its hook: if no strong opening line and thumbnail can be made from a topic, drop the topic.
- The script, images, video and edit all exist to answer that opening question. Every later step is checked against it.
- Details: `skills/step1_hook_thumbnail.md`, and section 1 of `02_script_rules.md`.

## 3. 작업 방식: 100% 로컬
- **Everything runs on the user's Windows PC, in one agent session:** research, script, prompts, generation in the browser (Flow, Muse), TTS, strict review, edit, thumbnail, upload text.
- There is no second session and no hand-off between machines. **The same agent that generates also reviews strictly.**
- **Media (images, video, audio) stays in the episode media folder (CB) on the PC.** It is never committed to git.
- **git is only a backup of text files:** scripts, prompts, plans, review records, HANDOFF. Commit and push to `main` after each step.
- **Browser:**
  - Flow and Muse are driven in Chrome. Muse uses the Chrome on debug port **9227**. Do not use the port-9222 Chrome.
  - **One at a time:** submit → wait 30–60 s and check once → save → next. Rapid repeated submissions trigger bot detection.
- **Working style:**
  - Make the whole list in one go. Do not stop every few items to report.
  - If the session hits its limit, commit what is finished, update HANDOFF, and continue in a new session from HANDOFF.
  - Take screenshots only when needed.

## 4. PC 폴더 구조
| 이름 | 경로 |
|---|---|
| Repository clone (text, scripts, records) | `D:\youtube\Cheezon-Ki-Hukumat\` |
| Channel folder | `D:\youtube\7. Cheezon Ki Hukumat\` |
| Episode media folder (CB) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\NN_name\` (e.g. `08_chenab_bridge`) |
| ├ Images (watermark removed) / originals | `CB\img\`, `CB\img_raw\` |
| ├ Video clips | `CB\clips_v1\` (old versions in `clips_v1\old\`) |
| ├ TTS | `CB\review_edit\narration_hi.wav`, `CB\review_edit\narr\{id}.wav` |
| ├ Review sheets and reports | `CB\review\` (frame sheets, contact sheets, `auto_report.md`) |
| ├ Thumbnail backgrounds | `CB\thumb\` (text-free backgrounds, always kept) |
| └ Render output | `CB\out\` (`v1_review_hi.mp4`, `v1_upload_hi.mp4`) |
| Background music (episodes 6–8) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\music\bgm.mp3` |

## 5. 저장소 구조 (한 편 = `episodes/epNN_name/`)
```
HANDOFF_epNN.md             인계: 확정 사항, 단계별 상태 표, 다음 할 일, 사용자 성향
hook_thumbnail.md           도입부 문구 후보·확정본, 썸네일 시안과 확정본 (1단계)
topic_candidates.md         소재 후보와 선정 이유 (후킹 문구 기준)
opening_candidates.md       참고 영상(100만+ 조회) 후보
refs/*.txt, refs_analysis.md  참고 영상 대본과 분석
script/script_ko_final.md   확정 한국어 대본 + 근거표 (확정 후 수정 금지)
script/lines_hi_ko.tsv      id \t 힌디어 \t 한국어 직역
review_edit/narr_timing.json  TTS 실측 시간표 (줄별 start/end)
plan/plan_vN.py → shot_list_vN.json, shot_table_vN.md   컷 계획 + 자동 점검
images/make_prompts_v1.py → prompts_v1.json, picks_v1.md, cloud_review_v1.py (검수 스크립트)
video/make_vprompts_v1.py → vprompts_v1.json, review_clips_v1.md, cloud_review_clips_v1.py (검수 스크립트)
review_edit/edit_v1.py      검수본·업로드본 렌더, review_v1.md
thumbnail/                  썸네일 스크립트와 결과 jpg (배경 원본은 CB\thumb\)
upload/                     upload_titles_keywords.md, upload_description_en.txt, upload_description_hi.txt
```
- The review scripts keep their episode-8 file names (`cloud_review_*.py`), but they run locally on the CB folders.

## 6. 도구
| 용도 | 도구 | 설정 |
|---|---|---|
| Images | Google **Flow** (Nano Banana 2.1) | 16:9, x1. One project per episode (episode 8: `baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd`). **Free**, so regenerate as often as needed. One image at a time |
| Video (default) | **Muse** (Chrome, debug port 9227) | Image-to-video, 16:9, 10.0 s, 1216×672, 24 fps. **Generate only with user approval** |
| Video (exception) | Flow video (Omni 1.1 Flash) | 1280×720, **15 credits each (paid)**. **Only on the user's instruction.** Star watermark at bottom right (x1132–1190, y572–630) is removed in editing with `delogo` |
| TTS | Voice Studio (free) | voice charonclone, seed 7, speed 1.0, each sentence -16 LUFS |
| Editing | Python + ffmpeg (numpy, soundfile, PIL) | `edit_v1.py` |
| Review | ffmpeg/ffprobe, PIL, numpy, OpenCV | Frame sheets, brightness, dhash similarity |
| Thumbnail | Python + PIL (raqm), Noto Sans Devanagari 900 | `make_thumb_v3.py` |

## 7. 공정 한눈에 (각 단계 = `skills/stepN_*.md`)
1. **Hook opening line and thumbnail (start here):** topic chosen for its hook, 3 reference videos, opening line (central question), thumbnail draft from a text-free background. User confirms both.
2. **Script:** Korean script and evidence table, built as the answer to the opening question → user review → freeze.
3. **Hindi and TTS:** sentence-matched Hindi → TTS → measured timing table `narr_timing.json`.
4. **Plan:** sentence-level cut plan script. Zero automatic-check errors.
5. **Images:** prompt JSON → generate in Flow → strict review → remakes → all confirmed.
6. **Video:** video prompt JSON → generate in Muse (after user approval) → frame review → usable ranges entered in the plan.
7. **Edit:** review-cut render → review from 0 s to the end → fixes → upload-cut render (background music, -14 LUFS) → check.
8. **Upload text and final thumbnail:** EN/HI titles, descriptions, chapters, sources, keywords 8+8, thumbnail finished from the step-1 draft.
9. **Records and hand-off:** HANDOFF after every step, commit and push the text files. Once a new version is confirmed, delete the one it replaced.

## 8. 사용자 성향 (반드시)
- **Communication:**
  - Do not make the user answer questions you can resolve yourself. Do the work, then report the result.
  - When something is long-running, say in one or two lines what you are doing, then carry on.
  - Report in Korean, briefly, with a table and the key numbers.
- **Instructions for the user:**
  - **Full paths.** Steps in order. Commands that can be pasted as they are.
- **Review:**
  - The user wants **strict review**. Images are free, so they can be remade as often as needed.
- **Hooks:**
  - **The opening line and thumbnail come first and decide the episode.**
  - **Bigger numbers hook harder.** Where sources disagree, use the highest figure (see `02_script_rules.md`).
  - Thumbnail text **very large, bold, thick black outline**, with margins at the top and bottom.
- **Speed:**
  - Cutting the work into small chunks (for example "report every 10 images") is too slow, so do not do it. Make the whole list, then report once.
