# 9단계: PC 작업 지시서 틀, git 주고받기, 검수 보고 방법

## 작업 지시서 틀 (`episodes/epNN/WORK_ORDER_<이름>.md`)
```
# N편 작업 지시서: <무엇> → push (YYYY-MM-DD)

목적: <한 줄>. PC는 생성·저장·간단 확인만, 엄격한 검수는 클라우드.
- 비용: <무료 / 사용자 허락 YYYY-MM-DD "시작">. 상시 허락(CLAUDE.md)대로 묻지 말고 진행.
- 목록 전체를 끊지 않고 만든 뒤 한 번에 push. 한도에 걸리면 만든 것까지 push하고 새 세션에서 이어 간다.

## 0. 먼저 읽기 (짧게)
1. D:\youtube\Cheezon-Ki-Hukumat\guidelines\CLAUDE.md (상시 허락)
2. 이 지시서
3. <입력 JSON 전체 경로>

## 경로
| 이름 | 경로 |   ← 모두 전체 경로

## 1단계: 동기화와 확인
(붙여 넣을 수 있는 PowerShell 명령. 기대 결과를 적는다: True / 개수 / ok)

## 2단계: <생성 또는 렌더>
(한 개씩, 입력값 그대로, 다시 만드는 조건 최대 2회, 거부 시 처리)

## 3단계: 클라우드로 보내기
$repo = "D:\youtube\Cheezon-Ki-Hukumat"; git pull → Copy-Item → (크기 확인) → git add → commit → push
- 거절되면 git pull --no-rebase origin main 후 다시 push. 마지막 줄 main -> main 확인.
- 95MB 넘으면 push하지 말고 보고.

## 4단계: 보고
- 만든 개수 / 다시 만든 id / 거부 id / 실제 길이·해상도 / push 성공 여부

## 금지
- 대본·숫자·순서·프롬프트 변경, 다른 첫 프레임, 글자만으로 생성, 연속 제출, 스크립트 수정, .claude\skills 직접 수정
```
- **Status of work orders:** once one is finished, put "진행 현황: 완료" at the top. If the rules change mid-way, add an overriding notice box at the top (for example "⚠ 운영 방식 변경").
- **PC messages to the user:** give one line they can paste into a new PC session:
  - "git pull 하고 D:\youtube\Cheezon-Ki-Hukumat\episodes\epNN\WORK_ORDER_x.md 대로 진행해"

## git 주고받기 (클라우드)
1. When the user says "푸시했대":
   - `git fetch origin main` and `git log origin/main`, to confirm the PC commit is really there.
   - If it is not there, ask the user to check it with `git status`, `git log --oneline -3` and `git push origin main` (three cases: commit only / not committed / over 95 MB).
2. Pull → copy the media to the scratch folder → `git rm -r` that folder → commit "remove … after cloud download (kept on PC)" → push.
3. After reviewing, commit and push the records (picks, review, plan, prompts, work order, HANDOFF) together.

## 검수 보고 형식 (사용자에게, 한국어)
- **First line:** the verdict (pass / N fixes / N remakes).
- **Table:** item | result, with the key numbers.
- **What was fixed:** before → after.
- **Left as is:** with the reason.
- **What happens next**, and the line to give the PC (full paths).
- Keep what was seen by eye separate from what was measured automatically. Do not claim to have reviewed what you have not looked at.
- If you could not see the original (because it is on the PC), say so, and say which copy you reviewed instead.

## HANDOFF 갱신 (매 단계)
- Status table: step | state | result (file paths).
- "다음 클라우드 세션이 할 일": what to do when the next push arrives.
- Confirmed items (opening line, thumbnail, script, number rules) and the user's preferences.
