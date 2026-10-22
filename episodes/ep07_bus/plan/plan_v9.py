"""EP7 컷 계획 v9 (사용자 2026-10-22 규칙): 영상은 10초 중 쓸 수 있는 구간 최대 사용, 카메라 무빙·원리 장면=영상,
고정 장면=이미지+효과(편집), 도입 0~30초는 긴 자연스러운 영상. 컷 2~3초 규칙 폐지.
입력: review_edit/narr_timing.json(실측). 출력: plan/shot_list_v9.json, plan/shot_table_v9.md
SEG = (시작 초, 소스 id, 'v' 영상 / 'i' 이미지, 소스 시작 초, 옵션). 끝 = 다음 행 시작(마지막은 나레이션 끝 + TAIL)."""
import json
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
FPS, TAIL, CEND = 30, 1.0, 9.95
T = json.load(open(EP / "review_edit/narr_timing.json", encoding="utf-8"))
VEND = T[-1]["end"] + TAIL
# 영상 소스: PC 경로(BUS 기준)와 쓸 수 있는 구간
VID = {  # id: (파일, [(쓸 구간)], 무빙/원리)
 "o1": ("clips_v8/o1.mp4", [(0, 5.4)], "무빙"), "o2": ("clips_v8/o2.mp4", [(0, CEND)], "도입"),
 "PB": ("clips_v8/PB.mp4", [(0, CEND)], "무빙"), "s09z": ("clips_v8/s09z.mp4", [(0, CEND)], "원리"),
 "s03": ("clips_v5/s03.mp4", [(0, 6)], "무빙"), "s04a": ("clips_v5/s04a.mp4", [(0, CEND)], "도해"),
 "s04b": ("clips_v5/s04b.mp4", [(0, CEND)], "무빙"), "s06b": ("clips_v5/s06b.mp4", [(0, CEND)], "원리"),
 "s07b": ("clips_v5/s07b.mp4", [(0, CEND)], "원리"), "s08": ("clips_v5/s08.mp4", [(0, CEND)], "원리"),
 "s09": ("clips_v5/s09.mp4", [(0, CEND)], "원리"), "s10": ("clips_v5/s10.mp4", [(0, 7)], "무빙·원리"),
 "s11a": ("clips_v5/s11a.mp4", [(0, CEND)], "원리"), "s12": ("clips_v5/s12.mp4", [(0, CEND)], "원리"),
 "s14a": ("clips_v5/s14a.mp4", [(3, CEND)], "원리"), "s14b": ("clips_v5/s14b.mp4", [(3, CEND)], "원리"),
 "s15a": ("clips_v5/s15a.mp4", [(0, 2), (5, CEND)], "무빙·원리"), "s15b": ("clips_v5/s15b.mp4", [(0, 7)], "원리"),
 "s16a": ("clips_v5/s16a.mp4", [(0, CEND)], "원리"), "s17b": ("clips_v5/s17b.mp4", [(0, CEND)], "무빙"),
 "s19": ("clips_v5/s19.mp4", [(0, CEND)], "무빙"), "s24": ("clips_v5/s24.mp4", [(0, CEND)], "무빙"),
 "s26": ("clips_v5/s26.mp4", [(0, CEND)], "원리"), "s28": ("clips_v5/s28.mp4", [(4, CEND)], "무빙"),
}
# 이미지 소스: PC img3d 파일 (picks_v5.txt, picks_v7.md)
IMG = {"s02": "v5_s02_1", "s04c": "v5_s04c_1", "s05": "v5_s05_1", "s06a": "v5_s06a_2", "s07a": "v5_s07a_1",
       "s11b": "v5_s11b_1", "s13": "v5_s13_1", "M3": "v5_M3_1", "s16b": "v5_s16b_2", "s17a": "v5_s17a_2", "s18": "v5_s18_2",
       "s20": "v5_s20_1", "s21a": "v5_s21a_2", "s21b": "v5_s21b_2", "s22": "v5_s22_1", "s23": "v5_s23_2", "s25": "v5_s25_2",
       "s27": "v5_s27_2"}
