# Lossless: CPU time in the frame

## The hottest NPC code in bank 1, unrolled

What runs for every NPC row on every frame lives in bank 1, run from the
fast mirror, because bank 0 had no room to make it faster: hiding the 128
objects at the start of each frame is unrolled, and a row that moved is
moved to its place in the sorted table in one search and one block move
—`mvn`/`mvp`—, instead of re-sorting the table or swapping one place at a
time.

- **Saves**: scan lines of every frame, on every map.
- **Where**: `oam_hide` and `fit_far` in `runtime/far_npcs.s`.
- **More**: the header of `runtime/far_npcs.s`.

## The tint's tables are copied, not rebuilt

While a flash lasts, the palette is rebuilt every frame; the tint's three
channel tables —products and divisions— are kept in a pristine copy and
restored by copying it, and the flash's own table saves the tint's
computation per entry. A picture's tint reuses the same tables and
restores them the same way.

- **Saves**: CPU on every frame of a flash or a tinted picture.
- **Where**: `tint_tables`, `restore_tables` and `flash_channel_table` in
  `runtime/character_flash.s`; `pic_palette` in `runtime/picture.s`.
- **More**: the comments of those routines.

## A DSP write the register already has is skipped

The music decoder keeps a copy of what it wrote to each DSP register, and
does not write again a value the register already holds.

- **Saves**: writes through the SPC700's ports, every music frame.
- **Where**: `mus_write` and `MUS_SHADOW` in `runtime/music.s`.
- **More**: [Audio](../../internals/audio.md).
