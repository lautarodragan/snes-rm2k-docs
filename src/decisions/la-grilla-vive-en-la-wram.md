# The grid lives in WRAM

## What

**The map's grid is decompressed whole into WRAM when the map loads, and
lives at `$7E8000-$7EFFFF`**, continuing at `$7F8000` if it goes past
32 KB: the upper half of both banks (`GRID` in `tools/runtime/far_ram.s`
in the-advocate). The cartridge carries it in LZ2, in two streams, one per
half (`lz2_grid` in `tools/runtime/decompress.s`).

Decided with taro on 2026-09-26, **as a trial, knowing it may have to be
reverted**.

## Why

The grids weighed 278 KB in `release` and in LZ2 they weigh 32: it is the
second biggest saving in the cartridge after the tiles. But they are read
cell by cell all the time —every strip that comes on screen, every
passability question— and they can't be read compressed. The two ways out
were splitting them into deduplicated 4×4 chunks, which saves 214 KB and
adds an indirection to every reader of the grid, or decompressing them
whole into WRAM and leaving direct access as it was. The second is better
in everything except RAM, and **it took changing two reads**: only
`ptr_more` and `ptr_minus` knew the grid was in LoROM, and the upper half
of two consecutive WRAM banks has the same shape as two LoROM banks.

taro's reasoning for accepting the cost: the maps and events already in the
ROM are a good sample of what happens in an RM2k game; if all of Lashe City
works with the RAM that is left, the rest of the game —close to 90% of it is
there— will too.

## What is lost

* **Half of the far RAM that was still free**: 32 KB of bank $7E. Before
  this, used far RAM reached `$7E7FFF` and from `$7E8000` on there was
  nothing; the day more RM2k state is needed —more variables, more
  switches, more events per map, a second interpreter— that is where it was
  going to go. What remains is `$7E7805-$7E7FFF` and the gaps below.
* **The upper half of $7F is shared with the battle** (`SCN_SCENE`), which
  overwrites it: on maps with more than 32 KB of grid it has to be
  decompressed again after leaving a battle. `back_from_battle` always
  decompresses it whole, which costs the same as on entering the map: 1.7
  frames on average and 8 on map 52, the 40 KB one.
* **Loading frames**: decompressing the grid adds the same as above to
  every map change. Measured in the ROM over `release`'s forty maps.
* **A map with more than 64 KB of grid doesn't fit**: the converter stops.
  The biggest today is 40,000 B (map 52, 500×40). RM2k goes up to 500×500,
  which would be 500 KB: a map like that doesn't fit in any way without
  chunks.

## How you would know it needs reverting

* **`pruebas/herramientas/test_reservas_de_la_wram.py` in the ABL port
  (the-advocate-ports/abl) fails** if any cartridge symbol falls in
  `$7E8000-$7FFFFF` and isn't the grid, the loading buffer or the battle
  scene. It is the alarm for whoever needs far RAM: if it fails, it isn't
  to add the symbol to its list, it is to read this. It doesn't see an
  address written as sixteen bits and used with the data bank at `$7E`,
  like `FAR_BATTLE`.
* **`pruebas/rpgmaker/test_carga_descomprimida.py` in the ABL port compares
  the whole grid in WRAM** against the one the converter left, on each of
  the forty maps, in snes9x and in bsnes, and **on returning from a battle**
  on map 52. An intruder writing there on those paths makes it fail.
* Or a map of the game still missing asks for more than 64 KB of grid, or
  what is still missing of RM2k doesn't fit in the far RAM that is left.

## How it is reverted

The grid goes back to the cartridge, not in LZ2: uncompressed, or in 4×4
chunks.

1. In `tools/port/snes_convert.py`, take `map_celdas` out of
   `CLASES_COMPRIMIDAS` and emit it again with `materiales.guardar(...,
   alinear=2)`: it doesn't need to be whole in one bank, `ptr_more` walks
   it.
2. In the ROM, the two reads of `GRID` —`cell_ptr` in `hero.s` and
   `fill_window` in `map_window.s`— go back to reading
   `map_table + M_PTR_MAP_CELLS`, and the two calls to `lz2_grid` —in
   `enter_map_no_events` and in `back_from_battle`— are removed.
3. `GRID` and its reservation in `far_ram.s`, `lz2_grid`, and the grid
   parts of `test_carga_descomprimida.py` and
   `test_reservas_de_la_wram.py` are deleted.

That is 246 KB of cartridge back. The rest of the compression —the tiles—
doesn't depend on this: its buffer is in bank $7F, which the battle already
used.

**Since 2026-10-01 the block table, its passability and the events'
bytecode depend on this**: they live in WRAM right behind the grid, and
`lz2_grid` decompresses them along with it (see `docs/port/maps.md` in
the-advocate). Reverting the grid also requires returning them to the
cartridge, uncompressed: in `rm2k-snes-mapdata`, take `map_ram` and
`map_code` out of `COMPRESSED_KINDS` and store them again as standalone
blocks with their labels in the register and in the page table; and in the
ROM, remove `code_carry_before` and `code_carry_after`, which only exist
because the bytecode moves.

**And the battle borrows half of `$7E`**, also since 2026-10-01: that is
where it decompresses the troop's battlers (`SCN_BATTLERS` in
`battle_scene.s`), because `back_from_battle` already decompressed the
whole grid again. Reverting the grid doesn't force them out: half of `$7E`
would be left free for them alone.
