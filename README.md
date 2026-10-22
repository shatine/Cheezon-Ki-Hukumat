# Cheezon Ki Hukumat

YouTube 채널 Cheezon Ki Hukumat (@CheezonKiHukumat) 제작 지침과 스킬, 제작 중인 편의 재료.

- `guidelines/` — CLAUDE.md, CHANNEL.md (PC `D:\youtube\7. Cheezon Ki Hukumat`)
- `skills/` — PC `.claude\skills` 전체 (영상 제작 전 반드시 읽을 것)
  - cheezon-video, cheezon-script, cheezon-claude-review는 최신 Codex 채널판(원본 `C:\Users\developer1\.codex\skills`, 사본 `폐버스가집이 될수없는 이유\제작_인계가이드\스킬_원문\Codex_채널`, 2026-10-19). `.claude\skills`의 같은 이름 스킬은 이보다 옛판이다.
  - **새 편 제작 공정 (필수):** `skills/cheezon-video/references/production-process.md`. 7편 완료 후 확정한 전체 순서, 검수 기준, 재발 금지 목록이 있다.
  - 영상 작업 읽는 순서: cheezon-video/SKILL.md → references/shot-plan.md → references/bhopal-production-lessons.md → references/production-process.md → video-camera·screen·edit·text·sound·verify
  - PC `.claude\skills`에도 이 저장소의 `skills/cheezon-video/`를 복사해 맞춘다.
- `episodes/ep07_bus/` — 7편 "버스에서 살 수 있을까요?"
  - `HANDOFF_ep07_2026-10-21.md` — 인계 요약, 규칙, 다음 할 일, 올리지 않은 이미지·영상의 PC 경로
  - `script/` — 한국어 대본 v3, 힌디 대본 + 한국어 직역 88줄
  - `images/` — Flow 이미지 프롬프트, 고른 목록, 카메라 무빙 선정, 모아보기
  - `video/` — Muse 영상 프롬프트, 쓸 구간
  - `plan/` — 컷 계획 v9 (plan_v9.py 점검·생성, shot_table_v9.md, shot_list_v9.json)
  - `review_edit/` — 검수 영상 TTS·편집 스크립트(edit_v9.py가 최신), 컷 목록, 자막

영상·원본 이미지·나레이션 음성은 용량 때문에 올리지 않았다. 위치는 HANDOFF 맨 아래 "로컬 경로".
