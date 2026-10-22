"""EP7 v7 이미지 30장 (새 규칙: 고정 장면=이미지+효과, 무빙·원리=영상). 목록 근거: 2026-10-22 대화의 '새로 만들어야 하는 것 30장'.
- make_prompts_v6.py의 문구를 재사용하고, s12b·s12c는 내용 변경, s06z·s15d·s24e는 신규.
- 영상으로 만들 것은 s09z 하나(원리 3D). 나머지 29장은 이미지로만 쓴다.
- Flow: 프로젝트 baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd, Nano Banana 2.1 / 16:9 / x2, 한 장씩 생성→검수→다음. ref 그림 첨부.
결과: images/prompts_v7.json (저장: BUS\\img3d\\v7_{id}_{n}.png)"""
import json, runpy
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = runpy.run_path(str(HERE / "make_prompts_v6.py"))   # v6 JSON도 다시 쓰지만 내용은 같다
P, D, BUS = g["P"], g["D"], g["BUS"]
V6 = {a: (b, c, d) for a, b, c, d in g["S"]}
KEEP = ["s08b", "s08c", "s09b", "s09z", "s10b", "s11c", "s13b", "s14c", "s15c", "s16d", "s18b", "s20b", "s22b", "s22c",
        "s23b", "s23c", "s23d", "s23e", "s24b", "s24c", "s24d", "s26b", "s26c", "s26d", "s27b"]
NEW = {
 "s06z": ("PB", "S06a~b 금속 옆판이 달궈짐", f"{P} Using the reference image: {BUS}. Close view of the bus's red-maroon metal side panel with rows of rivets and the yellow band, baking in harsh noon sun, visible heat shimmer rising off the metal, sharp hard shadows. No people."),
 "s12b": ("PB", "S12b 예쁜 합판으로 덮기", f"{P} Interior of the reference bus during conversion: an Indian adult worker fixes a smooth light-wood plywood panel onto the side wall; in the gap beside it the bare grey steel rib and thin insulation are still visible behind. Medium shot, bright window light, face small."),
 "s12c": ("PB", "S12c 돈과 시간 들이면 고칠 수 있다", f"{P} Interior of the reference bus near the end of a conversion: an Indian adult worker tightens the last screw on a finished wood-panelled wall, tools, offcuts and paint tins on the floor, bright clean light. Medium-wide shot, face small."),
 "s15d": (None, "S15c 바깥 전기 꽂기", f"{P} Close-medium shot of an adult's hand plugging a thick black outdoor power cable into a weatherproof socket box on a grey electric pole beside a parked vehicle, bright day. Only hand and arm visible, no readable text."),
 "s24e": ("s24", "S24e 바퀴 달린 방과 땅", f"{P} Using the reference image: the same Kerala caravan park, slightly high angle on one white caravan parked on its paved pad, water hose, drain hose and power cable running from it into the ground pedestal, fence and green hills around. Wide shot, no readable text."),
}
ORDER = ["s06z", "s08b", "s08c", "s09b", "s09z", "s10b", "s11c", "s12b", "s12c", "s13b", "s14c", "s15c", "s15d", "s16d", "s18b",
         "s20b", "s22b", "s22c", "s23b", "s23c", "s23d", "s23e", "s24b", "s24c", "s24d", "s24e", "s26b", "s26c", "s26d", "s27b"]
out = []
for k in ORDER:
    ref, line, pr = NEW[k] if k in NEW else V6[k]
    out.append(dict(id=k, ref=ref, line=line, prompt=pr, use="video" if k == "s09z" else "image"))
json.dump(out, open(HERE / "prompts_v7.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), sum(x["use"] == "video" for x in out))
