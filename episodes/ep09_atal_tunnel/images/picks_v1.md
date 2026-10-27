# 9편 이미지 선택·실제 시각 검토 기록 v1

갱신: 2026-10-27T13:33:35+09:00. 선택 **5/85 ID**, 기록 7 ID / 15시도. 미선택 80 ID. 미기록 78 ID.

2026-10-27 최초 생성 UI에서 지정 Flow 프로젝트, Nano Banana 2.1 / 16:9 / x1 / 0크레딧을 확인했다. 한 장씩 생성한다.

이미지는 관찰한 형상·승인 대본으로 새로 생성한 설명용 재구성이다. 현장 기록 사진·측량 결과가 아니다. 도구는 시각 합격을 판단하지 않고 root가 명시한 선택·재생성 결정과 실제 원본 크기로 연 여부를 기록한다.

자동 확인은 파일 존재·실제 형식·픽셀 크기·바이트 수·SHA-256·선행 선택 참조 파일에 한정된다. planned_ref와 master 재시도에서 명시한 미선택 원본 참조(actual_retake_reference_file)를 구분한다. 같은 프로젝트의 실제 첨부 원본 자산은 reference_assets_v1.json/생성 기록과 대조하며, 표의 선행 선택 PNG 파일은 그 원천을 구별하기 위한 선택 기록이다. PNG를 재업로드했다고 뜻하지 않는다. Flow에 실제 참조를 첨부했는지, 의미·형상·글자·사람·밝기·중복이 적절한지는 이 측정으로 검증하지 않는다. 오디오 받아쓰기 검사도 별개다.

새 결정은 result_media_url에 실제 결과 이미지 revision을 기록하고, actual_ui_references에 제출 전 실제 입력으로 본 ID·편집기 URL·source_media_url·방법·관찰자·근거를 명시한다. ref가 없으면 []로 입력 이미지 부재를 신고한다. 편집기 URL은 수정되는 컨테이너이므로 이미지 revision 식별자가 아니다. 도구는 신고의 순서·정확한 원천 revision·기록된 파일 해시를 확인하며 서비스의 실제 첨부를 자동 입증하지 않는다.

과거 결과 revision이 기록되지 않았으면 source_revision_observations_v1.json의 별도 관찰을 통해 원장·실제 원본과 raw SHA가 모두 같은 경우에만 해석한다. 별도 observed_at/evidence는 관찰한 실제 시점과 사후 확인 여부를 보존하며, 과거 입력 기록에 새 관찰을 소급해서 만들지 않는다. revision 미확인 상태에서는 후속 참조를 차단한다.

## 생성·실제 검토

