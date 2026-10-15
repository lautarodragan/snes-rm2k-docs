#!/usr/bin/env python3
"""The pictures of the book's "The tools" page, made by running the tools.

    python3 figures/tools/make.py --rtp <EasyRPG RTP> --soundfont <a .sf2> \
        --test-game <the-advocate's test-game/, after `just game`> \
        --out src/tools [--work <scratch directory>]

Every picture in `src/tools/` comes out of here, so that it can be made
again when a tool changes: the only thing this script does by itself is
count pixels, write requests and paste answers side by side. The tools
come from the PATH —`adeleine`, `voodoo`, `lz2`, `gunter`, `rm2k-render`,
`wally`, `rm2k-snes-screens`—, like for any game. What each step printed
goes to standard output, which is where the page's numbers were read
from.

The RTP is EasyRPG's (https://github.com/EasyRPG/RTP), whose pictures are
CC BY 4.0 or CC0; the page says whose each one is. The SoundFont only
lends one sample to Gunter's example; a free one keeps the picture free.
"""

import argparse
import json
import os
import struct
import subprocess
import sys
import wave

from PIL import Image, ImageDraw

CELL = 8
PALETTE = 16
USABLE = PALETTE - 1
GAP = 8
BACK = (48, 48, 48)
CHECKER = ((110, 110, 110), (150, 150, 150))


# --- small helpers -----------------------------------------------------------

def run(*command, **kwargs):
    """A tool, by name on the PATH; its standard output, and it stops on
    an error with the tool's message."""
    print("$", " ".join(str(c) for c in command))
    done = subprocess.run([str(c) for c in command], capture_output=True, text=True, **kwargs)
    if done.stdout.strip():
        print(done.stdout.rstrip())
    if done.returncode != 0:
        print(done.stderr.rstrip(), file=sys.stderr)
        raise SystemExit(f"{command[0]} failed with {done.returncode}")
    return done.stdout


def refuses(*command):
    """A tool that is expected to say no: its message, and the exit code."""
    print("$", " ".join(str(c) for c in command))
    done = subprocess.run([str(c) for c in command], capture_output=True, text=True)
    print(f"  exit {done.returncode}: {done.stderr.strip() or done.stdout.strip()}")
    return done.returncode, (done.stderr.strip() or done.stdout.strip())


def five(c):
    """A channel at 15 bits, as the console keeps it."""
    return c >> 3


def wide(c):
    """Five bits back to eight such that the same five come out again."""
    return (c << 3) | (c >> 2)


def rgba_of(picture):
    """An RM2k picture as RGBA with its colour key applied: in an indexed
    picture, index 0 is transparent, whatever colour the file gives it."""
    if picture.mode == "P":
        indexed = picture
        rgba = picture.convert("RGBA")
        for y in range(picture.height):
            for x in range(picture.width):
                if indexed.getpixel((x, y)) == 0:
                    rgba.putpixel((x, y), (0, 0, 0, 0))
        return rgba
    return picture.convert("RGBA")


def quantized(rgba):
    """The picture's opaque pixels at 15 bits: {(x, y): (r, g, b)}."""
    out = {}
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = rgba.getpixel((x, y))
            if a:
                out[(x, y)] = (five(r), five(g), five(b))
    return out


def counts_in_order(pixels):
    """[(colour, pixels)] in the order the colours are first met, row by
    row, which is how Wally hands them to Adeleine."""
    order, count = [], {}
    for y in range(max(y for _, y in pixels) + 1):
        for x in range(max(x for x, _ in pixels) + 1):
            c = pixels.get((x, y))
            if c is None:
                continue
            if c not in count:
                order.append(c)
                count[c] = 0
            count[c] += 1
    return [(c, count[c]) for c in order]


def painted(size, pixels, mapping=None):
    """An RGBA picture from 15-bit pixels, each colour through `mapping`."""
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    for (x, y), c in pixels.items():
        r, g, b = mapping[c] if mapping else c
        out.putpixel((x, y), (wide(r), wide(g), wide(b), 255))
    return out


