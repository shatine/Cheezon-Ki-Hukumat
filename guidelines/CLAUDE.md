# Cheezon Ki Hukumat

The channel's only production skill is `.claude/skills/cheezon-production/`. Before starting any work, read the whole of `SKILL.md` and its `references/` folder.

The skills and lessons from earlier episodes were all deleted on 2026-10-24 at the user's instruction. Only what was confirmed in episode 7, "버스에서 살 수 있을까요?", is kept. Where it disagrees with the latest user instruction, follow the latest instruction.
- Leave completed videos and confirmed scripts as they are. Do only the steps the user has approved.
- Roles:
  - **Cloud session:** script, plan, prompts, review, upload text.
  - **PC session:** generating images and video in Flow and Muse, and the final render.
- Exchange files through the `main` branch of GitHub https://github.com/shatine/Cheezon-Ki-Hukumat.

## 상시 허락 (사용자 2026-10-25): 묻지 말고 진행할 것
The user has authorized the following once and for all. **Do not ask "should I?"; do it, then report the result.**
- **Commit and push to git:** any file inside the repository `D:\youtube\Cheezon-Ki-Hukumat` (scripts, plans, review logs, selected images) may be committed and pushed to `main`. That includes uncommitted earlier-episode files: commit them as they are, push, and carry on.
- **동기화:** run `guidelines\sync_pc.ps1 -Apply`, and delete what it deletes: old skills and empty folders.
- **작업 지시서:** carry out each step through to the end, retrying anything that failed (TTS lines, image retakes) yourself.
- **Flow 이미지 생성:** generate and retake as many times as needed, one at a time. Free.

**Stop and ask only when:**
- a step would change the confirmed script, numbers or order;
- something would cost money, or a Muse video would be generated (unless the work order allows it);
- a file outside the repository and the episode working folder would be deleted;
- the same failure repeats 3 times after trying a fix.
