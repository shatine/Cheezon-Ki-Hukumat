"""엄격한 잡음(헛소리 음절) 검사 — 문장 wav 하나를 Whisper(Hindi, 단어 시각)로 받아쓰고 대본과 단어 단위로 맞춘다.
불합격 조건
 1) 받아쓰기에 대본에 없는 단어가 있음 (앞/중간/끝 어디든: 삽입 단어, 또는 대본 단어와 전혀 안 닮은 치환 단어)
 2) 첫 맞춘 단어 앞, 마지막 맞춘 단어 뒤에 소리 나는 구간이 0.15초 넘게 있음
 3) 첫/끝 단어 길이가 비정상(>1.0초: 잡음이 단어에 붙어 있을 때)
 4) WER > 0.15
길이 이상치(글자 수 대비)는 전체 문장을 모아 tts 스크립트에서 따로 본다.
사용: from junk_check import jcheck; jcheck(wav, text) -> dict
      python junk_check.py file.wav "대본"   (단독 검사)"""
import sys, re, json, difflib, unicodedata, requests, numpy as np, soundfile as sf
sys.path.insert(0, r"D:\youtube\7. Cheezon Ki Hukumat\.claude\skills\cheezon-production\tools")   # asr_check.py (이전 episode-pipeline\scripts에서 옮김)
from asr_check import tokens, same, skel, wer, MULT, _base

SPELL = {"उन्हत्तर": "उनहत्तर"}   # 낭독용 다른 철자 → 대본 철자 (검사 기준은 대본)
API = "http://127.0.0.1:3900/v1/audio/transcriptions"

