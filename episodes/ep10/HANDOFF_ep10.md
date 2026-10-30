# 10편 인계: 벵갈루루 폐식용유 → 트럭 연료 (로컬 단독, 2026-10-30)

Read first: `backup_portable/` (all of it), then `WORK_ORDER_ep10.md`, then this file.
- Until 2026-11-05 the local session on the PC does everything alone (no cloud session).

## 확정 사항
- **Topic (user, 2026-10-30):** Bengaluru: grease poured into kitchen drains blocks the sewers → kitchens collect used oil separately → the same oil becomes fuel for logistics trucks.
- **Opening line (user, 2026-10-30):** "하수구를 막는 기름으로 어떻게 트럭을 달리게 했을까요?"
- **Hindi (recommended, waiting at G1):** सीवर जाम करने वाले तेल से ट्रक कैसे दौड़ाए?
- **Thumbnail draft (waiting at G1):** `thumbnail/thumb_draft_v1_1280x720.jpg`
  - Red top line: सीवर जाम करने वाले तेल से
  - Yellow bottom line: ट्रक कैसे दौड़ाए?
  - Background: `CB\thumb\thumb_bg_3.png`.
- **Reference videos:** `opening_candidates.md`, `refs/*.txt`, `refs_analysis.md`
  - BBC Fatberg: 239만 views.
  - TED-Ed Biodiesel: 111만 views.
  - MR. INDIAN HACKER: 929만 views.
- **Facts:** `research/facts_v1.md`.
  - The weakest link is the trucks: trucks running on Bengaluru kitchen oil could not be confirmed (F20).
  - What is confirmed: McDonald's India's refrigerated trucks in Mumbai (2018, "soon in Bengaluru").

## 경로·도구
- **CB:** `D:\youtube\7. Cheezon Ki Hukumat\episodes\10_bengaluru_used_oil\`
- **Flow project:** `https://flow.google.com/project/39479e17-1555-4816-b12b-2ac9ae625c66` (Flow moved from labs.google to flow.google.com).
  - Nano Banana 2.1, 16:9, x1, 0 credits.
- **Saving images:** run `python CB\flow_recv.py` (port 8765; `sendTile(idx, name)` in the page saves to `img_raw` / `img` / `img_review`).
- **Thumbnail text:** `thumbnail/make_thumb_v1.py`.
  - This PC's Pillow has no raqm, so the text is drawn with headless Chrome.
  - Fonts: `D:\youtube\7. Cheezon Ki Hukumat\tools\fonts\`.

## 단계 상태
| 단계 | 상태 | 결과 |
|---|---|---|
| 1 도입부·썸네일 | **G1 대기** | Hindi A/B/C, 3 thumbnail drafts (3 recommended), title direction |
| 2 대본 | 대기 | — |
| 3 TTS | 대기 | — |
| 4 계획 | 대기 | — |
| 5 이미지 | 대기 | — |
| 6 영상 (Muse) | 대기 (G3 승인 필요) | — |
| 7 편집 | 대기 | — |
| 8 업로드 문구·썸네일 | 대기 | — |

## 다음 세션이 할 일
1. Get the user's G1 answers:
   - the Hindi line;
   - the thumbnail draft;
   - whether master reference images may be uploaded to the Flow project;
   - how to handle the truck link (F20).
2. Step 2: the script (`skills/step2_script.md`), starting from `research/facts_v1.md`.

## 사용자 승인 기록
- 2026-10-30: topic and opening line confirmed (`WORK_ORDER_ep10.md`).

## 사용자 성향
- Do not make the user answer questions you can resolve yourself. Report briefly in Korean with a table.
- Strict review. Bigger numbers. Very large thumbnail text. Make the whole list, then report once.
