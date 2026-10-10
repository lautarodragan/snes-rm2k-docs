# The map takes to VRAM only what it draws

## What

The ROM does not take the whole ChipSet to VRAM, as RM2k does, but **the
unique tiles of what the map draws**: the converter renders the map and takes
the tiles from there. An expanded RM2k chipset is hundreds of 8x8 tiles, and
they do not fit in what is left for the background with the message window
in place.

What is lost is that **two maps with the same chipset share their tiles**,
which would save cartridge bytes and the VRAM reload when crossing from one
to the other.

## Measured

On 2026-09-07, counting only the ids some map of the game uses: `ChipSet3`
gives 420 tiles and `BLchp1` 523. Map 1 draws 341 and map 2, 278, against the
420 of the chipset they share; the shared pool of the two is 437 and did not
fit in any VRAM layout of that day. The full count is in
[the study on RM2k graphics on the SNES](../research/graficos-de-rm2k-a-snes.md),
"Sharing tiles between maps".

## How it looks today

It is not seen: each map draws the same as in RM2k. Each map's layout is
chosen by `vram_layout` in `tools/port/vram.py` in snes-rm2k, and
`docs/port/vram.md` in snes-rm2k explains where the possible ones come from.

## When it stops being enough

A game whose maps use more distinct background tiles than fit in any layout.
There no layout saves it: VRAM has to be reloaded while the map scrolls,
which is a different engine from the one there is.
