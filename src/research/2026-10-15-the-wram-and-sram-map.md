# The WRAM and SRAM map, measured

> **Measured on 2026-10-15** by Hurón, with the tools of the-advocate at
> `6fa69781` and the ports at `f015801`, over the `release` cartridge of
> each of the eight games and ABL's eight test cartridges, built with those
> tools. It is a snapshot: the numbers are from that day and this file is
> not updated. How each number was obtained is at the end, in "How it was
> measured".

taro's question, on 2026-10-14, in the task
[`the-wram-and-sram-map-measured`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-wram-and-sram-map-measured.md):
the far RAM the linker hands out had 79 bytes left in ABL's release after
two tasks landed the same day —"are we going to reach an insurmountable
limit?"—. And on 2026-10-15, on top of it: whether switches used by a
single map could save RAM. They cannot matter —one bit per switch, 256
bytes for the whole table—, so the question became **what does weigh in
the console's 128 KB of WRAM and in the save, where each game is closest
to a wall, and what could be done about it**.

## Summary

* **The limit that was feared is not one.** The 79 bytes —12 today, in
  ABL— are what is left of `FARBSS`, an 832-byte stretch of bank `$7E`
  chosen by hand (`FAR_POOL_START` in `rm2k-snes/cartridge/src/banks.rs`
  in the-advocate). Around it, the map of `$7E2000`–`$7E7FFF` written by
  hand holds **3.2 KB (ABL) to 5.3 KB (Sunset) of slack inside fixed-size
  regions, plus 309 B of holes between them**, in every game: that is
  where `FARBSS` grows, as it already did twice.
* **The real walls are in bank 0, and they are the runtime's, not the
  game's**: the zero page has **3 B** left and the `BSS` **97 B**, the
  same in all eight games (`just space`). Only 55 of the zero page's 253
  bytes are used as `[dp],y` pointers, which is the one thing that has to
  live there.
* **One game hits a wall today**: Vampires Dawn names more RM2k variables
  than the 256 slots the port has —`FAR_VARIABLES` is 512 B, and the slot
  is one byte in the bytecode—. **145 variables have no slot and 224
  events are left out for it** (its `degradations.json`). Its switch table
  is at 206 of 256 B.
* **SRAM is 32 KB, not 8**, since 2026-10-04: a bank of the window per
  slot, four slots. ABL's save is **2,293 B of the 8,182 a slot holds**;
  the other games' 735–1,585 B. The save is nowhere near a wall, and
  **23.5 KB of the 32 are empty** in ABL, 26–29 KB in the others.