def over_checker(rgba, square=8):
    """A transparent picture over a checkerboard, to see where it is
    transparent."""
    out = Image.new("RGBA", rgba.size)
    for y in range(rgba.height):
        for x in range(rgba.width):
            out.putpixel((x, y), CHECKER[((x // square) + (y // square)) % 2] + (255,))
    out.alpha_composite(rgba)
    return out


def scaled(picture, factor):
    return picture.resize((picture.width * factor, picture.height * factor), Image.NEAREST)


def row(pictures, gap=GAP, back=BACK):
    """Pictures side by side, top-aligned, on a dark background."""
    width = sum(p.width for p in pictures) + gap * (len(pictures) - 1)
    height = max(p.height for p in pictures)
    out = Image.new("RGBA", (width, height), back + (255,))
    x = 0
    for p in pictures:
        out.alpha_composite(p.convert("RGBA"), (x, 0))
        x += p.width + gap
    return out


def column(pictures, gap=GAP, back=BACK):
    width = max(p.width for p in pictures)
    height = sum(p.height for p in pictures) + gap * (len(pictures) - 1)
    out = Image.new("RGBA", (width, height), back + (255,))
    y = 0
    for p in pictures:
        out.alpha_composite(p.convert("RGBA"), (0, y))
        y += p.height + gap
    return out


def swatches(colours, size=12, per_row=16):
    """Colours as a grid of squares, `None` drawn as a cross."""
    rows = (len(colours) + per_row - 1) // per_row
    out = Image.new("RGBA", (per_row * size, rows * size), BACK + (255,))
    draw = ImageDraw.Draw(out)
    for i, c in enumerate(colours):
        x, y = (i % per_row) * size, (i // per_row) * size
        if c is None:
            draw.line((x + 2, y + 2, x + size - 3, y + size - 3), fill=(120, 120, 120))
            draw.line((x + size - 3, y + 2, x + 2, y + size - 3), fill=(120, 120, 120))
        else:
            r, g, b = c
            draw.rectangle((x, y, x + size - 1, y + size - 1), fill=(wide(r), wide(g), wide(b)))
    return out


def merges_strip(merges, size=16):
    """Each merge as its victim, an arrow and its target."""
    out = Image.new("RGBA", (len(merges) * (size * 2 + 10) + 2, size + 2), BACK + (255,))
    draw = ImageDraw.Draw(out)
    x = 1
    for victim, target, _pixels in merges:
        for i, c in enumerate((victim, target)):
            r, g, b = c
            draw.rectangle((x + i * (size + 6), 1, x + i * (size + 6) + size - 1, size), fill=(wide(r), wide(g), wide(b)))
        draw.line((x + size + 1, size // 2, x + size + 4, size // 2), fill=(220, 220, 220))
        x += size * 2 + 10
    return out


def save(picture, out, name):
    path = os.path.join(out, name)
    picture.convert("RGB").save(path, optimize=True)
    print(f"  wrote {path}: {picture.width}x{picture.height}, {os.path.getsize(path)} bytes")


def write_json(work, name, data):
    path = os.path.join(work, name)
    with open(path, "w") as file:
        json.dump(data, file)
    return path


# --- Adeleine: merge, on one character ----------------------------------------

def adeleine_merge(rtp, work, out):
    """The elder of the test game, People1's character 6, brought to the
    fifteen colours of one object palette, as Wally's sprite half does it
    over the twelve poses."""
    print("\n== Adeleine merge: People1, character 6")
    sheet = rgba_of(Image.open(os.path.join(rtp, "CharSet", "People1.png")))
    index = 6
    x0, y0 = (index % 4) * 72, (index // 4) * 128
    character = sheet.crop((x0, y0, x0 + 72, y0 + 128))
    pixels = quantized(character)
    counts = counts_in_order(pixels)
    print(f"  {len(counts)} colours at 15 bits over the twelve poses; the console gives {USABLE}")
    request = write_json(work, "merge-request.json", {"counts": [[r, g, b, n] for (r, g, b), n in counts], "keep": USABLE})
    run("adeleine", "merge", "--request", request, "--out", work)
    answer = json.load(open(os.path.join(work, "merge.json")))
    mapping = {c: tuple(m) for (c, _), m in zip(counts, answer["mapping"])}
    merges = [(tuple(v), tuple(t), n) for v, t, n in answer["merges"]]
    print(f"  {len(merges)} merges, the first the cheapest; pixels moved per merge: {[n for _, _, n in merges]}")
    before = scaled(over_checker(character), 3)
    after = scaled(over_checker(painted(character.size, pixels, mapping)), 3)
    save(row([before, after]), out, "adeleine-merge.png")
    save(scaled(merges_strip(merges), 2), out, "adeleine-merge-pairs.png")
    return counts, merges


# --- Adeleine: reduce, on a whole ChipSet ------------------------------------

def tiles_of(pixels, width, height):
    """Each 8x8 cell's colours, in the order they are met inside it."""
    tiles = []
    for cy in range(height // CELL):
        for cx in range(width // CELL):
            seen = []
            for y in range(cy * CELL, cy * CELL + CELL):
                for x in range(cx * CELL, cx * CELL + CELL):
                    c = pixels.get((x, y))
                    if c is not None and c not in seen:
                        seen.append(c)
            tiles.append(seen)
    return tiles


def reduced_picture(pixels, size, tiles, answer):
    """The picture after `reduce`: every pixel of every tile through its
    tile's mapping, and the index each pixel gets in colour memory."""
    width, _ = size
    mapping = {}
    for n, (tile, decided) in enumerate(zip(tiles, answer["tiles"])):
        # A cell with nothing drawn gets no palette.
        if decided["palette"] is None:
            continue
        cx, cy = n % (width // CELL), n // (width // CELL)
        local = {c: tuple(m) for c, m in zip(tile, decided["mapping"])}
        palette = answer["palettes"][decided["palette"]]
        entry = {tuple(c): i + 1 for i, c in enumerate(palette)}
        for y in range(cy * CELL, cy * CELL + CELL):
            for x in range(cx * CELL, cx * CELL + CELL):
                c = pixels.get((x, y))
                if c is not None:
                    mapping[(x, y)] = (local[c], decided["palette"] * PALETTE + entry[local[c]])
    return mapping


def indexed_png(size, mapping, palettes, path):
    """An 8-bit indexed PNG whose indices are colour-memory entries, with
    every entry's colour as its palette: Voodoo's input."""
    out = Image.new("P", size, 0)
    for (x, y), (_, entry) in mapping.items():
        out.putpixel((x, y), entry)
    memory = [0, 0, 0] * 256
    for p, palette in enumerate(palettes):
        for i, (r, g, b) in enumerate(palette):
            e = p * PALETTE + i + 1
            memory[e * 3:e * 3 + 3] = [wide(r), wide(g), wide(b)]
    out.putpalette(memory)
    out.save(path)
    return path


def adeleine_reduce(rtp, work, out):
    """The Exterior ChipSet into eight, four, two and one palettes of
    fifteen, the way the layer above the hero is split."""
    print("\n== Adeleine reduce: the Exterior ChipSet")
    chipset = rgba_of(Image.open(os.path.join(rtp, "ChipSet", "Exterior.png")))
    pixels = quantized(chipset)
    counts = counts_in_order(pixels)
    tiles = tiles_of(pixels, chipset.width, chipset.height)
    print(f"  {len(counts)} colours at 15 bits, {len(tiles)} cells, {len([t for t in tiles if t])} with something drawn")
    crop = (192, 0, 384, 128)
    panels = [scaled(over_checker(chipset.crop(crop)), 2)]
    request = write_json(work, "pack-request.json", {"tiles": tiles, "palettes": 8})
    run("adeleine", "pack", "--request", request, "--out", work)
    packed = json.load(open(os.path.join(work, "pack.json")))
    print(f"  pack into 8 palettes, merging nothing: {'fits' if packed['palettes'] else 'does not fit'}")
    eight = None
    for n in (8, 4, 2, 1):
        request = write_json(work, f"reduce-{n}-request.json",
                             {"counts": [[r, g, b, k] for (r, g, b), k in counts], "tiles": tiles, "palettes": n})
        run("adeleine", "reduce", "--request", request, "--out", work)
        answer = json.load(open(os.path.join(work, "reduce.json")))
        mapping = reduced_picture(pixels, chipset.size, tiles, answer)
        kept = len({c for c, _ in mapping.values()})
        print(f"  {n} palette(s): {len(answer['merges'])} merges, {kept} colours left on the picture")
        after = Image.new("RGBA", chipset.size, (0, 0, 0, 0))
        for (x, y), (c, _) in mapping.items():
            r, g, b = c
            after.putpixel((x, y), (wide(r), wide(g), wide(b), 255))
        panels.append(scaled(over_checker(after.crop(crop)), 2))
        if n == 8:
            eight = indexed_png(chipset.size, mapping, answer["palettes"], os.path.join(work, "exterior-8.png"))
    save(column([row(panels[:3]), row(panels[3:])]), out, "adeleine-reduce.png")
    return eight


# --- Voodoo and LZ2 -----------------------------------------------------------

def voodoo_and_lz2(work, out, exterior_eight, meadow_background):
    print("\n== Voodoo: the ChipSet, reduced, into tiles")
    code, message = refuses("voodoo", "convert", exterior_eight, "--bpp", "4", "-o", os.path.join(work, "ex.4bpp"),
                            "--palette", os.path.join(work, "ex.cgram"), "--tilemap", os.path.join(work, "ex.map"), "--json")
    voodoo_said = (code, message)
    print("\n== Voodoo: the meadow's background, as Wally left it")
    tiles, cgram, tilemap = (os.path.join(work, f"meadow.{e}") for e in ("8bpp", "cgram", "map"))
    said = run("voodoo", "convert", meadow_background, "--bpp", "8", "-o", tiles, "--palette", cgram, "--tilemap", tilemap, "--json")
    report = json.loads(said)
    count = os.path.getsize(tiles) // 64
    # The tiles in a row, each drawn once: a tilemap that counts.
    sequence = os.path.join(work, "sequence.map")
    columns = min(count, 32)
    with open(sequence, "wb") as file:
        file.write(b"".join(struct.pack("<H", n) for n in range(count)))
        file.write(b"".join(struct.pack("<H", 0) for _ in range(-count % columns)))
    sheet = os.path.join(work, "sheet.png")
    run("voodoo", "render", tiles, "--palette", cgram, "--tilemap", sequence, "--columns", str(columns), "--bpp", "8", "-o", sheet)
    back = os.path.join(work, "back.png")
    run("voodoo", "render", tiles, "--palette", cgram, "--tilemap", tilemap, "--columns", "40", "--bpp", "8", "-o", back)
    same = list(Image.open(back).convert("RGB").getdata()) == list(Image.open(meadow_background).convert("RGB").getdata())
    print(f"  render gives the picture back {'identical' if same else 'DIFFERENT'}")
    save(scaled(Image.open(sheet).convert("RGBA"), 4), out, "voodoo-tiles.png")

    print("\n== LZ2: the meadow's tiles and tilemap")
    run("lz2", "compress", tiles, tiles + ".lz2", tilemap, tilemap + ".lz2")
    stats = run("lz2", "stats", tiles + ".lz2", tilemap + ".lz2")
    run("lz2", "decompress", tiles + ".lz2", tiles + ".back")
    same = open(tiles, "rb").read() == open(tiles + ".back", "rb").read()
    print(f"  decompress gives the tiles back {'identical' if same else 'DIFFERENT'}")
    return voodoo_said, report, stats


# --- Gunter -------------------------------------------------------------------

def samples_of(path):
    with wave.open(path) as file:
        assert file.getsampwidth() == 2 and file.getnchannels() == 1
        raw = file.readframes(file.getnframes())
        return struct.unpack(f"<{len(raw) // 2}h", raw), file.getframerate()


def waveform(samples, start, count, width=480, height=72, colour=(120, 200, 255)):
    out = Image.new("RGBA", (width, height), BACK + (255,))
    draw = ImageDraw.Draw(out)
    draw.line((0, height // 2, width, height // 2), fill=(80, 80, 80))
    peak = max(1, max(abs(s) for s in samples[start:start + count]))
    points = []
    for i in range(count):
        x = i * (width - 1) / (count - 1)
        y = height // 2 - samples[start + i] * (height // 2 - 2) / peak
        points.append((x, y))
    draw.line(points, fill=colour, width=1)
    return out


def gunter(soundfont, work, out):
    print("\n== Gunter: a piano from the SoundFont, into BRR and back")
    piano = os.path.join(work, "piano.wav")
    contract = json.loads(run("gunter", "sf2", soundfont, "--extract", "program:0", "-o", piano, "--json"))
    brr = os.path.join(work, "piano.brr")
    encoded = json.loads(run("gunter", "encode", piano, "-o", brr, "--json"))
    back = os.path.join(work, "piano-back.wav")
    run("gunter", "decode", brr, "-o", back, "--rate", str(encoded["rate"]))
    run("gunter", "info", brr)
    original, rate = samples_of(piano)
    decoded, _ = samples_of(back)
    # A window a little after the attack, where the waveform is busy.
    start = min(len(original) - 1, max(0, next((i for i, s in enumerate(original) if abs(s) > 2000), 0) + 400))
    count = min(600, len(original) - start, len(decoded) - start)
    save(column([waveform(original, start, count), waveform(decoded, start, count, colour=(255, 190, 120))]),
         out, "gunter-brr.png")
    return contract, encoded


# --- rm2k-render and Wally, on the test game's meadow --------------------------

def render_and_wally(test_game, work, out):
    data = os.path.join(test_game, "build", "data")
    game = os.path.join(test_game, "build", "game")
    empty = os.path.join(work, "no-rtp")
    os.makedirs(empty, exist_ok=True)
    print("\n== rm2k-render: the meadow's two layers")
    rendered = os.path.join(work, "render")
    os.makedirs(rendered, exist_ok=True)
    run("rm2k-render", "layers", "--map", "1", "--data", data, "--game-dir", game, "--rtp-dir", empty, "--out", rendered)
    lower = Image.open(os.path.join(rendered, "lower.png")).convert("RGBA")
    upper = Image.open(os.path.join(rendered, "upper.png")).convert("RGBA")
    save(row([lower, over_checker(upper)]), out, "rm2k-render-meadow.png")

    print("\n== rm2k-snes-screens window: the System's colours, in the message window")
    window = os.path.join(work, "window")
    os.makedirs(window, exist_ok=True)
    request = write_json(work, "window-request.json", {})
    run("rm2k-snes-screens", "window", "--data", data, "--game-dir", game, "--rtp-dir", empty, "--request", request, "--out", window)
    answer = json.load(open(os.path.join(window, "window.json")))
    print(f"  the window draws with {answer['brought']} colours and takes {answer['colors']} entries after {len(answer['merges'])} merges")
    system = rgba_of(Image.open(os.path.join(game, "System", "System.png")))
    pixels = quantized(system)
    mapping = {c: c for c in set(pixels.values())}
    for victim, target, _ in answer["merges"]:
        victim, target = tuple(victim), tuple(target)
        for c, m in mapping.items():
            if m == victim:
                mapping[c] = target
    save(row([scaled(over_checker(system), 2), scaled(over_checker(painted(system.size, pixels, mapping)), 2)]), out, "screens-window.png")
    save(scaled(merges_strip([(tuple(v), tuple(t), n) for v, t, n in answer["merges"]]), 2), out, "screens-window-pairs.png")

    print("\n== wally layers: the meadow, as the cartridge carries it")
    layers = os.path.join(work, "wally")
    os.makedirs(layers, exist_ok=True)
    request = write_json(work, "layers-request.json",
                         {"map": 1, "map_files": {}, "chipset_files": {}, "baked": [], "window_colors": answer["colors"]})
    run("wally", "layers", "--data", data, "--search-dir", game, "--request", request, "--out", layers)
    said = json.load(open(os.path.join(layers, "layers.json")))
    bg, above = said["background"], said["above"]
    print(f"  background: {bg['used']} colours of a budget of {bg['budget']}, {bg['tiles']} tiles over {bg['cells']} cells, {len(bg['merges'])} merges")
    print(f"  above: first palette {above['first']}, {len(above['merges'])} merges")
    background = Image.open(os.path.join(layers, "background.png"))
    above_png = Image.open(os.path.join(layers, "above.png"))
    # Each picture carries colour memory as its palette, with colours only
    # where it draws: the layer above's palette comes from its own file.
    bg_memory, ab_memory = background.getpalette(), above_png.getpalette()
    bg_drawn = set(background.getdata())
    ab_drawn = {i for i in above_png.getdata() if i % PALETTE}
    entries = []
    for e in range(128):
        memory = ab_memory if e in ab_drawn else bg_memory
        r, g, b = memory[e * 3:e * 3 + 3]
        entries.append((five(r), five(g), five(b)))
    drawn = bg_drawn | ab_drawn
    grid = swatches([c if e in drawn or e == 0 else None for e, c in enumerate(entries)], size=10)
    bg_rgba = background.convert("RGBA")
    ab_rgba = above_png.convert("RGBA")
    for y in range(ab_rgba.height):
        for x in range(ab_rgba.width):
            if above_png.getpixel((x, y)) % PALETTE == 0:
                ab_rgba.putpixel((x, y), (0, 0, 0, 0))
    save(row([bg_rgba, over_checker(ab_rgba), scaled(grid, 2)]), out, "wally-meadow.png")
    return os.path.join(layers, "background.png"), answer, said


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--rtp", required=True, help="EasyRPG's RTP, with ChipSet/ and CharSet/ inside")
    parser.add_argument("--soundfont", required=True, help="a .sf2 to take Gunter's sample from")
    parser.add_argument("--test-game", required=True, help="the-advocate's test-game/, with build/ made by `just game`")
    parser.add_argument("--out", required=True, help="the book's src/tools/")
    parser.add_argument("--work", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"),
                        help="where the requests, answers and intermediate files go")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.work, exist_ok=True)
    adeleine_merge(args.rtp, args.work, args.out)
    eight = adeleine_reduce(args.rtp, args.work, args.out)
    meadow_background, _, _ = render_and_wally(args.test_game, args.work, args.out)
    voodoo_and_lz2(args.work, args.out, eight, meadow_background)
    gunter(args.soundfont, args.work, args.out)


if __name__ == "__main__":
    main()
