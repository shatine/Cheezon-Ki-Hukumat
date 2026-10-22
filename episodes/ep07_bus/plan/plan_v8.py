"""EP7 컷 계획 v8: 문장별 배정 + 규칙 자동 점검 (cheezon-video '생성 전 필수 확인', bhopal-production-lessons).
입력: review_edit/narr_timing.json(실측), video/vprompts_v5.json·v6.json(클립 동작), images/prompts_v5/v6.json(기준 그림)
출력: plan/shot_list_v8.json (컷별 소스 구간·프레임), plan/shot_table_v8.md (문장별 표 + 점검 결과)
G = (문장 ID들, 클립 순서). 그룹 길이를 컷 수로 똑같이 나눈다. 같은 클립은 앞 사용의 다음 프레임부터 이어 쓴다(continuity).
신규 클립의 사용 가능 길이는 10초로 가정 → 생성 후 실제 쓸 구간으로 USE를 고치고 다시 실행한다."""
import json, re
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
FPS = 30
TAIL = 1.0                                          # edit: 영상 = 나레이션 끝 + 1초
T = json.load(open(EP / "review_edit/narr_timing.json", encoding="utf-8"))
END = {x["id"]: (T[i + 1]["start"] if i + 1 < len(T) else x["end"] + TAIL) for i, x in enumerate(T)}
START = {x["id"]: (0.0 if i == 0 else x["start"]) for i, x in enumerate(T)}
KO = {x["id"]: x["ko"] for x in T}
V5 = {x["id"]: x for x in json.load(open(EP / "video/vprompts_v5.json", encoding="utf-8"))}
V6 = {x["id"]: x for x in json.load(open(EP / "video/vprompts_v6.json", encoding="utf-8"))}
I6 = {x["id"]: x for x in json.load(open(EP / "images/prompts_v6.json", encoding="utf-8"))}
I5 = {x["id"]: x for x in json.load(open(EP / "images/prompts_v5.json", encoding="utf-8"))}
# 쓸 구간(초). v5: clips_v5_usable.md. h1의 앞 2.3초는 S01, 7~9.5초는 S25 회수 컷.
CEND = 9.95                                        # 10초 클립의 끝 0.05초는 쓰지 않는다(edit와 같음)
USE = {"PB": [(0, 7)], "s03": [(0, 6)], "s10": [(0, 7)], "s14a": [(3, CEND)], "s14b": [(3, CEND)], "s15a": [(5, CEND)],
       "s15b": [(0, 7)], "s28": [(4, CEND)], "h1": [(0, 2.5), (7, 9.5)]}
