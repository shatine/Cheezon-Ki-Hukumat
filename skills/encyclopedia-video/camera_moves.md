# 카메라 무빙 플레이북 (Grok Imagine 프롬프트용)

한 클립 = 3비트(앵글 3개). 비트마다 "복합 무빙" 1개를 쓰고, 비트 사이는 연결 기법으로 잇는다.
Grok 공식 가이드상 **한 비트에 카메라 경로는 하나**, 비트는 순서대로 쉼표/시간표로 나열해야 잘 따른다.

## 1. 복합 무빙 (두 축 이상을 동시에)

| 이름 | 프롬프트 표현 | 효과 | 쓰는 곳 |
|---|---|---|---|
| 버티고(돌리 줌) | dolly zoom: camera dollies in while zooming out, background stretches | 현기증·깨달음의 순간 | "문제는 여기서 생깁니다" 같은 반전 |
| 페데스탈 업 + 틸트 다운 | camera pedestals up while tilting down, keeping the subject centered as the world opens below | 피사체를 붙잡은 채 전체 드러내기 | 폰 → 도시 전경 |
| 페데스탈 다운 + 틸트 업 | camera sinks low while tilting up, subject towers over frame | 위압감·스케일 | 위성, 관제탑, 747 |
| 크레인 오버 더 헤드 | crane rises over the subject's head and tilts straight down into a top-down view | 인물 → 지도 시점 전환 | 사람 → 지도 |
| 오빗 + 푸시인 | slow 180° orbit while pushing in | 대상에 대한 긴장 상승 | 위성, 원자시계 |
| 에어리얼 풀백 (매크로→우주) | continuous pullback from macro detail to orbit, powers-of-ten style | 스케일 폭발 | 파란 점 → 지구 |
| 슈퍼 돌리 인 | ultra-long smooth dolly in from wide to extreme close-up | 핵심으로 빨려 들어감 | 시계 부품, 칩 |
| 더치 롤 | camera rolls into a dutch angle while pushing in | 불안·오류 | 007편, GPS 오차 |
| FPV 다이브 | FPV drone dives down and skims along the surface at high speed | 속도·몰입 | 하늘길, 도로, 전파 따라가기 |
| 패럴랙스 트럭 | lateral tracking past foreground objects, strong parallax | 입체감 | 도시, 공항 |
| 레이지 수전(턴테이블) | subject rotates while camera slowly cranes | 제품 쇼케이스 | 위성, 수신기 |
| 하이퍼랩스 무브 | hyperlapse while camera travels forward | 시간 압축 | 하루 두 바퀴, 교통 흐름 |

## 2. 강조 액센트 (비트 안에서 짧게)

- **크래시 줌 / 스냅 줌**: sudden crash zoom onto ... — 숫자·결정적 단어 순간.
- **랙 포커스**: focus racks from foreground ... to background ... — 시선 이동.
- **스피드 램프**: motion ramps into slow motion, then snaps back to speed — 결정적 순간 멈춤.
- **요요 줌**: quick zoom in and out — 리듬감 (남용 금지).

## 3. 비트 연결 (한 클립 안에서 앵글 바꾸기)

- **스루 오브젝트**: camera flies through the screen / window / cloud into the next view — 끊김 없는 앵글 전환. (가장 추천)
- **휩 팬**: fast whip pan with motion blur reveals ... — 컷 대신 전환.
- **매치 무브**: 앞 비트의 움직임 방향을 다음 비트가 이어받음 (up → up).
- **매크로→와이드 컨티뉴어스**: 한 번의 연속 무빙으로 3개 앵글을 지나감(원테이크).

## 4. 3비트 설계 원칙

1. **비트1 훅**: 극단적 근접 또는 극단적 원경. 첫 1초에 움직임 시작.
2. **비트2 전개**: 복합 무빙으로 공간 드러내기 (페데스탈+틸트, 오빗+푸시).
3. **비트3 임팩트**: 스케일 전환 또는 액센트 (돌리 줌, 에어리얼 풀백, 크래시 줌).
4. 비트 경계는 나레이션 문장 경계에 맞춘다 (1.2배속 확정 후 초 단위로 배치).
5. 흔들림 금지: smooth, stabilized, gimbal-like. 핸드헬드는 긴장 장면만.
6. 연속 비트는 방향을 바꿔 리듬 만들기 (들어가기 → 올라가기 → 빠지기).
7. 숫자·글자·정확한 도형은 영상에 넣지 않고 모션그래픽으로 얹는다.

## 5. S01 개선 예시 (15초, 원테이크 3비트)

```
[0-4s] Extreme macro of a smartphone screen at night: a single blue dot pulses on a dark abstract map; camera does a super slow dolly in, then the camera flies through the screen.
[4-9s] Emerging above a neon city street at night, camera pedestals up while tilting down, keeping a lone pedestrian holding a glowing phone centered as rivers of car lights open up around them, strong parallax.
[9-15s] Continuous aerial pullback, powers-of-ten style: city grid shrinks to a glowing map, clouds pass, rising to the curve of Earth at night where tiny satellites glint in orbit.
One continuous camera move, smooth, stabilized, cinematic, photorealistic. Audio: city night ambience, a soft ping, swelling low whoosh. no dialogue, no voice, no narration, no speech, no text, no logos
```

출처: Higgsfield Camera Controls 프리셋 목록 (https://higgsfield.ai/camera-controls), Replicate Grok Imagine 1.5 프롬프트 가이드 (https://replicate.com/blog/grok-imagine)
