# 02. 대본 생성 규칙

## 1. 대본보다 먼저: 후킹 도입부 문구와 썸네일 (1단계, `skills/step1_hook_thumbnail.md`)
**The script is written only after the user has confirmed the opening line and the thumbnail draft.**
1. **Hook opening line first.** It is the central question of the video and the first thing the viewer hears.
   - **A strong hook has:**
     - a visible contradiction or danger the viewer can picture at once;
     - **the biggest number** available (359 m, ×5, 266 km/h);
     - a question the viewer cannot answer yet, and wants answered;
     - short spoken words, readable on a thumbnail in under 2 seconds.
   - Write 3–5 candidates in `hook_thumbnail.md`, rank them, and recommend one. The user chooses or rewrites it. **Use what the user rewrote exactly as given.**
   - Episode 8: "지진이 오면 이 다리는 어떻게 될까? 359m 위 기차, 강바닥엔 기둥 하나 없다! 기둥 하나 못 세우는데, 다리는 어떻게 놓았나?"
   - Episode 7: "버스에서 살 수 있을까요?"
2. **Thumbnail draft at the same time.** The opening line in Hindi, very large, on a text-free background that shows the contradiction. The user confirms the draft together with the line.
3. **Topic:** an Indian structure, technology or everyday subject with a contradiction, inconvenience or risk that is visible on screen, **chosen because it gives a strong hook.**
   - Write candidates in `topic_candidates.md`, each with its best opening line and thumbnail idea. A topic without a strong hook is dropped.
4. **Reference videos:** find 3 videos on the same subject with **1M+ views** (`opening_candidates.md`). Clean their transcripts into `refs/*.txt`, then analyse them in `refs_analysis.md`:
   - **their hook and thumbnail first** (what the first 10 s and the thumbnail promise);
   - the flow of each video;
   - its comparisons;
   - how it explains the principles.
   - **Use only the order of information, the hooks and the comparisons. Never copy the wording.**
5. **Design, settled with the hook:**
   - the scene the viewer sees;
   - the visible contradiction;
   - **the central question (opening line)**;
   - the one-line twist;
   - the surprise;
   - the final realisation;
   - the thumbnail text.
6. **Opening line = central question = thumbnail text = what the title points to.**
   - Once the user confirms it, do not rewrite it on your own.
   - The whole script is the answer to this question. Cut anything that does not lead back to it.

## 2. 구조: 질문 사슬
- **Order:**
  1. Question (opening).
  2. 기: the first problem.
  3. 승: the second and third problems.
  4. 전: back to the first question, then the remaining variables.
  5. 결: back to the first question, with the answer.
- **The answer to one problem must lead to the next.**
  - Episode 8: earthquake? → why no piers → arch → the arch pushes on the mountain → but the mountain is cracked → fix the mountain first → how to build an arch in mid-air → back to the earthquake: the deck floats → wind and sunlight → answer.
  - Episode 7: fixing the heat → water and waste → the other end of that hose is land → the law.
- **Return to the opening question twice:** once in the middle (전) and once at the end (결).
- Cut lists of solutions and excuses unrelated to the question. Record what was cut, and why, in a table.
- **The last line is the subscribe call:**
  - Korean: "이런 이야기를 계속 받아 보시려면 구독, 하이프 쎄게 눌러 주세요!"
  - Hindi: "ऐसी और कहानियाँ पाने के लिए, सब्सक्राइब और हाइप ज़ोर से दबाइए!"
- **Length:** about 5–6 minutes of narration (episode 8: 334 s, 24 paragraphs, 70 Hindi lines).

## 3. 문장
- **Short spoken sentences.** One fact or one move per sentence.
- **Principles must be things the picture can show.**
  - Episode 8: "양 끝을 잡고 늘어뜨린 사슬을 뒤집으면 미는 힘만 받는 아치."
- **Comparisons are things the viewer knows:**
  - Episode 8: "에펠탑보다 35 m 높고, 쿠툽 미나르 다섯 개."
