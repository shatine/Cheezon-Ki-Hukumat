"""[8편 체납 철교 plan_v2: Muse v1 클라우드 검수(2026-10-26) 실측 쓸 구간 반영] SEG·VID·IMG만 8편으로 채움.
규칙(cheezon-production): 도입 0~30초는 긴 영상 3~5개, 3D 원리 문장은 영상, 나머지 영상은 10~20%(무빙·동작),
그 외 이미지+효과는 2~4초마다 바꾸고 4.5초를 넘기지 않는다. 영상은 쓸 구간 최대 사용, 감속·정지·반복 금지.
입력: review_edit/narr_timing.json(실측 334.3초). 출력: plan/shot_list_v2.json, plan/shot_table_v2.md
SEG = (시작 초, 소스 id, 'v' 영상 / 'i' 이미지, 소스 시작 초, 옵션). 끝 = 다음 행 시작(마지막은 나레이션 끝 + TAIL).
쓸 구간은 video/review_clips_v1.md 실측. 다시 만들 4개(V09 V16a V16b V20b)는 아직 0~CEND."""
import json
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
FPS, TAIL, CEND = 30, 1.0, 9.95
IMG_MAX = 4.5
T = json.load(open(EP / "review_edit/narr_timing.json", encoding="utf-8"))
VEND = T[-1]["end"] + TAIL
# 영상 소스: PC 경로(CB = episodes\08_chenab_bridge 기준)와 쓸 수 있는 구간. 'o…' = 도입, 'V…' = 3D 원리, 'v…' = 무빙·동작
USE = {"o01": (0, 10.0), "o02": (0, 10.0), "V02": (0.7, 10.0), "o03": (4.7, 10.0), "V04": (0, 10.0), "V05": (1.5, 10.0),
       "V06": (0, 10.0), "V07a": (0, 8.6), "V07b": (1.0, 8.6), "V10a": (0, 10.0), "V10b": (0, 6.0), "v12": (0, 10.0),
       "V13": (0, 10.0), "v14": (0, 10.0), "V14": (0, 10.0), "V17": (0, 8.1), "V18": (4.75, 10.0), "V22": (0, 10.0), "V20a": (0, 8.0), "v23": (0, 10.0)}
FILE = {"v14": "clips_v1/v14_real.mp4"}   # 윈도우는 v14와 V14를 같은 이름으로 본다
def V(i, role): return (FILE.get(i, f"clips_v1/{i}.mp4"), [USE.get(i, (0, CEND))], role)
VID = {
 "o01": V("o01", "도입"), "o02": V("o02", "도입"), "V02": V("V02", "원리"), "o03": V("o03", "도입"),
 "V04": V("V04", "원리"), "V05": V("V05", "원리"), "V06": V("V06", "원리"), "V07a": V("V07a", "원리"), "V07b": V("V07b", "원리"),
 "V09": V("V09", "원리"), "V10a": V("V10a", "원리"), "V10b": V("V10b", "원리"), "v12": V("v12", "무빙"), "V13": V("V13", "원리"),
 "v14": V("v14", "동작"), "V14": V("V14", "원리"), "V16a": V("V16a", "원리"), "V16b": V("V16b", "원리"), "V17": V("V17", "원리"),
 "V18": V("V18", "원리"), "V20a": V("V20a", "원리"), "V20b": V("V20b", "원리"), "V22": V("V22", "원리"), "v23": V("v23", "무빙"),
}
# 이미지 소스: CB\img\v1_{id}_{n}.png (images/picks_v1.md에서 고른 번호로 고친다)
PICK_N = dict(i03b=2, i03b2=2, i03c2=2, i03c3=3, i05a=2, i06a=2, i06c=2, i07a=3, i08c=2, i11b2=3, i15c=2, i15c2=4,
              i16a=3, i18a=3, i19a=5, i19a2=3, i19b2=2, i20a=2, i21b=2)
