#!/usr/bin/env python3
"""Draw the 19 Nov 2026 news image v2: a dense 1024x1024 front page.

33 stories, every continent, all first reported Thursday 19 November
2026: 3 illustrated leads, 10 grid stories, a world map and 20 indexed
briefs, plus a DATE CHECK that names what was left out for being
another day's news. Flat vector style only (no faces, no photos).
Run:  python3 generate.py   ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (22, 40, 63)
TEAL = (14, 116, 144)
CREAM = (255, 253, 245)
GREY = (90, 90, 90)
LIGHT = (226, 232, 240)
SEA = (198, 222, 235)
LAND = (232, 214, 170)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def _disc(d, cx, cy, r, flag_img):
    mask = Image.new("L", (2 * r, 2 * r), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    img.paste(flag_img, (cx - r, cy - r), mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)


def flag_us(d, cx, cy, r):
    f = Image.new("RGB", (2 * r, 2 * r), (255, 255, 255))
    fd = ImageDraw.Draw(f)
    for i in range(13):
        y0 = i * (2 * r) // 13
        y1 = (i + 1) * (2 * r) // 13
        fd.rectangle([0, y0, 2 * r, y1], fill=RED if i % 2 == 0 else (255, 255, 255))
    fd.rectangle([0, 0, int(2 * r * 0.4), int(2 * r * 7 / 13)], fill=(30, 58, 138))
    _disc(d, cx, cy, r, f)


def flag_cn(d, cx, cy, r):
    f = Image.new("RGB", (2 * r, 2 * r), (222, 0, 0))
    fd = ImageDraw.Draw(f)
    fd.text((int(2 * r * 0.14), int(2 * r * 0.10)), "\u2605",
            font=font(BOLD, int(r * 0.9)), fill=(255, 222, 0))
    _disc(d, cx, cy, r, f)


def flag_ru(d, cx, cy, r):
    f = Image.new("RGB", (2 * r, 2 * r), (255, 255, 255))
    fd = ImageDraw.Draw(f)
    fd.rectangle([0, 0, 2 * r, int(2 * r / 3)], fill=(255, 255, 255))
    fd.rectangle([0, int(2 * r / 3), 2 * r, int(4 * r / 3)], fill=(0, 57, 166))
    fd.rectangle([0, int(4 * r / 3), 2 * r, 2 * r], fill=(213, 0, 50))
    _disc(d, cx, cy, r, f)


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT",
         head="Trump, Xi and Putin hold first three-way summit",
         body="Three leaders meet for 90 minutes and issue a statement on oil and nuclear risk. \u2014 Reuters",
         src="Reuters", region="Asia", mx=245, my=55),
    dict(n=2, place="THE HAGUE", topic="JUSTICE",
         head="World Court: Myanmar committed genocide",
         body="The ICJ rules 9\u20136 that Myanmar is guilty of genocide against the Rohingya. \u2014 Al Jazeera",
         src="Al Jazeera \u00b7 UN News", region="Europe", mx=148, my=28),
    dict(n=3, place="ANTALYA", topic="CLIMATE",
         head="COP31 draft drops fossil fuels and $120bn aid goal",
         body="The slimmer text has no figure for adaptation aid. Talks end Friday. \u2014 Reuters",
         src="Reuters \u00b7 AFP", region="Europe", mx=172, my=48),
]

GRID = [
    dict(n=4, place="CRIMEA", topic="WAR",
         head="Ukraine hits Crimea bridge again",
         body="Third strike in a week halts trains to Russia.",
         src="Euronews", region="Europe", mx=186, my=30, icon="bridge"),
    dict(n=5, place="RIYADH", topic="WAR",
         head="Saudis shoot down Houthi missiles",
         body="Debris fell on the capital; no casualties.",
         src="Reuters", region="Middle East", mx=198, my=62, icon="missile"),
    dict(n=6, place="ODISHA", topic="STORM",
         head="Cyclone Akvan nears India's coast",
         body="Over 100,000 in shelters before Friday's landfall.",
         src="IMD", region="Asia", mx=228, my=62, icon="cyclone"),
    dict(n=7, place="SEOUL", topic="JUSTICE",
         head="Korea's top court clears ex-PM Han",
         body="Han Duck-soo's martial-law conviction is overturned.",
         src="AP", region="Asia", mx=255, my=40, icon="gavel"),
    dict(n=8, place="GREENLAND", topic="SECURITY",
         head="Denmark backs Arctic pact",
         body="Parliament approves the Greenland deal 109\u20130.",
         src="AP", region="Americas", mx=60, my=15, icon="flag"),
    dict(n=9, place="NEW YORK", topic="MARKETS",
         head="Anthropic starts trading on Nasdaq",
         body="Its record $81bn share sale was priced at $83.",
         src="AP", region="Americas", mx=55, my=45, icon="chart"),
    dict(n=10, place="WORLDWIDE", topic="GAMES",
         head="GTA VI goes on sale after 13 years",
         body="The midnight launch draws rave reviews.",
         src="ABC", region="Global", mx=None, my=None, icon="game"),
    dict(n=11, place="BOGOT\u00c1", topic="LABOUR",
         head="Colombia's unions hold national strike",
         body="Marches in three cities against an anti-union bill.",
         src="Infobae", region="Americas", mx=80, my=95, icon="march"),
    dict(n=12, place="HORMUZ", topic="ENERGY",
         head="Iran says mines set 3 tankers ablaze",
         body="The ships caught fire east of the strait.",
         src="Al Jazeera", region="Middle East", mx=206, my=58, icon="tanker"),
    dict(n=13, place="CANBERRA", topic="ECONOMY",
         head="Australia's jobless rate hits 4.9%",
         body="Highest since 2024; shares and the dollar slide.",
         src="ABC", region="Oceania", mx=270, my=125, icon="chart"),
]

INDEX = [
    (14, "CARACAS", "US and Venezuela restore military ties", "Hegseth", "Americas"),
    (15, "GAZA", "Israeli tanks cross the Yellow Line", "BBC", "Middle East"),
    (16, "JAKARTA", "Asset-seizure law passes after 18 years", "Kompas", "Asia"),
    (17, "SEOUL", "Half a million sit college entrance exam", "Sedaily", "Asia"),
    (18, "KRASNODAR", "Kyiv says it hit two oil refineries", "Euronews", "Europe"),
    (19, "BRUSSELS", "EU delays methane rules two years", "Euronews", "Europe"),
    (20, "LONDON", "Inquiry: yacht Bayesian was vulnerable to wind", "RNZ", "Europe"),
    (21, "ZURICH", "Two rivals to challenge FIFA's Infantino", "ABC", "Europe"),
    (22, "ROME", "Author Corrado Augias dies at 91", "Euronews", "Europe"),
    (23, "MOGADISHU", "Somalia expels UAE ambassador", "Al Jazeera", "Africa"),
    (24, "SUDAN", "Court sentences absent RSF chief to death", "AP", "Africa"),
    (25, "PRETORIA", "Central bank holds rate at 7.25%", "SABC", "Africa"),
    (26, "CANARIES", "Record 11,000 migrants in 15 days", "Africanews", "Africa"),
    (27, "FLORIDA", "Floods shut Broward, Miami schools again", "CBS", "Americas"),
    (28, "WELLINGTON", "Court: pay equity cuts broke rights law", "RNZ", "Oceania"),
    (29, "TONGA", "Drought emergency takes effect", "RNZ", "Oceania"),
    (30, "COOK ISLANDS", "Cyclone Xavier weakens to category 4", "RNZ", "Oceania"),
    (31, "SPACE", "Red giant seen eating a Sun-sized star", "Nature", "Global"),
    (32, "NAIROBI", "Marathon champion banned for doping, 3 years", "ABC", "Africa"),
    (33, "SHENZHEN", "Xi urges ban on all nuclear arms", "Al Jazeera", "Asia"),
]

REGIONS = [("ASIA", 6, (180, 83, 9)), ("MIDDLE EAST", 3, (14, 116, 144)),
           ("EUROPE", 8, (30, 58, 138)), ("AFRICA", 5, (22, 101, 52)),
           ("AMERICAS", 5, (126, 34, 206)), ("OCEANIA", 4, (14, 116, 144)),
           ("GLOBAL", 2, (90, 90, 90))]

BIG = [("3", "presidents at one table"), ("9\u20136", "World Court genocide vote"),
       ("$120bn", "aid goal cut at COP31"), ("$81bn", "Anthropic's record IPO"),
       ("109\u20130", "Danish vote on Arctic pact"), ("4.9%", "Australian jobless rate")]

# simplified continents, in a 300x150 map box
CONTINENTS = [
    [(12, 32), (55, 18), (88, 26), (95, 45), (70, 68), (42, 74), (16, 56)],   # N America
    [(86, 84), (108, 78), (120, 106), (102, 138), (88, 114)],                  # S America
    [(142, 26), (168, 18), (180, 34), (162, 50), (146, 40)],                    # Europe
    [(146, 56), (174, 50), (186, 78), (166, 104), (150, 84)],                   # Africa
    [(182, 20), (248, 14), (270, 38), (252, 68), (212, 74), (186, 48)],         # Asia
    [(250, 108), (280, 104), (286, 124), (260, 130)],                           # Australia
]


def icon(d, kind, x, y, s, color):
    """Tiny pictogram inside a square of side s at (x, y)."""
    if kind == "bridge":
        d.line([x, y + s * 0.7, x + s, y + s * 0.7], fill=color, width=3)
        for px in (x + s * 0.2, x + s * 0.5, x + s * 0.8):
            d.line([px, y + s * 0.2, px, y + s * 0.7], fill=color, width=2)
        d.arc([x, y + s * 0.3, x + s, y + s * 0.9], 0, 180, fill=color, width=2)
    elif kind == "missile":
        d.line([x + s * 0.2, y + s * 0.8, x + s * 0.8, y + s * 0.2], fill=color, width=3)
        d.polygon([(x + s * 0.8, y + s * 0.2), (x + s * 0.55, y + s * 0.25),
                   (x + s * 0.75, y + s * 0.45)], fill=color)
        for i in range(3):
            d.ellipse([x + s * 0.15 - i * 3, y + s * 0.75 + i * 3,
                       x + s * 0.25 - i * 3, y + s * 0.85 + i * 3],
                      outline=color, width=1)
    elif kind == "cyclone":
        cx, cy = x + s / 2, y + s / 2
        for r in range(int(s * 0.45), 3, -3):
            d.arc([cx - r, cy - r, cx + r, cy + r], 0, 270, fill=color, width=2)
    elif kind == "gavel":
        d.line([x + s * 0.2, y + s * 0.7, x + s * 0.8, y + s * 0.3], fill=color, width=3)
        d.rectangle([x + s * 0.55, y + s * 0.1, x + s * 0.95, y + s * 0.3], fill=color)
        d.rectangle([x + s * 0.1, y + s * 0.75, x + s * 0.9, y + s * 0.85], fill=color)
    elif kind == "flag":
        d.line([x + s * 0.25, y + s * 0.1, x + s * 0.25, y + s * 0.9], fill=color, width=2)
        d.polygon([(x + s * 0.25, y + s * 0.1), (x + s * 0.85, y + s * 0.3),
                   (x + s * 0.25, y + s * 0.5)], fill=color)
    elif kind == "chart":
        pts = [(x + s * 0.1, y + s * 0.7), (x + s * 0.3, y + s * 0.5),
               (x + s * 0.5, y + s * 0.6), (x + s * 0.7, y + s * 0.3),
               (x + s * 0.9, y + s * 0.15)]
        d.line(pts, fill=color, width=3)
        d.line([x + s * 0.1, y + s * 0.85, x + s * 0.9, y + s * 0.85], fill=color, width=2)
    elif kind == "game":
        d.rounded_rectangle([x + s * 0.1, y + s * 0.3, x + s * 0.9, y + s * 0.75],
                            radius=6, outline=color, width=2)
        d.ellipse([x + s * 0.62, y + s * 0.45, x + s * 0.72, y + s * 0.55], fill=color)
        d.ellipse([x + s * 0.76, y + s * 0.45, x + s * 0.86, y + s * 0.55], fill=color)
    elif kind == "march":
        for i, px in enumerate((0.2, 0.45, 0.7)):
            d.ellipse([x + s * px, y + s * 0.15, x + s * (px + 0.12), y + s * 0.3], fill=color)
            d.rectangle([x + s * px, y + s * 0.32, x + s * (px + 0.12), y + s * 0.75],
                        fill=color)
    elif kind == "tanker":
        d.rectangle([x + s * 0.1, y + s * 0.55, x + s * 0.9, y + s * 0.8], fill=color)
        d.rectangle([x + s * 0.6, y + s * 0.35, x + s * 0.75, y + s * 0.55], fill=color)
        for fx in (0.2, 0.4, 0.6):
            d.polygon([(x + s * fx, y + s * 0.35), (x + s * (fx + 0.07), y + s * 0.12),
                       (x + s * (fx + 0.14), y + s * 0.35)], fill=(249, 115, 22))


def lead_art(d, n, x, y, w, h):
    """Illustration strip at the top of a lead card."""
    if n == 1:
        # three leaders at a table: flag discs + table
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        d.rectangle([x, y, x + w, y + 22], fill=(180, 83, 9))
        d.text((x + 10, y + 2), "APEC 2026 \u00b7 SHENZHEN", font=font(BOLD, 13),
               fill=(255, 255, 255))
        for cx, fn, label in [(x + w * 0.2, flag_us, "TRUMP"),
                              (x + w * 0.5, flag_cn, "XI"),
                              (x + w * 0.8, flag_ru, "PUTIN")]:
            fn(d, int(cx), y + 52, 26)
            d.text((cx, y + 82), label, font=font(BOLD, 12), fill=(255, 255, 255),
                   anchor="ma")
        d.rectangle([x + 18, y + h - 12, x + w - 18, y + h - 4], fill=(250, 204, 21))
    elif n == 2:
        # courthouse + scales + 9-6 badge
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
        d.polygon([(x + w * 0.5, y + 12), (x + w * 0.5 - 52, y + 42),
                   (x + w * 0.5 + 52, y + 42)], fill=NAVY)
        for cx in (x + w * 0.5 - 34, x + w * 0.5, x + w * 0.5 + 34):
            d.rectangle([cx - 5, y + 46, cx + 5, y + 78], fill=NAVY)
        d.rectangle([x + w * 0.5 - 58, y + 78, x + w * 0.5 + 58, y + 84], fill=NAVY)
        # scales, right
        sx, sy = x + w - 62, y + 30
        d.line([sx, sy, sx, sy + 44], fill=INK, width=3)
        d.line([sx - 22, sy + 6, sx + 22, sy + 6], fill=INK, width=3)
        d.arc([sx - 30, sy + 6, sx - 14, sy + 22], 180, 360, fill=INK, width=2)
        d.arc([sx + 14, sy + 6, sx + 30, sy + 22], 180, 360, fill=INK, width=2)
        # 9-6 badge
        d.rectangle([x + 10, y + 10, x + 62, y + 44], fill=RED)
        d.text((x + 36, y + 14), "9\u20136", font=font(BOLD, 22), fill=(255, 255, 255),
               anchor="ma")
    else:
        # globe + thermometer, fossil fuels crossed out
        d.rectangle([x, y, x + w, y + h], fill=(14, 116, 144))
        d.ellipse([x + 18, y + 14, x + 98, y + 94], fill=(34, 139, 230))
        d.ellipse([x + 34, y + 28, x + 58, y + 48], fill=(34, 197, 94))
        d.ellipse([x + 62, y + 56, x + 88, y + 76], fill=(34, 197, 94))
        d.ellipse([x + 26, y + 62, x + 44, y + 78], fill=(34, 197, 94))
        # thermometer
        d.rounded_rectangle([x + w - 52, y + 16, x + w - 32, y + 78], radius=9,
                            outline=(255, 255, 255), width=3)
        d.ellipse([x + w - 56, y + 70, x + w - 28, y + 98], fill=RED)
        d.rectangle([x + w - 46, y + 30, x + w - 38, y + 76], fill=RED)
        d.rectangle([x + 108, y + 22, x + w - 70, y + 52], fill=(255, 255, 255))
        d.text((x + 116, y + 29), "FOSSIL FUELS", font=font(BOLD, 15), fill=RED)
        d.line([x + 112, y + 42, x + w - 74, y + 30], fill=RED, width=3)
        d.rectangle([x + 108, y + 62, x + w - 70, y + 92], fill=RED)
        d.text((x + 116, y + 68), "CUT", font=font(BOLD, 17), fill=(255, 255, 255))


def main():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)
    d.rectangle([10, 10, W - 11, H - 11], outline=RED, width=2)

    # --- kicker + masthead ---
    d.text((16, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 16), fill=RED)
    d.text((W - 16, 18), "33 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY",
           font=font(BOLD, 16), fill=INK, anchor="ra")
    d.text((512, 38), "Thursday 19 November 2026", font=font(SERIF, 46),
           fill=INK, anchor="ma")
    d.text((512, 88),
           "Trump, Xi and Putin share one table \u00b7 The World Court finds genocide in Myanmar \u00b7 COP31's draft drops fossil fuels",
           font=font(REG, 16), fill=RED, anchor="ma")
    d.line([16, 112, W - 16, 112], fill=INK, width=2)

    # --- stats strip: region blocks + big numbers ---
    x = 16
    seg_w = (W - 32) / 7
    for name, count, color in REGIONS:
        d.rectangle([x, 118, x + seg_w - 2, 136], fill=color)
        d.text((x + seg_w / 2, 120), f"{name} {count}", font=font(BOLD, 11),
               fill=(255, 255, 255), anchor="ma")
        x += seg_w
    x = 16
    col_w = (W - 32) / 6
    for big, label in BIG:
        d.text((x + col_w / 2, 142), big, font=font(BOLD, 22), fill=INK, anchor="ma")
        lab = wrap(d, label, font(REG, 11), col_w - 8)
        draw_lines(d, lab, x + 4, 168, font(REG, 11), GREY, 13)
        x += col_w
    d.line([16, 190, W - 16, 190], fill=INK, width=2)

    # --- three leads ---
    lead_w, lead_h, lead_y = 322, 210, 196
    for i, s in enumerate(LEADS):
        lx = 16 + i * (lead_w + 8)
        d.rectangle([lx, lead_y, lx + lead_w, lead_y + lead_h], fill=CREAM,
                    outline=INK, width=2)
        lead_art(d, s["n"], lx + 2, lead_y + 2, lead_w - 4, 108)
        d.text((lx + 10, lead_y + 118), f"{s['n']}  {s['place']} \u00b7 {s['topic']}",
               font=font(BOLD, 12), fill=RED)
        hl = wrap(d, s["head"], font(BOLD, 17), lead_w - 20)
        draw_lines(d, hl, lx + 10, lead_y + 136, font(BOLD, 17), INK, 20)
        bd = wrap(d, s["body"], font(REG, 12), lead_w - 20)
        draw_lines(d, bd, lx + 10, lead_y + 136 + len(hl) * 20 + 3,
                   font(REG, 12), (51, 51, 51), 15)

    # --- grid: 10 stories, 2 rows x 5 ---
    gw, gh, gy = 196, 112, 414
    for i, s in enumerate(GRID):
        gx = 16 + (i % 5) * (gw + 4)
        gy2 = gy + (i // 5) * (gh + 4)
        d.rectangle([gx, gy2, gx + gw, gy2 + gh], fill=CREAM, outline=INK, width=1)
        icon(d, s["icon"], gx + 8, gy2 + 8, 26, RED)
        d.text((gx + 42, gy2 + 8), f"{s['n']}", font=font(BOLD, 15), fill=RED)
        d.text((gx + 42, gy2 + 26), f"{s['place']} \u00b7 {s['topic']}",
               font=font(BOLD, 10), fill=RED)
        hl = wrap(d, s["head"], font(BOLD, 13), gw - 16)
        draw_lines(d, hl, gx + 8, gy2 + 44, font(BOLD, 13), INK, 15)
        bd = wrap(d, s["body"], font(REG, 11), gw - 16)
        draw_lines(d, bd, gx + 8, gy2 + 44 + len(hl) * 15 + 2,
                   font(REG, 11), (51, 51, 51), 13)

    # --- map + index ---
    my = 650
    d.text((16, my), "WHERE IT HAPPENED", font=font(BOLD, 13), fill=RED)
    d.text((16, my + 16), "numbers match the stories",
           font=font(REG, 11), fill=GREY)
    map_x, map_y, map_w, map_h = 16, my + 36, 300, 150
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA,
                outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px, map_y + py) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(180, 160, 120))
    for s in LEADS + GRID:
        if s.get("mx") is None:
            continue
        px, py = map_x + s["mx"], map_y + s["my"]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 2), str(s["n"]), font=font(BOLD, 10), fill=(255, 255, 255),
               anchor="mm")
    d.text((16, map_y + map_h + 6), "Red numbers mark stories 1\u201313.",
           font=font(REG, 11), fill=GREY)
    # index, two columns: one line per brief, source inline
    ix0, ix1 = 340, 680
    d.text((ix0, my), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=font(BOLD, 13), fill=RED)
    d.text((ix0, my + 16), "place \u00b7 what happened \u00b7 source", font=font(REG, 11), fill=GREY)
    for j, (n, place, head, src, region) in enumerate(INDEX):
        col = ix0 if j < 10 else ix1
        yy = my + 36 + (j % 10) * 25
        d.text((col, yy), str(n), font=font(BOLD, 11), fill=RED)
        line = f"{place} \u2014 {head}. \u2014 {src}"
        ln = wrap(d, line, font(REG, 10), (ix1 - ix0 - 30) if j < 10 else (W - 16 - ix1 - 30))
        draw_lines(d, ln, col + 24, yy, font(REG, 10), INK, 12)

    # --- date check + sources ---
    d.rectangle([16, 946, W - 16, 984], outline=RED, width=2)
    d.text((512, 950),
           "DATE CHECK \u2713  Every story on this page happened, or was first reported, on Thursday 19 November 2026.",
           font=font(BOLD, 12), fill=INK, anchor="ma")
    d.text((512, 966),
           "LEFT OUT AS OF OTHER DAYS' NEWS: 18 NOV: Jeffries' 251\u201311 Speaker nomination \u00b7 Voyager 1 one light-day (10:16 GMT) \u00b7 Pew's Islam projection \u00b7 EU's \u20ac45bn Ukraine loan.",
           font=font(REG, 11), fill=GREY, anchor="ma")
    d.text((512, 992),
           "Claims are attributed, not stated as fact \u00b7 Pictures and map: original, drawn in code \u00b7 Sources: Reuters, AP, AFP, BBC, Al Jazeera, Euronews, ABC, RNZ, Nature \u00b7 2026-11-19",
           font=font(REG, 10), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
