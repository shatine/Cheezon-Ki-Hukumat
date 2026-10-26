# 8편 V09 원리 영상 보정: Flow 클립(V09.mp4, 고정 카메라)의 금을 파이프 끝에서부터 회색 시멘트로 채운다.
# Muse·Flow 모두 "시멘트가 금을 채움"을 못 그려서(넘치거나 거의 안 보임) 클라우드에서 만든 금 마스크로 합성한다.
# 사용: python v09_fill.py <clips_v1\V09.mp4> <clips_v1\V09_fill.mp4>   (같은 폴더의 v09_crack_mask.png 사용, numpy·PIL·ffmpeg만 필요)
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
W, H, FPS = 1280, 720, 24
TIP = (540, 555)                 # 파이프 끝 (Flow V09 0초 프레임 기준)
T0, T1, EDGE = 0.5, 7.5, 40      # 0.5~7.5초에 끝까지 퍼짐, 앞쪽 40px은 부드럽게
CEMENT = np.array([150, 150, 146], np.float32)

crack = np.asarray(Image.open(Path(__file__).with_name("v09_crack_mask.png")).convert("L")) > 127
yy, xx = np.mgrid[0:H, 0:W]
dist = np.hypot(xx - TIP[0], yy - TIP[1])
dmax = dist[crack].max()

rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                      stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], stdin=subprocess.PIPE)
n = 0
while True:
    b = rd.stdout.read(W * H * 3)
    if len(b) < W * H * 3:
        break
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    r = np.clip((n / FPS - T0) / (T1 - T0), 0, 1) * (dmax + EDGE)
    a = (np.clip((r - dist) / EDGE, 0, 1) * crack)[..., None]
    wr.stdin.write((fr * (1 - a) + CEMENT * a).astype(np.uint8).tobytes())
    n += 1
wr.stdin.close(); wr.wait()
print("frames", n, "->", out)
