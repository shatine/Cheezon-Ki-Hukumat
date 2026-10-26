# 8단계: 업로드 문구와 썸네일

**Results:** `upload/upload_titles_keywords.md`, `upload/upload_description_en.txt`, `upload/upload_description_hi.txt`, `thumbnail/thumb_vN_1280x720.jpg`.
Examples: `episodes/ep07_bus/upload/`, `episodes/ep08/upload/`.

## 제목
- **Hindi (main) and English, each with 1 main and 2 alternatives.** They point to the same question as the opening line.
- Episode 8: `भूकंप आया तो इस पुल का क्या होगा? | 359 मीटर ऊँचा चिनाब पुल` / `What Happens to This 359 m Bridge in an Earthquake?`

## 설명 (영어·힌디어 파일을 따로, 합치지 않음)
Each description contains, in order:
1. The first line = the opening question.
2. A summary paragraph: the contradiction and the big numbers.
3. A summary of each problem.
4. **Chapters:** the start times of the paragraphs in `narr_timing.json`, as `M:SS`, starting at `0:00`.
   - **Every chapter must be 10 s or longer.** Merge any shorter ones.
5. **Sources:** the URLs from the evidence table, grouped by topic.
6. **Notes:**
   - the highest-figure rule, for example "Where sources give different figures, this video uses the highest published figure";
   - that government claims are claims;
   - assumed dimensions;
   - that it was made with AI, and that people and 3D are illustrations.
7. The subscribe call.
8. Hashtags (about 7).

- Keep each description **under 5,000 characters** (count them).

## 키워드
- English 8, Hindi 8, each on its own line.

## 썸네일
- **Text = the opening line in Hindi**, split into a top band and a bottom band.
  - Episode 8: top, red `भूकंप आया तो`; bottom, yellow `इस पुल का क्या होगा?`; green `359 मीटर` with a **vertical** arrow (height).
- **Layout:**
  - The subject (bridge, train) sits in the middle band. The text must not cover the subject.
  - **Leave margins above and below the text** (about 5% of the height). Text pushed against the edges was criticised.
  - **Text very large and bold**, Noto Sans Devanagari Black (900), black outline about 1/12 of the font size.
  - If a line would not fit in the width when enlarged, limit it to the width with side margins. Splitting into two lines that cover the subject is not allowed.
- **Image:**
  - Generate with no text (prompt B: keep the top and bottom 22% simple).
  - Draw the text in the edit with the exact font. Generators often misspell Devanagari.
  - Script: `episodes/ep08/thumbnail/make_thumb_v3.py`.
  - Fonts: npm `@fontsource/noto-sans-devanagari` (devanagari-900 woff2 → convert to ttf with fontTools). Draw "?" with the latin subset.
  - **Always keep the text-free background image.** Episode 8 had none, so the old text had to be inpainted out, which lowered the quality.
- **File:** 1280×720 JPG, under 2 MB.
- Record the user's final choice in `upload_titles_keywords.md` and HANDOFF.

## 업로드 후
- Update HANDOFF to "업로드 완료".
