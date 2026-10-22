# 7편 컷 계획 v7 (스킬 점검 반영, 실제 나레이션 기준, 2026-10-22)

shot_plan_v6를 저장소 스킬 전체와 대조해 고친 판이다. 대조한 스킬: CHANNEL, cheezon-video(+shot-plan), video-camera, video-screen, video-edit, video-text, video-sound, video-verify, video-story, channel-video-style, episode-pipeline, encyclopedia-video.

## v6에서 고친 것
| # | v6 문제 | 근거(스킬) | v7 |
|---|---|---|---|
| 1 | 초를 힌디 문장 길이로 추정 | CHANNEL 필수 분량 하한: 실측 기준 | `review_edit/narr_timing.json` 실측으로 다시 계산 (총 403.5초) |
| 2 | S03·S06·S14·S15가 v5에서 0.67~0.98배로 감속돼 있었는데 계획이 이를 안 다룸 | video-edit: 속도 급변·감속으로 채우기 금지 | 모든 컷 1.0배. S03은 **s03b** 추가, S14·S15는 v6 추가 클립으로 해결 |
| 3 | S19(6.4초)·S25(4.0초)·S28(4.6초)이 클립 1개 → 2~3초 컷을 하려면 같은 클립이 붙어야 함 | 사용자 규칙: 같은 클립 컷 연속 금지 | **s19b**, **s28b** 추가. S25는 S01과 같은 질문이라 h1의 안 쓴 구간(7~9.5초)을 회수 컷으로 사용 (video-edit: 의도적 회수 허용) |
| 4 | S22 여유 0% | CHANNEL: 편집 손실 여유분 | **s22c** 추가 |
| 5 | s23b(형제 촬영)·s23d(경찰 체포)가 실존 인물 재현 | CHANNEL·video-screen: 실존 인물 재현 금지 | s23b=촬영 장비 옆 캠핑카(사람 없음), s23c=뒷모습 군중, s23d=압수 차량 보관소 |
| 6 | "추가 클립 30개" | 실제 목록은 27개 | 27 + 4 = **31개 신규** + m2~m5 재생성 4개 = **35장/35클립** |
| 7 | 도입 S01·S02 컷이 v5에서 0.9~1.2초 | 사용자 규칙: 컷 2~3초 | 아래 "결정 필요" 참고 |

## 문단별 배정
| 문단 | 실제 나레이션(초) | 컷 수(2~3초) | 클립 (**굵게**=신규/재생성) | 최대 확보(초) | 여유 |
|---|---|---|---|---|---|
| S01 | 2.3 | 1~1 | h1 | 3 | +29% |
| S02 | 8.2 | 3~4 | h2, h3, h4, m1, **m2**, **m3s**, **m4**, **m5** | 72 | +781% |
| S03 | 12.5 | 5~6 | PB, s03, **s03b** | 22 | +76% |
| S04 | 17.4 | 6~8 | s04a, s04b, s01, s04c, M3 | 45 | +159% |
| S05 | 4.5 | 2~2 | s05, s02 | 18 | +299% |
| S06 | 18.2 | 7~9 | s06a, s06b, **s06c** | 27 | +49% |
| S07 | 13.0 | 5~6 | s07a, s07b | 18 | +39% |
| S08 | 14.7 | 5~7 | s08, **s08b**, **s08c** | 27 | +84% |
| S09 | 19.8 | 7~9 | s09, **s09b**, **s09z** | 27 | +36% |
| S10 | 10.9 | 4~5 | s10, **s10b** | 16 | +47% |
| S11 | 19.3 | 7~9 | s11a, s11b, **s11c** | 27 | +40% |
| S12 | 17.4 | 6~8 | s12, **s12b**, **s12c** | 27 | +55% |
| S13 | 12.0 | 4~5 | s13, **s13b** | 18 | +50% |
| S14 | 18.4 | 7~9 | s14a, s14b, **s14c** | 23 | +25% |
| S15 | 17.1 | 6~8 | s15a, s15b, **s15c** | 23 | +34% |
| S16 | 16.9 | 6~8 | s16a, **s16c**, **s16d** | 27 | +60% |
| S17 | 22.3 | 8~11 | s16b, s17a, s17b | 27 | +21% |
| S18 | 8.7 | 3~4 | s18, **s18b** | 18 | +107% |
| S19 | 6.4 | 3~3 | s19, **s19b** | 18 | +182% |
| S20 | 14.8 | 5~7 | s20, **s20b** | 18 | +22% |
| S21 | 14.5 | 5~7 | s21a, s21b | 18 | +24% |
| S22 | 15.6 | 6~7 | s22, **s22b**, **s22c** | 27 | +73% |
| S23 | 27.6 | 10~13 | s23, **s23b**, **s23c**, **s23d** | 36 | +30% |
| S24 | 28.5 | 10~14 | s24, **s24b**, **s24c**, **s24d** | 36 | +26% |
| S25 | 4.0 | 2~2 | s25, h1(7~9.5초, S01 회수) | 9 | +122% |
| S26 | 25.8 | 9~12 | s26, **s26b**, **s26c**, **s26d** | 36 | +40% |
| S27 | 8.2 | 3~4 | s27, **s27b** | 18 | +119% |
| S28 | 4.6 | 2~2 | s28, **s28b** | 15 | +226% |

