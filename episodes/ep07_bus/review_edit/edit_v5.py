"""EP7 v5 힌디 검수영상: narration_hi.wav + narr_timing.json + clips_v5 → out/v5_review_hi.mp4 (1920x1080, 30fps, 나레이션만).
- 문단별 클립 배정(PLAN), 쓸 구간(USE). 컷 2~3초(오프닝 S01·S02 1~1.5초). 문단 안에서 클립을 번갈아, 각 클립의 다음 안 쓴 연속 구간.
- 영상이 모자라면 문단 전체를 느리게(최저 0.6배). 그래도 모자라면 마지막 컷을 계속 재생(끝나면 마지막 프레임 유지) + 왼쪽 위 빨간 '영상 부족 N초'.
- 자막: 힌디(Nirmala UI 흰색+검은 테두리) 위, 한국어 직역(맑은 고딕 노랑, 작게) 아래. 한 줄 고정: 힌디는 넘치면 쉼표에서 나눔, 한국어는 글자 크기 축소.
- 결과: out/v5_review_hi.mp4, review_v5/subs_hi.srt, subs_ko.srt, subs.ass, cuts.json, edit_report.json"""
import json, re, subprocess, shutil, sys, tempfile, statistics
from pathlib import Path
import numpy as np, soundfile as sf
from PIL import ImageFont
HERE = Path(__file__).resolve().parent
BUS = HERE.parent; CL = BUS / "clips_v5"; OUT = BUS / "out"; SEG = OUT / "v5_hi_seg"; SEG.mkdir(parents=True, exist_ok=True)
FPS, W, H = 30, 1920, 1080
PLAN = {"S01": ["h1", "h2"], "S02g": ["h3", "h4"], "S02m": ["m1", "m2", "m3s", "m4", "m5"], "S03": ["PB", "s03"],
        "S04": ["s04a", "s04b", "s01", "s04c", "M3"], "S05": ["s05", "s02"], "S06": ["s06a", "s06b"], "S07": ["s07a", "s07b"],
        "S08": ["s08"], "S09": ["s09"], "S10": ["s10"], "S11": ["s11a", "s11b"], "S12": ["s12"], "S13": ["s13"], "S14": ["s14a", "s14b"],
        "S15": ["s15a", "s15b"], "S16": ["s16a"], "S17": ["s16b", "s17a", "s17b"], "S18": ["s18"], "S19": ["s19"], "S20": ["s20"],
        "S21": ["s21a", "s21b"], "S22": ["s22"], "S23": ["s23"], "S24": ["s24"], "S25": ["s25"], "S26": ["s26"], "S27": ["s27"], "S28": ["s28"]}
USE = {"PB": [(0, 7)], "s03": [(0, 6)], "s10": [(0, 7)], "s14a": [(3, 10)], "s14b": [(3, 10)], "s15a": [(0, 2), (5, 10)], "s15b": [(0, 7)], "s28": [(4, 10)]}
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
CLD = {k: dur(CL / f"{k}.mp4") for v in PLAN.values() for k in v}
def ranges(k): return [(a, min(b, CLD[k] - 0.05)) for a, b in USE.get(k, [(0, 10)])]

T = json.load(open(HERE / "narr_timing.json", encoding="utf-8"))
SR = 24000; AUD = sf.read(HERE / "narration_hi.wav", dtype="float32")[0]; ATOT = len(AUD) / SR
VTOT = round((ATOT + 1.0) * FPS) / FPS          # 나레이션 끝 + 1초
# 문단 경계: 각 문단 첫 줄 시작 (첫 문단은 0)
paras = []
for x in T:
    p = x["id"][:3]
    if not paras or paras[-1][0] != p: paras.append([p, x["start"]])
paras[0][1] = 0.0
# S02 안의 'एक महीने में' 시각 → 화려함/비참 경계
s02a = next(x for x in T if x["id"] == "S02a")
def silences(a, thr=-40, mn=0.10):
    hop = int(SR * 0.01); n = len(a) // hop
    db = 20 * np.log10(np.sqrt([np.mean(a[i*hop:(i+1)*hop] ** 2) + 1e-12 for i in range(n)]))
    out, i = [], 0
    while i < n:
        if db[i] < thr:
            j = i
            while j < n and db[j] < thr: j += 1
            if (j - i) * 0.01 >= mn and i > 0 and j < n: out.append((i + j) / 2 * 0.01)
            i = j
        else: i += 1
    return out
def boundary_times(lid, text, cuts_chars):
    """줄 wav 안에서 글자 위치(cuts_chars)에 해당하는 시각: 가장 가까운 쉼(무음) 중심, 없으면 글자 비례"""
    a = sf.read(HERE / "narr" / f"{lid}.wav", dtype="float32")[0]; d = len(a) / SR
    sil = silences(a); used = set(); res = []
    for c in cuts_chars:
        e = d * c / len(text)
        cand = [s for s in sil if abs(s - e) < 1.2 and s not in used]
        s = min(cand, key=lambda s: abs(s - e)) if cand else e
        used.add(s); res.append(s)
    return res
