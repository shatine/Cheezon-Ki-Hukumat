# 10편 작업 지시서: 참조 영상 → 업로드본까지 (로컬 Claude, 2026-10-30)

**진행 현황: 시작 전.** 참조 영상 URL은 `episodes/ep10/refs/urls.txt`에 있다. **비어 있으면 시작하지 말고 사용자에게 URL을 달라고 한 줄로 말한다.**

**Goal:** make episode 10 **the same way as episode 8**, from the reference videos the user gave to the upload cut, **100% locally on this PC in one session**.
- The rules are `backup_portable/` (latest, local version). Episode 8 (`episodes/ep08/`) is the template for every file.
- Where `guidelines/CLAUDE.md` or the old skills mention the cloud, the PC split, work orders or sending media through git, follow `backup_portable/` instead.

## 0. 먼저 읽기 (전부, 이 순서로)
1. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\README.md`
2. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\00_overall_guide.md`
3. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\01_strict_rules.md`
4. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\02_script_rules.md`
5. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\03_image_rules.md`
6. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\04_video_rules.md`
7. Before each step, the matching `backup_portable\skills\stepN_*.md`.
8. This work order. Then `episodes\ep08\HANDOFF_ep08.md` to see how episode 8 ran.

## ★ 8편 방식 = 간결하게 (9편에서 생긴 문제를 되풀이하지 말 것)
Episode 9 slowed to 19 of 85 images because the records grew far beyond what the rules ask. **For episode 10, do only what episode 8 did:**
- **Records are as short as episode 8's.** `picks_v1.md`: one line per image (id | ref | tries | chosen | note), plus one short section per review round. Compare `episodes\ep08\images\picks_v1.md`.
- **No extra ledgers:** no SHA-256 locks, revision/alias registries, receipts, provenance JSON, checkpoint JSON, pixel-identity proofs. The git history is the record.
- **HANDOFF stays under about 80 lines:** confirmed items, the status table, "다음 세션이 할 일", approvals. Replace old status instead of appending history.
- **No helper sub-agents driving the browser.** One session, one browser tab, one submission at a time.
- Reuse the episode-8 scripts by copying them and changing only the episode values. Do not write new frameworks around them.

