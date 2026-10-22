---
name: video-camera
description: 영상 생성(Omni 1.1/Flow, Grok, Veo) 프롬프트의 카메라 무빙 규칙. 장면 프롬프트를 쓸 때 항상 사용 — 장면 내용(모듈 A)과 카메라 지정(모듈 B)을 나눠 쓰고, 우리 장르(시네마틱 해설 다큐)에 맞는 무빙만 고른다. 전체 46개 무빙 목록은 refs/camera-movement-library-v2.md.
---

# 카메라 무빙 (사용자 제공 자료 v2를 우리 채널에 맞춤, 2026-10-08)

현재 규칙은 [CHANNEL.md](../../../CHANNEL.md)와 [cheezon-video](../cheezon-video/SKILL.md)다. 정밀 원리는 고정 구도도 허용하며 카메라 이동은 장치 작동을 대신하지 않는다.

## 0. 최우선: 카메라 무빙은 적게 (사용자 격노 2026-10-20, 7편 폐버스)

- 7편 69클립 전부에 "One single continuous camera movement … framing keeps changing clearly"를 붙여 모든 장면이 arc/slider/zoom으로 계속 돌았다 → "멀미 난다, 어지러워 못 보겠다". **이 문구는 금지.**
- **3D 단면·원리 도해는 카메라 고정(`locked-off static shot`)이 기본.** 움직임은 원리의 흐름에 쓴다: 열이 흐르고, 물이 차고, 선이 그려지고, 부품이 조립·분리된다. 카메라가 대신 움직이지 않는다.
- 카메라 무빙은 한 편 전체의 약 1/4 이하, 연속 두 클립에 같은 방향 무빙(좌→우, 우→좌 번갈아 돌리기) 금지. `arc`/`orbit`은 한 편에 1~2번만.
- 무빙을 쓸 때도 아주 느리게(`very slow, barely noticeable`), 끝은 정지 구도.

원본 전체(장르별 예시·46개 무빙 목록): `refs/camera-movement-library-v2.md`.
이 문서는 원본 중 **우리가 쓰는 부분 + 채널 규칙과 부딪히는 곳**만 정리한다. 화면 규칙은 `video-screen`, 스타일·Flow 조작은 `channel-video-style` §7.

## 1. 우리 장르

**시네마틱 해설 다큐멘터리 (cinematic explainer documentary)** — 원본의 "Educational & Documentary"에 속한다.
- 해설의 질문을 장면으로 증명한다. 상황은 현장 컷, 내부 원리는 단면·흐름·상태 변화로 보여준다. 인터뷰·대사 생성은 기본 작업이 아니다.
- 실사 인도 장소·어른(중간·먼 거리) + 물체 클로즈업 + 숫자·원리 도해.
- 무빙 원칙: 느리고 안정적, 한 클립에 무빙 하나, 피사체는 화면 가운데 70% 안. 액션·공포·SF 무빙(whip pan, crash zoom, handheld, snorricam, FPV)은 쓰지 않는다. 예외: "상식 뒤집기" 순간 1번 정도 `fast zoom in`(사람 얼굴이 아닌 물체로).

## 2. 프롬프트 틀 (모듈 A + 모듈 B)

```
[모듈 A: 장면 — 누가/무엇이, 어디서, 무엇을 하는지, 빛, 분위기]. [카메라 태그]. Movement: [방향·경로]. Speed: [속도]. Framing: [구도]. End: [끝 구도].
+ 채널 접미사 (photorealistic cinematic, warm golden light … Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark.)
```
- 속도와 끝 구도(End)를 꼭 쓴다 → 생성 안정성이 올라간다.
- 기준 그림(소재)을 붙일 때 모듈 A 첫 문장은 "The same … from the reference image (옷·소품)".

## 3. 우리 채널 규칙과 부딪히는 곳