- No awkward or abstract sentences, and no analogies that contradict the facts.
- **Use sentences the user rewrote exactly as given.**

## 4. 근거표 (대본 파일 아래에 반드시)
`| ID | 주장 | 근거 (출처 URL) | 상태 |`
- **Status values:**
  - 확인 (confirmed);
  - 확인 (높은 숫자 채택) (confirmed, highest figure used);
  - 계산 (calculated);
  - 일반 원리 (general principle);
  - 확인 (참고 영상 기반) (confirmed, based on a reference video);
  - 정부 주장 (출처 명시) (government claim, attributed);
  - **미확인** (unconfirmed).
- Put the evidence ID after the sentence in the script, for example `[E1][E2]`.
- **미확인 claims:** the user decides. If no source can be found, drop the claim.
  - Example from episode 8: the "90 km/h stop" rule appeared only in a 2017 planning article, so it was removed and replaced with confirmed facts.
- Where sources disagree on a date or a detail, drop the claim. Example from episode 8: the 1892 vs 1898 Maharaja proposal.
- Quote court rulings and laws in their original wording only, without widening their scope.
- **Real people:** use only facts confirmed in articles. Do not re-enact them on screen.

## 5. 숫자 규칙 (사용자 2026-10-24)
- **Where sources give different figures, use the highest.** Bigger numbers hook harder.
  - In the evidence table, list the other values and write "높은 숫자 채택".
  - Episode 8: Eiffel Tower +35 m (not 29 m), arch 469 m (not 467 m), steel 35,000 t (not 30,000 / 25,000), wind 266 km/h (not 260), sensors 120 (not 100+ / 117).
  - Say this in the upload description too: "Where sources give different figures, this video uses the highest published figure."
- **Attribute government and company claims in the sentence:** "정부는 규모 8의 지진도 견딜 수 있다고 밝혔습니다."
- Do not give a number that has not been made public. Example from episode 8: the wind threshold was described only as "허용 기준을 넘으면".

## 6. 검수·확정
1. Show the user the Korean script and the evidence table, and get their review.
2. Once the review is done, write the **confirmed file** `script/script_ko_final.md`.
   - Put "사용자 검수 완료 YYYY-MM-DD — 이후 내용·순서·숫자 변경 금지" in its title.
   - After that, never change its content, order or numbers.
3. Delete the old drafts (v1, v2 and so on); the git history keeps them.

## 7. 힌디어 번역
- **Sentence-matched translation.** One row per line: `id \t Hindi \t Korean literal translation` (`script/lines_hi_ko.tsv`).
  - Ids are paragraph + letter: S01a, S01b, …
- **Write numbers out in words** so they are easy to read aloud. Examples: "तीन सौ उनसठ मीटर", "दो हज़ार इक्कीस".
- Write English proper nouns in Devanagari. Examples: चिनाब, एफ़िल टावर.
- **Tone:** natural, conversational Hindi. Questions end with "?".
- Thumbnail and opening line: write the Hindi of the opening line exactly as it is. Example: "भूकंप आया तो इस पुल का क्या होगा?"

## 8. TTS (무료 Voice Studio, 로컬 실행)
- **Settings:** voice `charonclone`, **seed 7 fixed**, speed 1.0, one sentence at a time, each sentence -16 LUFS.
- **Reference files:**
  - `skills/cheezon-production/tools/voice_ref_male_charonclone.wav`
  - `ref_text.txt`
- **Pauses:** 0.35 s between sentences in the same paragraph, 0.8 s between paragraphs.
- **Strict defect check** (`junk_check.py`, `asr_check.py`). If a line fails:
  1. Regenerate it with the same seed, changing the commas.
  2. If it still fails, split it at a comma.
  3. If it still fails, split it in half.
- **Results:**
  - `CB\review_edit\narr\{id}.wav`
  - `narration_hi.wav`
  - `episodes/epNN/review_edit/narr_timing.json`, the measured start and end of each line. **All later planning uses this.**
- **Do not** speed up or cut the narration to fit the picture.
- Report what the user heard separately from what the automatic checks found.
