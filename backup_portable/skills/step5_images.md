# 5단계: 이미지 프롬프트 → Flow 생성 → 엄격 검수 → 재생성 → 전부 확정

**규칙:** `../03_image_rules.md` (all of it).

## 프롬프트
1. Copy `episodes/ep08/images/make_prompts_v1.py` and fill in only the `S` list for the new episode.
   - **Master reference images first.** Realistic master `CB`, 3D master `G3D`, recurring object (for example the train `o01`).
   - Then every `IMG` (kind `image`) and `VID` (kind `frame`, the first frame of a video) in the plan.
   - Each prompt = header (realistic or 3D) + "Using the reference image: the SAME …" + scene + NOCOPY (realistic) + "No readable text."
   - The opening shots (0–30 s) must show exactly what the hook line says.
2. Running it produces `prompts_v1.json`: `id`, `ref`, `kind`, `script`, `prompt`.

## 생성 (Flow, 한 장씩)
1. Masters first → upload them to the Flow project media → everything else in paragraph order.
2. Attach the files given in the `ref` column. Paste the prompt from the JSON as it is.
3. Submit → wait 30–60 s and check once → quick check (section 4 of the rules) → next.
4. Remove the watermark (`dewm.py`); originals in `CB\img_raw\`, cleaned images in `CB\img\`.
5. Make the whole list without stopping to report.

## 엄격 검수 (회차마다)
1. Run `python episodes\epNN\images\cloud_review_v1.py "CB\review\img_vN" "CB\img"` → read `auto_report.md` and the sheets.
2. **Look at every image at original size** (review table in `03_image_rules.md`).
   - Look for neighbouring duplicates (dhash), copies of CB's composition, the subject's orientation on screen, text, faces, principle arrows and brightness.
3. Add a "검수 vN" section to `picks_v1.md`: pass list, remake list (cause → prompt change), edit options (blur, brightness, labels).
4. Fix the remake prompts in `make_prompts_v1.py` → run it again → regenerate **only those ids** in Flow → review them again.
5. Repeat until every image is confirmed. Write the final pick for each id (for example `V02 = v1_V02_6`) and copy it into the plan's `PICK_N`.
6. Commit the records (prompts, picks, plan). Never the images.

## 완료 기준
- Every id is confirmed, and the edit options (`blur_plate` coordinates, `bright` gamma, labels) are recorded.