IMG = {k: f"v1_{k}_{PICK_N.get(k, 1)}" for k in [
 "i03a", "i03b", "i03b2", "i03c", "i03c2", "i03c3", "i04", "i05a", "i05b", "i06a", "i06c", "i06c2", "i07a", "i07e",
 "i08a", "i08b", "i08c", "i08c2", "i09a", "i10d", "i10d2", "i11a", "i11b", "i11b2", "i11c", "i12a", "i12b", "i13a",
 "i15a", "i15b", "i15c", "i15c2", "i15c3", "i16a", "i17a", "i18a", "i19a", "i19a2", "i19a3", "i19b", "i19b2", "i19c", "i19c2",
 "i20a", "i21", "i21b", "i23b", "i24"]}
OPT_NOTE = {"hflip": "좌우 반전", "bright": "밝기 점진 보정", "blur_plate": "로고·번호판 흐림", "haze": "아지랑이",
            "recall": "의도적 회수(같은 샷의 겹치지 않는 뒷구간)"}
SEG = [
 (0.0, "o01", "v", 0, ""), (7.08, "o02", "v", 0, ""), (15.75, "V02", "v", 0.72, "x5 표기(쿠툽 옆)"), (25.0, "o03", "v", 4.74, ""),   # ---- 도입 30초
 (30.22, "i03a", "i", 0, ""), (32.92, "i03b", "i", 0, ""), (35.2, "i03b2", "i", 0, ""),
 (37.86, "i03c", "i", 0, ""), (40.8, "i03c2", "i", 0, ""), (43.7, "i03c3", "i", 0, ""),
 (47.33, "i04", "i", 0, ""), (51.3, "V04", "v", 0, ""),
 (60.06, "i05a", "i", 0, ""), (64.04, "i05b", "i", 0, ""), (67.89, "V05", "v", 1.5, ""),
 (74.17, "i06a", "i", 0, ""), (76.86, "V06", "v", 0, ""), (86.28, "i06c", "i", 0, ""), (88.6, "i06c2", "i", 0, ""),
 (91.72, "i07a", "i", 0, ""), (93.92, "V07a", "v", 0, ""), (102.13, "V07b", "v", 1.0, ""), (108.09, "i07e", "i", 0, ""),
 (112.39, "i08a", "i", 0, ""), (114.9, "i08b", "i", 0, ""), (117.61, "i08c", "i", 0, ""), (120.0, "i08c2", "i", 0, ""),
 (122.33, "i09a", "i", 0, ""), (125.46, "V09", "v", 0, ""),
 (131.25, "V10a", "v", 0, ""), (141.0, "V10b", "v", 0, ""), (146.89, "i10d", "i", 0, ""), (149.3, "i10d2", "i", 0, ""),
 (152.38, "i11a", "i", 0, ""), (156.22, "i11b", "i", 0, ""), (159.6, "i11b2", "i", 0, ""), (163.41, "i11c", "i", 0, ""),
 (167.76, "i12a", "i", 0, ""), (170.23, "i12b", "i", 0, ""), (172.9, "v12", "v", 0, "bright"),
 (181.54, "i13a", "i", 0, ""), (185.8, "V13", "v", 0, ""),
 (193.41, "v14", "v", 0, ""), (198.98, "V14", "v", 0, ""),
 (208.9, "i15a", "i", 0, ""), (212.47, "i15b", "i", 0, ""), (215.6, "i15c", "i", 0, ""), (219.0, "i15c2", "i", 0, ""), (222.0, "i15c3", "i", 0, ""),
 (224.98, "i16a", "i", 0, ""), (226.95, "V16a", "v", 0, ""), (236.85, "V16b", "v", 0, ""),
 (241.76, "i17a", "i", 0, ""), (244.42, "V17", "v", 0, ""),
 (252.53, "i18a", "i", 0, ""), (257.03, "V18", "v", 4.75, ""),
 (262.25, "i19a", "i", 0, ""), (265.8, "i19a2", "i", 0, "blur_plate"), (269.3, "i19a3", "i", 0, ""),
 (273.2, "i19b", "i", 0, ""), (276.5, "i19b2", "i", 0, ""), (280.06, "i19c", "i", 0, ""), (283.5, "i19c2", "i", 0, ""),
 (287.74, "i20a", "i", 0, "blur_plate"), (289.44, "V20a", "v", 0, ""), (296.41, "V20b", "v", 0, ""),
 (303.86, "i21", "i", 0, ""), (305.74, "i21b", "i", 0, ""),
 (308.5, "V22", "v", 0, ""), (318.4, "v23", "v", 0, ""),
 (328.3, "i23b", "i", 0, "bright"), (331.2, "i24", "i", 0, "bright"),
]
PRINCIPLE_SENT = {"S02c", "S04c", "S05c", "S06b", "S07c", "S07d", "S09b", "S10b", "S10c", "S13c", "S14c", "S16c", "S16d", "S17b",
                  "S18c", "S20c", "S20d", "S22a", "S22b"}
