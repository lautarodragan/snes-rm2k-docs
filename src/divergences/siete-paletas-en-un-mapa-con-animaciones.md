# Seven palettes on a map with animations

## What

The battle animation's box needs **a whole sprite palette to itself**: its
fifteen colors belong to the animation and are overwritten when another one
starts, so a character placed there would change color with it. On the maps
that show animations the characters share **seven** palettes instead of
eight, and that merges more of their colors than in RM2k, where there are no
palettes.

**Unless the timer does not fit in seven**: then the timer wins, it goes back
to eight and that map does not draw animations. The rule is
`map_palette_cap`, in `tools/port/obj_extras.py` in snes-rm2k, which says how
many palettes the characters share.

## Measured

On 2026-09-12 the maps with animations were 2 and 3, the intro's. The one
left without a box because of the timer was 9.

## How it looks today

The characters on those maps may have an extra merged color or two; the
converter writes down each map's merges next to the ROM.
