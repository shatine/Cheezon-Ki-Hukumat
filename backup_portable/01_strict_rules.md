# 01. 엄격한 규칙 (절대 하지 말 것 / 반드시 할 것)

Breaking these has already caused real problems in earlier episodes. No exceptions.

## A. 상시 허락: 묻지 말고 할 것 (사용자 2026-10-25)
- Commit and push to `main` any file inside the repository: scripts, plans, review logs, work orders and so on.
- Run `guidelines\sync_pc.ps1 -Apply`, and delete what it deletes (old skills and empty folders).
- Carry each work-order step through to the end, retrying anything that failed (TTS lines, image retakes) yourself.
- Generate and retake **Flow images** as many times as needed. They are free.

## B. 멈추고 묻는 경우 (이때만)
1. A step would change the **confirmed script, numbers or order**.
2. Something would **cost money**:
   - Flow video at 15 credits each;
   - paid TTS;
   - paid music;
   - and so on.
3. **Muse video** would be generated, unless the work order records the user's approval.
4. A file outside the repository and the episode working folder would be **deleted**.
5. The **same failure repeats 3 times** after trying a fix.

## C. 대본·내용 금지
- **Never change** the content, order or numbers of a confirmed script (`script_ko_final.md`) or the confirmed Hindi lines.
- Do not write a claim without a source. Mark it "미확인" in the evidence table and let the user decide.
- Do not widen a court ruling or a legal provision beyond what it says. Quote only the original wording.
- Do not reword a sentence the user rewrote. Use it exactly as given.
- No awkward or abstract sentences, and no analogies that contradict the facts.
  - Example from episode 7: saying that heat "escapes", which gets the direction wrong.
- Attribute government and company claims in the sentence itself ("정부는 …라고 밝혔다").

## D. 화면 금지
- **No re-enactment of real people.** Show only cars, places, people from behind, or hands.
- **No children.** Indian adults only. Faces small (under about 1/4 of the screen height). No close-ups of mouths or noses.
- **No text in generated images:** letters, numbers, number plates, brand logos, signs, prayer flags, scripts. Broken Devanagari is rejected too.
  - Blurring is the last resort. Regenerate first.
- **Editing must not stretch time:**
  - No slow motion or speed changes.
  - No freezing the last frame.
  - No repeating or reversing the same segment.
  - No "영상 부족" placeholders.
  - In episode 7, one shot was stretched by 28 s, then played at 0.6×, and this drew strong criticism.
- **Images:** no image may stay on screen longer than 4.5 s. Change every 2–4 s.
- **Camera movement:** no moves in the 3D principle videos. Only about 2/10 of clips move. Do not dolly in towards people, because faces get large.
- **Never use the phrase "One single continuous camera movement…".** Every clip spun, and it caused motion sickness.
- Do not reuse an image on two cuts. Reuse a video only on non-overlapping ranges, and only when the callback is intended.
- A realistic shot must not copy the composition of the master reference image (CB) as it is.

## E. 생성 공정 금지
- **Text-only generation** when a reference image is refused is **not allowed**.
  - In episode 7 the bus came out different and had to be remade.
  - Retry once with the same image. If it is still refused, write "거부" in the report and move on.
- **No rapid repeated submissions** in Flow or Muse (bot detection). One at a time.
- **Do not edit prompts on the PC.** Paste the prompts from the JSON exactly as they are.
  - If one has to be changed, record what changed and why in the `picks` note.
- No generation without the reference image the plan specifies, and no first frame other than the one in the JSON.
- Do not edit the scripts on the PC. If something breaks, report the error message (the last 20 lines) as it is. The cloud fixes it.
- Do not edit `.claude\skills` directly on the PC. Change it in git, then sync.

## F. 편집·계획 금지
- Do not estimate times from sentence length. **Use only the measured TTS** `narr_timing.json`.
  - Episode 7 v6 was estimated and had to be redone.
- Do not speed up or cut the narration to fit the picture.
- A video's usable range must end at or before **length − 0.05 s**. The edit script rejects `src_end > dur − 0.03`.
  - Episode 8 caps everything at `CEND = 9.95`.
- Do not assume videos are 10 s. Check the tool's current setting and the actual measured length.
- Do not render a plan that has automatic-check errors. Errors must be 0.

## G. 보고·검수 금지
- Do not merge automatic measurements and visual review into one statement. Report **what was actually seen** separately from **what was measured**.
- Do not report a pass on something you have not reviewed.
- Do not say "it should arrive" or "it must be there" about a push you have not checked. Confirm with `git fetch` and `git log origin/main`.
- Do not make the user answer questions you can resolve yourself.
- Do not narrate options you are not going to use. Give a recommendation and act on it.

## H. git·파일 금지
- Do not leave media (images, video) in git. Once the cloud has downloaded it, `git rm` it right away.
- No force-push, history rewriting or `reset --hard`.
- Do not delete files outside the repository or the episode folder without asking the user.
- Do not write model names or tool names into commit messages or repository files.
  - This applies only to the AI model names that are unrelated to the content.
- Once a new result is confirmed, delete the old version it replaced (the git history keeps it).