for k in ["s06z_1", "s08b_1", "s08c_2", "s09b_1", "s10b_1", "s11c_2", "s12b_1", "s12c_1", "s13b_1", "s14c_2", "s15c_1", "s15d_1",
          "s16d_2", "s18b_2", "s20b_1", "s22b_1", "s22c_1", "s23b_1", "s23c_1", "s23d_2", "s23e_1", "s24b_1", "s24c_1", "s24d_1",
          "s24e_3", "s26b_1", "s26c_2", "s26d_1", "s27b_1"]:
    IMG[k.rsplit("_", 1)[0]] = "v7_" + k
OPT_NOTE = {"hflip": "좌우 반전(o1과 버스 방향 맞춤)", "bright": "5.5초 이후 밝기 점진 보정", "blur_plate": "그릴·번호판 흐림",
            "haze": "열 아지랑이 효과", "recall": "의도적 회수(같은 샷의 겹치지 않는 뒷구간)"}
SEG = [
 (0.0, "o1", "v", 0, ""), (5.4, "o2", "v", 0, "hflip"), (10.5, "PB", "v", 0, "bright"), (20.43, "s03", "v", 0, ""),
 (23.0, "s04a", "v", 0, ""),                                                     # ---- 도입 30초 끝
 (30.0, "s04b", "v", 0, ""), (35.7, "s04c", "i", 0, ""), (40.4, "s02", "i", 0, ""),
 (44.9, "s06z", "i", 0, "haze"), (50.9, "s06a", "i", 0, ""), (55.2, "s06b", "v", 0, ""),
 (63.1, "s07a", "i", 0, ""), (67.4, "s07b", "v", 0, ""),
 (76.0, "s08b", "i", 0, ""), (78.9, "s08", "v", 0, ""), (87.1, "s08c", "i", 0, ""),
 (90.7, "s09", "v", 0, ""), (98.7, "s09b", "i", 0, ""), (100.6, "s09z", "v", 0, ""),
 (110.5, "s10b", "i", 0, ""), (114.4, "s10", "v", 0, ""),
 (121.4, "s11c", "i", 0, ""), (125.3, "s11a", "v", 0, ""), (135.2, "s11b", "i", 0, ""),
 (140.7, "s12", "v", 0, ""), (148.0, "s12b", "i", 0, ""), (153.0, "s12c", "i", 0, ""),
 (158.1, "s13b", "i", 0, ""), (163.7, "s13", "i", 0, ""),
 (170.1, "s14c", "i", 0, ""), (173.8, "s14a", "v", 3, ""), (180.75, "s14b", "v", 3, ""), (183.5, "M3", "i", 0, ""),
 (188.6, "s15c", "i", 0, ""), (191.6, "s15a", "v", 5, ""), (195.2, "s15b", "v", 0, ""), (202.2, "s15d", "i", 0, ""),
 (205.7, "s16a", "v", 0, ""), (215.6, "s16d", "i", 0, ""),
 (222.5, "s17a", "i", 0, ""), (226.7, "s17b", "v", 0, ""), (234.7, "s18b", "i", 0, ""), (237.9, "s16b", "i", 0, ""),
 (244.8, "s18", "i", 0, ""), (250.9, "s05", "i", 0, ""),
 (253.5, "s19", "v", 0, ""),
 (259.9, "s20b", "i", 0, ""), (265.8, "s20", "i", 0, ""),
 (274.6, "s21a", "i", 0, ""), (280.1, "s21b", "i", 0, ""), (283.7, "s26b", "i", 0, ""),
 (289.2, "s22", "i", 0, ""), (293.6, "s22b", "i", 0, ""), (299.0, "s22c", "i", 0, ""),
 (304.7, "s23b", "i", 0, "blur_plate"), (308.9, "s23", "i", 0, ""), (314.3, "s23e", "i", 0, "blur_plate"),
 (319.8, "s23c", "i", 0, ""), (323.8, "s23d", "i", 0, ""),
 (332.4, "s24", "v", 0, ""), (340.1, "s24b", "i", 0, ""), (346.1, "s24d", "i", 0, ""), (352.0, "s24c", "i", 0, ""),
 (355.9, "s24e", "i", 0, ""),
 (360.9, "s25", "i", 0, ""),
 (364.9, "s19", "v", 6.4, "recall"), (367.4, "s26c", "i", 0, ""), (375.0, "s04b", "v", 5.7, "recall"),
 (378.2, "s26d", "i", 0, ""), (382.2, "s26", "v", 0, ""),
 (390.7, "s27", "i", 0, ""), (394.5, "s27b", "i", 0, ""),
 (398.9, "s28", "v", 4, ""),
]
PRINCIPLE_SENT = {"S06d", "S06e", "S07c", "S08c", "S09b", "S09d", "S10c", "S11b", "S11c", "S12a", "S14c", "S15c", "S16c", "S26e"}

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
        used[k] = [(0, d)]; c.update(file=f"img3d/{IMG[k]}.png", role="고정+효과")
    cuts.append(c)
