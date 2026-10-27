# 9편 TTS 작업 지시서 — 생성·엄격 검사·실측 시간표

2026-10-27. 한국어 확정 승인: 같은 날짜 사용자 “진행”. 무료 로컬 생성만 실행한다. 영상 생성 승인이 아니다.

진행 현황: **78/78 생성·엄격 검사·전체 조립 검증 완료. 469.412초.** 실패 ID 없음. 완료된 WAV는 유지하며 아래 명령은 재개·재검증할 때만 사용한다. `review_edit/tts_report.md`, `tts_validation.json` 참조. 직접 청취 검수는 미수행이다.

## 경로

| 용도 | 전체 경로 |
|---|---|
| 저장소 | `D:\youtube\Cheezon-Ki-Hukumat` |
| 확정 한국어 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\script\script_ko_final.md` |
| 힌디어·직역 78행 | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\script\lines_hi_ko.tsv` |
| PC TTS 폴더 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit` |
| 실행기 | `D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\tts.py` |
| 기준 도구 | `D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools` |

## 1. 준비 / 다른 PC 세션에서 재개할 때

```powershell
git -C 'D:\youtube\Cheezon-Ki-Hukumat' pull --ff-only origin main
New-Item -ItemType Directory -Force -Path 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit' | Out-Null
Copy-Item -LiteralPath 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\tts.py' -Destination 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\tts.py'
Copy-Item -LiteralPath 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\tts_config.json' -Destination 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\tts_config.json'
Copy-Item -LiteralPath 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\script\lines_hi_ko.tsv' -Destination 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\lines.tsv'
Invoke-RestMethod 'http://127.0.0.1:3900/health'
```

기대 결과: Voice Studio `status: ok`. 기준 PC 도구는 저장소와 파일 해시가 같은지 확인했다. 번역 입력과 기준 음성의 SHA-256도 실행기가 검사한다.

## 2. 생성·엄격 검사

```powershell
python -u 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\tts.py'
```

- charonclone, seed7, speed1.0, 문장 -16LUFS, 문장 간0.35초, 문단 간0.8초.
- seed를 바꾸지 않는다. 같은 seed에서 쉼표 변형→분할→반분의 기존 재시도 경로를 사용한다.
- 통과한 줄은 재실행 시 건너뛴다. 불합격은 기록하며 임의로 PASS 처리하지 않는다.
- 한 줄 재검사는 `--only S01a --redo S01a`처럼 명시한다. 문구는 바꾸지 않는다.
- `narration_hi.wav`, `narr\*.wav`와 캐시는 PC에 둔다. 힌디어 대본을 시간에 맞춰 자르거나 속도를 바꾸지 않는다.

## 3. 결과 공유

전체 생성 뒤 실제 WAV와 시간표를 검증한다.

```powershell
python 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\verify_tts.py'
```

`automatic_checks_passed`, 78문장·실패0·오류0을 확인했다. `narr_timing.json`, `narr_check.json`, `tts_validation.json`과 검사 요약만 저장소에 넣는다. 오디오는 git에 넣지 않는다.

```powershell
Copy-Item -LiteralPath 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\narr_timing.json' -Destination 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\narr_timing.json'
Copy-Item -LiteralPath 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\narr_check.json' -Destination 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\narr_check.json'
Copy-Item -LiteralPath 'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit\tts_validation.json' -Destination 'D:\youtube\Cheezon-Ki-Hukumat\episodes\ep09_atal_tunnel\review_edit\tts_validation.json'
git -C 'D:\youtube\Cheezon-Ki-Hukumat' add -- 'episodes/ep09_atal_tunnel/review_edit/narr_timing.json' 'episodes/ep09_atal_tunnel/review_edit/narr_check.json'
git -C 'D:\youtube\Cheezon-Ki-Hukumat' commit -m 'Add ep09 measured narration timing and checks'
git -C 'D:\youtube\Cheezon-Ki-Hukumat' push origin main
```

push가 fetch-first로 거절될 때만 `git pull --no-rebase origin main` 후 다시 push한다. 실제 생성 개수·실패 ID·총 실측 길이·자동 검사와 직접 청취 범위를 나눠 보고한다. 같은 실패가 수정 후 세 번 반복되면 그 원인과 생성물을 보존하고 사용자에게 보고한다.