mahine = s02a["start"] + boundary_times("S02a", s02a["hi"], [s02a["hi"].index(", एक महीने") + 1])[0]
segs = []   # (이름, 시작, 끝)
for i, (p, st) in enumerate(paras):
    en = paras[i + 1][1] if i + 1 < len(paras) else VTOT
    if p == "S02": segs += [("S02g", st, mahine), ("S02m", mahine, en)]
    else: segs.append((p, st, en))

# ---- 컷 배정 ----
def fr(t): return int(round(t * FPS))
cuts, report = [], {"short": [], "slow": []}
for name, st, en in segs:
    clips = PLAN[name]; P = en - st
    opening = name in ("S01", "S02g", "S02m")
    base = 1.25 if opening else 2.5
    total = sum(b - a for k in clips for a, b in ranges(k))
    f = 1.0 if total >= P else max(0.6, total / P)
    n = max(1, round(P / base)); n = max(n, min(len(clips), int(P / (0.9 if opening else 1.8))))   # 클립이 여러 개면 가능한 한 다 보이게
    def alloc(f):
        cur = {k: [list(r) for r in ranges(k)] for k in clips}         # 남은 쓸 구간
        f0, f1 = fr(st), fr(en); bounds = [f0 + round((f1 - f0) * j / n) for j in range(n + 1)]
        seq, ci = [], 0
        for j in range(n):
            need = (bounds[j + 1] - bounds[j]) / FPS
            src = need * f; k = None
            for _ in range(len(clips)):                                   # 다음 클립 중 이 컷 길이만큼 연속 구간이 남은 것
                kk = clips[ci % len(clips)]; ci += 1
                fit = [r for r in cur[kk] if r[1] - r[0] >= src - 1e-6]
                if fit:
                    while cur[kk][0] is not fit[0]: cur[kk].pop(0)       # 짧은 남은 조각은 버리고 다음 구간으로
                    k = kk; break
            if k is None:   # 다 모자라면 가장 긴 남은 조각
                left = [(r[1] - r[0], kk) for kk in clips for r in cur[kk][:1]]
                if not left:   # 모든 클립 소진 → 직전 컷을 계속 재생
                    seq[-1]["f1"] = bounds[j + 1]; continue
                k = max(left)[1]
            a, b = cur[k][0]
            if b - a >= src - 1e-6:
                cur[k][0][0] = a + src
                if b - (a + src) < 0.05: cur[k].pop(0)
            else:                       # 이 구간 남은 길이만큼만 쓰고 모자란 몫은 이 컷이 계속 재생(over)
                cur[k].pop(0)
            seq.append({"para": name, "clip": k, "f0": bounds[j], "f1": bounds[j + 1], "ss": round(a, 3), "speed": f, "use_end": b})
        # 같은 클립 연속 컷 합치기(점프컷 방지)
        merged = []
        for c in seq:
            if merged and merged[-1]["clip"] == c["clip"] and abs(merged[-1]["ss"] + (merged[-1]["f1"] - merged[-1]["f0"]) / FPS * f - c["ss"]) < 0.05:
                merged[-1]["f1"] = c["f1"]; merged[-1]["use_end"] = c["use_end"]
            else: merged.append(c)
        for c in merged:
            d = (c["f1"] - c["f0"]) / FPS; avail = (c["use_end"] - c["ss"]) / c["speed"]
            c["short_from"] = round(avail, 3) if avail < d - 0.25 else None
        return merged
    while True:   # 남은 조각 손실로 조금 모자라면 조금 더 느리게(최저 0.6배)
        merged = alloc(f)
        if f <= 0.6 or not any(c["short_from"] is not None for c in merged): break
        f = max(0.6, f - 0.02)
    if f < 1: report["slow"].append({"para": name, "speed": round(f, 2), "need": round(P, 2), "have": round(total, 2)})
    for c in merged:
        if c["short_from"] is not None:
            d = (c["f1"] - c["f0"]) / FPS
            report["short"].append({"para": name, "clip": c["clip"], "sec": round(d - c["short_from"], 2), "at": round(c["f0"] / FPS + c["short_from"], 2)})
    cuts += merged

# ---- 컷 렌더 ----
FONT = "C\\:/Windows/Fonts/malgunbd.ttf"
lst = []
for i, c in enumerate(cuts):
    d = (c["f1"] - c["f0"]) / FPS; f = c["speed"]; seg = SEG / f"{i:03d}.mp4"; c["file"] = seg.name; c["dur"] = round(d, 3)
    vf = (f"trim=start={c['ss']},setpts=(PTS-STARTPTS)/{f},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,"
          f"tpad=stop_mode=clone:stop_duration={d + 1}")
    if c["short_from"] is not None:
        n = round(d - c["short_from"])
        vf += (f",drawtext=fontfile='{FONT}':text='영상 부족 {max(n,1)}초':x=24:y=24:fontsize=40:fontcolor=white:box=1:boxcolor=red@0.85:boxborderw=10"
               f":enable='gte(t,{c['short_from']})'")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(CL / f"{c['clip']}.mp4"), "-vf", vf, "-frames:v", str(c["f1"] - c["f0"]), "-an",
                        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", str(FPS), str(seg)], capture_output=True, text=True)
    if r.returncode: print(c, r.stderr[-600:]); sys.exit(1)
    lst.append(f"file '{seg.as_posix()}'")
    print(i, c["para"], c["clip"], c["ss"], d, round(f, 2), "SHORT" if c["short_from"] is not None else "", flush=True)
