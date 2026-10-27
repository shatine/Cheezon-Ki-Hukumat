"""ep09 편집 준비 초안: 읽기 전용 미디어 preflight와 문장 실측 검토 자막만 만든다.

전체 렌더러가 아니다. production render/Muse/upload/BGM 명령은 구현하지 않았다.
python edit_v1.py --check-only --make-review-subtitles
python edit_v1.py --subtitles-only

기본 PC 미디어는 CB 환경변수 또는 --media-root로 지정한다. 자막의 새 시각은 만들지
않으며 78문장 실측 start/end를 그대로 쓴다. 줄바꿈은 같은 cue 안에서만 한다.
자막 단독 준비는 exit 0, 입력 오류는 exit 1, 미디어/실측USE 부족은 exit 2다.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys

from PIL import ImageFont, features

EP = Path(__file__).resolve().parent.parent
FPS, W, H, EXPECTED_CUTS, EXPECTED_FRAMES = 30, 1920, 1080, 79, 14112
BODY_SHA = "b6f91f4fcf8a86d100157ee3e1bdb51f4c392780625716b845d7075333eb34c6"
MAX_WIDTH = 1740


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition, message, errors):
    if not condition:
        errors.append(message)


def core_inputs(ep):
    timing = read_json(ep / "review_edit/narr_timing.json")
    plan = read_json(ep / "plan/shot_list_v1.json")
    overlays = read_json(ep / "plan/overlays_v1.json")["overlays"]
    source = read_json(ep / "script/source_ko_sentences.json")
    with (ep / "script/lines_hi_ko.tsv").open(encoding="utf-8-sig", newline="") as handle:
        lines = list(csv.reader(handle, delimiter="\t"))
    errors = []
    body = (ep / "script/script_ko_final.md").read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("## 대본\n", 1)[1].split("## 근거표\n", 1)[0]
    check(hashlib.sha256(body.encode("utf-8")).hexdigest() == BODY_SHA, "Approved Korean body hash mismatch", errors)
    ids = [x["id"] for x in timing]
    check(len(timing) == 78 and ids == [x["id"] for x in source], "Measured sentence IDs/count/order mismatch", errors)
    check(len(lines) == 78 and all(len(x) == 3 for x in lines), "HI/KO sentence table schema mismatch", errors)
    if not errors:
        check(all([x["id"], x["hi"], x["ko"]] == y for x, y in zip(timing, lines)), "Measured text differs from approved translation table", errors)
    prev = 0.0
    for row in timing:
        a, b = row["start"], row["end"]
        check(math.isfinite(a) and math.isfinite(b) and 0 <= a < b and a >= prev - 1e-6, f"Invalid measured interval: {row['id']}", errors)
        prev = b
    cuts = plan["cuts"]
    check(plan.get("fps") == FPS and len(cuts) == EXPECTED_CUTS, "Expected 79 cuts at 30fps", errors)
    previous, names, used_ranges = 0, set(), {}
    for cut in cuts:
        f0, f1 = cut["out_f0"], cut["out_f1"]
        check(isinstance(f0, int) and isinstance(f1, int) and f0 == previous and f1 > f0, f"Cut frame gap/overlap/nonpositive: {cut['src']}", errors)
        check(abs(cut["start"] - f0 / FPS) < 1e-5 and abs(cut["end"] - f1 / FPS) < 1e-5 and abs(cut["dur"] - (f1 - f0) / FPS) < 1e-5, f"Cut second/frame mismatch: {cut['src']}", errors)
        check(cut["src"].casefold() not in names, f"Source ID reused/case-clashed: {cut['src']}", errors)
        names.add(cut["src"].casefold())
        if cut["kind"] == "v":
            a, b = cut["src_start"], cut["src_end"]
            check(0 <= a < b and abs(b - a - (f1 - f0) / FPS) < 1e-5, f"Video normal-speed source range mismatch: {cut['src']}", errors)
            for old_a, old_b in used_ranges.get(cut["src"], []):
                check(not (a < old_b and b > old_a), f"Video source range overlap: {cut['src']}", errors)
            used_ranges.setdefault(cut["src"], []).append((a, b))
        else:
            check(cut["kind"] == "i" and f1 - f0 <= round(4.5 * FPS), f"Image kind/maximum duration error: {cut['src']}", errors)
        previous = f1
    check(previous == EXPECTED_FRAMES and sum(c["out_f1"] - c["out_f0"] for c in cuts) == EXPECTED_FRAMES, "Expected exactly 14,112 contiguous output frames", errors)
    check(abs(previous / FPS - (timing[-1]["end"] + 1)) <= 1 / (2 * FPS) + 1e-6, "Video length differs from measured narration plus one-second tail", errors)
    by_id = {x["id"]: x for x in timing}
    for label in overlays:
        row = by_id.get(label["source_sentence_id"])
        check(row is not None and abs(label["start"] - row["start"]) < 1e-6 and abs(label["end"] - row["end"]) < 1e-6, f"Overlay not tied to measured sentence: {label['id']}", errors)
    return timing, plan, overlays, errors


def timecode(seconds, scale, separator):
    units = round(seconds * scale)
    total_s, frac = divmod(units, scale)
    hours, remain = divmod(total_s, 3600)
    mins, secs = divmod(remain, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}{separator}{frac:0{3 if scale == 1000 else 2}d}"


def review_subtitles(ep, timing, overlays, write):
    hf = Path(os.environ.get("HI_FONT", r"C:\Windows\Fonts\Nirmala.ttc"))
    kf = Path(os.environ.get("KO_FONT", r"C:\Windows\Fonts\malgunbd.ttf"))
    hfont = ImageFont.truetype(str(hf), 58, index=0)
    kfont = ImageFont.truetype(str(kf), 44)
    lfont = ImageFont.truetype(str(hf), 42, index=0)
    def wrap(text, font):
        out = []
        for paragraph in text.splitlines():
            current = ""
            for word in paragraph.split():
                candidate = (current + " " + word).strip()
                if current and font.getlength(candidate) * 1.08 + 12 > MAX_WIDTH:
                    out.append(current)
                    current = word
                else:
                    current = candidate
            if current:
                out.append(current)
        if not out or any(font.getlength(x) * 1.08 + 12 > MAX_WIDTH for x in out):
            raise ValueError("A subtitle token cannot fit; no text or time is truncated")
        if " ".join(out).split() != text.split():
            raise ValueError("Subtitle wrapping changed visible source text")
        return out
    hi_srt, ko_srt = [], []
    ass = ["[Script Info]", "Title: ep09 sentence-timed HI+KO review only; not upload subtitles", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: HI,Nirmala UI,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,1,2,80,80,180,1",
           "Style: KO,Malgun Gothic,44,&H0000E6FF,&H0000E6FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,1,2,80,80,72,1",
           "Style: INFO,Nirmala UI,42,&H0033FF33,&H0033FF33,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,3,2,0,7,90,90,90,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    layout = []
    for number, row in enumerate(timing, 1):
        hlines, klines = wrap(row["hi"], hfont), wrap(row["ko"], kfont)
        a, b = timecode(row["start"], 1000, ","), timecode(row["end"], 1000, ",")
        hi_srt.append(f"{number}\n{a} --> {b}\n" + "\n".join(hlines) + "\n")
        ko_srt.append(f"{number}\n{a} --> {b}\n" + "\n".join(klines) + "\n")
        st, en = timecode(row["start"], 100, "."), timecode(row["end"], 100, ".")
        hbottom = H - 72 - len(klines) * 58 - 22
        for style, text, y in (("HI", "\\N".join(hlines), hbottom), ("KO", "\\N".join(klines), H - 72)):
            ass.append(f"Dialogue: 0,{st},{en},{style},{row['id']},0,0,0,,{{\\an2\\pos(960,{y})\\q2}}{text}")
        layout.append(dict(id=row["id"], measured_start=row["start"], measured_end=row["end"], hi_lines=len(hlines), ko_lines=len(klines)))
    for label in overlays:
        text = "\\N".join(wrap(label["text_hi"], lfont))
        ass.append(f"Dialogue: 1,{timecode(label['start'],100,'.')},{timecode(label['end'],100,'.')},INFO,{label['id']},0,0,0,,{{\\an7\\pos(90,90)\\q2}}{text}")
    outputs = {"subs_hi_review_v1.srt": "\n".join(hi_srt), "subs_ko_review_v1.srt": "\n".join(ko_srt), "subs_review_v1.ass": "\n".join(ass) + "\n"}
    if write:
        for name, content in outputs.items():
            (ep / "review_edit" / name).write_text(content, encoding="utf-8")
    return dict(status="sentence_timed_review_text_prepared" if write else "sentence_timed_review_text_checked_only", files_written=list(outputs) if write else [],
                hi_cues=len(timing), ko_cues=len(timing), measured_label_cues=len(overlays),
                timing_basis="actual sentence start/end only; wrap within one cue; no character-time estimate or inserted split point",
                srt_rounding_max_sec=0.0005, ass_rounding_max_sec=0.005, ass_spacing=0,
                hi_font=str(hf), ko_font=str(kf), pillow_raqm=features.check("raqm"),
                width_measurement="Pillow font metrics with safety margin; actual libass shaping/layout NOT visually reviewed",
                actual_subtitle_render_or_visual_review_performed=False,
                upload_one_line_subtitles="withheld; exact pause/word alignment required before splitting timed text",
                max_hi_lines=max(x["hi_lines"] for x in layout), max_ko_lines=max(x["ko_lines"] for x in layout), sentence_layout=layout)


def probe(path, executable):
    result = subprocess.run([executable, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)


def media_preflight(ep, media, plan, timing, clip_review_path):
    ffprobe = shutil.which("ffprobe")
    picks_path = ep / "images/picks_v1.json"
    picks = read_json(picks_path).get("picks", {}) if picks_path.exists() else {}
    image_defs = {x["id"]: x for x in read_json(ep / "images/prompts_v1.json")}
    clip_reviews = read_json(clip_review_path).get("clips", {}) if clip_review_path.exists() else {}
    entries, blockers = [], []
    for cut in plan["cuts"]:
        sid, issues = cut["src"], []
        entry = dict(id=sid, kind=cut["kind"], planned_file=cut["file"], actual_file=None, issues=issues)
        if cut["kind"] == "i":
            pick = picks.get(sid)
            if not pick:
                issues.append("no_actual_chosen_image_pick")
            else:
                name = pick.get("file")
                if not isinstance(name, str) or Path(name).name != name or image_defs.get(sid, {}).get("kind") != "image":
                    issues.append("invalid_static_image_pick_or_kind")
                else:
                    path = media / "img" / name
                    entry.update(actual_file=str(path), actual_pick_attempt=pick.get("attempt"))
                    if not path.is_file():
                        issues.append("actual_picked_image_file_missing")
                    else:
                        header = path.read_bytes()[:24]
                        clean_reviewed = pick.get("root_opened_clean_original") is True or pick.get("raw_and_cleaned_opened_at_original_size") is True
                        if not str(pick.get("visual_status", "")).startswith("chosen_") or not clean_reviewed:
                            issues.append("image_explicit_clean_original_review_missing")
                        if sha(path) != pick.get("sha256"):
                            issues.append("image_pick_ledger_sha_mismatch")
                        if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or list(struct.unpack(">II", header[16:24])) != pick.get("dimensions"):
                            issues.append("image_png_dimensions_or_format_mismatch")
        else:
            path = media / cut["file"]
            entry["actual_file"] = str(path)
            if not path.is_file():
                issues.append("video_source_missing")
            elif not ffprobe:
                issues.append("ffprobe_unavailable")
            else:
                try:
                    info = probe(path, ffprobe)
                    stream = next(x for x in info["streams"] if x.get("codec_type") == "video")
                    rate = float(Fraction(stream.get("avg_frame_rate", "0/1")))
                    duration = float(stream["duration"])
                    if not math.isfinite(duration) or duration <= 0 or not math.isfinite(rate) or rate <= 0:
                        raise ValueError("invalid measured video duration/fps")
                    actual_sha = sha(path)
                    entry.update(actual_duration=duration, actual_fps=rate, actual_width=stream.get("width"), actual_height=stream.get("height"), actual_sha256=actual_sha)
                    if cut["src_end"] > duration - 0.05 + 1e-6:
                        issues.append("planned_use_exceeds_actual_duration_minus_0.05")
                    review = clip_reviews.get(sid, {})
                    if review.get("status") != "confirmed" or review.get("visual_review_performed") is not True or review.get("sha256") != actual_sha or review.get("file") != cut["file"]:
                        issues.append("actual_clip_visual_review_or_exact_file_hash_missing")
                    ranges = review.get("usable_ranges", [])
                    entry["reviewed_usable_ranges"] = ranges if review else None
                    valid_ranges = (bool(ranges) and all(isinstance(r, list) and len(r) == 2 and all(isinstance(x, (int, float)) and math.isfinite(x) for x in r) and 0 <= r[0] < r[1] <= duration - 0.05 + 1e-6 for r in ranges))
                    if not valid_ranges:
                        issues.append("reviewed_USE_missing_or_exceeds_actual_duration_minus_0.05")
                    elif not any(a <= cut["src_start"] + 1e-6 and cut["src_end"] <= b + 1e-6 for a, b in ranges):
                        issues.append("planned_cut_outside_actual_reviewed_USE")
                except (KeyError, StopIteration, ValueError, ZeroDivisionError, subprocess.SubprocessError) as exc:
                    issues.append("ffprobe_or_actual_USE_measurement_error: " + str(exc))
        if issues:
            blockers.append(dict(id=sid, reasons=issues))
        entries.append(entry)
    audio = media / "review_edit/narration_hi.wav"
    audio_result = dict(file=str(audio), exists=audio.is_file(), measured_duration=None)
    if audio.is_file() and ffprobe:
        try:
            info = probe(audio, ffprobe)
            stream = next(x for x in info["streams"] if x.get("codec_type") == "audio")
            duration = float(stream.get("duration", info["format"]["duration"]))
            audio_result.update(measured_duration=duration, sample_rate=stream.get("sample_rate"), channels=stream.get("channels"))
            if abs(duration - timing[-1]["end"]) > 0.001:
                blockers.append(dict(id="narration", reasons=["measured_WAV_duration_differs_from_TTS_timing"]))
        except (ValueError, KeyError, StopIteration, subprocess.SubprocessError) as exc:
            blockers.append(dict(id="narration", reasons=[str(exc)]))
    else:
        blockers.append(dict(id="narration", reasons=["actual_audio_or_ffprobe_missing"]))
    return dict(ffprobe=ffprobe, media_entries=entries, blockers=blockers, checked_source_count=len(entries),
                unavailable_source_count=sum(any("missing" in issue or "no_actual_chosen" in issue for issue in x["issues"]) for x in entries),
                clip_review_manifest=str(clip_review_path), clip_review_manifest_exists=clip_review_path.exists(), narration=audio_result)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-only", action="store_true")
    mode.add_argument("--subtitles-only", action="store_true")
    parser.add_argument("--make-review-subtitles", action="store_true")
    parser.add_argument("--episode-root", type=Path, default=EP)
    parser.add_argument("--media-root", type=Path, default=Path(os.environ.get("CB", r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")))
    parser.add_argument("--clip-review", type=Path)
    args = parser.parse_args()
    ep = args.episode_root
    try:
        timing, plan, overlays, errors = core_inputs(ep)
        subtitles = review_subtitles(ep, timing, overlays, write=args.make_review_subtitles or args.subtitles_only) if not errors else None
        media = media_preflight(ep, args.media_root, plan, timing, args.clip_review or ep / "video/review_clips_v1.json") if args.check_only and not errors else None
        blockers = media["blockers"] if media else []
        report = dict(status="invalid_input" if errors else ("blocked_missing_or_unreviewed_media" if blockers else "draft_preparation_only"),
                      scope="check-only and measured sentence review subtitles; no renderer implemented",
                      render_ready=False, actual_render_performed=False, actual_video_visual_review_performed=False,
                      full_fake_render_test_performed=False, actual_muse_submission_performed=False,
                      upload_or_bgm_work_performed=False, core_errors=errors,
                      measured_narration_seconds=timing[-1]["end"], cut_count=len(plan["cuts"]), output_frames=plan["cuts"][-1]["out_f1"],
                      output_seconds=plan["cuts"][-1]["out_f1"] / FPS, target_width=W, target_height=H, target_fps=FPS,
                      review_subtitles=subtitles, media=media,
                      remaining_work=["actual media and confirmed measured USE", "full renderer implementation and isolated full-render test", "libass typography/layout review", "exact pause/word alignment for upload single-line subtitles", "0-to-end final visual/audio review"])
        (ep / "review_edit/edit_preflight_v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: report[k] for k in ("status", "scope", "render_ready", "core_errors", "measured_narration_seconds", "cut_count", "output_frames")}, ensure_ascii=False, indent=2))
        if media:
            print(f"Source blockers: {len(media['blockers'])}; unavailable source count: {media['unavailable_source_count']}")
        raise SystemExit(1 if errors else (2 if blockers else 0))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps(dict(status="preparation_stopped", reason=str(exc), render_ready=False), ensure_ascii=False, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
