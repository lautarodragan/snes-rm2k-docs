#!/usr/bin/env python3
"""The three graded maps of the test game, each as RPG Maker 2000 draws it
and as the console does, with where they differ.

    python3 figures/tools/grades.py --goldens <the-advocate's test-game/tests/golden> \
        --originals figures/tools/originals --out src/tools

The console's side is the test game's goldens —what snes9x drew, and
bsnes the same at 15 bits—: 256x224, the camera on the hero. The
original's side is a capture of RPG_RT running the folder `just game`
makes, at the window's 320x240, kept in `--originals` as
`rm2k-<map>.png`, since nothing here can run RPG Maker. The console's
window is found inside the original by the offset where the two agree
on the most pixels at 15 bits, and the third panel marks the pixels that
still differ there.
"""

import argparse
import os

from PIL import Image

MAPS = ["meadow", "garden", "showcase"]
GAP = 8
BACK = (48, 48, 48)
MARK = (255, 90, 60)


def fifteen(picture):
    rgb = picture.convert("RGB")
    return [(r >> 3, g >> 3, b >> 3) for r, g, b in rgb.getdata()], rgb.size


def window_offset(original, console):
    """Where the console's picture sits in the original: the offset with
    the most equal pixels, tried over every position the window fits."""
    ow, oh = original.size
    cw, ch = console.size
    o15, _ = fifteen(original)
    c15, _ = fifteen(console)
    best, best_at = -1, (0, 0)
    for dy in range(0, oh - ch + 1, 8):
        for dx in range(0, ow - cw + 1, 8):
            same = 0
            for y in range(0, ch, 4):
                row = (dy + y) * ow + dx
                crow = y * cw
                for x in range(0, cw, 4):
                    if o15[row + x] == c15[crow + x]:
                        same += 1
            if same > best:
                best, best_at = same, (dx, dy)
    return best_at


def compare(original, console, at):
    dx, dy = at
    cw, ch = console.size
    window = original.crop((dx, dy, dx + cw, dy + ch))
    w15, _ = fifteen(window)
    c15, _ = fifteen(console)
    mask = Image.new("RGB", console.size, BACK)
    differing = 0
    for i, (a, b) in enumerate(zip(w15, c15)):
        if a != b:
            differing += 1
            mask.putpixel((i % cw, i // cw), MARK)
    return window, mask, differing


def row(pictures):
    width = sum(p.width for p in pictures) + GAP * (len(pictures) - 1)
    height = max(p.height for p in pictures)
    out = Image.new("RGB", (width, height), BACK)
    x = 0
    for p in pictures:
        out.paste(p.convert("RGB"), (x, 0))
        x += p.width + GAP
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--goldens", required=True)
    parser.add_argument("--originals", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for name in MAPS:
        original = Image.open(os.path.join(args.originals, f"rm2k-{name}.png"))
        console = Image.open(os.path.join(args.goldens, f"{name}.png"))
        at = window_offset(original, console)
        window, mask, differing = compare(original, console, at)
        total = console.width * console.height
        print(f"{name}: the console's window at {at} in the original; {differing} of {total} pixels differ at 15 bits ({100 * differing / total:.1f}%)")
        picture = row([window, console, mask])
        path = os.path.join(args.out, f"grade-{name}.png")
        picture.save(path, optimize=True)
        print(f"  wrote {path}: {picture.width}x{picture.height}, {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
