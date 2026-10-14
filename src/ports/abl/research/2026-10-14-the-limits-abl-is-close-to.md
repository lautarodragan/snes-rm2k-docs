# The limits ABL is close to

> **Measured on 2026-10-14**, by Cardón, with the tools at `0255f8f7`
> (the-advocate) and ABL at `a6823c8` (the-advocate-ports): the whole game
> in `release`, read from its `converter.log`, `mapdata.inc`, `memory.cfg`
> and `just space`. It is a snapshot: the numbers are from that day and
> this file is not updated; how to redo each one is at the end. The task is
> [`abl-the-limits-it-is-close-to`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-limits-it-is-close-to.md).

taro's question, after the items were cut at 255 to get the whole game in:
"let's measure what other limitations like that ABL has."

Nothing was changed or rebuilt. **Ratio** is value over limit; above 1.00 the
limit is already passed and something is being degraded or cut. A limit the
converter checks with an error is by construction not passed (the build
finished), so those rows only say how near they are. Rows that were not
measured are said so at the end.

## Summary

Four limits are **already passed**: the item index (264 of 255), the item
window's tile pairs (202 of 184), the background tiles of two maps (544 of
543) and the route slots of three maps (75 of 12 in the worst). Right at the
edge, with nothing left, are the direct page (3 B), the program's RAM
(20 B), far RAM (13 B), the composed-name tiles of the slot screen (48 of
48), the message pairs (158 of 158), the sprite tiles, slots and palettes of
the busiest maps, and CGRAM in 29 maps. The cartridge itself is at 95%
(121 of 127 data banks).

## The ranking

