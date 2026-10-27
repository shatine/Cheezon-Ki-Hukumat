# ep09 libass 정지 프레임 조판 검토

실측 문장·라벨이 활성인 시각 5개에서 `ffmpeg color → libass → PNG 1프레임`을 각각 실행했다. 영상·클립·음성·가짜 영상 소스는 만들지 않았다. 승인 문구·타임코드·폰트·배치는 변경하지 않았다.

PNG는 모두 1920×1080이며 PC의 아래 폴더에만 저장했다.

`D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\image_review_v1\subtitle_qa`

| 문장 / 라벨 | 실제 문장 구간(초) | 정지 프레임 시각(초) | 파일 | 검토 초점 |
|---|---:|---:|---|---|
| S01b / L01 | 3.903–12.956 | 8.430 | qa_S01b_L01_008430ms.png | 시공사 귀속·최대 8,000리터/분 |
| S02b / L02 | 25.634–33.565 | 29.600 | qa_S02b_L02_029600ms.png | 9.02 소수·3,000 고도·두 줄 라벨 |
| S02c / L03 | 33.915–45.518 | 39.716 | qa_S02c_L03_039716ms.png | HI 3줄+KO 2줄·라벨 3줄·BRO 귀속·상부 굴착 약 4년 |
| S20b / L08 | 403.088–411.542 | 407.315 | qa_S20b_L08_407315ms.png | 2020년 10월 3일 날짜 |
| S21b / L09 | 416.241–427.096 | 421.668 | qa_S21b_L09_421668ms.png | HI 3줄+KO 2줄·2024년 글·결합문자/누크타/찬드라빈두 |

5장 원본을 assistant가 `view_image(detail="original")`로 직접 열어 확인했다. 표본에서 눈에 띄는 대체 사각형 문자, 결합문자 분리, 외곽 잘림, HI/KO 상호 겹침, 상단 라벨과 하단 자막 겹침을 발견하지 못했다. 긴 HI 3줄+KO 2줄도 현재 프레임 안에 들어온다. 폰트·레이아웃 수정은 하지 않았다.

실제 libass fontselect 로그는 `Nirmala UI, 700 → NirmalaUI-Bold`와 `Malgun Gothic, 700 → MalgunGothicBold`를 확인했다. 누락 glyph 오류 로그는 0이다. 각 PNG SHA256, 실제 문장 구간, 표본 시각과 폰트 로그는 `subtitle_qa_v1.json`에 기록했다. ASS·timing·overlay의 실행 전후 SHA도 동일하다.

root도 위 5개 원본 PNG를 모두 원본 크기로 직접 열어 확인했다고 명시적으로 보고했다. 확인 시각은 8.430 / 29.600 / 39.716 / 407.315 / 421.668초이며, 눈에 띄는 glyph 깨짐·잘림·HI/KO 겹침·라벨 충돌은 발견하지 못했다. 폰트·문구·타이밍 변경은 필요하지 않다고 확인했다. root가 검토한 5개 PNG의 SHA256은 JSON의 `root_original_png_review`에 연결해 기록했다.

이 결과는 단색 배경 위 5개 정지 조판 표본의 검토다. 실제 장면 위 가독성, 전체 78문장·9라벨 모든 조합, 자막 전환·음성 동기 및 최종 영상 검수는 미수행이다. 업로드용 한 줄 자막은 계속 보류한다.

`edit_preflight_v1.json`의 자막 시각검수 미수행 표시는 최초 preflight 당시의 상태다. 이 문서와 `subtitle_qa_v1.json`이 그 후 수행한 정지 표본 검토를 보충하며, 전체 렌더 완료나 `render_ready=true`로 바꾸지 않는다.

재현 명령:

```powershell
python 'C:\Users\developer1\Documents\ChatGPT\프로젝트명 미정\work\ep09_atal_tunnel\review_edit\subtitle_qa_v1.py'
```

스크립트는 정지 PNG와 기계 실행 결과 JSON만 만든다. 재실행이 사람의 시각 검토 기록을 자동으로 새로 승인하지 않는다.
