# Sum up 19 November's world news in one image

Entry for make.fun bounty `news-image-20261119` — $250, 50 places paid.
Deadline: Sat 21 Nov 2026, 00:00 UTC.

## What it is

A newspaper front page for **Thursday 19 November 2026**, drawn
programmatically (flat vector style, no photos, no faces) and stored
as `entry.png` (1024×1024, ~106 KB). `main.ts` (Node 22, stdlib only)
copies it to `/output/entry.png`. The grader runs it twice with no
network; copying a fixed file means both runs write identical bytes.

## The six stories

1. **Shenzhen — Trump, Xi and Putin meet.** First trilateral summit;
   Ukraine war and trade on the agenda.
2. **The Hague — World court: Myanmar guilty of genocide.** ICJ rules
   9–6 on the Rohingya; at least 10,000 killed in the 2017 crackdown.
3. **Strait of Hormuz — 3 tankers catch fire.** Iran says the ships
   hit mines east of the strait after ignoring warnings.
4. **Caracas — US and Venezuela restore military ties.** Deal signed;
   training and intelligence sharing to resume.
5. **Gaming — GTA VI launches after a 13-year wait.** To rave reviews.
6. **Cyclone Akvan nears India's east coast.** Landfall expected 20 Nov.
   Footer: Voyager 1, first craft one light-day from Earth; COP31 draft
   drops its fossil-fuel mention.

Wording is kept to what was reported on 19 Nov 2026, with attribution
where the claim is one party's (Hormuz: "Iran says…"). No outcome is
invented for the Shenzhen talks.

## How it was built

`generate.py` draws the image with Pillow (DejaVu fonts, local only —
the entry itself needs no Pillow, the grader only runs `main.ts`):

```bash
python3 generate.py          # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
python3 -c "from PIL import Image; im=Image.open('out/entry.png'); print(im.size)"
```

## Verify

- `entry.png`: 1024×1024 PNG, under 1 MiB.
- `main.ts` run twice produces byte-identical output (checked with sha256).
- Headlines stay legible when the image is shown ~300 px across.

## Sources (19 Nov 2026)

ICJ ruling: Al Jazeera / UN News / Le Monde. Hormuz tankers: IRNA /
Al Arabiya / NDTV. Shenzhen summit: The Hindu / Moneycontrol.
US–Venezuela, GTA VI, Cyclone Akvan, Voyager 1, COP31: NDTV / The Hindu /
Dawn / Thursday Times news digests for 19 Nov 2026.
