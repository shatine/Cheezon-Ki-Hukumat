# 9편 TTS 실행 기록

2026-10-27. 상태: **무료 로컬 생성 78/78 완료, 문장별 엄격 검사와 전체 WAV·시간표 무결성 검사 통과.** 직접 청취 검수는 미수행이다.

- 입력: 확정 한국어 24문단에 대응하는 힌디어 78문장. 대본 원문 해시는 `../script/script_lock.json` 참조.
- 설정: charonclone 기준 음성, seed7, speed1.0, 문장 -16LUFS, 24kHz mono, 문장 사이0.35초·문단 사이0.8초.
- PC 위치: `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit`.
- 실측 총 길이: **469.412초(7분 49.412초)**. 24kHz, mono, 24문단·78문장. 마지막 문장 종료와 전체 WAV 프레임 수가 일치한다.
- 생성 방법: seed7 그대로 66문장, 같은 seed의 쉼표 변형 8문장, 같은 seed의 분할·결합 4문장. 모든 결합 결과도 엄격 검사에 통과했다. 실패 ID는 없다.
- 첫 문장 S01a와 같은 질문 S13b·S22b, 긴 문장 S21b는 분할 생성 및 결합 후 검사로 통과했다. 원문 단어는 바꾸지 않았다.
- S01b(최대8천L/min·시공사 귀속), S02b(해발3천m 초과·9.02km), S02c(발주처 귀속·600m 미만·약4년)는 실제 ASR에 모두 보존됐으며 각 WER0.0으로 통과했다.
- 숫자 확인은 **자동 받아쓰기 기록의 검토**다. 직접 청취한 결과와 구분한다.
- 전체 연결 WAV 측정값: **-16.4 LUFS / -1.4 dBTP**. 문장별 -16 LUFS 처리 뒤 정해진 쉼을 연결한 작업용 내레이션이다. 최고음량은 0.1dB 눈금 표시값이며, 최종 편집에서는 채널 납품 기준 -14 LUFS / -1.5 dBTP를 다시 적용·실측해야 한다.
- 한국어 본문 SHA-256: `b6f91f4fcf8a86d100157ee3e1bdb51f4c392780625716b845d7075333eb34c6`. 승인 본문과 일치한다.
- 전체 WAV SHA-256: `0a542c9b8d47e31643948ae8ce1b16f7bbf2962d028d30699e21a24a01353621`.
- 재검증 도구: `verify_tts.py`. 입력 문장·순서, 고정 원문 해시, 실제 WAV 길이/포맷, 문장·문단 쉼, 전체 조립 프레임 수, 엄격 검사 결과, seed 고정, 음량을 확인했다.
- 공유 결과: `narr_timing.json`, `narr_check.json`, `tts_validation.json`. **오디오·캐시·실행 로그는 git에 넣지 않는다.**
- PC 전체 음성: `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\narration_hi.wav`.
- PC 미리듣기: `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\narration_hi_preview.mp3`.