예상 총 컷 수(평균 2.5초): 약 161

"최대 확보" = 클립당 컷 3개 이하·컷 3초 이하·같은 클립 연속 금지 조건에서 낼 수 있는 최대 초. 사용 구간 제한(PB 0~7, s03 0~6, s10 0~7, s14a/b 3~10, s15a 0~2+5~10, s15b 0~7, s28 4~10)을 반영했다. 신규 클립은 10초 전체 사용 가능으로 가정했으며, 생성 후 실제 쓸 구간으로 다시 계산한다.

## 카메라 (video-camera §0)
- 무빙은 v5의 9개(PB, s03, s04b, s10, s15a, s17b, s19, s24, s28)에 신규 2개(s06c slider right, s26b slider left)를 더해 80클립 중 11개(약 14%)다.
- 나머지는 모두 고정이다. 3D(s09z)는 열 흐름만 움직인다.
- 같은 방향 무빙은 연속되지 않는다.

## 기준 그림 (Flow에 첨부)
| 기준 | 대상 |
|---|---|
| PB | 버스 실사 장면 전부 (m2~m5 포함) |
| s09 | 벽 단면 3D (s09z) |
| s19 | 판데이 캠핑카 (s20b, s22b, s26b) |
| s22 | RTO 사무실 (s22c) |
| s23 | E Bull Jet 캠핑카 (s23b~d) |
| s24 | 카라반 파크 (s15c, s24b~d) |

## 파일
- **이미지 프롬프트:** `images/prompts_v6.json`. Generator: `make_prompts_v6.py`. Save to PC as `BUS\img3d\v6_{id}.png`.
- **영상 프롬프트:** `video/vprompts_v6.json`. Generator: `make_vprompts_v6.py`. Save to PC as `BUS\clips_v6\{id}.mp4`.
  - m2~m5 replace the old v5 versions; once the new ones pass review, delete the old v5_m2~m5 images and clips.
- **편집:** `review_edit/edit_v5.py` still needs these changes before reuse (not yet edited):
  - Add the new clips to `PLAN`.
  - Remove the 0.6× slowdown and the "영상 부족" label code. If footage is short, stop and report instead.
  - Add the h1 callback range for S25.

## 결정 필요
- **도입 컷 길이:** S01+S02 = 10.5 s. Two options:
  - **2–3 s cuts:** about 4–5 cuts in total. That uses only 1–2 of the glamour shots (h1–h4) and 2 of the misery shots (m1–m5). The leftover m clips become spares.
  - **v5-style 1 s montage:** 9 cuts. This breaks the 2–3 s rule.
- **m2~m5 내용:** the original prompts are not in the repo, so the m2~m5 content is my guess from the script: heat, sewage, mould/condensation, eviction. Check it against the PC images before generating.
