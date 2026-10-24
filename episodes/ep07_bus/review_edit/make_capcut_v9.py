"""EP7 v9 캡컷 검수 드래프트 (6편 make_capcut06.py 방식). 캡컷을 끈 상태에서, edit_v9_upload.py를 먼저 돌린 뒤 실행.
트랙: 컷 영상 out/v9_up_seg/NNN.mp4 104개 / 힌디어 자막(out/v9_upload_subs_hi.srt) / 한국어 자막(narr_timing.json ko) / 나레이션 / 배경음.
힌디어는 업로드본과 같은 위치(아래), 한국어 검수 자막은 그 아래 노란색. 결과: 캡컷 프로젝트 폴더/cheezon_bus_ep07_v9"""
import copy, json, re, subprocess, time, uuid
from pathlib import Path
HERE = Path(__file__).resolve().parent; BUS = HERE.parent
EP = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes")
CH = json.load(open(EP / "05_morbi_dam_bridge" / "channel.json", encoding="utf-8"))
NAME = "cheezon_bus_ep07_v9"
BGM = EP / "05_morbi_dam_bridge" / "music" / "bgm.mp3"
FPS = 30
PL = json.load(open(BUS / "plan" / "shot_list_v9.json", encoding="utf-8")); cuts = PL["cuts"]; T0 = cuts[-1]["out_f1"] / FPS
NT = json.load(open(HERE / "narr_timing.json", encoding="utf-8"))

C = CH["capcut"]; ROOT = Path(C["root"])
TEMPLATE = ROOT / C["template_draft"] / "draft_content.json"
META_TEMPLATE = ROOT / C.get("meta_template_draft", C["template_draft"]) / "draft_meta_info.json"
OUT = ROOT / NAME
SKIP_REFS = {"transitions", "effects"}
us = lambda s: int(round(s * 1_000_000))
uid = lambda: str(uuid.uuid4()).upper()


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height", "-of", "json", str(p)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout); st = next((s for s in j.get("streams", []) if "width" in s), {})
    return float(j["format"]["duration"]), st.get("width", 0), st.get("height", 0)


T = json.loads(TEMPLATE.read_text(encoding="utf-8"))
where = {}
for k, v in T["materials"].items():
    if isinstance(v, list):
        for x in v:
            if isinstance(x, dict) and "id" in x: where[x["id"]] = (k, x)
seg_sample = {t["type"]: t["segments"][0] for t in T["tracks"] if t["segments"]}
track_sample = {t["type"]: {k: v for k, v in t.items() if k != "segments"} for t in T["tracks"]}
draft = {k: copy.deepcopy(v) for k, v in T.items() if k not in ("materials", "tracks")}
draft["id"] = uid()
mats = {k: ([] if isinstance(v, list) else copy.deepcopy(v)) for k, v in T["materials"].items()}


def make_seg(kind, material_id, start, dur, src_start=0.0, render_index=0, track_index=0):
    s = copy.deepcopy(seg_sample[kind])
    s["id"] = uid(); s["material_id"] = material_id
    s["target_timerange"] = {"start": us(start), "duration": us(dur)}
    if s.get("source_timerange") is not None: s["source_timerange"] = {"start": us(src_start), "duration": us(dur)}
    refs = []
    for r in s["extra_material_refs"]:
        if r not in where or where[r][0] in SKIP_REFS: continue
        lst, obj = where[r]; o = copy.deepcopy(obj); o["id"] = uid()
        if lst == "material_animations":  # 틀(0825) 자막의 "스파클 러브" 하트 애니메이션이 복제되지 않게 비운다
            o["animations"] = []
        if lst == "speeds": o["speed"] = 1.0
        mats[lst].append(o); refs.append(o["id"])
    s["extra_material_refs"] = refs; s["speed"] = 1.0
    s["render_index"] = render_index; s["track_render_index"] = track_index
    s["keyframe_refs"] = []; s["common_keyframes"] = []
    return s


def video_material(p):
    d, w, h = probe(p)
    m = copy.deepcopy(next(x for x in T["materials"]["videos"] if x.get("type") == "video"))
    m.update(id=uid(), path=p.as_posix(), material_name=p.name, duration=us(d), width=w, height=h,
             has_audio=False, local_material_id=str(uuid.uuid4()), unique_id=uuid.uuid4().hex)
    mats["videos"].append(m); return m["id"], d


def audio_material(p):
    d, _, _ = probe(p)
    m = copy.deepcopy(T["materials"]["audios"][0])
    m.update(id=uid(), name=p.name, path=p.as_posix(), duration=us(d), music_id=str(uuid.uuid4()),
             local_material_id=str(uuid.uuid4()), unique_id=uuid.uuid4().hex, wave_points=[])
    mats["audios"].append(m); return m["id"], d


