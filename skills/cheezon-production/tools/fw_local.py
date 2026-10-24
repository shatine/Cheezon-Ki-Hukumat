"""Voice Studio 서버가 꺼졌을 때: 같은 모델(faster-whisper large-v3, 같은 캐시)을 Voice Studio venv 파이썬으로 직접 돌려 받아쓰기.
사용: <venv python> fw_local.py out.json a.wav [b.wav ...]  → [{text, words:[{word,start,end}]}]"""
import sys, json, glob
import os, torch  # cuDNN·cuBLAS DLL 경로를 먼저 올림 (없으면 ctranslate2가 죽음)
import site
for sp in site.getsitepackages():
    d = os.path.join(sp, 'cudnn8_compat', 'nvidia', 'cudnn', 'bin')
    if os.path.isdir(d): os.add_dll_directory(d); os.environ['PATH'] = d + os.pathsep + os.environ['PATH']
from faster_whisper import WhisperModel
path = glob.glob(r"C:\Users\developer1\AppData\Local\OmniVoice\hf_cache\models--Systran--faster-whisper-large-v3\snapshots\*")[0]
m = WhisperModel(path, device="cuda", compute_type="float16"); res = []
for wav in sys.argv[2:]:
    segs, _ = m.transcribe(wav, language="hi", word_timestamps=True, vad_filter=True)
    words, texts = [], []
    for s in segs:
        texts.append(s.text); words += [{"word": w.word, "start": w.start, "end": w.end} for w in (s.words or [])]
    res.append({"text": " ".join(texts).strip(), "words": words})
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
os._exit(0)   # 종료 중 CUDA 정리에서 죽는 문제 회피
