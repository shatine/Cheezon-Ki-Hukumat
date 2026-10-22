"""완성 영상 검증기. 신비한 건축사전 인기 상위 10편에서 잰 기준값(targets.json)과 비교해 PASS/FAIL 표를 만든다.
사용: python check_output.py <영상.mp4> [--srt <자막.srt>] [--lang ko|en] [--out report.md]
필요: ffmpeg, ffprobe (PATH), numpy.  기준 영상도 같은 방법으로 쟀다(같은 자로 재야 비교가 된다).
측정 방법
- 컷: 15fps·가로 480으로 줄여 장면 변화 점수 > 0.2, 0.4초 안의 중복은 하나로
- 자막 띠: 1초 1장, 화면 아래 40%에서 '흰 글자 + 어두운 테두리' 픽셀이 모인 가로 띠
- 소리: ebur128(통합 음량·최고 피크), 50ms RMS로 말 레벨·쉼·바닥 레벨
- 말 속도: --srt 를 주면 글자(한글 음절 또는 영어 단어)/초"""
import json, re, subprocess, sys, argparse
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
T = json.loads((HERE / "targets.json").read_text(encoding="utf-8"))
INFO = set(T.get("info_only", []))


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe(p):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,codec_type", "-of", "json", str(p)])
    j = json.loads(r.stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"][0]
    return float(j["format"]["duration"]), v["width"], v["height"]


def cuts(p):
    import tempfile, os
    fd, tmp = tempfile.mkstemp(suffix=".txt"); os.close(fd)
    sh(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-filter_complex",
        f"[0:v]fps=15,scale=480:-1,select='gt(scene,0.2)',metadata=print:file='{Path(tmp).as_posix()}'", "-an", "-f", "null", "-"])
    ts = sorted(float(t) for t in re.findall(r"pts_time:([\d.]+)", Path(tmp).read_text()))
    os.remove(tmp)
    out, last = [], -9
    for t in ts:
        if t - last > 0.4:
            out.append(t)
            last = t
    return out


def frames_gray(p, w=480, h=270):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"fps=1,scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    return a.reshape(-1, h, w, 3)


def sub_band(fr):
    n, h, w, _ = fr.shape
    res = []
    for im in fr:
        white = im.min(2) > 215
        dark = im.mean(2) < 60
        d = dark.copy()
        d[1:] |= dark[:-1]; d[:-1] |= dark[1:]; d[:, 1:] |= dark[:, :-1]; d[:, :-1] |= dark[:, 1:]
        txt = white & d
        y0 = int(h * 0.6)
        rows = txt[y0:].sum(1)
        r = np.where(rows >= 4)[0]
        if len(r) < 3:
            continue
        groups = np.split(r, np.where(np.diff(r) > 3)[0] + 1)
        g = max(groups, key=lambda x: rows[x].sum())
        if rows[g].sum() < 40:
            continue
        cols = np.where(txt[y0 + g[0]:y0 + g[-1] + 1].sum(0) > 0)[0]
        res.append((g[0] + y0, g[-1] + y0, cols.min(), cols.max()))
    if not res:
        return dict(present=0.0)
    R = np.array(res, float)
    return dict(present=len(res) / n, bottom_margin_pct=(h - np.median(R[:, 1])) / h * 100,
                band_height_pct=np.median(R[:, 1] - R[:, 0] + 1) / h * 100,
                two_line_pct=float(((R[:, 1] - R[:, 0] + 1) / h > 0.09).mean() * 100),
                center_offset_pct=abs(np.median((R[:, 2] + R[:, 3]) / 2) - w / 2) / w * 100)


