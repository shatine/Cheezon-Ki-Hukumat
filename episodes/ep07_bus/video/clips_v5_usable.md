# 7편 v5 Muse 클립 (2026-10-21)

All 40 clips are done and checked.
- **PC location:** `BUS\clips_v5\{id}.mp4`
- **Format:** 10 s each, 1216x672
- **Watermarks / children:** none
- **First frame:** matches the source image in every clip

## 편집 때 쓸 구간 (나머지는 10초 전체 사용 가능)
| 클립 | 쓸 구간 | 이유 |
|---|---|---|
| PB | 0–7 s | 끝에서 어두워짐 |
| s03 | 0–6 s | 끝에서 한 대에 너무 다가감 |
| s10 | 0–7 s | 끝에서 어두워짐 |
| s14a, s14b | 3–10 s | 초반에 살짝 줌인 |
| s15a | 0–2 s + 5–10 s | 3초 무렵 바닥에 물이 차는 오류 |
| s15b | 0–7 s | 8초부터 배경이 검어짐 |
| s28 | 4–10 s | 초반엔 오히려 다가감 |

## 약하게 남은 문제
- s07b and s08 still have a very slight zoom-in.
- s07a (Y89) and s13 (Y75) have slightly dark interiors, already present in the source images.

## 재생성 기록
| 클립 | 시도 | 내용 |
|---|---|---|
| M3 | 3 | 줌인되면서 모양 변함 → 카메라 고정본 |
| s06b | 4 | 버스 전체가 주황색이 되고 옆면이 닫힘 → 그림에 있는 화살표만 움직임 |
| s14b | 4 | 생성 실패 → 문구 완화 |
| s04b, s05, s07b, s13, s16b | 2 | 카메라가 밀리거나 패닝되거나 Muse가 거부함 |

- **s04b:** changed the move from push past to a slow glide down the aisle.
- **s13:** generated with the person standing instead of walking.

## PC 파일
- **Report:** `_clips_v5_report.md`
- **Check sheets:** `_sheet`
- **Versions before regeneration:** `_try`
