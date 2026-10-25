# 8편 작업 지시서: Flow 이미지 2차 (다시 만들 11장 + 남은 22장) → push

> ## ⚠ 운영 방식 변경 (사용자 2026-10-25, 즉시 적용, 아래 모든 단계보다 우선)
> Reason: PC session token savings. Screenshots and the conversation grow, so cost rises fast in long sessions.
> 1. **PC는 생성, 저장, 간단 확인만 한다.**
>    - **Quick check** = look at the result **once**, at the size shown on screen. If any of these holds, regenerate right away:
>      - the subject is wrong;
>      - realistic or 3D came out the other way round;
>      - text is obviously visible;
>      - the image is dark.
>    - **Do not** zoom in, compare, or write detailed review notes. The **cloud** does the strict review.
>    - Keep only one image per id (the one that passed the quick check). The cloud will send back what to remake.
> 2. **10장마다 push하고 세션을 끝낸다.**
>    - After 10 images, run step 6 (push) and step 7 (a short report), and **end the session**.
>    - The next PC session starts from this work order again.
> 3. **새 세션의 시작:**
>    - `git pull`, then read only `CLAUDE.md` (상시 허락), this work order and the last section of `picks_v1.md`.
>    - **Read the skill folder only the first time.** From then on, the rules in this work order are enough.
>    - Skip ids that are already in `picks_v1.md` or already in `img\`.
> 4. **진행 중이던 세션:** stop after the image you are working on, push what is finished (step 6), and end. Then start a new session after pulling.
> 5. **Screenshots** only when needed. Check completion by **waiting once** at a long enough interval (about 30–60 s), not by repeated shots.

**Purpose:** finish Flow images for episode 8 and send them to the cloud for review.
- Start from the cloud review results of 2026-10-25: 41 pass, 11 to remake, 22 not yet made.
- **Do not generate any Muse video.** Video comes in a later work order.

## 0. 먼저 읽기 (빠짐없이, 순서대로)
1. `D:\youtube\Cheezon-Ki-Hukumat\guidelines\CLAUDE.md`, including the **상시 허락** section. Do not ask about commit, push, sync or retakes; do them and report.
2. Everything in `D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\` (SKILL.md → references\process.md → script-and-voice.md → prompts.md)
3. `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\HANDOFF_ep08.md`
4. `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\picks_v1.md`, especially the last section, **클라우드 검수 v1**.

## 경로
| 이름 | 경로 |
|---|---|
| Repository (exchange) | `D:\youtube\Cheezon-Ki-Hukumat\` |
| Prompts (latest) | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\prompts_v1.json` |
| Review log | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\picks_v1.md` |
| Image folder (source, permanent) | `D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\img\` (watermark removed), `img_raw\` (originals) |
| Folder for sending to the cloud | `D:\youtube\Cheezon-Ki-Hukumat\episodes\ep08\images\v1\` |

## 1단계: 동기화
```powershell
git -C "D:\youtube\Cheezon-Ki-Hukumat" pull origin main
powershell -ExecutionPolicy Bypass -File "D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1" -Apply
```
- **Check:** in `prompts_v1.json`, the `ref` for `o03` is `CB+o01` and the `ref` for `v14` is `i13a`. If not, the pull did not work, so pull again.

## 2단계: V14 바꿔 쓰기 (생성 없음)
```powershell
Copy-Item "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\img\v1_v14_2.png" "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\img\v1_V14_1.png"
```
- If there is a matching original in `img_raw\`, copy it under the same name too.

## 3단계: 기준 그림을 Flow 프로젝트 미디어에 올리기
- Flow project `baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd`, Nano Banana 2.1, 16:9, x1.
- CB and G3D are already uploaded. **Upload two more:**
  - `o01` = `img\v1_o01_1.png`: the train reference. Every shot with a train attaches it.
  - `i13a` = `img\v1_i13a_1.png`: the real half-arch construction reference, for v14.
- **How to read the `ref` column:**
  | ref | 첨부할 것 |
  |---|---|
  | `CB` | v1_CB_1 |
  | `G3D` | v1_G3D_2 |
  | `CB+o01` | **두 장 모두** (CB first, o01 second). The prompt says "second reference image" |
  | `o01` | v1_o01_1 only (i21: the same composition as the earthquake scene) |
  | `i13a` | v1_i13a_1 only. **Do not attach G3D** (both earlier v14 tries came out as 3D) |
  | `None` | 첨부 없음 |

## 4단계: 다시 만들 11장 (먼저)
Paste each id's `prompt` from `prompts_v1.json` **as it is**. Save as `v1_{id}_{next number}.png`.

| id | ref | 이전 탈락 이유 → 이번 합격 기준 |
|---|---|---|
| V02 | G3D | The Qutub looked like one tower → **five separate copies, each countable**. Eiffel Tower about 9/10 of the deck height |
| o03 | CB+o01 | Same composition as CB → **a camera clearly different from CB** (from far downstream, high). Same train as o01 |
| i03b2 | None | Prayer flags → no flags, shrines or signs |
| i03c2 | CB+o01 | Same angle as the next shot, i03c3 → a close side view of the train at deck height, the train filling the frame width |
| i05a | None | Stupa and prayer flags → only wild mountains |
| i06a | CB | Same composition as CB → looking along the top of the arch from a cliff top at one end |
| V06 | G3D | The half-arches floated in the air → **each half-arch's foot sits on its cliff foundation**, orange arrows go down into the rock |
| i11b2 | CB | Sandstone canyon and calm lake → fast turquoise river, grey rock, the same Himalayan gorge |
| v14 | i13a | Came out as 3D → **real photograph**: the last segment hanging above the gap between the two half-arches |
| i15c2 | CB+o01 | Train blue and red, same composition as CB → looking up from below one side of the arch, the same train as o01 |
| i16a | CB | A second deck appeared → right under one deck looking up, **one deck only** |

## 5단계: 아직 안 만든 22장 (문단 순서대로)
V16a, V16b, i17a, V17, i18a, V18, i19a, i19a2, i19a3, i19b, i19b2, i19c, i19c2, i20a, V20a, V20b, i21, i21b, V22, v23, i23b, i24
- Attach the references given in `ref`. Shots with a train (i21b, v23) attach `CB+o01`.
- Points the cloud already flagged:
  - **글자:** no numbers on the seismograph paper (i15c is already done), no number plate on the signal mast (i19c), no label text on the control-room panel (i19c2). Zoom in to check.
  - **원리:**
    - V16a and V16b: the deck **sits on its bearings**, not fixed.
    - V17: one pier is red and the deck still continues.
    - V18: white wind lines narrow as they pass through the gorge.
    - V20a: only the left half of the arch is red.
    - V22: orange arrows go into both cliffs, plus anchors and bearings.
  - **3D 일관성:** V16a and V20b are close-ups. Keep the same grey steel, white background and colours as G3D and V14.
  - **구도:** i21 must keep **the same composition** as o01 (calm, no dust). i24 must not repeat the previous shot, i23b.
- If a realistic bridge shot copies CB's composition as it is, reject it and generate again (NOCOPY is already in the prompt).

## 생성 규칙 (모든 장)
- **One at a time:** submit → confirm complete → review → next. No rapid repeated submissions (bot detection). Free, so remake as often as needed.
- Remove the watermark the same way as before (dewm.py). Save the original in `img_raw\` and the cleaned version in `img\`.
- **PC 간단 확인** (one look; regenerate only for an obvious failure). The table below is the **cloud** strict-review standard, for reference: you do not need to check it item by item.
  | 항목 | 기준 |
  |---|---|
  | 같은 다리 | Two-rib truss arch, piers on the arch, straight deck, no piers in the river, **the arch spanning from left to right** |
  | 기차 | The same white train as o01 (thin blue stripe) |
  | 3D | Same diorama and colour code as G3D (push = orange, pull = blue, heat = red, wind = white) |
  | 원리 | Arrow directions and attachment state are right (no floating parts) |
  | 사람 | Indian adults, faces small, no children |
  | 글자 | Readable text, numbers, logos, plates, flags or scripts mean rejection |
  | 화질 | Bright, no blurring, no compositing traces |
  | 중복 | Must not look like the shot before or after, or like CB's composition |
- **Record (short):** add one row per image to the table in `picks_v1.md`: id | ref | tries | chosen | a one-line note. For the 11 remakes, the note is "클라우드 재생성".
- **If the generation limit hits mid-way:** do steps 6–7 with what is finished so far, then report.

## 6단계: 클라우드로 보내기 (고른 것만)
**Every 10 images**, copy only the newly **chosen** images into the send folder, then push. After the push, end the session. Do not send rejected tries; this saves space.
```powershell
$img  = "D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge\img"
$repo = "D:\youtube\Cheezon-Ki-Hukumat"
$dst  = "$repo\episodes\ep08\images\v1"
git -C $repo pull origin main
New-Item -ItemType Directory -Force $dst | Out-Null
# 아래 목록을 실제로 고른 파일 이름으로 채운다 (예: v1_V02_4, v1_o03_2 ...)
$chosen = @("v1_V02_4","v1_o03_2")
foreach ($n in $chosen) { Copy-Item "$img\$n.png" $dst }
Write-Host "복사:" (Get-ChildItem $dst -Filter *.png).Count "장"
git -C $repo add -A episodes/ep08
git -C $repo commit -m "EP8: Flow round 2 images for cloud review"
git -C $repo push origin main
```
- If the push is rejected (fetch first), run `git -C $repo pull --no-rebase origin main` and push again.
- The cloud removes `images\v1\` from git after downloading. The originals stay in `img\`.

## 7단계: 보고 (사용자에게)
- The count of remade (out of 11) and newly made (out of 22) images, and the total number of tries.
- Ids still not passing and why.
- Whether the push succeeded (the last line `main -> main`).

## 금지
- Changing the confirmed script, numbers or order.
- Generating Muse videos.
- Rewriting prompts arbitrarily. If you have to change one, add a line to the `picks_v1.md` note saying what you changed and why.
- Editing `.claude\skills` directly.