| ID | 첨부 기준의 선행 선택 | 시도 | 원본 / 처리본 | 결정 | 원본 크기 직접 열기 raw / clean | 실제로 본 내용·조치(root 기록) |
|---|---|---:|---|---|---|---|
| AT_S | 없음 | 1 | v1_AT_S_1.jpg / v1_AT_S_1.png | 보류·재생성 | 예 / 예 | 1376×768 원본과 처리본을 직접 확인. 직사각형 입구, 주황 세로 외장, 갈색 차양, 숲·산악, 읽히는 글자 없음은 충족. 전경의 두 점선이 입구 쪽까지 이어져 3차로처럼 읽힐 여지가 있어 기준 그림으로 채택하지 않음. 실제 접근부의 오류 확정은 아니며 본선 2차로 의미 전달을 분명하게 하는 목적. 멀리 작은 실루엣도 보여 사람 없는 마스터 지시를 강화함. |
| AT_S | 없음 | 2 | v1_AT_S_2.jpg / v1_AT_S_2.png | 선택 | 예 / 예 | 1376×768 원본과 처리본을 직접 확인. 총 2차로·중앙선 하나가 입구까지 분명함. 사람·읽히는 글자 없음. 노랑/주황 세로 외장·갈색 사선 차양·직사각형 입구·숲과 보강 사면을 유지. 처리 후 모서리의 번짐이나 형상 변화가 보이지 않음. 현장 측량 사진이 아닌 생성 재구성 기준으로 채택. |
| AT_N | 없음 | 1 | v1_AT_N_1.jpg / 없음 | 보류·재생성 | 예 / 아니오 | 북측 큰 녹색 뒤 박공·작은 적갈색 앞 박공·오른쪽 사각 차량 입구·왼쪽 작은 관리공간·2차로는 읽힘. 오른쪽 입구 기둥에 두 줄의 흰 글자/표지 같은 흔적이 보여 원본과 해당 부분 확대를 직접 확인한 뒤 보류. 읽을 수 있는 특정 문구를 발견했다고 주장하지 않으며, 생성 글자처럼 보이는 흔적을 제거할 무료 재생성을 요청함. |
| AT_N | 없음 | 2 | v1_AT_N_2.jpg / v1_AT_N_2.png | 보류·재생성 | 아니오 / 예 | 처리본을 실제 1376×768 크기로 열어 확인. 사람 없음·2차로·중앙선 하나·밝기는 충족하지만 적갈색 앞 박공이 큰 녹색 뒤 박공과 거의 같은 폭으로 확장되어 왼쪽의 작은 전면 박공이라는 기준 형상이 약해짐. 작은 흰 사각 패치는 글자로 확인되지 않았고 그 자체를 탈락 이유로 삼지 않음. 시도1의 지붕 형상을 참조로 고정하고 기둥의 글자 흔적만 수정하는 재생성을 요청함. |
| AT_C | 없음 | 1 | v1_AT_C_1.jpg / 없음 | 보류·재생성 | 예 / 아니오 | 원본 1376×768을 직접 확인. 굴착면·직선 종방향 강관·횡방향 지보는 보이지만 천장 강관 사이의 밝은 틈이 지표면으로 열린 구멍과 외광처럼 읽힘. 지하 작업등으로 밝힌 연속된 암반/숏크리트 천장을 보여 줘야 하므로 보류. 일반 실사 머리말의 daylight와 지하 조명 지시가 충돌할 수 있어 실내 전용 전기조명 머리말로 고침. 전면 인물은 더 멀리 작게 배치하도록 조정하되 기존 얼굴이 화면 1/4을 넘었다고 주장하지 않음. |
| AT_C | 없음 | 2 | v1_AT_C_2.jpg / 없음 | 보류·재생성 | 예 / 아니오 | 원본을 실제 크기로 직접 확인. 닫힌 천장과 전기 작업등은 해결됨. 다만 굴착면을 가로지르는 긴 평행 봉 묶음과 짧은 돌출 파이프가 선행 강관의 진행 방향을 모호하게 만듦. 실사 기준은 단순한 횡방향 아치 지보와 닫힌 지반을 보여 주고 선행 보강은 지반 내부에 가리도록 수정함. 파이프 루프의 축 방향과 단면 배열은 별도 3D 원리 기준에서 명확히 설명한다. 기계 외장도 표식 없는 단색으로 강화함. |
| AT_C | 없음 | 3 | v1_AT_C_3.jpg / v1_AT_C_3.png | 선택 | 예 / 예 | 1376×768 원본·처리본을 각각 직접 확인. 연속된 닫힌 암반/숏크리트 천장·횡방향 아치 지보·실제 보이는 전기 작업등·흙과 바닥 물·작은 장비 및 먼 성인 작업자2명이 읽힘. 잘못된 노출 강관 묶음과 하늘 구멍이 없음. 기계의 작은 사각 부분을 확대해 글자가 아닌 손잡이/해치 모양임을 확인. 읽히는 글자·로고·워터마크 흔적이 보이지 않아 설명용 공사 재현 기준으로 선택. 실제 현장 기록 사진이나 모든 지보 상세의 실측 재현이라고 주장하지 않음. |
| AT_INT | 없음 | 1 | v1_AT_INT_1.jpg / v1_AT_INT_1.png | 선택 | 예 / 예 | root가 원본 JPEG와 처리 PNG를 각각 원본 크기로 직접 열었다. 중앙 점선 하나로 나뉜 단일 양방향 2차로, 매끈한 회색 벽, 닫힌 평평한 내부 천장, 밝은 전기조명과 닫힌 측면 배수 그릴이 보인다. 사람·차·읽을 수 있는 글자는 보이지 않고 워터마크 제거 부위에도 눈에 띄는 흔적을 발견하지 못했다. 실제 현장 측량 색상이나 기록 사진이 아닌 완공 내부 설명용 재구성 기준으로 선택한다. |
| G3D_EXC | 없음 | 1 | v1_G3D_EXC_1.jpg / v1_G3D_EXC_1.png | 보류·재생성 | 예 / 예 | root가 원본 JPEG와 처리 PNG를 원본 크기로 각각 열었고 독립 검토자도 처리본을 직접 봤다. 곧은 청록관과 회색 횡단 아치는 구별되지만, 이미 열린 왼쪽 공간·중앙 작업면·오른쪽 고체 지반을 보여줄 종단 절개가 분명하지 않고 뒤가 계속 열린 어두운 통로처럼 읽힌다. 보라색 주입재도 초기 단계에 이미 있어 후속 공정 설명용 기준으로 부적합. 프롬프트를 종단 side-cut, 중앙의 막힌 작업면, 오른쪽 고체 지반, 초기 보라 재료 없음으로 수정했다. |
| AT_N | 없음; master 재시도 raw: v1_AT_N_1.jpg (첨부는 root 신고) | 3 | v1_AT_N_3.jpg / v1_AT_N_3.png | 선택 | 예 / 예 | root가 원본 JPEG와 처리 PNG를 원본 크기로 각각 직접 열었다. 큰 녹색 후면 박공과 폭이 작은 왼쪽 적갈색 전면 박공, 오른쪽 사각 도로 개구부, 빈 단일 양방향 2차로, 설산·회색 옹벽이 시도1 비례로 유지됐다. 시도1 오른쪽 기둥의 흰 글자 같은 흔적이 제거되고 읽을 수 있는 글자나 제거부위의 눈에 띄는 흔적을 발견하지 못했다. 독립된 작은 왼쪽 서비스 부분을 두번째 차량 튜브로 보지 않는다. 현장 사진이 아닌 설명용 재구성 기준으로 선택한다. Flow editURL은 원본과 동일한 컨테이너이므로 결과 media revision을 별도로 고정한다. |
| G3D_EXC | 없음 | 2 | v1_G3D_EXC_2.jpg / v1_G3D_EXC_2.png | 보류·재생성 | 예 / 예 | root가 원본 JPEG와 처리 PNG를 각각 원본 크기로 직접 열었다. 왼쪽 열린 상부 공간·중앙 거친 작업면·오른쪽 고체 지반과 하부 벤치 구분은 수정됐고 보라 주입재도 없어졌다. 그러나 청록관이 천장 꼭대기의 몇 가닥 묶음으로 모여 있고 길이 방향 일부가 물결처럼 굽어 보이며, 관 끝이 천장 전체 아치에 배열되는 관계를 보여주지 못한다. 시도2 형상을 입력으로 유지하고 관 배치·직선성만 바로잡는 명시적 수정 프롬프트를 준비했다. |
| G3D_EXC | 없음; master 재시도 raw: v1_G3D_EXC_2.jpg (첨부는 root 신고) | 3 | v1_G3D_EXC_3.jpg / v1_G3D_EXC_3.png | 보류·재생성 | 예 / 예 | root가 원본 JPEG와 처리 PNG를 각각 원본 크기로 직접 열었다. 좌측 굴착 공간·중앙 막힌 작업면·우측 고체 지반과 관 끝의 아치 배열은 좋아졌다. 그러나 오른쪽 지반을 따라 드러난 긴 청록관 여러 가닥이 물결치거나 서로 붙어 보여 직선 강관의 형상·평행관계를 설명하는 기준으로는 보류한다. 다음 수정은 관 끝 아치와 굴착 형상을 유지하며, 앞쪽 고체 지반에 묻힌 관을 불필요하게 바깥으로 노출하지 않고 보이는 짧은 몸통만 직선으로 정리한다. |
| G3D_EXC | 없음; master 재시도 raw: v1_G3D_EXC_3.jpg (첨부는 root 신고) | 4 | v1_G3D_EXC_4.jpg / v1_G3D_EXC_4.png | 선택 | 예 / 예 | root가 원본 JPEG와 처리 PNG를 원본 크기로 각각 직접 열었다. 왼쪽 열린 상부 굴착 공간·중앙의 거친 막힌 작업면·오른쪽 고체 지반, 연속된 하부 벤치가 분명하다. 회색 횡단 아치 지보의 발이 벤치에 닿고 청록관의 원형 끝이 천장 아치로 배열된다. 보이는 짧은 몸통이 굴착축 방향의 직선이며 오른쪽 매몰부는 불투명 지반에 가려져 이전의 파형 외부 노출이 없어졌다. 보라 주입재·임시 인버트·완공 차도·사람·글자가 없고 처리부위의 눈에 띄는 흔적을 발견하지 못했다. 실제 시공 단면 치수나 기록사진이 아닌 원리 모형 기준으로 선택한다. |
| G3D_DEEP | G3D_EXC=v1_G3D_EXC_4.png | 1 | v1_G3D_DEEP_1.jpg / v1_G3D_DEEP_1.png | 보류·재생성 | 예 / 예 | root가 raw JPEG와 clean PNG를 원본 크기로 각각 직접 열었다. 앞단에 작은 U자 바닥과 평평한 슬래브만 추가되고, 뒤쪽에 남은 하부 벤치·기존 아치와 하부구조의 연결이 불분명하다. 전체 난구간 후속 최종 인버트가 닫힌 구조 링을 이룬다는 설명에 필요한 길이 방향 하부 제거와 연속된 영구 라이닝이 읽히지 않아 보류. master 프롬프트를 전체 왼쪽 하부 벤치 제거, 길이 방향 깊은 바닥, 크라운·벽·바닥의 연속된 링으로 수정했다. |
| o001 | AT_C=v1_AT_C_3.png | 1 | v1_o001_1.jpg / v1_o001_1.png | 보류·재생성 | 예 / 예 | root가 raw JPEG와 clean PNG 및 C3 기준 PNG를 각각 원본 크기로 열어 대조했다. 닫힌 지하 천장·작업등·작은 성인·굴착면 물 유입은 읽히지만, 정면 구도가 기준과 너무 비슷하고 중앙의 열린 관과 여러 호스가 집수부에서 이어지는 연속 배수 경로를 보여주지 못한다. 물 유입량을 설명하는 문장에 불필요한 배수 동작은 제거하고, 이미 있는 균열에서 아래 얕은 집수 영역으로 흐르는 물만 움직이게 영상 정의를 수정했다. 이미지도 오른쪽 벽에서 왼쪽 작업면을 비스듬히 보는 구도로 명시해 새로 생성한다. 내레이션 내용·숫자·순서는 변경하지 않았다. |