## 경로
| 이름 | 경로 |
|---|---|
| Repository | `D:\youtube\Cheezon-Ki-Hukumat\` |
| Episode text (git) | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep10\` |
| Episode media (CB, not git) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\10_<english_topic>\` (create it once the topic is fixed in step 1, e.g. `10_pamban_bridge`) |
| Background music | `D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\music\bgm.mp3` |
| Episode-8 templates | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\` |
| TTS tools, voice reference | `D:\youtube\Cheezon-Ki-Hukumat\skills\cheezon-production\tools\` |

## 사용자 확인 지점 (여기서만 멈춘다)
| # | 언제 | 사용자에게 보여 줄 것 | 확인 후 |
|---|---|---|---|
| G1 | End of step 1 | Topic, opening line candidates (ranked, one recommended), **thumbnail drafts** (files in `CB\thumb\`), title direction | Step 2 |
| G2 | End of step 2 | Korean script + evidence table + "확인할 점" | Freeze → steps 3–5 without stopping |
| G3 | End of step 5 + video prompts | Video list (count, ids, what each shows) | Muse generation (record "날짜 + 사용자 원문" in HANDOFF) |
| G4 | End of step 7 | Upload cut + final thumbnail + titles | User uploads |

Between gates, follow `01_strict_rules.md` A (상시 허락): do not ask, carry on, report at the gate.
- **At G1 also ask once** whether the master reference images may be uploaded to this episode's Flow project (they are Flow's own outputs). Record the answer in HANDOFF, so step 5 does not stop for it.
- Flow project and Chrome: a **new Flow project for episode 10**, in the Chrome profile the user last named (episode 9: `artbuilder883`). If unsure which Chrome to use, ask at G1. Muse: Chrome on port 9227.

## 1단계: 참조 영상 → 후킹 도입부 문구 + 썸네일 시안 (`skills/step1_hook_thumbnail.md`)
1. Get each URL in `refs\urls.txt`:
   ```
   cd D:\youtube\Cheezon-Ki-Hukumat\episodes\ep10\refs
   yt-dlp --skip-download --write-info-json --write-auto-subs --write-subs --sub-langs "en.*,hi.*" --convert-subs vtt -o "%(id)s.%(ext)s" <URL>
   yt-dlp --skip-download --write-thumbnail -o "%(id)s" <URL>
   ```
   - Clean each transcript into `refs\<id>.txt` (no timestamps; same as `episodes\ep08\refs\*.txt`).
   - Record title, views, length, upload date, thumbnail (what it shows, the words, the number) in `opening_candidates.md`.
   - Do not commit the thumbnail images or the info JSON; keep them in `CB\refs\`.
2. `refs_analysis.md` (like episode 8): **first each video's hook (first 10 s) and thumbnail**, then its flow (numbered), comparisons, how it explains principles, strengths. Use only the order, hooks and comparisons. Never copy the wording.
3. **Topic:** the Indian subject the references are about. If they are not about India, propose 3 Indian counterparts in `topic_candidates.md`, each with its best opening line and thumbnail idea, and recommend one.
4. **Opening line candidates (3–5)** in `hook_thumbnail.md`, ranked, one recommended. Visible contradiction or danger, **the biggest number**, a question the viewer wants answered, readable in 2 s.
5. **Thumbnail drafts:** 2–3 text-free backgrounds in Flow (free) → `CB\thumb\` → text drawn with a copy of `episodes\ep08\thumbnail\make_thumb_v3.py` (Noto Sans Devanagari 900, very large, black outline, margins top and bottom) → check at 320×180 → `thumbnail\thumb_draft_v1_1280x720.jpg`.
6. Create `HANDOFF_ep10.md` (layout of `episodes\ep08\HANDOFF_ep08.md`). Commit and push the text files. **→ G1.**

## 2단계: 대본 (`skills/step2_script.md`, `02_script_rules.md`)
- Question chain from the confirmed opening line to its answer, 5–6 minutes (episode 8: 24 paragraphs, 334 s).
- S01 = the confirmed opening line, word for word. The last paragraph is the subscribe call.
- Evidence table with source URLs. Where sources disagree, **use the highest number** and write "높은 숫자 채택". Government claims attributed in the sentence. Unconfirmed claims are marked 미확인 for the user.
- Show the Korean script. Apply the user's edits exactly as written. **→ G2.** Then freeze `script\script_ko_final.md` ("사용자 검수 완료 YYYY-MM-DD — 이후 내용·순서·숫자 변경 금지").

## 3–5단계: 연속 진행 (멈추지 않는다)
- **Step 3:** `script\lines_hi_ko.tsv` → TTS (charonclone, seed 7, speed 1.0, -16 LUFS, pauses 0.35 / 0.8 s) → defect checks → `review_edit\narr_timing.json`, `narr_check.json`. Audio stays in `CB\review_edit\`.
- **Step 4:** copy `episodes\ep08\plan\plan_v2.py` → `plan\plan_v1.py`. Measured times only. Automatic-check errors must be 0 ("점검: 통과").
- **Step 5:** copy `episodes\ep08\images\make_prompts_v1.py` → `prompts_v1.json` → masters first → every image in Flow, one at a time → watermark removal → **after the whole list,** strict review with a copy of `cloud_review_v1.py` → remakes → all confirmed. `picks_v1.md` short, as in episode 8.
- Then write the video prompts (copy `episodes\ep08\video\make_vprompts_v1.py`): principle videos with the still-object sentence and light/colour/arrows only; about 2/10 with camera moves. **→ G3.**

## 6–7단계: 영상 → 편집
- **Step 6 (after G3):** Muse, one at a time → `CB\clips_v1\` → after the whole list, frame review with a copy of `cloud_review_clips_v1.py` → usable ranges (end ≤ length − 0.05 s) → remakes of failed ids only → plan `USE` updated, errors 0. Flow video only on the user's instruction (paid).
- **Step 7:** copy `episodes\ep08\review_edit\edit_v1.py` → review cut → review the original from 0 s to the end (1 s frame sheets, brightness, frame difference, `ebur128`, `silencedetect`, first 10 s against the hook) → fixes → `--upload` render (BGM -21 dB with ducking, -14 LUFS, TP -1.5) → check.

## 8단계: 업로드 문구와 썸네일 (`skills/step8_upload_thumbnail.md`)
- `upload\upload_titles_keywords.md` (HI and EN titles, 1 + 2 each, keywords 8 + 8), `upload_description_en.txt`, `upload_description_hi.txt` (chapters ≥ 10 s from `narr_timing.json`, sources, highest-number note, AI note, under 5,000 characters).
- Final thumbnail from the G1 draft: same text, improved background → `thumbnail\thumb_v1_1280x720.jpg` (under 2 MB). **→ G4.**

## 매 단계 끝
- Commit and push **text only** (`skills/step9_records_handoff.md`). Before each commit, check `git status` shows no png/jpg backgrounds/mp4/wav.
- Update HANDOFF: status table and "다음 세션이 할 일". If the session ends, the next session continues from HANDOFF.
- Report to the user in Korean: verdict line, a table with key numbers, what happens next.

## 금지 (요약; 전체는 `01_strict_rules.md`)
- Starting the script, images or video before G1 is confirmed.
- Changing the confirmed opening line, script, numbers or order.
- Muse before G3; Flow video or anything paid without the user's instruction.
- Text-only generation when a reference image is refused; rapid repeated submissions.
- Estimated times; slow motion, freezes, repeats; images longer than 4.5 s.
- Committing media. Records longer than episode 8's.