VS_PY = r"C:\Users\developer1\AppData\Roaming\VoiceStudio\runtime\project\.venv\Scripts\python.exe"
def whisper_words(wav, lang="hi", prompt=None):
    import os, subprocess, tempfile
    if os.environ.get("WHISPER_LOCAL"):   # 서버 대신 같은 모델(faster-whisper large-v3)을 직접 실행 (fw_local.py)
        out = tempfile.mktemp(suffix=".json")
        subprocess.run([VS_PY, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fw_local.py"), out, str(wav)], check=False,
                       env=dict(os.environ, HF_HUB_OFFLINE="1"))
        d = json.load(open(out, encoding="utf-8"))[0]
        return d["text"].strip(), [w for w in d["words"] if w["word"].strip()]
    import time
    data = {"language": lang, "response_format": "verbose_json", "timestamp_granularities[]": "word"}
    for k in range(4):   # 서버가 가끔 모델 확인 중 연결 끊김으로 500 → 잠시 뒤 다시
        with open(wav, "rb") as f:
            r = requests.post(API, files={"file": ("a.wav", f, "audio/wav")}, data=data, timeout=900)
        if r.status_code != 500 or k == 3: break
        time.sleep(10)
    r.raise_for_status(); d = r.json()
    return d["text"].strip(), [w for w in d.get("words", []) if w["word"].strip()]

def fix_words(words):
    """'1' '.5' '-2', '7,90,' '000' 처럼 쪼개진 숫자 조각을 합치고, '1.5-2' → '1.5 से 2'"""
    ws = []
    for w in words:
        w = dict(w); w["word"] = w["word"].strip()
        if ws and ((re.search(r"[\d]$", ws[-1]["word"]) and re.match(r"[.,\-–]\d", w["word"]))
                   or (re.fullmatch(r"[\d,.]+,", ws[-1]["word"]) and re.match(r"\d", w["word"]))):
            ws[-1]["word"] += w["word"]; ws[-1]["end"] = w["end"]
        else: ws.append(w)
    EQ = {"यह": "ये", "वह": "वो", "यहां": "यहाँ"}   # 같은 단어의 표준/구어 표기
    for w in ws: w["word"] = EQ.get(re.sub(r"[,.।?]+$", "", w["word"]), w["word"])
    for w in ws: w["word"] = re.sub(r"(?<=\d)\s*[-–]\s*(?=\d)", " से ", w["word"])
    return ws


def hyp_tokens(words):
    """Whisper 단어 → 정규화 토큰 (숫자 단어 묶음 포함), 토큰마다 (시작, 끝) 시각"""
    words = fix_words(words)
    out = []
    # 숫자 묶음을 위해 연속 단어를 tokens()로 같이 돌리고, 결과 토큰을 단어 범위에 대응시킨다
    i = 0
    while i < len(words):
        # 단어 하나씩 늘려 가며 토큰 수가 안정되는 단위를 찾는다 (숫자 묶음은 최대 6단어)
        best = None
        for j in range(i + 1, min(i + 7, len(words)) + 1):
            t = tokens(" ".join(w["word"] for w in words[i:j]))
            if len(t) == 1 and re.fullmatch(r"[\d.]+", t[0]): best = (j, t)
        if best:
            j, t = best
            out.append((t[0], words[i]["start"], words[j-1]["end"])); i = j; continue
        for t in tokens(words[i]["word"]):
            out.append((t, words[i]["start"], words[i]["end"]))
        i += 1
    return merge_digits(out)

def merge_digits(out):
    """Whisper가 '36 लाख', '7 लाख 90 हज़ार' 처럼 숫자+단위로 적은 것 → 하나의 숫자 토큰"""
    res, k = [], 0
    isnum = lambda t: re.fullmatch(r"\d+", t) is not None
    while k < len(out):
        t, s, e = out[k]
        if isnum(t) and k + 1 < len(out) and _base(out[k+1][0]) in MULT:
            total, cur, j, last_num = 0, 0, k, False
            while j < len(out):
                tj = out[j][0]; b = _base(tj)
                if isnum(tj) and not last_num: cur += int(tj); last_num = True
                elif b in MULT and (cur or last_num):
                    m = MULT[b]; last_num = False
                    if m == 100: cur = (cur or 1) * 100
                    else: total, cur = total + (cur or 1) * m, 0
                else: break
                j += 1
            res.append((str(total + cur), s, out[j-1][2])); k = j
        else:
            res.append(out[k]); k += 1
    return res

def align(ref, hyp):
    """ref 토큰, hyp 토큰 문자열 → 각 hyp 토큰의 상태 ('m' 맞음, 's' 치환, 'i' 삽입, 'j' 두 hyp가 ref 하나)"""
    n, m = len(ref), len(hyp); INF = 10**9
    d = [[INF] * (m + 1) for _ in range(n + 1)]; bt = [[None] * (m + 1) for _ in range(n + 1)]
    d[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0: continue
            c = []
            if i > 0: c.append((d[i-1][j] + 1, "del"))
            if j > 0: c.append((d[i][j-1] + 1, "ins"))
            if i > 0 and j > 0:
                sc = 0 if same(ref[i-1], hyp[j-1]) else (0.5 if sim(ref[i-1], hyp[j-1]) >= 0.5 else 1)
                c.append((d[i-1][j-1] + sc, "sub"))
            if i > 0 and j > 1 and merge_ok(ref[i-1], hyp[j-2] + hyp[j-1]): c.append((d[i-1][j-2] + 0.1, "j2"))
            if i > 0 and j > 2 and merge_ok(ref[i-1], hyp[j-3] + hyp[j-2] + hyp[j-1]): c.append((d[i-1][j-3] + 0.2, "j3"))
            if i > 1 and j > 0 and merge_ok(ref[i-2] + ref[i-1], hyp[j-1]): c.append((d[i-2][j-1] + 0.1, "r2"))
            d[i][j], bt[i][j] = min(c)
    st = [None] * m; i, j = n, m; pairs = []
    while i > 0 or j > 0:
        op = bt[i][j]
        if op == "del": i -= 1
        elif op == "ins": j -= 1; st[j] = ("i", None)
        elif op == "sub":
            i -= 1; j -= 1; st[j] = ("m" if same(ref[i], hyp[j]) else "s", ref[i])
        elif op == "j2": i -= 1; j -= 2; st[j] = ("m", ref[i]); st[j+1] = ("m", ref[i])
        elif op == "j3": i -= 1; j -= 3; st[j] = st[j+1] = st[j+2] = ("m", ref[i])
        elif op == "r2": i -= 2; j -= 1; st[j] = ("m", ref[i] + ref[i+1])
    return st

def merge_ok(a, b):
    """띄어쓰기만 다른 경우(किलो मीटर = किलोमीटर)만 합침: 발음 골격 같음 + 글자 자체도 85% 이상 같음"""
    return same(a, b) and difflib.SequenceMatcher(None, unicodedata.normalize("NFC", a), unicodedata.normalize("NFC", b)).ratio() >= 0.85


def sim(a, b):
    sa, sb = skel(a), skel(b)
    if not sa or not sb: return 0.0
    return difflib.SequenceMatcher(None, sa, sb).ratio()

def voiced_frames(wav):
    a, sr = sf.read(wav, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    hop = int(sr * 0.01); n = len(a) // hop
    db = np.array([20 * np.log10(np.sqrt(np.mean(a[i*hop:(i+1)*hop] ** 2) + 1e-12)) for i in range(n)])
    return db > -40, len(a) / sr

def jcheck(wav, text, lang="hi"):
    t, words = whisper_words(wav, lang)
    for a, b in SPELL.items(): text = text.replace(a, b)
    ref = tokens(text.replace("डेढ़", "1.5")); ht = hyp_tokens(words); hyp = [x[0] for x in ht]
    st = align(ref, hyp) if hyp else []
    junk = []
    for k, (tok, s, e) in enumerate(ht):
        kind, r = st[k]
        if kind == "i": junk.append(f"+{tok}@{s:.2f}")
        elif kind == "s" and (sim(tok, r) < 0.5 or re.fullmatch(r"[\d.]+", tok) or re.fullmatch(r"[\d.]+", r)):
            junk.append(f"{r}->{tok}@{s:.2f}")      # 숫자는 정확히 같아야 함 (1969 ≠ 1979)
    v, total = voiced_frames(wav)
    matched = [k for k in range(len(ht)) if st[k][0] in "ms"]
    if matched:
        t0, t1 = ht[matched[0]][1], ht[matched[-1]][2]
        pre = float(v[: int(t0 * 100)].sum()) * 0.01
        post = float(v[int(t1 * 100) + 1:].sum()) * 0.01
        fw = ht[matched[0]][2] - t0; lw = t1 - ht[matched[-1]][1]
    else:
        pre = post = total; fw = lw = 0
    # 단어 안에 0.15초 넘는 무음이 끼어 있으면 = 떨어진 소리 덩어리(잡음)가 단어에 붙어 있음
    gaps = []
    edge = [k for k in range(len(ht)) if st and st[k][0] in "ms"]
    edge = {edge[0], edge[-1]} if edge else set()
    for k, (tok, s, e) in enumerate(ht):
        if k not in edge: continue      # 문장 첫/끝 단어만 (쉼표 뒤 단어는 Whisper가 앞 쉼을 포함시킴)
        seg = v[int(s * 100):int(e * 100)]; run = best = 0
        for x in seg:
            run = 0 if x else run + 1; best = max(best, run)
        if best * 0.01 >= 0.15: gaps.append(f"{tok}@{s:.2f}:{best * 0.01:.2f}s")
    w = round(wer(ref, hyp), 3)
    reasons = []
    if gaps: reasons.append("silence_inside_word")
    if junk: reasons.append("junk_words")
    if pre > 0.15: reasons.append(f"voiced_before_{pre:.2f}s")
    if post > 0.15: reasons.append(f"voiced_after_{post:.2f}s")
    if fw > 1.0: reasons.append(f"long_first_word_{fw:.2f}s")
    if lw > 1.0: reasons.append(f"long_last_word_{lw:.2f}s")
    if w > 0.15: reasons.append(f"wer_{w}")
    return {"transcript": t, "wer": w, "junk": junk, "gaps": gaps, "pre_voiced": round(pre, 2), "post_voiced": round(post, 2),
            "first_w": round(fw, 2), "last_w": round(lw, 2), "dur": round(total, 3), "chars": len(text),
            "sec_per_char": round(total / max(len(text), 1), 4), "reasons": reasons, "pass": not reasons}

if __name__ == "__main__":
    import io; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(json.dumps(jcheck(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=1))