(SEG / "list.txt").write_text("\n".join(lst), encoding="utf-8")

# ---- 자막 ----
HFS, KFS, MAXW = 58, 44, 1800
hfont = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", HFS, index=0)
kfont = lambda s: ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", s)
def wid(font, s): return font.getlength(s) * 1.06 + 8   # 테두리 여유
def clean(s): return re.sub(r"[।,.\s]+$", "", s.strip())
def split_fit(s):
    if wid(hfont, s) <= MAXW: return [s]
    parts = [p for p in re.split(r"(?<=[,।])\s+", s) if p]
    if len(parts) > 1:   # 쉼표 단위로 욕심껏 합치기
        out = [parts[0]]
        for p in parts[1:]:
            if wid(hfont, out[-1] + " " + p) <= MAXW: out[-1] += " " + p
            else: out.append(p)
        return [y for x in out for y in split_fit(x)]
    w = s.split(); m = min(range(1, len(w)), key=lambda i: abs(len(" ".join(w[:i])) - len(s) / 2))
    return split_fit(" ".join(w[:m])) + split_fit(" ".join(w[m:]))
def ts_srt(t): t = max(0, t); return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(round(t*1000))%1000:03d}"
def ts_ass(t): t = max(0, t); cs = int(round(t * 100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"
hi_ev, ko_ev = [], []
for i, x in enumerate(T):
    nxt = T[i + 1]["start"] if i + 1 < len(T) else VTOT
    end = min(nxt, x["end"] + 0.4)
    ko_ev.append((x["start"], end, x["ko"]))
    chunks = split_fit(x["hi"])
    if len(chunks) == 1: hi_ev.append((x["start"], end, clean(chunks[0]))); continue
    pos, cc = 0, []
    for ch in chunks[:-1]: pos = x["hi"].index(ch, pos) + len(ch); cc.append(pos)
    bt = [x["start"] + b for b in boundary_times(x["id"], x["hi"], cc)]
    edges = [x["start"]] + bt + [end]
    for k, ch in enumerate(chunks): hi_ev.append((edges[k], edges[k + 1], clean(ch)))
with open(HERE / "subs_hi.srt", "w", encoding="utf-8") as f:
    for n, (a, b, s) in enumerate(hi_ev, 1): f.write(f"{n}\n{ts_srt(a)} --> {ts_srt(b)}\n{s}\n\n")
with open(HERE / "subs_ko.srt", "w", encoding="utf-8") as f:
    for n, (a, b, s) in enumerate(ko_ev, 1): f.write(f"{n}\n{ts_srt(a)} --> {ts_srt(b)}\n{s}\n\n")
ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       f"Style: HI,Nirmala UI,{HFS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,1,2,40,40,104,1",
       f"Style: KO,Malgun Gothic,{KFS},&H0000E6FF,&H0000E6FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,1,2,40,40,40,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
shrunk = []
for a, b, s in hi_ev: ass.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},HI,,0,0,0,,{s}")
for a, b, s in ko_ev:
    fs = KFS
    while wid(kfont(fs), s) > MAXW and fs > 24: fs -= 1
    if fs < KFS: shrunk.append((s, fs))
    ass.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},KO,,0,0,0,,{{\\fs{fs}}}{s}" if fs < KFS else f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},KO,,0,0,0,,{s}")
(HERE / "subs.ass").write_text("\n".join(ass) + "\n", encoding="utf-8-sig")

# ---- 최종: 이어붙이기 + 자막 굽기 + 나레이션 ----
tmp = Path(tempfile.mkdtemp(prefix="v5hi_")); shutil.copy(HERE / "subs.ass", tmp / "subs.ass")
final = OUT / "v5_review_hi.mp4"
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(SEG / "list.txt"), "-i", str(HERE / "narration_hi.wav"),
                    "-vf", "ass=subs.ass", "-af", "apad,aresample=48000", "-ac", "2", "-t", f"{VTOT:.3f}",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(final)], cwd=tmp, capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
L = [c["dur"] for c in cuts]
report.update({"total_sec": round(dur(final), 2), "narration_sec": round(ATOT, 2), "cuts": len(cuts), "median_cut": round(statistics.median(L), 2),
               "max_cut": max(L), "min_cut": min(L), "max_cut_at": cuts[L.index(max(L))]["para"] + " " + cuts[L.index(max(L))]["clip"],
               "s02_misery_from": round(mahine, 2), "hi_subs": len(hi_ev), "ko_subs": len(ko_ev), "ko_shrunk": shrunk})
json.dump(cuts, open(HERE / "cuts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(report, open(HERE / "edit_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False, indent=1))
