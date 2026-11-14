#!/usr/bin/env python3
"""
Pixel-art images for the profile README.

Edit CONFIG, then run:

    python3 generate.py

Writes assets/banner.svg and assets/hotbar.svg. Text is drawn pixel by pixel
from the bitmap fonts below, so nothing depends on fonts GitHub would block.
"""
import os
import random
from collections import defaultdict

CONFIG = {
    "name": "3vhy",
    # Hotbar slots: (code of up to 3 characters, full name for the alt text)
    "skills": [
        ("PY", "Python"),
        ("JV", "Java"),
        ("JS", "JavaScript"),
        ("TS", "TypeScript"),
        ("CSS", "HTML and CSS"),
        ("SQL", "SQL"),
        ("GIT", "Git"),
        ("SH", "Bash"),
        ("C++", "C++"),
    ],
    "seed": 7,  # change for a different star and terrain layout
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
PX = 4  # SVG units per art pixel

# A neutral ramp tinted toward the two accents, #44506a (5) and #8290ad (7)
PAL = {
    "0": "#0d1017",
    "1": "#151a25",
    "2": "#1c2231",
    "3": "#262d3f",
    "4": "#323b51",
    "5": "#44506a",
    "6": "#5f6c8a",
    "7": "#8290ad",
    "8": "#a9b3cb",
    "9": "#d3d9e6",
    "a": "#f2f4f9",
}

# Bitmap fonts ('#' = lit). Glyphs can have any width.
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
_F57_LOWER = {  # 9 rows: x-height on rows 2-6, descenders on rows 7-8
    "a": "..... ..... .###. ....# .#### #...# .#### ..... .....",
    "b": "#.... #.... ####. #...# #...# #...# ####. ..... .....",
    "c": "..... ..... .#### #.... #.... #.... .#### ..... .....",
    "d": "....# ....# .#### #...# #...# #...# .#### ..... .....",
    "e": "..... ..... .###. #...# ##### #.... .#### ..... .....",
    "f": "..## .#.. #### .#.. .#.. .#.. .#.. .... ....",
    "g": "..... ..... .#### #...# #...# #...# .#### ....# .###.",
    "h": "#.... #.... ####. #...# #...# #...# #...# ..... .....",
    "i": "# . # # # # # . .",
    "j": "..# ... ..# ..# ..# ..# ..# #.# .#.",
    "k": "#... #... #..# #.#. ##.. #.#. #..# .... ....",
    "l": "#. #. #. #. #. #. .# .. ..",
    "m": "..... ..... ####. #.#.# #.#.# #.#.# #.#.# ..... .....",
    "n": "..... ..... ####. #...# #...# #...# #...# ..... .....",
    "o": "..... ..... .###. #...# #...# #...# .###. ..... .....",
    "p": "..... ..... ####. #...# #...# #...# ####. #.... #....",
    "q": "..... ..... .#### #...# #...# #...# .#### ....# ....#",
    "r": ".... .... #.## ##.. #... #... #... .... ....",
    "s": "..... ..... .#### #.... .###. ....# ####. ..... .....",
    "t": ".#.. .#.. #### .#.. .#.. .#.. ..## .... ....",
    "u": "..... ..... #...# #...# #...# #...# .#### ..... .....",
    "v": "..... ..... #...# #...# #...# .#.#. ..#.. ..... .....",
    "w": "..... ..... #...# #.#.# #.#.# #.#.# .#.#. ..... .....",
    "x": "..... ..... #...# .#.#. ..#.. .#.#. #...# ..... .....",
    "y": "..... ..... #...# #...# #...# #...# .#### ....# .###.",
    "z": "..... ..... ##### ...#. ..#.. .#... ##### ..... .....",
}
F57 = {k: v.split() for k, v in {**_F57, **_F57_LOWER}.items()}
for _g in F57.values():  # pad capitals to the 9-row grid
    _g.extend(["." * len(_g[0])] * (9 - len(_g)))
M35 = {k: v.split() for k, v in _M35.items()}
for _k, _g in F57.items():
    assert len(_g) == 9 and len({len(r) for r in _g}) == 1, _k


# --------------------------------------------------------------------------- #
#  Pixel canvas that writes merged-rectangle SVG paths
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
        self.layers = []

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
#  Scenery
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


# --------------------------------------------------------------------------- #
#  Banner: the name on calm sky, a hillside rising on the right
# --------------------------------------------------------------------------- #
def make_banner(cfg):
    W, H = 320, 120
    rng = random.Random(cfg["seed"])
    name = cfg["name"]
    svg = Svg(W, H, f"{name}, written in pixels over a blocky hillside at night")

    sky = svg.layer()
    bands = [(0, "1"), (84, "2"), (100, "3"), (H, "3")]
    for y in range(H):
        k = max(i for i, (b, _) in enumerate(bands[:-1]) if b <= y)
        nxt_b, nxt_c = bands[k + 1]
        for x in range(W):
            d = nxt_b - y
            c = bands[k][1]
            if d <= 3 and dither(x, y, (4 - d) / 4):
                c = nxt_c
            sky.set(x, y, c)

    scale = max(1, min(5, 150 // max(1, text_width(name))))
    nx, ny = 24, 30
    nw = text_width(name, scale=scale)
    mx, my = 214, 14

    def clear(x, y):
        in_name = nx - 8 <= x <= nx + nw + 8 and ny - 8 <= y <= ny + 9 * scale + 4
        in_moon = mx - 4 <= x <= mx + 16 and my - 4 <= y <= my + 16
        return not (in_name or in_moon)

    stars = svg.layer()
    placed = 0
    while placed < 60:
        x, y = rng.randrange(2, W - 2), rng.randrange(2, 74)
        if clear(x, y):
            stars.set(x, y, rng.choice("5667"))
            placed += 1
    placed = 0
    while placed < 4:
        x, y = rng.randrange(6, W - 6), rng.randrange(4, 60)
        if clear(x - 2, y - 2) and clear(x + 2, y + 2):
            stars.set(x, y, "9")
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                stars.set(x + dx, y + dy, "6")
            placed += 1

    moon = svg.layer()
    moon.rect(mx, my, 12, 12, "9")
    moon.rect(mx + 10, my, 2, 12, "8")
    moon.rect(mx, my + 10, 12, 2, "8")
    moon.rect(mx, my, 10, 1, "a")
    moon.rect(mx, my, 1, 10, "a")
    for cx, cy, cw, ch in ((3, 3, 2, 2), (7, 5, 2, 2), (3, 7, 2, 1)):
        moon.rect(mx + cx, my + cy, cw, ch, "8")

    heights = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 5, 5, 5, 5]
    ground = svg.layer()
    for col, h in enumerate(heights):
        bx = col * 16
        for level in range(h):
            by = H - 16 * (level + 1)
            kind = "grass" if level == h - 1 else ("dirt" if level >= h - 3 else "stone")
            block(ground, bx, by, kind, rng)
        tufts(ground, bx, H - 16 * h, rng)
    tree(ground, 12 * 16 + 8, H - 16 * heights[12], rng)
    tree(ground, 17 * 16 + 8, H - 16 * heights[17], rng)

    draw_text(svg.layer(), name, nx, ny, "9", scale=scale)
    svg.save("banner.svg")


# --------------------------------------------------------------------------- #
#  Hotbar: one still row of inventory slots
# --------------------------------------------------------------------------- #
def make_hotbar(cfg):
    skills = cfg["skills"]
    n = len(skills)
    slot, gap = 30, 2
    total = n * slot + (n - 1) * gap
    W, H = total + 6, slot + 6
    svg = Svg(W, H, "Skills: " + ", ".join(full for _, full in skills))

    bar = svg.layer()
    bar.rect(0, 0, W, H, "2")
    bar.frame(0, 0, W, H, "0")
    bar.rect(1, 1, W - 2, 1, "4")

    inner = slot - 4
    scale = 2 if all(text_width(c, M35, 2) <= inner for c, _ in skills) else 1
    for i, (code, _) in enumerate(skills):
        x, y = 3 + i * (slot + gap), 3
        bar.rect(x, y, slot, slot, "1")
        bar.rect(x, y, slot, 1, "0")
        bar.rect(x, y, 1, slot, "0")
        bar.rect(x, y + slot - 1, slot, 1, "3")
        bar.rect(x + slot - 1, y, 1, slot, "3")
        tw = text_width(code, M35, scale)
        draw_text(bar, code, x + (slot - tw) // 2, y + (slot - 5 * scale) // 2, "9",
                  font=M35, scale=scale, shadow="0", shadow_off=1)
    svg.save("hotbar.svg")


def main():
    make_banner(CONFIG)
    make_hotbar(CONFIG)


if __name__ == "__main__":
    main()
