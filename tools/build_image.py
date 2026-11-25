#!/usr/bin/env python3
"""Build the entry image for the make.fun bounty
"Sum up 24 November's world news in one image" (news-image-20261124).

Draws a 1024x1024 newspaper-style summary of the real world news of
Tuesday 24 November 2026, as reported that day by Al Jazeera, Reuters,
the Associated Press, UN News, the Kyiv Independent and USA Today.
Six stories, one per region/field, each a short headline plus one
faithful one-line summary. Text is drawn with PIL (no AI text render)
so every label is exact and legible.

Output: assets/news-20261124.png (PNG, 1024x1024, under 1 MiB).
Run: python3 tools/build_image.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "news-20261124.png")

W, H = 1024, 1024

NAVY = (14, 42, 71)
GOLD = (232, 184, 75)
WHITE = (255, 255, 255)
INK = (17, 24, 33)
GREY = (70, 80, 92)
LIGHT_ROW = (241, 244, 248)
RULE = (214, 220, 228)
FOOT_GREY = (110, 120, 132)

# Six stories of 24 November 2026 (all reported that day).
STORIES = [
    ("ISRAEL-GAZA", "Israel kills Hamas security chief",
     "Airstrike in Gaza City kills Naim Abu Nahal; 7 dead despite ceasefire.",
     (179, 64, 42)),
    ("UKRAINE WAR", "Russian strike hits Zaporizhzhia",
     "Overnight attack kills 2, wounds 40, four of them children; flats hit.",
     (106, 63, 160)),
    ("EUROPE", "Germany first to use Delta system",
     "Berlin signs deal for first access to Ukraine's battlefield system.",
     (36, 86, 166)),
    ("IRAQ", "Baghdad moves on Kurdish oilfields",
     "PM orders federal takeover of oilfields and border posts; Kurds reject it.",
     (194, 112, 14)),
    ("AFRICA", "Ebola workers trapped in Congo",
     "WHO teams shelter in an Ituri maternity ward as fighting rages nearby.",
     (30, 122, 76)),
    ("AMERICAS", "Trump awards Giuliani top medal",
     "Medal of Freedom, the top US civilian honour, given in private ceremony.",
     (14, 124, 123)),
]


def font(name, size):
    """Liberation Sans (Arial-metric) with DejaVu fallback."""
    candidates = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % name,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"
        % ("-Bold" if name == "Bold" else ""),
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    f_kicker = font("Bold", 24)
    f_date = font("Bold", 74)
    f_sub = font("Regular", 25)
    f_tag = font("Bold", 20)
    f_head = font("Bold", 30)
    f_sum = font("Regular", 22)
    f_num = font("Bold", 32)
    f_foot = font("Regular", 18)

    # ---- header band ----
    d.rectangle([0, 0, W, 196], fill=NAVY)
    d.text((36, 30), "THE WORLD IN ONE IMAGE", font=f_kicker, fill=GOLD)
    d.text((34, 62), "24 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.text((36, 152), "TUESDAY  \u00b7  SIX STORIES FROM AROUND THE WORLD",
           font=f_sub, fill=(178, 196, 216))
    d.rectangle([0, 196, W, 200], fill=GOLD)

    # ---- story rows ----
    top = 200
    row_h = 127
    for i, (tag, head, summ, color) in enumerate(STORIES):
        y0 = top + i * row_h
        if i % 2 == 1:
            d.rectangle([0, y0, W, y0 + row_h], fill=LIGHT_ROW)
        # number badge
        d.rounded_rectangle([28, y0 + 31, 92, y0 + 95], radius=10, fill=color)
        num = str(i + 1)
        nb = d.textbbox((0, 0), num, font=f_num)
        d.text((60 - (nb[2] - nb[0]) / 2, y0 + 31 + (64 - (nb[3] - nb[1])) / 2 - 2),
               num, font=f_num, fill=WHITE)
        # category tag
        d.text((114, y0 + 20), tag, font=f_tag, fill=color)
        # headline
        d.text((112, y0 + 46), head, font=f_head, fill=INK)
        # one-line summary
        d.text((112, y0 + 88), summ, font=f_sum, fill=GREY)
        if i < len(STORIES) - 1:
            d.line([(28, y0 + row_h), (W - 28, y0 + row_h)], fill=RULE, width=1)

    # ---- footer ----
    foot = "Sources: Al Jazeera \u00b7 Reuters \u00b7 UN News \u00b7 AP News \u00b7 Kyiv Independent  \u2014  all events reported on 24 Nov 2026"
    fb = d.textbbox((0, 0), foot, font=f_foot)
    d.text(((W - (fb[2] - fb[0])) / 2, 200 + 6 * row_h + 14), foot,
           font=f_foot, fill=FOOT_GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s (%dx%d, %d bytes)" % (OUT, W, H, size))
    assert size <= 1024 * 1024, "image over 1 MiB!"

    # ---- width checks: every headline/summary must fit its row ----
    for tag, head, summ, _ in STORIES:
        hw = d.textbbox((0, 0), head, font=f_head)[2]
        sw = d.textbbox((0, 0), summ, font=f_sum)[2]
        print("  %-34s head %3dpx  summary %3dpx" % (head, hw, sw))
        assert hw <= 872, "headline too wide: %s" % head
        assert sw <= 872, "summary too wide: %s" % summ
    fw = d.textbbox((0, 0), foot, font=f_foot)[2]
    print("  footer %dpx (limit 952)" % fw)
    assert fw <= 952, "footer too wide"


if __name__ == "__main__":
    main()