* **The upper halves of both banks —the grid, the load buffer and the
  battle scene— are far from full**: the heaviest map leaves 16.5 KB of
  the 32 behind its grid (Vampires Dawn's 195), and 18 maps across the eight
  games keep their bytecode in the cartridge because it would not fit
  there.
* **One latent bug**: nothing caps the number of LDB actors against the
  128 B of `FAR_HP` and `FAR_SP`. ABL has 61 actors —122 of 128 B—; a
  game with 65 would have its HP table run into its SP table in silence.

The suggestions, ranked, are at the end: let the linker place the far
RAM map; widen the variable slot; evict the zero page's non-pointer
variables; move the DMA-only buffers out of bank 0; and leave the save as
it is.

## The console's memory, and who has it

The 65816 sees 128 KB of WRAM as two banks, `$7E` and `$7F`, and the
first 8 KB of `$7E` again at `$0000`–`$1FFF` of every bank that has ROM:
that is "bank 0's RAM", the only RAM absolute addressing reaches with the
data bank at zero. The rest is "far RAM": reached with 24-bit addresses
(`lda f:`), through the `WMADD`/`WMDATA` window, or with the data bank
set to `$7E`, which is what the battle and the text layer do —in bank
`$7E`, `$0000`–`$1FFF` **is** bank 0's RAM, so code running there sees
both—.

How it is laid out today, from bottom to top:

| Range | Size | What | Placed by |
|---|---|---|---|
| `$7E0000`–`$7E00FF` | 256 B | `ZEROPAGE`: the direct page | the linker |
| `$7E0100`–`$7E1F7F` | 7,808 B | `BSS`: bank 0's RAM | the linker |
| `$7E1F80`–`$7E1FFF` | 128 B | the stack (`STACK` in `banks.rs`: a cap, not a measurement) | by hand |
| `$7E2000`–`$7E66BF` | 18,112 B | the far RAM map written by hand, part 1 | by hand |
| `$7E66C0`–`$7E69FF` | 832 B | `FARBSS`: the far RAM the linker hands out | the linker |
| `$7E6A00`–`$7E7CFF` | 4,864 B | the map written by hand, part 2 | by hand |
| `$7E7D00`–`$7E7DFF` | 256 B | `SWITCHES`: the switch table | the linker |
| `$7E7E00`–`$7E7FFF` | 512 B | the map written by hand, part 3 | by hand |
| `$7E8000`–`$7EFFFF` | 32 KB | the map's grid (`GRID`); a troop's battlers during a battle | by hand |
| `$7F0000`–`$7F5FFF` | 24 KB | the load buffer (`LZ2_BUFFER`); the battle's clean background; a screen's image; the bytecode carried across a teleport | by hand |
| `$7F6000`–`$7F7FFF` | 8 KB | the ChipSet animation's drawings; a big picture's palette and waves | by hand |
| `$7F8000`–`$7FFFFF` | 32 KB | the grid past 32 KB, then the block table, its passability and the map's bytecode; the composed battle scene | by hand |

Everything "by hand" is a `NAME = $7Exxxx` in `runtime/far_ram.s` of
the-advocate or in the file of its subsystem —`battle_scene.s`,
`audio_package.s`, `pano.s`, `painted.s`, `custom_menu.s`…—: 198
constants with the bank in front, 88 with sixteen bits read with the data
bank at `$7E`, and 238 derived from them (`BA_HP = FAR_BATTLE + 0`),
spread over eleven files. The three linker segments are the exception,
and they are new: `BSS` and `ZEROPAGE` always were, `FARBSS` since
2026-10-11 and `SWITCHES` since 2026-10-15 (the decision is
[RAM is placed by the linker](../decisions/ram-is-placed-by-the-linker.md)).

### What the linker places, and what it has left

`just space`, in each game's directory of the ports, prints these four
lines for every cartridge. They were the same in all eight games' `release`
except far RAM and the switch table, which depend on the game:

| Game | `ZEROPAGE` left | `BSS` left | far RAM (`FARBSS`) left | switch table left |
|---|---|---|---|---|
| A Blurred Line | 3 B | 97 B | **12 B** | 128 B |
| The Book of Three | 3 B | 97 B | 216 B | 128 B |
| Desert Nightmare | 3 B | 97 B | 274 B | 128 B |
| Dooms 2 | 3 B | 97 B | 252 B | 128 B |
| El Dorado | 3 B | 97 B | 312 B | 128 B |
| The Frozen World | 3 B | 97 B | 276 B | 121 B |
| Sunset over Imdahl | 3 B | 97 B | 279 B | 128 B |
| Vampires Dawn | 3 B | 97 B | **64 B** | **50 B** |

ABL's eight test cartridges have 204–276 B of far RAM left: `release` is
the tightest because it carries the whole game's 23 experience slots
(`EXP_K`), and the materials' table in `FARBSS` is twelve bytes per slot.

**Why the zero page and the `BSS` do not change with the game**: nothing
the converter sizes lives there. The `BSS` is 7,711 B of 7,808, and
7,596 of those are declared in `low_ram.s`; the only per-game tables in
bank 0 are sized by caps the runtime fixes —`EV_MAX` 120 events,
`NPC_MAX` 104 NPCs, `ROUTE_EV_MAX` 12 routes, `FLASH_MAX` 4 flashes,
`SUB_MAX` 16 substitutions— and not by the game.

What weighs in the `BSS`, by label (from the cartridge's `.dbg`, which
has every label's size):

| Bytes | Label | What | Scales with |
|---|---|---|---|
| 1,968 | `text_buf` | the message line being composed, two tile rows | — |
| 1,664 | `npc_buf` | the loaded map's NPC table, copied | `NPC_MAX` × 16 |
| 512 | `oam` (+32 `oam_high`) | the sprite table, sent by DMA each frame | — |
| 512 | `cgram_shadow` | the tinted palette, sent by DMA | — |
| 512 | `pal_buf` | the palette being tinted; the battle borrows a page of it as direct page | — |
| 480 | `ev_pos_buf` | where each event is, copied | `EV_MAX` × 4 |
| 384 | `route_ev` | the forced routes running | `ROUTE_EV_MAX` × 32 |
| 384 | `strip_col`/`_col2`/`_row`/`_row2` | the tilemap strips being built | — |
| 240 | `pick_by_ev` | the active page of each event with routes | `EV_MAX` × 2 |
| 120 | `ev_flags` | two bits per event | `EV_MAX` |
| 96 + 96 | `pure`, `table_r/g/b` | the tint tables | — |
| 64 | `pose_slot_masks` | — | — |
| ~700 | the rest | some two hundred small variables | — |

Adding one event to `EV_MAX` costs 7 B of `BSS` (`ev_flags`,
`ev_pos_buf`, `pick_by_ev`) and 9 B of far RAM (`FAR_PAIR_STATE`,
`CACHE_EV`): with 97 B left, `EV_MAX` cannot grow by more than 13 without
moving something.

And the zero page: 253 of 256 B used, 252 declared in `zero_page.s`. Of
those, **55 B in 18 labels are used in a mode that needs the direct
page** —`[ptr],y`, `(ptr),y`—: `code_ptr` (213 such uses), `msg_ptr`,
`page_ptr`, `comp_glyph`, `cells_ptr`, `music`, `route_ptr`,
`poses_ptr`, `npc_ptr`, `temp` and eight more three-byte pointers. The
other **198 B in 119 labels** are read with plain direct-page
addressing, which is one byte and one cycle cheaper than absolute, and
that is the only reason they are there: `hero_x`, `camera_x`, `pad`,
`map_width`, `tile_x`, the `comp_*` of the compositor, `party`… Some of
them are in the hottest loops of the frame and earn their place; many
—`title_sel`, `menu_open`, `slot`, `is_pal`, `jumps_left`, `cam_max_x`—
are touched once per frame or less.

### The far RAM map written by hand

The 24 KB of `$7E2000`–`$7E7FFF`, region by region, as they are in ABL's
release. "Used" is what the game fills, with its constants substituted
(`VARIABLES_N` 176, `ITEMS_N` 451, `ACTORS_N` 61, `EXP_K` 23,
`SKILL_BYTES` 32, `SAMPLES_N` 192, `EV_MAX` 120); "cap" is what the
region was given. **S** travels in the save. "Lives" says how long the
content means anything: *game* is state, *map* is rebuilt on every map
load, *battle*/*screen*/*page*/*window* while one is open, *frame* less
than a frame.

| Address | Used / cap | | Lives | Region | Owner |
|---|---|---|---|---|---|
| `$2000` | 960 / 1,024 | | map | `FAR_PAIR_STATE`: the parallel interpreters, 8 B per event | interpreter |
| `$2400` | 384 / 384 | | map | `FAR_PAIR_LIST`: the parallel pages, 8 B each | interpreter |
| `$2580`–`$25FF` | 101 / 128 | | mixed | pictures' tones, shared slots, `InputNumber`, BGM levels, the big picture, the speed keys, the window's place, `MessageOptions`, access, hero speed, random seed | nine files |
| `$2600` | 352 / 512 | S | game | `FAR_VARIABLES`: the RM2k variables, a word each | `variables.s` |
| `$2800` | 451 / 512 | S | game | `FAR_ITEMS`: the inventory, a byte per item | `items.s` |
| `$2A00` | 510 / 512 | | screen | `FAR_ITEM_LIST`: the items screen's list; the battle's too | `items.s` |
| `$2C00` | 610 / 752 | S | game | `FAR_EQUIPMENT`: five words per actor | equipment |
| `$2EF0` | 16 / 16 | | map | `FAR_WEATHER` | `rain.s` |
| `$2F00` | 225 / 416 | | map | `FAR_RAIN`: 3 B per drop, 75 drops | `rain.s` |
| `$30A0`–`$30FF` | 88 / 96 | | mixed | the two sound-effect voices' state, the turn slot, the audio package's, the MSU-1's, the picture slots, the message's pauses | six files |
| `$3100` | 384 / 512 | | game | `FAR_ARAM_OF`: where each sample is in ARAM | `audio_package.s` |
| `$3300` | 192 / 256 | | game | `FAR_WANTS` | `audio_package.s` |
| `$3400`–`$35FF` | 512 / 512 | | game | `INT_INIT`, `INT_END`: the ARAM allocation | `audio_package.s` |
| `$3600`–`$3623` | 29 / 36 | | map | the battle animation's state, the message arrow | two files |
| `$3640` | 89 / 192 | | screen | `CM_RAM`: the custom menus | `custom_menu.s` |
| `$3700` | 122 / 128 | S | game | `FAR_HP`: a word per LDB actor | battle |
| `$3780` | 122 / 128 | S | game | `FAR_SP` | battle |
| `$3800` | 61 / 256 | S | game | `FAR_ACTOR_GFX`: a byte per actor | `far_ram.s` |
| `$3900` | 9 / 256 | | map | `FAR_ENCOUNTER` | `encounters.s` |
| `$3A00` | 713 / 768 | | battle | `FAR_BATTLE`: the fight's state, the combatants at 40 B each | `battle*.s` |
| `$3D00` | 24 / 32 | | game | the second sound-effect voice | `sound_effects.s` |
| `$3D20` | 8,778 / 8,928 | | screen | `FAR_TEXT_LAYER`: the screens' text layer, its tilemap and its per-cell bookkeeping | `text_layer.s` |
| `$6000` | 32 / 256 | S | game | `FAR_SKILL`: a bit per (actor, skill) | `far_ram.s` |
| `$6120` | 205 / 224 | | page | a variable's digits; the level-up page | two files |
| `$6200` | 92 / 504 | S | game | `FAR_EXP`: experience and level, 4 B per slot; `EXP_TEXT` | `level.s` |
| `$6400` | 80 / 512 | | battle | `FAR_PAGE`: the troop pages | `battle_troop.s` |
| `$6600` | 176 / 192 | | battle | `SCN_*`: the scene's state and the borrowed direct page's copy | `battle_scene.s` |
| `$66C0` | 820 / 832 | s | mixed | **`FARBSS`**, see below | 13 files |
| `$6A00` | 386 / 386 | | frame | `FAR_STRIP_*`: the second set of tilemap strips; `FAR_VRAM_MAP` | `map_window.s` |
| `$6C00` | 1,024 / 1,024 | | game | `FAR_MUSIC`: the decoder's shadow and state, and **512 B of log the tests read** | `music.s` |
| `$7000` | 2,048 / 2,048 | | frame | `ANIMB_BUF`: the battle animation's frame; `TL_STAGE` while a screen is up | two files |
| `$7800`–`$7AFF` | 403 / 672 | | mixed | twenty small reservations of 16 or 32 B each, allotted to agents working at the same time, and `ChangeExp`'s 176: the victory, the drops, the transitions, the painted maps, the Game Over… | fifteen files |
| `$7B00` | 226 / 256 | | battle | `BA_MBUF`: the battle's message being composed | battle |
| `$7C00` | 200 / 256 | | map | `CACHE_*`: the cache of pose slots | `cache_slots.s` |
| `$7D00` | 128 / 256 | S | game | **`SWITCHES`** | `switches.s` |
| `$7E00` | 231 / 240 | 9 B | map | `PANO_*`: the panorama, with its ring's strips | `pano.s` |
| `$7EF0` | 258 / 272 | | teleport | `CARRY_MAP`, `ROUTE_CARRY`: what goes on after a teleport | `decompress.s` |

The totals, per game (same method; the regions sized by the game are the
variables, the inventory, the equipment, the HP, SP, graphics, skills and
experience of the actors, the samples, and the two linker segments):

| Game | Used in regions | Slack inside regions | Holes between regions |
|---|---|---|---|
| A Blurred Line | 21,049 B | 3,218 B | 309 B |
| The Book of Three | 19,533 B | 4,734 B | 309 B |
| Desert Nightmare | 19,310 B | 4,957 B | 309 B |
| Dooms 2 | 19,703 B | 4,564 B | 309 B |
| El Dorado | 19,157 B | 5,110 B | 309 B |
| The Frozen World | 20,127 B | 4,140 B | 309 B |
| Sunset over Imdahl | 18,974 B | 5,293 B | 309 B |
| Vampires Dawn | 20,547 B | 3,720 B | 309 B |

The holes are the same ten in every game, because they are between
regions chosen by hand: `$25A0` (16 B), `$25C0` (6), `$25F2` (4), `$25FA`
(1), `$3624` (28), `$6100` (32), `$6B82` (126), `$7830` (16), `$7870`
(64), `$7A00` (16). The slack is mostly in regions whose cap was chosen
for "any game" and that this game does not fill: `FAR_EXP` (412 B
unused in ABL), `FAR_ENCOUNTER` (247), `FAR_SKILL` (224), `FAR_ACTOR_GFX`
(195), `FAR_RAIN` (191), `FAR_VARIABLES` (160), `FAR_EQUIPMENT` (142),
`FAR_ARAM_OF` (128), `CM_RAM` (103)… none of them big, all of them
added up.

**`FARBSS`, the 832 B the linker hands out**, holds today, in ABL (from
the `.dbg`; the first two are sized by the game):

| Bytes | Label | File |
|---|---|---|
| 276 | `FAR_GROWTH`: what the materials added, 12 B per experience slot | `medicine.s` |
| 194 | `ba_bg_src` and the tone's flags: the battle background's 96 colours | `battle_tone.s` |
| 128 | `FAR_FLASH_PAL`: the four flash palettes | `character_flash.s` |
| 120 | `ba_states`: the combatants' conditions, 8 B each | `battle_states.s` |
| 53 | the pure parallel common events (`compar_*`), 6 B each | `common_events.s` |
| 21 | a medicine's scratch | `far_ram.s` |
| 28 | the message waits, the walkers, the skills screen and six more bytes | seven files |

In Vampires Dawn `compar_*` is 155 B (23 pure parallel common events)
and `FAR_GROWTH` 96; that is how it has 64 B left with eight experience
slots where ABL has 12 with twenty-three.

### What is shared in time, and what is idle when

The map above is of *addresses*; in time, several of them are two things:

* **`$7F`, all of it**, belongs to whoever is loading: a map load
  decompresses each tile block into `LZ2_BUFFER` and uploads it; the
  ChipSet animation's drawings stay at `$7F6000` as long as the map does;
  the bytecode carried across a teleport sits at `$7F1100`–`$7F5EFF`
  while the map changes under it. **A battle takes the whole bank**: the
  clean background at `$7F0000`, the composed scene at `$7F8000`, and the
  troop's battlers in the grid's half of `$7E`; `back_from_battle`
  decompresses the grid and the drawings again. A big picture puts its
  palette and waves over the drawings. The title and Game Over screens
  decompress their image over all of it, grid included: from there one
  goes to the boot or to `enter_map`, never back.
* **`ANIMB_BUF`** (2 KB) is the battle animation's frame on the map and
  the text layer's stage (`TL_STAGE`) while a screen is up.
* **`FAR_ITEM_LIST`** is the items screen's list and the battle's.
* **A page of `pal_buf`** (bank 0) is the battle scene's borrowed direct
  page, saved and restored around it.

And what is idle: **the text layer's 8.9 KB is dead while the map is
played** —it is filled from scratch when a screen opens—, and it is the
single largest region of the hand-written map; the battle's 1.3 KB
(`FAR_BATTLE`, `FAR_PAGE`, `SCN_*`, `BA_MBUF`, the small battle
reservations) is dead outside a fight; `FAR_MUSIC`'s 512 B log is written
only when a test turns it on; `FAR_RAIN` only on maps with rain,
`PANO_*` on maps with a panorama, `CACHE_*` on maps with a cache,
`CM_RAM` with a custom menu open. None of them can host *state*
—variables, switches, the party— because state has to outlive all of
them; they could host each other's scratch, and the stage already does.

### The upper halves: the grid and what lives behind it

Every map's grid is decompressed to `$7E8000`, continuing at `$7F8000`
past 32 KB, and behind it in `$7F` go the block table, its passability
and the map's bytecode (`lz2_grid` in `runtime/decompress.s`;
[the decision](../optimizations/lossless/the-map/the-grid-in-wram.md)).
A map whose bytecode does not fit there —or is over the 19,968 B of
`LZ2_CAP_CODE`, which is what the teleport carry can hold— keeps it in
the cartridge instead, and nothing else changes. From each game's
`mapdata.inc`:

| Game | Maps | Grids past 32 KB | Largest grid | Most taken of `$7F`'s upper half | Bytecode kept in the cartridge |
|---|---|---|---|---|---|
| A Blurred Line | 280 | 3 (the three Lashe City escapes, 500×40 = 40,000 B) | 40,000 B | 12,153 B (map 4) | 0 maps |
| The Book of Three | 70 | 0 | 10,500 B | 6,613 B | 2 |
| Desert Nightmare | 189 | 0 | 3,608 B | 5,377 B | 1 |
| Dooms 2 | 90 | 0 | 4,000 B | 1,436 B | 2 |
| El Dorado | 13 | 0 | 600 B | 6,128 B | 0 |
| The Frozen World | 150 | 0 | 7,000 B | 11,950 B | 4 |
| Sunset over Imdahl | 65 | 0 | 2,400 B | 3,153 B | 1 |
| Vampires Dawn | 430 | 0 | 24,000 B | 15,809 B (map 195) | 8 |

Nothing is near the 32 KB. The wall there is a single map's grid over
32,768 B per half —a 200×200 map does not fit the cell stream, see the
draft
[`a-200x200-map-does-not-fit-the-cell-stream`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-200x200-map-does-not-fit-the-cell-stream.md)—,
which is a format question and not a RAM one: no ABL map gets near it.

## SRAM: the save

Since 2026-10-04 the cartridge declares 32 KB of SRAM and **each of the
four slots is a whole 8 KB bank of the window** (`SRAM_STRIDE` in
`runtime/save_game.s`): slot N is `$6000`–`$7FFF` of bank `$20 + N`. The
slot holds a 10-byte header —signature, checksum, length, format— and the
save, which is what `save_table` in `bank1.s` lists, in order. Its size
is `SAVE_BYTES`, which the converter's constants fix per game (from each
cartridge's `.dbg`):

| Game | `SAVE_BYTES` | Of 8,182 | Left per slot | Empty in the 32 KB |
|---|---|---|---|---|
| A Blurred Line | 2,293 B | 28% | 5,889 B | 23,556 B |
| The Book of Three | 1,051 B | 13% | 7,131 B | 28,524 B |
| Desert Nightmare | 1,082 B | 13% | 7,100 B | 28,400 B |
| Dooms 2 | 917 B | 11% | 7,265 B | 29,060 B |
| El Dorado | 802 B | 10% | 7,380 B | 29,520 B |
| The Frozen World | 1,360 B | 17% | 6,822 B | 27,288 B |
| Sunset over Imdahl | 735 B | 9% | 7,447 B | 29,788 B |
| Vampires Dawn | 1,585 B | 19% | 6,597 B | 26,388 B |

What ABL's 2,293 B are, line by line of `save_table`:

| Bytes | What | Sized by |
|---|---|---|
| 610 | the equipment: five words per LDB actor | `ACTORS_N` × 10 |
| 451 | the inventory: a byte per LDB item | `ITEMS_N` |
| 352 | the variables | `VARIABLES_N` × 2 |
| 276 | what the materials added: six words per experience slot | `EXP_K` × 12 |
| 128 | the switches | `SWITCH_BYTES` |
| 122 + 122 | the HP and the SP, a word per actor | `ACTORS_N` × 2, twice |
| 92 | the experience and level, 4 B per slot | `EXP_K` × 4 |
| 61 | which graphic each actor's sprite was changed to | `ACTORS_N` |
| 32 | which skills each actor knows | `SKILL_BYTES` |
| 47 | the hero's place, direction, cell and map; the party; the tint; the timer; the gold; the song; the locks; the speed; the permissions; the message options; the panorama | fixed |

Three quarters of ABL's save are the actor tables, because ABL has 61
LDB actors —the leaders that swap and their copies—; Vampires Dawn's
1,585 B are 512 of variables and 206 of switches. **Nothing here is
near a wall**: the slot that was tight on 2026-10-04 was a 2 KB one, and
the move to a bank per slot made each one more than three times the
biggest save there is. The price is that **72% of the 32 KB is empty in ABL and 81–91%
in the other games**, and that the cartridge asks a flash cart for 32 KB
of SRAM instead of 8. Both are cheap: any cartridge or flash cart has 32
KB, and the slots are four because taro wanted four, not because the
SRAM is full.

What RM2k saves and the port does not, for the record: the memorized
BGM, the screen transitions, the pictures, the encounter count and the
battle —each with its why in `far_ram.s`—. None of them weighs more than
a few bytes; the save format is not where the port loses fidelity.

## Pressure: where each game is closest to a wall

Each number, with the command or file that printed it:

| Wall | Where it is today | Who is closest | Printed by |
|---|---|---|---|
| **Zero page**, 256 B | 3 B left, every game | the runtime | `just space` |
| **`BSS`**, 7,808 B | 97 B left, every game | the runtime | `just space` |
| **`FARBSS`**, 832 B | 12 B left | A Blurred Line (`EXP_K` 23) | `just space` |
| **Variable slots**, 256 (a byte in the bytecode; 512 B of `FAR_VARIABLES`) | **over**: 145 variables without a slot, 224 events left out | Vampires Dawn | its `degradations.json` |
| **Switch table**, 2,048 switches (256 B) | 206 B used: its highest switch falls in the 206th byte | Vampires Dawn | `just space` |
| **LDB actors**, 64 (`FAR_HP` and `FAR_SP` are 128 B apart; nothing asserts it) | 61 actors, 122 of 128 B | A Blurred Line | the `.dbg` (`ACTORS_N`) |
| **Samples**, 256 (`FAR_ARAM_OF` is 512 B) | 219 | Vampires Dawn (`SAMPLES_N`) | the `.dbg` |
| **Experience slots**, 126 (`FAR_EXP` to `EXP_TEXT`) | 23 | A Blurred Line (`EXP_K`) | the `.dbg` |
| **Skill bits**, 2,048 (`FAR_SKILL` 256 B) | 32 B used | A Blurred Line | the `.dbg` |
| **Text layer**, 8,928 B | 8,778 B used, 150 left; it does not depend on the game | the runtime | the `.dbg` (`TL_END`) |
| **Behind the grid**, 32 KB of `$7F` | 15,809 B | Vampires Dawn, map 195 | `mapdata.inc` |
| **A grid's half**, 32,768 B | 40,000 B grids in ABL use both halves; none past 64 KB in the eight | A Blurred Line | `mapdata.inc` |
| **The save**, 8,182 B per slot | 2,293 B | A Blurred Line | the `.dbg` (`SAVE_BYTES`) |
| **Bank 0 ROM** (for reference) | 740–908 B left | ABL's `test-change-system` | `just space` |

Two of these are already past the line or one game away from it: the
variables, which Vampires Dawn is over, and the actors, which ABL is three
short of with nothing to stop the fourth. The three bank 0 ones are the
ones every new feature bumps into: the comments of `low_ram.s` and
`zero_page.s` say "it does not fit there", "the direct page is full" or
"there were three bytes left" more than a dozen times.

## Suggestions, ranked

Each with what it would save —measured where it could be—, what it costs,
what could go wrong, and what it would open. None of them was
implemented; the ones worth doing have a draft in the tasks repo.

### 1. Let the linker place the far RAM map

**What**: move the 24 KB of `$7E2000`–`$7E7FFF` into segments the linker
places, sized by the game's constants, in the order and groups the code
needs; keep only the grid, `$7F` and the stack by hand. It is the plan
the [decision](../decisions/ram-is-placed-by-the-linker.md) already
states as the way `FARBSS` grows, done once for everything instead of
stretch by stretch.

**Saving, measured**: the slack and the holes become one pool: **3,527 B
in ABL, 4,029 B in Vampires Dawn, up to 5,602 B in Sunset**, on top of
the 12–312 B `FARBSS` has today. And `just space` would print what is
left in total, which is what taro asked.

**Cost**: 198 24-bit constants, 88 sixteen-bit ones and 238 derived from
them, in eleven files; 493 `.loword` uses that stay as they are if the
labels keep their banks; 41 uses of the `WMADD` window that walk a
contiguous block —`clear_variables` wipes from `FAR_MSG_OPTIONS` to the
end of the inventory in one pass; `save_table` copies each line as a
block—, which have to stay contiguous: one segment per block, in order,
or a single `.res` with the fields as offsets. The battle's and the
scene's sixteen-bit names become `.loword()` of labels, as `FAR_GROWTH`
did. The ROM changes everywhere and the behaviour nowhere: the goldens
do not move, and the suite plus `test_wram_reservations.py` —which has
to learn the new segments— are the net. A label used before its
declaration in `main.s`'s order is taken as sixteen bits and fails the
link, which is the mechanical part. Three to five days, best done
subsystem by subsystem with the ROM compared after each.

**Risk**: medium. The failure that is not mechanical is a block that
something walks as a range without the code saying so —the `.assert`s of
`far_ram.s` catch the ones that were written down—. `test_decompressed_load.py`
and the save tests cover the two big ones.

**Unlocks**: every game-sized table grows with its game instead of a cap
chosen for ABL: Vampires Dawn's variables (see 2), a game with more
actors, more experience slots, more switches; `FARBSS` stops being a pool
that two tasks can empty in one day.

### 2. Widen the variable slot

**What**: the RM2k variable is a slot in the bytecode, and the slot is a
byte (`variable_slot` returns a `u8` in the event compiler;
`var_read` masks with `VAR_SLOT`). Make it a word in the opcodes that
carry one —`ControlVars`, the conditions, `InputNumber`, the key input,
the picture by variable— and size `FAR_VARIABLES` by `VARIABLES_N` with
no cap below RM2k's 5,000.

**Saving**: none in RAM; it *costs* 2 B per variable past 256 in RAM and
in the save: Vampires Dawn would need 802 B instead of 512, which fits in
the slack of suggestion 1 and in any slot of the SRAM.

**Cost**: a bytecode change —every opcode with a variable operand grows a
byte, the compiler and the interpreter on both sides, the test cases that
spell bytecode by hand— plus the two save tests. Two days.

**Risk**: low-medium: it is the kind of change the goldens and the
events' test cases see at once, and the opcode declaration does not
compile with a mismatch.

**Unlocks**: **224 events of Vampires Dawn**, today left out for a
variable without a slot; and the next game with more than 256 variables,
which in RM2k is not rare.

### 3. Evict the zero page's non-pointer variables

**What**: of the 253 B, 55 are pointers used with `[dp],y` and have to
stay; 198 are there for the one byte and one cycle direct-page
addressing saves. Move the ones no hot loop reads —`title_*`, `menu_open`,
`slot`, `is_pal`, `pal_tick`, `token`, `panic`, `jumps_left`, the `jump_*`
and `entry_*` of a teleport, `cam_max_*`, `map_ofs`, `npc_total`,
`restart`…— to the `BSS`, keeping the compositor's, the camera's, the
strips' and the hero's.

**Saving**: 60–100 B of zero page, by inspection of the list; the exact
number is the sum of what gets moved. Each costs one byte of ROM and one
cycle per access, in bank 0's ROM, which has 740–908 B left.

**Cost**: a day; mechanical, the ROM compared before and after for the
unchanged routines, the suite for the changed ones. It needs
`BSS` room first, which is suggestion 4.

**Risk**: low. The one trap is a variable read with `ldx`/`ldy` in
sixteen bits where a one-byte neighbour follows: moving it changes the
neighbour, and the comments warn about it twice.

**Unlocks**: new code that needs a pointer. Today a new `[dp],y` pointer
cannot be added at all: the hero's forced route already lives in the
`BSS` and is copied into `route_ptr` to be read, for want of one
(`hero_route` in `low_ram.s`).

### 4. Move the DMA-only buffers out of bank 0

**What**: `oam` and `oam_high` (544 B), `cgram_shadow` (512 B) and
`text_buf` (1,968 B) are built in bank 0 and leave it by DMA, which reads
any bank. Move them to far RAM with `f:` addressing where they are
written: 11, 1, 4 and 8 indexed uses respectively (`grep` on the runtime),
and the `#^` bank bytes of their DMAs, which already exist.

**Saving**: up to **3,024 B of `BSS`**, against 97 today. `pal_buf` stays:
the battle scene borrows a page of it as direct page, which has to be in
bank 0. `npc_buf` (1,664 B) stays too: `build_oam` walks it 118 times
with indexed absolute addressing in the per-object loop, and long
addressing there is a cycle per field per object per frame.

**Cost**: a day. Each `sta oam, x` becomes `sta f:oam, x`: one byte of ROM
and one cycle each —a few hundred cycles per frame for the OAM, built
object by object; less for the palette; and the compositor's eight
writes, per letter row—.

**Risk**: low-medium: a DMA whose `A1B` is left at zero reads bank 0's
copy of nothing and the screen shows it at once; `test_cores.py` and the
goldens see it.

**Unlocks**: `EV_MAX` past 120 (7 B each), `NPC_MAX` past 104 (16 B each),
`ROUTE_EV_MAX`, and suggestion 3.

### 5. Leave the save as it is

**What**: nothing. The alternatives were measured and found not worth it:
two slots per bank (a 4 KB stride, eight slots in the same 32 KB) costs
a multiply in `slot_bank` and a slots screen that lists eight; going back
to 8 KB of SRAM with four 2 KB slots does not hold ABL's 2,293 B. The 23.5
KB that are empty cost nobody anything, and RM2k's fifteen slots were
never wanted.

**If something is done**: the one thing worth a line is the latent bug
above —`ACTORS_N` against the 128 B of `FAR_HP` and `FAR_SP` and the 752 of
`FAR_EQUIPMENT`—, which belongs to the runtime as an `.assert` or to
suggestion 1, where the tables are sized by the game and cannot overlap.

### What was not worth suggesting

* **The switch table**: 2,048 switches, Vampires Dawn at 1,648. Suggestion
  1 sizes it by the game; alone it is 256 B and not a wall.
* **Map-only switches** —taro's original question—: one bit each, so a
  map that owns twenty switches owns 2.5 B. Nothing to gain.
* **The music log**: 512 B of far RAM written only under test. It could
  share a dead region, but every candidate is alive during some test
  that reads the log, and 512 B is not what anyone is short of.
* **The text layer's 8.9 KB idle on the map**: nothing that lives on the
  map and dies when a screen opens is big enough to be worth putting
  there; the stage already shares `ANIMB_BUF`.

## How it was measured

Everything comes from the built cartridges and the runtime's sources;
nothing was changed, built by hand or relinked.

* **The segments and their areas**: `just space` in each game's directory
  of the ports; for ABL's test cartridges, `rm2k-snes-space` with the
  path of each `test.sfc`. The same numbers, as JSON, with `--json`.
* **Who owns each byte of `ZEROPAGE`, `BSS`, `FARBSS` and `SWITCHES`**:
  the `.dbg` `ld65` leaves next to each ROM has a `sym` record per label
  with its `size`, its segment and the line it was defined on, which
  names the file. The per-game constants (`VARIABLES_N`, `ACTORS_N`,
  `EXP_K`, `SAVE_BYTES`, `TL_END`…) are `equ` records of the same file.
* **The hand-written map**: every `NAME = $7Exxxx` and every sixteen-bit
  far constant of `runtime/*.s`, with each region's size from its
  comments and `.assert`s, and the game's constants substituted; the
  regions were then checked against the `.dbg`: every 24-bit equate in
  `$7E2000`–`$7E7FFF` of the eight cartridges falls inside a listed
  region. The slack is each region's cap minus what the game fills; the
  holes are what no region covers.
* **The zero page's pointers**: the `ZEROPAGE` labels of the `.dbg`
  searched in the runtime's sources for `[label]`, `[label],y`,
  `(label),y` and `(label,x)`.
* **The buffers' addressing**: `grep` over the runtime for each label
  followed by `,x` or `,y`, by `f:`, and by `#<`/`#^`.
* **The grid and what lives behind it**: each cartridge's `mapdata.inc`:
  `MAP_BW` × `MAP_BH` × 2 per map, the `block_pass` pointer's offset from
  `GRID_HIGH`, and the `map_code` table's length per map, 0 for a map
  whose bytecode stays in the cartridge.
* **The save**: `SAVE_BYTES` from the `.dbg`, and its lines from
  `save_table` in `runtime/bank1.s` with the constants substituted; the
  sum was checked against the constant for every cartridge.
* **Vampires Dawn's variables**: its `degradations.json`, the entries
  whose text ends in "which has no slot in far RAM": 224 entries, 145
  distinct variables.
* **The counts of hand constants**: `grep` over `runtime/*.s` for
  `= $7E…`/`= $7F…`, for `= $2000`–`$7FFF` outside the files that use
  those ranges for VRAM, SRAM or registers, and for `= NAME + n` in the
  files that lay out a region.

The scripts that did the parsing were throwaway, as the working rules
want, and are not kept: each step above is a few lines over the `.dbg`
and the `.inc`, and the inputs are what the build leaves next to every
ROM.
