r"""8편 체납 철교 검수본 v1 (7편 edit_v9.py 템플릿 기반).
narration_hi.wav + narr_timing.json + plan/shot_list_v2.json → CB/out/v1_review_hi.mp4 (1920x1080, 30fps, 나레이션만, 힌디어+한국어 자막)
+ 클라우드 검수용 작은 본 CB/out/v1_review_small.mp4 (960x540).
- 이 파일은 저장소 episodes/ep08/review_edit/에 있고, 미디어는 CB(D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge)에서 읽는다.
  - CB\review_edit\narration_hi.wav, CB\review_edit\narr\{id}.wav (TTS 결과), CB\clips_v1\*.mp4, CB\img\*.png
- 계획(plan_v2)의 컷을 그대로 렌더한다. 영상은 쓸 구간 그대로 1.0배속, 이미지는 느린 줌·이동.
- 옵션 (plan_v2 opt):
  - flow_wm: Flow 클립(1280x720) 오른쪽 아래 별 워터마크 지우기(delogo)
  - bright: 영상은 컷 전체에 걸쳐 점진 밝기 보정(v12), 이미지는 BRIGHT 감마(i23b, i24)
  - blur_plate: 이미지 BLUR 좌표 흐림(i19a2 명판, i20a 번호판)
  - x5 표기: V02에 숫자 표기 LABEL ("359 m" 초록 막대 위, "×5" 쿠툽 옆)
- 소스가 없거나 짧으면 렌더하기 전에 멈춘다.
- 결과: CB/out/v1_review_hi.mp4, v1_review_small.mp4, 이 폴더의 subs_hi.srt, subs_ko.srt, subs.ass, cuts_v1.json, edit_report_v1.json"""
import json, re, subprocess, shutil, sys, tempfile, statistics
from pathlib import Path
import numpy as np, soundfile as sf
from PIL import ImageFont
import os
HERE = Path(__file__).resolve().parent; EP = HERE.parent
BUS = Path(os.environ.get("CB", r"D:\youtube\7. Cheezon Ki Hukumat\episodes\08_chenab_bridge"))
AUDIO = BUS / "review_edit"; OUT = BUS / "out"; SEG = OUT / "v1_hi_seg"; SEG.mkdir(parents=True, exist_ok=True)
FPS, W, H = 30, 1920, 1080
ZOOM = 0.06                      # 이미지 효과: 컷 전체에 걸쳐 6% 확대/축소
BLUR = {"i19a2": [(0.2413, 0.5234, 0.0291, 0.0391)], "i20a": [(0.0, 0.6120, 0.0545, 0.0456)]}   # (x, y, w, h) 이미지 비율 (1376x768 원본, 클라우드 검수 v3·v4)
BRIGHT = {"i23b": 1.15, "i24": 1.25}   # 이미지 감마 (노을 장면)
FLOW_WM = "delogo=x=1132:y=572:w=58:h=58"   # Flow 1280x720 별 워터마크 (V05·V09·V20b)
FONT = os.environ.get("LABEL_FONT", "C\\:/Windows/Fonts/arialbd.ttf")
# V02 숫자 표기: (글자, x, y, 컷 안 시작 초) 1920x1080 출력 기준. 초록 = 숫자 (채널 색 약속)
LABEL = {"V02": [("359 m", 1040, 175, 5.0), ("×5", 1185, 430, 0.8)]}
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)

T = json.load(open(HERE / "narr_timing.json", encoding="utf-8"))
AUD, SR = sf.read(AUDIO / "narration_hi.wav", dtype="float32"); ATOT = len(AUD) / SR
PL = json.load(open(EP / "plan" / "shot_list_v2.json", encoding="utf-8"))
cuts = PL["cuts"]; VTOT = cuts[-1]["out_f1"] / FPS
if VTOT < ATOT: sys.exit(f"계획 길이 {VTOT:.2f}초 < 나레이션 {ATOT:.2f}초: narr_timing.json과 narration_hi.wav가 다르다")
bad = []
for c in cuts:
    p = BUS / c["file"]
    if not p.exists(): bad.append(f"없음 {p}"); continue
    if c["kind"] == "v" and c["src_end"] > dur(p) - 0.03: bad.append(f"짧음 {c['src']} {c['src_end']}초 필요")
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
    a = sf.read(AUDIO / "narr" / f"{lid}.wav", dtype="float32")[0]; d = len(a) / SR
    sil = silences(a); used = set(); res = []
    for c in cuts_chars:
        e = d * c / len(text)
        cand = [s for s in sil if abs(s - e) < 1.2 and s not in used]
        s = min(cand, key=lambda s: abs(s - e)) if cand else e
        used.add(s); res.append(s)
    return res
