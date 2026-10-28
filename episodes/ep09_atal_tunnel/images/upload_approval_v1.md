# ep09 선택 master 6개 외부 전송 승인 검토 자료

작성 시각: 2026-10-28T09:49:47+09:00. **미승인(`authorized=false`)이며, 업로드와 업로드 별칭의 확인 기록은 없다(`confirmed_upload=false`, `confirmed_upload_identity_alias=false`).** 이 문서는 승인을 기록하거나 전송을 실행하지 않는다.

대상은 Google Flow 프로젝트 `cb1e7ac3-1d61-4206-ac72-3444f121843c`, Chrome 프로필 별칭 `artbuilder883`이다. 목적은 아탈 터널 편의 후속 설명 이미지에서 대상·형상 일관성을 유지하기 위한 참조다. 개인 이메일은 기록하지 않았다.

전송을 구체적으로 승인하고 실행하면 **아래 선택된 PNG 6개 파일의 전체 이미지 데이터가 로컬 컴퓨터 밖의 Google Flow 계정·프로젝트로 전송되어 저장된다.** 파일명이나 SHA만 전달하는 작업이 아니다. 동영상 생성 승인, 외부 게시 승인, 다른 파일 전송, 기존 자산 이동·삭제 승인은 포함하지 않는다.

선택 원장 스냅샷: **10/85 선택, 23개 검토 기록**. 현재 원장을 읽었으며 과거 수치로 덮어쓰지 않았다.

## 검토 대상 전체 목록

모든 파일은 실제 PNG 1376×768이며, 아래 SHA가 원장의 현재 선택 SHA 및 `img_selected` 보관 복사본과 완전히 일치했다. raw·clean 원본 크기 직접 검수 상태는 기존 root 명시 기록에서 가져왔다. 이 자료 준비가 새 시각 합격 판정은 아니다.

| ID | 선택 시도 | 정확한 전송 대상 PNG 경로 | 크기 | SHA-256 | 기존 root 원본 크기 검수 raw / clean |
|---|---:|---|---|---|---|
| AT_S | 2 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_S_2.png` | 1376×768 | `bf4dedc1e5fd2dd08bc89de585780f9d4faa18aa8bd6e8aeaff8be1dea5b723c` | 예 / 예 |
| AT_N | 3 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_N_3.png` | 1376×768 | `2556ea607269fbf045cff7a064fd0ea58fbbbf781e1d11586b6b7193554028df` | 예 / 예 |
| AT_C | 3 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_C_3.png` | 1376×768 | `384f9fb144125e9fed28d3e8bb8d15c6e7bb3e3ae8a4f6c2576e9a8b5a1553c5` | 예 / 예 |
| AT_INT | 1 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_AT_INT_1.png` | 1376×768 | `f920c96dd54fd18123466be948e5d68bb634cf9062a81f09c5ac21e9942d42a0` | 예 / 예 |
| G3D_EXC | 4 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_G3D_EXC_4.png` | 1376×768 | `c6994b47651cd174800087371627e34a2a0f4dab1f18761a8417fa490e6e802e` | 예 / 예 |
| G3D_DEEP | 3 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img\v1_G3D_DEEP_3.png` | 1376×768 | `f03c33f6a2a099da69bd24b887264441785bc64ced7d46cffd96026d90f9b9c4` | 예 / 예 |

동일 바이트의 선택 보관본은 `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_selected` 아래 같은 파일명이다. JSON에는 원래 Flow 출처 URL, 선택 attempt, 정확한 보관 경로와 파일 크기도 보존했다.

## 자동 승인 검토 거절과 앞선 시도의 불확실성

root 보고에 따르면 `v1_AT_C_3.png`의 두 번째 browserClipboard 붙여넣기 시도 전체가 자동 승인 검토에서 거절됐다. 사유는 **특정 로컬 AT_C 참조 이미지를 외부 Google Flow로 전송하는 승인이 프로젝트 작업 지시만으로 명확하지 않다**는 것이다. 부모가 전달한 사유 원문은 JSON의 별도 필드에 보존했다.

첫 번째 시도는 연결 실패로 끝났고 **외부 수신 여부는 미확인**이다. 따라서 실제 업로드·서버 별칭이 0개였다고 단정하지 않는다. 확인된 업로드나 별칭이 없다는 상태만 기록한다.

구체적인 사용자 승인과 적용되는 승인 요건이 충족되기 전에는 이 차단된 전송을 클립보드·파일 첨부·드래그 등 다른 방법으로도 재시도하지 않는다. 이 자료에서는 사용자에게 질문하거나 선택을 요청하지 않는다.

