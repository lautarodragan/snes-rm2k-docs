# A cell with both ChipSet animations

## What

Cells that change carry their own tiles, in one run per family: one for the
water and another for the animated tiles. A cell that changed with both
—water on the lower layer and an animated tile on the upper one— would need
every combination of frames and not two runs, so **Voodoo rejects it** and
the converter does not build the ROM. RM2k draws it without trouble.

See "Animations" in `tools/snes/voodoo/README.md` in snes-rm2k.

## Measured

On 2026-09-09, zero such cells in the 328 `.lmu` files the game ships.

## How it looks today

It is not seen: there are none in *A Blurred Line*. It is one of the ones to
look at if this is pointed at another game, and there it stops with the cell
in the error message instead of emitting a drawing that is right half of the
time.
