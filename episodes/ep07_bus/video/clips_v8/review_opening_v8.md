# EP7 도입 v8 — Flow 이미지 2장 + Muse 영상 4개 (2026-10-22, PC 세션)

## 이미지 (Flow, 기준 그림 v5_PB_1, 1376x768, 워터마크 제거)
| id | 파일 | 시도 | 검수 |
|---|---|---|---|
| o1 | images/v8/v8_o1_1.png | 1 | 같은 PB 버스, 크림 커튼·꼬마전구·나무 데크·차 마시는 부부, 얼굴 작음, 밝음 |
| o2 | images/v8/v8_o2_1.png | 1 | 처진 커튼·늘어진 전구·마른 화분·물통·웅덩이·머리 감싼 남자. 웅덩이가 뒤쪽이 아니라 앞바퀴 쪽 |

## 영상 (Muse 9227 사이드 채팅, 1개씩, 10초, 1216x672, 24fps)
밝기 = 1초마다 회색 평균(Y, 0~255).

| id | 파일 | 시도 | 밝기 Y (0→10초) | 검수 / 쓸 구간 |
|---|---|---|---|---|
| o1 | clips_v8/o1.mp4 | 2 | 94~102 | 0~5.4초 사용 가능(버스 앞부분·부부 작게 유지). 5초 이후 빠르게 밀고 들어가 부부가 커짐 → 6초 이후 쓰지 말 것. 1·2차 모두 같은 현상(컷은 아님, 빠른 전진) |
| o2 | clips_v8/o2.mp4 | 1 | 108~112 일정 | 10초 전부. 고정 카메라, 남자가 고개 들고 얼굴 닦음, 4초 무렵 마른 잎 날림 |
| PB | clips_v8/PB.mp4 | 2 | 120 → 0~6초 114~117 → 마지막 3초 110·104·96 | 조건부 통과. 1차(PB_try1, PC에만)는 119→69로 어두워지고 앞 그릴까지 접근해 탈락. 2차는 버스 전체가 거의 끝까지 화면 안, 마지막 3초 약간 어두워짐. 8초 이후 앞면에 작은 "KSRTC" 글자 보임 → 편집 시 확인 |
| s09z | clips_v8/s09z.mp4 | 1 | 152~154 일정 | 10초 전부. 고정, 열이 바깥 판→갈비뼈→안쪽 판으로 번짐, 단열재는 옅음. 왼쪽 바깥 열 화살표는 4초 무렵 사라짐 |

PC 원본: BUS\clips_v8\ (o1_try1.mp4, PB_try1.mp4 포함), 이미지 BUS\img3d\v8_o1_1.png, v8_o2_1.png

## 클라우드 재검수 (2026-10-22)
Checked the two images, a 1 s frame strip of each video, full-size frames at the key points, and brightness every 0.5 s.

| id | 판정 | 내용 |
|---|---|---|
| o1 이미지·영상 | 통과, 0~5.4초 | The frame at 5.4 s is fine: the couple is medium-small, faces not large. Brightness swings 86–103 with the light flicker, which is natural. |
| o2 이미지·영상 | 통과, **편집에서 좌우 반전** | o1 has the bus front on the left, o2 on the right. Cut together, the bus appears to turn around. Mirroring o2 puts the front on the left, and puts the door on the bus's left side, as on Indian buses, the same as o1. The small text on the front is unreadable, so mirroring causes no problem. |
| PB | 조건부, 10초 전부 사용 제안 | From about 5 s the camera curves round to a near-frontal view. The bus shape stays the same, and it reads as a natural approach. Brightness is 120 to 5.5 s, then falls gradually to 91 at 9.5 s. In the edit, brighten 5.5–10 s gradually to match the opening. From about 6.5 s, "KSRTC" and "KERALA STATE ROAD TRANSPORT CORPORATION" are clearly readable, spelled correctly, and they match the narration S03b (KSRTC). |
| s09z | 통과, 10초 전부 | Locked camera; heat spreads along the rib to the inner panel. The outer heat arrows disappear at about 3–4 s, but the rib stays hot, so the explanation still holds. The faint arrow over the insulation in the first 3 s is also in the reference s09. |
