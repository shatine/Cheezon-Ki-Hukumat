"""EP7 s26 원리 영상(통제 그래픽): img3d/v5_s26_1.png 그대로 + 호스·케이블 안에서만 움직이는 빛 펄스 → clips_v9/s26g.mp4 (1920x1080, 30fps, 10초).
Muse 재생성(2회)이 호스 모양을 바꾸고 물빛을 잔디로 흘려서 원리가 틀어짐 → 경로를 손으로 따서 그린다.
방향: 물(파랑) 기둥 → 버스 물탱크, 오수(갈색) 화장실·회색 탱크 → 기둥 옆 땅, 전기(노랑) 기둥 → 버스 소켓.
사용: python make_s26_flow.py <BUS 폴더>"""
import sys, subprocess
from pathlib import Path
import cv2, numpy as np

BUS = Path(sys.argv[1]); SRC = BUS / "img3d" / "v5_s26_1.png"; OUT = BUS / "clips_v9" / "s26g.mp4"; OUT.parent.mkdir(exist_ok=True)
FPS, SEC, W, H = 30, 10.0, 1920, 1080
# 경로(원본 1376x768 좌표), 흐름 방향 순서. 그리드 확대(img 600~1200 x 330~540)에서 관 중심선을 땀
PATHS = [
    # (점들, BGR 색, 펄스 반지름, 간격 px, 속도 px/s)
    ([(1137, 435), (1130, 455), (1120, 475), (1090, 490), (1025, 502), (960, 510), (925, 507), (900, 495), (865, 487),
      (825, 490), (775, 502), (730, 517), (720, 505), (715, 480), (695, 462)], (255, 170, 40), 4.0, 34, 70),      # 물
    ([(995, 350), (1010, 360), (1015, 390), (1015, 420), (1025, 440), (1040, 450), (1050, 455), (1065, 460)],
     (40, 75, 120), 3.2, 30, 45),                                                                                 # 오수(화장실)
    ([(877, 427), (890, 432), (897, 450), (900, 470), (910, 485), (940, 492), (990, 487), (1040, 477), (1065, 467)],
     (40, 75, 120), 3.2, 30, 45),                                                                                 # 오수(회색 탱크)
    ([(1135, 410), (1120, 430), (1100, 445), (1080, 442), (1065, 425), (1055, 405), (1047, 390), (1042, 385)],
     (60, 240, 255), 2.6, 22, 90),                                                                                # 전기
]
img8 = cv2.imdecode(np.fromfile(str(SRC), np.uint8), cv2.IMREAD_COLOR); base = img8.astype(np.float32)
SCALE = 2   # 2배로 그린 뒤 줄여 가장자리를 부드럽게
hsv = cv2.cvtColor(img8, cv2.COLOR_BGR2HSV)
MASK = {"blue": cv2.inRange(hsv, (95, 110, 90), (125, 255, 255)), "yellow": cv2.inRange(hsv, (18, 90, 140), (38, 255, 255))}
def resample(pts, step=2.0):
    p = np.array(pts, np.float32); out = [p[0]]
    for a, b in zip(p[:-1], p[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step)); out += [a + (b - a) * k / n for k in range(1, n + 1)]
    p = np.array(out, np.float32); seg = np.linalg.norm(np.diff(p, axis=0), axis=1); return p, np.concatenate([[0], np.cumsum(seg)])
def snap(p, mask, rad=14):
    """손으로 딴 점을 관 색 마스크의 중심으로 옮긴다(수직 방향으로 rad 안에서)"""
    q = p.copy()
    for i in range(len(p)):
        a, b = p[max(0, i - 3)], p[min(len(p) - 1, i + 3)]; d = b - a; n = np.array([-d[1], d[0]]); n /= np.linalg.norm(n) + 1e-6
        hits = [k for k in range(-rad, rad + 1) if mask[int(round(p[i][1] + n[1] * k)), int(round(p[i][0] + n[0] * k))]]
        if hits: q[i] = p[i] + n * np.mean(hits)
    q = cv2.GaussianBlur(q.reshape(-1, 1, 2), (1, 9), 0).reshape(-1, 2)   # 들쭉날쭉 정리
    seg = np.linalg.norm(np.diff(q, axis=0), axis=1); return q, np.concatenate([[0], np.cumsum(seg)])
KIND = ["blue", None, None, "yellow"]
paths = []
for (pts, col, r, gap, v), k in zip(PATHS, KIND):
    p, cum = resample(pts)
    if k: p, cum = snap(p, MASK[k])
    paths.append(((p, cum), col, r, gap, v))
def at(p, cum, s):
    i = min(np.searchsorted(cum, s, side="right") - 1, len(cum) - 2); t = (s - cum[i]) / max(cum[i + 1] - cum[i], 1e-6)
    return p[i] + (p[i + 1] - p[i]) * t
proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(OUT)], stdin=subprocess.PIPE)
big = cv2.resize(base, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_CUBIC)
for f in range(int(FPS * SEC)):
    t = f / FPS; glow = np.zeros_like(big); core = np.zeros_like(big)
    fade = min(1.0, t / 0.6)                                   # 첫 0.6초에 흐름이 켜짐
    for (p, cum), col, r, gap, v in paths:
        L = cum[-1]; off = (t * v) % gap; s = off
        while s < L:
            x, y = at(p, cum, s); e = min(1.0, s / 12, (L - s) / 12)   # 관 끝에서 부드럽게
            c = (int(x * SCALE), int(y * SCALE))
            cv2.circle(glow, c, int(r * 2.0 * SCALE), [k * e * fade for k in col], -1, cv2.LINE_AA)
            cv2.circle(core, c, int(r * SCALE), [min(255, k * 0.5 + 128) * e * fade for k in col], -1, cv2.LINE_AA)
            s += gap
    glow = cv2.GaussianBlur(glow, (0, 0), 3 * SCALE); core = cv2.GaussianBlur(core, (0, 0), 0.8 * SCALE)
    out = np.clip(big + glow * 0.55 + core * 0.75, 0, 255)
    frame = cv2.resize(out, (W, H), interpolation=cv2.INTER_AREA).astype(np.uint8)
    proc.stdin.write(frame.tobytes())
proc.stdin.close(); proc.wait()
print("saved", OUT)
