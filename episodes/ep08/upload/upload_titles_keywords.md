# 8편 업로드: 제목·키워드·썸네일 (2026-10-26)

The title, thumbnail and first line all point to the same question as the opening: "지진이 오면 이 다리는 어떻게 될까?" (Hindi: भूकंप आया तो इस पुल का क्या होगा?).
- Descriptions are kept as separate files per language: `upload_description_en.txt` and `upload_description_hi.txt`.
- Chapter times are the start times of each paragraph in `review_edit/narr_timing.json`.
  - Every chapter is 10 s or longer (a YouTube requirement). S08 (1:52) is 10 s long, so it is merged into "Fixing the mountain first".
- Figures follow the script's evidence table (`script/script_ko_final.md`), including the highest-figure rule. The description also says this.

## 제목
**Hindi (main, the channel's main language):** भूकंप आया तो इस पुल का क्या होगा? | 359 मीटर ऊँचा चिनाब पुल
- Alternatives:
  - नदी में एक भी खंभा नहीं, फिर 359 मीटर ऊँचा पुल खड़ा कैसे है?
  - दुनिया का सबसे ऊँचा रेल पुल भूकंप में गिरेगा क्या?

**English:** What Happens to This 359 m Bridge in an Earthquake?
- Alternatives:
  - No Pillar in the River: How India Built the World's Highest Rail Bridge
  - Why the Chenab Bridge Has No Pillars — and Why That Makes It Safer

## 키워드 (각 8개)
**English:** Chenab bridge, Chenab rail bridge, world's highest railway bridge, Jammu Kashmir railway, arch bridge, earthquake proof bridge, Indian Railways engineering, how bridges work
**Hindi:** चिनाब पुल, चिनाब रेल पुल, दुनिया का सबसे ऊँचा रेल पुल, जम्मू कश्मीर रेल, आर्च पुल, भूकंप और पुल, भारतीय रेल, पुल कैसे बनता है

## 썸네일
- **Text (confirmed with the script):**
  - Top, red: `भूकंप आया तो`
  - Bottom, yellow: `इस पुल का क्या होगा?`
  - Beside the vertical arrow, green: `359 मीटर`
- **확정 (사용자 2026-10-26): `thumbnail/thumb_v3_1280x720.jpg`** (1280x720 JPG, under YouTube's 2 MB limit). Upload it as it is.
  - **Changes from v2 (user request):**
    - Margins above and below the text: 48 px at the 941 px height.
    - Top line `भूकंप आया तो` is 1.5 times larger (font size about 170 → 255).
    - The bottom line `इस पुल का क्या होगा?` already used almost the full width, so at 1.5 times it would not fit on one line. As two lines it covered the bridge, so that was rejected. It stays one line, as large as fits the width with side margins.
  - **How it was made:**
    - The old text was removed from `thumb_v2_full.png` (OpenCV inpaint), and the text was drawn again in Noto Sans Devanagari Black, with an outline 1/12 of the font size.
    - The bottom strip is blurred to hide the traces of the removed text.
  - `thumbnail/thumb_v3_full.png` (1672x941, 1.7 MB) is the larger original. Either file can be uploaded.
