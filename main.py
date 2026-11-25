#!/usr/bin/env python3
"""Entry program for the make.fun bounty
"Sum up 24 November's world news in one image" (news-image-20261124).

Writes one image summing up the world news of Tuesday 24 November 2026
to /output/entry.png.

The image itself is a fixed asset held in this repo
(assets/news-20261124.png, drawn by tools/build_image.py from the real
news of that day: Israel killing Hamas security chief Naim Abu Nahal in
Gaza, a Russian strike on Zaporizhzhia, Germany first to use Ukraine's
Delta battlefield system, Baghdad moving on Kurdish oilfields, Ebola
workers trapped in Congo, and Trump awarding Giuliani the Medal of
Freedom).

This program copies that asset byte-for-byte, so every run writes
identical bytes: no network, no clock, no randomness, stdlib only.
"""

import hashlib
import os
import shutil
import struct
import sys

ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "assets", "news-20261124.png")
MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def png_dimensions(path):
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def output_path():
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "output", "entry.png")


def main():
    if not os.path.isfile(ASSET):
        print("missing asset: %s" % ASSET, file=sys.stderr)
        return 1
    if os.path.getsize(ASSET) > MAX_BYTES:
        print("asset over 1 MiB", file=sys.stderr)
        return 1
    width, height = png_dimensions(ASSET)
    if width > MAX_DIM or height > MAX_DIM:
        print("asset over 1024x1024 (%dx%d)" % (width, height),
              file=sys.stderr)
        return 1
    out = output_path()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(ASSET, out)
    with open(out, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)"
          % (out, os.path.getsize(out), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
