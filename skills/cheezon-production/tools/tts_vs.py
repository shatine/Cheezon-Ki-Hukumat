"""힌디 나레이션 (무료 Voice Studio): voice_ref_male_charonclone.wav, raw, seed 7, 속도 1.0, 문장(।/?)마다 생성, -16 LUFS.
엄격 잡음 검사(junk_check.jcheck) 불합격 → 같은 seed로 쉼표에서 나눠 조각마다 생성·검사 → 그래도 안 되면 조각을 반으로 →
최후에만 다른 seed(11, 23) (로그에 표시). 같은 seed는 같은 결과(결정적)라서 '그대로 다시'는 의미 없음.
결과: tts_vs/<줄>.wav (문장 사이 0.35초), tts_vs/_sent/*.wav, tts_meta_vs.json, junk_check_vs.json
사용: python tts_vs.py [줄id ...]   (지정 줄만 다시)"""
import json, sys, re, io, shutil, subprocess, hashlib, requests, numpy as np, soundfile as sf
from pathlib import Path
TOOLS = Path(r"D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools")   # 이 스크립트가 쓰는 파일은 모두 여기
sys.path.insert(0, str(TOOLS))
from junk_check import jcheck
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

API = "http://127.0.0.1:3900/generate"
VOICE = TOOLS / "voice_ref_male_charonclone.wav"             # 원본: 채널 voice 폴더
REF_TEXT = (TOOLS / "ref_text.txt").read_text(encoding="utf-8")   # 1편 tts_meta.json의 s01_1 + " " + s01_4 spoken (원래 그 파일에서 읽던 것)
OUT = Path("tts_vs"); SENT = OUT / "_sent"; CACHE = OUT / "_cache"
for p in (SENT, CACHE): p.mkdir(parents=True, exist_ok=True)
SR = 24000; GAP_SENT, GAP_PIECE = 0.35, 0.22

def shorten_gaps(a, sr, thr_db=-45, longer=0.6, keep=0.4):
    hop = int(sr * 0.01); n = len(a) // hop
    db = 20 * np.log10(np.sqrt([np.mean(a[i*hop:(i+1)*hop] ** 2) + 1e-12 for i in range(n)]))
    quiet = db < thr_db; cuts = []; i = 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if i > 0 and j < n and (j - i) * 0.01 > longer:
                h = int(keep / 2 / 0.01); cuts.append(((i + h) * hop, (j - h) * hop))
            i = j
        else: i += 1
    for s, e in reversed(cuts): a = np.concatenate([a[:s], a[e:]])
    return a

def gen(text, seed=7):
    key = hashlib.md5(f"{text}|{seed}".encode()).hexdigest()[:16]; out = CACHE / f"{key}.wav"
    if out.exists(): return out
    with open(VOICE, "rb") as f:
        r = requests.post(API, files={"ref_audio": ("ref.wav", f, "audio/wav")}, data={"text": text, "language": "Hindi",
            "ref_text": REF_TEXT, "seed": str(seed), "speed": "1.0", "effect_preset": "raw"}, timeout=900)
    if not r.content.startswith(b"RIFF"): raise RuntimeError(r.text[:300])
    raw = CACHE / f"{key}_raw.wav"; raw.write_bytes(r.content)
    a, sr = sf.read(raw, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    sf.write(raw, shorten_gaps(a, sr), sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5",
        "-ar", str(SR), "-ac", "1", str(out)], check=True)
    raw.unlink(); return out

def load(p):
    a, _ = sf.read(p, dtype="float32"); return a

def join(parts, gap):
    z = np.zeros(int(SR * gap), np.float32); out = []
    for k, a in enumerate(parts):
        if k: out.append(z)
        out.append(a)
    return np.concatenate(out)

def halves(t):
    w = t.split(); m = len(w) // 2
    return [" ".join(w[:m]), " ".join(w[m:])] if len(w) >= 6 else [t]

def comma_split(t):
    p = [x.strip() for x in re.split(r"(?<=,)\s+", t) if x.strip()]
    return p if len(p) > 1 else halves(t)

