# 8편 썸네일 v3: thumb_v2 글자를 지운 바탕(clean.png) 위에 글자를 크게, 위아래 여백을 두고 다시 넣는다.
import sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
DEV, LAT = "nsd900_devanagari.ttf", "nsd900_latin.ttf"
W, H = 1672, 941
base = Image.open("clean.png").convert("RGB")
orig = Image.open("thumb_v2_full.png").convert("RGB")
mode = sys.argv[1]          # one = 하단 한 줄 (폭에 맞춤), two = 하단 두 줄 1.5배
MARGIN = 48                 # 위·아래 여백 (941 기준)
TOP_FS = 255                # 기존 약 170 → 1.5배
def text_w(fs, s, q=False):
    w = ImageFont.truetype(DEV, fs).getlength(s)
    return w + (ImageFont.truetype(LAT, fs).getlength("?") if q else 0)
def draw_line(d, s, fs, y_top, fill, q=False, cx=W / 2):
    fd, fl = ImageFont.truetype(DEV, fs), ImageFont.truetype(LAT, fs)
    sw = max(8, fs // 12)
    w = text_w(fs, s, q); x = cx - w / 2
    top = fd.getbbox(s, anchor="ls")[1]          # 기준선에서 글자 맨 위까지 (음수)
    yb = y_top - top + sw
    d.text((x, yb), s, font=fd, fill=fill, anchor="ls", stroke_width=sw, stroke_fill="black")
    if q: d.text((x + fd.getlength(s), yb), "?", font=fl, fill=fill, anchor="ls", stroke_width=sw, stroke_fill="black")
    bot = fd.getbbox(s, anchor="ls")[3]
    return yb + bot + sw                          # 글자 맨 아래 y
# 바닥 띠: 지운 자국을 가리려고 원본 아래쪽을 크게 흐리고 살짝 어둡게
img = base.copy()
band_top = 700 if mode == "one" else 520
blur = base.crop((0, band_top, W, H)).filter(ImageFilter.GaussianBlur(28))
grad = np.linspace(0, 1, H - band_top)[:, None, None]
a = np.clip(grad * 1.6, 0, 1)
mix = (np.asarray(base.crop((0, band_top, W, H)), float) * (1 - a) + np.asarray(blur, float) * a * 0.72)
img.paste(Image.fromarray(mix.astype(np.uint8)), (0, band_top))
# 위 띠: 하늘 지운 자국을 부드럽게
sky = img.crop((0, 0, W, 300)).filter(ImageFilter.GaussianBlur(14))
ma = np.clip(1 - np.linspace(0, 1, 300) / 0.85, 0, 1)[:, None, None] * 0.9
img.paste(Image.fromarray((np.asarray(img.crop((0, 0, W, 300)), float) * (1 - ma) + np.asarray(sky, float) * ma).astype(np.uint8)), (0, 0))
d = ImageDraw.Draw(img)
draw_line(d, "भूकंप आया तो", TOP_FS, MARGIN, (255, 40, 30))
YEL = (255, 225, 0)
if mode == "one":
    s = "इस पुल का क्या होगा"; fs = 300
    while text_w(fs, s, True) + 2 * (fs // 12) > W - 2 * 56: fs -= 2
    fd = ImageFont.truetype(DEV, fs); hgt = fd.getbbox(s, anchor="ls")[3] - fd.getbbox(s, anchor="ls")[1] + 2 * (fs // 12)
    draw_line(d, s, fs, H - MARGIN - hgt, YEL, q=True)
    print("bottom fs", fs)
else:
    fs = 255
    fd = ImageFont.truetype(DEV, fs)
    def h(s): b = fd.getbbox(s, anchor="ls"); return b[3] - b[1] + 2 * (fs // 12)
    y2 = H - MARGIN - h("क्या होगा"); y1 = y2 - h("इस पुल का") + 10
    draw_line(d, "इस पुल का", fs, y1, YEL)
    draw_line(d, "क्या होगा", fs, y2, YEL, q=True)
img.save(f"thumb_v3_{mode}_full.png")
img.resize((1280, 720), Image.LANCZOS).save(f"thumb_v3_{mode}_1280x720.jpg", quality=92)
