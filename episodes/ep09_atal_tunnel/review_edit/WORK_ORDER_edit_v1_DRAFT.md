# ep09 편집 준비 작업지시서 — DRAFT

현재 범위는 입력·실물 미디어 preflight와 문장 실측 검토 자막이다. 전체 편집 렌더러는 구현하지 않았다. 실제 렌더, 영상 검수 완료, Muse 전송·생성, 업로드, BGM 작업을 수행했다는 뜻이 아니다.

## 현재 입력과 결과

- 승인된 한국어 원문과 힌디어 문장, 실제 TTS 타이밍을 변경하지 않는다.
- 실제 내레이션: 78문장 / 24문단 / 469.412초.
- 컷 계획: 79컷 / 30fps / 연속 14,112프레임 / 470.4초. 내레이션 뒤 약 1초 여백을 포함한다.
- 첫 실행에서 핵심 입력 검사 오류 0. 실제 컷 소스 79개가 없거나 미선택 상태라 `blocked_missing_or_unreviewed_media`, 종료 코드 2, `render_ready=false`가 정상 결과였다.
- 실제 WAV는 읽기 전용 ffprobe로 확인한다. TTS 파일·타이밍을 재생성하거나 정규화하지 않는다.

## 실행

Python과 Pillow가 필요하다. `ffprobe`가 PATH에 있어야 실물 파일 검사를 진행한다. 100% 로컬 작업이므로 저장소의 스크립트를 PC 미디어 폴더에 바로 실행한다.

```powershell
python 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\edit_v1.py' --check-only --make-review-subtitles --media-root 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel'
```

종료 코드 0은 요청한 준비 검사의 종료이고 렌더 준비 완료 판정이 아니다. 1은 입력 오류로 중지, 2는 실제 미디어·선택·실측 USE·명시 검토 기록 부족으로 중지한다. 자막만 다시 만들 때 `--subtitles-only`를 사용한다. 이 모드는 preflight 보고서의 미디어 검사 항목을 수행하지 않은 상태로 다시 기록하므로, 최종 상태를 남길 때는 위 `--check-only --make-review-subtitles`를 실행한다.

## 검토용 자막

- `subs_hi_review_v1.srt`: 힌디어 78큐.
- `subs_ko_review_v1.srt`: 한국어 78큐.
- `subs_review_v1.ass`: HI+KO 문장 156이벤트와 실측 수치 라벨 9이벤트.
- 각 큐는 `narr_timing.json`의 실제 문장 시작·끝을 사용한다. 문장 내부 줄바꿈만 적용한다. 글자 수 비례 시간 분배나 새 중간 시각을 만들지 않는다.
- SRT는 밀리초, ASS는 센티초 표기 반올림만 발생한다. 허용 최대 오차는 각각 0.0005초 / 0.005초다.
- 업로드용 힌디어 한 줄 자막은 보류한다. 긴 문장을 나눌 정확한 발화 pause 또는 word alignment를 확보한 뒤 편집·검수해야 한다.
- ASS는 1920×1080 기준, HI Nirmala UI 58 / KO Malgun Gothic 44 / 자간 0이다. KO 아래, HI 위에 배치한다. 수치 라벨은 상단 안전 영역에 둔다.
- 현재 Pillow RAQM이 비활성이다. 폭 계산은 여유를 둔 임시 측정이며 힌디어 조형과 실제 libass 레이아웃 검수는 수행하지 않았다. 검토용 HI 최대 3줄 / KO 최대 2줄이므로 최종 한 줄 자막으로 취급하지 않는다.

## 실제 미디어가 들어온 뒤의 중지 조건

정지 이미지는 `images/picks_v1.json`에 실제 선택된 파일명·시도 번호를 사용한다. `_1` 등 임의 번호나 master를 대체 소스로 만들지 않는다. 실제 PNG SHA·픽 원장 SHA·크기, 명시적인 clean 원본 검토가 일치해야 한다.

각 원본 클립을 ffprobe로 열어 duration·fps·크기를 읽는다. 타임라인의 소스 끝과 수동 검토 USE 끝은 모두 `실제 duration - 0.05초` 이하여야 한다. 예정한 10초 제작 요구 사양과 임시 USE는 실제 파일 실측을 대신하지 못한다.

추후 실제 클립을 보고 1초 간격 프레임·0.5초 간격 밝기 검사를 마친 사람이 아래 명시 검토 원장을 별도로 작성해야 한다. 현재 이 파일은 만들지 않았으며, 코드가 시각 합격이나 USE를 자동으로 만들어 넣지 않는다. 파일명·SHA·실측 USE가 현재 실물과 다르면 중지한다.

```json
{
  "clips": {
    "p001": {
      "status": "confirmed",
      "visual_review_performed": true,
      "file": "clips_v1/p001.mp4",
      "sha256": "실제 검토한 파일의 SHA256",
      "usable_ranges": [[0.0, 9.90]]
    }
  }
}
```

위 숫자는 스키마 예시이며 실제 p001의 실측·검토 결과가 아니다. 기본 경로는 해당 episode의 `video/review_clips_v1.json`이며 `--clip-review`로 다른 실제 원장을 지정할 수 있다. `visual_review_performed=true`는 사람이 실제 검토를 마쳤다는 신고여야 한다. 존재·해시·범위의 기계 검사 통과가 영상 시각 검수 완료를 뜻하지 않는다.

## 후속 미완료 작업

실제 소스와 USE가 확보된 뒤 전체 렌더러 구현, step7의 격리된 전체 가짜 소스 렌더 검사, 실제 libass 자막 레이아웃 확인을 수행해야 한다. 최종 영상은 작은 사본이 아니라 PC 원본 `out\v1_review_hi.mp4`로 0초부터 끝까지 화면·음성·전환·수치 라벨을 검수하고 수정한다. 처음 10초에서 확정 도입부 문구가 또렷하게 들리고 보이는지도 확인한다. 현재는 이 작업들을 수행하거나 완료했다고 기록하지 않는다.

현재 파일은 사전 준비 초안이다. 실제 영상 생성 승인, 외부 게시, 음악 구매·생성, production render를 지시하지 않는다.
