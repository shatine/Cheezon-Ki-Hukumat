# 8편 작업 지시서: TTS → 장면 계획 → 이미지 생성·검수 (영상 생성 직전까지)

- **대상:** the PC session (Claude desktop app, local, folder `D:\youtube\7. Cheezon Ki Hukumat`). Written 2026-10-25.
- **목표:** finish everything up to the point before Muse video generation. That means:
  - Hindi TTS and measured timings
  - A sentence-level plan with zero errors
  - Every image generated in Flow and strictly reviewed
  - Video prompts written (**videos are not generated**)
- **규칙:** follow `.claude\skills\cheezon-production`. Read `SKILL.md` and all of `references\` before starting.
- **Generation pace:** Flow one image at a time: submit → confirm complete → review → next. No rapid repeated submissions (bot detection).
- **진행 방식:** follow the **상시 허락** section in `CLAUDE.md`. Do not ask whether to commit, push or sync. Do it, keep going, and report at the end of each step.
  - Stop only for the stop conditions listed in `CLAUDE.md`.

## 경로
| 이름 | 경로 |
|---|---|
| Repository (text, scripts, review logs) | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\` |
| Local working folder (media: wav, png, mp4) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\` (CB below) |
| Skill tools | `D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools\` |
| Confirmed script (do not change) | `episodes\ep08\script\script_ko_final.md`, `episodes\ep08\script\lines_hi_ko.tsv` (70 lines) |
| Reference-video analysis | `episodes\ep08\refs_analysis.md` |

---

## 0단계: 동기화 확인
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" status
powershell -ExecutionPolicy Bypass -File "D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1" -Apply
Get-ChildItem "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills" -Directory
```
- If the sync stops because of uncommitted changes, **commit them as they are without asking** (`git add -A`, `git commit -m "WIP before sync"`, `git push origin main`), then run the sync again.
- If an empty folder remains, delete it after restarting the app. If it can't be deleted yet, leave it and continue to step 1; it does not affect the work.
- `.claude\skills` must contain only `cheezon-production`.

## 1단계: 힌디어 TTS
```powershell
New-Item -ItemType Directory -Force "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\review_edit" | Out-Null
Copy-Item "D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools\tts_template.py" "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\review_edit\tts.py"
Copy-Item "D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\script\lines_hi_ko.tsv" "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\review_edit\lines.tsv"
cd "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\review_edit"
python tts.py
```
- **Pass:** the last line shows `fail 0`, and `narration_hi.wav` and `narr_timing.json` exist.
- **If something fails:** regenerate only the failing ids with `python tts.py S0xx`. Keep seed 7. Do not change the script.
- **Report:**
  - Total length in seconds.
  - Which numbers sound wrong when read aloud, e.g. "तीन सौ उनसठ" and "दो सौ छियासठ". Only the user can actually listen; the session reports the automatic checks only.
