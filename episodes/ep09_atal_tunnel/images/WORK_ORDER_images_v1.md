# 9편 이미지 작업 지시서: 기준 그림 → 79개 컷 그림 → 원본 검수 (2026-10-28)

진행 현황(원장 스냅샷 2026-10-28T02:40:15.395411+00:00): **선택14/85·검토30시도·잔여71·실제 첫 프레임2/50·동작 검토2/50·영상0.** root가 cb1/artbuilder883에서 한 장씩 후속 이미지를 생성·검수 중이다. 생성완료·미선택 출력: **o003 시도3**. 진행/출력 미확인 레코드: **없음**. 생성 결과와 원본 검수·선택을 구별하고 최신 번호를 자동 선택하지 않는다.

**현재 프로젝트·연결:** 사용자 지정 cb1 `cb1e7ac3-1d61-4206-ac72-3444f121843c`, Chrome 프로필 artbuilder883, root 관찰 browser10/tab96308644다. 사용자가 file-URL 접근 허용을 켠 뒤 정상 chooser.setFiles6장 반환·권리 안내 확인·정확한 filename 완료 타일6개를 root가 실제로 보았다. 현재 UI·업로드 차단은 없다. UI는 root 한 명만 조작한다. 정책의 허용ID는 `baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd`, `22cd5ad1-3dbb-4183-a36b-48c7bc3e5144`, `cb1e7ac3-1d61-4206-ac72-3444f121843c` 정확히3개이며 임의4번째는 거부한다. 기존old 자산과 미사용103f 프로젝트를 이동·삭제하지 않는다.

**6장 수신·별칭 실등록:** 사용자의 “기준 그림 6장 업로드 승인”은 정확한 목록PNG6장의 cb1 외부 전송·저장 승인이다. `upload_approval_v1.json`은 authorized/confirmed_upload/confirmed_upload_identity_alias=true이며 실제 수신·등록6개가 있다. 검증유형은 `root_reviewed_service_representation`이며 `exact_pixel_equal=false`, `lossless=false`, `deterministic_transform_proven=false`다. 원본 PNG와 서버 JPEG가 같은 픽셀이라고 보고하지 않는다. 승인·수신·등록이 각 새 생성의 실제 UI 입력 관찰을 대신하지 않는다. 영상 생성 승인은 여전히 false다.

**검수 근거와 모델 구분:** 원AGENTS/portable은 계획된 실제master 첨부와 형태·색·부품·화면방향의 일관성, 원본 크기 직접 검수를 요구한다. RGB완전동일은 우리가 작업 중 추가한 보수적인 strict 별칭 모델이었다. 실제 서버가 JPEG로 변환해 strict 비교와 metadata 기반 단1회 재인코딩도 실패했으며 이 실패를 유지한다. 별도 수동 유형은 exact6 입력파일SHA·실제 batch receipt·filename 타일에서 관찰한 새editor/revision·실다운로드SHA 및 root가 선택PNG6개/서버JPEG6개 총12개 원본을 직접 쌍비교한 결정JSON으로 연결한다. 자동 오차계량에 허용오차를 주어 합격시킨 것이 아니다. `upload_aliases_v1.json`, `upload_registration_validation_v1.json`, `upload_review_v1.json`, `upload_receipts_v1/`, `upload_comparisons_v1/`, `upload_proofs_v1/`, `jpeg_reencode_experiment_v1.json`을 대조한다.

**과거 오류의 보존:** 22cd 서비스/reCAPTCHA 오류, old 프로필의 setFiles 장기 대기, browser4/6 Debugger 연결 오류, 승인 전 자동 전송 검토 거절, 승인 후 clipboard pipe 종료와 file-URL 권한 오류·당시 Windows URL 확인 불가 UI 종료는 각각 역사다. 최초 연결 실패의 외부 수신 여부는 unknown이며, 이후 확인된 batch6장과 섞어 총 업로드 횟수를 단정하지 않는다. 현재 해결된 차단을 되살리거나 재승인을 요구하지 않는다.

