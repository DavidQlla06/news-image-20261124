#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261124.

Fresh code written in-session on 24 Nov 2026. Draws a map-led newspaper
front page for Tuesday 24 November 2026: masthead, lead story (Nvidia /
Huang reinstatement), world map with 13 numbered pins, a numbered key,
12 brief cards and a 6-item ticker. Deterministic: no clock, no random.
Output: 1024x1024 PNG, well under 1 MiB.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (96, 90, 78)
RULE = (60, 56, 48)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREEN = (22, 101, 52)
LAND = (206, 198, 178)
LAND_EDGE = (125, 118, 99)
CARD_BG = (255, 255, 255)
CARD_EDGE = (205, 198, 184)
SEA = (233, 230, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def load_stories():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        return json.load(fh)


# --- simplified continent outlines (lon, lat), rough but recognisable ---
NORTH_AMERICA = [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 57),
                 (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29),
                 (-110, 24), (-105, 20), (-97, 16), (-92, 14), (-87, 13),
                 (-83, 9), (-79, 9), (-77, 7), (-80, 8), (-84, 12), (-87, 15),
                 (-90, 14), (-91, 18), (-94, 19), (-97, 22), (-97, 26),
                 (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
                 (-76, 35), (-74, 39), (-70, 42), (-68, 44), (-66, 45),
                 (-60, 47), (-55, 52), (-60, 55), (-65, 58), (-68, 58),
                 (-72, 62), (-78, 62), (-85, 66), (-90, 69), (-95, 69),
                 (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-44, 60), (-40, 64), (-32, 68), (-22, 70), (-25, 76),
             (-40, 80), (-55, 80), (-58, 76), (-55, 70), (-50, 64)]
SOUTH_AMERICA = [(-77, 7), (-75, 10), (-72, 12), (-64, 10), (-60, 8),
                 (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-35, -15),
                 (-39, -22), (-48, -28), (-52, -33), (-58, -38), (-62, -41),
                 (-65, -45), (-68, -50), (-70, -54), (-73, -50), (-73, -40),
                 (-72, -30), (-70, -20), (-75, -15), (-80, -8), (-81, -3),
                 (-80, 2), (-77, 6)]
AFRICA = [(-17, 15), (-16, 20), (-10, 30), (-6, 33), (0, 36), (10, 37),
          (11, 34), (20, 32), (25, 32), (30, 31), (32, 31), (34, 28),
          (36, 22), (39, 18), (43, 12), (48, 11), (51, 10), (48, 2),
          (42, -2), (40, -10), (38, -18), (35, -24), (32, -29), (28, -33),
          (20, -35), (16, -29), (14, -22), (12, -15), (13, -10), (12, -6),
          (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12)]
EUROPE = [(-10, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 50),
          (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (13, 56), (18, 56),
          (21, 55), (21, 58), (24, 59), (28, 60), (30, 61), (28, 65),
          (25, 69), (20, 70), (15, 69), (12, 66), (10, 62), (6, 58),
          (5, 60), (-5, 58), (-8, 55), (-10, 52), (-10, 48), (-9, 43)]
ASIA = [(30, 61), (32, 64), (35, 67), (40, 68), (48, 68), (55, 69),
        (62, 70), (70, 72), (78, 73), (88, 75), (100, 76), (110, 74),
        (120, 73), (130, 72), (140, 72), (150, 70), (158, 68), (162, 65),
        (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 59),
        (142, 54), (140, 48), (138, 44), (135, 38), (130, 35), (127, 33),
        (122, 31), (120, 27), (116, 23), (110, 20), (108, 15), (105, 10),
        (103, 8), (100, 7), (98, 10), (96, 15), (94, 17), (92, 21),
        (89, 22), (86, 20), (83, 17), (80, 15), (77, 8), (75, 10),
        (72, 20), (70, 23), (66, 25), (62, 25), (58, 26), (54, 27),
        (52, 29), (49, 30), (47, 30), (44, 29), (42, 31), (40, 35),
        (38, 38), (36, 36), (34, 36), (32, 38), (30, 36)]
AUSTRALIA = [(114, -22), (113, -26), (115, -32), (118, -35), (124, -33),
             (129, -32), (132, -32), (136, -35), (140, -38), (146, -39),
             (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
             (142, -15), (142, -11), (137, -12), (135, -12), (132, -11),
             (130, -13), (126, -14), (124, -16), (122, -17), (118, -20),
             (114, -21)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
               (174, -42), (171, -44), (168, -46)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (1, 51), (-2, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (141, 39),
         (141, 42), (143, 44), (145, 44), (143, 42), (141, 38), (139, 35),
         (136, 33), (133, 32)]
INDONESIA = [(95, 5), (98, 3), (100, 0), (103, -2), (106, -6), (110, -7),
             (114, -8), (118, -9), (120, -10), (119, -5), (117, -2),
             (114, 1), (110, 2), (106, 3), (102, 5)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
              (147, -9), (142, -8), (137, -6), (132, -4)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (50, -20), (47, -24),
              (45, -25), (43, -22), (43, -18)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE,
              ASIA, AUSTRALIA, NEW_ZEALAND, BRITAIN, JAPAN, INDONESIA,
              NEW_GUINEA, MADAGASCAR]

# Map geometry: equirectangular, lon -180..180 -> x, lat 78..-58 -> y.
MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 20, 300, 1004, 524


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (78.0 - lat) / 136.0 * (MAP_Y1 - MAP_Y0)
    return x, y


# Pixel nudges so neighbouring pins never overlap (pin: (dx, dy)).
PIN_NUDGE = {6: (-38, 6), 7: (12, 4), 12: (-12, -5)}


def draw_map(draw, pinned):
    draw.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=SEA,
                   outline=CARD_EDGE, width=1)
    # graticule every 30 degrees
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0)
        draw.line([(x, MAP_Y0), (x, MAP_Y1)], fill=(226, 222, 210), width=1)
    for lat in range(60, -59, 30):
        _, y = project(0, lat)
        draw.line([(MAP_X0, y), (MAP_X1, y)], fill=(226, 222, 210), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # equator label
    _, y_eq = project(0, 0)
    draw.text((MAP_X1 - 62, y_eq + 3), "EQUATOR", font=F_SANS(9),
              fill=(150, 144, 128))
    for p in pinned:
        x, y = project(p["lon"], p["lat"])
        dx, dy = PIN_NUDGE.get(p["n"], (0, 0))
        x, y = x + dx, y + dy
        r = 10
        draw.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        label = str(p["n"])
        tw = draw.textlength(label, font=F_SANS_B(11))
        draw.text((x - tw / 2, y - 8), label, font=F_SANS_B(11),
                  fill=(255, 255, 255))


def draw_header(draw):
    draw.text((20, 10), "THE WORLD IN ONE PAGE", font=F_SERIF_B(40),
              fill=INK)
    draw.text((20, 56), "31 STORIES  ·  EVERY REGION  ·  WHAT HAPPENED TODAY",
              font=F_SANS_B(13), fill=RED)
    date_txt = "TUESDAY 24 NOVEMBER 2026"
    tw = draw.textlength(date_txt, font=F_SANS_B(16))
    draw.text((1004 - tw, 16), date_txt, font=F_SANS_B(16), fill=NAVY)
    draw.text((1004 - draw.textlength("24 NOV 2026 — EDITION 24", font=F_SANS(11)),
               40), "24 NOV 2026 — EDITION 24", font=F_SANS(11), fill=MUTED)
    draw.line([(20, 84), (1004, 84)], fill=RULE, width=2)
    draw.line([(20, 88), (1004, 88)], fill=RULE, width=1)


def draw_lead(draw, lead):
    y0, y1 = 96, 272
    draw.rectangle([20, y0, 1004, y1], fill=CARD_BG, outline=CARD_EDGE,
                   width=1)
    draw.rectangle([20, y0, 1004, y0 + 4], fill=RED)
    # left: headline + copy
    draw.text((36, y0 + 16), "LEAD STORY — BUSINESS · USA",
              font=F_SANS_B(12), fill=RED)
    draw.text((36, y0 + 36), lead["headline"], font=F_SERIF_B(50), fill=INK)
    sub_lines = wrap(draw, lead["sub"], F_SANS_B(17), 600)
    yy = y0 + 92
    for ln in sub_lines:
        draw.text((36, yy), ln, font=F_SANS_B(17), fill=NAVY)
        yy += 22
    det_lines = wrap(draw, lead["detail"], F_SANS(13), 600)
    for ln in det_lines:
        draw.text((36, yy), ln, font=F_SANS(13), fill=MUTED)
        yy += 17
    # right: drawn NVDA chip + rising chart
    x0, x1 = 700, 988
    draw.rectangle([x0, y0 + 14, x1, y1 - 14], fill=(235, 245, 235),
                   outline=(180, 200, 180), width=1)
    # chip
    cx0, cy0, cx1, cy1 = 724, y0 + 30, 844, y0 + 118
    for gx in range(cx0 + 14, cx1 - 10, 16):
        draw.line([(gx, cy0 - 8), (gx, cy0)], fill=(176, 141, 43), width=3)
        draw.line([(gx, cy1), (gx, cy1 + 8)], fill=(176, 141, 43), width=3)
    for gy in range(cy0 + 14, cy1 - 10, 16):
        draw.line([(cx0 - 8, gy), (cx0, gy)], fill=(176, 141, 43), width=3)
        draw.line([(cx1, gy), (cx1 + 8, gy)], fill=(176, 141, 43), width=3)
    draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=10, fill=GREEN,
                           outline=(12, 60, 30), width=2)
    draw.rounded_rectangle([cx0 + 16, cy0 + 16, cx1 - 16, cy1 - 16], radius=6,
                           outline=(255, 255, 255), width=1)
    t = "NVDA"
    tw = draw.textlength(t, font=F_SANS_B(26))
    draw.text((cx0 + (cx1 - cx0 - tw) / 2, cy0 + 30), t,
              font=F_SANS_B(26), fill=(255, 255, 255))
    # rising chart line (right of the chip, below the +27% label)
    pts = [(850, y1 - 40), (880, y1 - 50), (910, y1 - 66), (940, y1 - 82)]
    draw.line(pts, fill=GREEN, width=4, joint="curve")
    draw.polygon([(940, y1 - 82), (924, y1 - 76), (936, y1 - 64)],
                 fill=GREEN)
    draw.text((858, y0 + 30), "+27%", font=F_SANS_B(30), fill=GREEN)
    draw.text((858, y0 + 66), "in a day", font=F_SANS(13), fill=MUTED)
    draw.text((724, y1 - 34), "≈ $1 TRILLION ADDED IN VALUE",
              font=F_SANS_B(12), fill=INK)


def draw_key(draw, pinned):
    draw.text((20, 532), "13 ON THE MAP — THE DAY'S OTHER BIG STORIES",
              font=F_SANS_B(13), fill=INK)
    draw.line([(20, 550), (1004, 550)], fill=RULE, width=1)
    # three columns: 5 + 4 + 4 items
    cols = [pinned[0:5], pinned[5:9], pinned[9:13]]
    x_starts = [20, 352, 684]
    col_w = [316, 316, 320]
    for ci, col in enumerate(cols):
        yy = 556
        for p in col:
            badge_r = 8
            draw.ellipse([x_starts[ci], yy, x_starts[ci] + 16, yy + 16],
                         fill=RED)
            lab = str(p["n"])
            tw = draw.textlength(lab, font=F_SANS_B(10))
            draw.text((x_starts[ci] + 8 - tw / 2, yy + 2), lab,
                      font=F_SANS_B(10), fill=(255, 255, 255))
            txt = trunc(draw, p["headline"], F_SANS_B(12), col_w[ci] - 24)
            draw.text((x_starts[ci] + 22, yy + 1), txt, font=F_SANS_B(12),
                      fill=INK)
            yy += 17


def draw_cards(draw, briefs):
    x0, y0 = 20, 648
    cw, ch, gap = 312, 74, 12
    for i, b in enumerate(briefs):
        r, c = divmod(i, 3)
        x = x0 + c * (cw + gap)
        y = y0 + r * (ch + 6)
        draw.rectangle([x, y, x + cw, y + ch], fill=CARD_BG,
                       outline=CARD_EDGE, width=1)
        draw.rectangle([x, y, x + 4, y + ch], fill=NAVY)
        draw.text((x + 12, y + 7), b["region"], font=F_SANS_B(10),
                  fill=RED)
        lines = wrap(draw, b["headline"], F_SANS_B(14), cw - 24)
        yy = y + 22
        for ln in lines[:2]:
            draw.text((x + 12, yy), ln, font=F_SANS_B(14), fill=INK)
            yy += 17
        if len(lines) > 2:
            # squeeze: replace last line with truncated full headline
            pass
        summ = trunc(draw, b["summary"], F_SANS(11), cw - 24)
        draw.text((x + 12, y + ch - 18), summ, font=F_SANS(11),
                  fill=MUTED)


def draw_ticker(draw, ticker):
    y0, y1 = 970, 1016
    draw.rectangle([20, y0, 1004, y1], fill=INK)
    line1 = "ALSO TODAY:  " + "  •  ".join(ticker[0:3])
    line2 = "  •  ".join(ticker[3:6])
    draw.text((32, y0 + 6), trunc(draw, line1, F_SANS_B(13), 940),
              font=F_SANS_B(13), fill=(255, 210, 63))
    draw.text((32, y0 + 25), trunc(draw, line2, F_SANS(13), 940),
              font=F_SANS(13), fill=(220, 220, 220))


def build():
    data = load_stories()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_lead(draw, data["lead"])
    draw.text((20, 278), "WHERE IT HAPPENED — 13 STORIES ON THE MAP",
              font=F_SANS_B(13), fill=INK)
    draw_map(draw, data["pinned"])
    draw_key(draw, data["pinned"])
    draw_cards(draw, data["briefs"])
    draw_ticker(draw, data["ticker"])
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
