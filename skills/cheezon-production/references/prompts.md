# 이미지·영상 프롬프트와 카메라 (7편 기준)

## 이미지 (Flow)
Flow는 한 장씩: 제출 → 완료 확인 → 검수 → 다음. 같은 대상(건물·차·장치·장소)은 **기준 그림을 반드시 첨부**한다.

**실사 머리말 (모든 실사 장면 앞에)**
```
Photorealistic cinematic still, bright clear Indian daylight, vivid natural Bollywood colours, sharp focus, 16:9. No text, no letters, no logos, no watermark. Adults only, people small or medium distance, faces not close-up.
```

**3D 도해 머리말 (원리 장면 앞에, 색 약속 포함)**
```
Clean bright 3D educational diorama render, soft studio light, white-grey background, saturated clear colours, 16:9, no text, no labels, no letters. Colour code: heat = red-orange glow arrows, cold = icy blue, clean water = bright blue, waste water = brown-grey, electricity = thick cable with glowing yellow core, moisture = small white droplets.
```

**같은 대상 고정 문구 (기준 그림 첨부 시, 대상 특징을 구체적으로)**
```
Using the reference image: the SAME retired Kerala KSRTC ordinary bus as the reference image: classic red-maroon body with one yellow band, rounded front, flat roof, long row of side windows, faded paint, no readable text, ...
```
3D 판:
```
Using the reference image: EXACTLY the same diorama and the SAME stylised 3D bus as the reference image (same shape, colours, window count, cut-away left side). ...
```

**문장마다 하는 일:**
- 그 문장의 뜻이 한눈에 읽히는 상태 변화·반응·클로즈업을 정한다.
- 사람은 "Indian adult, face small, seen from behind/side, only hands"로 쓴다.
- 실존 인물은 재현하지 않는다.
- 끝에 "no readable text"를 붙인다. 번호판·상표·간판이 생기기 쉬운 장면(차 앞면, 시내 거리)은 각도를 옆·뒤로 돌린다.

예시 31장: `tools/image_prompts_example.py`

## 영상 (Muse)
**틀:** `[장면 동작]. [카메라 태그]. Movement: … Speed: … Framing: … End: …` + 접미사

**고정 카메라 (기본, 3D 원리는 항상)**
```
[locked-off static shot]. Movement: camera completely still, no zoom, no pan. Speed: none. Framing: exactly the composition of the image. End: same frame.
```

**실사 접미사**
```
Photorealistic, bright midday daylight, vivid colours. Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark.
```

**3D 접미사**
```
Clean bright 3D educational render, white-grey studio background. Keep the exact same bus shape, colours and layout as the image. No new objects, no arrows, no text, no labels. Ambient sound only. No dialogue, no music, no watermark.
```

**3D 원리:** 카메라는 고정하고 열·물·냉기·전기 흐름만 움직인다. "Keep the exact same shape … No new objects"를 넣는다.

**밝기가 떨어질 위험이 있을 때:** "The lighting stays the same bright midday sun for the whole shot, no darkening, no fade."
7편 PB 영상은 이 문구를 넣고도 끝 3초가 조금 어두워져서 편집에서 보정했다.

## 카메라 규칙
- **무빙은 영상 클립의 약 2/10만.**
  - 7편 초기에 모든 클립에 무빙을 넣었다가 "멀미 난다"는 지적을 받았다.
  - "One single continuous camera movement …" 문구는 금지.
- **클립 하나에 무빙 하나**, 아주 느리게, 끝은 정지 구도. 같은 방향 무빙을 연속으로 쓰지 않는다.
- **사람 쪽으로 dolly in 하지 않는다.** 얼굴이 커진다. 7편 o1은 5초 뒤 빠르게 밀고 들어가서 0~5.4초만 썼다.
- **쓰는 무빙:**
  - slow dolly in: 대상·장소로 다가감
  - slider left/right: 줄지은 대상, 창
  - drone pull back: 장소 전체·마무리
  - macro slow zoom in: 물체의 원리, 예: 물병 결로
- **생성 후 측정:**
  - 1초 간격 프레임으로 모양·얼굴 크기·원리 방향·글자를 확인한다.
  - 0.5초마다 평균 밝기를 잰다.
  - 쓸 구간을 기록해 계획의 USE에 넣는다.
