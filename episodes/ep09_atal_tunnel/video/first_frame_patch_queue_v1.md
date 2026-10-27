# 영상 동작을 위한 첫 프레임 보완 큐 v1

**과거 설계 기록 — 현재 적용 지시가 아니다.** 아래 11개 장비 보완은 앞선 단계에서 이미지 정의에 적용됐다. 이후 원리43개를 `backup_portable/04_video_rules.md`의 고체 고정·빛/색 방식으로 고쳤으므로 아래의 삽입·굴착·분사·착좌·탄성 응답 문구를 다시 실행하지 않는다. 특히 p019는 하부 고체 위 **이미 연결된 얕은 임시 폐합**, p020은 하부 고체를 제거한 후기의 **이미 연결된 깊은 최종 폐합**으로 재설계했다. p038만 후기 진행 중 공정의 미완 접합부를 유지하며 빛으로도 틈을 메우지 않는다. 현재 권위 파일은 `images/prompts_v1.json`, `video/vprompts_v1_draft.json`, `WORK_ORDER_muse_v1.md`다. 아래 master SHA는 당시 스냅샷이며 현재 참조 식별자가 아니다. 현재 선택 원본·revision은 `images/reference_assets_v1.json`을 쓴다.

**상태: 이미지 담당자의 master 생성 대기/완료 후 일괄 적용할 목록. 이 문서 작성 시 실제 이미지·이미지 생성기·JSON에 적용됐다고 보고하지 않는다.** 현재 독립 master 생성은 이 큐 때문에 중단하지 않는다. 아래 11개는 아직 미생성인 후속 frame의 장비·공급 경로·받침 초기 배치만 보완한다.

수정 금지: 승인 한국어/힌디어/숫자/순서, master 6개의 형상·색·프롬프트, 남·북 포털 구분, 공통 3D 좌표계, 임시/최종 인버트의 단계 구분. `FRAME_INITIAL`의 해당 문장 키만 보완하고 이미지 생성기 → `prompts_v1.json`으로 재생성한다. 아직 생성하지 않은 frame을 영상에서 보충하는 지시가 아니다.

## 추가할 초기 상태

| frame ID | FRAME_INITIAL 키 | 보완 이유와 추가할 영어 문구 |
|---|---|---|
| p008 | S07d | 도구 없이 단단한 땅이 사라지는 동작을 피한다. `A compact schematic excavator is already supported on the firm left-hand bench. Its short mechanical arm and bucket touch only the edge of the next short solid patch below the canopy. A small existing muck receiver and continuous leftward removal route are visible on the supported floor. The next patch is still largely solid; the bucket has not made its first local stroke.` |
| p010 | S08c | 기존 이중 강관은 그대로 두고 짧은 대표 동작을 시작한다. `A compact ground-supported excavator, short arm and face-contact bucket already stand behind the face, with an existing small muck receiver to the left. One local grey transverse support is already held almost in its final place just behind the exposed edge by a visible supported positioning arm; only a small seating connection remains. Nothing is floating and no long area is already excavated.` |
| p011 | S09a | 굴착 → 즉시 지보가 재료 순간 생성으로 읽히지 않게 한다. `Show the compact excavator and its bucket already touching the short solid patch, supported on the existing left bench, with a visible receiving route for the small removed fragments. One local grey support is pre-positioned almost at its connection immediately behind the exposure and held by an existing mechanical positioning arm. Keep the forward ground solid and the prior support unchanged.` |
| p012 | S09c | 10초에 1m 전체가 지워지는 가속 굴착을 금지한다. `The existing ground-supported excavator bucket touches only the near edge of the highlighted narrow axial patch. A small receiver and continuous leftward muck route already exist. The highlighted patch remains solid except for its natural rough face; it is ready for one shallow representative bucket stroke, not a whole advance completed in seconds.` |
| p013 | S09d | 다음 구간의 새 동작을 기존 도구로 수행한다. `At the next adjacent strip, the same type of compact ground-supported machine and face-contact bucket are already present with a small muck receiver and removal path. A local support is already almost seated and held by a visible supported positioning arm. The previous rib and shotcrete stay installed and the next strip remains solid.` |
| p014 | S10a | 숏크리트가 공중에서 생기지 않도록 노즐의 공급 경로를 명확히 한다. `The existing shotcrete nozzle is connected to a visible supported feed hose. A little grey concrete is visible at the nozzle mouth, ready for a small controlled spray onto the still-rough target patch. Keep the hose physically continuous and do not coat the patch before the action.` |
| p019 | S12a | 임시 인버트가 늘어나며 닫히는 모핑을 피한다. `A short final grey connection component already rests on the still-solid lower bench beside the shallow temporary-invert end joint. A short supported guide or mechanical ram is aligned with it for one small seating movement. All parts already exist and are supported; the end connection remains slightly open. No deep final invert and no traffic road.` |
| p020 | S12b | 최종 깊은 인버트는 후속 단계에서 기존 재료 공급으로 작은 결합부만 채운다. `At the small later final-invert closing gap, a stable local form and a visible concrete feed hose/nozzle are already present. A little fresh grey concrete is already in the hose mouth and receiving form, ready for a small bounded flow. The lower excavation is already open and upper support remains fixed. No temporary upper floor, solid lower bench, traffic or claim of a precast-segment method.` |
| p032 | S17c | 계측이 지보를 마법처럼 생성하거나 띄우지 않게 한다. `The additional grey support already staged on firm ground is held by a visible supported guide or positioning arm, aligned almost at its prepared local connection. A continuous supported placement path is visible for a small final seating movement. Observation targets and previous-position outlines remain passive; no automatic sensor repair.` |
| p038 | S19c | 후속 최종 바닥 공정을 상부 굴착 당시와 섞지 않는다. `The small deep-final-invert closing form is supported on the already opened stable lower base. A visible feed hose/nozzle and a little fresh grey concrete are already present at the local gap for a small bounded flow. Keep the retained upper support unchanged, with no temporary upper floor, lower bench or moving traffic.` |
| a001 | S20a | 관통이 벽 용해·순간 삭제가 되지 않게 한다. `The compact machine already present has a short supported face-contact tool at the edge of the pilot hole, and a small existing fragment receiving area directly below. The thin partition remains mostly intact, ready for only a few small fragments to be physically removed. Keep the same distant workers behind the existing safe barrier, with no ceremony, flags or identifiable real person.` |

