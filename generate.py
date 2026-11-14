#!/usr/bin/env python3
"""
Pixel-art asset generator for a GitHub profile README.

Edit CONFIG below, then run:

    python3 generate.py

Every image is written to ./assets as a crisp SVG. Text is drawn pixel by pixel
from the bitmap fonts in this file, so nothing depends on fonts or files that
GitHub would block.
"""
import math
import os
import random
from collections import defaultdict

# --------------------------------------------------------------------------- #
#  CONFIG: change these, then re-run the script
# --------------------------------------------------------------------------- #
CONFIG = {
    "greeting": "HI THERE, I'M",
    "name": "3VHY",
    "tagline": "> BUILDING THINGS ONE BLOCK AT A TIME",
    "level": 12,      # number above the XP bar (age, years coding, anything)
    "xp": 0.65,       # how full the XP bar is, 0.0 to 1.0
    "hearts": 10,     # hearts on the left of the status bar
    "gems": 10,       # gems on the right of the status bar
    # Hotbar: (slot code of up to 3 characters, full name shown in the tooltip)
    "skills": [
        ("PY", "PYTHON"),
        ("JV", "JAVA"),
        ("JS", "JAVASCRIPT"),
        ("TS", "TYPESCRIPT"),
        ("CSS", "HTML & CSS"),
        ("SQL", "SQL"),
        ("GIT", "GIT"),
        ("SH", "BASH"),
        ("C++", "C++"),
    ],
    "headers": {      # file name -> (icon, text)
        "about": ("book", "ABOUT ME"),
        "inventory": ("chest", "INVENTORY"),
        "quests": ("scroll", "QUEST LOG"),
        "stats": ("star", "STATS"),
        "contact": ("envelope", "SAY HI"),
    },
    "footer": "THANKS FOR STOPPING BY!",
    "seed": 7,        # change for a different terrain / star layout
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
PX = 4  # SVG units per art pixel

# Palette: a ramp built around the two accents, #44506a (5) and #8290ad (7).
PAL = {
    "0": "#0d1017",
    "1": "#151a25",
    "2": "#1c2231",
    "3": "#262d3f",
    "4": "#323b51",
    "5": "#44506a",  # accent, dark
    "6": "#5f6c8a",
    "7": "#8290ad",  # accent, light
    "8": "#a9b3cb",
    "9": "#d3d9e6",
    "a": "#f2f4f9",
}

# --------------------------------------------------------------------------- #
#  Bitmap fonts ('#' = lit). Glyphs can have any width.
# --------------------------------------------------------------------------- #
_F57 = {
    "A": ".###. #...# #...# ##### #...# #...# #...#",
    "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.",
    "D": "####. #...# #...# #...# #...# #...# ####.",
    "E": "##### #.... #.... ####. #.... #.... #####",
    "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .####",
    "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": "### .#. .#. .#. .#. .#. ###",
    "J": "..### ...#. ...#. ...#. #..#. #..#. .##..",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    "N": "#...# #...# ##..# #.#.# #..## #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.",
    "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#",
    "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.",
    "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.",
    "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# ##.## #...#",
    "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    "0": ".###. #...# #..## #.#.# ##..# #...# .###.",
    "1": "..#.. .##.. ..#.. ..#.. ..#.. ..#.. #####",
    "2": ".###. #...# ....# ..##. .#... #.... #####",
    "3": ".###. #...# ....# ..##. ....# #...# .###.",
    "4": "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    "5": "##### #.... ####. ....# ....# #...# .###.",
    "6": "..##. .#... #.... ####. #...# #...# .###.",
    "7": "##### ....# ...#. ..#.. .#... .#... .#...",
    "8": ".###. #...# #...# .###. #...# #...# .###.",
    "9": ".###. #...# #...# .#### ....# ...#. .##..",
    " ": "... ... ... ... ... ... ...",
    "!": "# # # # # . #",
    ".": ". . . . . . #",
    ",": ".. .. .. .. .. .# #.",
    "'": "# # . . . . .",
    ":": ". # . . . # .",
    "-": "... ... ... ### ... ... ...",
    "_": "..... ..... ..... ..... ..... ..... #####",
    "/": "....# ...#. ...#. ..#.. .#... .#... #....",
    "?": ".###. #...# ....# ...#. ..#.. ..... ..#..",
    "&": ".##.. #..#. .##.. .#... #.#.# #..#. .##.#",
    "+": "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    "#": ".#.#. .#.#. ##### .#.#. ##### .#.#. .#.#.",
    "@": ".###. #...# #.### #.#.# #.### #.... .####",
    "(": "..# .#. #.. #.. #.. .#. ..#",
    ")": "#.. .#. ..# ..# ..# .#. #..",
    ">": "#... .#.. ..#. ...# ..#. .#.. #...",
    "<": "...# ..#. .#.. #... .#.. ..#. ...#",
    "*": "..... #.#.# .###. ##### .###. #.#.# .....",
    "=": "..... ..... ##### ..... ##### ..... .....",
    "|": "# # # # # # #",
    "%": "##..# ##..# ...#. ..#.. .#... #..## #..##",
}
_M35 = {
    "A": ".#. #.# ### #.# #.#",
    "B": "##. #.# ##. #.# ##.",
    "C": ".## #.. #.. #.. .##",
    "D": "##. #.# #.# #.# ##.",
    "E": "### #.. ##. #.. ###",
    "F": "### #.. ##. #.. #..",
    "G": ".## #.. #.# #.# .##",
    "H": "#.# #.# ### #.# #.#",
    "I": "### .#. .#. .#. ###",
    "J": "..# ..# ..# #.# .#.",
    "K": "#.# #.# ##. #.# #.#",
    "L": "#.. #.. #.. #.. ###",
    "M": "#...# ##.## #.#.# #...# #...#",
    "N": "#..# ##.# #.## #..# #..#",
    "O": ".#. #.# #.# #.# .#.",
    "P": "##. #.# ##. #.. #..",
    "Q": ".#. #.# #.# ##. .##",
    "R": "##. #.# ##. #.# #.#",
    "S": ".## #.. .#. ..# ##.",
    "T": "### .#. .#. .#. .#.",
    "U": "#.# #.# #.# #.# ###",
    "V": "#...# #...# .#.#. .#.#. ..#..",
    "W": "#...# #...# #.#.# ##.## #...#",
    "X": "#.# #.# .#. #.# #.#",
    "Y": "#.# #.# .#. .#. .#.",
    "Z": "### ..# .#. #.. ###",
    "0": "### #.# #.# #.# ###",
    "1": ".#. ##. .#. .#. ###",
    "2": "##. ..# .#. #.. ###",
    "3": "##. ..# .#. ..# ##.",
    "4": "#.# #.# ### ..# ..#",
    "5": "### #.. ##. ..# ##.",
    "6": ".## #.. ### #.# ###",
    "7": "### ..# .#. .#. .#.",
    "8": "### #.# ### #.# ###",
    "9": "### #.# ### ..# ##.",
    "+": "... .#. ### .#. ...",
    "#": "#.# ### #.# ### #.#",
    ".": ". . . . #",
    "-": "... ... ### ... ...",
    " ": ".. .. .. .. ..",
    "/": "..# ..# .#. #.. #..",
    "!": "# # # . #",
    "?": "##. ..# .#. ... .#.",
    "&": ".#. #.# .#. #.# .##",
}
F57 = {k: v.split() for k, v in _F57.items()}
M35 = {k: v.split() for k, v in _M35.items()}

# --------------------------------------------------------------------------- #
#  Sprites: 16x16 icons ('.' = transparent, otherwise a palette key)
# --------------------------------------------------------------------------- #
ICONS = {
    "pickaxe": [
        "................",
        "....00000.......",
        "...0999870......",
        "....0678870.....",
        ".....0000870....",
        "........06770...",
        ".......0500760..",
        "......060.0760..",
        ".....050..0660..",
        "....060....060..",
        "...050......0...",
        "..060...........",
        ".050............",
        "060.............",
        ".0..............",
        "................",
    ],
    "book": [
        "................",
        "..000000000000..",
        "..045888888870..",
        "..045777777760..",
        "..045755555760..",
        "..045759995760..",
        "..045755555760..",
        "..045777777760..",
        "..045777777760..",
        "..045777777760..",
        "..045777777760..",
        "..045666666660..",
        "..040999999990..",
        "..040888888880..",
        "..000000000000..",
        "................",
    ],
    "chest": [
        "................",
        "................",
        ".00000000000000.",
        ".08777777777780.",
        ".07666666666650.",
        ".07666666666650.",
        ".000000aa000000.",
        ".07666098066650.",
        ".07666600666650.",
        ".07666666666650.",
        ".04444444444440.",
        ".07666666666650.",
        ".06555555555540.",
        ".00000000000000.",
        "................",
        "................",
    ],
    "scroll": [
        ".00000000000000.",
        ".05888888888850.",
        ".05777777777750.",
        ".00999999999900.",
        "..099999999990..",
        "..096666666990..",
        "..099999999990..",
        "..096666699990..",
        "..099999999990..",
        "..096666666690..",
        "..099999999990..",
        "..099999999990..",
        ".00000000000000.",
        ".05888888888850.",
        ".05777777777750.",
        ".00000000000000.",
    ],
    "heart": [
        "................",
        "..0000....0000..",
        ".099770..077770.",
        "0997777007777760",
        "0977777777777760",
        "0777777777777660",
        "0777777777776660",
        ".07777777777660.",
        "..077777777660..",
        "...0777777660...",
        "....07777660....",
        ".....077660.....",
        "......0760......",
        ".......00.......",
        "................",
        "................",
    ],
    "envelope": [
        "................",
        "................",
        ".00000000000000.",
        ".06999999999960.",
        ".09699999999690.",
        ".09969999996990.",
        ".09996999969990.",
        ".09999699699990.",
        ".09999966999990.",
        ".08999999999980.",
        ".08888888888880.",
        ".07777777777770.",
        ".00000000000000.",
        "................",
        "................",
        "................",
    ],
    "bubble": [
        "................",
        "................",
        "..000000000000..",
        ".08999999999980.",
        ".09999999999980.",
        ".09999999999980.",
        ".09955955955980.",
        ".09955955955980.",
        ".09999999999980.",
        ".08888888888870.",
        "..077000000000..",
        "..0760..........",
        "..00............",
        "................",
        "................",
        "................",
    ],
}

HEART9 = [
    ".000.000.",
    "0a9707770",
    "097777770",
    "077777750",
    ".0777750.",
    "..07750..",
    "...050...",
    "....0....",
]
GEM9 = [
    "..00000..",
    ".0a88760.",
    "0a8877650",
    "067765550",
    ".0676550.",
    "..06550..",
    "...050...",
    "....0....",
]


def _star_icon():
    cx, cy, outer, inner = 7.5, 8.4, 7.9, 3.4
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = outer if i % 2 == 0 else inner
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    def inside(x, y):
        hit = False
        for i in range(len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[i - 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                hit = not hit
        return hit

    mask = {(x, y) for y in range(16) for x in range(16) if inside(x + 0.5, y + 0.5)}
    edge = {p for p in mask if any((p[0] + dx, p[1] + dy) not in mask
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    rows = []
    for y in range(16):
        row = ""
        for x in range(16):
            if (x, y) not in mask:
                row += "."
            elif (x, y) in edge:
                row += "0"
            elif (x - 1, y) in edge or (x, y - 1) in edge:
                row += "9" if x < 8 else "8"
            elif (x + 1, y) in edge or (x, y + 1) in edge:
                row += "6"
            else:
                row += "7"
        rows.append(row)
    return rows


ICONS["star"] = _star_icon()

for _name, _rows in ICONS.items():
    assert len(_rows) == 16 and all(len(r) == 16 for r in _rows), _name


# --------------------------------------------------------------------------- #
#  Tiny pixel canvas that writes merged-rectangle SVG paths
# --------------------------------------------------------------------------- #
class Layer:
    def __init__(self, attrs=""):
        self.px = {}
        self.attrs = attrs

    def set(self, x, y, c):
        self.px[(x, y)] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px[(xx, yy)] = c

    def frame(self, x, y, w, h, c, t=1):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def sprite(self, rows, x, y):
        for yy, row in enumerate(rows):
            for xx, c in enumerate(row):
                if c != ".":
                    self.px[(x + xx, y + yy)] = c


def glyphs(text, font=F57, scale=1, spacing=1):
    """Return ({(x, y): font_row}, width, height) for a text string."""
    pts, x = {}, 0
    for ch in text:
        g = font.get(ch) or font.get(ch.upper()) or font["?"]
        for gy, row in enumerate(g):
            for gx, v in enumerate(row):
                if v == "#":
                    for sy in range(scale):
                        for sx in range(scale):
                            pts[(x + gx * scale + sx, gy * scale + sy)] = gy
        x += (len(g[0]) + spacing) * scale
    height = len(next(iter(font.values()))) * scale
    return pts, max(0, x - spacing * scale), height


def text_width(text, font=F57, scale=1):
    return glyphs(text, font, scale)[1]


def draw_text(layer, text, x, y, color, font=F57, scale=1, shadow=None, shadow_off=None,
              outline=None, extrude=0, extrude_color=None, shade=None, shade_from=99):
    pts, w, h = glyphs(text, font, scale)
    face = {(x + px, y + py): row for (px, py), row in pts.items()}
    ext = set()
    for d in range(1, extrude + 1):
        ext |= {(px, py + d) for (px, py) in face}
    ext -= set(face)
    if outline:
        body = set(face) | ext
        ring = {(px + dx, py + dy) for (px, py) in body
                for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - body
        for p in ring:
            layer.set(*p, outline)
    if shadow:
        off = shadow_off if shadow_off is not None else scale
        for (px, py) in face:
            if (px + off, py + off) not in face:
                layer.set(px + off, py + off, shadow)
    for p in ext:
        layer.set(*p, extrude_color)
    for p, row in face.items():
        layer.set(*p, shade if shade and row >= shade_from else color)
    return w, h


def _rects(points):
    rows = defaultdict(list)
    for x, y in points:
        rows[y].append(x)
    rects, active = [], {}
    for y in sorted(rows):
        xs = sorted(rows[y])
        runs, start, prev = [], xs[0], xs[0]
        for x in xs[1:]:
            if x == prev + 1:
                prev = x
                continue
            runs.append((start, prev + 1))
            start = prev = x
        runs.append((start, prev + 1))
        cur = {}
        for r in runs:
            if r in active and active[r][1] == y:
                active[r][1] = y + 1
                cur[r] = active[r]
            else:
                cur[r] = [y, y + 1]
        for r, span in active.items():
            if cur.get(r) is not span:
                rects.append((r[0], span[0], r[1] - r[0], span[1] - span[0]))
        active = cur
    for r, span in active.items():
        rects.append((r[0], span[0], r[1] - r[0], span[1] - span[0]))
    return rects


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.layers, self.css = [], ""

    def layer(self, attrs=""):
        layer = Layer(attrs)
        self.layers.append(layer)
        return layer

    def render(self):
        W, H = self.w * PX, self.h * PX
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img">',
            f"<title>{esc(self.title)}</title>",
        ]
        if self.css:
            out.append("<style>" + self.css +
                       "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
                       "</style>")
        out.append(f'<g transform="scale({PX})">')
        for layer in self.layers:
            by_color = defaultdict(list)
            for (x, y), c in layer.px.items():
                if 0 <= x < self.w and 0 <= y < self.h:
                    by_color[c].append((x, y))
            if not by_color:
                continue
            out.append(f"<g{(' ' + layer.attrs) if layer.attrs else ''}>")
            for c in sorted(by_color):
                d = "".join(f"M{x} {y}h{w}v{h}h-{w}z" for x, y, w, h in _rects(by_color[c]))
                out.append(f'<path fill="{PAL.get(c, c)}" d="{d}"/>')
            out.append("</g>")
        out.append("</g></svg>")
        return "\n".join(out)

    def save(self, name):
        path = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(self.render())
        print(f"  wrote assets/{name}")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dither(x, y, frac):
    return BAYER[y % 4][x % 4] < frac * 16


# --------------------------------------------------------------------------- #
#  Shared scenery pieces
# --------------------------------------------------------------------------- #
def block(layer, bx, by, kind, rng, ore_chance=0.3):
    """Draw one 16x16 block texture."""
    layer.rect(bx, by, 16, 16, "3" if kind == "stone" else "5")

    def speckle(count, colors, sizes):
        for _ in range(count):
            x, y = rng.randrange(16), rng.randrange(16)
            w, h = rng.choice(sizes)
            layer.rect(bx + x, by + y, min(w, 16 - x), min(h, 16 - y), rng.choice(colors))

    if kind == "stone":
        speckle(10, "4442", ((2, 1), (3, 1), (2, 2), (1, 1)))
        speckle(3, "1", ((1, 1), (2, 1)))
        if rng.random() < ore_chance:
            ox, oy = rng.randint(2, 10), rng.randint(2, 10)
            for _ in range(rng.randint(2, 4)):
                x, y = ox + rng.randint(0, 3), oy + rng.randint(0, 3)
                layer.rect(bx + x, by + y, 2, 2, "8")
                layer.set(bx + x, by + y, "a")
                layer.set(bx + x + 1, by + y + 1, "7")
        return

    speckle(12, "44446", ((1, 1), (2, 1), (1, 2), (2, 1)))
    if kind == "grass":
        d = 3
        for x in range(16):
            d = max(2, min(5, d + rng.choice((-1, 0, 0, 1))))
            depth = d + (2 if rng.random() < 0.12 else 0)
            for y in range(depth):
                r = rng.random()
                c = "8" if (y == 0 and r < 0.4) else ("6" if r < 0.1 else "7")
                layer.set(bx + x, by + y, c)
            layer.set(bx + x, by + depth, "4")


def tufts(layer, x0, top, rng, width=16):
    for x in range(x0, x0 + width):
        r = rng.random()
        if r < 0.07:
            layer.set(x, top - 1, "7")
            if rng.random() < 0.5:
                layer.set(x, top - 2, "8")
        elif r < 0.09:  # little flower
            layer.set(x, top - 1, "6")
            layer.set(x, top - 2, "6")
            layer.set(x, top - 3, "a")


def tree(layer, cx, base, rng):
    layer.rect(cx - 1, base - 10, 1, 10, "5")
    layer.rect(cx, base - 10, 1, 10, "3")
    half = [3, 5, 6, 7, 7, 7, 7, 6, 5, 3]
    top = base - 9 - len(half)
    for i, hw in enumerate(half):
        y = top + i
        for x in range(cx - hw, cx + hw):
            r = rng.random()
            right = x > cx + 1
            low = i > 6
            if i == 0 or x == cx - hw:
                c = "7" if r < 0.5 else "6"
            elif (right or low) and r < 0.45:
                c = "5"
            elif r < 0.22:
                c = "7"
            else:
                c = "6"
            layer.set(x, y, c)
        if i == len(half) - 1:
            for x in range(cx - hw, cx + hw):
                layer.set(x, y, "5" if rng.random() < 0.7 else "4")


def starfield(svg, rng, w, ymax, count, avoid=None, twinkle=8):
    stars = svg.layer()
    for _ in range(count):
        x, y = rng.randrange(1, w - 1), rng.randrange(1, ymax)
        if avoid and avoid(x, y):
            continue
        stars.set(x, y, rng.choice("6678"))
    n = 0
    while n < twinkle:
        x, y = rng.randrange(4, w - 4), rng.randrange(3, ymax - 2)
        if avoid and avoid(x, y):
            continue
        delay = round(rng.uniform(0, 4), 2)
        dur = round(rng.uniform(2.5, 4.5), 2)
        s = svg.layer(f'class="tw" style="animation-duration:{dur}s;animation-delay:{delay}s"')
        s.set(x, y, "a")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s.set(x + dx, y + dy, "7")
        n += 1


TWINKLE_CSS = (".tw{animation:tw 3s step-end infinite}"
               "@keyframes tw{0%{opacity:1}45%{opacity:.25}60%{opacity:1}75%{opacity:.6}}")


# --------------------------------------------------------------------------- #
#  Banner
# --------------------------------------------------------------------------- #
def make_banner(cfg):
    W, H = 320, 120
    rng = random.Random(cfg["seed"])
    svg = Svg(W, H, f"{cfg['greeting']} {cfg['name']}. {cfg['tagline'].lstrip('> ')}")

    # sky: dithered bands
    sky = svg.layer()
    bands = [(0, "1"), (36, "2"), (64, "3"), (90, "4"), (H, "4")]
    for y in range(H):
        k = max(i for i, (b, _) in enumerate(bands[:-1]) if b <= y)
        nxt_b, nxt_c = bands[k + 1]
        for x in range(W):
            d = nxt_b - y
            c = bands[k][1]
            if d <= 3 and dither(x, y, (4 - d) / 4):
                c = nxt_c
            sky.set(x, y, c)

    # moon
    mx, my = 268, 12
    moon = svg.layer()
    for i, (pad, frac) in enumerate(((5, 0.5), (3, 1.0))):
        for y in range(my - pad, my + 14 + pad):
            for x in range(mx - pad, mx + 14 + pad):
                if frac == 1.0 or dither(x, y, frac):
                    moon.set(x, y, "2" if i == 0 else "3")
    moon.rect(mx, my, 14, 14, "9")
    moon.rect(mx + 12, my, 2, 14, "8")
    moon.rect(mx, my + 12, 14, 2, "8")
    moon.rect(mx, my, 12, 1, "a")
    moon.rect(mx, my, 1, 12, "a")
    for (cx, cy, cw, ch) in ((3, 3, 3, 2), (8, 6, 2, 2), (4, 8, 2, 3), (9, 2, 1, 1)):
        moon.rect(mx + cx, my + cy, cw, ch, "8")

    starfield(svg, rng, W, 70, 90,
              avoid=lambda x, y: mx - 6 <= x <= mx + 20 and my - 6 <= y <= my + 20)

    # clouds drift left forever (layer is duplicated one screen to the right)
    clouds = svg.layer('class="drift" opacity="0.9"')
    shapes = [
        (18, 30, [(4, 0, 12, 2), (0, 2, 26, 3), (16, 1, 6, 1)]),
        (120, 18, [(6, 0, 8, 2), (2, 2, 22, 2), (0, 4, 30, 2)]),
        (196, 40, [(3, 0, 10, 2), (0, 2, 18, 3)]),
        (238, 28, [(8, 0, 10, 2), (0, 2, 28, 3), (20, 1, 4, 1)]),
    ]
    for ox, oy, rects in shapes:
        mask = {(ox + x + i, oy + y + j) for x, y, w, h in rects for i in range(w) for j in range(h)}
        for (x, y) in mask:
            c = "4" if (x, y - 1) not in mask else ("2" if (x, y + 1) not in mask else "3")
            clouds.set(x, y, c)
            clouds.set(x + W, y, c)  # copy for seamless wrap

    # terrain
    heights = [4, 4, 3, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 3, 4, 4]
    ground = svg.layer()
    for col, h in enumerate(heights):
        bx = col * 16
        for level in range(h):
            by = H - 16 * (level + 1)
            kind = "grass" if level == h - 1 else ("dirt" if level >= h - 3 else "stone")
            block(ground, bx, by, kind, rng)
        tufts(ground, bx, H - 16 * h, rng)
    tree(ground, 40, H - 16 * heights[2], rng)
    tree(ground, 280, H - 16 * heights[17], rng)

    # fireflies
    for i in range(7):
        x = rng.randrange(60, 260)
        y = rng.randrange(80, 100)
        f = svg.layer(f'class="ff" style="animation-delay:{round(i * 0.9, 1)}s"')
        f.set(x, y, "a")

    # text
    text = svg.layer()
    gw = text_width(cfg["greeting"], scale=2)
    draw_text(text, cfg["greeting"], (W - gw) // 2, 12, "7", scale=2, shadow="0", shadow_off=1)

    name_scale = max(1, min(5, 260 // max(1, text_width(cfg["name"]))))
    nw = text_width(cfg["name"], scale=name_scale)
    draw_text(text, cfg["name"], (W - nw) // 2, 32, "a", scale=name_scale,
              outline="0", extrude=name_scale, extrude_color="5", shade="9", shade_from=4)

    tw = text_width(cfg["tagline"], scale=1)
    tx = (W - tw - 6) // 2
    draw_text(text, cfg["tagline"], tx, 78, "9", shadow="0", shadow_off=1)
    cursor = svg.layer('class="blink"')
    cursor.rect(tx + tw + 2, 78, 4, 7, "7")

    svg.css = (
        TWINKLE_CSS +
        f".drift{{animation:drift 120s steps({W}) infinite}}"
        f"@keyframes drift{{from{{transform:translateX(0)}}to{{transform:translateX(-{W}px)}}}}"
        ".blink{animation:blink 1.1s step-end infinite}"
        "@keyframes blink{50%{opacity:0}}"
        ".ff{opacity:0;animation:ff 6.3s steps(9) infinite}"
        "@keyframes ff{0%{opacity:0;transform:translate(0,0)}15%{opacity:1}"
        "50%{transform:translate(3px,-5px)}85%{opacity:1}100%{opacity:0;transform:translate(0,-10px)}}"
    )
    svg.save("banner.svg")


# --------------------------------------------------------------------------- #
#  Status bar (hearts, XP, coffee)
# --------------------------------------------------------------------------- #
def panel(layer, x, y, w, h, fill="1"):
    layer.rect(x, y, w, h, fill)
    layer.frame(x, y, w, h, "0")
    layer.rect(x + 1, y + 1, w - 2, 1, "3")
    layer.rect(x + 1, y + 1, 1, h - 2, "3")


def make_status(cfg):
    W, H = 320, 30
    svg = Svg(W, H, f"Status bar: {cfg['hearts']} hearts, level {cfg['level']}, "
                    f"{round(cfg['xp'] * 100)}% XP, {cfg['gems']} gems")
    base = svg.layer()
    panel(base, 0, 0, W, H)

    for i in range(cfg["hearts"]):
        base.sprite(HEART9, 6 + i * 10, 5)
    for i in range(cfg["gems"]):
        base.sprite(GEM9, W - 6 - 9 - i * 10, 5)

    label = f"LEVEL {cfg['level']}"
    lw = text_width(label)
    draw_text(base, label, (W - lw) // 2, 5, "8", outline="0")

    x0, x1, y0 = 6, W - 6, 18
    inner = x1 - x0 - 2
    base.rect(x0, y0, x1 - x0, 7, "0")
    base.rect(x0 + 1, y0 + 1, inner, 5, "2")
    for x in range(x0 + 1 + 19, x1 - 1, 19):
        base.rect(x, y0 + 1, 1, 5, "3")

    fill_w = round(inner * max(0.0, min(1.0, cfg["xp"])))
    xp = svg.layer('class="xp"')
    xp.rect(x0 + 1, y0 + 1, fill_w, 5, "7")
    xp.rect(x0 + 1, y0 + 1, fill_w, 1, "8")
    xp.rect(x0 + 1, y0 + 5, fill_w, 1, "6")
    for x in range(x0 + 1 + 19, x0 + 1 + fill_w, 19):
        xp.rect(x, y0 + 1, 1, 5, "6")

    svg.css = (
        ".xp{transform-box:fill-box;transform-origin:0 50%;"
        "animation:grow 1.6s steps(16) both .3s}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    )
    svg.save("status.svg")


# --------------------------------------------------------------------------- #
#  Section headers
# --------------------------------------------------------------------------- #
def make_header(key, icon, label, rng):
    W, H = 320, 22
    svg = Svg(W, H, label.title())
    g = svg.layer()
    g.rect(0, 0, W, H, "3")
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            r = rng.random()
            if r < 0.07:
                g.set(x, y, "4")
            elif r < 0.12:
                g.set(x, y, "2")
    g.frame(0, 0, W, H, "0")
    g.rect(1, 1, W - 2, 1, "5")
    g.rect(1, 1, 1, H - 2, "5")
    g.rect(1, H - 2, W - 2, 1, "1")
    g.rect(W - 2, 1, 1, H - 2, "1")

    # inset icon tile
    g.rect(3, 3, 16, 16, "1")
    g.rect(3, 3, 16, 1, "0")
    g.rect(3, 3, 1, 16, "0")
    g.rect(3, 18, 16, 1, "5")
    g.rect(18, 3, 1, 16, "5")
    g.sprite(ICONS[icon], 3, 3)

    draw_text(g, label, 25, 4, "a", scale=2, shadow="1", shadow_off=2)

    for i, c in enumerate("567"):
        g.rect(W - 26 + i * 7, 9, 4, 4, c)
        g.rect(W - 26 + i * 7, 12, 4, 1, "1")
    svg.save(f"header-{key}.svg")


# --------------------------------------------------------------------------- #
#  Hotbar with an animated selection + tooltip
# --------------------------------------------------------------------------- #
def make_hotbar(cfg):
    skills = cfg["skills"]
    n = len(skills)
    W = 320
    gap = 2
    slot = min(32, (W - 8 - gap * (n - 1)) // n)
    total = n * slot + (n - 1) * gap
    px0 = (W - total - 6) // 2
    sx0, sy = px0 + 3, 27
    H = sy + slot + 5
    names = ", ".join(full for _, full in skills)
    svg = Svg(W, H, f"Skill hotbar: {names}")

    bar = svg.layer()
    bar.rect(px0, 24, total + 6, slot + 6, "3")
    bar.frame(px0, 24, total + 6, slot + 6, "0")
    bar.rect(px0 + 1, 25, total + 4, 1, "5")
    bar.rect(px0 + 1, 24 + slot + 4, total + 4, 1, "1")

    inner = slot - 4
    scale = 2 if all(text_width(c, M35, 2) <= inner for c, _ in skills) else 1
    for i, (code, _) in enumerate(skills):
        x = sx0 + i * (slot + gap)
        bar.rect(x, sy, slot, slot, "2")
        bar.rect(x, sy, slot, 1, "1")
        bar.rect(x, sy, 1, slot, "1")
        bar.rect(x, sy + slot - 1, slot, 1, "4")
        bar.rect(x + slot - 1, sy, 1, slot, "4")
        tw = text_width(code, M35, scale)
        th = 5 * scale
        draw_text(bar, code, x + (slot - tw) // 2, sy + (slot - th) // 2, "9",
                  font=M35, scale=scale, shadow="0", shadow_off=1)

    step = 2.2
    dur = round(step * n, 2)
    sel = svg.layer('class="sel"')
    sel.frame(sx0 - 2, sy - 2, slot + 4, slot + 4, "a", 2)
    sel.frame(sx0 - 1, sy - 1, slot + 2, slot + 2, "8")

    for i, (_, full) in enumerate(skills):
        style = f'style="animation-delay:{round(i * step, 2)}s"'
        tip = svg.layer(f'class="tip{" first" if i == 0 else ""}" {style}')
        tw = text_width(full, scale=2)
        bw = tw + 10
        bx = (W - bw) // 2
        tip.rect(bx, 1, bw, 20, "1")
        tip.frame(bx, 1, bw, 20, "0")
        tip.frame(bx + 1, 2, bw - 2, 18, "7")
        draw_text(tip, full, bx + 5, 4, "a", scale=2, shadow="0", shadow_off=1)

    pitch = slot + gap
    frames = "".join(f"{round(100 * i / n, 3)}%{{transform:translateX({i * pitch}px)}}"
                     for i in range(n))
    vis = round(100 / n, 3)
    svg.css = (
        f".sel{{animation:sel {dur}s step-end infinite}}"
        f"@keyframes sel{{{frames}100%{{transform:translateX(0)}}}}"
        f".tip{{opacity:0;animation:tip {dur}s step-end infinite}}.tip.first{{opacity:1}}"
        f"@keyframes tip{{0%{{opacity:1}}{vis}%{{opacity:0}}100%{{opacity:0}}}}"
    )
    svg.save("hotbar.svg")


# --------------------------------------------------------------------------- #
#  Footer strip
# --------------------------------------------------------------------------- #
def make_footer(cfg):
    W, H = 320, 56
    rng = random.Random(cfg["seed"] + 1)
    svg = Svg(W, H, cfg["footer"].title())
    sky = svg.layer()
    for y in range(24):
        for x in range(W):
            sky.set(x, y, "2" if (y >= 20 and dither(x, y, (y - 19) / 4)) else "1")
    starfield(svg, rng, W, 20, 40, twinkle=4,
              avoid=lambda x, y: 60 <= x <= 260 and 5 <= y <= 17)
    ground = svg.layer()
    for col in range(W // 16):
        block(ground, col * 16, 24, "grass", rng)
        block(ground, col * 16, 40, "stone", rng, ore_chance=0.35)
        tufts(ground, col * 16, 24, rng)
    text = svg.layer()
    tw = text_width(cfg["footer"])
    draw_text(text, cfg["footer"], (W - tw) // 2, 8, "8", shadow="0", shadow_off=1)
    svg.css = TWINKLE_CSS
    svg.save("footer.svg")


# --------------------------------------------------------------------------- #
#  Inline icons
# --------------------------------------------------------------------------- #
def make_icons():
    for name, rows in ICONS.items():
        svg = Svg(16, 16, name.title())
        svg.layer().sprite(rows, 0, 0)
        svg.save(f"icons/{name}.svg")


def main():
    print("Generating pixel art...")
    make_banner(CONFIG)
    make_status(CONFIG)
    rng = random.Random(CONFIG["seed"] + 2)
    for key, (icon, label) in CONFIG["headers"].items():
        make_header(key, icon, label, rng)
    make_hotbar(CONFIG)
    make_footer(CONFIG)
    make_icons()
    print("Done.")


if __name__ == "__main__":
    main()
