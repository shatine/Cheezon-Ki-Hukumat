# 10편 도입부 문장 + 썸네일 (1단계, 2026-10-30)

## 확정 도입부 문장 (사용자 2026-10-30)
**"하수구를 막는 기름으로 어떻게 트럭을 달리게 했을까요?"**
- Opening line = central question = thumbnail text = what the title points to. The wording is not changed.

## 힌디어 (같은 뜻, 덧붙인 말 없음)
| # | 힌디어 | 한국어 직역 | 비고 |
|---|---|---|---|
| ★ A | सीवर जाम करने वाले तेल से ट्रक कैसे दौड़ाए? | 하수구를 막는 기름으로 트럭을 어떻게 달리게 했나요? | **추천.** सीवर (sewer) is the everyday word in Indian cities. दौड़ाए = made them run, which matches "달리게" |
| B | नाली जाम करने वाले तेल से ट्रक कैसे चलाए? | 배수구를 막는 기름으로 트럭을 어떻게 움직였나요? | नाली = a small drain (gutter). चलाए is softer than दौड़ाए |
| C | जो तेल सीवर जाम करता है, उससे ट्रक कैसे दौड़ाए गए? | 하수구를 막는 그 기름으로 트럭이 어떻게 달리게 됐나요? | Spoken but long (9 words); too long for the thumbnail |

**Thumbnail split (A):**
- Top, red (the problem): `सीवर जाम करने वाले तेल से` (하수구를 막는 기름으로)
- Bottom, yellow (the question): `ट्रक कैसे दौड़ाए?` (트럭을 어떻게 달리게 했나?)

## 썸네일 시안 (`thumbnail/make_thumb_v1.py`)
- Text-free backgrounds made in Flow: `CB\thumb\thumb_bg_1.png` to `thumb_bg_3.png` (always kept).
- Drafts: `CB\thumb\draft_bg1.jpg` to `draft_bg3.jpg`. Small size: `draft_bgN_320.jpg`, `drafts_320_sheet.jpg`.
- **Recommended: background 3 → `thumbnail/thumb_draft_v1_1280x720.jpg`.**

| 배경 | 그림 | 320×180 판정 |
|---|---|---|
| 1 | Roadside drain with yellow grease + white truck | Both lines readable, but the bottom line hides the grease, so only a truck shows → drop |
| 2 | Manhole with a grease lump + red truck | Same: the bottom line covers the grease lump → drop |
| ★ 3 | Cut-open sewer pipe packed with yellow grease (left) → a gold stream of oil → white truck's fuel tank (right) | Pipe, grease and truck stay visible; **the whole question shows in one picture**. Both lines readable in under 2 s |

- Text: Noto Sans Devanagari Black, black outline (1/7 of the font size), 30 px margins at top and bottom (1280×720). Top line about 100 px, bottom line about 150 px (fitted to the width).
- The text is drawn with headless Chrome because this PC's Pillow lacks Devanagari shaping (raqm). Conjuncts (ट्रक) and the nukta (ड़) render correctly.

## 제목 방향 (최종은 8단계)
- Same question as the opening line: "Sewer-clogging oil → running trucks: how?"
- HI draft: `सीवर जाम करने वाले तेल से ट्रक कैसे दौड़ाए? | बेंगलुरु`
- EN draft: `How Did Bengaluru Run Trucks on the Oil That Clogs Its Sewers?`

## 처음 30초 영상 계획 (초안)
1. A kitchen pours a wok of used oil into the sink → it runs into the drain.
2. Under the street: oil cools and turns white and hard inside the pipe (3D cross-section).
3. A sewer overflowing onto a Bengaluru street.
4. Contrast: a logistics truck leaving at dawn. The fuel cap closes.
5. Back to the oil: the same yellow liquid, in a collection drum.
