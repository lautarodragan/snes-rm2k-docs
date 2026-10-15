# Maps

#### The map is not stored as a tilemap

Expanded, it would not fit in the cartridge: 1000×80 cells at two bytes
each are 156 KB, more than the whole ROM. What is stored is **RM2k's 16×16
cell**, which is the unit the game was drawn with and which repeats a lot.

```text
map 52, 1000x80 cells    expanded tilemap   160,000 B
                         block grid          40,000 B + 1,744 B of table
```

A block carries its four background cells, its four cells of the layer
above, and its passability, all together. In the whole game the maximum is
512 distinct blocks.

Having passability travel in the block **erased the whole collision
table** —one byte per cell, up to 20 KB—. And it is not a shortcut: two
cells that are drawn the same could have different permissions if they came
from different ChipSet tiles, so passability goes into the key blocks are
deduplicated by, and those two separate on their own.

Where the hero is inside the grid isn't an index either but a **pointer
that moves with him**, one cell or one row per step. That way nothing ever
has to multiply or build a 24-bit address from scratch, which is awkward
because the grid crosses banks and the banks are not contiguous: going past
`$FFFF` leads to the next bank's `$8000`, and only `ptr_more` and
`ptr_minus` know that.

#### The grid lives in WRAM, and the cartridge carries it compressed

Since 2026-09-26 the grid travels in the cartridge as LZ2 and is
decompressed whole when the map loads, at `$7E8000`, continuing at
`$7F8000` if it is over 32 KB (`GRID` in `runtime/far_ram.s`,
`lz2_grid` in `decompress.s`). The upper halves of two consecutive WRAM
banks have the shape of two LoROM banks, so the readers didn't change:
the pointer used to point into the cartridge, now it points into WRAM. A
battle overwrites the `$7F` half, and `back_from_battle` decompresses it
again. What reserving that RAM cost and how it is reverted:
[the grid lives in WRAM](../optimizations/lossless/the-map/the-grid-in-wram.md).

The same happens with the tiles of the background, of the layer above, of
the sprites, and with the drawings of the ChipSet animation: they travel as
LZ2, are decompressed to `$7F0000` and uploaded with the same DMA as
before. The animation drawings stay at `$7F6000` for as long as the map
lasts, because they are uploaded every time the clock changes. How each
block is split into streams and with which WRAM limits: `materials.rs` in
`rm2k-snes/mapdata/`; the format and the compressor:
`snes/lz2/`, which the emission uses as a library.

And since 2026-10-01, **the block table, its passability and the event
bytecode**: the CPU reads them while the game is played, so they are not
uploaded to VRAM but live in WRAM **right behind the grid**, in the `$7F`
half. The blocks travel as a third stream stuck to the two of the grid, and
the bytecode in one of its own, which the `map_code` table names;
`lz2_grid` decompresses each where the previous one ended, and they come
back with it after a battle. What happens to a page that keeps running in
another map: see [Events](events.md). The address is not computed by the
ROM: the converter puts it in the map's record (`map_ram_pointers` in
`record.rs`), and the test below checks that it matches where things ended
up. The converter stops if a map doesn't fit: what the grid takes of `$7F`
plus what goes behind it can't exceed its 32 KB. The bytecode is the
exception: a map whose code does not fit keeps it in the cartridge (see
[Events](events.md)).

What is left in VRAM and WRAM after loading is compared by
`tests/rpgmaker/test_decompressed_load.py` in the ABL port against what
the converter leaves uncompressed in ABL's `build/<cartridge>/crudos/`.
