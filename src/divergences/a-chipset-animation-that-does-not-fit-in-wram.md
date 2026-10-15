# A ChipSet animation that does not fit in WRAM

## What

The tiles the ChipSet animates —the water, three drawings, and the animated
tiles, four— go in one run per family at the end of the background's bank,
and the console uploads each drawing of a run from WRAM whenever the clock
changes. Those drawings have 8 KB of WRAM, `ANIM_DRAWINGS` in the runtime's
`far_ram.s`: room for 128 tiles' worth of drawings at 8 bits per pixel, so
for 42 water tiles with no animated ones, or 32 animated tiles with no
water.

A map whose drawings take more **keeps the tiles that cover the most cells
of the map moving, and the rest stand still on their first drawing**, with a
warning in the converter's log. RM2k animates them all. Before 2026-10-10
such a map did not build.

Standing still needs nothing redrawn: the bank already carries each tile's
first drawing, which is how RM2k shows it before the clock moves, and the
console uploads only the first tiles of each drawing. So a run is cut, not
reordered, and how much of each family stays is the one choice: the one
that keeps the most cells of the map moving within the 8 KB. The tiles that
stay are the first ones Voodoo numbered, which are the first met row by
row, and those turn out to be the ones the map uses most.

See `rm2k-snes/mapdata/src/animation.rs` in the-advocate.

## Measured

On 2026-10-10, each map in a cartridge with its game's starting map:

| Map | Drawings | What stands still |
|---|---|---|
| *The Book of Three*, 46 | 10,432 bytes | 9 of its 25 water tiles: 25 of 115 cells; 2 of its 22 animated tiles: 2 of 2,185 cells |
| *Desert Nightmare*, 182 | 9,792 bytes | 9 of its 51 water tiles: 44 of 1,469 cells |
| *Vampires Dawn*, 236 | 9,792 bytes | 9 of its 51 water tiles: 26 of 1,480 cells |
| *Vampires Dawn*, 351 | 9,152 bytes | 5 of its 37 water tiles: 9 of 674 cells |
| *Vampires Dawn*, 1 | 27,264 bytes | 100 of its 142 water tiles: 4,275 of 262,866 cells |

*A Blurred Line* has no such map: its cartridge comes out byte for byte the
same. To see it, build *The Book of Three* or *Desert Nightmare*: the
warning is in the release's `converter.log`, one line per map.

## How it looks today

Where a frozen tile borders one that moves, the water is still in one
8x8 cell and moving in the next. In the first four maps it is a handful of
edge cells; in *Vampires Dawn*'s world map it is most of the water's
shapes, but not most of its cells: the open sea moves.

## As an optimization

What it saves, and where it lives in the code: [A ChipSet animation that does not fit in WRAM stands still in part](../optimizations/lossy/tiles.md#a-chipset-animation-that-does-not-fit-in-wram-stands-still-in-part), in Optimizations.