def make_piece(text, log):
    """조각 하나: seed 7 → (실패) 반으로 → (실패) seed 11, 23. 결과 (wav배열, 검사결과, 방법)"""
    r = jcheck(gen(text), text)
    if r["pass"]: return load(gen(text)), r, "seed7"
    log.append(f"   piece FAIL seed7 {r['reasons']} {r['junk']} | {text}")
    hs = halves(text)
    if len(hs) > 1:
        rs = [jcheck(gen(h), h) for h in hs]
        if all(x["pass"] for x in rs):
            return join([load(gen(h)) for h in hs], GAP_PIECE), {"pass": True, "parts": rs}, "seed7_halves"
        log.append(f"   halves FAIL {[x['reasons'] for x in rs]}")
    for s in (11, 23):
        r2 = jcheck(gen(text, s), text)
        if r2["pass"]: return load(gen(text, s)), r2, f"seed{s}"
        log.append(f"   piece FAIL seed{s} {r2['reasons']} {r2['junk']}")
    return load(gen(text)), r, "FAILED"

def make_sentence(text, log):
    r = jcheck(gen(text), text)
    if r["pass"]: return load(gen(text)), r, "seed7"
    log.append(f"  sent FAIL seed7 {r['reasons']} {r['junk']} | {text}")
    for vt in comma_variants(text):          # 같은 단어·같은 seed, 쉼표(쉼) 위치만 다르게
        rv = jcheck(gen(vt), vt)
        if rv["pass"]: return load(gen(vt)), rv | {"variant": vt}, "seed7_comma"
        log.append(f"   variant FAIL {rv['reasons']} {rv['junk']} | {vt}")
    pieces = comma_split(text); res = [make_piece(p, log) for p in pieces]
    method = "split:" + "+".join(x[2] for x in res)
    return join([x[0] for x in res], GAP_PIECE), {"pass": all(x[2] != "FAILED" for x in res), "pieces": [x[1] for x in res],
                                                  "first_try": r}, method

CONJ = {"और", "तो", "पर", "लेकिन", "कि", "जो", "जिसमें", "क्योंकि", "फिर", "इसलिए", "यानी", "ताकि"}
def comma_variants(t, n=2):
    w = t.split(); m = len(w) / 2
    idx = sorted([i for i in range(2, len(w) - 2) if w[i] in CONJ and not w[i-1].endswith(",")], key=lambda i: abs(i - m))
    v = [" ".join(w[:i]) + ", " + " ".join(w[i:]) for i in idx[:n]] if len(w) >= 8 else []
    base = t[:-1] if t.endswith(("।", ".")) else t
    return v + [base + ".", base]   # 끝 문장부호만 다르게 / 없이


def sentences(line):
    return [s.strip() for s in re.split(r"(?<=[।?])\s+", line) if s.strip()]

M = json.load(open("tts_meta.json", encoding="utf-8"))
jp = Path("junk_check_vs.json"); J = json.load(open(jp, encoding="utf-8")) if jp.exists() else {}
redo = set(sys.argv[1:])
meta = {}
for lid, v in M.items():
    x = v[0]; out = OUT / x["wav"]
    if not out.exists() or lid in redo or lid not in J:
        log = []; parts = []; info = []
        for k, s in enumerate(sentences(x["spoken"])):
            a, r, how = make_sentence(s, log)
            sf.write(SENT / f"{Path(x['wav']).stem}_{k+1:02d}.wav", a, SR)
            parts.append(a); info.append({"text": s, "method": how, "pass": r["pass"], "dur": round(len(a) / SR, 2),
                                          "chars": len(s), "check": r})
            print(lid, k + 1, how, "PASS" if r["pass"] else "FAIL", round(len(a) / SR, 2), flush=True)
        for l in log: print(l)
        sf.write(out, join(parts, GAP_SENT), SR)
        J[lid] = {"sentences": info, "log": log}
        json.dump(J, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    d = len(load(out)) / SR
    meta[lid] = [{"text": x["text"], "spoken": x["spoken"], "wav": x["wav"], "dur": round(d, 3)}]
json.dump(meta, open("tts_meta_vs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
allS = [s for v in J.values() for s in v["sentences"]]
spc = np.array([s["dur"] / s["chars"] for s in allS]); med = float(np.median(spc))
out_l = [(lid, k + 1, round(s["dur"] / s["chars"] / med, 2)) for lid, v in J.items() for k, s in enumerate(v["sentences"])
         if not 0.75 <= s["dur"] / s["chars"] / med <= 1.3]
bad = [(lid, k + 1) for lid, v in J.items() for k, s in enumerate(v["sentences"]) if not s["pass"]]
tot = sum(v[0]["dur"] for v in meta.values())
print("sentences", len(allS), "fail", bad, "duration outliers (ratio to median s/char)", out_l)
print("total", round(tot, 1), "s")
