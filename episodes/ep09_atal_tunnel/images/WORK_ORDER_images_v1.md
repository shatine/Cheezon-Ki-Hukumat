# 9편 이미지 작업 지시서: 기준 그림 → 79개 컷 그림 → 원본 검수 (2026-10-27)

진행 현황: **선택4/85, 생성·검수 중.** AT_S 시도2·AT_N 시도3·AT_C 시도3·AT_INT 시도1 선택. G3D_EXC 시도1은 종단 공간 구분/초기 주입재, 시도2/3은 관 배치·직선성 문제로 보류하고 시도4 명시적 수정 준비·진행. 실제 상태는 `images/picks_v1.md`·`generation_progress.json`에 기록한다.

**사용자 최신 프로젝트 지시:** “flow프로젝트 안 옮겨도 돼 그냥 놔둬”(2026-10-27). 기존 고정 프로젝트를 유지한다. 점검 중 만든 빈 9편 프로젝트는 미사용 상태로 두며 복사·이동·삭제하지 않는다. 원래 편당 프로젝트 지침보다 이 명시 지시를 따른다.

**로컬 업로드 차단:** 확장의 파일 URL 접근 권한이 꺼져 있다는 실제 도구 오류를 확인했다. `setFiles`는 지정 시간 제한을 넘겨 대기했으므로 반복하지 않는다. 확장 권한을 임의 변경하지 않는다. 같은 프로젝트에 이미 있는 정확한 원본 revision을 실제 편집기 입력으로 사용한다.

**재업로드 호출 지연에 따른 같은 프로젝트 참조 경로:** 이 PC가 같은 Flow 프로젝트에서 직접 만든 선택 후보의 원본 자산은 이미 미디어 목록에 있다. 재업로드가 장시간 응답하지 않아, `reference_assets_v1.json`이 연결하는 **바로 그 선택 시도의 기존 Flow 원본 자산**을 직접 첨부한다. 원본과 선택 처리본의 차이가 우하단 처리 영역뿐인지 파일·픽셀로 확인한다. AT_S 시도2는 변경 픽셀0.272%, 범위 x1244–1313/y636–705로 확인했다. 실제로 첨부한 것은 Flow 원본이며, 처리 PNG를 업로드했다고 기록하지 않는다. 정리된 PNG는 편집·영상 첫 프레임의 선택 파일로 유지한다. 다른 후보나 다른 대상을 참조하는 대체가 아니다.

목적: 승인된 78문장과 실측 79컷에 필요한 **기준 그림 6장 + 영상 첫 프레임 50장 + 정지 이미지 29장 = 85장**을 만들고 모든 그림을 원본 크기로 검수한다. 이번 작업자는 생성·저장·간단 확인과 엄격 검수를 같은 PC에서 맡는다.

- 비용: Flow 이미지 무료, UI에서 **Nano Banana 2.1 / 16:9 / x1 / 0 credits** 확인 완료. 상시 허락에 따라 무료 생성·재생성은 계속 진행한다.
- 고정 프로젝트: [Flow 지정 프로젝트](https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd). 현재 프로젝트를 유지한다.
- 한 장 제출 → 완료 확인 → 간단 확인·저장 → 다음 한 장 순서다. 동시에 여러 장을 제출하지 않는다.
- 영상 첫 프레임도 **이미지**로만 만든다. Muse 영상 생성 승인은 이 지시서에 없다.
- 생성 그림은 관찰 요약·승인 대본에 근거한 재구성/설명용 모형이다. 실제 기록 사진·실측 시공 도면으로 소개하지 않는다. 외부 사진 원본을 다운로드하거나 첨부하지 않았다.

## 0. 먼저 읽기

1. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\AGENTS.md`
2. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\01_strict_rules.md`
3. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\03_image_rules.md`
4. `D:\youtube\Cheezon-Ki-Hukumat\backup_portable\skills\step5_images.md`
5. 이 지시서와 아래 명세·프롬프트 파일 전체

## 경로

| 이름 | 전체 경로 |
|---|---|
| 저장소 | `D:\youtube\Cheezon-Ki-Hukumat` |
| 이미지 생성기 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\make_prompts_v1.py` |
| 기준 그림 프롬프트 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\masters_v1.json` |
| 전체 85행 프롬프트 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\prompts_v1.json` |
| 형상·공정 명세 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\scene_spec_v1.md` |
| 관찰 출처·한계 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\reference_brief.md` |
| 실측 장면 카탈로그 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\plan\scene_catalog_v1.json` |
| 실측 컷 목록 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\plan\shot_list_v1.json` |
| PC 원본 이미지(실제 다운로드 형식 보존) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw` |
| PC 워터마크 제거 PNG | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img` |
| PC 최종 선택 PNG | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_selected` |
| PC 검수 복사본·측정·모음 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\image_review_v1` |
| 워터마크 제거 도구 | `D:\youtube\7. Cheezon Ki Hukumat\tools\lama\dewm.py` |
| 자동 측정 도구 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\cloud_review_v1.py` |
| 선택·탈락 기록 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\picks_v1.md` |

## 1. 동기화와 입력 확인

```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" status --short
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull --ff-only origin main
python "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\make_prompts_v1.py"
Test-Path -LiteralPath "D:\youtube\7. Cheezon Ki Hukumat\tools\lama\dewm.py"
Test-Path -LiteralPath "D:\youtube\7. Cheezon Ki Hukumat\tools\lama\mask_img.png"
Test-Path -LiteralPath "D:\youtube\7. Cheezon Ki Hukumat\tools\lama\lama_fp32.onnx"
$ep09ImagePrompts = Get-Content -LiteralPath "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\prompts_v1.json" -Raw | ConvertFrom-Json
$ep09ImagePrompts.Count
$ep09ImagePrompts | Group-Object kind | Select-Object Name, Count
New-Item -ItemType Directory -Force -Path "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_selected" | Out-Null
```

기대 결과: 생성기 `status: pass`, `errors: []`, `asset_count: 79`, `master_count: 6`, 세 번의 `True`, 전체 `85`, master `6` / frame `50` / image `29`. 기존 사용자 변경이 있으면 덮어쓰지 말고 먼저 확인한다. 내레이션과 시간표는 편집하지 않는다.

## 2. 기준 그림부터 생성·저장

`masters_v1.json` 순서 그대로 **AT_S → AT_N → AT_C → AT_INT → G3D_EXC → G3D_DEEP**를 한 장씩 만든다.

1. 각 JSON 행의 `prompt`를 수정 없이 붙여 넣는다. AT_S·AT_N·AT_C·AT_INT·G3D_EXC는 `ref: null`인 최초 기준 생성이다. 외부 사진을 첨부했다고 표현하지 않는다.
2. 생성 완료 후 원본을 실제 형식으로 저장한다. 확인된 첫 시도는 `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw\v1_AT_S_1.jpg`다. JPEG 파일의 확장자만 PNG로 바꾸지 않는다. PNG 원본이면 `.png`를 쓴다. 재시도는 숫자를 올리고 이전 원본을 보존한다.
3. 워터마크를 제거한다. 다음 명령은 AT_S 첫 시도 예시다. 다른 ID·시도 번호는 실제 파일과 일치하게 바꾼다.

```powershell
python "D:\youtube\7. Cheezon Ki Hukumat\tools\lama\dewm.py" "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw\v1_AT_S_1.jpg" "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_S_1.png"
Test-Path -LiteralPath "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_S_1.png"
```

4. 원본 크기로 형상·밝기·글자·워터마크 흔적을 보고 기준으로 채택할지 결정한다. 채택된 제거본만 `img_selected`로 복사한다. 아래 명령으로 원본·처리본과 기존 Flow 자산의 연결을 기록한 뒤, 이미 같은 프로젝트에 있는 **채택한 동일 시도의 Flow 원본 자산**을 선택한다. `source_correspondence_verified`가 아닌 항목은 쓰지 않는다. G3D_DEEP은 **채택된 G3D_EXC의 원본 Flow 자산**을 첨부한다. 파일명·제목이 비슷한 다른 시도는 그림과 결과 URL로 구별한다.

```powershell
python 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\make_reference_manifest.py'
```