## 현재 명시적 선택

| ID | 선택 파일 | 처리본 픽셀 크기 | SHA-256 |
|---|---|---|---|
| AT_S | `v1_AT_S_2.png` | 1376×768 | `bf4dedc1e5fd2dd08bc89de585780f9d4faa18aa8bd6e8aeaff8be1dea5b723c` |
| AT_N | `v1_AT_N_3.png` | 1376×768 | `2556ea607269fbf045cff7a064fd0ea58fbbbf781e1d11586b6b7193554028df` |
| AT_C | `v1_AT_C_3.png` | 1376×768 | `384f9fb144125e9fed28d3e8bb8d15c6e7bb3e3ae8a4f6c2576e9a8b5a1553c5` |
| AT_INT | `v1_AT_INT_1.png` | 1376×768 | `f920c96dd54fd18123466be948e5d68bb634cf9062a81f09c5ac21e9942d42a0` |
| G3D_EXC | `v1_G3D_EXC_4.png` | 1376×768 | `c6994b47651cd174800087371627e34a2a0f4dab1f18761a8417fa490e6e802e` |

## 출처·범위·PC 보관

- AT_S 시도1은 부모와 독립 검토자가 각각 실제 파일을 열었다. 시도2는 root가 원본·처리본을 실제 원본 크기로 연 기존 명시 기록을 보존했다. 이 도구 실행은 새 시각 검수가 아니다.
- Primary 본문의 단일 튜브·2차로 설명은 재확인했다. 독립 검토에서 남측 원사진 재열람이 실패했으므로 이 회차에 원사진과 나란히 직접 대조했다고 보고하지 않는다.
- 기존 AT_S 시도1·2의 문장·날짜·Flow 출처와 당시 전체 JSON/Markdown은 JSON의 `legacy_record`에 원문 보존한다. 원본 JPEG와 워터마크 처리 PNG를 구별한다. 기존 `tools\lama\dewm.py` 처리를 기록하며 생성 글자를 흐려서 통과시키지 않는다.
- PC 원본: `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_raw`. 처리본: `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img`. 명시 선택 복사본: `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\img_selected`. 원본은 보존하며 이 도구는 이미지를 편집·삭제하지 않는다.
- 최신 번호를 자동 선택하지 않는다. 재생성 결정은 이전의 별도 선택을 자동 해제하지 않으며, 새 `chosen` 결정만 해당 ID 선택을 교체한다. 정규 planned_ref는 결정 당시 선행 선택의 파일·해시로 고정한다. master 재시도의 같은 ID 앞선 원본만 별도 raw 참조로 허용하며 정규 참조의 선행 선택 조건을 면제하지 않는다.