OPENING = {"h1", "h2", "h3", "h4", "m1"}           # v5 도입 클립(프롬프트 저장소에 없음)
G = [
 (["S01a"], ["h1"]),
 (["S02a"], ["h2", "m1"]),                          # 화려함 → 한 달 뒤
 (["S02b"], ["m3s"]),
 (["S03a", "S03b", "S03c"], ["PB", "s03", "s03b", "s03", "s03b"]),
 (["S04a", "S04b"], ["s04a", "M3", "s04a"]),
 (["S04c", "S04d"], ["s01", "s04b"]),
 (["S04e"], ["s04c", "s01"]),
 (["S05a"], ["m2", "s02"]),
 (["S06a", "S06b"], ["s06b", "s09b"]),
 (["S06c"], ["s06a", "s06d"]),
 (["S06d", "S06e"], ["s06b", "s06c", "s06b"]),
 (["S07a"], ["s07a", "s06c"]),
 (["S07b", "S07c"], ["s07b", "s07a", "s07b"]),
 (["S08a", "S08b"], ["s08b"]),
 (["S08c", "S08d"], ["s08", "s08b", "s08", "s08c"]),
 (["S09a", "S09b"], ["s09b", "s09", "s09b"]),
 (["S09c", "S09d", "S09e"], ["s09z", "s09", "s09z", "s09"]),
 (["S10a"], ["s09z"]),
 (["S10b", "S10c"], ["s10b", "s10", "s10b", "s10"]),
 (["S11a"], ["s11c"]),
 (["S11b", "S11c"], ["s11a", "s11c", "s11a", "s11c"]),
 (["S11d"], ["s11b", "s11a"]),
 (["S12a"], ["s12b", "s12", "s12c"]),
 (["S12b"], ["s11b", "s12"]),
 (["S12c"], ["s12b", "s12c"]),
 (["S13a", "S13b", "S13c"], ["s13", "s13b", "s13", "s13b"]),
 (["S14a", "S14b"], ["s14c", "M3", "s14a"]),
 (["S14c"], ["s14b", "s14a", "s14b"]),
 (["S14d"], ["s14c", "M3"]),
 (["S15a"], ["s15c", "s15a", "s15c"]),
 (["S15b", "S15c"], ["s15b", "s07b", "s15b", "s15c"]),
 (["S16a", "S16b"], ["s15a", "s16a"]),
 (["S16c"], ["s16c", "s16a"]),
 (["S16d"], ["s16d", "s16b", "s16d"]),
 (["S17a", "S17b"], ["s16b", "s17a"]),
 (["S17c"], ["s17b", "s18b", "s17b", "s18b"]),
 (["S17d"], ["s17a", "s16b", "s17a"]),
 (["S18a"], ["s16c", "s18", "s18b"]),
 (["S18b"], ["s05"]),
 (["S19a"], ["s19", "s19b", "s19"]),
 (["S20a"], ["s20", "s20b"]),
 (["S20b", "S20c"], ["s20", "s20b", "s20"]),
 (["S21a"], ["s21a", "s21c"]),
 (["S21b", "S21c"], ["s21b", "s26b", "s21b", "s26b"]),
 (["S22a", "S22b"], ["s22", "s22b", "s22", "s22b"]),
 (["S22c"], ["s22", "s22c"]),
 (["S23a"], ["s23b", "s23"]),
 (["S23b"], ["s23b", "s23", "s23e", "s23"]),
 (["S23c"], ["s23c", "s23d"]),
 (["S23d"], ["s18", "s23d", "s23e"]),
 (["S24a", "S24b"], ["s24", "s24b", "s24"]),
 (["S24c"], ["s24c", "s24b", "s24d", "s24c"]),
 (["S24d", "S24e"], ["s24", "s24c", "s16a"]),
 (["S25a", "S25b"], ["s25", "h1"]),                 # h1 = S01 질문 회수(의도적 재사용, 겹치지 않는 구간)
 (["S26a"], ["s19"]),
 (["S26b"], ["s26c", "s20b", "s26b"]),
 (["S26c", "S26d"], ["s04b", "s26d", "s12"]),
 (["S26e"], ["s26", "s26d", "s26"]),
 (["S27a", "S27b"], ["s04b", "s27b", "s27"]),
 (["S28a"], ["s28", "s28b"]),
]

def motion(c):
    v = V6.get(c) or V5.get(c)
    return v["prompt"].split(" [")[0] if v else "(v5 도입 클립, 프롬프트 기록 없음)"
def ref(c):
    i = I6.get(c) or I5.get(c)
    return (i.get("ref") or "-") if i else "-"
def is_new(c): return c in V6

cuts, errs, pos, uses = [], [], {}, {}
seq = [s for g in G for s in g[0]]
if seq != [x["id"] for x in T]: errs.append("문장 순서/누락 불일치")
for sids, clips in G:
    a, b = START[sids[0]], END[sids[-1]]
    # 누적 경계를 프레임으로 반올림해 오차가 쌓이지 않게 한다
    fb = [round((a + (b - a) * k / len(clips)) * FPS) for k in range(len(clips) + 1)]
    for k, c in enumerate(clips):
        f0, f1 = fb[k], fb[k + 1]; d = (f1 - f0) / FPS
        rngs = USE.get(c, [(0, CEND)]); p = pos.get(c, (0, rngs[0][0]))
        ri, ss = p
        while ri < len(rngs) and ss + d > rngs[ri][1] + 1e-6:
            ri += 1; ss = rngs[ri][0] if ri < len(rngs) else ss
        if ri >= len(rngs): errs.append(f"{c}: 쓸 구간 부족 ({sids[0]})"); ri = len(rngs) - 1
        pos[c] = (ri, ss + d); uses[c] = uses.get(c, 0) + 1
        cuts.append(dict(group=sids, clip=c, out_f0=f0, out_f1=f1, dur=round(d, 3), src_start=round(ss, 3),
                         src_end=round(ss + d, 3), src_f0=round(ss * FPS), src_f1=round((ss + d) * FPS), speed=1.0,
                         new=is_new(c), ref=ref(c), motion=motion(c)))
