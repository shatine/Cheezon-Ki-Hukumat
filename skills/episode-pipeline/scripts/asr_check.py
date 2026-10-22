"""나레이션 받아쓰기 검증 (필수). 로컬 Whisper(Voice Studio /transcribe, faster-whisper large-v3, GPU)로 문장마다 받아쓰고 대본과 비교.
사용: python asr_check.py tts_meta.json tts [asr_check.json] [--lang hi] [--only s03_1.wav ...]
불합격: WER>0.25 / 앞 3단어·끝 3단어 불일치(잘림·참조 음성 단어 새어 나옴) / 단어당 초 <0.25 또는 >0.9.
다른 스크립트에서: from asr_check import check  ->  check(wav경로, 대본문장) -> dict
정규화: NFC, 문장부호 제거, 영문 소문자, 누크타·찬드라빈두 무시, 힌디 숫자 단어↔숫자 같게, 영어 단어↔데바나가리 표기는 발음 골격으로 비교."""
import json, re, sys, unicodedata, difflib, subprocess, requests
from pathlib import Path

API = "http://127.0.0.1:3900/transcribe"
MAX_WER, MIN_SPW, MAX_SPW = 0.25, 0.25, 0.9

_N = "शून्य एक दो तीन चार पांच छह सात आठ नौ दस ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह उन्नीस बीस इक्कीस बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस तीस इकतीस बत्तीस तैंतीस चौंतीस पैंतीस छत्तीस सैंतीस अड़तीस उनतालीस चालीस इकतालीस बयालीस तैंतालीस चवालीस पैंतालीस छियालीस सैंतालीस अड़तालीस उनचास पचास इक्यावन बावन तिरपन चौवन पचपन छप्पन सत्तावन अट्ठावन उनसठ साठ इकसठ बासठ तिरसठ चौंसठ पैंसठ छियासठ सड़सठ अड़सठ उनहत्तर सत्तर इकहत्तर बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उन्यासी अस्सी इक्यासी बयासी तिरासी चौरासी पचासी छियासी सत्तासी अट्ठासी नवासी नब्बे इक्यानवे बानवे तिरानवे चौरानवे पचानवे छियानवे सत्तानवे अट्ठानवे निन्यानवे".split()
_EXTRA = {"छः": 6, "छे": 6, "पन्द्रह": 15, "उनासी": 79, "इक्यानबे": 91, "बानबे": 92, "तिरानबे": 93, "चौरानबे": 94, "पचानबे": 95, "छियानबे": 96, "सत्तानबे": 97, "अट्ठानबे": 98, "निन्यानबे": 99}
_MULT = {"सौ": 100, "हजार": 1000, "लाख": 100000, "करोड": 10**7}

def _base(w):  # 누크타·찬드라빈두 무시, 영문 소문자
    w = unicodedata.normalize("NFD", w).replace("़", "").replace("ँ", "ं")
    return unicodedata.normalize("NFC", w).lower()

NUM = {_base(w): i for i, w in enumerate(_N)} | {_base(k): v for k, v in _EXTRA.items()}
MULT = {_base(k): v for k, v in _MULT.items()}
PCT = {_base(w) for w in ("प्रतिशत", "परसेंट", "पर्सेंट", "percent")}

def tokens(s):
    s = unicodedata.normalize("NFC", s).replace("%", " percent ")
    s = re.sub(r"(?<=\d),(?=\d)", "", s)               # 1,46,000 -> 146000
    s = re.sub(r"(?<=\d)\.(?=\d)", "DOT", s)            # 2.6 는 소수로 남김
    s = re.sub(r"[^\w\sऀ-ॿ]|[।॥]", " _ ", s)  # 문장부호(। 포함) 제거, 숫자 끊는 자리
    out, cur, tot, innum, last, dec = [], 0, 0, False, False, None
    def flush():
        nonlocal cur, tot, innum, dec
        if innum: out.append(str(tot + cur) if dec is None else f"{dec}.{tot + cur}")
        elif dec is not None: out.append(str(dec))
        cur, tot, innum, dec = 0, 0, False, None
    for w in (re.sub(r"(?<=\d)dot(?=\d)", ".", _base(x)) for x in s.split()):
        if w in NUM:
            if innum and last: flush()       # "दो तीन" 같은 나열은 따로
            cur, innum, last = cur + NUM[w], True, True
        elif w in MULT and innum:
            m = MULT[w]; last = False
            if m == 100: cur = (cur or 1) * 100
            else: tot, cur = tot + (cur or 1) * m, 0
        elif skel(w) == "dsmlv" and innum and dec is None:  # दो दशमलव छह -> 2.6
            dec, cur, tot, innum, last = tot + cur, 0, 0, False, False
        else:
            flush(); last = False
            if w != "_": out.append("percent" if w in PCT else w)
    flush()
    return out

