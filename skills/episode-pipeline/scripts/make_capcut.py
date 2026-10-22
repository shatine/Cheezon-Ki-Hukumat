"""캡컷 드래프트 만들기. 실제 캡컷 드래프트(channel.json capcut.template_draft)를 틀로 삼아 소재·세그먼트 구조를 그대로 복사한다.
트랙: 장면 영상(work/<장면>_fit.mp4) / 자막 / 모션그래픽 글자 / 나레이션(문장별 wav). 나레이션 없는 장면은 비워 둔다.
결과 폴더: 캡컷 프로젝트 폴더/<slug>_<에피소드>. 캡컷을 끈 상태에서 실행. render_episode.py 를 먼저 돌려야 한다."""
import copy, json, subprocess, time, uuid
from pathlib import Path
from kit import HERE, CH, NAME, LEAD, GAP, load

C = CH["capcut"]
ROOT = Path(C["root"])
TEMPLATE = ROOT / C["template_draft"] / "draft_content.json"
META_TEMPLATE = ROOT / C.get("meta_template_draft", C["template_draft"]) / "draft_meta_info.json"
OUT = ROOT / NAME
SKIP_REFS = {"transitions", "effects"}  # 틀의 전환 효과·글자 효과는 가져오지 않는다
MG = load("scenes.json").get("mg", [])

us = lambda s: int(round(s * 1_000_000))
uid = lambda: str(uuid.uuid4()).upper()


def wrap(t, maxc=42):
    """긴 자막은 여러 줄로 나눈다(한 줄이면 화면 양옆이 잘림)."""
    n = -(-len(t) // maxc)
    if n <= 1 or " " not in t:
        return t
    lines, target = [""], len(t) / n
    for w in t.split(" "):
        if lines[-1] and len(lines[-1]) + 1 + len(w) > target + 6 and len(lines) < n:
            lines.append(w)
        else:
            lines[-1] = (lines[-1] + " " + w).strip()
    return "\n".join(lines)


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height",
                        "-of", "json", str(p)], capture_output=True, text=True)
    j = json.loads(r.stdout)
    st = next((s for s in j.get("streams", []) if "width" in s), {})
    return float(j["format"]["duration"]), st.get("width", 0), st.get("height", 0)


T = json.loads(TEMPLATE.read_text(encoding="utf-8"))
where = {}
for k, v in T["materials"].items():
    if isinstance(v, list):
        for x in v:
            if isinstance(x, dict) and "id" in x:
                where[x["id"]] = (k, x)
seg_sample = {t["type"]: t["segments"][0] for t in T["tracks"] if t["segments"]}
track_sample = {t["type"]: {k: v for k, v in t.items() if k != "segments"} for t in T["tracks"]}

draft = {k: copy.deepcopy(v) for k, v in T.items() if k not in ("materials", "tracks")}
draft["id"] = uid()
mats = {k: ([] if isinstance(v, list) else copy.deepcopy(v)) for k, v in T["materials"].items()}


def make_seg(kind, material_id, start, dur, src_start=0.0, render_index=0, track_index=0):
    s = copy.deepcopy(seg_sample[kind])
    s["id"] = uid()
    s["material_id"] = material_id
    s["target_timerange"] = {"start": us(start), "duration": us(dur)}
    if s.get("source_timerange") is not None:
        s["source_timerange"] = {"start": us(src_start), "duration": us(dur)}
    refs = []
    for r in s["extra_material_refs"]:
        if r not in where or where[r][0] in SKIP_REFS:
            continue
        lst, obj = where[r]
        o = copy.deepcopy(obj)
        o["id"] = uid()
        if lst == "speeds":
            o["speed"] = 1.0
        mats[lst].append(o)
        refs.append(o["id"])
    s["extra_material_refs"] = refs
    s["speed"] = 1.0
    s["render_index"] = render_index
    s["track_render_index"] = track_index
    s["keyframe_refs"] = []
    s["common_keyframes"] = []
    return s


