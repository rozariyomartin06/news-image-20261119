#!/usr/bin/env python3
"""Draw the 19 Nov 2026 news image: a 1024x1024 newspaper front page.

Flat vector style only (no faces, no photos): flags, a skyline, a
courthouse, a tanker, a game controller and a cyclone spiral, drawn
with Pillow primitives. All text is set in DejaVu, large enough to
read when the image is shown about 300 px across.
Run:  python3 generate.py   ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (22, 40, 63)
NAVY2 = (30, 58, 95)
TEAL = (14, 116, 144)
CREAM = (255, 253, 245)
GREY = (226, 232, 240)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
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
    mask = Image.new("L", (2*r, 2*r), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 2*r-1, 2*r-1], fill=255)
    img.paste(flag_img, (cx-r, cy-r), mask)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=INK, width=3)


def flag_us(d, cx, cy, r):
    f = Image.new("RGB", (2*r, 2*r), (255, 255, 255))
    fd = ImageDraw.Draw(f)
    for i in range(13):
        y0 = i * (2*r) // 13
        y1 = (i+1) * (2*r) // 13
        fd.rectangle([0, y0, 2*r, y1], fill=RED if i % 2 == 0 else (255, 255, 255))
    fd.rectangle([0, 0, int(2*r*0.4), int(2*r*7/13)], fill=(30, 58, 138))
    for sx in range(3):
        for sy in range(3):
            fd.ellipse([8+sx*22, 8+sy*14, 16+sx*22, 16+sy*14], fill=(255, 255, 255))
    _disc(d, cx, cy, r, f)


def flag_cn(d, cx, cy, r):
    f = Image.new("RGB", (2*r, 2*r), (222, 0, 0))
    fd = ImageDraw.Draw(f)
    fd.text((int(2*r*0.14), int(2*r*0.10)), "\u2605", font=font(BOLD, int(r*0.9)), fill=(255, 222, 0))
    _disc(d, cx, cy, r, f)


def flag_ru(d, cx, cy, r):
    f = Image.new("RGB", (2*r, 2*r), (255, 255, 255))
    fd = ImageDraw.Draw(f)
    fd.rectangle([0, int(2*r/3), 2*r, 2*r], fill=(213, 0, 50))
    fd.rectangle([0, int(2*r/3), 2*r, int(4*r/3)], fill=(0, 57, 166))
    # white top, blue middle, red bottom: redraw in order
    fd.rectangle([0, 0, 2*r, int(2*r/3)], fill=(255, 255, 255))
    fd.rectangle([0, int(2*r/3), 2*r, int(4*r/3)], fill=(0, 57, 166))
    fd.rectangle([0, int(4*r/3), 2*r, 2*r], fill=(213, 0, 50))
    _disc(d, cx, cy, r, f)


def flag_ve(d, cx, cy, r):
    f = Image.new("RGB", (2*r, 2*r), (255, 204, 0))
    fd = ImageDraw.Draw(f)
    fd.rectangle([0, int(2*r/3), 2*r, int(4*r/3)], fill=(0, 47, 167))
    fd.rectangle([0, int(4*r/3), 2*r, 2*r], fill=(207, 20, 43))
    _disc(d, cx, cy, r, f)


def main():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)
    d.rectangle([10, 10, W - 11, H - 11], outline=RED, width=2)

    # --- masthead ---
    d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SERIF, 52),
           fill=INK, anchor="ma")
    d.rectangle([16, 92, W - 16, 128], fill=RED)
    d.text((512, 97), "THURSDAY  •  19 NOVEMBER 2026", font=font(BOLD, 28),
           fill=(255, 255, 255), anchor="ma")

    # --- hero: Shenzhen summit ---
    d.rectangle([16, 136, W - 16, 424], fill=NAVY)
    d.text((40, 152), "SHENZHEN  •  DIPLOMACY", font=font(BOLD, 22), fill=(250, 204, 21))
    hero_head = wrap(d, "TRUMP, XI AND PUTIN MEET IN SHENZHEN", font(BOLD, 44), 540)
    draw_lines(d, hero_head, 40, 186, font(BOLD, 44), (255, 255, 255), 52)
    sub = wrap(d, "First trilateral summit — the three leaders talk Ukraine war and trade.",
               font(REG, 22), 540)
    draw_lines(d, sub, 40, 186 + len(hero_head) * 52 + 8, font(REG, 22),
               (203, 213, 225), 30)
    # skyline silhouette along the hero bottom
    for x0, hgt in [(620, 70), (660, 110), (700, 85), (745, 125), (790, 95), (835, 115), (880, 80), (925, 105)]:
        d.rectangle([x0, 424 - hgt, x0 + 34, 424], fill=(10, 22, 40))
    # three flag discs
    for cx, fn, label in [(700, flag_us, "USA"), (800, flag_cn, "CHINA"), (900, flag_ru, "RUSSIA")]:
        fn(d, cx, 210, 48)
        d.text((cx, 268), label, font=font(BOLD, 18), fill=(255, 255, 255), anchor="ma")

    # --- panel helper ---
    def panel(x, y, w, h, bg, accent):
        d.rectangle([x, y, x + w, y + h], fill=bg, outline=INK, width=2)
        d.rectangle([x, y, x + w, y + 8], fill=accent)

    def story(x, y, w, h, kicker, headline, body, accent):
        panel(x, y, w, h, CREAM, accent)
        d.text((x + 18, y + 18), kicker, font=font(BOLD, 18), fill=accent)
        hl = wrap(d, headline, font(BOLD, 27), w - 36)
        draw_lines(d, hl, x + 18, y + 46, font(BOLD, 27), INK, 32)
        bd = wrap(d, body, font(REG, 20), w - 36)
        draw_lines(d, bd, x + 18, y + 46 + len(hl) * 32 + 6, font(REG, 20),
                   (51, 51, 51), 26)

    # --- row A ---
    # ICJ (left): courthouse icon drawn in the top-right corner space is
    # kept minimal — columns under the kicker line instead of a picture.
    story(16, 440, 488, 224, "THE HAGUE  •  JUSTICE",
          "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
          "ICJ rules 9–6 on the Rohingya — at least 10,000 killed in the 2017 crackdown.",
          RED)
    # courthouse columns, bottom-right of the ICJ panel, below the text
    for cx in [400, 432, 464]:
        d.rectangle([cx, 618, cx + 12, 652], fill=NAVY)
    d.rectangle([392, 610, 486, 618], fill=NAVY)
    d.rectangle([386, 652, 492, 658], fill=NAVY)

    story(520, 440, 488, 224, "STRAIT OF HORMUZ  •  ENERGY",
          "3 TANKERS CATCH FIRE OFF HORMUZ",
          "Iran says the ships hit mines east of the strait after ignoring warnings.",
          (180, 83, 9))
    # tanker + flames, bottom of the Hormuz panel, below the text
    d.rectangle([560, 648, 980, 656], fill=(14, 116, 144))
    d.rectangle([640, 630, 880, 648], fill=INK)
    d.rectangle([700, 612, 730, 630], fill=INK)
    for fx, fh in [(660, 22), (700, 30), (750, 24), (800, 28)]:
        d.polygon([(fx, 630), (fx + 13, 630 - fh), (fx + 26, 630)], fill=(249, 115, 22))

    # --- row B ---
    story(16, 680, 488, 224, "CARACAS  •  AMERICAS",
          "US AND VENEZUELA RESTORE MILITARY TIES",
          "Deal signed in Caracas — training and intelligence sharing to resume.",
          TEAL)
    flag_us(d, 410, 868, 30)
    flag_ve(d, 472, 868, 30)

    story(520, 680, 488, 224, "GAMING  •  CULTURE",
          "GTA VI LAUNCHES AFTER 13-YEAR WAIT",
          "Rockstar's blockbuster arrives to rave reviews worldwide.",
          (126, 34, 206))
    d.text((980, 892), "VI", font=font(SERIF, 88), fill=(126, 34, 206), anchor="rb")
    d.text((560, 856), "★ ★ ★ ★ ★", font=font(BOLD, 22), fill=(126, 34, 206))

    # --- cyclone strip ---
    d.rectangle([16, 920, W - 16, 968], fill=TEAL)
    # spiral
    cx, cy = 52, 944
    for r in range(20, 4, -4):
        d.arc([cx - r, cy - r, cx + r, cy + r], 0, 270, fill=(255, 255, 255), width=3)
    d.text((84, 928), "CYCLONE AKVAN NEARS INDIA'S EAST COAST — landfall expected 20 Nov.",
           font=font(BOLD, 21), fill=(255, 255, 255))

    # --- footer ---
    d.text((512, 982), "ALSO: Voyager 1, first craft one light-day from Earth  •  COP31 draft drops fossil-fuel mention",
           font=font(REG, 17), fill=(51, 51, 51), anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
