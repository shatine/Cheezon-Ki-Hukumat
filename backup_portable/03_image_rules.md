# 03. 이미지 생성·검수 규칙 (Google Flow)

## 1. 생성 설정
- **Flow:** Nano Banana 2.1, 16:9, x1. One project per episode.
  - Free, so regenerate as often as needed.
  - The result is 1376×768. **Remove the watermark** with `dewm.py`.
  - Save the original in `CB\img_raw\` and the cleaned image in `CB\img\`. Filename: `v1_{id}_{n}.png`.
- **One image at a time:** submit → check it finished (wait 30–60 s, once) → quick check → next.
- **Master reference images are made first:**
  - The main subject as a realistic shot (episode 8 `CB`: the bridge).
  - The 3D diorama (episode 8 `G3D`: gorge cross-section + arch + deck).
  - The recurring object (episode 8 `o01`: a white train with a blue stripe).
  - Upload them to the Flow project's media first.
- **The `ref` column says what to attach:**
  | ref | 첨부 |
  |---|---|
  | `CB` | the realistic master |
  | `G3D` | the 3D master |
  | `CB+o01` | **both**: CB first, the train second. The prompt says "second reference image" |
  | `None` | nothing |
  - A realistic shot should never come out as 3D. Do not attach G3D to a realistic shot. Example from episode 8: v14 came out as 3D twice.

## 2. 프롬프트 틀 (`images/make_prompts_v1.py` → `prompts_v1.json`)
Each row: `(id, ref, kind, script sentence, prompt)`. `kind` is one of:
- `master`: a reference image;
- `image`: an image with an effect in the edit;
- `frame`: the first frame of a video.

**Realistic header**
```
Photorealistic cinematic still, bright clear Indian daylight, vivid natural Bollywood colours, sharp focus, 16:9. No text, no letters, no logos, no watermark. Adults only, people small or medium distance, faces not close-up.
```
**3D header (colour and force codes)**
```
Clean bright 3D educational diorama render, soft studio light, white-grey background, saturated clear colours, 16:9, no text, no labels, no letters. Colour code: heat = red-orange glow arrows, cold = icy blue, clean water = bright blue, waste water = brown-grey, electricity = thick cable with glowing yellow core, moisture = small white droplets. Force code: push = orange arrows, pull = blue arrows, heat = red glow, wind = white flow lines.
```
**Same-object phrase:** the first sentence of the prompt describes the shape in concrete terms.
```
Using the reference image: the SAME Chenab Rail Bridge as the reference image (one giant two-rib grey steel truss arch springing from near-vertical rock cliffs …, no piers in the river, the arch spanning from left to right as in the reference)
```
**Phrase against copying the composition (NOCOPY):** add it to every realistic shot.
```
Use the reference only for the bridge design and orientation; use a clearly different camera position and framing from the reference image.
```
**Fixed recurring object (episode 8 TRAIN):**
```
a white passenger train with a thin blue stripe (the same train as in the second reference image)
```
**Ending:** `No readable text.`

**For each sentence:**
- Choose a change of state, a reaction or a close-up that makes the sentence's meaning readable at a glance.
- People: "Indian adult, face small, seen from behind/side, only hands".
- Scenes that tend to produce text are shot from the side or behind:
  - the fronts of vehicles;
  - city streets;
  - signal masts;
  - control panels;
  - seismograph paper.
  - In the prompt, also write "no number plate", "no label text", "no numbers on paper".
- Wide shots of mountains should not have stupas or prayer flags: write "only wild mountains, no shrines, flags or signs".
- 3D principle shots: the attachment state has to be right.
  - Episode 8: the half-arch's foot sits on the cliff foundation, not floating. The deck sits on bearings.
- Use colour to separate the parts that matter.
  - Episode 8 V17: one pier is red. V20a: only the left half of the arch is red.

## 3. 엄격 검수 (생성 목록을 다 만든 뒤, 같은 세션에서)
Generation and review are separate passes. During generation, do only the quick check (section 4). Once the whole list is made, review every image strictly.

**Preparation:** `python episodes\epNN\images\cloud_review_v1.py "CB\review\img_vN" "CB\img"` (full paths). It produces:
- `auto_report.md`: size, mean brightness, % of dark pixels, **dhash similarity with neighbouring cuts in plan order**, missing ids;
- contact sheets.

**Then look at every image at original size, and zoom in where needed.** The automatic report is only an aid.

| 항목 | 탈락 기준 |
|---|---|
| **Same subject / consistency** | Different shape, colour, number of parts or front. **Different orientation on screen** (episode 8: the arch must span left to right). A second deck, piers in the river, and so on |
| **Recurring object** | A train or vehicle that differs from the master (colour, stripe) |
| **Realistic / 3D** | It came out the other way round |
| **Principle** | Arrow directions, colour code, attachment state (floating parts), cause and effect cannot be read |
| **Meaning** | The sentence's meaning cannot be read at a glance |
| **People** | Not Indian, children, face larger than about 1/4 of the screen height, close-ups of mouths or noses |
| **Text** | Any readable letters, numbers, number plates, brand logos, signs, flags, scripts. Broken Devanagari |
| **Quality** | Dark, blurred, watermark traces, awkward compositing, smearing |
| **Duplicates** | Nearly the same composition as the shot before or after (high dhash similarity, confirmed by eye). **Copying the master (CB) composition** |
| **Natural features** | The landscape is different (episode 8 i11b: a sandstone canyon and calm lake instead of a turquoise river) |

- **Edit fixes, as a last resort, recorded in the plan's `opt`:**
  - `blur_plate`: blur a small plate or label (BLUR coordinates as image ratios x, y, w, h).
  - `bright`: gamma correction (sunset scenes).
  - `hflip`: mirror, only for images without text, to make neighbouring shots face the same way.
  - Edit labels: draw the numbers in the edit instead of in the image (episode 8 V02 "359 m", "×5"). A number the image cannot show is added as a label.
- **Record:** add a section per review round to `images/picks_v1.md`:
  - each id: pass / remake (why → what to change in the prompt);
  - the final pick filename, for example `V02 = v1_V02_6`.
- **Remakes:**
  - Fix the prompt in `make_prompts_v1.py`, run it again, and update `prompts_v1.json`.
  - Regenerate only those ids in Flow, then review them again.
  - Repeat until every image is confirmed. Episode 8: 74 images over 4 review rounds.

## 4. 생성 중 간단 확인
- One look, at the size shown on screen. Regenerate right away only in these cases:
  - the subject is wrong;
  - realistic and 3D are swapped;
  - text is obviously visible;
  - the image is dark.
- No zooming or comparing at this point; that is the strict review's job. Keep one image per id (the one that passed the quick check).
- Write one line per image in `picks_v1.md`: id | ref | tries | chosen | note.
