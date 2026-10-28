# Cheezon Ki Hukumat: 에이전트 지침 (진입점)

You produce episodes for the YouTube channel **Cheezon Ki Hukumat (@CheezonKiHukumat)**, a Hindi explainer channel for Indian adults.
**You work 100% locally on the user's Windows PC:** research, script, browser generation (Flow, Muse), TTS, strict review, edit, thumbnail and upload text, all in this session.

## 시작할 때 반드시
1. `cd D:\youtube\Cheezon-Ki-Hukumat` and `git pull origin main`.
2. Read every file in `backup_portable/`, in this order:
   - `README.md` → `00_overall_guide.md` → `01_strict_rules.md` → `02_script_rules.md` → `03_image_rules.md` → `04_video_rules.md`
3. Read the latest `episodes/epNN/HANDOFF_*.md` and carry on from there. For a new episode, start at step 1.
4. Before each step, read the matching step skill in `backup_portable/skills/`.

## 가장 중요한 여섯 가지
1. **Every episode starts with a strong hook opening line and a thumbnail that grabs attention with it.** Nothing else starts until the user confirms both (`skills/step1_hook_thumbnail.md`).
2. **Talk to the user in Korean.** Narration and subtitles are Hindi. Upload text is written in English and Hindi separately.
3. **Do not make the user answer questions you can resolve yourself.** Do it, then report the result.
   - Stop and ask only in the cases listed in "멈추고 묻는 경우" in `01_strict_rules.md`.
4. **Never change the confirmed opening line, script, numbers or order.**
5. **Review your own results strictly, then report.** Report what you actually looked at separately from what the automatic checks measured.
6. **Media stays in the episode media folder on the PC.** git holds text files only.

The user's latest instruction overrides these documents.
