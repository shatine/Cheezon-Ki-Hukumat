"""720p 편집본. clips/<장면>.mp4 를 plan.json 장면 길이에 맞추고 나레이션·자막·모션그래픽을 입힌다.
- 클립이 짧으면 느리게, 길면 자른다. 소리가 없는 클립(Veo 무음)은 빈 소리를 붙인다.
- 클립이 없는 장면은 first/<장면>.png 첫 그림을 천천히 확대하는 영상으로 채운다(재생성 대신).
- 나레이션 없는 장면(silent_len)은 영상과 현장음만.
- 모션그래픽: scenes.json "mg" = [["장면", 문장번호, "글자"], ...] 문장이 시작될 때 떠서 끝날 때까지.
결과: <slug>_<에피소드>_720p.mp4, <slug>_<에피소드>.srt  (-14 LUFS)"""
import json, os, subprocess
from kit import HERE, CH, NAME, LEAD, GAP, load, dur, run

CL = HERE / "clips"
WORK = HERE / "work"; WORK.mkdir(exist_ok=True)
BG_VOL, SILENT_BG = 0.22, 0.45
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
meta = load("tts_meta.json", {})
plan = load("plan.json")
MG = load("scenes.json").get("mg", [])
SUB_FONT = CH.get("subtitle_font", "Segoe UI Semibold")
MG_FONT = CH.get("mg_font", "Georgia")
MG_COLOUR = CH.get("mg_ass_colour", "&H0048C8F0")  # ASS BGR, 기본 금색


def has_audio(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def ts_ass(s):
    return f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"


def ts_srt(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def wrap(t, width=46):
    if len(t) <= width or " " not in t:
        return t
    mid = len(t) / 2
    i = min((i for i, c in enumerate(t) if c == " "), key=lambda s: abs(s - mid))
    return t[:i] + "\\N" + t[i + 1:]


def chunks(a, b, text, maxw=6):
    """자막을 한 줄 최대 maxw단어 조각으로 나눈다(문장부호 뒤 우선). 시각은 글자 수 비율로 나눈다."""
    words = text.replace('"', "").split()
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        if len(cur) >= maxw or (len(cur) >= 3 and w[-1] in ",.?!।") or i == len(words) - 1:
            out.append(" ".join(cur)); cur = []
    total = sum(len(s) for s in out) or 1
    res, t = [], a
    for s in out:
        d = (b - a) * len(s) / total
        res.append((t, t + d, s)); t += d
    return res


def fit(sid, need, vol):
    out = WORK / f"{sid}_fit.mp4"
    src = CL / f"{sid}.mp4"
    if not src.exists():  # 영상이 없으면 첫 그림 줌인
        n = int(need * 24) + 1
        run(["ffmpeg", "-y", "-loop", "1", "-i", str(HERE / "first" / f"{sid}.png"), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
             "-filter_complex", f"[0:v]scale=2560:-2,zoompan=z='min(1+0.0018*on,1.3)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
             f"d={n}:s=1280x720:fps=24,setsar=1[v]",
             "-map", "[v]", "-map", "1:a", "-t", f"{need:.3f}", *ENC, str(out)])
        return out, 0.0
    f = need / dur(src)
    v = "fps=24" if f <= 1.0 else f"setpts={f:.4f}*PTS,fps=24"
    if has_audio(src):
        a = "anull" if f <= 1.0 else f"atempo={max(0.5, 1 / f):.4f}"
        run(["ffmpeg", "-y", "-i", str(src), "-filter_complex",
             f"[0:v]{v},scale=1280:720,setsar=1[v];[0:a]{a},aresample=48000,volume={vol}[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{need:.3f}", *ENC, str(out)])
    else:
        run(["ffmpeg", "-y", "-i", str(src), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex",
             f"[0:v]{v},scale=1280:720,setsar=1[v]", "-map", "[v]", "-map", "1:a", "-t", f"{need:.3f}", *ENC, str(out)])
    return out, f


cues, mgs, parts, t0 = [], [], [], 0.0
for p in plan:
    sid, D = p["id"], p["len"]
    items = meta.get(sid, [])
    clip, f = fit(sid, D, BG_VOL if items else SILENT_BG)
    out = WORK / f"{sid}.mp4"
    if items:
        inputs, chain, t = [], [], LEAD
        for k, x in enumerate(items):
            inputs += ["-i", str(HERE / "tts" / x["wav"])]
            chain.append(f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(t * 1000)}|{int(t * 1000)}[n{k}]")
            cues += chunks(t0 + t, t0 + t + x["dur"], x["text"])  # 한 줄 6단어 이하 조각
            for s, i, txt in MG:
                if s == sid and i == k:
                    mgs.append((t0 + t, t0 + t + x["dur"] + 0.4, txt))
            t += x["dur"] + GAP
        run(["ffmpeg", "-y", "-i", str(clip), *inputs, "-filter_complex",
             ";".join(chain) + ";[0:a]" + "".join(f"[n{k}]" for k in range(len(items))) +
             f"amix=inputs={len(items) + 1}:normalize=0,atrim=0:{D:.3f}[a]",
             "-map", "0:v", "-map", "[a]", "-t", f"{D:.3f}", *ENC, str(out)])
    else:
        out = clip
    parts.append(out)
    print(f"{sid} {D:.1f}s x{f:.2f}", flush=True)
    t0 += D

(WORK / "list.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
joined = WORK / "joined.mp4"
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"), "-c", "copy", str(joined)])

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{SUB_FONT},38,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,0,0,0,0,100,100,0,0,1,2.4,1,2,70,70,40,1
Style: MG,{MG_FONT},76,{MG_COLOUR},{MG_COLOUR},&H00102040,&H64000000,1,0,0,0,100,100,1,0,1,4,3,8,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = "".join(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},Default,,0,0,0,,{t}\n" for a, b, t in cues)
ev += "".join(f"Dialogue: 1,{ts_ass(a)},{ts_ass(b)},MG,,0,0,0,,{{\\fad(250,300)\\fscx80\\fscy80\\t(0,300,\\fscx100\\fscy100)}}{t}\n"
              for a, b, t in mgs)
(WORK / "subs.ass").write_text(head + ev, encoding="utf-8")
(HERE / f"{NAME}.srt").write_text("".join(
    f"{i}\n{ts_srt(a)} --> {ts_srt(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues, 1)), encoding="utf-8")

final = HERE / f"{NAME}_720p.mp4"
os.chdir(WORK)
run(["ffmpeg", "-y", "-i", str(joined), "-vf", "ass=subs.ass:fontsdir=C\\\\:/Windows/Fonts",
     "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
     "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
     "-movflags", "+faststart", str(final)])
print("TOTAL", f"{t0:.1f}s", final)