- AT_S 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/d7501eaa-9047-474c-8302-ab06402c0ef2 · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_S 시도2 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/dcc6ae0f-7d2a-47bf-a1df-22155cd468c1 · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_N 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/a10bade0-3cad-479d-93a8-5d68d9986821 · 자동 측정 raw JPEG [1376, 768] / clean 없음; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_N 시도2 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/7f4dcf8f-3c87-4c25-8a79-383752abfa7d · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_C 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/1c1d1fed-7d49-4efc-a0d3-602af496d9b4 · 자동 측정 raw JPEG [1376, 768] / clean 없음; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_C 시도2 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/a4165e2e-b1ce-4c0c-b2cc-9bc76abd5ed3 · 자동 측정 raw JPEG [1376, 768] / clean 없음; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_C 시도3 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/cd6db3c3-bb6c-47ff-aa86-81589494c904 · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- AT_INT 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/e1a3929c-8a91-4682-9b0c-dc22a2bafc94 · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.
- G3D_EXC 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/e564feda-eb2e-4398-acfc-6e649f565f3d · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: 기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함.
  - UI 입력 관찰 신고: 참조 입력 없음([]). 자동 UI 검증은 아니다.
- AT_N 시도3 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/a10bade0-3cad-479d-93a8-5d68d9986821 · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: https://flow-content.google/image/5799362b-258f-4b6a-b5c9-797653871bd6.
  - UI 입력 관찰 신고: AT_N / https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/a10bade0-3cad-479d-93a8-5d68d9986821 / current_image_editor_input / revision https://flow-content.google/image/c0332dd2-7b24-4bca-809d-62db79763071 / 제출 전 / 관찰자 ep09_image_prompts / 근거 Before submit, observer directly saw AT_N1 as main source in image editor above the change-image field: large green rear gable, small left red-brown front gable, right road opening. After submit, history material-thumbnail src was directly read and downloaded; root independently verified downloaded SHA identical to raw N1. The media URL and byte comparison are later corroboration, not claimed as pre-submit URL observation. See generation_records_v1/AT_N_3.json and source_revision_observations_v1.json.. 자동 UI 검증은 아니다.