def text_material(txt, size, color, stroke_w):
    m = copy.deepcopy(T["materials"]["texts"][0])
    style = {"fill": {"content": {"render_type": "solid", "solid": {"color": color}}},
             "strokes": [{"content": {"render_type": "solid", "solid": {"color": [0, 0, 0]}}, "width": stroke_w, "mode": 0}],
             "shadows": [{"diffuse": 0.05, "alpha": 0.6, "distance": 3.0, "angle": -45,
                          "content": {"render_type": "solid", "solid": {"color": [0, 0, 0]}},
                          "thickness_projection_enable": False, "thickness_projection_angle": -45, "thickness_projection_distance": 0}],
             "size": size, "useLetterColor": True, "range": [0, len(txt.encode("utf-16-le")) // 2]}
    hexc = "#" + "".join(f"{int(c * 255):02x}" for c in color)
    m.update(id=uid(), content=json.dumps({"text": txt, "styles": [style]}, ensure_ascii=False),
             text_color=hexc, font_size=float(size), font_path="", font_resource_id="", font_id="", font_name="",
             border_color="#000000", border_width=stroke_w, effect_id="", text_preset_resource_id="",
             line_max_width=0.92, alignment=1)
    mats["texts"].append(m); return m["id"]


def read_srt(p):
    def s(x): h, m, r = x.split(":"); a, b = r.split(","); return int(h) * 3600 + int(m) * 60 + int(a) + int(b) / 1000
    out = []
    for b in p.read_text(encoding="utf-8").strip().split("\n\n"):
        L = b.split("\n"); a, e = L[1].split(" --> "); out.append((s(a), s(e), " ".join(L[2:])))
    return out


# 영상: 업로드본과 같은 컷 파일(효과·반전·흐림 적용됨)
segs = sorted((BUS / "out" / "v9_up_seg").glob("[0-9][0-9][0-9].mp4"))
assert len(segs) == len(cuts), (len(segs), len(cuts))
vtrack, htrack, ktrack, atrack, btrack = [], [], [], [], []
for c, f in zip(cuts, segs):
    mid, d = video_material(f)
    s = make_seg("video", mid, c["out_f0"] / FPS, (c["out_f1"] - c["out_f0"]) / FPS, 0.0, 0, 0); s["volume"] = 0.0
    vtrack.append(s)
# 힌디어 자막(업로드본과 같은 나눔·시간)
for a, b, txt in read_srt(BUS / "out" / "v9_upload_subs_hi.srt"):
    tid = text_material(txt, 6, [1, 1, 1], 0.06)
    s = make_seg("text", tid, a, b - a, render_index=14000 + len(htrack), track_index=1)
    s["clip"]["transform"] = {"x": 0.0, "y": -0.70}; htrack.append(s)
# 한국어 검수 자막(문장 단위, edit_v9.py와 같은 시간)
for i, x in enumerate(NT):
    nxt = NT[i + 1]["start"] if i + 1 < len(NT) else T0
    a, b = x["start"], min(nxt, x["end"] + 0.4)
    tid = text_material(x["ko"], 5, [1.0, 0.90, 0.0], 0.06)
    s = make_seg("text", tid, a, b - a, render_index=15000 + len(ktrack), track_index=2)
    s["clip"]["transform"] = {"x": 0.0, "y": -0.88}; ktrack.append(s)
amid, ad = audio_material(HERE / "narration_hi.wav")
atrack.append(make_seg("audio", amid, 0.0, ad, 0.0, 0, 3))
bt = 0.0
while bt < T0 - 0.05:
    bid, bd = audio_material(BGM); L = min(bd, T0 - bt)
    s = make_seg("audio", bid, bt, L, 0.0, 0, 4); s["volume"] = 0.0225
    btrack.append(s); bt += L

tracks = []
for kind, sg, name in (("video", vtrack, "scenes"), ("text", htrack, "subs_hi"), ("text", ktrack, "subs_ko_review"),
                       ("audio", atrack, "narration_hi"), ("audio", btrack, "music")):
    tr = copy.deepcopy(track_sample[kind]); tr.update(id=uid(), name=name, is_default_name=False, segments=sg); tracks.append(tr)
draft["tracks"] = tracks; draft["materials"] = mats; draft["duration"] = us(T0); draft["name"] = ""
now = int(time.time() * 1_000_000); draft["create_time"] = draft["update_time"] = 0
ids = {x["id"] for v in mats.values() if isinstance(v, list) for x in v if isinstance(x, dict) and "id" in x}
broken = [r for tr in tracks for s in tr["segments"] for r in [s["material_id"], *s["extra_material_refs"]] if r not in ids]
assert not broken, broken[:5]

OUT.mkdir(exist_ok=True)
(OUT / "draft_content.json").write_text(json.dumps(draft, ensure_ascii=False), encoding="utf-8")
m = json.loads(META_TEMPLATE.read_text(encoding="utf-8"))
size = sum(Path(x["path"]).stat().st_size for x in mats["videos"] + mats["audios"])
m.update(draft_fold_path=OUT.as_posix(), draft_id=uid(), draft_name=NAME, draft_cover="", draft_root_path=str(ROOT),
         tm_draft_create=now, tm_draft_modified=now, tm_duration=us(T0), draft_timeline_materials_size_=size)
def entry(x):
    return {"ai_group_type": "", "create_time": now // 1_000_000, "duration": x["duration"], "enter_from": 0,
            "extra_info": Path(x["path"]).name, "file_Path": x["path"], "height": x.get("height", 0), "id": str(uuid.uuid4()),
            "import_time": now // 1_000_000, "import_time_ms": now, "item_source": 1, "material_color_tag": "", "md5": "",
            "metetype": "video" if x["type"] == "video" else "music",
            "roughcut_time_range": {"duration": x["duration"], "start": 0}, "sub_time_range": {"duration": -1, "start": -1},
            "type": 0, "width": x.get("width", 0)}
m["draft_materials"] = [{"type": 0, "value": [entry(x) for x in mats["videos"] + mats["audios"]]}] + \
    [{"type": t, "value": []} for t in (1, 2, 3, 6, 7, 8)]
(OUT / "draft_meta_info.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
print("tracks", [(tr["name"], len(tr["segments"])) for tr in tracks], "duration", round(T0, 1), "->", OUT)
