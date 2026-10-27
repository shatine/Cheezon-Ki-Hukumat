# 9편 검수 준비: 실제 원본 크기 확인을 돕는 자동 측정과 대조표를 만든다.
# 사용: python3 cloud_review_v1.py <작업 폴더>   (그 뒤 git rm -r images/v1 && commit)
# 자동 측정(크기, 밝기, 이웃 컷 유사도)은 보조일 뿐이다. 모든 장을 원본 크기로 직접 본다.
import json, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
EP = HERE.parent
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "v1"

prompts = {p["id"]: p for p in json.load(open(HERE / "prompts_v1.json", encoding="utf-8"))}
# 마스터 뒤에 실제 JSON 컷 순서. 표의 프레임 열/서식에 의존하지 않는다.
order = [p["id"] for p in prompts.values() if p["kind"] == "master"]
plan = json.loads((EP / "plan" / "shot_list_v1.json").read_text(encoding="utf-8-sig"))
cut_order = list(dict.fromkeys(c["src"] for c in plan["cuts"]))
for cut in plan["cuts"]:
    if cut["src"] not in order:
        order.append(cut["src"])

def pid(name):  # v1_i03c3_3.png -> i03c3
    m = re.match(r"v1_(.+)_(\d+)\.png$", name)
    return m.group(1) if m else None

files = {}
for f in sorted(SRC.glob("*.png"), key=lambda p: (pid(p.name) or "", int(re.search(r"_(\d+)\.png$", p.name).group(1)) if pid(p.name) else 0)):
    i = pid(f.name)
    if i:
        files.setdefault(i, []).append(f)
        if f.resolve() != (OUT / f.name).resolve():
            shutil.copy2(f, OUT / f.name)

def dhash(im, n=16):
    g = np.asarray(ImageOps.grayscale(im).resize((n + 1, n)), dtype=np.int16)
    return (g[:, 1:] > g[:, :-1]).flatten()

rows, hashes = [], {}
for i in order:
    if i not in files:
        continue
    f = files[i][-1]
    im = Image.open(f).convert("RGB")
    a = np.asarray(im, dtype=np.float32)
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])
    hashes[i] = dhash(im)
    rows.append(dict(id=i, file=f.name, size=f"{im.width}x{im.height}",
                     mean=round(float(lum.mean()), 1), dark=round(float((lum < 40).mean()) * 100, 1)))

for r in rows:  # 누락된 파일을 건너뛰어 멀리 있는 컷을 이웃으로 오인하지 않는다.
    k = cut_order.index(r["id"]) if r["id"] in cut_order else None
    near = [cut_order[j] for j in (k - 1, k + 1) if 0 <= j < len(cut_order) and cut_order[j] in hashes] if k is not None else []
    r["near"] = {n: round(float((hashes[r["id"]] != hashes[n]).mean()), 2) for n in near}
    refs = re.split(r"[+,\s]+", prompts.get(r["id"], {}).get("ref") or "")
    r["reference_distance"] = {n: round(float((hashes[r["id"]] != hashes[n]).mean()), 2)
                               for n in refs if n in hashes}

missing = [i for i in order if i not in files]
extra = [i for i in files if i not in order]
rep = ["자동 측정은 시각 승인과 구별한다. dhash는 거리(0=동일, 1=상이)이며 낮은 값은 직접 비교할 후보일 뿐이다.", "", "| id | 파일 | 크기 | 평균 밝기 | 어두운 % | 실제 이웃 컷 거리 | 첨부 기준 거리 |", "|---|---|---|---|---|---|---|"]
for r in rows:
    flag = " **밝기**" if r["mean"] < 90 else ""
    dup = ", ".join(f"{n} {v}" + (" **중복?**" if v < 0.25 else "") for n, v in r["near"].items())
    references = ", ".join(f"{n} {v}" for n,v in r["reference_distance"].items())
    rep.append(f"| {r['id']} | {r['file']} | {r['size']} | {r['mean']}{flag} | {r['dark']} | {dup} | {references} |")
rep += ["", f"빠진 id ({len(missing)}): {' '.join(missing) or '없음'}", f"계획에 없는 id: {' '.join(extra) or '없음'}"]
(OUT / "auto_report.md").write_text("\n".join(rep), encoding="utf-8")
(OUT / "auto_report.json").write_text(json.dumps(dict(
    scope="image dimensions, luminance and neighbouring dhash only; not visual approval",
    expected_count=len(order), measured_count=len(rows), missing_ids=missing,
    extra_ids=extra, rows=rows), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

# 대조용 모음: 계획 순서로 4열, 각 칸 아래 id
W, H, C = 480, 268, 4
for s in range(0, len(rows), 16):
    part = rows[s:s + 16]
    sheet = Image.new("RGB", (C * W, ((len(part) + C - 1) // C) * (H + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for k, r in enumerate(part):
        x, y = (k % C) * W, (k // C) * (H + 24)
        sheet.paste(Image.open(OUT / r["file"]).convert("RGB").resize((W, H)), (x, y))
        d.text((x + 6, y + H + 4), f"{r['id']}  ({prompts.get(r['id'], {}).get('ref', '-')})", fill="black")
    sheet.save(OUT / f"sheet_{s // 16 + 1}.jpg", quality=90)

print("\n".join(rep))
