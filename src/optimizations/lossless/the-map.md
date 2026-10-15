# Lossless: the map

## The 16x16 block grid

The map is not stored as a tilemap but as a grid of RM2k's 16x16 cells,
each pointing to a **block** that carries its four background cells, its
four cells of the layer above and its passability. Blocks repeat a lot,
and identical ones are stored once. Expanded, a big map's tilemap would
not fit in the cartridge at all.

- **Saves**: ROM —one grid entry per 16x16 cell instead of four tilemap
  entries per layer—; and since passability travels in the block, **the
  whole collision table** —one byte per cell— is gone.
- **Where**: `materials.rs` in `rm2k-snes/mapdata/`; the readers, `ptr_more`
  and `ptr_minus` in the runtime.
- **More**: [Maps](../../internals/maps.md).

## A pointer that walks with the hero

Where the hero is in the grid is a 24-bit pointer that moves one cell or
one row per step, not an index: nothing multiplies or builds an address
from scratch, even though the grid crosses banks.

- **Saves**: CPU on every step and every passability question.
- **Where**: `ptr_more` and `ptr_minus`, the only routines that know how
  the grid crosses a bank.
- **More**: [Maps](../../internals/maps.md).

## The grid, its blocks and the bytecode, in LZ2 and decompressed into WRAM

The grid travels in the cartridge as LZ2 and is decompressed whole into
the upper halves of the two WRAM banks when the map loads; the block
table, its passability and the event bytecode go right behind it, in the
same load. The upper half of two consecutive WRAM banks has the shape of
two LoROM banks, so the readers did not change.

- **Saves**: ROM, most of the grids' weight, keeping direct access cell
  by cell.
- **Costs**: 32 KB of far RAM in `$7E`, and the decompression on every map
  load and on returning from a battle.
- **Where**: `GRID` in `runtime/far_ram.s`, `lz2_grid` in
  `runtime/decompress.s`, `map_ram_pointers` in `record.rs` of
  `rm2k-snes/mapdata/`.
- **More**: [The grid lives in WRAM](the-map/the-grid-in-wram.md), with what it
  costs, how to know it needs reverting and how;
  [Maps](../../internals/maps.md).

## The map's tiles in LZ2

The tiles of the background, of the layer above, of the sprite bank and
the drawings of the ChipSet animation travel as LZ2, are decompressed into
a WRAM buffer and uploaded with the same DMA as before. A background too
big for the buffer goes in two streams.

- **Saves**: ROM.
- **Where**: `materials.rs` in `rm2k-snes/mapdata/`; the format and the
  compressor, `snes/lz2/`; `lz2_backdrop` in `runtime/decompress.s`.
- **More**: [Maps](../../internals/maps.md), [The VRAM split](../../internals/vram.md).

## Only the tiles the map draws go to VRAM

The ROM does not take the whole ChipSet to VRAM, as RM2k does, but the
unique 8x8 tiles of what the map draws: the converter renders the map and
takes the tiles from there. An expanded ChipSet is hundreds of 8x8 tiles,
and they do not fit in what is left for the background next to the
message window. Nothing changes on screen: each map draws as in RM2k.

On 2026-09-07, counting only the ids some map of ABL uses, `ChipSet3`
gave 420 tiles and `BLchp1` 523; map 1 drew 341 and map 2, 278, against
the 420 of the ChipSet they share, and the pool of the two, 437, fit in no
VRAM layout of that day. The full count is in [the study on RM2k graphics
on the SNES](../../research/graphics-and-sound-from-rm2k-to-the-snes.md),
"Sharing tiles between maps".

- **Saves**: VRAM.
- **Costs**: two maps with the same ChipSet do not share their tiles,
  which would save cartridge bytes and the VRAM reload between them.
- **When it stops being enough**: a game whose maps use more distinct
  background tiles than any layout holds. No layout saves that: VRAM would
  have to be reloaded while the map scrolls, a different engine from this
  one —except for a painted map, below—.
- **Where**: Wally, `rm2k-snes/wally/`; the layout, `vram_layout` in
  `vram.rs` of `rm2k-snes/mapdata/`.
- **More**: [The VRAM split](../../internals/vram.md).

## The VRAM layout is chosen map by map

There is no single split of the 64 KB that serves every map, so the
converter picks, for each map, the first of a fixed list of layouts where
its background, its sprites and its layer above fit, and emits the
register values ready-made. New layouts go at the end, so no map that
already fit changes.

- **Saves**: VRAM —each map gets the split it needs, within the
  hardware's alignments—.
- **Where**: `vram_layout` and `LAYOUT_WINDOW*` in `vram.rs` of
  `rm2k-snes/mapdata/`.
- **More**: [The VRAM split](../../internals/vram.md).

## The CGRAM split is chosen map by map, background first

The lower half of CGRAM is shared by the 8-bit background and the 4-bit
layer above. The converter decides the cut for each map: the background
keeps the palettes it needs, and the layer above takes what is left.

- **Saves**: CGRAM —no fixed cut serves every map—; merging colours only
  where nothing else is left.
- **Where**: `convert_with` in `rm2k-snes/wally/src/background/layers.rs`.
- **More**: [The CGRAM split](../../internals/cgram.md).

## Opaque fixed events baked into the map

An event drawn with a ChipSet tile that is also opaque and never moves is
painted into the map, and its row is hidden from the sprite pass.

- **Saves**: sprite tiles, OAM entries and CPU in `build_oam`.
- **Where**: `baking::bakeable` in Wally (`rm2k-snes/wally/src/baking.rs`);
  `build_oam` skips the hidden row.
- **More**: [Events](../../internals/events.md).

## A painted map keeps only what the screen shows

A map whose panorama *is* the map goes in BG1 in mode 1, one tile per 8x8
cell, and VRAM holds only the cells the screen can show, in a ring of
slots that the camera fills as it moves. A spare row uploaded ahead keeps
the vblank short.

- **Saves**: VRAM —a painted map has far more distinct cells than any
  layout holds—.
- **Where**: `runtime/painted.s`, `paint_table` in `panorama.rs` of
  `rm2k-snes/mapdata/`. Only a cartridge with a painted map assembles it.
- **More**: [The VRAM split](../../internals/vram.md#a-painted-map-keeps-only-what-the-screen-shows).

## A panorama gets only the layer it needs

For each map the tools choose how to show its panorama: not at all if it
is never seen, baked into the background if it does not move against the
map, in the second layer if the map draws little above the hero, or with
the map in mode 1 and the panorama on a third layer.

- **Saves**: VRAM and a background layer, in the maps that do not need
  one.
- **Where**: `Way` in `rm2k-snes/wally/src/background/panorama.rs`;
  `runtime/pano.s`.
- **More**: [Mode 3 by default](../../internals/mode-3.md),
  [Panoramas](../../research/2026-10-05-panoramas.md).
