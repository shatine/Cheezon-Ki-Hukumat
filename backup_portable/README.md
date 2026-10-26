# Cheezon Ki Hukumat 제작 지침 백업 (도구 공통판, 2026-10-26)

**Purpose:** let another AI coding agent (Codex, Gemini CLI and so on) reproduce the same production work that ran in Claude Code up to episode 8.
- **Contents:** everything confirmed in episode 7 ("버스에서 살 수 있을까요?") and episode 8 ("체납 철교", uploaded 2026-10-26):
  - rules and lessons;
  - the user's preferences;
  - mistakes not to repeat.
- **Source documents (originals):**
  - `guidelines/CLAUDE.md`, `guidelines/CHANNEL.md`
  - `skills/cheezon-production/` (SKILL.md, references/, tools/)
  - each `episodes/epNN/HANDOFF_*.md`
- This folder gathers their content in one place and in a tool-independent form.
- **If they conflict:** the user's latest instruction comes first. Next is this folder. Next are the original documents.

## 도구별 불러오기
| 도구 | 방법 |
|---|---|
| **Codex (CLI / IDE)** | Reads `AGENTS.md` at the repository root automatically. Copy `backup_portable/AGENTS.md` to the root, or start the session with "backup_portable/AGENTS.md를 먼저 읽어". |
| **Gemini CLI** | Reads `GEMINI.md` at the root automatically. Copy `backup_portable/GEMINI.md` to the root, or give the same instruction. |
| **Any other tool** | Start with "backup_portable/README.md부터 순서대로 다 읽고 작업해". |

`AGENTS.md` and `GEMINI.md` have the same content. Each is a short entry point that tells the agent to read the whole of this folder.

## 읽는 순서 (빠짐없이)
| 순서 | 파일 | 내용 |
|---|---|---|
| 1 | `00_overall_guide.md` | Channel, roles (cloud/PC), file exchange, folder layout, tools, the whole process at a glance |
| 2 | `01_strict_rules.md` | **Never do this.** Rules that must not be broken |
| 3 | `02_script_rules.md` | Script rules: question chain, evidence, number rule, Hindi, TTS |
| 4 | `03_image_rules.md` | Image generation and review rules (Flow) |
| 5 | `04_video_rules.md` | Video generation and review rules (Muse / Flow video) |
| 6 | `skills/` | Step skills 1–9. Read the matching file before starting each step |

## 단계별 스킬 (skills/)
| 파일 | 단계 |
|---|---|
| `skills/step1_topic_opening.md` | Topic choice, reference video analysis, opening line = thumbnail text |
| `skills/step2_script.md` | Korean script, evidence table, user review, freezing it |
| `skills/step3_hindi_tts.md` | Hindi line mapping, TTS, measured timing table |
| `skills/step4_plan.md` | Sentence-level cut plan with automatic checks |
| `skills/step5_images.md` | Image prompts → PC generation → strict cloud review |
| `skills/step6_video.md` | Video prompts → PC generation → frame review → usable ranges |
| `skills/step7_edit.md` | Review-cut render → review from 0 s to the end → upload-cut render |
| `skills/step8_upload_thumbnail.md` | Upload text (EN/HI separately), keywords, thumbnail |
| `skills/step9_work_orders.md` | PC work order template, git exchange protocol, how to review |

## 실제 자료 (그대로 템플릿으로 쓴다)
- `skills/cheezon-production/tools/`: TTS (Voice Studio), plan template, edit template, voice reference file.
- Episode 8 has the latest scripts. Copy them for a new episode and change only the episode-specific values.
  - `episodes/ep08/images/make_prompts_v1.py`, `cloud_review_v1.py`
  - `episodes/ep08/video/make_vprompts_v1.py`, `cloud_review_clips_v1.py`
  - `episodes/ep08/plan/plan_v2.py`
  - `episodes/ep08/review_edit/edit_v1.py` (review cut, plus the `--upload` mode)
  - `episodes/ep08/thumbnail/make_thumb_v3.py`
- Work order examples:
  - `episodes/ep08/WORK_ORDER_*.md`: TTS → images, Flow round 2, Muse v1–v3, edit, upload.
- Upload text examples: `episodes/ep07_bus/upload/`, `episodes/ep08/upload/`.
