"""Grok용 이미지→영상 프롬프트(i2v.json). 장면마다 기준 그림 + 첫 장면 이미지 프롬프트 + 영상 프롬프트.
- 기준 그림은 ref/ 폴더(channel.json refs 의 파일들). 장면별로 scenes.json "refs" 에 필요한 것만 적는다.
- 첫 이미지 프롬프트는 scenes.json "image"(없으면 첫 비트)."""
from kit import CH, NO_TEXT, load, save, HERE

STY = CH["styles"]
plan = load("plan.json")
out = []
for p in plan:
    st = STY[p["style"]]
    refs = [str(HERE / "ref" / r) for r in p["refs"]]
    keep = " ".join(CH["refs"][r] for r in p["refs"] if r in CH["refs"])
    first_beat = p["prompt"].split("\n")[0].split("] ", 1)[1]
    img = f"{keep} {p['image'] or first_beat} {st['suffix']} 16:9. No text, no letters, no numbers. Only adults, no children.".strip()
    beats = p["prompt"].split("Audio:")[0].strip().replace("\n", " ")
    audio = "Audio:" + p["prompt"].split("Audio:")[1].split("\n")[0]
    vid = (f"Animate this exact image. {st.get('keep', 'Keep every character and the drawing style exactly the same in every frame.')} "
           f"{beats} {audio} No new characters. {NO_TEXT}")
    out.append({"id": p["id"], "style": p["style"], "gen": p["gen"], "len": p["len"], "refs": refs, "image": img, "video": vid})
save("i2v.json", out)
print(len(out), "scenes; longest video prompt", max(len(o["video"]) for o in out))
