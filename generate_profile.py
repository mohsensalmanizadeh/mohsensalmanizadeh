"""
Neon cyberpunk GitHub profile card generator.
  pip install pillow opencv-python-headless numpy
  python generate_profile.py photo.jpg
Output: profile.svg  (+ README.md that embeds it)
Edit CONFIG below, then run again.
"""
import sys
from html import escape
from PIL import Image, ImageOps, ImageFilter

# ===================== CONFIG (edit me) =====================
CONFIG = {
    "username":  "mohsensalmanizadeh",
    "name":      "Mohsen Salmanizadeh",
    "tagline":   "Front-End Developer  //  Always Learning",
    "title_bar": "mohsensalmanizadeh",
    "info": [("OS", "Front-End Developer"), ("Role", "Web Developer"),
             ("Focus", "Modern Web Development"), ("Status", "Always Learning")],
    # (name, level 0..20)
    "languages": [("HTML", 14), ("CSS", 14), ("JavaScript", 14)],
    "tools": ["Tailwind CSS", "WordPress", "React", "Git", "GitHub"],
    "interests": ["UI/UX Design", "Web Performance", "Responsive Design", "Clean Code"],
    "contact": [("globe", "Website", "webilio.ir"),
                ("github", "GitHub", "mohsensalmanizadeh"),
                ("linkedin", "LinkedIn", "Mohsen Salmanizadeh"),
                ("x", "X", "@mohsen_cw"),
                ("telegram", "Telegram", "@Uronik"),
                ("mail", "Email", "mohsensalmanizadeh67@gmail.com")],
    "footer": "ALWAYS LEARNING",
}
PHOTO = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
CROP  = (40, 50, 420, 430)     # (left, top, right, bottom) around head+shoulders
COLS, GAMMA, LOW = 186, 1.0, 22
# ============================================================

W, H = 1536, 1024
FONT = "'JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace"
PURPLE, VIOLET, ORANGE, WHITE, BLUE, BG = "#a855f7", "#7c3aed", "#f5a623", "#e8e6f5", "#60a5fa", "#07060f"
LEVELS = ["#7050e8", "#9275f8", "#bca6ff", "#e8deff"]

# ---------- ASCII art ----------
import cv2, numpy as np
def prepare(path, crop):
    l, t, r, b = crop
    bgr = cv2.imread(path)[t:b, l:r]
    h, w = bgr.shape[:2]
    sx, sy = w / 380, h / 380
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # background removal (grabCut seeded for a head+shoulders portrait)
    mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    def R(x0, y0, x1, y1, v): cv2.rectangle(mask, (int(x0*sx), int(y0*sy)), (int(x1*sx), int(y1*sy)), v, -1)
    def E(cx, cy, rx, ry, v): cv2.ellipse(mask, (int(cx*sx), int(cy*sy)), (int(rx*sx), int(ry*sy)), 0, 0, 360, v, -1)
    R(20, 8, 340, 375, cv2.GC_PR_FGD); R(0, 0, 100, 285, cv2.GC_BGD)
    R(305, 0, 380, 250, cv2.GC_BGD); R(0, 0, 380, 12, cv2.GC_BGD)
    E(205, 75, 85, 50, cv2.GC_FGD); E(205, 170, 55, 75, cv2.GC_FGD); R(110, 290, 330, 375, cv2.GC_FGD)
    bg = np.zeros((1, 65)); fg = np.zeros((1, 65))
    cv2.grabCut(bgr, mask, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    m = cv2.GaussianBlur(cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), (5, 5), 0)
    cl = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6)).apply(gray)
    return Image.fromarray((cl.astype(float) * (m / 255.)).astype(np.uint8))