이 명령은 실제 UI 첨부를 검증하지 않는다. 편집기 URL은 같은 컨테이너에서 수정 전후가 같을 수 있으므로, **제출 직전 실제 입력 이미지의 media revision**도 대조한다. `record_review.py`는 새 결정의 결과 revision과 실제 UI 입력 원천 revision·관찰 근거를 기록하고 정확한 선택/재시도 원본과 대조한다. 기존 기록은 별도 관찰 파일에 실제 다운로드 SHA가 과거 raw와 일치할 때만 연결하며, 사후 확인을 과거 관찰로 소급하지 않는다. `generation_records_v1/`에는 정확한 제출 프롬프트와 실제 원천/결과 revision을 보존한다. 선택 원본이 없거나 정확한 revision을 UI에서 선택할 수 없으면 임의 그림이나 텍스트만으로 대체하지 않는다.
5. 남측·북측 포털은 서로 다른 기준이다. AT_S의 사각 도로 개구부·차양과 AT_N의 박공지붕·오른쪽 사각 개구부를 합치지 않는다. 별도 전통 접근문을 실제 입구처럼 만들지 않는다.

초기 기준 그림이 잘못됐으면 그 기준을 쓰는 후속 그림을 시작하지 않는다. 무료 재생성은 고쳐서 계속한다. 참조 첨부를 거부하면 같은 참조로 한 번 재시도하고, 다시 거부하면 `거부`로 기록한 뒤 해당 의존 그림은 보류한다. 참조 없이 텍스트만으로 대체하지 않는다.

## 3. 나머지 79개 그림 생성

`prompts_v1.json`에서 master 이후의 행을 계획 순서대로 처리한다. `o001` 등 50개 frame은 후속 영상의 첫 프레임이고, `i001` 등 29개 image는 편집 효과를 넣을 정지 그림이다.

- `ref`에 적힌 **채택된 동일 후보의 원본 Flow 자산**을 첨부한다. `reference_assets_v1.json`의 선택 번호/결과 URL과 대조한다. `null`이면 그 장면은 반복 고유 대상을 강제하지 않는 독립 설명 장면이다. 실사에는 3D 기준을 첨부하지 않는다.
- `ref`는 마스터 6장 외에 앞서 채택한 컷 그림을 가리킬 수 있다. 예를 들어 설경 두 번째 컷은 첫 설경 컷, 자료 검토 두 번째 컷은 첫 자료 검토 컷을 첨부해 같은 도로·소품을 유지한다. 선행 그림이 아직 선택되지 않았다면 의존 컷을 먼저 만들지 않는다.
- 한 행의 `visual_source_ids`가 그림에 실제로 보일 문장이다. `source_ids`는 해당 컷과 겹치는 발화 전체라 더 길 수 있다. 서로 다른 장소를 한 그림에 합치거나 모핑하지 않는다.
- `initial_state`가 있으면 아직 동작이 끝나지 않은 첫 상태를 만든다. 임시 바닥 연결과 후속 깊은 최종 인버트는 다른 단계다.
- 제거본 이름은 `v1_{id}_{n}.png`. 원본은 실제 다운로드 형식의 확장자로 `img_raw`, 제거본은 `img`, 채택된 한 장만 `img_selected`에 둔다.
- 간단 확인은 대상 오류, 실사/3D 뒤바뀜, 뚜렷한 글자, 어두운 화면을 즉시 가린다. 세밀한 원리·일관성 검수는 다음 단계에서 한다.
- 고칠 때는 생성기의 프롬프트를 먼저 수정하고 JSON을 재생성한다. PC에서만 임의 문구를 바꾸지 않는다. 같은 실패를 고친 뒤에도 세 번 반복하면 그 ID·원인·시도 내역을 보고한다.

## 4. 자동 측정과 별도 원본 검수

모든 시도의 제거본을 측정할 수 있다. 이 도구는 원본을 변경하거나 삭제하지 않는다.

```powershell
python "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\cloud_review_v1.py" "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\image_review_v1" "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img"
```

`image_review_v1\auto_report.md`·`auto_report.json`·모음을 읽고, **85개 ID의 채택 후보 원본을 각각 원본 크기로 직접 본다.** 자동 도구는 해상도·밝기·실제 인접 컷/마스터와의 dhash 거리만 측정한다. 최신 시도 번호가 자동 채택이라는 뜻은 아니다.

