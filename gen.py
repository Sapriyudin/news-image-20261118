#!/usr/bin/env python3
"""Variant A — front-page newspaper + world map.

"THE WORLD IN ONE DAY", Wednesday 18 November 2026.
Deterministic local generator (PIL). Run: python3 gen.py -> entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 22, 33)
GREY = (90, 88, 80)
PANEL = (255, 253, 247)
SKY = (196, 209, 216)
SEA = (111, 142, 163)
SEA_DARK = (84, 112, 134)
LAND = (188, 175, 148)
MAP_BG = (232, 227, 211)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                 (-85, 70), (-75, 62), (-60, 55), (-55, 47), (-70, 42),
                 (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-97, 16),
                 (-105, 20), (-110, 24), (-120, 34), (-125, 40), (-125, 49),
                 (-140, 60), (-155, 58), (-165, 60)]
SOUTH_AMERICA = [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8),
                 (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -55),
                 (-73, -40), (-70, -20), (-80, -5), (-80, 10)]
AFRICA = [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
          (35, 28), (40, 15), (43, 11), (48, 10), (51, 12), (40, 0),
          (35, -15), (30, -25), (20, -35), (15, -30), (12, -18), (9, 0),
          (8, 4), (-8, 5), (-17, 15)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
          (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62),
          (25, 65), (20, 70), (15, 70), (5, 58), (5, 53), (-5, 50),
          (-10, 43), (-10, 36)]
ASIA = [(30, 62), (40, 68), (60, 70), (80, 73), (100, 76), (120, 73),
        (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 52),
        (142, 50), (140, 40), (130, 35), (127, 40), (122, 38), (120, 32),
        (110, 20), (108, 10), (105, 8), (100, 7), (95, 15), (90, 22),
        (88, 22), (80, 15), (77, 8), (72, 20), (66, 25), (60, 25),
        (56, 26), (50, 29), (48, 30), (44, 29), (40, 32), (36, 36),
        (30, 36), (28, 40), (30, 45), (30, 55), (30, 62)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
             (132, -32), (137, -35), (140, -38), (145, -38), (150, -37),
             (153, -27), (150, -22), (146, -19), (142, -11), (135, -12),
             (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51),
           (-3, 50)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (144, 44),
         (141, 40), (138, 36), (133, 33)]
CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EUROPE, ASIA,
              AUSTRALIA, BRITAIN, JAPAN]


def draw_map_strip(w, h, dots):
    """World map on its own strip image (PIL clips overflow at the edges).

    Latitude is stretched 1.6x around a lat-25 pivot so continents read
    instead of squashing flat; far north/south tips clip at the strip edge,
    like a normal web map.
    """
    strip = Image.new("RGB", (w, h), MAP_BG)
    dd = ImageDraw.Draw(strip)
    dd.text((12, 6), "WHERE IT HAPPENED — 18 NOVEMBER 2026",
            font=font(SANS_B, 16), fill=INK)
    map_x0, map_y0 = 8, 26
    map_w, map_h = w - 16, h - 34
    k = map_h / 130.0 * 1.6
    cy = map_h * 0.42
    # continents + dots live on their own layer, clipped to the map area
    # below the title (PIL clips drawing to the layer's bounds).
    layer = Image.new("RGB", (map_w, map_h), MAP_BG)
    ld = ImageDraw.Draw(layer)

    def xy(lon, lat):
        x = (lon + 170.0) / 360.0 * map_w
        y = cy + (25.0 - lat) * k
        return (x, y)

    for poly in CONTINENTS:
        ld.polygon([xy(lon, lat) for lon, lat in poly], fill=LAND,
                   outline=(120, 108, 84))
    num_f = font(SANS_B, 13)
    for n, lon, lat in dots:
        px, py = xy(lon, lat)
        ld.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                   outline=(255, 255, 255), width=2)
        lab = str(n)
        lw = ld.textlength(lab, font=num_f)
        ld.text((px - lw / 2, py - 7), lab, font=num_f, fill=(255, 255, 255))
    strip.paste(layer, (map_x0, map_y0))
    return strip


def icon_gulf(d, x, y, s):
    d.arc([x, y + s * 0.15, x + s * 0.55, y + s * 0.7], 180, 360,
          fill=INK, width=4)
    d.line([x + s * 0.27, y + s * 0.42, x + s * 0.27, y + s * 0.85],
           fill=INK, width=4)
    d.line([x + s * 0.05, y + s * 0.85, x + s * 0.5, y + s * 0.85],
           fill=INK, width=4)
    dx, dy = x + s * 0.62, y + s * 0.12
    d.ellipse([dx, dy, dx + s * 0.1, dy + s * 0.1], fill=RED)
    d.line([dx - s * 0.12, dy + s * 0.05, dx + s * 0.22, dy + s * 0.05],
           fill=INK, width=3)
    d.line([dx + s * 0.05, dy - s * 0.08, dx + s * 0.05, dy + s * 0.18],
           fill=INK, width=3)
    d.arc([x, y + s * 0.88, x + s, y + s * 1.08], 180, 360, fill=SEA, width=3)


def icon_plane(d, x, y, s):
    d.ellipse([x + s * 0.68, y, x + s * 0.98, y + s * 0.3],
              fill=(214, 164, 60))
    d.polygon([(x + s * 0.05, y + s * 0.55), (x + s * 0.75, y + s * 0.45),
               (x + s * 0.92, y + s * 0.52), (x + s * 0.75, y + s * 0.62),
               (x + s * 0.05, y + s * 0.68)], fill=INK)
    d.polygon([(x + s * 0.35, y + s * 0.5), (x + s * 0.5, y + s * 0.28),
               (x + s * 0.62, y + s * 0.5)], fill=INK)
    d.polygon([(x + s * 0.3, y + s * 0.62), (x + s * 0.42, y + s * 0.85),
               (x + s * 0.52, y + s * 0.62)], fill=INK)
    d.line([x, y + s * 0.95, x + s, y + s * 0.95], fill=GREY, width=2)


def icon_chip(d, x, y, s):
    d.rectangle([x + s * 0.18, y + s * 0.22, x + s * 0.62, y + s * 0.66],
                fill=INK)
    d.rectangle([x + s * 0.32, y + s * 0.36, x + s * 0.48, y + s * 0.52],
                fill=RED)
    for i in range(4):
        px = x + s * (0.26 + i * 0.11)
        d.line([px, y + s * 0.08, px, y + s * 0.22], fill=INK, width=3)
        d.line([px, y + s * 0.66, px, y + s * 0.8], fill=INK, width=3)
        py = y + s * (0.3 + i * 0.11)
        d.line([x + s * 0.04, py, x + s * 0.18, py], fill=INK, width=3)
        d.line([x + s * 0.62, py, x + s * 0.76, py], fill=INK, width=3)
    d.line([x + s * 0.68, y + s * 0.85, x + s * 0.95, y + s * 0.1],
           fill=RED, width=5)
    d.polygon([(x + s * 0.82, y + s * 0.08), (x + s * 0.98, y + s * 0.08),
               (x + s * 0.95, y + s * 0.24)], fill=RED)


def icon_ban(d, x, y, s):
    d.rectangle([x + s * 0.12, y + s * 0.05, x + s * 0.62, y + s * 0.9],
                outline=INK, width=3, fill=(255, 255, 255))
    for i in range(3):
        yy = y + s * (0.22 + i * 0.16)
        d.line([x + s * 0.22, yy, x + s * 0.52, yy], fill=GREY, width=3)
    d.ellipse([x + s * 0.48, y + s * 0.55, x + s * 0.98, y + s * 1.05],
              outline=RED, width=6)
    d.line([x + s * 0.56, y + s * 0.97, x + s * 0.9, y + s * 0.63],
           fill=RED, width=6)


def icon_flags(d, x, y, s):
    d.line([x + s * 0.2, y + s * 0.1, x + s * 0.2, y + s * 0.95],
           fill=INK, width=3)
    d.line([x + s * 0.78, y + s * 0.1, x + s * 0.78, y + s * 0.95],
           fill=INK, width=3)
    d.rectangle([x + s * 0.2, y + s * 0.12, x + s * 0.48, y + s * 0.42],
                fill=RED)
    d.rectangle([x + s * 0.29, y + s * 0.12, x + s * 0.39, y + s * 0.42],
                fill=(255, 255, 255))
    d.polygon([(x + s * 0.34, y + s * 0.18), (x + s * 0.36, y + s * 0.24),
               (x + s * 0.39, y + s * 0.24), (x + s * 0.37, y + s * 0.28),
               (x + s * 0.38, y + s * 0.34), (x + s * 0.34, y + s * 0.31),
               (x + s * 0.30, y + s * 0.34), (x + s * 0.31, y + s * 0.28),
               (x + s * 0.29, y + s * 0.24), (x + s * 0.32, y + s * 0.24)],
              fill=RED)
    d.rectangle([x + s * 0.5, y + s * 0.12, x + s * 0.78, y + s * 0.42],
                fill=RED)
    d.ellipse([x + s * 0.54, y + s * 0.16, x + s * 0.6, y + s * 0.22],
              fill=(255, 220, 80))
    d.ellipse([x + s * 0.63, y + s * 0.16, x + s * 0.66, y + s * 0.19],
              fill=(255, 220, 80))
    d.ellipse([x + s * 0.63, y + s * 0.24, x + s * 0.66, y + s * 0.27],
              fill=(255, 220, 80))
    d.ellipse([x + s * 0.54, y + s * 0.26, x + s * 0.57, y + s * 0.29],
              fill=(255, 220, 80))


def icon_cyclone(d, x, y, s):
    cx, cy = x + s * 0.5, y + s * 0.42
    for r, a0, a1 in [(s * 0.42, 20, 300), (s * 0.3, 140, 420),
                      (s * 0.18, 260, 540)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=INK, width=4)
    d.ellipse([cx - s * 0.06, cy - s * 0.06, cx + s * 0.06, cy + s * 0.06],
              fill=RED)
    for yy in (y + s * 0.82, y + s * 0.94):
        d.arc([x, yy, x + s, yy + s * 0.22], 180, 360, fill=SEA, width=3)


def icon_cricket(d, x, y, s):
    for i in range(3):
        sx = x + s * (0.28 + i * 0.16)
        d.rectangle([sx, y + s * 0.15, sx + s * 0.07, y + s * 0.75],
                    fill=INK)
    d.line([x + s * 0.28, y + s * 0.1, x + s * 0.44, y + s * 0.1],
           fill=INK, width=4)
    d.line([x + s * 0.44, y + s * 0.1, x + s * 0.6, y + s * 0.1],
           fill=INK, width=4)
    d.ellipse([x + s * 0.68, y + s * 0.62, x + s * 0.9, y + s * 0.84],
              fill=RED)
    d.line([x + s * 0.05, y + s * 0.92, x + s * 0.95, y + s * 0.92],
           fill=GREY, width=3)


def draw_lead_art(d, x, y, w, h):
    """Crimean Bridge: deck across a strait, middle span collapsed."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 78, y + 18, x + w - 28, y + 68], fill=(232, 196, 110))
    for bx, bw, bh in [(18, 34, 52), (58, 26, 78), (90, 40, 44),
                       (136, 30, 66), (172, 24, 40), (w - 150, 30, 58),
                       (w - 112, 26, 44)]:
        d.rectangle([x + bx, y + h - 150 - bh, x + bx + bw, y + h - 150],
                    fill=(168, 176, 182))
    d.rectangle([x, y + h - 150, x + w, y + h], fill=SEA)
    for wy in (y + h - 118, y + h - 88, y + h - 52, y + h - 22):
        for wx in range(0, w, 64):
            d.arc([x + wx, wy, x + wx + 44, wy + 16], 180, 360,
                  fill=SEA_DARK, width=2)
    deck_y = y + h - 168
    # intact deck spans
    d.rectangle([x, deck_y, x + w * 0.42, deck_y + 14], fill=INK)
    d.rectangle([x + w * 0.62, deck_y, x + w, deck_y + 14], fill=INK)
    # fallen span: tilted deck slab half-sunk, with splash
    d.polygon([(x + w * 0.44, deck_y + 4), (x + w * 0.60, deck_y + 4),
               (x + w * 0.55, deck_y + 92), (x + w * 0.40, deck_y + 78)],
              fill=(58, 58, 58))
    d.line([x + w * 0.44, deck_y + 4, x + w * 0.40, deck_y + 78],
           fill=(200, 200, 200), width=3)
    d.arc([x + w * 0.36, deck_y + 82, x + w * 0.62, deck_y + 118],
          180, 360, fill=(235, 240, 242), width=3)
    d.arc([x + w * 0.40, deck_y + 92, x + w * 0.58, deck_y + 122],
          180, 360, fill=(235, 240, 242), width=2)
    # towers + cables
    for tx in (x + w * 0.16, x + w * 0.80):
        d.rectangle([tx - 6, deck_y - 92, tx + 6, deck_y], fill=INK)
    d.line([x + w * 0.16, deck_y - 92, x + w * 0.42, deck_y], fill=INK,
           width=2)
    d.line([x + w * 0.80, deck_y - 92, x + w * 0.62, deck_y], fill=INK,
           width=2)
    # light smoke above the gap
    for sx, sy, sr in [(x + w * 0.50, deck_y - 40, 22),
                       (x + w * 0.54, deck_y - 66, 26),
                       (x + w * 0.47, deck_y - 88, 18)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                  fill=(150, 150, 148))
    # drones
    for dx, dy in [(x + w * 0.30, y + 34), (x + w * 0.42, y + 62),
                   (x + w * 0.68, y + 44)]:
        d.line([dx - 12, dy, dx + 12, dy], fill=INK, width=3)
        d.line([dx, dy - 8, dx, dy + 8], fill=INK, width=3)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
    d.rectangle([x, y + h - 34, x + 206, y + h], fill=RED)
    d.text((x + 12, y + h - 30), "KERCH STRAIT  ·  19 KM",
           font=font(SANS_B, 15), fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    CW = W - 2 * M

    # ---- masthead ------------------------------------------------------
    y = 12
    draw_center(d, W // 2, y, "THE WORLD IN ONE DAY",
                font(SERIF_B, 60), INK)
    y += 74
    draw_center(d, W // 2, y, "WEDNESDAY  ·  18 NOVEMBER 2026",
                font(SANS_B, 25), RED)
    y += 38
    d.rectangle([M, y, W - M, y + 5], fill=RED)
    d.rectangle([M, y + 9, W - M, y + 11], fill=INK)

    # ---- lead story ----------------------------------------------------
    ly, lh, art_w = 142, 292, 470
    d.rectangle([M, ly, M + art_w, ly + lh], outline=INK, width=2)
    draw_lead_art(d, M + 2, ly + 2, art_w - 4, lh - 4)
    tx = M + art_w + 22
    tw = W - M - tx
    d.text((tx, ly + 2), "1  ·  EUROPE — WAR IN UKRAINE",
           font=font(SANS_B, 19), fill=RED)
    head_f = font(SERIF_B, 46)
    hy = ly + 34
    for ln in wrap(d, "CRIMEA BRIDGE CUT IN TWO", head_f, tw):
        d.text((tx, hy), ln, font=head_f, fill=INK)
        hy += 54
    sub_f = font(SANS, 20)
    sub = ("Ukraine hits Putin's 19 km road link a second "
           "day — its biggest drone attack of the war, "
           "1,441 drones in one night — as Russia "
           "pounds Kyiv's bridges.")
    sy = hy + 6
    for ln in wrap(d, sub, sub_f, tw):
        d.text((tx, sy), ln, font=sub_f, fill=GREY)
        sy += 26

    # ---- map strip -----------------------------------------------------
    dots = [(1, 34, 45), (2, 50.5, 26), (3, 121, 14.6), (4, -122, 37),
            (5, 0, 51.5), (6, 114, 22.5), (7, 88, 15), (8, 80, 13)]
    img.paste(draw_map_strip(CW, 142, dots), (M, 442))
    d.rectangle([M, 442, W - M, 442 + 142], outline=INK, width=1)

    # ---- secondary grid ------------------------------------------------
    gy = 592
    gap = 6
    rows, cols = 4, 2
    cell_w = (CW - gap) // cols
    cell_h = (H - M - gy - (rows - 1) * gap) // rows
    stories = [
        (2, "GULF", "GULF DRONES INTERCEPTED",
         "Iran hits US radar in Bahrain; Kuwait too.",
         icon_gulf),
        (3, "ASIA", "TRUMP IN MANILA FOR QUAD TALKS",
         "Ahead of China visit; trio meet Thursday.",
         icon_plane),
        (4, "TECH", "NVIDIA SALES DOUBLE TO $115.8BN",
         "Sales +103%; board: Huang won't return.",
         icon_chip),
        (5, "BRITAIN", "UK SANCTIONS SETTLEMENT FIRMS",
         "Eight firms hit over West Bank settlements.",
         icon_ban),
        (6, "TRADE", "CANADA AND CHINA EXTEND DEALS",
         "Xi meets Carney ahead of the APEC summit.",
         icon_flags),
        (7, "WEATHER", "CYCLONE AKVAN STRENGTHENS",
         "Bay of Bengal storm severe by Thursday.",
         icon_cyclone),
        (8, "SPORT", "DHONI RETIRES FROM THE IPL",
         "India great to mentor Chennai Super Kings.",
         icon_cricket),
    ]
    head_f2 = font(SANS_B, 22)
    sub_f2 = font(SANS, 16)
    kick_f = font(SANS_B, 14)
    for i, (num, kick, head, sub, icon) in enumerate(stories):
        r, c = divmod(i, cols)
        cx = M + c * (cell_w + gap)
        cy = gy + r * (cell_h + gap)
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=PANEL,
                    outline=(200, 192, 172), width=1)
        d.rectangle([cx + 8, cy + 8, cx + 38, cy + 38], fill=RED)
        lab = str(num)
        lw = d.textlength(lab, font=font(SANS_B, 18))
        d.text((cx + 23 - lw / 2, cy + 11), lab, font=font(SANS_B, 18),
               fill=(255, 255, 255))
        icon(d, cx + 46, cy + 12, 56)
        tx2 = cx + 112
        tw2 = cx + cell_w - 10 - tx2
        d.text((tx2, cy + 7), kick, font=kick_f, fill=RED)
        hy2 = cy + 25
        for ln in wrap(d, head, head_f2, tw2)[:2]:
            d.text((tx2, hy2), ln, font=head_f2, fill=INK)
            hy2 += 26
        sy2 = hy2 + 2
        for ln in wrap(d, sub, sub_f2, tw2)[:1]:
            d.text((tx2, sy2), ln, font=sub_f2, fill=GREY)
    # numbers box (last cell)
    r, c = 3, 1
    cx = M + c * (cell_w + gap)
    cy = gy + r * (cell_h + gap)
    d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=INK)
    d.text((cx + 14, cy + 7), "THE DAY IN NUMBERS", font=kick_f,
           fill=(232, 196, 110))
    stats = [("1,441", "drones in one night"),
             ("$115.8bn", "Nvidia Q3 sales"),
             ("19 km", "bridge cut in two"),
             ("8", "firms sanctioned")]
    stat_f = font(SERIF_B, 20)
    stat_s = font(SANS, 14)
    for j, (big, small) in enumerate(stats):
        sx = cx + 14 + (j % 2) * (cell_w // 2)
        sy3 = cy + 32 + (j // 2) * 32
        d.text((sx, sy3), big, font=stat_f, fill=(255, 255, 255))
        bw = d.textlength(big, font=stat_f)
        d.text((sx + bw + 8, sy3 + 5), small, font=stat_s,
               fill=(200, 200, 200))

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