## 측정 범위

선택 master 6개와 보관 복사본의 파일 SHA·실제 PNG 형식·픽셀 크기를 측정하고, 작업 끝에 현재 master 선택 항목 및 파일 SHA가 그대로임을 다시 확인했다. 원장·그림·프롬프트·motion·코드 게이트를 수정하지 않았으며 CUA/UI 또는 전송을 실행하지 않았다.

## 이번 승인 요청 직전 확인

2026-10-28T01:05:43.200720+00:00: 현재 **13/85 선택·28개 검토 기록**, 잔여 72개. 위 기준 PNG 6장과 선택 보관본의 SHA를 현재 선택 원장과 다시 대조해 모두 일치했다. 업로드 승인과 확인된 전송·별칭은 여전히 미기록이다. 앞의 10/85·23개는 자료 작성 당시 스냅샷이다.

## 사용자 전송 승인

2026-10-28T02:09:37.026071+00:00: 사용자 답변 **기준 그림 6장 업로드 승인**을 직접 받았다. 위 정확한 PNG6장과 cb1/artbuilder883 대상으로 전송·저장 승인됨(`authorized=true`). 실제 업로드·서버 별칭 확인은 아직 미수행이다. 앞의 미승인 표시는 승인 전 준비 시점 이력이다. 영상 생성은 승인하지 않았다.


## 2026-10-28 전송 승인 후 차단 상태

사용자가 요청 목록의 기준 PNG6장에 대해 **기준 그림 6장 업로드 승인**이라고 답했다. cb1/artbuilder883의 해당 6장 전송·저장은 승인됐으며 재승인을 요구하지 않는다. 영상 생성은 승인되지 않았다. 선택13/85·검토28·잔여72·실제 영상0은 그대로다.

승인 후 AT_C clipboard 입력은 native pipe 종료로 실패했고 같은 프로필 browser9로 복구했다. 복구 화면에서 신규 기준 타일·소재 첨부를 확인하지 못했으므로 외부 수신은 미확인이다. 이어서 문서화된 filechooser를 정상 열었으나 setFiles가 현재 프로필의 ChatGPT 확장 **Allow access to file URLs**가 필요하다는 오류를 즉시 반환했다. Windows 기본 선택창 fallback은 현재 브라우저 URL을 정책 적용에 필요한 신뢰도로 확인할 수 없어 Computer Use가 이 턴에서 종료됐다. 그 뒤 UI 조작은 하지 않았다.

사용자가 artbuilder883 Chrome의 chrome://extensions → ChatGPT 확장 세부정보에서 파일 URL에 대한 액세스 허용을 켜야 기본 업로드 경로를 재개할 수 있다. 설정 변경은 자동으로 수행하지 않았다. 확인된 업로드·서버 별칭은 없으며 실제 수신0개라고 단정하지 않는다. 기존 자산을 이동·삭제하지 않았고 참조를 빼고 생성하지 않는다. 승인과 최신 차단 근거는 images/upload_approval_v1.json 및 upload_attempts_v1/AT_C_* 기록이다.

## 파일 URL 활성화 후 실제 업로드 완료

사용자가 파일 URL 액세스를 켰다고 알린 뒤, 동일 artbuilder883 프로필 browser10의 지정 cb1 프로젝트에서 기본 파일 선택창으로 승인된6장 PNG 전체를 업로드했다. 정확한6개 파일명 완료 타일과 각각의 새 editor/revision을 직접 확인하고 서버 원본을 내려받았다. 현재6장 수신 확인 및 수동 원본 대조형 참조 등록을 완료했다. 추가 전송 승인은 필요하지 않다.

서버에서 내려받은6장은 JPEG이며 선택 PNG와 픽셀 단위로 동일하지 않다. 기존 엄격 RGB동일 검사와 metadata기반1회 재인코딩 실험은 실패로 보존했다. root는6쌍12개 파일을1376x768 원본 크기로 직접 열어 같은형상·구도·내용을 대조했고, 실제입력SHA/업로드수신기록/새revision/다운로드SHA/명시수동검토를 연결한 root_reviewed_service_representation 유형으로6개를등록했다. 이 유형은 자동 유사도 합격·무손실·결정적 인코더 증명이 아니다. 원본 PNG·oldsource URLs는 그대로다. 후속 장면마다 실제 입력 revision은 별도 확인한다.

근거: upload_receipts_v1/cb1_six_masters_20261028_1.json, upload_comparisons_v1/, upload_aliases_v1.json, upload_registration_validation_v1.json. 실제 영상 생성0·영상 생성 승인false 유지.