| # | Limit | ABL | Cap | Ratio | State |
|---|-------|-----|-----|-------|-------|
| 1 | Route slots: distinct events sent walking in one map | 75 (map 285), 18 (127), 13 (207) | 12 | 6.3 | **over** in 3 maps: a route that finds all slots moving is lost |
| 2 | Item text: tile pairs the item list asks for | 202 | 184 | 1.10 | **over**: `WARNING` in the log, the list asks for more than the windows leave |
| 3 | Event cache slots | 33 on screen at once (map 127) | 30 | 1.10 | **over** in 1 map |
| 4 | Items the tables name (one-byte index) | 264 | 255 | 1.04 | **over**: 9 left out (411, 413-416, 418-421), TEMPORARY hack |
| 5 | Background tiles of one map | 544 (maps 148 and 250) | 543 | 1.002 | **over**: 74 and 79 tiles fused into their nearest |
| 6 | Sprite slots in one map | 32 (map 127) | 32 | 1.00 | full; with the cache below, the ones drawn last wait |
| 7 | Sprite tiles in VRAM | 512 (maps 127 and 285) | 512 | 1.00 | full (145 has 508) |
| 8 | Sprite palettes | 8 (several maps) | 8 | 1.00 | full: 32 maps do not rain, 2 draw no battle animations, 3 skip pictures, the timer is lent a palette in 1 |
| 9 | CGRAM entries for the background | 99 in 29 maps | 99 | 1.00 | full; every one of the 29 merged colours (up to 108 in one map) |
| 10 | Composed names in the slot screen (tiles) | 48 | 48 | 1.00 | full (the menu's own: 100 of 124) |
| 11 | Message letter pairs | 158 | 158 | 1.00 | full by design: the most frequent ones are taken, more would compress better |
| 12 | Route graphics table | 8 (map 207) | 8 | 1.00 | full: one route's change of graphic is ignored |
| 13 | Program RAM (BSS) | 20 B free | 7,808 B | 0.997 | |
| 14 | Battle animation index | highest id 169 | 170 | 0.99 | the database has 180; ids from 170 are not addressable |
| 15 | Samples of one audio package (ARAM) | 62,703 B (map 127 + its song) | 63,419 B | 0.989 | 716 B left; 5 maps cannot hold their whole sound effects next to the song |
| 16 | Direct page | 253 B | 256 B | 0.988 | 3 B left |
| 17 | Far RAM | 13 B free | 832 B | 0.984 | |
| 18 | NPCs drawn in one map | 101 (map 214) | 104 | 0.97 | the rest are not drawn |
| 19 | Bank 0 | 1,324 B free | 32,704 B | 0.96 | |
| 20 | Data banks | 121 | 127 | 0.95 | 6 halves of 32 KB left; 18,169 B of gaps in the used ones |
| 21 | Events in one map | 114 (map 108) | 120 | 0.95 | |
| 22 | Bank 1 | 1,855 B free | 32,768 B | 0.94 | |
| 23 | Bank $C0 | 3,588 B free | 32,768 B | 0.89 | |
| 24 | Menu bank tiles | 400 | 448 | 0.89 | |
| 25 | Shop text tile pairs | 164 | 191 | 0.86 | |
| 26 | Parallel events in one map | 41 (maps 52, 54) | 48 | 0.85 | |
| 27 | Switches (highest named by a page condition) | 860 | 1,024 | 0.84 | commands not measured |
| 28 | Texts | 210,382 B | 262,144 B | 0.80 | 51,762 B left; 4,982 boxes |
| 29 | Variables | 175 | 256 | 0.68 | the database declares 250 |
| 30 | Skills screen tile pairs | 290 | 447 | 0.65 | |
| 31 | Troop pages in one troop | 33 | 64 | 0.52 | |
| 32 | 16x16 blocks of a map | 520 (map 312) | 1,024 | 0.51 | |
| 33 | Enemies in a troop | 4 | 8 | 0.5 | |
| 34 | Skill pairs of one actor | 54 | 255 | 0.21 | 251 in the game, of 2,048 |
| 35 | Shared common event bodies | 33 | 256 | 0.13 | |

Counts that are far from their cap and need no row: actors 61 of 255, states
31 of 256, troops 152 of a 32,768 cap, songs 106, sound effects 138, maps 313.

## The ones already degrading, by kind

From `converter.log`, counted by line:

* **Items past 255 left out**: 9, and a drop of one drops nothing.
* **Names cut to the window**: 17 skill names in battle, 9 item names, 7
  actor names, 6 leader names in the slot screen.
* **Background tiles fused**: 2 maps (148, 250).
* **CGRAM merges**: 29 maps at 99 of 99, colours merged in each.
* **Graphics drawn with another's palette**: 31 map lines, and 11 faces.
* **Poses quantized differently** (own pose bank): 54 map lines.
* **Panoramas**: 12 flattened, 3 hidden, 8 baked, 5 not flattened because
  more than 1,024 pixels would go to the wrong side of the hero.
* **No rain**: 32 maps. **Battle animations not drawn**: 2 maps. **Pictures
  not drawn**: 3 maps. **Timer lent a palette**: 1 map; 6 characters lose
  colours to make room for it.
* **Route slots over**: 3 maps. **Route graphic change ignored**: 1.
* **Event cache short of slots**: 1 map (127).
* **Sound effects that wait for the song**: 5 packages.
* **Commands the ROM does not do** (`ACCEPTED_UNDONE`): 2 lines.
* **Item text list over its pool**: 1.

## The fix, for the top ones

1. **Items**: carry the item index in 16 bits in the tables and the runtime
   (`items_and_battle` in `rm2k-snes/mapdata/src/emit.rs` and the item
   routines), or drop the unreferenced ones from the emitted set if the
   count of really named items is under 255.
2. **Item text pairs**: give the list more of the pool (the item and equipment
   windows share it), or cut the descriptions' pair set to what fits.
3. **Route slots**: grow `ROUTE_EV_MAX` (12) in the declaration; map 285
   alone asks for 75 and would still be cut, so a slot per event only where
   the routes overlap in time is what matches RM2k.
4. **Background tiles**: the layouts leave 543 of the 1,024 the plane can
   index; a layout with fewer panorama tiles on those two maps, or the
   fusing moved to the Adeleine decision where the loss is visible.
5. **Direct page, BSS, far RAM**: nothing to fix until someone needs a
   variable; the linker places new ones and refuses when they do not fit,
   so the first request that adds one is the one that has to pay: move
   what is rarely used (random state, speed keys) into far RAM or bank 1.
6. **Sprite slots, tiles and cache of map 127 and 285**: a pose bank
   shared between maps (already in `share_data`) with `SHARED_MAX` over 15,
   or the cache with more than 32 slots (`CACHE_MAX`, the runtime's and
   Wally's together).
7. **Sprite palettes**: eight is the console's; the answer is the
   priority between rain, the animation box, pictures and the timer, not a
   bigger limit.
8. **CGRAM in 29 maps**: 99 is what the layouts leave of 256; the fix is a
   layout with less for the sprites in those maps, or more palettes for
   the panorama (mode 1 instead of mode 3 for them).
9. **Message pairs**: 158 is `WAIT - PAIR_FIRST` in
   `rm2k-snes/events/src/messages.rs`; the escape range could be shortened.
10. **ARAM of map 127**: nothing, it fits, but that map's song and
    effects are 98.9% of a package.
11. **Banks**: 6 half banks are left; the next lever is the MSU-1 and the
    LZ2 on what is not yet compressed (see
    [Fitting the whole game in 8 MB](2026-10-14-fitting-the-whole-game-in-8-mb.md)).

## Not measured

The LZ2 stream caps (`LZ2_CAP_*`), pictures per map, sound-effect and map
indices, the switches named by commands rather than conditions, and the
battler and enemy counts against their caps. The build finished, so they
are under their caps; by how much was not looked at.

## How it was measured

* The caps: `grep` in the-advocate for `> 255`, `> 256`, `n't fit`, `_MAX`
  constants and `assert!` in `rm2k-snes/{mapdata,events,screens,battle,wally,cartridge}`,
  plus the `*_MAX` constants the header of `mapdata.inc` writes.
* The values: `build/release/converter.log` (per-map lines and warnings),
  table lengths counted from `mapdata.inc` by label, `memory.cfg` for the
  sizes of the RAM regions, and `just space` for the free bytes.
* The totals are properties of the console: 256 B of direct page, 7,808 B
  of program RAM and 832 B of far RAM in the link configuration, 32,704 B in
  bank 0.
