"""장면 계획표(plan.json, plan.md). 나레이션 길이(tts_meta.json)로 장면 길이와 비트 시각을 계산한다.
- 장면 길이 = LEAD + 문장 길이 합 + 문장 사이 GAP + TAIL
- 나레이션 없는 장면(브릿지·음악 구간)은 scenes.json 에 "silent_len" 초로 지정
- 생성 길이: Grok 6/10/15초, Veo 4/6/8초 중 1.1배 안에 드는 가장 짧은 것(channel.json "gen_lengths")"""
from collections import Counter
from kit import CH, LEAD, GAP, TAIL, NO_TEXT, load, save, HERE

SC = load("scenes.json")
meta = load("tts_meta.json", {})
LENS = CH.get("gen_lengths", [6, 10, 15])
STY = CH["styles"]

plan, t0 = [], 0.0
md = [f"# {HERE.name} 장면 계획표", "", "| 장면 | 스타일 | 시작 | 길이 | 생성 | 나레이션 |", "|---|---|---|---|---|---|"]
for sid in SC["order"]:
    s = SC["scenes"][sid]
    beats = s["beats"]
    if "silent_len" in s:
        L = float(s["silent_len"]); marks = [round(L * i / len(beats), 1) for i in range(len(beats) + 1)]; text = "(나레이션 없음)"
    else:
        ds = [x["dur"] for x in meta[sid]]
        assert len(ds) == len(beats), f"{sid}: 문장 {len(ds)}개, 비트 {len(beats)}개 — 문장 수와 비트 수를 맞추세요"
        marks, t = [0.0], LEAD
        for i, d in enumerate(ds):
            t += d
            if i < len(ds) - 1:
                t += GAP
            marks.append(round(t if i < len(ds) - 1 else t + TAIL, 1))
        L = marks[-1]; text = " ".join(x["text"] for x in meta[sid])
    gen = next((g for g in LENS if g * 1.1 >= L), LENS[-1])
    lines = [f"[{marks[i]:.0f}-{marks[i+1]:.0f}s] {b}" for i, b in enumerate(beats)]
    prompt = "\n".join(lines) + f"\nAudio: {s.get('audio', 'soft ambience')}.\n" + STY[s["style"]]["suffix"] + " " + NO_TEXT
    plan.append({"id": sid, "style": s["style"], "start": round(t0, 1), "len": round(L, 2), "gen": gen, "text": text,
                 "refs": s.get("refs", []), "image": s.get("image", ""), "prompt": prompt})
    md.append(f"| {sid} | {STY[s['style']]['label']} | {t0:.1f} | {L:.1f} | {gen} | {text[:70]}{'…' if len(text) > 70 else ''} |")
    t0 += L
md += ["", f"총 길이 {t0:.1f}초 ({t0/60:.1f}분), 클립 {len(plan)}개", "", "## 프롬프트", ""]
for p in plan:
    md += [f"### {p['id']} ({p['len']:.1f}s → {p['gen']}s)", "", "```", p["prompt"], "```", ""]
save("plan.json", plan)
(HERE / "plan.md").write_text("\n".join(md), encoding="utf-8")
print(f"{len(plan)} clips, {t0:.1f}s", Counter(p["gen"] for p in plan), Counter(p["style"] for p in plan))