_DV = dict(zip("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ",
               "k k g g n c c j j n t t d d n t t d d n p f b b m y r l v s s s h l".split()))
def skel(w):  # 발음 골격: 자음만, 비슷한 소리 합침 (영어 표기와 데바나가리 표기 비교용)
    if re.fullmatch(r"[\d.]+", w): return w
    r = "".join(_DV.get(c, "") if "ऀ" <= c <= "ॿ" else c for c in w)
    r = re.sub(r"tion|sion", "sn", r)
    r = r.translate(str.maketrans("cqzjxwf", "kksssvp"))
    r = re.sub(r"[aeiouy]", "", r); r = r[:1] + r[1:].replace("h", "")
    return re.sub(r"(.)\1+", r"\1", r)

def same(a, b):
    if a == b: return True
    sa, sb = skel(a), skel(b)
    if not sa or not sb: return False
    if sa[0].isdigit() or sb[0].isdigit(): return sa == sb
    return sa == sb or difflib.SequenceMatcher(None, sa, sb).ratio() >= 0.75

def wer(ref, hyp):
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): d[i][0] = i
    for j in range(m + 1): d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + (0 if same(ref[i-1], hyp[j-1]) else 1))
            if j > 1 and same(ref[i-1], hyp[j-2] + hyp[j-1]): d[i][j] = min(d[i][j], d[i-1][j-2])  # किलो मीटर = किलोमीटर
            if i > 1 and same(ref[i-2] + ref[i-1], hyp[j-1]): d[i][j] = min(d[i][j], d[i-2][j-1])
    return d[n][m] / max(n, 1)

def edge_ok(ref3, hyp, tail=False):  # 앞(끝) 3단어 골격이 받아쓰기 앞(끝) 2~5단어와 맞는지
    r = "".join(skel(w) for w in ref3)
    cands = [hyp[-k:] if tail else hyp[:k] for k in range(2, 6) if k <= len(hyp)] or [hyp]
    return max(difflib.SequenceMatcher(None, r, "".join(skel(w) for w in c)).ratio() for c in cands) >= 0.7

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)

def transcribe(wav, lang="hi"):
    with open(wav, "rb") as f:
        r = requests.post(API, files={"audio": (Path(wav).name, f, "audio/wav")}, data={"language": lang, "mode": "accurate"}, timeout=900)
    r.raise_for_status(); return r.json()["text"].strip()

def check(wav, text, lang="hi"):
    t = transcribe(wav, lang); ref, hyp = tokens(text), tokens(t); d = dur(wav)
    w = round(wer(ref, hyp), 3); spw = round(d / max(len(text.split()), 1), 3)
    h, tl = edge_ok(ref[:3], hyp), edge_ok(ref[-3:], hyp, tail=True)
    return {"transcript": t, "wer": w, "head_ok": h, "tail_ok": tl, "dur": round(d, 3), "sec_per_word": spw,
            "pass": w <= MAX_WER and h and tl and MIN_SPW <= spw <= MAX_SPW}

def main():
    a = sys.argv[1:]; lang = "hi"; only = set()
    if "--lang" in a: i = a.index("--lang"); lang = a[i+1]; del a[i:i+2]
    if "--only" in a: i = a.index("--only"); only = set(a[i+1:]); del a[i:]
    meta, folder = json.load(open(a[0], encoding="utf-8")), Path(a[1])
    out = Path(a[2] if len(a) > 2 else "asr_check.json")
    res = json.load(open(out, encoding="utf-8")) if out.exists() and only else {}
    for items in meta.values():
        for x in items:
            if only and x["wav"] not in only: continue
            res[x["wav"]] = r = check(folder / x["wav"], x["spoken"], lang)
            print(x["wav"], "PASS" if r["pass"] else "FAIL", r["wer"], r["head_ok"], r["tail_ok"], r["sec_per_word"], flush=True)
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bad = [k for k, v in res.items() if not v["pass"]]
    print(f"{len(res)-len(bad)}/{len(res)} pass", "FAIL:", bad if bad else "none")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
