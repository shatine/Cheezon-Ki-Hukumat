# 10편 썸네일 시안: 글자 없는 배경(CB\thumb\) 위에 도입부 문장 힌디어를 크게 넣는다.
# 이 PC의 Pillow에는 raqm이 없어 데바나가리가 깨지므로, 글자는 크롬 헤드리스(HTML)로 그린다.
# 사용: python make_thumb_v1.py <배경.png> <출력.jpg>
import sys, subprocess, tempfile, pathlib
from PIL import Image
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FONT_DEV = pathlib.Path(r"D:\youtube\7. Cheezon Ki Hukumat\tools\fonts\NotoSansDevanagari-VF.ttf").as_uri()
FONT_LAT = pathlib.Path(r"D:\youtube\7. Cheezon Ki Hukumat\tools\fonts\NotoSans-VF.ttf").as_uri()
W, H = 1280, 720
MARGIN = 30                      # 위·아래 여백
SIDE = 34                        # 좌우 여백
TOP = ("सीवर जाम करने वाले तेल से", "#ff2a1e")     # 빨강 = 문제
BOT = ("ट्रक कैसे दौड़ाए?", "#ffe100")             # 노랑 = 질문
bg, out = sys.argv[1], sys.argv[2]
html = f"""<!doctype html><meta charset="utf-8"><style>
@font-face {{ font-family: D; src: url('{FONT_DEV}'); }}
@font-face {{ font-family: L; src: url('{FONT_LAT}'); }}
html,body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; }}
body {{ background:url('{pathlib.Path(bg).as_uri()}') center/cover; position:relative; }}
.t {{ position:absolute; left:0; width:{W}px; text-align:center; white-space:nowrap;
     font-family:D, L; font-weight:900; line-height:1.18; paint-order:stroke fill;
     -webkit-text-stroke: var(--sw) #000; }}
</style><body>
<div class="t" id="a" style="top:{MARGIN}px;color:{TOP[1]}">{TOP[0]}</div>
<div class="t" id="b" style="bottom:{MARGIN}px;color:{BOT[1]}">{BOT[0]}</div>
<script>
document.fonts.ready.then(()=>{{
  for (const [id, max] of [['a', 150], ['b', 210]]) {{
    const e = document.getElementById(id); let fs = max;
    do {{ e.style.fontSize = fs + 'px'; e.style.setProperty('--sw', Math.round(fs/7) + 'px');
         e.style.width = 'auto'; fs -= 2; }} while (e.scrollWidth + fs/7 > {W - 2*SIDE});
    e.style.width = '{W}px';
  }}
}});
</script>"""
with tempfile.TemporaryDirectory() as d:
    p = pathlib.Path(d) / "t.html"; p.write_text(html, encoding="utf-8")
    png = pathlib.Path(d) / "t.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    f"--window-size={W},{H}", "--virtual-time-budget=3000", f"--screenshot={png}", p.as_uri()],
                   check=True, capture_output=True)
    Image.open(png).convert("RGB").save(out, quality=92)
    Image.open(out).resize((320, 180), Image.LANCZOS).save(out.replace(".jpg", "_320.jpg"), quality=90)
print("saved", out)