콘크리트 공급 장비는 원리를 읽게 하는 일반적인 재현 도구이며, 특정 실측 시공 장비·형식·정확한 시공 방법을 새 사실로 주장하지 않는다. 영상은 대표적인 작은 한 동작을 정상 속도로 보여 준다. 실제 한 번의 1m 굴착, 상부/하부 전체 공정 또는 관통 전체를 10초에 끝냈다고 표현하지 않는다.

## 별도 첫 프레임 수정이 필요 없는 처리

- p021: 첫 프레임에 없는 힘 화살표나 입자를 동영상에서 추가하지 않는다. 기존 지반-라이닝 접촉부의 극소 물리적 정착과 탄성 응답만 다룬다. 구조는 계속 연결되고 차도는 평평하고 마르게 유지한다.
- a002/a003: 현재 첫 프레임 프롬프트는 국부 누수·배수구이며 검사 기술자가 없다. 화면 메모의 기술자를 동영상에서 새로 생성하지 않는다. 기존 물방울의 중력 낙하·배수구의 작은 물결만 보여 준다. 2024년 기록 설명용 재구성이며 2026년 실황으로 표기하지 않는다.
- p024/p025: 이미 채워진 작은 균열의 보라색 주입재는 그대로 둔다. 없는 주입호스를 새로 만들지 않고 기존 큰 물길의 배수만 움직인다.

## 적용 확인

1. 먼저 위 대상들이 여전히 미생성인지 실제 선택 기록에서 확인한다.
2. `images/make_prompts_v1.py`의 해당 `FRAME_INITIAL`만 수정한다. master의 참조 문구나 다른 장면 의미를 바꾸지 않는다.
3. 이미지 생성기를 실행하여 `images/prompts_v1.json`, 이미지 프롬프트 검사 결과를 갱신한다.
4. 실제 변경된 frame ID가 위 11개인지 확인한다. `FRAME_INITIAL`은 각 frame의 첫 `visual_source_id`를 사용하므로, 같은 문장이 포함된 인접 frame 전체를 무조건 바꾸지 않는다.
5. master 6개의 `prompt` UTF-8 SHA256이 아래와 같은지 확인한다. 큐 적용 때문에 바뀌면 중단하고 원인을 검토한다.
6. 영상 담당자에게 적용된 문장 키와 실제 frame ID 목록을 전달한다. 영상 담당자는 실제 새 JSON으로 초안을 다시 만들어 동작 계약 해시를 갱신한다.

| master | 큐 작성 시 prompt SHA256 |
|---|---|
| AT_S | `7d7f34b2f426f5961010a42d26beac6a2572360e188c3d5c3bb35d2d54a0ebf1` |
| AT_N | `f907e4bf7f88b55c6134c58f92428f64ed0b6a0d6b3a005c665ce42b4d8885ba` |
| AT_C | `39b682dd28e5486d32970a40b39cb6f3ad9e8018e290748c491139ac051f3387` |
| AT_INT | `fa72d49bffff2b3b043e832d9964deb967df6fb4ee54a59ffd56b2ec047d6c2f` |
| G3D_EXC | `8efa8bb00ca0e62bc6acffb2ec65c59e26def54bcd8d84a9e08eb27f619dabd6` |
| G3D_DEEP | `8b58d14d958be7ed92ddf6b4b6f07051c389274ae3485892efb963e2a0e4a4a9` |

**적용·선택·실제 시각 검수는 아직 완료로 표시하지 않는다.** `--ready`는 각 실제 선택 PNG 해시와 해당 동작 계약 해시에 대한 확인이 모두 있어야 통과한다. 현재 이 준비 작업에서 Muse 전송/영상 생성은 0개다.