- G3D_EXC 시도2 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: https://flow-content.google/image/8f1d0888-32a8-40d3-900b-a9c67ff1110d.
  - UI 입력 관찰 신고: 참조 입력 없음([]). 자동 UI 검증은 아니다.
- G3D_EXC 시도3 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: https://flow-content.google/image/76a3473e-8fb4-4f83-ae83-a15d459d1ee5.
  - UI 입력 관찰 신고: G3D_EXC / https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d / current_image_editor_input / revision https://flow-content.google/image/8f1d0888-32a8-40d3-900b-a9c67ff1110d / 제출 전 / 관찰자 ep09_image_prompts / 근거 Before submit observer directly read visible main image src as exact EXC2 media revision, downloaded the displayed input, measured SHA identical to raw EXC2, and saw the change-image editor input and zero-credit settings. See generation_records_v1/G3D_EXC_3.json; exact wall-clock time was not separately captured and is not invented.. 자동 UI 검증은 아니다.
- G3D_EXC 시도4 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: https://flow-content.google/image/dcf20746-d09d-48e9-b963-bcc682e40e2f.
  - UI 입력 관찰 신고: G3D_EXC / https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d / current_image_editor_input / revision https://flow-content.google/image/76a3473e-8fb4-4f83-ae83-a15d459d1ee5 / 제출 전 / 관찰자 ep09_image_prompts / 근거 Before submit actual visible main image src matched EXC3 revision; UI download SHA matched stored raw EXC3. Image was the current source above change-image field. Settings showed image editing/16:9/zero credits. Explicit clock stamps and exact prompt are in generation_records_v1/G3D_EXC_4.json; no local upload used.. 자동 UI 검증은 아니다.