- **Into git (text only):** copy `narr_timing.json` to `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\review_edit\narr_timing.json`, then commit and push.
  - `narration_hi.wav` and `narr\` stay in CB.

## 2단계: 장면 계획 (문장 단위, 자동 점검 오류 0)
1. Copy `tools\plan_template.py` to `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\plan\plan_v1.py`. Fill in SEG, VID and IMG for episode 8, based on the measured `narr_timing.json` and the scene draft below.
2. **규칙 (스킬과 같음):**
   - Opening 0–30 s: 3–5 long, natural **videos**.
   - Every **3D principle** sentence is a moving **video**.
   - Of the rest, only 10–20% is video (camera moves or action).
   - Everything else is an **image + effect**, changed every 2–4 s. No image stays longer than 4.5 s.
   - Videos use as much of their usable range as possible. No slow-motion, frozen frames or repeats.
3. Run `python plan_v1.py` until it prints `errors: []`.
4. Commit and push `plan_v1.py`, `shot_list_v1.json` and `shot_table_v1.md`.

### 장면 초안 (문단별, 시간은 TTS 실측에 맞춰 나눈다)
Legend:
- **V** = principle video (required)
- **v** = move/action video (counts toward the 10–20%)
- **I** = image + effect

| 문단 | 내용 | 장면 |
|---|---|---|
| S01 (도입) | 지진? 359m, 강바닥 기둥 없음 | **v** earthquake moment: rocks fall in the gorge, bridge and train intact (the thumbnail scene as a moving shot). **v** low angle from the river looking up 359 m: no piers in the river, deck in the sky. **v** drone along the gorge revealing the whole arch. |
| S02 (도입) | 359m, 에펠탑+35m, 쿠툽 5개, 2025 개통 | **V** 3D height comparison: Qutub Minar ×5 rises beside the Eiffel Tower and the bridge's height bar, without text (numbers go in during editing). **I** bridge with a train on it in bright daylight. |
| S03 | 눈에 막히는 길 → 기차 3시간 | **I** snowbound Kashmir road with stopped trucks. **I** train on the bridge, snowy peaks behind. |
| S04 | V자 협곡, 43~77° | **V** 3D gorge cross-section: the V shape of the valley, the steep slopes appear. |
| S05 | 젊은 산·금 간 바위, 기둥은 미끄러짐 | **I** close-up of cracked, crumbling rock. **V** 3D: a tall pier on one side of the V slowly slides down the slope (a "what would happen" scene). |
| S06 | 아치가 산을 밀며 469m를 한 번에 | **V** 3D: half-arches rise from both cliffs and meet; push arrows run into the mountains. **I** wide realistic view of the arch spanning the gorge. |
| S07 | 늘어진 사슬 → 뒤집으면 아치 | **V** 3D: a chain hangs across the gorge (pull) → flips over → becomes an arch (push). |
| S08 | 산이 그 힘을 버틸까? | **I** crumbling slope with falling gravel. **I** foot of the arch pressing into the rock (realistic close-up). |
| S09 | 시멘트 주입 | **V** 3D rock section: cement fills the cracks and the rock blocks join into one. **I** workers grouting (faces small). |
| S10 | 앵커 당김 → 비탈을 누름, 숏크리트 | **V** 3D: drill → steel tendon → jack pulls it tight → the block presses the slope inward. **I** rows of anchor blocks on the slope (realistic). **I** shotcrete spraying (people small). |
| S11 | 길 없음: 노새·배, 강철 3만 5천 t | **I** mules carrying loads up a mountain track (people small, from behind). **I** a boat on the river. **I** stacked steel plates in the gorge. |
| S12 | 915m 케이블 크레인 | **v** a steel segment hanging from the cable, crossing the gorge (slow side move). **I** cable-crane tower on a cliff top. |
| S13 | 반쪽 아치를 케이블로 뒤에서 붙잡음 | **V** 3D: half-arches growing out over the gap, held by back-stay cables anchored in the rock. **I** realistic: half-arch tip in mid-air, workers tiny. |
| S14 | 2021.4.5 결합, 유압잭 | **v** the crown segment is lowered and the gap closes (realistic). **V** 3D: jacks adjust gap and height → the two halves lock. |
| S15 | 지진: 5구역 기준, 규모 8(정부 발표) | **I** the bridge seen from the foot of the gorge, dust rising (ground shaking). |
| S16 | 상판은 받침 위, 신축이음 | **V** 3D: ground shakes → piers move → the deck rides on its bearings and expansion joints open and close. |
| S17 | 기둥 하나 망가져도 30km/h | **V** 3D: one pier goes red and disappears; the deck holds and a slow train crosses. |
| S18 | 협곡 바람 깔때기 | **V** 3D: wind flow lines narrow through the gorge and speed up. |
| S19 | 지형 모형 풍동 시험, 266km/h, 센서 120개, 빨간불·경보 | **I** wind-tunnel model of the bridge and terrain. **I** sensor box and anemometer on the bridge railing. **I** signal turning red (no lettering). **I** alarm in the station master's room (people from behind). |
| S20 | 햇빛이 한쪽만 → 아치 휨 → 레일 미끄러짐 | **V** 3D: sun heats one side of the arch (red) → slight bend → the rail slides in its fixing. |
| S21 (결) | 처음 질문 다시 | **I** the earthquake scene from the opening, but quiet now (contrast). |
| S22 | 산이 받치고 선로가 흘려보냄 | **V** 3D summary: arch push → reinforced mountain; deck floating on bearings. |
| S23 | 산과 함께 버틴다 | **v** drone pull back: the whole bridge and the mountains together, train crossing. |
| S24 | 구독 | **I** the bridge at sunset with lights on. |

## 3단계: 이미지 프롬프트
1. Copy `tools\image_prompts_example.py` to `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\make_prompts_v1.py` and write the episode 8 list S. Output: `prompts_v1.json`.
2. **기준 그림을 먼저 만들고 확정한다:**
   - **CB (realistic master):** the whole Chenab Rail Bridge, three-quarter view from low in the gorge, bright daylight.
     - One giant two-rib steel truss arch springing from near-vertical cliffs.
     - A flat deck on top on slender steel piers. No piers in the river.
     - Every later realistic bridge shot **attaches this CB image**.
   - **G3D (3D master):** a clean bright 3D diorama of the V-shaped gorge cross-section with the arch and deck. White-grey background, colour code as in the skill.
     - Every later 3D scene **attaches this G3D image**.
   - Optional: a real photo as reference (search terms: Wikimedia Commons `Chenab Rail Bridge`). **Check the photo's license, and record the source URL.**
3. **머리말:** use `references\prompts.md`, with the realistic header and 3D header as they are. For the subject, use a fixed sentence such as "Using the reference image: the SAME Chenab Rail Bridge (giant two-rib steel truss arch, flat deck on slender steel piers, deep V-shaped Himalayan gorge) …".
4. Do not include principle shots in the image-only list. Their images are made as the first frame for the video (still make them, and review them the same way).

## 4단계: Flow 생성과 엄격한 검수
- **Order:** CB → G3D → the rest, in paragraph order.
- **Rule:** one at a time. Free and unlimited, so remake anything you're not happy with.
- **검수 표 (모두 통과해야 채택):**

| 항목 | 기준 |
|---|---|
| 같은 다리 | Arch shape (two ribs, truss), the piers' position on top of the arch, deck straight, no piers in the river. **The same left/right orientation as CB.** |
| 3D 일관성 | Same diorama, same colour code (push = orange arrows, pull = blue, heat = red, wind = white flow lines) |
| 원리 정확성 | Push and pull directions, the anchor pressing *into* the slope, the deck resting on bearings and not fixed |
| 사람 | Indian adults only, faces small, no children, no real people re-enacted |
| 글자 | Readable letters, numbers, logos or number plates mean rejection. Broken Devanagari means rejection |
| 화질 | Bright (dark images rejected), no watermark traces, no blurring, no awkward compositing |
| 중복 | Layout must not nearly match the shot before or after |
| 의미 | The sentence's meaning reads at a glance |

- **Record:** add a row per image to `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\picks_v1.md`: id, reference image, number of tries, why earlier tries failed, why this one was chosen.
- **Save:** originals in `CB\img\v1_{id}_{n}.png`. Watermark-removed versions follow the episode 7 method.

## 5단계: 영상 프롬프트 작성 (생성은 하지 않음)
- For the video segments (V, v, and the opening), write `episodes\ep08\video\make_vprompts_v1.py` → `vprompts_v1.json`.
- **Rules:**
  - Movement / Speed / Framing / End.
  - 3D principle shots are `locked-off static shot` with only the force/flow moving.
  - Moves only on about 2 in 10 video clips; no dolly toward people.
  - Add a constant-lighting sentence ("same bright light for the whole shot, no darkening").
- **Do not run Muse.**

## 6단계: 클라우드 검수 요청
- Copy the selected images (only the chosen `v1_*`) into `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\v1\` and push.
  - The cloud reviews them, then removes them from git right away.
- **Report:**
  - TTS total length.
  - Plan statistics (number of cuts, video/image seconds, video share among non-principle scenes).
  - Image count and number of retakes.
  - Anything still unresolved.

## 금지
- Changing the confirmed script, numbers or order.
- Generating Muse videos.
- Submitting several generation requests in a row.
- Editing `.claude\skills` directly.