# ---- 컷 렌더 ----
FIT = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
def img_vf(c):
    n = c["out_f1"] - c["out_f0"]; e = c["effect"]; zin = e.startswith("in")
    z = f"1+{ZOOM}*on/{n}" if zin else f"1+{ZOOM}-{ZOOM}*on/{n}"
    x = {"c": "(iw-iw/zoom)/2", "l": "(iw-iw/zoom)*(1-on/" + str(n) + ")", "r": "(iw-iw/zoom)*on/" + str(n)}[e[-1]]
    pre = ""
    if c["opt"] == "blur_plate":
        for k, (bx, by, bw, bh) in enumerate(BLUR.get(c["src"], [])):
            pre += (f"split[a{k}][b{k}];[b{k}]crop=iw*{bw}:ih*{bh}:iw*{bx}:ih*{by},gblur=sigma=6[bb{k}];"
                    f"[a{k}][bb{k}]overlay=W*{bx}:H*{by},")
    if c["src"] in BRIGHT: pre += f"eq=gamma={BRIGHT[c['src']]},"
    vf = (f"{pre}scale={W*2}:{H*2}:force_original_aspect_ratio=increase:flags=lanczos,crop={W*2}:{H*2},"
          f"zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps={FPS},setsar=1")
    if c["opt"] == "haze":   # 아지랑이: 위쪽 절반을 아주 약하게 흔든다
        vf += ",split[h0][h1];[h1]crop=iw:ih/2:0:0,boxblur=1,geq=lum='lum(X+2*sin(Y/9+T*6),Y)':cb='cb(X,Y)':cr='cr(X,Y)'[hh];[h0][hh]overlay=0:0"
    return vf
lst = []
for i, c in enumerate(cuts):
    n = c["out_f1"] - c["out_f0"]; seg = SEG / f"{i:03d}.mp4"; c["seg"] = seg.name; src = str(BUS / c["file"])
    if c["kind"] == "v":
        vf = f"trim=start={c['src_start']},setpts=PTS-STARTPTS,fps={FPS}," + (FLOW_WM + "," if c["opt"] == "flow_wm" else "") + FIT
        if c["opt"] == "hflip": vf += ",hflip"
        if c["opt"] == "bright": vf += f",eq=eval=frame:brightness='min(t/{c['dur']},1)*0.14':gamma='1+min(t/{c['dur']},1)*0.25'"
        for k, (txt, lx, ly, t0) in enumerate(LABEL.get(c["src"], [])):
            vf += (f",drawtext=fontfile='{FONT}':text='{txt}':fontsize=96:fontcolor=0x33FF33:"
                   f"borderw=7:bordercolor=black:x={lx}:y={ly}:enable='gte(t,{t0})'")
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", vf]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", src, "-filter_complex", img_vf(c)]
    r = subprocess.run(cmd + ["-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
                              "-r", str(FPS), str(seg)], capture_output=True, text=True)
    if r.returncode: print(c, r.stderr[-800:]); sys.exit(1)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                              "-of", "csv=p=0", str(seg)], capture_output=True, text=True).stdout.strip() or 0)
    if got != n: sys.exit(f"{i:03d} {c['src']}: 프레임 {got}/{n}")
    lst.append(f"file '{seg.as_posix()}'")
    print(i, c["start"], c["src"], c["kind"], c["dur"], c.get("effect", ""), c["opt"], flush=True)
(SEG / "list.txt").write_text("\n".join(lst), encoding="utf-8")

# ---- 자막 ----
HFS, KFS, MAXW = 58, 44, 1800
hfont = ImageFont.truetype(os.environ.get("HI_FONT", r"C:\Windows\Fonts\Nirmala.ttc"), HFS, index=0)
kfont = lambda s: ImageFont.truetype(os.environ.get("KO_FONT", r"C:\Windows\Fonts\malgunbd.ttf"), s)
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
tmp = Path(tempfile.mkdtemp(prefix="v1hi_")); shutil.copy(HERE / "subs.ass", tmp / "subs.ass")
final = OUT / "v1_review_hi.mp4"
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(SEG / "list.txt"), "-i", str(AUDIO / "narration_hi.wav"),
                    "-vf", "ass=subs.ass", "-af", "apad,aresample=48000", "-ac", "2", "-t", f"{VTOT:.3f}",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(final)], cwd=tmp, capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
L = [c["dur"] for c in cuts]
report = {"total_sec": round(dur(final), 2), "narration_sec": round(ATOT, 2), "cuts": len(cuts), "video_cuts": sum(c["kind"] == "v" for c in cuts), "image_cuts": sum(c["kind"] == "i" for c in cuts),
          "median_cut": round(statistics.median(L), 2), "max_cut": max(L), "min_cut": min(L), 
          "hi_subs": len(hi_ev), "ko_subs": len(ko_ev), "ko_shrunk": shrunk}
json.dump(cuts, open(HERE / "cuts_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(report, open(HERE / "edit_report_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False, indent=1))

# ---- 클라우드 검수용 작은 본 (깃 100MB 제한) ----
small = OUT / "v1_review_small.mp4"
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "30", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(small)], capture_output=True, text=True)
if r.returncode: print(r.stderr[-800:]); sys.exit(1)
print("small:", small, round(small.stat().st_size / 1e6, 1), "MB")
