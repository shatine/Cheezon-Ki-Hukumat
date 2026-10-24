# 8편 썸네일 프롬프트 v2 (2026-10-24)

Changes from v1, based on the user's first result:
- **Text much bigger.** Split into top and bottom bands, each about 20–25% of the frame height.
- **359 m arrow fixed.** In v1 the arrow ran **horizontally** along the deck, which reads as length. It is now a **vertical** arrow from the deck down towards the river, which reads as height.
- **Layout:** the bridge and train sit in the middle band, so the text never covers them.

Draft made in the cloud: `thumbnail/thumb_v2_1280x720.jpg`. The user's image with the text redrawn larger.

- **문구:**
  - Top, red: `भूकंप आया तो`
  - Bottom, yellow: `इस पुल का क्या होगा?`
  - Beside the arrow, green: `359 मीटर`
  - Every letter extra-heavy with a thick black outline.

## A. 글자 포함 (Flow)
```
Eye-catching YouTube thumbnail, photorealistic, ultra bright saturated colours, very high contrast, dramatic, sharp focus, 16:9.
COMPOSITION IN THREE BANDS:
TOP BAND (top 22% of the frame): clean bright blue sky, with HUGE bold Hindi text "भूकंप आया तो" in saturated bright red, extra-heavy Devanagari font, letters filling the band height, thick black outline around every letter, left-aligned.
MIDDLE BAND: the Chenab Rail Bridge in Jammu and Kashmir seen from low in the gorge — one gigantic steel truss arch springing from two near-vertical rocky cliffs of a deep V-shaped Himalayan gorge, a long flat railway deck on top supported by slender steel piers standing on the arch, a modern white-and-blue passenger train crossing the deck. EARTHQUAKE MOMENT: the cliffs are shaking, big rocks and dust tumbling down both slopes, cracks across the foreground rock — but the bridge and train stand intact. A thick bright green VERTICAL double-headed arrow with black outline runs straight down from the middle of the deck towards the river under the arch, with bold green text "359 मीटर" (black outline) beside it.
BOTTOM BAND (bottom 22% of the frame): HUGE bold Hindi text "इस पुल का क्या होगा?" in saturated bright yellow, extra-heavy Devanagari font, spanning almost the full width, thick black outline, centred, over the river and rocks.
Text spelled exactly as given, crisp and fully legible. Text never covers the train or the arch. No other text, no logos, no watermark, no people close-up.
```

## B. 글자 없음 (힌디어 철자가 깨질 때. 글자와 화살표는 편집에서 넣는다)
```
Eye-catching YouTube thumbnail background, photorealistic, ultra bright saturated colours, very high contrast, dramatic, 16:9. No text, no letters, no arrows, no logos, no watermark.
The Chenab Rail Bridge: one gigantic steel truss arch springing from two near-vertical rocky cliffs of a deep V-shaped Himalayan gorge, flat railway deck on slender steel piers standing on the arch, a modern white-and-blue passenger train crossing. Earthquake moment: big rocks and dust tumbling down the shaking cliffs, cracks across the foreground rock — bridge and train intact. Low angle from the river.
Keep the TOP 22% of the frame as clean bright blue sky and the BOTTOM 22% as calm river and low rocks, with the whole bridge, arch and train inside the middle band, for large text above and below.
```

## 편집으로 글자를 넣을 때 (클라우드에서 가능)
- Font: Noto Sans Devanagari Black (Google Fonts).
- Outline thickness about 1/12 of the font size.
- Top line about 220 px and bottom line about 230 px, at 1672 px frame width.
- If you upload the image to git, the cloud places the text the same way as in `thumb_v2`.