| 원본 권장 | 문제 | 우리 방식 |
|---|---|---|
| 인터뷰 `slow zoom in` toward the subject's face | 얼굴 1/4 초과, 대사 생김 | 사람 장면은 `locked-off static shot` 또는 `side tracking shot`, Framing에 "face stays small, figure ≤ 1/3 of frame height" |
| `dolly in`으로 사람에게 다가감 | Flow 시험(2026-10-08)에서 끝에 얼굴이 1/5까지 커짐 | 다가갈 땐 **사람 말고 물체·장소**로. 사람이 있으면 End를 "medium-wide shot" 으로 고정 |
| 다큐 `talking to camera` | 대사·립싱크 생김 | 쓰지 않음. 손·뒷모습·옆모습 |
| 야생·풍경 telephoto | 아이·군중이 끼기 쉬움 | "empty road / only a few adults far away" 명시 |

## 4. 장면 종류별 무빙 (해설 다큐 전용)

| 장면 역할 | 무빙 태그 | 쓰는 때 |
|---|---|---|
| 장소 소개·규모 | `drone push in`, `crane up`, `helicopter-style aerial shot` | 첫 장면, 새 장소 |
| 사람의 일상 행동 | `side tracking shot`, `locked-off static shot` | 기사·상인·노동자가 일하는 모습 |
| 물체 관찰(핵심 소품) | `slider right/left`, `arc right/left`, `slow zoom in`(물체로) | 트럭 그림, 경적, 도구, 문서 |
| 원리·속 보기 | `pass-through movement`, `macro slow zoom in` | 단면, 엔진 속, 돈 흐름 도해 |
| 시간 흐름·숫자 증가 | `locked-camera time-lapse` | "수십 년 동안", 교통량 |
| 상식 뒤집기(아하) | `fast zoom in`(물체), `dolly out` reveal | 문제 제시 → 진짜 이유 |
| 마무리·여운 | `drone pull back`, `crane up` | 끝 장면 |

## 5. 해설 다큐 기본 5무빙 (사용자 제공 2026-10-08, 인도 소재로 바꿈)

Movement/Speed/Framing/End 문장은 사용자 원문 그대로 둔다(검증된 문구). 모듈 A(장면)만 바꿔 쓴다.

| # | 역할 | 태그 | 언제 |
|---|---|---|---|
| 1 | 거대한 배경·스케일 제시 | `drone pull back` | 오프닝, 새 장소, 마무리 |
| 2 | 정밀 탐구·세부 관찰 | `slow zoom in` / `slider right` | 문서·도구·질감·숫자 근거 |
| 3 | 피사체 입체 조망 | `arc right` / `clockwise orbit` | 건축물·트럭·기계 한 대 |
| 4 | 공간·문맥 전환 | `push past` | 장(챕터) 바뀔 때, "그런데 진짜 이유는…" |
| 5 | 핵심 주제 밀착 | `dolly in` | 해설의 핵심 물체. **사람에게는 쓰지 않음**(얼굴 커짐) |

**1. drone pull back — 스케일**
```
A colourful truck-art truck parked alone at a roadside dhaba on an endless Indian national highway at dawn, mist over dry fields, cinematic bright natural daylight lighting. drone pull back. Movement: fly smoothly backward away from the subject or destination. Speed: controlled aerial retreat. Framing: keep the subject readable as more landscape appears. End: finish on a wider aerial composition.
```

**2. slow zoom in — 세부 관찰**
```
A close-up of an old hand-written transport permit and a brass truck horn on a worn wooden desk in a small Indian transport office, soft directional window light, no readable text. slow zoom in. Movement: slowly increase lens focal length toward a tighter frame. Speed: gradual and even. Framing: keep the main visual target readable as it becomes larger in frame. End: finish on a stable tighter composition.
```

**3. arc right — 입체 조망**
```
A fully decorated Indian truck with hand-painted panels, tassels and chrome bumper standing in a quiet truck yard at bright natural daylight, no people. arc right. Movement: move on a shallow curved path around the main subject toward the right side. Speed: smooth measured curve. Framing: keep distance, height and subject readability consistent while the angle changes. End: finish from a new right-side angle.
```

