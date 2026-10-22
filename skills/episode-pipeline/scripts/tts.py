"""나레이션 생성. scene_lines.json 문장마다 로컬 TTS 서버로 참조 음성(channel.json voice)을 복제해 wav 를 만든다.
결과: tts/<장면>_<번호>.wav, tts_meta.json
사용: python tts.py            (없는 파일만 생성)
      python tts.py H2 F1      (지정 장면은 다시 생성 — 받아쓰기로 발음이 이상한 문장만)"""
import sys, requests
from kit import HERE, CH, load, save, dur

V = CH["voice"]
OUT = HERE / "tts"; OUT.mkdir(exist_ok=True)
REF = HERE / V["ref_audio"]  # 기본 assets/voice_ref.wav 를 에피소드 폴더에 복사. 채널에 맞는 목소리로 교체 가능
REPL = load("scenes.json").get("repl", [])  # 숫자·연도 읽는 법 [["In 2012", "In twenty twelve"], ...]


def normalize(t):
    for a, b in REPL + [['"', ""]]:
        t = t.replace(a, b)
    return t


lines = load("scene_lines.json")
only = set(sys.argv[1:]); meta = {}
for sid, texts in lines.items():
    meta[sid] = []
    for i, text in enumerate(texts):
        out = OUT / f"{sid}_{i:02d}.wav"; spoken = normalize(text)
        if not out.exists() or sid in only:
            with open(REF, "rb") as f:
                r = requests.post(V["api"], files={"ref_audio": ("ref.wav", f, "audio/wav")},
                                  data={"text": spoken, "language": V["language"], "ref_text": V["ref_text"], "seed": str(V["seed"]),
                                        "speed": str(V["speed"]), "effect_preset": V["effect_preset"]}, timeout=600)
            r.raise_for_status()
            if not r.content.startswith(b"RIFF"):
                raise RuntimeError(f"{sid}_{i}: {r.text[:300]}")
            out.write_bytes(r.content)
        meta[sid].append({"text": text, "spoken": spoken, "wav": out.name, "dur": dur(out)})
    print(sid, f"{sum(x['dur'] for x in meta[sid]):.1f}s", flush=True)
save("tts_meta.json", meta)