OPENING_END = 30.22

cuts, errs, used = [], [], {}
for i, (st, k, kind, ss, opt) in enumerate(SEG):
    en = SEG[i + 1][0] if i + 1 < len(SEG) else VEND
    f0, f1 = round(st * FPS), round(en * FPS); d = (f1 - f0) / FPS
    if d <= 0: errs.append(f"{st}: 길이 0 이하")
    c = dict(start=round(f0 / FPS, 3), end=round(f1 / FPS, 3), out_f0=f0, out_f1=f1, dur=round(d, 3), src=k, kind=kind, opt=opt)
    if kind == "v":
        if k not in VID: errs.append(f"{k}: 영상 소스 없음"); continue
        rngs = VID[k][1]; se = ss + d
        if not any(a - 1e-6 <= ss and se <= b + 1e-6 for a, b in rngs): errs.append(f"{k} {ss:.2f}~{se:.2f}: 쓸 구간 {rngs} 밖")
        for a, b in used.get(k, []):
            if ss < b - 1e-6 and se > a + 1e-6: errs.append(f"{k}: 소스 구간 겹침 {a:.2f}~{b:.2f} / {ss:.2f}~{se:.2f}")
        used.setdefault(k, []).append((ss, se)); c.update(src_start=round(ss, 3), src_end=round(se, 3), file=VID[k][0], role=VID[k][2])
    else:
        if k not in IMG: errs.append(f"{k}: 이미지 없음"); continue
        if k in used: errs.append(f"{k}: 같은 이미지 재사용")
        if d > IMG_MAX + 1e-6: errs.append(f"{k}: 이미지 {d:.2f}초 > {IMG_MAX}초")
        used[k] = [(0, d)]; c.update(file=f"img/{IMG[k]}.png", role="고정+효과")
    cuts.append(c)
if abs(cuts[-1]["end"] - VEND) > 0.04: errs.append("총 길이 불일치")
unused = sorted(set(VID) - {c["src"] for c in cuts if c["kind"] == "v"}) + sorted(set(IMG) - {c["src"] for c in cuts if c["kind"] == "i"})
if unused: errs.append(f"계획에 안 쓰인 소스: {unused}")
# 원리 문장은 영상이어야 한다
for x in T:
    if x["id"] in PRINCIPLE_SENT:
        a, b = x["start"], x["end"]
        ov = [c for c in cuts if c["start"] < b and c["end"] > a]
        vsec = sum(min(b, c["end"]) - max(a, c["start"]) for c in ov if c["kind"] == "v")
        if vsec < 0.6 * (b - a): errs.append(f"{x['id']} 원리 문장인데 영상 {vsec:.1f}/{b-a:.1f}초")
