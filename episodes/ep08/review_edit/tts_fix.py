"""8편 TTS 보정 (tts.py 이후 실행, 대본 글자는 바꾸지 않음).
1) S18b "हवा।": 한 단어는 Voice Studio가 0초 소리를 냄 → S18a + " हवा।"를 한 번에 생성(seed 7)하고 Whisper 단어 시각으로 "हवा"만 잘라 씀.
2) ASR 오판으로 판단한 문장은 문장 전체 seed 7 원본을 쓰고 pass로 표시(asr_false_positive, 사용자 청취 확인 필요):
   - S01b·S02b·S23a(359), S06c(469): 두 ASR 모두 उन- 숫자를 +10으로 받아씀. 369를 적은 'तीन सौ उनहत्तर'도 379로 받아씀(시험 확인).
   - S03c: '+से' 삽입은 두 번째 ASR(/transcribe)에서 나오지 않음.
   - S19b: चौबीसों → '24' 숫자 표기 차이.
   - S21b: 'भूकंप आया' → 'भूकम पाया' 단어 경계 차이.
끝나면 python tts.py 를 다시 돌려 narration_hi.wav와 narr_timing.json을 만든다(통과 줄은 건너뜀)."""
import json, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = Path(r"D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools")
os.chdir(EP); sys.path.insert(0, str(EP))
head = open(EP / "tts_vs.py", encoding="utf-8").read().split("def sentences(line):")[0]
head = head.replace('OUT = Path("tts_vs"); SENT = OUT / "_sent"; CACHE = OUT / "_cache"', 'OUT = HERE / "narr"; SENT = OUT / "_sent"; CACHE = OUT / "_cache"')
exec(compile(head, "tts_vs_head", "exec"))
from junk_check import whisper_words
L = {l.split("\t")[0]: l.rstrip("\n").split("\t")[1] for l in open(HERE / "lines.tsv", encoding="utf-8") if l.strip()}
JP = HERE / "narr_check.json"; J = json.load(open(JP, encoding="utf-8"))

# 1) S18b
ctx = L["S18a"] + " " + L["S18b"]
p = gen(ctx); a = load(p); txt, words = whisper_words(p)
hw = [w for w in words if "हवा" in w["word"]]
if not hw: sys.exit(f"S18b: 문맥 생성에서 हवा를 못 찾음: {txt}")
w = hw[-1]; s0 = max(0, int((w["start"] - 0.06) * SR)); cut = a[s0:]
fade = min(len(cut), int(0.01 * SR)); cut[:fade] *= np.linspace(0, 1, fade)
sf.write(SENT / "S18b_01.wav", cut, SR); sf.write(OUT / "S18b.wav", cut, SR)
J["S18b"] = {"sentences": [{"text": L["S18b"], "method": "context_cut(S18a+S18b)", "pass": True, "dur": round(len(cut) / SR, 2),
                            "junk": [], "note": f"context asr: {txt}; cut at {w['start']:.2f}s"}], "log": [f"context take: {txt}"]}
print("S18b", round(len(cut) / SR, 2), "s | context asr:", txt, flush=True)

# 2) ASR 오판 → 문장 전체 원본
NOTE = {"S01b": "asr +10 on उन- numbers (359->369)", "S02b": "asr +10 on उन- numbers (359->369)", "S23a": "asr +10 on उन- numbers (359->369)",
        "S06c": "asr +10 on उन- numbers (469->479)", "S03c": "'+से' not in second ASR", "S19b": "चौबीसों written as digits 24",
        "S21b": "word boundary भूकंप आया -> भूकम पाया"}
for lid, note in NOTE.items():
    t = L[lid]; a = load(gen(t))
    sf.write(SENT / f"{lid}_01.wav", a, SR); sf.write(OUT / f"{lid}.wav", a, SR)
    old = J[lid]["sentences"][0]
    J[lid]["sentences"] = [{"text": t, "method": "seed7_full", "pass": True, "dur": round(len(a) / SR, 2), "junk": [],
                            "asr_false_positive": note, "first_check": old.get("method"), "needs_listening": True}]
    print(lid, round(len(a) / SR, 2), "s |", note, flush=True)
json.dump(J, open(JP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
