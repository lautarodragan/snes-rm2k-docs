# ExHiROM, 8 MB

A whole RPG Maker game doesn't fit in 4 MB, so the cartridge is
**ExHiROM, 8 MB**. The code was first written for LoROM, and some of that
shape remains on purpose:

- **Data lives in 64 KB banks** that follow one another, so anything read
  across banks only adds one to the bank.
- **The code still sees banks 0 and 1 as in LoROM**: 32 KB from `$8000`,
  in `$00` and its fast mirror `$80`. In ExHiROM those two are different
  parts of the ROM, so the build places the code banks twice. It costs
  64 KB, and the runtime never had to know.
- **The third code bank is not LoROM's**: `FAR2` is the low half of `$C0`,
  fast and without a copy, because what lives there is only entered with a
  `jsl` to its address. Which code goes in which of the three is said by
  the header of `runtime/main.s` in the-advocate.
- **Only the first 4 MB are fast** (FastROM doesn't reach `$40`–`$7D`), so
  the packer fills those first.
- **There is ROM that is not used**: the low halves of `$70`–`$7D`, where
  Mesen2 and Mesen-S put the SRAM even if the cartridge has ROM there, and
  those of `$7E` and `$7F`, which are the WRAM.
- **Save data (SRAM) is at `$20:6000`**, 8 KB, and LoROM saves do not
  load.

All of that came out of a test ROM run on five emulators before moving the
game —ABL's `exhirom` experiment in the-advocate-ports—; the detail is in
the documentation of `banks.rs`, in `rm2k-snes/cartridge/src/` in
the-advocate. Why 8 MB: [The cartridge goes to 8 MB](../decisions/the-cartridge-goes-to-8-mb.md).

## Tables live in bank 0

`lda table, x` reads from the **data bank register**, not from the bank
the table was written in. That register is 0 almost everywhere, so a table
in another bank is read from the wrong place, silently. Everything the CPU
walks with an index therefore lives in bank 0, in a `TABLES` segment the
linker places there. The exception is the battle, which sets the register
to `$7E` and says so.

It is easy to half-fix: what keeps working with a table in the wrong bank
are the direct writes and the DMA clears, which carry the bank explicitly,
so the screen corruption can go away while the bug stays.

Bank 0 is 32 KB, so a table that grows with the game moves out and is read
with a long address (`lda f:table, x`). That costs one byte per instruction
and **forces the index to be X**: absolute long addressing indexed with Y
does not exist.

What does not fit in a bank cannot be walked with an index. The cell grid
of a large map is read with a 24-bit pointer; it lives decompressed in the
upper half of the two WRAM banks —see [The grid lives in WRAM](../optimizations/the-grid-in-wram.md)—,
which has the shape of a LoROM bank: going past `$FFFF` leads to the next
bank's `$8000`, not to its `$0000`. `ptr_more` and `ptr_minus` are the only
routines that know it.

A table that moved out, or one walked with `[ptr], y`, **is declared with
`.block`** so it does not end up split between two banks: see `block` in
`asm.rs` of `rm2k-snes/mapdata/`. The packing refuses to build with an
undeclared RODATA label, and what crosses on purpose —the music stream,
what is uploaded to the SPC700— carries `.crossbank`, and crosses only
between two banks that follow each other: see `resolve` in
`rm2k-snes/cartridge/src/banks.rs`.