for i, x in enumerate(cuts):
    if not (2.0 - 1e-6 <= x["dur"] <= 3.05): errs.append(f"컷 길이 {x['dur']}초: {x['clip']} {x['group'][0]}")
    if i and cuts[i - 1]["clip"] == x["clip"]: errs.append(f"같은 클립 연속: {x['clip']} {x['group'][0]}")
for c, n in uses.items():
    if n > 3: errs.append(f"{c}: {n}컷 (최대 3)")
    if c not in V5 and c not in V6 and c not in OPENING: errs.append(f"{c}: 프롬프트 없음")
total = cuts[-1]["out_f1"] / FPS
if abs(total - END["S28a"]) > 0.05: errs.append("총 길이 불일치")

# 출력
json.dump(dict(fps=FPS, narration_sec=END["S28a"] - TAIL, video_sec=END["S28a"], cuts=cuts), open(EP / "plan/shot_list_v8.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
new_used = sorted({x["clip"] for x in cuts if x["new"]}); new_all = sorted(V6)
L = ["# 7편 문장별 컷 표 v8 (자동 생성: plan/plan_v8.py)", "",
     f"- **나레이션 실측:** {END['S28a'] - TAIL:.1f}초 (narr_timing.json). 영상은 끝에 {TAIL:.0f}초 여유를 더해 {END['S28a']:.1f}초.",
     f"- **컷:** {len(cuts)}개, 길이 {min(x['dur'] for x in cuts):.2f}~{max(x['dur'] for x in cuts):.2f}초, 모두 1.0배속.",
     f"- **클립:** {len(uses)}개 사용, 그중 신규·재생성 {len(new_used)}개.",
     f"- **점검:** {'통과' if not errs else '실패 ' + str(len(errs)) + '건'} (컷 2~3초, 같은 클립 연속 금지, 클립당 3컷 이하, 쓸 구간 안, 구간 겹침 없음, 문장 누락 없음).",
     "- **가정:** 신규 클립은 10초 전체를 쓸 수 있다고 가정했다. 생성 후 실제 쓸 구간을 USE에 넣고 다시 실행해야 확정된다.", ""]
L += [f"  - {e}" for e in errs]
unused = [c for c in new_all if c not in uses]
if unused: L += ["", f"**만들었지만 이 계획에서 안 쓰는 신규 클립(도입 컷 길이 결정에 따라 사용):** {', '.join(unused)}"]
L += ["", "## 문장별", "", "| 문장 | 시작~끝 | 초 | 한국어 | 컷: 클립[소스 초] | 기준 그림 | 화면 변화 |", "|---|---|---|---|---|---|---|"]
for sid in seq:
    a, b = START[sid], END[sid]
    cs = [x for x in cuts if x["out_f0"] / FPS < b - 1e-6 and x["out_f1"] / FPS > a + 1e-6]
    cl = "<br>".join(f"{'**' if x['new'] else ''}{x['clip']}{'**' if x['new'] else ''}[{x['src_start']:.1f}–{x['src_end']:.1f}]" for x in cs)
    rf = "<br>".join(x["ref"] for x in cs); mv = "<br>".join(x["motion"][:70] for x in cs)
    L.append(f"| {sid} | {a:.1f}–{b:.1f} | {b-a:.1f} | {KO[sid]} | {cl} | {rf} | {mv} |")
L += ["", "## 클립별 사용", "", "| 클립 | 컷 수 | 소스 구간 |", "|---|---|---|"]
for c in sorted(uses):
    r = ", ".join(f"{x['src_start']:.1f}–{x['src_end']:.1f}" for x in cuts if x["clip"] == c)
    L.append(f"| {'**'+c+'**' if is_new(c) else c} | {uses[c]} | {r} |")
(EP / "plan/shot_table_v8.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(len(cuts), "cuts", len(uses), "clips", "errors:", errs, "unused new:", unused)