# 도입 영상 수, 원리 외 영상 비율(10~20%)
op = [c for c in cuts if c["start"] < OPENING_END - 0.05]
if not (3 <= len(op) <= 5 and all(c["kind"] == "v" for c in op)): errs.append(f"도입 30초: 영상 3~5개여야 함 ({[(c['src'], c['kind']) for c in op]})")
rest = [c for c in cuts if c["start"] >= OPENING_END - 0.05 and not (c["kind"] == "v" and c["role"] == "원리")]
rest_t = sum(c["dur"] for c in rest); rest_v = sum(c["dur"] for c in rest if c["kind"] == "v"); share = rest_v / rest_t
if not 0.10 <= share <= 0.20: errs.append(f"원리 외 영상 비율 {share*100:.0f}% (10~20%)")
# 이미지 효과: 줌 인/아웃·이동 방향을 번갈아(연속 같은 방향 금지)
MOVES = ["in_c", "out_c", "in_l", "out_r", "in_r", "out_l"]; m = 0
for c in cuts:
    if c["kind"] == "i": c["effect"] = MOVES[m % len(MOVES)]; m += 1
json.dump(dict(fps=FPS, narration_sec=T[-1]["end"], video_sec=VEND, cuts=cuts), open(EP / "plan/shot_list_v2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

vt = sum(c["dur"] for c in cuts if c["kind"] == "v"); it = sum(c["dur"] for c in cuts if c["kind"] == "i")
pv = sum(c["dur"] for c in cuts if c["kind"] == "v" and c["role"] == "원리")
L = ["# 8편 컷 표 v2 (자동 생성: plan/plan_v2.py)", "",
     f"- **나레이션:** {T[-1]['end']:.1f}초. 영상은 끝에 {TAIL:.0f}초 여유를 더해 {VEND:.1f}초.",
     f"- **컷:** {len(cuts)}개.",
     f"  - 영상: {sum(c['kind']=='v' for c in cuts)}컷, {vt:.1f}초 ({vt/VEND*100:.0f}%), 소스 {len({c['src'] for c in cuts if c['kind']=='v'})}개 (원리 {pv:.1f}초).",
     f"  - 이미지+효과: {sum(c['kind']=='i' for c in cuts)}컷, {it:.1f}초. 최장 {max(c['dur'] for c in cuts if c['kind']=='i'):.2f}초.",
     f"  - 도입 30초: 영상 {len(op)}개. 원리 외 영상 비율: {share*100:.1f}% ({rest_v:.1f}/{rest_t:.1f}초).",
     f"- **컷 길이:** {min(c['dur'] for c in cuts):.1f}~{max(c['dur'] for c in cuts):.1f}초.",
     f"- **점검:** {'통과' if not errs else '실패 ' + str(len(errs)) + '건'}.",
     "  - 쓸 구간 안, 소스 구간 겹침 없음, 이미지 재사용 없음, 이미지 4.5초 이하, 원리 문장은 영상, 도입 영상 3~5개, 원리 외 영상 10~20%, 총 길이 일치.", ""]
L += [f"  - {e}" for e in errs]
L += ["", "| 시간 | 초 | 문장 | 소스 | 종류 | 소스 구간 / 효과 | 옵션 |", "|---|---|---|---|---|---|---|"]
for c in cuts:
    sids = [x["id"] for x in T if x["start"] < c["end"] - 0.05 and x["end"] > c["start"] + 0.05]
    src = f"{c['src_start']:.2f}–{c['src_end']:.2f} ({c['role']})" if c["kind"] == "v" else c["effect"]
    L.append(f"| {c['start']:.1f}–{c['end']:.1f} | {c['dur']:.1f} | {' '.join(sids)} | {c['src']} | {'영상' if c['kind']=='v' else '이미지'} | {src} | {OPT_NOTE.get(c['opt'], '')} |")
(EP / "plan/shot_table_v2.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(len(cuts), "cuts; video", round(vt, 1), "s; image", round(it, 1), "s; non-principle video share", f"{share*100:.1f}%; errors:", errs)