def audio(p):
    r = sh(["ffmpeg", "-v", "info", "-i", str(p), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 800
    n = len(a) // hop
    db = 20 * np.log10(np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-6)
    med = np.median(db[db > np.median(db)])
    low = db < med - 15
    runs, c = [], 0
    for x in low:
        if x:
            c += 1
        else:
            if c:
                runs.append(c * 0.05)
            c = 0
    runs = np.array(runs)
    pauses = runs[runs >= 0.15]
    floor = float(np.median(db[low])) if low.any() else -90.0
    onset = float(np.argmax(db > -40) * 0.05)
    return dict(I=I, TP=TP, speech_minus_floor=float(med - floor), pause_p90=float(np.percentile(pauses, 90)) if len(pauses) else 0.0,
                pauses_over_1s=int((pauses > 1.0).sum()), first_sound=onset)


def speech_rate(srt, lang):
    txt = Path(srt).read_text(encoding="utf-8")
    times = re.findall(r"(\d+):(\d+):(\d+),(\d+)", txt)
    secs = [int(a) * 3600 + int(b) * 60 + int(c) + int(d) / 1000 for a, b, c, d in times]
    body = " ".join(l for l in txt.splitlines() if l.strip() and "-->" not in l and not l.strip().isdigit())
    span = max(secs) - min(secs)
    if lang == "ko":
        return len(re.findall(r"[가-힣]", body)) / span
    return len(re.findall(r"[A-Za-z']+", body)) / span


def judge(name, val, lo=None, hi=None, info=False):
    ok = (lo is None or val >= lo) and (hi is None or val <= hi)
    rng = f"{'' if lo is None else lo} ~ {'' if hi is None else hi}"
    return (name, round(val, 2), rng, ("참고-범위안" if ok else "참고-범위밖") if info else ("PASS" if ok else "FAIL"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--srt"); ap.add_argument("--lang", default="en"); ap.add_argument("--out")
    a = ap.parse_args()
    dur, W, H = probe(a.video)
    c = cuts(a.video)
    b = [0] + c + [dur]
    L = np.diff(b)
    first = [x for x in c if x < 30]
    sb = sub_band(frames_gray(a.video))
    au = audio(a.video)
    t = T["targets"]
    rows = [
        judge("화면 비율 (가로/세로)", W / H, 1.76, 1.79),
        judge("샷 길이 중앙값(초)", float(np.median(L)), *t["shot_median_s"]),
        judge("샷 길이 상위10%(초)", float(np.percentile(L, 90)), None, t["shot_p90_max_s"]),
        judge("가장 긴 샷(초)", float(L.max()), None, t["shot_max_s"]),
        judge("첫 30초 평균 컷 간격(초)", 30 / (len(first) + 1), None, t["first30_mean_max_s"]),
        judge("자막이 보이는 시간 비율(%)", sb.get("present", 0) * 100, t["sub_present_min_pct"], None),
    ]
    if sb.get("present"):
        rows += [judge("자막 아래 여백(화면 높이 %)", sb["bottom_margin_pct"], *t["sub_bottom_margin_pct"]),
                 judge("자막 두 줄 비율(%)", sb["two_line_pct"], None, t["sub_two_line_max_pct"]),
                 judge("자막 가운데 어긋남(%)", sb["center_offset_pct"], None, t["sub_center_offset_max_pct"])]
    rows += [judge("통합 음량(LUFS)", au["I"], *t["lufs"]),
             judge("최고 피크(dBTP)", au["TP"], None, t["true_peak_max"]),
             judge("말 - 배경 바닥 차이(dB)", au["speech_minus_floor"], *t["speech_minus_floor_db"], info="speech_minus_floor_db" in INFO),
             judge("쉼 상위10%(초)", au["pause_p90"], None, t["pause_p90_max_s"], info="pause_p90_max_s" in INFO),
             judge("1초 넘는 쉼(개)", au["pauses_over_1s"], None, t["pauses_over_1s_max"], info="pauses_over_1s_max" in INFO),
             judge("첫 소리 시작(초)", au["first_sound"], None, t["first_sound_max_s"])]
    if a.srt:
        lo, hi = t["speech_rate"][a.lang]
        rows.append(judge(f"말 속도({'음절' if a.lang == 'ko' else '단어'}/초)", speech_rate(a.srt, a.lang), lo, hi))
    fails = [r for r in rows if r[3] == "FAIL"]
    md = [f"# 검증: {Path(a.video).name}", "", f"길이 {dur:.1f}초, {W}x{H}, 컷 {len(c)}개", "",
          "| 항목 | 측정값 | 기준 | 결과 |", "|---|---|---|---|"] + [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |" for r in rows]
    md += ["", f"**{'통과' if not fails else f'미달 {len(fails)}개'}**"]
    text = "\n".join(md)
    print(text)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
