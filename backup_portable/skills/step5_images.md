# 5단계: 이미지 프롬프트 → PC 생성 → 클라우드 엄격 검수 → 재생성 → 전부 확정

**규칙:** `../03_image_rules.md` (all of it).

## 클라우드: 프롬프트
1. Copy `episodes/ep08/images/make_prompts_v1.py` and fill in only the `S` list for the new episode.
   - **Master reference images first.** Realistic master `CB`, 3D master `G3D`, recurring object (for example the train `o01`).
   - Then every `IMG` (kind `image`) and `VID` (kind `frame`, the first frame of a video) in the plan.
   - Each prompt = header (realistic or 3D) + "Using the reference image: the SAME …" + scene + NOCOPY (realistic) + "No readable text."
2. Running it produces `prompts_v1.json`: `id`, `ref`, `kind`, `script`, `prompt`.
3. **PC work order** (step 9 template). Order:
   - masters → upload them to the Flow project media → everything else in paragraph order.
   - Attach the files given in the `ref` column.
   - Remove the watermark (`dewm.py`); originals in `img_raw\`, cleaned images in `img\`.
   - Copy the chosen images into `episodes/epNN/images/v1/`, then push them once.

## PC
- One at a time. Paste the prompt as it is. Quick check only. Make the whole list, then push once.

## 클라우드: 검수 (회차마다)
1. `git pull` → copy `images/v1/*.png` to the scratch folder → `git rm -r episodes/epNN/images/v1` → commit and push.
2. Run `python3 episodes/epNN/images/cloud_review_v1.py <scratch>/out <scratch>/src` → read `auto_report.md` and the sheets.
3. **Look at every image at original size** (review table in `03_image_rules.md`).
   - Look for neighbouring duplicates (dhash), copies of CB's composition, the subject's orientation on screen, text, faces, principle arrows and brightness.
4. Add a "클라우드 검수 vN" section to `picks_v1.md`: pass list, remake list (cause → prompt change), edit options (blur, brightness, labels).
5. Fix the remake prompts in `make_prompts_v1.py` → run it again → write a work order for **only the ids to remake** → push.
6. Repeat until every image is confirmed. Write the final pick for each id (for example `V02 = v1_V02_6`) and copy it into the plan's `PICK_N`.

## 완료 기준
- Every id is confirmed, and the edit options (`blur_plate` coordinates, `bright` gamma, labels) are recorded.
