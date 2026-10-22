"""<slug>_<에피소드> 캡컷 드래프트의 자막을 5~6단어 단위로 잘라 다시 만든다.
- 시간은 드래프트 안 나레이션 오디오 세그먼트의 실제 위치를 기준으로 한다(사용자가 옮겼어도 따라감).
- 문장 안 단어 시점은 글자 수 비율로 잡고, 음성 파형의 가장 조용한 지점(숨 쉬는 곳)에 맞춘다.
- 자막 스타일·등장 애니메이션은 사용자가 입힌 첫 자막 세그먼트를 그대로 복제한다.
캡컷을 끈 상태에서 실행. 실행 전 draft_content.json 을 백업한다."""
import copy, json, re, shutil, subprocess, time, uuid
from pathlib import Path
import numpy as np

from kit import HERE, CH, NAME
D = Path(CH["capcut"]["root"]) / NAME
SR, HOP = 16000, 160  # 10ms
uid = lambda: str(uuid.uuid4()).upper()


def chunks(text):
    """문장을 최대 6단어 조각으로. 쉼표·마침표 뒤에서 끊는 걸 우선하고, 너무 짧은 조각은 피한다."""
    w = text.split()
    n = len(w)
    if n <= 6:
        return [text]
    punct = lambda i: bool(re.search(r"[,.?!:;]\"?$", w[i - 1]))
    best = [0.0] + [1e9] * n; prev = [0] * (n + 1)
    for j in range(1, n + 1):
        for k in range(max(0, j - 6), j):
            L = j - k
            cost = best[k] + (0 if (j == n or punct(j)) else 3) + (4 if L <= 2 else 0) + 0.2 * (6 - L)
            if cost < best[j]:
                best[j], prev[j] = cost, k
    out, j = [], n
    while j:
        out.append(" ".join(w[prev[j]:j])); j = prev[j]
    return out[::-1]


def wav(path):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, dtype=np.float32)


def boundaries(text, parts, x):
    """각 조각의 시작 시각(초, 문장 기준)."""
    dur = len(x) / SR
    n = len(x) // HOP
    env = np.convolve(np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1)), np.ones(5) / 5, "same")
    letters = lambda s: len(re.sub(r"[\W_]", "", s)) + 0.5 * s.count(",") * 6
    total = letters(text); acc = 0; starts = [0.0]
    for p in parts[:-1]:
        acc += letters(p)
        est = acc / total * dur
        lo, hi = max(1, int((est - 0.25) * 100)), min(n - 1, int((est + 0.25) * 100))
        j = lo + int(np.argmin(env[lo:hi])) if hi > lo else int(est * 100)
        starts.append(max(starts[-1] + 0.3, j / 100))
    return starts, dur


p = D / "draft_content.json"
shutil.copy(p, D / f"draft_content.before_split_{time.strftime('%H%M%S')}.json")
d = json.loads(p.read_text(encoding="utf-8"))
M = d["materials"]
where = {x["id"]: (k, x) for k, v in M.items() if isinstance(v, list) for x in v if isinstance(x, dict) and "id" in x}

# 자막 트랙 = 화면 아래(y<0)에 있는 글자 트랙
sub_tr = next(t for t in d["tracks"] if t["type"] == "text" and t["segments"] and t["segments"][0]["clip"]["transform"]["y"] < 0)
proto_seg = copy.deepcopy(sub_tr["segments"][0])
proto_mat = copy.deepcopy(where[proto_seg["material_id"]][1])
proto_refs = [copy.deepcopy(where[r]) for r in proto_seg["extra_material_refs"] if r in where]

# 기존 자막 세그먼트와 그 소재 제거
old = set()
for s in sub_tr["segments"]:
    old.add(s["material_id"]); old.update(s["extra_material_refs"])
for k, v in M.items():
    if isinstance(v, list):
        M[k] = [x for x in v if not (isinstance(x, dict) and x.get("id") in old)]

# 나레이션 오디오 위치: 소재 파일 이름 → 타임라인 시작
audio_at = {}
for t in d["tracks"]:
    if t["type"] == "audio":
        for s in t["segments"]:
            k, m = where.get(s["material_id"], (None, {}))
            if k == "audios":
                audio_at[Path(m.get("path", "")).name] = s["target_timerange"]["start"] / 1e6

meta = json.loads((HERE / "tts_meta.json").read_text(encoding="utf-8"))
segs, missing = [], []
for sid, items in meta.items():
    for x in items:
        if x["wav"] not in audio_at:
            missing.append(x["wav"]); continue
        t0 = audio_at[x["wav"]]
        parts = chunks(x["text"])
        starts, dur = boundaries(x["text"], parts, wav(HERE / "tts" / x["wav"]))
        ends = starts[1:] + [dur]
        for txt, a, b in zip(parts, starts, ends):
            m = copy.deepcopy(proto_mat); m["id"] = uid()
            c = json.loads(m["content"]); c["text"] = txt
            c["styles"] = [dict(c["styles"][0], range=[0, len(txt.encode("utf-16-le")) // 2])]
            m["content"] = json.dumps(c, ensure_ascii=False)
            M["texts"].append(m)
            s = copy.deepcopy(proto_seg); s["id"] = uid(); s["material_id"] = m["id"]
            s["target_timerange"] = {"start": int(round((t0 + a) * 1e6)), "duration": int(round((b - a) * 1e6))}
            refs = []
            for k, o in proto_refs:
                o = copy.deepcopy(o); o["id"] = uid()
                for an in o.get("animations", []) or []:  # 등장 애니메이션이 조각보다 길면 줄인다
                    if an.get("type") == "in":
                        an["duration"] = min(an["duration"], int((b - a) * 1e6 * 0.6))
                    elif an.get("type") == "out":
                        an["duration"] = min(an["duration"], int((b - a) * 1e6 * 0.3))
                        an["start"] = s["target_timerange"]["duration"] - an["duration"]
                M[k].append(o); refs.append(o["id"])
            s["extra_material_refs"] = refs
            s["render_index"] = 14000 + len(segs)
            segs.append(s)
segs.sort(key=lambda s: s["target_timerange"]["start"])
sub_tr["segments"] = segs

ids = {x["id"] for v in M.values() if isinstance(v, list) for x in v if isinstance(x, dict) and "id" in x}
broken = [r for t in d["tracks"] for s in t["segments"] for r in [s["material_id"], *s["extra_material_refs"]] if r not in ids]
assert not broken, broken[:5]
p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print("subtitle chunks", len(segs), "missing audio", missing)
txt_of = {m["id"]: json.loads(m["content"])["text"] for m in M["texts"]}
for s in segs:
    print(f'{s["target_timerange"]["start"] / 1e6:7.2f} {s["target_timerange"]["duration"] / 1e6:5.2f}  {txt_of[s["material_id"]]}')
