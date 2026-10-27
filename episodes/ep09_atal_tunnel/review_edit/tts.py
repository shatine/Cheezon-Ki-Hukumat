"""9편 무료 로컬 TTS. 승인된 lines.tsv, charonclone, seed 7, speed 1.0.

기존 tts_template.py의 생성·엄격 검사·같은 seed 재시도를 사용한다.
오디오와 캐시는 PC 에피소드 폴더에만 보관한다. 실패를 통과로 바꾸지 않는다.
사용: python tts.py [--only S01a ...] [--redo S01a ...]
"""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = Path(r"D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools")
CONFIG = json.loads((HERE / "tts_config.json").read_text(encoding="utf-8"))
input_bytes = (HERE / "lines.tsv").read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
if hashlib.sha256(input_bytes).hexdigest() != CONFIG["lines_sha256"]:
    raise RuntimeError("lines.tsv differs from the reviewed Hindi input")
if hashlib.sha256((TOOLS / "voice_ref_male_charonclone.wav").read_bytes()).hexdigest() != CONFIG["voice_reference_sha256"]:
    raise RuntimeError("Voice reference differs from the confirmed charonclone file")

parser = argparse.ArgumentParser()
parser.add_argument("--only", nargs="+")
parser.add_argument("--redo", nargs="*", default=[])
args = parser.parse_args()
os.chdir(TOOLS)
sys.path.insert(0, str(TOOLS))
head = (TOOLS / "tts_vs.py").read_text(encoding="utf-8").split("def sentences(line):")[0]
for old, new in (
    ('    for s in (11, 23):', '    for s in ():'),
    ('OUT = Path("tts_vs"); SENT = OUT / "_sent"; CACHE = OUT / "_cache"',
     'OUT = HERE / "narr"; SENT = OUT / "_sent"; CACHE = OUT / "_cache"'),
    ('"effect_preset": "raw"', '"effect_preset": "raw", "engine": "omnivoice"'),
):
    if old not in head:
        raise RuntimeError("Production TTS template changed; inspect before running")
    head = head.replace(old, new)
exec(compile(head, "episode_tts_template", "exec"))

import junk_check as _junk
import asr_check as _asr
_original_tokens = _junk.tokens

def decimal_tokens(text):
    # 9.02의 낭독형에서 0을 보존한다. 9.2를 9.02로 허용하지 않는다.
    text = re.sub(r"नौ\s+दशमलव\s+(?:शून्य|जीरो|ज़ीरो)\s+दो", "9.02", text)
    # 기존 fix_words가 가설에만 적용하던 표준/구어 지시어 대응을 원문에도 동일 적용.
    equivalent = {_asr._base("यह"): _asr._base("ये"), _asr._base("वह"): _asr._base("वो")}
    return [equivalent.get(token, token) for token in _original_tokens(text)]

_junk.tokens = decimal_tokens
_asr.tokens = decimal_tokens

rows = [dict(zip(("id", "hi", "ko"), line.split("\t")))
        for line in input_bytes.decode("utf-8").splitlines() if line]
selected = set(args.only or [x["id"] for x in rows])
unknown = selected - {x["id"] for x in rows}
if unknown:
    raise RuntimeError(f"Unknown sentence ids: {sorted(unknown)}")
check_path = HERE / "narr_check.json"
checks = json.loads(check_path.read_text(encoding="utf-8")) if check_path.exists() else {}

for x in rows:
    lid = x["id"]
    if lid not in selected:
        continue
    output = OUT / f"{lid}.wav"
    previous = checks.get(lid, {})
    if (output.exists() and previous.get("hi") == x["hi"] and lid not in args.redo
            and previous.get("sentences") and all(s["pass"] for s in previous["sentences"])):
        continue
    print(lid, "START", flush=True)
    class ReviewLog(list):
        def append(self, message):
            super().append(message)
            print(lid, "RETRY", message, flush=True)
    log, parts, info = ReviewLog(), [], []
    for k, text in enumerate(s.strip() for s in re.split(r"(?<=[।?!])\s+", x["hi"]) if s.strip()):
        a, result, method = make_sentence(text, log)
        sentence_path = SENT / f"{lid}_{k+1:02d}.wav"
        sf.write(sentence_path, a, SR)
        if method.startswith("split:"):
            combined = _junk.jcheck(sentence_path, text)
            result = {**result, "pass": bool(result["pass"] and combined["pass"]), "combined_check": combined}
        parts.append(a)
        info.append({"text": text, "method": method, "pass": bool(result["pass"]),
                     "dur": round(len(a) / SR, 3), "check": result})
        print(lid, k+1, method, "PASS" if result["pass"] else "FAIL", round(len(a)/SR, 2), flush=True)
    sf.write(output, join(parts, GAP_SENT), SR)
    checks[lid] = {"hi": x["hi"], "sentences": info, "log": log}
    check_path.write_text(json.dumps(checks, ensure_ascii=False, indent=1), encoding="utf-8")

missing = [x["id"] for x in rows if not (OUT / f"{x['id']}.wav").exists()]
bad = [x["id"] for x in rows if x["id"] in checks
       and not all(s["pass"] for s in checks[x["id"]]["sentences"])]
if missing:
    print("Partial generation; remaining", len(missing), "failed", bad, flush=True)
    sys.exit(1 if bad else 0)

full, timing, t = [], [], 0.0
for i, x in enumerate(rows):
    if i:
        gap = 0.8 if x["id"][:3] != rows[i-1]["id"][:3] else 0.35
        full.append(np.zeros(int(SR * gap), np.float32))
        t += gap
    a = load(OUT / f"{x['id']}.wav")
    full.append(a)
    timing.append({"id": x["id"], "start": round(t, 3), "end": round(t + len(a)/SR, 3),
                   "hi": x["hi"], "ko": x["ko"]})
    t += len(a) / SR
full = np.concatenate(full)
sf.write(HERE / "narration_hi.wav", full, SR)
(HERE / "narr_timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding="utf-8")
print("narration_hi.wav", round(len(full)/SR, 3), "seconds | lines", len(rows), "| failed", bad, flush=True)
sys.exit(1 if bad else 0)