- G3D_DEEP 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: https://flow-content.google/image/73abcd51-6180-4aba-a819-643d36a008c0.
  - UI 입력 관찰 신고: G3D_EXC / https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d / current_image_editor_input / revision https://flow-content.google/image/dcf20746-d09d-48e9-b963-bcc682e40e2f / 제출 전 / 관찰자 ep09_image_prompts / 근거 Observer directly read EXC4 visible main-image revision and downloaded it before submit; raw SHA matched the selected EXC4 source. Current image editor supplied that actual input; free-image settings observed. See generation_records_v1/G3D_DEEP_1.json.. 자동 UI 검증은 아니다.
- o001 시도1 Flow: https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/cd6db3c3-bb6c-47ff-aa86-81589494c904 · 자동 측정 raw JPEG [1376, 768] / clean PNG [1376, 768]; 세부 SHA·바이트는 JSON.
  - 결과 revision: https://flow-content.google/image/512551f1-c95c-4f22-b1d6-a0dc33ee69bf.
  - UI 입력 관찰 신고: AT_C / https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/cd6db3c3-bb6c-47ff-aa86-81589494c904 / current_image_editor_input / revision https://flow-content.google/image/493fbbed-dbb1-44a2-ad2c-a3a1a7413ba9 / 제출 전 / 관찰자 ep09_image_prompts / 근거 Before submission visible main source revision and UI download SHA were checked against raw C3. Current image-editor input, zero credits, 16:9 and selected image model were directly observed. Exact prompt and observations are in generation_records_v1/o001_1.json.. 자동 UI 검증은 아니다.
