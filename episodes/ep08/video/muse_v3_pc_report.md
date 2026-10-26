# 8편 Muse 다시 만들기 v3: PC 보고 (2026-10-26)

- **Result:** 4 of 4 made, none refused by Muse.
  - Made in Muse 9227, in a new side chat for every try.
  - The `retake_v3` prompts were pasted unchanged.
  - Every clip is 10.0 s at 1216x672.
- **Files:**
  - Pushed: `video/v1/{id}.mp4` (4 files).
  - On the PC, in `clips_v1\old\`:
    - the v2 versions, as `{id}_v2.mp4`;
    - every v3 try, as `{id}_v3t1/t2/t3.mp4`.
  - V20a and v23 keep their v2 versions, as instructed.
- **Strict review is the cloud's.** The quick check below is one 8-frame sheet per clip.

| id | 시도 | 올린 본 | 간단 확인 |
|---|---|---|---|
| V09 | 3 (at the limit) | try 3 | **Not passed.** In all 3 tries the grey cement spreads over the block's front face, and by the end it covers the whole face. Try 1 also changed the top slope. Try 3 adds blue arrows that spread out from the needle and is the closest to the intent, but the grey covering remains. |
| V16a | 2 | try 2 | Passed. The deck pieces and bearings stay in place, and only the blue light and arrows pulse. Try 1 failed because the two deck pieces moved apart in the second half. |
| V16b | 1 | try 1 | Passed. The bridge and terrain stay the same, and only the blue lights and the shake marks at the base move. |
| V20b | 3 (at the limit) | try 2 | **Close to passing.** The rails stay visible for most of the clip, but around 2 s they briefly disappear in the strong red glow on the left half. In try 1 the left deck surface turned into a melted red mass and the rails were lost. In try 3 the left rails were hidden by the glow for most of the middle. |

- **For the cloud:**
  - V09 fails the same way with every prompt so far. Muse seems to treat "grout fills the rock" as covering the block. The prompt may need another approach.
  - Making a clip in Flow costs credits and needs the user's instruction.

## 추가: V09·V20b를 Flow에서 다시 만듦 (사용자 지시, 2026-10-26)
- **Why:** the user asked for the clips that did not pass to be made in Flow. That was V09 (failed) and V20b (close, but not passed).
- **Settings:**
  - Flow, 1 try each, the start frame is the same `image`, the v3 prompt is unchanged.
  - Omni 1.1 Flash, 720p, 10 s, x1, 15 credits each, 30 credits in all.
- **Files:** `video/v1/V09.mp4` and `video/v1/V20b.mp4` are now the Flow clips. The Muse versions are kept on the PC as `clips_v1\old\{id}_muse_final.mp4`.
- **Spec differs:** 1280x720, 24 fps, 10.0 s. The Muse clips are 1216x672. V05 is a Flow clip too.

| id | 간단 확인 (Flow) |
|---|---|
| V09 | The block's shape and position, the pipe and the outer surfaces stay the same. No cement leaks or covers the face. The cracks turning grey is **weak**: only a few thin grey lines appear around the middle. |
| V20b | Both rails and all fastenings stay visible for the whole clip. Orange arrows pulse along the rails. The red glow on the left half **fades almost completely out in the middle** and comes back at the end, so check that this "breathing" is acceptable. |
