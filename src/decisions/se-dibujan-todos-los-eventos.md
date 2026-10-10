# Every event is drawn

## What

**Every event is drawn, even if with someone else's palette.**

## Why

It is taro's, from 2026-09-08: *"if we can't include every event, the
whole project falls apart"*. The one that doesn't get its own palette
hangs on to the one it is missing the fewest colors from, and each missing
color goes to the nearest by luma. A sprite with its colors changed is a
visible error; one that isn't drawn is an invisible wall that triggers and
blocks the way, and it already cost an afternoon with the door Core
breaks.

## Measured

What it costs, measured before deciding. Per graphic, the percentage of its
pixels that change color and the worst jump in one channel, out of 31:

    @tile:BLchp1:112     0%
    Chara2:0            21%, jump 9
    @tile:BLchp1:53     23%, jump 11
    Future1:7           38%, jump 15
    @tile:BLchp1:117    42%, jump 1     ← the door of Talan's pad
    Future3:1           49%, jump 17
    @tile:BLchp1:111    70%, jump 13

The door is the case that shows why the percentage alone isn't enough: 42%
of its pixels change, but none moves more than 1 out of 31, so to the eye
it is the same door.

What it unblocked: map 8 —the street the pad opens onto— asked for
thirteen palettes out of eight and no split was possible, and it went on to
fit with six borrowed graphics, the save point among them; the Hover-Tram
(map 13) asked for eleven and went on to fit with two. The limit stopped
being the number of palettes and became the sprite tile budget in VRAM:
see `docs/port/vram.md` in the-advocate.
