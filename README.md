"""
Generate a neofetch-style GitHub README from your photo.
Usage: python ascii_gen.py photo.jpg
Needs: pip install pillow
Tune CROP, COLS, LOW (background cutoff) and GAMMA until your face looks right.
"""
import sys
from PIL import Image, ImageOps

PHOTO = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
CROP  = (120, 60, 380, 340)
COLS  = 56        # width in characters
LOW   = 45        # pixels darker than this become blank (kills the background)
GAMMA = 0.8       # <1 brightens
CHARS = " .:-=+*#%@"

INFO = [
    "your_name@github",
    "-----------------",
    "OS: Kali Linux, macOS",
    "Uptime: X years",
    "Host: YourBrand",
    "Kernel: Your Role / Title",
    "Tools: Tool1, Tool2, Tool3",
    "",
    "Languages.Programming: Python, Bash, TypeScript",
    "Languages.Computer: SQL, HTML, YAML, Markdown",
    "Languages.Real: Persian, English",
    "",
    "Focus.Offense: Web App & API Pentesting",
    "Focus.Research: Vuln Research, Red Teaming",
    "",
    "- Contact",
    "Email: you@example.com",
    "Website: yoursite.com",
    "LinkedIn: your-id",
    "Instagram: your_id",
    "",
    "- GitHub Stats",
    "Repos: 0 | Stars: 0",
    "Commits: 0 | Followers: 0",
]

im = Image.open(PHOTO).convert("L")
if CROP:
    im = im.crop(CROP)
im = ImageOps.autocontrast(im, cutoff=1)
im = im.point(lambda v: int(255 * ((v / 255) ** GAMMA)))
rows = int(COLS * im.height / im.width * 0.5)
im = im.resize((COLS, rows), Image.LANCZOS)

art = []
for y in range(rows):
    row = ""
    for x in range(COLS):
        v = max(0, im.getpixel((x, y)) - LOW) / (255 - LOW)
        row += CHARS[min(len(CHARS) - 1, int(v * len(CHARS)))]
    art.append(row.ljust(COLS))

lines = []
for i in range(max(len(art), len(INFO) + 2)):
    a = art[i] if i < len(art) else " " * COLS
    t = INFO[i - 2] if 0 <= i - 2 < len(INFO) else ""
    lines.append(f"{a}   {t}".rstrip())

with open("README.md", "w", encoding="utf-8") as f:
    f.write("```\n" + "\n".join(lines) + "\n```\n")
print("README.md written")
