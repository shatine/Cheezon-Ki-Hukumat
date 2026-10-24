"""EP7 v9 업로드본(힌디어): edit_v9.py와 같은 컷 렌더 + 힌디어 한 줄 자막만 + 배경음(덕킹) + -14 LUFS → out/v9_upload_hi.mp4.
- 검수본(edit_v9.py)과 다른 점:
  - 한국어 자막 없음. 힌디어 자막은 6편 업로드본 스타일(Nirmala UI 60, 아래 여백 64).
  - 배경음: 6편과 같은 05_morbi_dam_bridge/music/bgm.mp3, -21 dB, 나레이션 사이드체인 덕킹.
  - 끝 2초 페이드아웃, loudnorm I=-14, TP=-1.5.
- 결과: out/v9_upload_hi.mp4, out/v9_upload_subs_hi.srt, review_edit/subs_upload.ass, edit_report_v9_upload.json
------ 아래는 edit_v9.py 설명 ------
EP7 v9 힌디 검수영상: narration_hi.wav + narr_timing.json + plan/shot_list_v9.json → out/v9_review_hi.mp4 (1920x1080, 30fps, 나레이션만).
- plan/plan_v9.py의 컷을 그대로 렌더한다.
  - 영상(kind v)은 쓸 구간 그대로 1.0배속으로 쓴다.
  - 이미지(kind i)는 느린 줌·이동 효과를 준다(effect).
- 옵션:
  - hflip: 좌우 반전.
  - bright: 5.5초 뒤 밝기를 점진적으로 보정한다.
  - blur_plate: 그릴·번호판 영역을 흐린다. 좌표는 BLUR에 있다.
  - haze: 열 아지랑이를 넣는다.
- 소스가 없거나 짧으면 렌더하기 전에 멈춘다.
- 자막은 edit_v5/v8과 같다.
- 결과: out/v9_review_hi.mp4, review_edit/subs_hi.srt, subs_ko.srt, subs.ass, cuts_v9.json, edit_report_v9.json"""
import json, re, subprocess, shutil, sys, tempfile, statistics
from pathlib import Path
import numpy as np, soundfile as sf
from PIL import ImageFont
HERE = Path(__file__).resolve().parent
BUS = HERE.parent; OUT = BUS / "out"; SEG = OUT / "v9_up_seg"; SEG.mkdir(parents=True, exist_ok=True)
BGM = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\05_morbi_dam_bridge\music\bgm.mp3"); BGM_DB = -21.0
FPS, W, H = 30, 1920, 1080
ZOOM = 0.06                      # 이미지 효과: 컷 전체에 걸쳐 6% 확대/축소
BLUR = {"s23b": [(0.5785, 0.5951, 0.0320, 0.0260), (0.5901, 0.6836, 0.0305, 0.0365)], "s23e": [(0.5901, 0.5013, 0.0363, 0.0208), (0.5945, 0.5703, 0.0407, 0.0312), (0.6599, 0.5260, 0.0218, 0.0208)]}   # (x, y, w, h) 이미지 비율: 그릴 상표 글자·번호판 (1376x768 원본에서 확인)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)

T = json.load(open(HERE / "narr_timing.json", encoding="utf-8"))
SR = 24000; AUD = sf.read(HERE / "narration_hi.wav", dtype="float32")[0]; ATOT = len(AUD) / SR
PL = json.load(open(BUS / "plan" / "shot_list_v9.json", encoding="utf-8"))
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
    a = sf.read(HERE / "narr" / f"{lid}.wav", dtype="float32")[0]; d = len(a) / SR
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
    vf = (f"{pre}scale={W*2}:{H*2}:force_original_aspect_ratio=increase:flags=lanczos,crop={W*2}:{H*2},"
          f"zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps={FPS},setsar=1")
    if c["opt"] == "haze":   # 아지랑이: 위쪽 절반을 아주 약하게 흔든다
        vf += ",split[h0][h1];[h1]crop=iw:ih/2:0:0,boxblur=1,geq=lum='lum(X+2*sin(Y/9+T*6),Y)':cb='cb(X,Y)':cr='cr(X,Y)'[hh];[h0][hh]overlay=0:0"
    return vf
lst = []
for i, c in enumerate(cuts):
    n = c["out_f1"] - c["out_f0"]; seg = SEG / f"{i:03d}.mp4"; c["seg"] = seg.name; src = str(BUS / c["file"])
    if c["kind"] == "v":
        vf = f"trim=start={c['src_start']},setpts=PTS-STARTPTS,fps={FPS},{FIT}"
        if c["opt"] == "hflip": vf += ",hflip"
        if c["opt"] == "bright": vf += ",eq=eval=frame:brightness='if(gt(t,5.5),min((t-5.5)/4.5,1)*0.11,0)'"
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
HFS, KFS, MAXW = 60, 44, 1800
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
with open(OUT / "v9_upload_subs_hi.srt", "w", encoding="utf-8") as f:
    for n, (a, b, s) in enumerate(hi_ev, 1): f.write(f"{n}\n{ts_srt(a)} --> {ts_srt(b)}\n{s}\n\n")
ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       f"Style: HI,Nirmala UI,{HFS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,1.5,2,60,60,64,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for a, b, s in hi_ev: ass.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},HI,,0,0,0,,{s}")
(HERE / "subs_upload.ass").write_text("\n".join(ass) + "\n", encoding="utf-8-sig")

# ---- 소리: 나레이션 + 덕킹 배경음, -14 LUFS (6편 render06.py와 같은 방식) ----
tmp = Path(tempfile.mkdtemp(prefix="v9up_")); shutil.copy(HERE / "subs_upload.ass", tmp / "subs.ass")
SR2 = 48000
fc = (f"[1:a]aresample={SR2},aformat=channel_layouts=stereo,volume={BGM_DB}dB,atrim=0:{VTOT:.3f}[bg];"
      f"[0:a]aresample={SR2},aformat=channel_layouts=stereo,apad,atrim=0:{VTOT:.3f},asplit[n1][n2];"
      f"[bg][n2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
      f"[n1][duck]amix=inputs=2:normalize=0:duration=first,afade=t=out:st={VTOT - 2.0:.3f}:d=2,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(HERE / "narration_hi.wav"), "-stream_loop", "-1", "-i", str(BGM),
                    "-filter_complex", fc, "-map", "[out]", "-ar", str(SR2), str(tmp / "mix.wav")], capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)

# ---- 최종: 이어붙이기 + 힌디어 자막 굽기 + 믹스 ----
final = OUT / "v9_upload_hi.mp4"
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(SEG / "list.txt"), "-i", "mix.wav",
                    "-vf", "ass=subs.ass", "-t", f"{VTOT:.3f}",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)], cwd=tmp, capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
lu = subprocess.run(["ffmpeg", "-v", "info", "-i", str(final), "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
L = [c["dur"] for c in cuts]
report = {"total_sec": round(dur(final), 2), "narration_sec": round(ATOT, 2), "cuts": len(cuts), "video_cuts": sum(c["kind"] == "v" for c in cuts), "image_cuts": sum(c["kind"] == "i" for c in cuts),
          "median_cut": round(statistics.median(L), 2), "max_cut": max(L), "min_cut": min(L), "hi_subs": len(hi_ev),
          "lufs": (re.findall(r"I:\s+(-?[\d.]+) LUFS", lu) or ["?"])[-1], "true_peak_dbfs": (re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lu) or ["?"])[-1],
          "bgm": str(BGM), "bgm_db": BGM_DB}
json.dump(report, open(HERE / "edit_report_v9_upload.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False, indent=1))
