# 1단계: 후킹 도입부 문구 + 썸네일 (모든 제작의 시작)

**Every episode starts here.** The script, images and video do not start until the user has confirmed **the opening line and the thumbnail draft.**
**Results:** `topic_candidates.md`, `opening_candidates.md`, `refs/*.txt`, `refs_analysis.md`, `hook_thumbnail.md`, `CB\thumb\` (text-free backgrounds), `thumbnail/thumb_draft_vN.jpg`, `HANDOFF_epNN.md` started.

## 순서
1. **Topic candidates (3–5), judged by their hook.** Indian infrastructure, technology or everyday subjects with a visible contradiction, inconvenience or risk.
   - For each candidate write: **its best opening line**, **its thumbnail idea** (picture + words), the contradiction, the possible "big numbers", the principles you can show on screen, and the views of similar videos.
   - A candidate without a strong opening line and thumbnail is dropped, however interesting it is.
   - Recommend one, and confirm it with the user.
2. **Reference videos:** find **3 videos with 1M+ views** on the same subject (any language). Record the views, length, style **and thumbnail** in `opening_candidates.md`.
   - Clean the transcripts into `refs/<videoID>.txt` (remove timestamps).
   - `refs_analysis.md`: **first their hook (the first 10 s) and their thumbnail** (what it promises, how many words, which number), then each video's flow (numbered), comparisons, how it explains principles, and its strengths.
   - **Use only the order of information, hooks and comparisons. Never copy the wording.** Re-verify every number against original sources at the script stage.
3. **Opening line candidates (3–5)** in `hook_thumbnail.md`, ranked, with a recommendation. A strong hook has:
   - a visible contradiction or danger the viewer can picture at once;
   - **the biggest number** available ("359m 위 기차, 강바닥엔 기둥 하나 없다!");
   - a question the viewer cannot answer yet, and wants answered;
   - short spoken words, readable on a thumbnail in under 2 seconds (about 3–7 Hindi words per line).
   - The user chooses, or rewrites it. **Use what the user rewrote exactly as given.**
4. **Thumbnail draft, made right away from the chosen line:**
   - **Text = the opening line in Hindi**, split into a top band and a bottom band. Colours:
     - yellow = question;
     - red = failure or danger;
     - green = numbers or solutions (with an arrow when it is a size or height);
     - white = linking words.
   - **Background:** generate 2–3 text-free backgrounds in Flow that show the contradiction (subject in the middle band; top and bottom 22% kept simple). Save them in `CB\thumb\` and **always keep them.**
   - Draw the text with `make_thumb_v3.py` (rules in `step8_upload_thumbnail.md`): very large, bold, black outline, margins above and below.
   - Check it at small size (about 320×180): can the question and the number be read in under 2 s?
   - Show the user the line and the draft together. The user confirms both, or asks for changes.
5. **Title direction:** the title points to the same question as the opening line. Write it as a one-line note now; the final titles are made in step 8.
6. **The 30 s opening:** plan 3–5 long natural videos (5–10 s each) that show what the opening line says. Contrast "the impressive sight vs the risk or reality".
7. Create `HANDOFF_epNN.md`. It holds:
   - the confirmed opening line, thumbnail draft (file path) and title direction;
   - the step status table;
   - "다음 세션이 할 일";
   - the user's preferences.

## 완료 기준
- The user has confirmed the topic, **the opening line and the thumbnail draft**, and they are recorded in `hook_thumbnail.md` and HANDOFF.
- Only then go on to step 2. The script is written as the answer to this opening question.