**4. push past — 공간 전환**
```
Moving through the open gate of a busy Indian truck-painting workshop into a wide yard where several adult painters work on truck panels far away. push past. Movement: move forward past a visible foreground object, edge or opening. Speed: smooth forward glide. Framing: let the foreground pass close to the lens while the space beyond becomes clearer, people stay small in the distance. End: arrive inside or beyond the foreground layer.
```

**5. dolly in — 핵심 물체**
```
The painted "eyes" motif and lemon-chilli charm on the front grille of an Indian truck, warm late-afternoon sunlight, no people. dolly in. Movement: move the camera physically forward in a straight line toward the main subject. Speed: smooth controlled push. Framing: keep camera height, lens direction and subject position consistent while distance closes. End: finish in a tighter composition.
```

- 시간 경과는 `locked-camera time-lapse`(아래 예시)로 고정 구도에서 빛·배경만 바꾼다.
- 사람이 나오는 장면에 1~5를 쓸 때: Framing 끝에 `people stay small, faces ≤ 1/4 of frame height` 추가. 5번(dolly in)은 사람 대신 그 사람의 물건(핸들, 찻잔, 공구)으로.

## 6. 카메라 용어 예시 (실제 질문·대상·근거에 맞춰 수정)

**장소 소개 — drone push in**
```
A long Indian national highway at bright natural daylight, a line of colourful truck-art trucks moving slowly, dhabas and dry fields on both sides. drone push in. Movement: fly forward low above the highway toward the leading truck. Speed: slow, steady aerial glide. Framing: wide shot, trucks centered in the middle 70%, lower 15% of the frame plain road. End: settle on a wide view of the leading truck's painted back panel.
```

**사람 행동 — side tracking shot**
```
The same truck driver from the reference image (sky-blue shirt, orange checked gamchha, thick moustache) walks along his parked truck, checking the tyres with one hand. side tracking shot. Movement: travel parallel to him from the side at waist height. Speed: calm, matching his slow walk. Framing: medium-wide, full body visible, face small in frame. End: hold a medium-wide shot as he stops at the front wheel.
```

**물체 관찰 — slider right**
```
Close view of the hand-painted back of an Indian truck: bright flowers, a pair of eyes, a lotus pattern, a brass bell hanging below. slider right. Movement: glide slowly to the right across the painted panel. Speed: smooth, museum-guide pacing. Framing: panel fills the middle 70% of the frame, paint texture crisp. End: settle centered on the brass bell. (No readable letters on the panel.)
```

**아하 순간 — fast zoom in (물체)**
```
A dusty truck horn button on a worn steering wheel inside an Indian truck cabin, clear natural dashboard lighting. fast zoom in. Movement: one quick decisive zoom straight to the horn button. Speed: fast, punchy, then still. Framing: horn button centered. End: hold a sharp close-up of the button, hands out of frame.
```

**시간 흐름 — locked-camera time-lapse**
```
A busy Indian highway toll plaza from a high side angle, trucks queuing and passing. locked-camera time-lapse. Movement: none, camera fixed. Speed: time accelerates from afternoon to night, headlights becoming light trails. Framing: wide, toll booths centered. End: night scene full of light trails.
```

**마무리 — drone pull back**
```
The same truck driver from the reference image sitting at a roadside dhaba table at dusk with a glass of chai, his truck parked behind. drone pull back. Movement: rise and fly backward away from him. Speed: slow, contemplative. Framing: start medium-wide, figure small. End: wide aerial view of the glowing dhaba beside the endless highway.
```

## 7. 점검

- 클립 하나에 무빙 태그 하나. 두 개를 섞으면 Omni·Veo가 엉뚱하게 섞는다.
- 사람 장면 End에 "medium-wide" 또는 "figure small" 이 있는가.
- 원리·숫자 장면은 카메라가 거의 멈춰 있어야 편집에서 숫자·화살표를 얹기 쉽다.
- 생성 후 시작·중간·끝 프레임에서 부품 구조, 변화 방향, 다음 컷 연결, 얼굴 크기·글자·자막 가림을 확인한다.
