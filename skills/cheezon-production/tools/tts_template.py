"""[템플릿: 7편 tts_v5.py] 새 편 폴더 review_edit/에 복사해 쓴다. 힌디 나레이션: lines_v5.tsv (id, hi, ko) → narr/{id}.wav → narration_hi.wav.
6편 tts_06.py 방식 그대로: 무료 Voice Studio, charonclone, seed 7 고정(다른 seed 없음), 속도 1.0, 문장 -16 LUFS,
junk_check 엄격 검사 → 불합격이면 같은 seed로 쉼표 변형 → 쉼표에서 나눠 조각 생성 → 반으로.
문장 사이 0.35초, 문단(S01, S02 …) 사이 0.8초. 타이밍 narr_timing.json.
사용: python tts_v5.py [id ...]"""
import json, sys, re, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = Path(r"D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools")   # tts_vs.py, junk_check.py (5편 폴더에서 옮겨 둔 것)
os.chdir(EP); sys.path.insert(0, str(EP))
src = open(EP / "tts_vs.py", encoding="utf-8").read()
head = src.split("def sentences(line):")[0]
head = head.replace('    for s in (11, 23):', '    for s in ():')          # seed 7 only
head = head.replace('OUT = Path("tts_vs"); SENT = OUT / "_sent"; CACHE = OUT / "_cache"', 'OUT = HERE / "narr"; SENT = OUT / "_sent"; CACHE = OUT / "_cache"')
exec(compile(head, "tts_vs_head", "exec"))
def sentences(line): return [s.strip() for s in re.split(r"(?<=[।?!])\s+", line) if s.strip()]
L = [dict(zip(("id", "hi", "ko"), l.rstrip("\n").split("\t"))) for l in open(HERE / "lines_v5.tsv", encoding="utf-8") if l.strip()]
JP = HERE / "narr_check.json"; J = json.load(open(JP, encoding="utf-8")) if JP.exists() else {}
redo = set(sys.argv[1:])
for x in L:
    lid = x["id"]; out = OUT / f"{lid}.wav"
    if out.exists() and lid in J and lid not in redo and all(s["pass"] for s in J[lid]["sentences"]): continue
    log = []; parts = []; info = []
    for k, s in enumerate(sentences(x["hi"])):
        a, r, how = make_sentence(s, log)
        sf.write(SENT / f"{lid}_{k+1:02d}.wav", a, SR)
        parts.append(a); info.append({"text": s, "method": how, "pass": bool(r["pass"]), "dur": round(len(a) / SR, 2),
                                      "junk": [str(j) for j in (r.get("junk") or [])]})
        print(lid, k + 1, how, "PASS" if r["pass"] else "FAIL", round(len(a) / SR, 2), flush=True)
    for l in log: print(l, flush=True)
    sf.write(out, join(parts, GAP_SENT), SR)
    J[lid] = {"sentences": info, "log": log}
    json.dump(J, open(JP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# 전체: 같은 문단 안 0.35초, 문단 바뀔 때 0.8초
full, tim, t = [], [], 0.0
for i, x in enumerate(L):
    if i:
        g = 0.8 if x["id"][:3] != L[i-1]["id"][:3] else 0.35
        full.append(np.zeros(int(SR * g), np.float32)); t += g
    a = load(OUT / f"{x['id']}.wav"); full.append(a)
    tim.append({"id": x["id"], "start": round(t, 3), "end": round(t + len(a) / SR, 3), "hi": x["hi"], "ko": x["ko"]}); t += len(a) / SR
full = np.concatenate(full)
sf.write(HERE / "narration_hi.wav", full, SR)
json.dump(tim, open(HERE / "narr_timing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bad = [(lid, k + 1, s["text"]) for lid, v in J.items() for k, s in enumerate(v["sentences"]) if not s["pass"]]
print("narration_hi.wav", round(len(full) / SR, 1), "sec | lines", len(J), "/", len(L), "| fail", bad, flush=True)
