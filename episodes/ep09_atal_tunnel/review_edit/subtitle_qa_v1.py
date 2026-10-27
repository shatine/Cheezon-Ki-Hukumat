"""Render exactly five subtitle QA PNGs with libass; no video/clip/audio output.

python subtitle_qa_v1.py
The only raster outputs are under the PC episode image_review_v1/subtitle_qa.
Approved subtitle text and measured start/end are read, never rewritten.
This checks static typesetting only, not video editing or whole-film review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


EP = Path(__file__).resolve().parent.parent
PC = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
SAMPLES = [
    ("S01b", "L01", "contractor attribution; 8,000 litres/minute"),
    ("S02b", "L02", "decimal length 9.02 and altitude above 3,000 metres"),
    ("S02c", "L03", "long HI three lines + KO two lines; BRO and upper excavation four years"),
    ("S20b", "L08", "opening date 3 October 2020"),
    ("S21b", "L09", "long HI three lines + KO two lines; 2024 historical article attribution"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode-root", type=Path, default=EP)
    parser.add_argument("--media-root", type=Path, default=PC)
    args = parser.parse_args()
    ep, media = args.episode_root.resolve(), args.media_root.resolve()
    ass = ep / "review_edit/subs_review_v1.ass"
    timing_path, labels_path = ep / "review_edit/narr_timing.json", ep / "plan/overlays_v1.json"
    timing = {x["id"]: x for x in read(timing_path)}
    labels = {x["id"]: x for x in read(labels_path)["overlays"]}
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise ValueError("ffmpeg is unavailable")
    frozen = {str(x): sha(x) for x in (ass, timing_path, labels_path)}
    output = media / "image_review_v1/subtitle_qa"
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for sentence_id, label_id, purpose in SAMPLES:
        sentence, label = timing[sentence_id], labels[label_id]
        if label["source_sentence_id"] != sentence_id:
            raise ValueError("Label/sentence relationship changed")
        # Millisecond midpoint lies strictly inside the actual measured cue.
        sample_ms = round((sentence["start"] + sentence["end"]) * 500)
        sample_seconds = sample_ms / 1000
        if not sentence["start"] < sample_seconds < sentence["end"]:
            raise ValueError("Measured cue has no usable midpoint")
        target = output / f"qa_{sentence_id}_{label_id}_{sample_ms:06d}ms.png"
        # A single color frame carries the actual timestamp into libass.
        # No .mp4, intermediate clip, audio or fake footage is generated.
        vf = f"settb=1/1000,setpts=PTS+{sample_ms},ass=filename={ass.name}"
        command = [ffmpeg, "-hide_banner", "-nostdin", "-loglevel", "verbose", "-y",
                   "-f", "lavfi", "-i", "color=c=0x202A36:s=1920x1080:r=1:d=1",
                   "-vf", vf, "-frames:v", "1", "-fps_mode", "passthrough",
                   "-update", "1", str(target)]
        result = subprocess.run(command, cwd=ass.parent, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=60)
        if result.returncode != 0 or not target.is_file():
            raise ValueError("Static PNG render failed: " + result.stderr[-4000:])
        font_lines = [x for x in result.stderr.splitlines() if "fontselect:" in x]
        glyph_errors = [x for x in result.stderr.splitlines()
                        if "glyph" in x.lower() and ("not found" in x.lower() or "failed" in x.lower())]
        if glyph_errors:
            raise ValueError("libass reports missing glyphs: " + "\n".join(glyph_errors))
        records.append(dict(sentence_id=sentence_id, label_id=label_id, purpose=purpose,
                            measured_sentence_start=sentence["start"], measured_sentence_end=sentence["end"],
                            requested_timestamp=sample_seconds, filter_timestamp_ms=sample_ms,
                            png=str(target), png_sha256=sha(target),
                            font_selection_log=font_lines, missing_glyph_errors=glyph_errors))
    if any(sha(Path(path)) != digest for path, digest in frozen.items()):
        raise ValueError("Read-only subtitle inputs changed while rendering QA")
    report = dict(status="five_static_libass_pngs_prepared_for_visual_review",
                  scope="static subtitle typesetting samples only", input_sha256=frozen,
                  raster_output_directory=str(output), ffmpeg=ffmpeg, frames=records,
                  static_png_count=len(records), png_width=1920, png_height=1080,
                  approved_text_or_timecodes_changed=False, video_or_clip_created=False,
                  audio_output_created=False, production_render_performed=False,
                  full_video_review_performed=False, root_original_png_review_performed=False,
                  missing_glyph_log_check="no missing-glyph errors; visual inspection still required")
    report_path = ep / "review_edit/subtitle_qa_v1.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