if abs(cuts[-1]["end"] - VEND) > 0.04: errs.append("총 길이 불일치")
# 원리 문장은 영상이어야 한다
for x in T:
    if x["id"] in PRINCIPLE_SENT:
        a, b = x["start"], x["end"]
        ov = [c for c in cuts if c["start"] < b and c["end"] > a]
        vsec = sum(min(b, c["end"]) - max(a, c["start"]) for c in ov if c["kind"] == "v")
        if vsec < 0.6 * (b - a): errs.append(f"{x['id']} 원리 문장인데 영상 {vsec:.1f}/{b-a:.1f}초")
# 이미지 효과: 줌 인/아웃·이동 방향을 번갈아(연속 같은 방향 금지)
MOVES = ["in_c", "out_c", "in_l", "out_r", "in_r", "out_l"]; m = 0
for c in cuts:
    if c["kind"] == "i": c["effect"] = MOVES[m % len(MOVES)]; m += 1
json.dump(dict(fps=FPS, narration_sec=T[-1]["end"], video_sec=VEND, cuts=cuts), open(EP / "plan/shot_list_v9.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

vt = sum(c["dur"] for c in cuts if c["kind"] == "v"); it = sum(c["dur"] for c in cuts if c["kind"] == "i")
long_i = [f"{c['src']} {c['dur']:.1f}초" for c in cuts if c["kind"] == "i" and c["dur"] > 7]
L = ["# 7편 컷 표 v9 (자동 생성: plan/plan_v9.py)", "",
     f"- **나레이션:** {T[-1]['end']:.1f}초. 영상은 끝에 {TAIL:.0f}초 여유를 더해 {VEND:.1f}초.",
     f"- **컷:** {len(cuts)}개.",
     f"  - 영상: {sum(c['kind']=='v' for c in cuts)}컷, {vt:.1f}초 ({vt/VEND*100:.0f}%), 소스 {len({c['src'] for c in cuts if c['kind']=='v'})}개.",
     f"  - 이미지+효과: {sum(c['kind']=='i' for c in cuts)}컷, {it:.1f}초.",
     f"- **컷 길이:** {min(c['dur'] for c in cuts):.1f}~{max(c['dur'] for c in cuts):.1f}초. 7초 넘는 이미지: {', '.join(long_i) or '없음'}.",
     f"- **점검:** {'통과' if not errs else '실패 ' + str(len(errs)) + '건'}.",
     "  - 쓸 구간 안, 소스 구간 겹침 없음, 이미지 재사용 없음, 원리 문장은 영상, 문장 누락 없음, 총 길이 일치.", ""]
L += [f"  - {e}" for e in errs]
L += ["", "| 시간 | 초 | 문장 | 소스 | 종류 | 소스 구간 / 효과 | 옵션 |", "|---|---|---|---|---|---|---|"]
for c in cuts:
    sids = [x["id"] for x in T if x["start"] < c["end"] - 0.05 and x["end"] > c["start"] + 0.05]
    src = f"{c['src_start']:.2f}–{c['src_end']:.2f} ({c['role']})" if c["kind"] == "v" else c["effect"]
    L.append(f"| {c['start']:.1f}–{c['end']:.1f} | {c['dur']:.1f} | {' '.join(sids)} | {c['src']} | {'영상' if c['kind']=='v' else '이미지'} | {src} | {OPT_NOTE.get(c['opt'], '')} |")
(EP / "plan/shot_table_v9.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(len(cuts), "cuts; video", round(vt, 1), "s; image", round(it, 1), "s; errors:", errs)