im = prepare(PHOTO, CROP)
CW, PITCH, FS = 3.12, 3.5, 5.2
rows = int(COLS * CW / PITCH * im.height / im.width)
im = im.resize((COLS, rows), Image.LANCZOS)
CHARS = " .-:=+*#"
ART_X, ART_Y = 50, 118
art = []
for y in range(rows):
    runs, cur, buf = [], None, ""
    for x in range(COLS):
        v = max(0, im.getpixel((x, y)) - LOW) / (255 - LOW)
        ch = CHARS[min(len(CHARS)-1, int((v ** 0.85) * len(CHARS)))]
        lv = min(3, int((v ** 0.6) * 4))
        if ch == " ":
            lv = -1
        if lv != cur and buf:
            runs.append((cur, buf)); buf = ""
        cur = lv; buf += ch
    runs.append((cur, buf))
    ts = "".join(
        f'<tspan fill="{LEVELS[l]}">{escape(t)}</tspan>' if l >= 0 else escape(t)
        for l, t in runs)
    art.append(f'<text x="{ART_X}" y="{ART_Y + y*PITCH:.1f}" textLength="{COLS*CW:.1f}" '
               f'lengthAdjust="spacing" xml:space="preserve">{ts}</text>')

# ---------- icons ----------
GH = ("M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12")
def icon(kind, x, y, c="#8b7cf6"):
    s = 22
    if kind == "github":
        return f'<path d="{GH}" fill="{c}" transform="translate({x},{y}) scale({s/24})"/>'
    if kind == "globe":
        return (f'<g transform="translate({x},{y})" fill="none" stroke="{c}" stroke-width="1.8">'
                f'<circle cx="11" cy="11" r="9.5"/><ellipse cx="11" cy="11" rx="4" ry="9.5"/>'
                f'<line x1="1.5" y1="11" x2="20.5" y2="11"/></g>')
    if kind == "linkedin":
        return (f'<g transform="translate({x},{y})"><rect width="22" height="22" rx="3" fill="{c}"/>'
                f'<text x="4" y="17" font-family="{FONT}" font-size="14" font-weight="700" fill="{BG}">in</text></g>')
    if kind == "x":
        return (f'<g transform="translate({x},{y})" stroke="{c}" stroke-width="2.4" stroke-linecap="round">'
                f'<line x1="2" y1="2" x2="20" y2="20"/><line x1="20" y1="2" x2="2" y2="20"/></g>')
    if kind == "telegram":
        return (f'<path transform="translate({x},{y})" fill="{c}" '
                f'd="M21 1 1 9l6 2 2 7 3-4 5 4zM8 11l9-6-7 8z" fill-rule="evenodd"/>')
    if kind == "mail":
        return (f'<g transform="translate({x},{y+3})" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round">'
                f'<rect x="1" y="1" width="20" height="15" rx="2.5"/><path d="M1.5 3l9.5 7.5L20.5 3"/></g>')
    return ""

def section(title, y, x=688, color=PURPLE, end=1488):
    w = len(title) * 13.2 + 16
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="21" font-weight="600">{escape(title)}</text>'
            f'<line x1="{x+w}" y1="{y-7}" x2="{end}" y2="{y-7}" stroke="{color}" stroke-opacity=".7" stroke-dasharray="5 4"/>')

