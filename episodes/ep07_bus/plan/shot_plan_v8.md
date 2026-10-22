# 7편 컷 계획 v8 (최신 Codex 스킬 반영, 2026-10-22)

v7을 최신 cheezon-video(장면 분량 부족 재발 방지, 생성 전 필수 확인, 정지·중복 금지, 분량 하한), shot-plan, bhopal-production-lessons에 맞춰 문장 단위로 다시 만들었다. v6·v7 문서는 이 판으로 대체했다.

- **문장별 표:** `shot_table_v8.md` (88문장 전부. 시작·끝·초, 컷별 클립과 소스 구간, 기준 그림, 화면 변화)
- **컷 목록:** `shot_list_v8.json` (컷별 출력 프레임, 소스 시작/끝 초·프레임, 1.0배속)
- **생성·점검:** `plan_v8.py`. 프롬프트나 쓸 구간(USE)을 바꾸면 다시 실행한다. 규칙을 하나라도 어기면 실패 목록을 출력한다.
- **편집:** `review_edit/edit_v8.py`가 shot_list_v8.json을 그대로 렌더한다. 감속·프레임 유지·"영상 부족" 표시는 없고, 소스가 없거나 짧거나 겹치면 렌더 전에 멈춘다.
  - 2026-10-22 클라우드에서 합성 클립·무음으로 시험했다. 158컷, 1920×1080, 30fps, 12136프레임(404.5초)이 계획과 일치했다.
  - 실제 클립·음성·자막 품질은 시험하지 않았다.

## v7에서 바뀐 것
| 스킬 요구 | v8 |
|---|---|
| 문장마다 필요 초수, 화면 변화, 기준 그림, 클립 수, 예상 사용 구간을 기록 (생성 전 필수 확인) | 문단 표 대신 88문장 표로 바꿈 |
| 다른 내용의 여분 클립으로 특정 구간의 부족을 메우지 않음 | 클립을 문장 내용에 맞춰 배정. 그 결과 클립이 모자란 곳 3군데를 찾아 신규 3개 추가 |
| 같은 행동은 연속 소스 프레임 사용, 누적 경계로 프레임 계산 | 같은 클립은 앞 컷이 끝난 지점부터 이어 쓰고, 출력 경계는 누적 프레임으로 반올림 |
| 10초 초과 구간은 분할 | S17c(11.2초)·S23b(10.9초)·S24c(11.9초)를 각각 4컷으로 나눔 |
| 편집 손실 여유 | 클립 끝 0.05초는 쓰지 않음 |

신규 3개:
- **s06d (버스 손잡이도 뜨거움):** S06c(4.3초)의 손잡이 클립이 하나뿐이라 4.3초 한 컷이나 같은 클립 연속이 됐다.
- **s21c (캠핑카 물탱크가 빔):** S21a의 물이 떨어지는 장면.
- **s23e (견인되는 캠핑카):** S23(27.6초)이 클립 4개로는 모자랐다.

## 숫자 (CHANNEL 분량 하한 기록 항목)
- **나레이션 실측:** 403.6초 (narration_hi.wav). Video length is 404.5 s, including a 1 s tail.
- **영상 도구:** Muse, 10 s per clip, 1216×672.
  - The clip length is measured from the v5 output; check the current UI setting before generating.
- **컷과 클립:** 158 cuts, each 2.00–3.03 s. 79 clips are used.
  - Each clip gives at most 3 cuts, and no two adjacent cuts come from the same clip.
- **신규·재생성:** 38 images / 38 clips.
  - New: 34 (the 31 from v7 plus s06d, s21c, s23e).
  - Remakes: m2, m3s, m4, m5.
  - The plan uses 36 of them; m4 and m5 are unused (see 결정 필요 below).
- **카메라:** 11 of the 79 clips used have camera movement (14%), covering 24 of the 158 cuts (15%). The rest are locked. No same-direction move appears in two adjacent cuts.
- **Status:** these are pre-generation numbers. After generation, put each clip's real usable range into USE and run plan_v8.py again; the plan passes only if there are no errors.

## 생성 순서 (스킬 규칙)
1. **Flow 이미지:** `images/prompts_v6.json`, 38 images, generated one at a time.
   - Keep the Nano Banana 2.1 / 16:9 / x2 setting.
   - Submit the next request only after the previous output has fully finished and passed review.
   - Attach the reference image named in `ref`.
   - Save to PC as `BUS\img3d\v6_{id}.png`.
2. **검수:** check every image for body proportions, part connections, cut-away layers, consistency with the same bus, watermarks, broken text, children, and face size.
   - Hold back any image that fails, then fix it.
3. **Muse 영상:** `video/vprompts_v6.json`, one at a time.
   - Save to `BUS\clips_v6\{id}.mp4`.
   - Before resubmitting after a timeout, check whether a result already exists.
4. **영상 검수:** check the start, middle and end of each clip.
   - A generation error that changes the principle (a broken pipe reconnecting, a new part appearing, a changed shape) is excluded from usable footage.
   - Record the usable range in `USE` in `plan_v8.py`, then run plan_v8.py.
5. **편집과 검사:** run `edit_v8.py`, then video-verify over the whole video (0 s to the end).
   - Look for frozen frames, duplicates and loops.
   - Check cut boundaries and play the video through.
6. **삭제:** delete the old files listed in the handoff, plus the old v5_m2~m5 images and clips.

## 결정 필요
- **도입 컷 길이:** the plan currently uses 2–3 s cuts.
  - S01–S02 is 4 cuts: h1 → h2 → m1 → m3s. S05 uses m2 and s02.
  - h3, h4, m4 and m5 are unused, so m4 and m5 don't need to be generated.
  - For the v5-style 1 s montage instead, only the G list in plan_v8.py needs changing.
- **m2~m5 내용:** guessed from the script. Compare with the PC images before generating.
- **효과음:** pick from Myinstants during the editing stage. Not yet started.
