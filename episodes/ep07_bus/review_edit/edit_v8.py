"""EP7 v8 힌디 검수영상: narration_hi.wav + narr_timing.json + plan/shot_list_v8.json → out/v8_review_hi.mp4 (1920x1080, 30fps, 나레이션만).
- 컷 배정은 plan/plan_v8.py가 만든 shot_list_v8.json을 그대로 따른다(문장별 배정·연속 소스 구간·2~3초·1.0배속).
- 감속·마지막 프레임 유지·'영상 부족' 표시는 없다. 소스가 모자라면 렌더하지 않고 멈춘다 → USE를 고치고 plan_v8.py를 다시 실행.
- 클립: clips_v6/{id}.mp4가 있으면 그것(신규·재생성), 없으면 clips_v5/{id}.mp4.
- 자막: edit_v5.py와 같다. 힌디(Nirmala UI 흰색+검은 테두리) 위, 한국어 직역(맑은 고딕 노랑, 작게) 아래.
- 결과: out/v8_review_hi.mp4, review_edit/subs_hi.srt, subs_ko.srt, subs.ass, cuts_v8.json, edit_report_v8.json"""
import json, re, subprocess, shutil, sys, tempfile, statistics
from pathlib import Path
import numpy as np, soundfile as sf
from PIL import ImageFont
HERE = Path(__file__).resolve().parent
BUS = HERE.parent; OUT = BUS / "out"; SEG = OUT / "v8_hi_seg"; SEG.mkdir(parents=True, exist_ok=True)
CL5, CL6 = BUS / "clips_v5", BUS / "clips_v6"
FPS, W, H = 30, 1920, 1080
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
def clip(k): return CL6 / f"{k}.mp4" if (CL6 / f"{k}.mp4").exists() else CL5 / f"{k}.mp4"

T = json.load(open(HERE / "narr_timing.json", encoding="utf-8"))
SR = 24000; AUD = sf.read(HERE / "narration_hi.wav", dtype="float32")[0]; ATOT = len(AUD) / SR
PL = json.load(open(BUS / "plan" / "shot_list_v8.json", encoding="utf-8"))
cuts = PL["cuts"]; VTOT = cuts[-1]["out_f1"] / FPS
if VTOT < ATOT: sys.exit(f"계획 길이 {VTOT:.2f}초 < 나레이션 {ATOT:.2f}초: narr_timing.json과 narration_hi.wav가 다르다")
# 소스 확인: 파일 존재, 길이, 겹침 (계획을 만든 뒤 클립이 바뀌었을 수 있으므로 다시 본다)
bad, seen = [], {}
for c in cuts:
    p = clip(c["clip"])
    if not p.exists(): bad.append(f"없음 {p}"); continue
    if c["src_end"] > dur(p) - 0.05: bad.append(f"짧음 {c['clip']} {c['src_end']}초 필요")
    for a, b in seen.get(c["clip"], []):
        if c["src_start"] < b - 1e-6 and c["src_end"] > a + 1e-6: bad.append(f"겹침 {c['clip']} {a}-{b} / {c['src_start']}-{c['src_end']}")
    seen.setdefault(c["clip"], []).append((c["src_start"], c["src_end"]))
if bad: print("\n".join(sorted(set(bad)))); sys.exit("소스 문제 → 렌더 중단")

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
# ---- 컷 렌더 (1.0배속, 소스 구간 그대로) ----
lst = []
for i, c in enumerate(cuts):
    n = c["out_f1"] - c["out_f0"]; seg = SEG / f"{i:03d}.mp4"; c["file"] = seg.name
    vf = (f"trim=start={c['src_start']},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(clip(c["clip"])), "-vf", vf, "-frames:v", str(n), "-an",
                        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", str(FPS), str(seg)], capture_output=True, text=True)
    if r.returncode: print(c, r.stderr[-600:]); sys.exit(1)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                              "-of", "csv=p=0", str(seg)], capture_output=True, text=True).stdout.strip() or 0)
    if got != n: sys.exit(f"{i:03d} {c['clip']}: 프레임 {got}/{n} (소스 끝 도달)")
    lst.append(f"file '{seg.as_posix()}'")
    print(i, c["group"][0], c["clip"], c["src_start"], c["dur"], flush=True)
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
tmp = Path(tempfile.mkdtemp(prefix="v8hi_")); shutil.copy(HERE / "subs.ass", tmp / "subs.ass")
final = OUT / "v8_review_hi.mp4"
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(SEG / "list.txt"), "-i", str(HERE / "narration_hi.wav"),
                    "-vf", "ass=subs.ass", "-af", "apad,aresample=48000", "-ac", "2", "-t", f"{VTOT:.3f}",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(final)], cwd=tmp, capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
L = [c["dur"] for c in cuts]
report = {"total_sec": round(dur(final), 2), "narration_sec": round(ATOT, 2), "cuts": len(cuts), "clips": len({c["clip"] for c in cuts}),
          "median_cut": round(statistics.median(L), 2), "max_cut": max(L), "min_cut": min(L), "speed": 1.0,
          "hi_subs": len(hi_ev), "ko_subs": len(ko_ev), "ko_shrunk": shrunk}
json.dump(cuts, open(HERE / "cuts_v8.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(report, open(HERE / "edit_report_v8.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False, indent=1))
