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
- **Only the first 4 MB are fast** (FastROM doesn't reach `$40`–`$7D`), so
  the packer fills those first.
- **Save data (SRAM) is at `$20:6000`**, 8 KB.

## Tables live in bank 0

`lda table, x` reads from the **data bank register**, not from the bank
the table was written in. That register is 0 almost everywhere, so a table
in another bank is read from the wrong place, silently. Everything the CPU
walks with an index therefore lives in bank 0, and a table that grows with
the game moves out and is read with a long address (`lda f:table, x`).
