# 과거 브라우저 조작 관찰

아래는 2026-10-08 전후의 UI·모델·가격·계정 기록이다. 현재 정책·잔액·가격·도구 선택 지시가 아니다. 최신 승인 범위와 현재 UI를 먼저 확인한다. 이 자료는 해당 도구를 실제 사용하기로 한 경우에만 참고한다.

## 6. Grok 조작 (Claude in Chrome, grok.com/imagine)

- 입력창 아래 해상도(480p/720p/1080p)·길이(6/10/15s) 드롭다운.
- 이미지: find로 file input → file_upload → **호출을 끝내고** 다음 호출에서 이미지 모드 클릭(업로드 직후 같은 호출 안의 첫 클릭은 무시됨) → 다음 호출에서 종횡비 16:9, 입력창 입력, 확대 캡처로 확인 후 Enter. 기준 그림이 있으면 결과 페이지로 바로 감.
- 입력이 사라지면 JS로 `form [contenteditable]` focus 후 `document.execCommand('insertText', …)`, 2초 뒤 `form button[type=submit]` 클릭.
- 영상: 결과 페이지 "동영상 만들기" → Add Prompt → `button[aria-label="동영상 길이"]` 메뉴 → 입력 → Enter. 720p·길이는 유지됨.
- 받기: 영상 주소에서 JS `button[aria-label="다운로드"]` 클릭 → **5~6초 기다린 뒤** 이동(바로 이동하면 취소됨). 생성 직후 "포스트를 찾을 수 없음"이면 이미지 주소에서 마지막 `button[aria-label^="Thumbnail"]` 클릭 → 바뀐 주소로 이동해서 받기. 놓친 영상은 /library 에서 찾는다.
- 한도: 720p 이미지+영상 1세트가 주간 한도 약 1.5~2.5%. 31세트에 약 50%.

## 7. Google Flow 조작 (Claude in Chrome, flow.google.com) — 2026-10-08 시험

- 사용자 크롬(PRO 로그인)에서 새 탭으로 `labs.google/fx/tools/flow` → flow.google.com 으로 넘어감. 홈의 "새 프로젝트" 클릭 → 첫 안내창 "시작하기". 위의 "가장 오래된 제작물이 곧 만료" 파란 띠는 무시.
- 입력창 오른쪽 아래 칩(`동영상 · 720p · 8초 · x1` 또는 `Nano Banana 2.1 · x1`)을 누르면 설정 메뉴: 이미지/동영상, 프레임(시작·종료 그림)/소재(참조 그림), 16:9, 모델, 해상도, 길이(4/6/8/10초), 개수(x1~x4). 메뉴 맨 아래에 **이번 생성 크레딧**이 나온다. 메뉴는 Escape로 닫는다. 모델 목록이 열린 채 다른 칸을 누르면 목록 항목이 눌리니(Veo로 바뀜) 한 번에 하나씩 누르고 캡처로 확인.
- 크레딧(2026-10-08 화면): 이미지 Nano Banana 2.1 = **0크레딧**. 동영상 Omni 1.1 Flash 720p 8초 x1 = **12크레딧**, Veo 3.1 Lite 8초 = 10크레딧(Fast·Quality는 더 큼). 영상 제출 버튼은 크레딧을 쓰므로 **사용자가 그 생성을 직접 요청했을 때만** 누른다(자동 모드 분류기도 허락 없이는 막음). 생성은 약 1분.
- 일관성 절차: ① 이미지 모드로 기준 인물 그림(전신, 중간·먼 거리, 얼굴 작게) → ② 동영상 + **소재** 모드, 입력창 왼쪽 `+` → 프로젝트 미디어에서 그림 선택 → "프롬프트에 추가" → ③ 프롬프트에 "The same … from the reference image (옷·소품 나열)" + 새 장면·동작 + "Ambient sound only … No dialogue, no speech, no music" (Omni·Veo는 소리까지 만든다) → 오른쪽 화살표로 제출.
- 영상 받기: 결과 타일에 마우스를 올리면 `video` 요소가 생김(`flow-content.google/video/…`) → 같은 fetch→blob→download. 결과 1280x720, 8.0초, 소리 포함(H.264 mp4). 기다릴 때 JS 안에서 반복 대기하면 45초 제한에 걸리니 wait+캡처로 기다린다.
- 이미지 받기: 결과 타일 `img[alt="사용자 이미지를 표시하는 타일"]`의 currentSrc를 페이지 안 fetch → blob → `<a download>` 클릭 → 사용자 Downloads 폴더에 생김 → 작업 폴더로 mv. 미리보기 이미지는 1376x768 jpg.
- 시험 결과: 기준 인물 `flow_test/flow_ref_truck_driver.jpeg`(트럭 기사, 하늘색 셔츠·주황 감차) — 실사 인도 어른·트럭 아트 잘 나옴, 글자 없음.
- 시험 영상 `flow_test/flow_omni11_dhaba_chai_8s.mp4`(12크레딧, 기준 그림 소재 1장): 옷·감차·콧수염·트럭 아트가 기준 그림과 같게 유지됨, 걷기→앉기→차이 마시기 동작 자연스러움, 대사 없음(평균 -31.5dB 주변음). 밀고 들어가는 카메라라 끝에서 얼굴이 화면 높이 약 1/5까지 커짐 → 얼굴 규칙(1/4 이하) 안이지만 "no push-in"이나 "static wide shot"을 쓰면 더 안전. 캡처 시트 `flow_test/sheet.jpg`.
- 카메라 무빙은 `video-camera` 스킬(장르: 시네마틱 해설 다큐, 모듈 A 장면 + 모듈 B 카메라)을 따른다.
