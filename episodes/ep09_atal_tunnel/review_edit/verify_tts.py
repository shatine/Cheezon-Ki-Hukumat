"""Verify actual episode audio and export only JSON reports to the repository staging folder."""
import collections
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import soundfile as sf

sys.stdout.reconfigure(encoding="utf-8")

STAGE = Path(__file__).resolve().parent.parent
PC = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel\review_edit")
rows = [dict(zip(("id", "hi", "ko"), line.split("\t")))
        for line in (STAGE / "script" / "lines_hi_ko.tsv").read_text(encoding="utf-8").splitlines()]
lock = json.loads((STAGE / "script" / "script_lock.json").read_text(encoding="utf-8"))
source = json.loads((STAGE / "script" / "source_ko_sentences.json").read_text(encoding="utf-8"))
script = (STAGE / "script" / "script_ko_final.md").read_text(encoding="utf-8")
body = script.split("## 대본\n", 1)[1].split("## 근거표\n", 1)[0]
timing = json.loads((PC / "narr_timing.json").read_text(encoding="utf-8"))
checks = json.loads((PC / "narr_check.json").read_text(encoding="utf-8"))
full = sf.info(PC / "narration_hi.wav")
errors = []
if hashlib.sha256(body.encode("utf-8")).hexdigest() != lock["body_sha256"]:
    errors.append("locked Korean body changed")
if [r["id"] for r in rows] != [x["id"] for x in timing] or len(rows) != 78:
    errors.append("timing sentence ids/order/count differ")
if [r["id"] for r in rows] != [x["id"] for x in source]:
    errors.append("Hindi ids/order differ from the locked Korean sentences")
if set(checks) != {r["id"] for r in rows}:
    errors.append("check ids differ")
frames = 0
durations = []
methods = collections.Counter()
for i, row in enumerate(rows):
    lid = row["id"]
    info = sf.info(PC / "narr" / f"{lid}.wav")
    duration = info.frames / info.samplerate
    durations.append({"id": lid, "duration_sec": round(duration, 3),
                      "seconds_per_character": duration / len(row["hi"])})
    if info.samplerate != 24000 or info.channels != 1 or info.frames <= 0:
        errors.append(f"{lid}: invalid audio format or zero duration")
    if abs((timing[i]["end"] - timing[i]["start"]) - duration) > 0.0011:
        errors.append(f"{lid}: duration differs from actual WAV")
    if timing[i]["hi"] != row["hi"] or timing[i]["ko"] != row["ko"] or checks[lid].get("hi") != row["hi"]:
        errors.append(f"{lid}: text differs")
    if not checks[lid]["sentences"] or not all(s["pass"] for s in checks[lid]["sentences"]):
        errors.append(f"{lid}: failed strict speech check")
    for entry in checks[lid]["sentences"]:
        methods[entry["method"]] += 1
        if "seed11" in entry["method"] or "seed23" in entry["method"]:
            errors.append(f"{lid}: forbidden seed")
    if i:
        gap = 0.8 if lid[:3] != rows[i-1]["id"][:3] else 0.35
        if abs(timing[i]["start"] - timing[i-1]["end"] - gap) > 0.0011:
            errors.append(f"{lid}: incorrect pause gap")
        frames += int(24000 * gap)
    frames += info.frames
if frames != full.frames or full.samplerate != 24000 or full.channels != 1:
    errors.append("assembled audio frame count or format differs")
if abs(timing[-1]["end"] - full.frames / full.samplerate) > 0.001:
    errors.append("final timing does not match audio duration")

cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(PC / "narration_hi.wav"),
       "-filter_complex", "ebur128=peak=true", "-f", "null", "-"]
meter = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", check=True).stderr
integrated = re.findall(r"Integrated loudness:\s*I:\s*(-?[\d.]+) LUFS", meter)
peaks = re.findall(r"True peak:\s*Peak:\s*(-?[\d.]+) dBFS", meter)
if not integrated or not peaks:
    errors.append("loudness meter result unavailable")
report = {
    "checked_date": "2026-10-27", "timezone": "Asia/Seoul",
    "result": "automatic_checks_passed" if not errors else "automatic_checks_failed",
    "scope": "Measured WAV/timing integrity and saved strict ASR checks; listening review not performed",
    "sentence_count": len(rows), "paragraph_count": len({r['id'][:3] for r in rows}),
    "narration_seconds": round(full.frames / full.samplerate, 3),
    "sample_rate_hz": full.samplerate, "channels": full.channels,
    "integrated_lufs": float(integrated[-1]) if integrated else None,
    "true_peak_dbtp": float(peaks[-1]) if peaks else None,
    "strict_check_pass_count": sum(all(s['pass'] for s in v['sentences']) for v in checks.values()),
    "failed_ids": [lid for lid,v in checks.items() if not all(s['pass'] for s in v['sentences'])],
    "generation_methods": dict(methods),
    "korean_body_sha256": lock["body_sha256"],
    "narration_wav_sha256": hashlib.sha256((PC / "narration_hi.wav").read_bytes()).hexdigest(),
    "audio_folder": str(PC), "audio_committed_to_git": False,
    "errors": errors,
}
(PC / "tts_validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
for filename in ("narr_timing.json", "narr_check.json", "tts_validation.json"):
    shutil.copy2(PC / filename, STAGE / "review_edit" / filename)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(PC / "narration_hi.wav"),
                "-codec:a", "libmp3lame", "-b:a", "128k", str(PC / "narration_hi_preview.mp3")], check=True)