원본 시각 검수는 남·북 포털 형상, 단일 양방향 튜브, 강관 축 방향과 횡단 지보 분리, 실제 연결·접합, 임시/최종 인버트 단계, 물·토사·미는 힘 색, 배수구의 열린 출구, 날짜/귀속의 시각적 오해, 얼굴 크기·글자·워터마크·중복 구도를 확인한다. 설명용 물은 파랑, 누르는 힘은 주황이다. 대피 통로를 배수로로 쓰지 않는다.

`picks_v1.md`에 ID별 `pass / remake / pending / 거부`, 참조 ID, 시도 횟수, 탈락 원인→프롬프트 수정, 실제 선택 파일명, 원본 크기로 본 여부를 기록한다. 선택 전에는 파일명과 합격을 가정하지 않는다. 이미지 79개를 계획의 실제 선택 번호에 연결하고 다시 자동 점검한다.

## 5. 기록 동기화와 보고

현재 작업자는 같은 PC의 원본을 직접 검수하므로 이미지 파일을 GitHub로 운반할 필요가 없다. 원본·제거본·선택본은 PC 에피소드 폴더에 보존한다. 저장소에는 프롬프트·선택·검수·계획의 **텍스트 기록만** 반영한다. 오디오·캐시·생성 PNG는 커밋하지 않는다.

텍스트 기록이 실제 완료 상태를 반영한 다음 저장소의 변경 파일을 확인하고 이 에피소드 파일만 add/commit/push한다. 다른 작업의 변경을 섞지 않는다. push 뒤에는 반드시 원격을 다시 확인한다.

```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" status --short
git -C "D:\youtube\Cheezon-Ki-Hukumat" diff --check
git -C "D:\youtube\Cheezon-Ki-Hukumat" add -- "episodes/ep09_atal_tunnel/images/make_prompts_v1.py" "episodes/ep09_atal_tunnel/images/masters_v1.json" "episodes/ep09_atal_tunnel/images/prompts_v1.json" "episodes/ep09_atal_tunnel/images/prompt_validation_v1.json" "episodes/ep09_atal_tunnel/images/scene_spec_v1.md" "episodes/ep09_atal_tunnel/images/reference_brief.md" "episodes/ep09_atal_tunnel/images/cloud_review_v1.py" "episodes/ep09_atal_tunnel/images/WORK_ORDER_images_v1.md" "episodes/ep09_atal_tunnel/images/picks_v1.md"
git -C "D:\youtube\Cheezon-Ki-Hukumat" diff --cached --check
git -C "D:\youtube\Cheezon-Ki-Hukumat" diff --cached --stat
git -C "D:\youtube\Cheezon-Ki-Hukumat" commit -m "Add ep09 image prompts and review records"
git -C "D:\youtube\Cheezon-Ki-Hukumat" push origin main
git -C "D:\youtube\Cheezon-Ki-Hukumat" fetch origin main
git -C "D:\youtube\Cheezon-Ki-Hukumat" rev-parse HEAD
git -C "D:\youtube\Cheezon-Ki-Hukumat" rev-parse origin/main
git -C "D:\youtube\Cheezon-Ki-Hukumat" log -1 --oneline origin/main
```

두 `rev-parse`가 같아야 원격 반영 확인이다. push가 원격 선행 변경으로 거절되면 `git -C "D:\youtube\Cheezon-Ki-Hukumat" pull --no-rebase origin main`으로 변경을 보존해 합친 뒤 push/fetch/두 커밋 비교를 다시 한다. 아직 없는 선택 기록 파일을 가짜로 만들어 add하지 않는다.

보고: 생성 완료 ID 수 / 최종 선택 ID 수 / 재생성 ID / 거부·미완료 ID / 실제 해상도 / 자동 측정 결과 / 실제로 본 원본과 판단 / 원격 확인 커밋. 85개가 선택·검수되기 전에는 이 작업을 완료로 표기하지 않는다.

## 금지

승인 대본·수치·순서 변경, 다른 첫 프레임, 참조 거부 후 텍스트만으로 생성, 연속 동시 제출, 실존 인물 재현, 생성 글자·번호판·로고, 유료 생성, Muse 영상 생성, 미검수 합격 표기, `.claude\skills` 직접 수정.