def video_material(p):
    d, w, h = probe(p)
    m = copy.deepcopy(next(x for x in T["materials"]["videos"] if x.get("type") == "video"))
    m.update(id=uid(), path=p.as_posix(), material_name=p.name, duration=us(d), width=w, height=h,
             has_audio=True, local_material_id=str(uuid.uuid4()), unique_id=uuid.uuid4().hex)
    mats["videos"].append(m)
    return m["id"], d


def audio_material(p):
    d, _, _ = probe(p)
    m = copy.deepcopy(T["materials"]["audios"][0])
    m.update(id=uid(), name=p.name, path=p.as_posix(), duration=us(d), music_id=str(uuid.uuid4()),
             local_material_id=str(uuid.uuid4()), unique_id=uuid.uuid4().hex, wave_points=[])
    mats["audios"].append(m)
    return m["id"], d


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
             line_max_width=0.82, alignment=1)
    mats["texts"].append(m)
    return m["id"]


meta = load("tts_meta.json", {})
plan = load("plan.json")
vtrack, strack, mtrack, atrack = [], [], [], []
t0 = 0.0
for p in plan:
    sid, D = p["id"], p["len"]
    mid, d = video_material(HERE / "work" / f"{sid}_fit.mp4")
    seg = make_seg("video", mid, t0, min(D, d), 0.0, 0, 0)
    seg["volume"] = 1.0
    vtrack.append(seg)
    t = LEAD
    for k, x in enumerate(meta.get(sid, [])):
        amid, ad = audio_material(HERE / "tts" / x["wav"])
        atrack.append(make_seg("audio", amid, t0 + t, ad, 0.0, 0, 3))
        tid = text_material(wrap(x["text"]), 6, [1, 1, 1], 0.06)
        s = make_seg("text", tid, t0 + t, x["dur"], render_index=14000 + len(strack), track_index=1)
        s["clip"]["transform"] = {"x": 0.0, "y": -0.78}
        strack.append(s)
        for ms, i, word in MG:
            if ms == sid and i == k:
                gid = text_material(word, 13, [0.94, 0.78, 0.28], 0.08)
                g = make_seg("text", gid, t0 + t, x["dur"] + 0.4, render_index=15000 + len(mtrack), track_index=2)
                g["clip"]["transform"] = {"x": 0.0, "y": 0.62}
                mtrack.append(g)
        t += x["dur"] + GAP
    t0 += D

tracks = []
for kind, segs, name in (("video", vtrack, "scenes"), ("text", strack, "subtitles"), ("text", mtrack, "motion_text"),
                         ("audio", atrack, "narration")):
    tr = copy.deepcopy(track_sample[kind])
    tr.update(id=uid(), name=name, is_default_name=False, segments=segs)
    tracks.append(tr)
draft["tracks"] = tracks
draft["materials"] = mats
draft["duration"] = us(t0)
draft["name"] = ""
now = int(time.time() * 1_000_000)
draft["create_time"] = draft["update_time"] = 0

# 참조 무결성 확인
ids = {x["id"] for v in mats.values() if isinstance(v, list) for x in v if isinstance(x, dict) and "id" in x}
broken = [r for tr in tracks for s in tr["segments"] for r in [s["material_id"], *s["extra_material_refs"]] if r not in ids]
assert not broken, broken[:5]

OUT.mkdir(exist_ok=True)
(OUT / "draft_content.json").write_text(json.dumps(draft, ensure_ascii=False), encoding="utf-8")
m = json.loads(META_TEMPLATE.read_text(encoding="utf-8"))
size = sum(Path(x["path"]).stat().st_size for x in mats["videos"] + mats["audios"])
m.update(draft_fold_path=OUT.as_posix(), draft_id=uid(), draft_name=NAME, draft_cover="",
         draft_root_path=str(ROOT), tm_draft_create=now, tm_draft_modified=now, tm_duration=us(t0),
         draft_timeline_materials_size_=size)
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
print("tracks", [(tr["type"], len(tr["segments"])) for tr in tracks], "duration", round(t0, 1), "->", OUT)
