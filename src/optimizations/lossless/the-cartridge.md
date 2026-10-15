# Lossless: the cartridge

## Identical blocks are stored once

Every data block the converter emits —tiles, grids, block tables,
bytecode, and the rest— has an identity of its own, `<class>_<n>`, and
the map stores which one it points to: two maps with the same bytes in a
class share the block.

- **Saves**: ROM, wherever maps repeat data.
- **Where**: `Materials::store` in `rm2k-snes/mapdata/src/materials.rs`.
- **More**: [Graphics and sound, from RM2k to the SNES](../../research/graphics-and-sound-from-rm2k-to-the-snes.md).

## Tables of pointers, stored once by their text

A table whose bytes are pointers the linker sets cannot be compared by
its bytes, so it is shared by its text, which names the same labels when
it points to the same things. The per-map leader table and the per-map
table of the poses of each character that changes pose go this way: most
maps bring one another map already brought.

- **Saves**: ROM.
- **Where**: `Materials::store_text` and `Materials::store_symbolic` in
  `rm2k-snes/mapdata/src/materials.rs`; `actor_table_asm` and
  `npc_poses_asm` in `record.rs`.
- **More**: [Fitting the whole game in 8 MB](../../ports/abl/research/2026-10-14-fitting-the-whole-game-in-8-mb.md),
  the research that measured them.

## The fast half first

Only the first 4 MB of an ExHiROM cartridge are FastROM, so the packer
fills those first.

- **Saves**: CPU on reads from ROM.
- **Where**: `banks.rs` in `rm2k-snes/cartridge/src/`.
- **More**: [ExHiROM, 8 MB](../../internals/exhirom.md).

## What does not fit, in the `.msu`

A game whose ROM does not reach declares `[rom] msu = "required"`, and the
data read when a map or a battle loads —LZ2 streams, panorama and picture
tiles, samples— travels in the `.msu`. Nothing is lost, but the game needs
the MSU-1.

- **Saves**: ROM.
- **Where**: the `.msu` in front of a `.block`, marked by each emitter;
  `lz2_msu` and `msu_dma0` in `runtime/decompress.s`.
- **More**: [The `.msu` file](../../internals/the-msu-file.md#what-does-not-fit-in-the-rom),
  [The MSU-1 is required only when the ROM does not reach](../../decisions/the-msu-1-is-required-only-when-the-rom-does-not-reach.md).
