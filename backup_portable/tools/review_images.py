# 이미지 검수 준비: CB\img의 그림을 검수 폴더로 복사하고, 자동 측정과 대조표를 만든다.
# 사용: episodes\epNN\images\에 review_images_v1.py로 복사한 뒤  python review_images_v1.py <검수 폴더> <CB\img>
# 자동 측정(크기, 밝기, 이웃 컷 유사도)은 보조일 뿐이다. 모든 장을 원본 크기로 직접 본다.
import json, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import numpy as np

HERE = Path(__file__).resolve().parent
EP = HERE.parent
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SRC = Path(sys.argv[2])

prompts = {p["id"]: p for p in json.load(open(HERE / "prompts_v1.json", encoding="utf-8"))}
# 계획 순서: 컷 표의 소스 열 (기준 그림 CB·G3D는 맨 앞)
order = ["CB", "G3D"]
for line in open(EP / "plan" / "shot_table_v1.md", encoding="utf-8"):
    m = re.match(r"\| [\d.]+–[\d.]+ \| [\d.]+ \| [^|]+ \| (\w+) \|", line)
    if m and m.group(1) not in order:
        order.append(m.group(1))

def pid(name):  # v1_i03c3_3.png -> i03c3
    m = re.match(r"v1_(.+)_(\d+)\.png$", name)
    return m.group(1) if m else None

files = {}
for f in sorted(SRC.glob("*.png")):
    i = pid(f.name)
    if i:
        files.setdefault(i, []).append(f)
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

ids = [r["id"] for r in rows]
for k, r in enumerate(rows):  # 이웃 컷과 구도 유사도(0=같음, 1=전혀 다름)
    near = [ids[j] for j in (k - 1, k + 1) if 0 <= j < len(ids)]
    r["near"] = {n: round(float((hashes[r["id"]] != hashes[n]).mean()), 2) for n in near}

missing = [i for i in order if i not in files]
extra = [i for i in files if i not in order]
rep = ["| id | 파일 | 크기 | 평균 밝기 | 어두운 % | 이웃 유사도 |", "|---|---|---|---|---|---|"]
for r in rows:
    flag = " **밝기**" if r["mean"] < 90 else ""
    dup = ", ".join(f"{n} {v}" + (" **중복?**" if v < 0.25 else "") for n, v in r["near"].items())
    rep.append(f"| {r['id']} | {r['file']} | {r['size']} | {r['mean']}{flag} | {r['dark']} | {dup} |")
rep += ["", f"빠진 id ({len(missing)}): {' '.join(missing)}", f"계획에 없는 id: {' '.join(extra)}"]
(OUT / "auto_report.md").write_text("\n".join(rep), encoding="utf-8")

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
