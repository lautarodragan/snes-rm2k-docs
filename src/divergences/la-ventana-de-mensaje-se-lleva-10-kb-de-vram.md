# The message window takes 10 KB of VRAM

## What

The message window takes **8 KB of tiles and 2 KB of tilemap of its own**
out of the 64 KB of VRAM, and that is what shrinks the background's bank in
every layout that carries it.

The tiles of the text area are 240 because **the glyph is not 8 pixels
wide**: it does not line up with the cell, so each cell is a tile of its own
that the ROM composes pixel by pixel. It is what Final Fantasy does, and it
was checked against its decompilation before ruling out alternatives.

Until 2026-10-03 the glyph was 6 wide, RM2k's, and the line had 39
characters. Since that day the font is variable width —the `low-variable`
sheet in `tools/rm2k-snes/text/fonts/` in the-advocate, or whichever the game
names in `[text] font`— and the line measures **240 pixels**: with that font
about 49 letters fit, almost as many as RM2k's window, which at 320 wide and
6 per letter takes about 50.

## Measured

The alternative that exists and was not taken: 8-pixel glyphs, aligned to
the cell. It would save about 48 tiles —1.5 KB, that is, 24 background
tiles— and bring the line down to **30 characters**. Measured on
2026-10-03: with 39, 1245 of ABL's boxes were re-flowed and 299 did not fit
in a single one; with the variable-width font, one is re-flowed.

## How it looks today

Almost as in RM2k: ABL's boxes fit as the author wrote them. What it costs
is VRAM, not something that shows. The width of the line is in the
`layout.rs` of `rm2k-snes-screens`, next to the 240 tiles.

## When it stops being enough

A box that does not fit is re-flowed —`refit` in `rm2k-snes-text`, which
measures in pixels with the same font—, so what does not fit stops being cut
text and becomes one extra box. Going to 30 columns would be only an
aesthetic cost; with the variable-width font, a large one.