c = CONFIG
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
o.append(f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#5b21b6"/><stop offset="1" stop-color="#a855f7"/></linearGradient>'
         f'<filter id="glow"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
o.append(f'<rect x="18" y="20" width="1500" height="984" rx="18" fill="#0a0817" stroke="{VIOLET}" stroke-width="2"/>')
# title bar
o.append(f'<line x1="18" y1="74" x2="1518" y2="74" stroke="{VIOLET}" stroke-opacity=".5"/>')
for cx, col in ((49, "#ff5f57"), (85, "#febc2e"), (120, "#28c840")):
    o.append(f'<circle cx="{cx}" cy="47" r="10.5" fill="{col}"/>')
o.append(icon("github", 170, 28, "#e8e6f5").replace("scale(0.9166666666666666)", "scale(1.67)"))
o.append(f'<line x1="230" y1="22" x2="230" y2="74" stroke="{VIOLET}" stroke-opacity=".5"/>')
o.append(f'<text x="248" y="54" fill="{WHITE}" font-size="20">{escape(c["title_bar"])}</text>')
o.append(f'<g transform="translate(1478,36)" fill="none" stroke="#8b7cf6" stroke-width="2"><rect x="6" y="0" width="16" height="18" rx="3"/><path d="M3 5v15a3 3 0 0 0 3 3h12"/></g>')
# art
o.append(f'<g font-size="{FS}" transform="translate(-24,-76) scale(1.2)" opacity=".98">' + "".join(art) + '</g>')
# name block
o.append(f'<text x="58" y="802" fill="{PURPLE}" font-size="42" font-weight="700" filter="url(#glow)">{escape(c["name"])}</text>')
o.append(f'<text x="58" y="843" fill="{WHITE}" font-size="23" xml:space="preserve">{escape(c["tagline"])}</text>')
o.append(f'<line x1="58" y1="873" x2="610" y2="873" stroke="{VIOLET}" stroke-opacity=".6"/>')
o.append(f'<text x="58" y="916" fill="{VIOLET}" font-size="22">~/</text><rect x="95" y="898" width="14" height="24" fill="{PURPLE}"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>')
# header
o.append(f'<text x="688" y="111" font-size="25"><tspan fill="{PURPLE}" font-weight="700">{escape(c["username"])}</tspan><tspan fill="{WHITE}">@github</tspan></text>')
o.append(f'<line x1="688" y1="132" x2="1488" y2="132" stroke="{PURPLE}" stroke-opacity=".6" stroke-dasharray="6 4"/>')
y = 172
for k, v in c["info"]:
    o.append(f'<text x="690" y="{y}" fill="{ORANGE}" font-size="22">{escape(k)}</text>'
             f'<text x="866" y="{y}" fill="{ORANGE}" font-size="22">:</text>'
             f'<text x="892" y="{y}" fill="{WHITE}" font-size="22">{escape(v)}</text>')
    y += 29.5
# languages
o.append(section("Languages", 303))
y = 340
for n, lv in c["languages"]:
    o.append(f'<text x="690" y="{y}" fill="{ORANGE}" font-size="22">{escape(n)}</text><text x="842" y="{y}" fill="{ORANGE}" font-size="22">:</text>')
    for i in range(20):
        fill = "url(#g)" if i < lv else "#1a1530"
        o.append(f'<rect x="{869 + i*15.5:.1f}" y="{y-17}" width="13" height="18" fill="{fill}"/>')
    y += 29
# tools
o.append(section("Frameworks & Tools", 440))
o.append(f'<text x="690" y="476" fill="{WHITE}" font-size="21">' + f'  <tspan fill="{PURPLE}">|</tspan>  '.join(escape(t) for t in c["tools"]) + '</text>')
# interests
o.append(section("Interests", 518))
il = c["interests"]
o.append(f'<text x="690" y="554" fill="{WHITE}" font-size="21" xml:space="preserve">' + f'  <tspan fill="{PURPLE}">|</tspan>  '.join(escape(t) for t in il[:3]) + '</text>')
if len(il) > 3:
    o.append(f'<text x="690" y="583" fill="{WHITE}" font-size="21">' + f'  <tspan fill="{PURPLE}">|</tspan>  '.join(escape(t) for t in il[3:]) + '</text>')
# contact
o.append(section("Contact", 625, color=ORANGE))
y = 663
for ic, k, v in c["contact"]:
    o.append(icon(ic, 695, y - 18))
    o.append(f'<text x="746" y="{y}" fill="{ORANGE}" font-size="22">{escape(k)}</text>'
             f'<text x="892" y="{y}" fill="{ORANGE}" font-size="22">:</text>'
             f'<text x="918" y="{y}" fill="{BLUE}" font-size="22">{escape(v)}</text>')
    y += 29
# footer
o.append(f'<line x1="52" y1="972" x2="516" y2="972" stroke="{VIOLET}"/><line x1="1020" y1="972" x2="1484" y2="972" stroke="{VIOLET}"/>')
o.append(f'<text x="768" y="979" fill="{PURPLE}" font-size="23" text-anchor="middle" letter-spacing="3">&lt;/&gt;  {escape(c["footer"])}  &lt;/&gt;</text>')
o.append('</svg>')
open("profile.svg", "w", encoding="utf-8").write("\n".join(o))
open("README.md", "w", encoding="utf-8").write(
    '<div align="center">\n\n![profile](profile.svg)\n\n'
    '[Website](https://webilio.ir) · [LinkedIn](https://www.linkedin.com/in/mohsen-salmanizadeh-b16688349/) · '
    '[X](https://x.com/mohsen_cw) · [Telegram](https://t.me/Uronik) · [Email](mailto:mohsensalmanizadeh67@gmail.com)\n\n</div>\n')
print("profile.svg + README.md written")