**재개 대기열과 참조:** `make_resume_queue_v1.py`는 현재 picks/생성 기록/승인/실별칭을 읽고 실제 `validate_registered_alias`를 통과한 master 옵션을 표시한다. 직접ref와 선택된 선행 그림을 구별하며 선택ID는 제외한다. 이미 생성된 미선택 결과는 먼저 root 결정을 기다린다. 등록된 참조에도 매번 root가 정확한 upload_alias_id 및 현재 입력media revision·순서를 관찰해야 한다. 편집기URL은 계속 수정되는 컨테이너라 URL만 같다는 이유로 최신 결과를master로 쓰지 않는다. 최초 master의 old source URL과 선택PNG는 보존하고, 편집·영상 첫 프레임은 계속 그 실제 선택PNG를 사용한다. 필요한 참조를 다른ID/임의그림/무참조로 바꾸지 않는다.

목적: 승인된 78문장과 실측 79컷에 필요한 **기준 그림 6장 + 영상 첫 프레임 50장 + 정지 이미지 29장 = 85장**을 만들고 모든 그림을 원본 크기로 검수한다. 이번 작업자는 생성·저장·간단 확인과 엄격 검수를 같은 PC에서 맡는다.

- 비용: Flow 이미지 무료, UI에서 **Nano Banana 2.1 / 16:9 / x1 / 0 credits** 확인 완료. 상시 허락에 따라 무료 생성·재생성은 계속 진행한다.
- 현재 프로젝트: [사용자 지정 cb1 Flow 프로젝트](https://flow.google.com/project/cb1e7ac3-1d61-4206-ac72-3444f121843c), 프로필 별칭 artbuilder883. 기존master 원천은 old 계정의 [baa9 프로젝트](https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd)에 보존돼 있다. cb1에는 승인된 선택PNG에서 수신한 JPEG 표현6개가 명시 수동 검수 유형으로 등록됐다. 다음 생성에서 실제 첨부했는지는 제출마다 새로 확인한다.
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

현재 기준6장은 이미 선택됐다. 선택본을 자동 재생성하지 않는다. 아래는 기준 재생성이 실제로 필요할 때의 초기 절차이며, 새 계정으로 전송할 권한을 부여하지 않는다. 필요한 경우 `masters_v1.json`의 **AT_S → AT_N → AT_C → AT_INT → G3D_EXC → G3D_DEEP** 순서를 따른다.

1. 각 JSON 행의 `prompt`를 수정 없이 붙여 넣는다. AT_S·AT_N·AT_C·AT_INT·G3D_EXC는 `ref: null`인 최초 기준 생성이다. 외부 사진을 첨부했다고 표현하지 않는다.
2. 생성 완료 후 원본을 실제 형식으로 저장한다. 확인된 첫 시도는 `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw\v1_AT_S_1.jpg`다. JPEG 파일의 확장자만 PNG로 바꾸지 않는다. PNG 원본이면 `.png`를 쓴다. 재시도는 숫자를 올리고 이전 원본을 보존한다.
3. 워터마크를 제거한다. 다음 명령은 AT_S 첫 시도 예시다. 다른 ID·시도 번호는 실제 파일과 일치하게 바꾼다.

```powershell
python "D:\youtube\7. Cheezon Ki Hukumat\tools\lama\dewm.py" "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw\v1_AT_S_1.jpg" "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_S_1.png"
Test-Path -LiteralPath "D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_S_1.png"
```

4. 원본 크기로 형상·밝기·글자·워터마크 흔적을 보고 기준으로 채택할지 결정한다. 채택된 제거본만 `img_selected`로 복사한다. 아래 명령은 원본·처리본과 원래 Flow 출처의 대응을 기록한다. `source_correspondence_verified`는 현재 계정의 가용성이나 UI 첨부 확인이 아니다. 실제 현재 UI에서 **채택한 동일 시도의 원천 revision 또는 명시적으로 등록·재검증한 수동 서버 표현 별칭 revision**을 확인할 수 있을 때만 선택한다. G3D_DEEP의 G3D_EXC 원천도 같으며, old 계정 원천을 선택할 수 없으면 승인 없는 로컬 전송이나 무참조로 대체하지 않는다. 파일명·제목이 비슷한 다른 시도는 그림과 결과 URL로 구별한다.

```powershell
python 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\images\make_reference_manifest.py'
```

이 명령은 실제 UI 첨부를 검증하지 않는다. 편집기 URL은 같은 컨테이너에서 수정 전후가 같을 수 있으므로, **제출 직전 실제 입력 이미지의 media revision**도 대조한다. `record_review.py`는 새 결정의 결과 revision과 실제 UI 입력 원천 revision·관찰 근거를 기록하고 정확한 선택/재시도 원본과 대조한다. 기존 기록은 별도 관찰 파일에 실제 다운로드 SHA가 과거 raw와 일치할 때만 연결하며, 사후 확인을 과거 관찰로 소급하지 않는다. `generation_records_v1/`에는 정확한 제출 프롬프트와 실제 원천/결과 revision을 보존한다. 선택 원본이 없거나 정확한 revision을 UI에서 선택할 수 없으면 임의 그림이나 텍스트만으로 대체하지 않는다.
5. 남측·북측 포털은 서로 다른 기준이다. AT_S의 사각 도로 개구부·차양과 AT_N의 박공지붕·오른쪽 사각 개구부를 합치지 않는다. 별도 전통 접근문을 실제 입구처럼 만들지 않는다.

초기 기준 그림이 잘못됐으면 그 기준을 쓰는 후속 그림을 시작하지 않는다. 무료 재생성은 고쳐서 계속한다. 정상 서비스가 특정 참조를 거부하면 사유를 확인하고 허용 범위에서 같은 참조로 한 번 재시도할 수 있으며, 다시 거부하면 해당 의존 그림을 보류한다. 이 절차는 자동 승인 검토의 로컬 외부 전송 거절에 적용하지 않는다. 해당 전송은 구체적 사용자 승인 전 재시도하지 않는다. 참조 없이 텍스트만으로 대체하지 않는다.

## 3. 나머지 79개 그림 생성

`prompts_v1.json`에서 master 이후의 행을 계획 순서대로 처리한다. `o001` 등 50개 frame은 후속 영상의 첫 프레임이고, `i001` 등 29개 image는 편집 효과를 넣을 정지 그림이다.

- `ref`에 적힌 **채택된 동일 후보의 실제 서버 원천 또는 검증된 수동 표현 별칭**을 첨부한다. 원래 선택 번호·old URL은 `reference_assets_v1.json`, 새 수동 표현의 alias ID·revision·근거는 `upload_aliases_v1.json`으로 구분하고 실제 제출 전 입력을 대조한다. `null`이면 그 장면은 반복 고유 대상을 강제하지 않는 독립 설명 장면이다. 실사에는 3D 기준을 첨부하지 않는다.
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



## 최신 진행 중 원장 체크포인트

{
  "recorded_at_utc": "2026-10-28T02:52:41.319464+00:00",
  "selected_images": 16,
  "reviewed_attempts": 32,
  "remaining_images": 69,
  "selected_frames": 4,
  "motion_compatible_frames": 4,
  "registered_master_service_representations": 6,
  "original_png_and_server_jpeg_pixel_identical": false,
  "first_frame_blockers": 46,
  "video_generation_authorized": false,
  "actual_video_generated": 0,
  "actual_unreviewed_outputs": [],
  "in_flight_attempts": [
    {
      "id": "i001",
      "attempt": 1,
      "record": "images\\generation_records_v1\\i001_1.json",
      "status": "current result unobserved; do not resubmit"
    }
  ],
  "strict_43_sentence_preserved": true,
  "o001_original_motion_contract_preserved": true,
  "o003_draft_adjusted_before_video": "Two existing cars move normally in their actual incoming/outgoing lanes; narration unchanged.",
  "principle_image_prompt_corrections": "p005 includes complete visible drainage route/open outlet; scene_spec separates first-image stage construction from later fixed geometry."
}

수치는 이 체크포인트가 우선한다. 진행 중 시도는 새 출력 관찰 전 중복 제출하지 않는다. 생성용 영상 ready 파일은 미작성 상태다.
