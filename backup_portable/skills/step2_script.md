# 2단계: 한국어 대본 → 근거표 → 사용자 검수 → 확정

**Before this step:** the opening line and the thumbnail draft are confirmed (step 1). **규칙:** `../02_script_rules.md` (all of it). **Result:** `script/script_ko_final.md`.

## 순서
1. **Fix the question chain first** (a one-line list), starting from the confirmed opening line and ending with its answer, for example: earthquake? → why no piers → arch → … → answer.
   - S01 is the confirmed opening line, word for word.
2. **Write the Korean script:** paragraphs S01–Snn, divided into 도입 / 기 / 승 / 전 / 결.
   - Short spoken sentences, with evidence ids `[E1]` after the sentence.
   - The last paragraph is the subscribe call.
3. **Research evidence:** find sources for every number and claim.
   - Prefer original sources: government, the builders, papers, major newspapers.
   - If sources disagree on a number, **use the highest** and record the others.
   - Write government claims as "정부는 …라고 밝혔다".
   - If it cannot be confirmed, mark it **미확인** → the user decides (keep, replace or drop).
4. **Evidence table** at the bottom of the file: `| ID | 주장 | 근거 | 상태 |`.
5. **"확인할 점" section:** points the user should decide, and what was removed and why.
6. **User review:** show the script in Korean.
   - Apply the user's edits **exactly as written**, then show it again.
7. **Freeze:** once review is finished, put "사용자 검수 완료 YYYY-MM-DD — 이후 내용·순서·숫자 변경 금지" in the title.
   - Delete the old drafts.
   - Record in HANDOFF that the script is confirmed.

## 금지
- Changing the content, order or numbers after confirmation.
- Claims without a source.
- Abstract analogies, and analogies whose direction contradicts the facts.
- Re-enacting real people.
