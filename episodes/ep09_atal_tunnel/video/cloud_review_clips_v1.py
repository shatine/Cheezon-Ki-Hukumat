# 8편 클라우드 영상 검수 준비: video/v1/*.mp4 → 작업 폴더에 1초 간격 프레임 모음과 0.5초 밝기표를 만든다.
# 사용: python3 cloud_review_clips_v1.py <작업 폴더> [영상 폴더]   (그 뒤 git rm -r video/v1 && commit)
# 자동 측정은 보조다. 모음 시트를 보고 모양·얼굴 크기·원리 방향·글자를 직접 확인한다.
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "v1"
order = [c["id"] for c in json.load(open(HERE / "vprompts_v1.json", encoding="utf-8"))]

def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(f)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout); st = j["streams"][0]
    return st["width"], st["height"], st["r_frame_rate"], float(j["format"]["duration"])

def frames(f, fps, w):  # fps 간격 프레임을 w 폭 RGB 배열로
    h = w * 9 // 16
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", f"fps={fps},scale={w}:{h}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    return a.reshape(-1, h, w, 3)

rep = ["| id | 크기 | fps | 길이 | 밝기 0.5초 간격 (최소–최대) | 처음→끝 변화 |", "|---|---|---|---|---|---|"]
for i in order:
    f = SRC / f"{i}.mp4"
    if not f.exists():
        rep.append(f"| {i} | **없음** | | | | |"); continue
    w, h, r, d = probe(f)
    fr = frames(f, 2, 320)
    lum = [round(float((0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]).mean()), 1) for x in fr.astype(np.float32)]
    drop = round(lum[-1] - lum[0], 1)
    rep.append(f"| {i} | {w}x{h} | {r} | {d:.2f} | {min(lum)}–{max(lum)} : {' '.join(str(round(v)) for v in lum)} | {drop}{' **어두워짐**' if drop < -15 else ''} |")
    one = frames(f, 1, 384)  # 1초 간격 모음
    C = 4; H = 216
    sheet = Image.new("RGB", (C * 384, ((len(one) + C - 1) // C) * (H + 20)), "white")
    dr = ImageDraw.Draw(sheet)
    for k, x in enumerate(one):
        X, Y = (k % C) * 384, (k // C) * (H + 20)
        sheet.paste(Image.fromarray(x), (X, Y)); dr.text((X + 4, Y + H + 3), f"{i}  {k}s", fill="black")
    sheet.save(OUT / f"{i}_sheet.jpg", quality=88)
(OUT / "auto_report.md").write_text("\n".join(rep), encoding="utf-8")
print("\n".join(rep))
