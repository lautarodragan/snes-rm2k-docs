# Frozen World's battle system

> **Measured on 2026-10-15** by Carpintero, with the tools of the-advocate
> at `497be031` and the ports at `0ddf815`. The Frozen World's own data,
> as Ditto dumps it into the port. It is a snapshot: the numbers are from
> that day and this file is not updated. The prototypes it mentions were
> built to measure and were not merged. How each number was obtained is at
> the end.

taro's question, on 2026-10-15, in the task
[`frozen-world-the-custom-battle-system`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/frozen-world-the-custom-battle-system.md):
The Frozen World fights with events, on maps 1 and 2, and both are left
out of the cartridge. Which limits does that combat hit —the runtime's, the
tools', the console's— and which patterns in its events allow "creative"
ways out: rethinking the events while they stay RM2k, as with
[map 11 of A Blurred Line](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/map-11-redesigned.md);
optimising them the way a C++ or Rust compiler would; an intermediate
representation that also covers the 32-bit arithmetic of
[the HP percentages](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/frozen-world-hp-percentages-past-327-hp.md);
and, as a last resort taro would rather avoid, streaming the commands from
the ROM or the MSU-1.

What was known before is on the progress page
[The Book of Three and The Frozen World](../progress/book-of-three-and-frozen-world.md).


## Summary

* **It is a menu, not an action game.** The combat is four maps the hero
  walks on as a cursor: map 1, the battle screen; map 3, the command grid;
  map 14, the item menu; map 2, the plate placement outside battle. Almost
  every page is an **action page called as a subroutine** (`CallEvent` to
  another event of the same map). Per frame it does very little: two
  parallel pages on map 1 and one on map 2. The weight is not CPU, it is
  **code size**. The one CPU risk is that one of those parallel pages
  writes variables the HP meters look at, every frame, and each write asks
  for a refresh of all of map 1's pages: on A Blurred Line's map 8 that did
  not fit in a frame.
* **What keeps map 1 out is that the compiler pastes every call.** A
  `CallEvent` to a map event is compiled by pasting the called page in
  place, four levels deep, and map 1's pages call the same pages dozens of
  times: **map 1 is 3,993,422 bytes of bytecode**, monster pages of 63 KB
  each. `CombatController`'s round page "stops at the page as a whole"
  because pasted it goes past **64 KB, the reach of a jump**: every branch's
  destination is an absolute 16-bit offset in the page.
* **With calls compiled as calls, map 1 is 90,339 bytes** (44 times less),
  **69,227 with identical pages stored once**, and the round page compiles
  at 5,177 bytes. Measured with a prototype of the compiler. The whole game
  goes from 4.17 MB to 243 KB of bytecode; A Blurred Line, from 161 to
  154 KB (its map 11, from 10.5 to 3.4 KB).
* **Even then it does not fit in WRAM**, which holds 19,968 bytes of a
  map's code; map 2 needs 38,185. **The cartridge has room**: 54 free banks
  of 64 KB in Frozen World's. Keeping the code of the maps that do not fit
  in the cartridge, uncompressed, costs about 110 KB of ROM, and the runtime
  already runs bytecode from the cartridge (the shared common events, the
  troops). **The MSU-1 is not needed.**
* **Behind those two there are five small ones**: switches up to 1,077
  (the table holds 1,024), `ChangeActorFace`, a false refusal of the
  converter (a flash that runs after a teleport to map 3 is checked as if
  it ran on map 1), chains of calls six deep (the compiler drops calls
  past four, the runtime's stack has three levels), and the HP percentages
  that saturate at sixteen bits —which on the battle screen are the HP
  meters—.
* **What a C++ compiler would do, measured on this game**: the payoff is in
  calls instead of pastes, identical pages once, the empty `else` (6,752
  of 7,773 on the maps, 3 bytes and one jump each), running a parallel page
  only when what it reads changes (about 100 of a frame's 262 lines on map
  1, every frame, estimated) and fusing multiply-then-divide (all three
  in the game are that). Constant folding, loop unrolling and inlining gain
  **nothing** here: one branch in the whole game looks at a switch nobody
  writes, map 1 has two loops, and inlining is exactly what blew it up.
* **The recommendation**: calls as calls and the code of the big maps in
  the cartridge, with the five small ones, gets the combat compiled; then
  the fidelity (the backdrops, the palettes, the plates' graphics); and the
  intermediate representation as the third step, because its first step
  —jumps by label— is also what lifts the 64 KB limit. See the end.


## What the battle system is

### Four maps, a cursor and switches

A monster on a map is an event that, touched, memorises the place, turns
on the battle's switches —which monster in each of the three places, which
battle— and teleports to **map 1**. From there the fight goes around:

* **Map 1, "Battle Screen"** (20×15, 48 events, 28,989 commands).
  `CombatController` (event 7) has three automatic pages:
  * **page 1**, with no condition: the battle's setup. A chain of `if switch
    → PlayBGM` for the music, a chain of 113 `if switch → call common event`
    that loads each battle's monster statistics (common events 14 to 70),
    the plate removers' pages, and a `Teleport` to map 3;
  * **page 6**, switch 172: **the monsters' round**. A long dispatch on
    variable 37 (the monster type: 24 cases), each with what that monster
    does —steal gold, unequip a slot's plates, heal, cast— computed with
    `ControlVars`, random numbers and messages, and calls to the attack
    pages; at the end, common event 7 and `GenericMonsterTurn`;
  * **page 7**, switch 175: the end of the round, the states that wear off.

  The three **monster events** (A, B, C) have one page per monster that
  can stand there (29, 15 and 8), each conditioned on two switches, all
  with **the same 195 commands**: which plate the hero used (switches 184,
  187, 189…) and a call to that hero's `CommandData` page. The hero, as a
  cursor, walks up to a monster and presses the action key on it (read in
  the data, not played). The
  `CommandDataHero` pages (three heroes, three pages each) compute the
  damage —`ControlVars` with additions, subtractions and random numbers—
  and call `MonsterData1`/`2` (1,007 and 1,357 commands) and the plate
  removers (513 commands, five pages per hero). The **HP meters** are three
  events with nine pages each, conditioned on variables 174 to 176 at 0, 30,
  40 … 100: the HP percentage.
* **Map 3, "Command Grid"**: each hero has five slots, one plate per slot
  (Attack, Steal, Study, Fire, Heal…: the plates are the commands). The
  cursor walks to a slot and presses the key; the slot's page turns the
  action's switch on and teleports back to map 1. It is already in the
  cartridge: it has no parallel page.
* **Map 14, "Use Menu"**: the items.
* **Map 2, "Plate Placement"** (40×15, 51 events, 12,225 commands), outside
  battle: fifteen slot events (three heroes, five slots) with **24 pages
  each, one per plate**, and the inventory of each plate type. Placing one
  asks "Do you want to place this plate here?", turns switches and teleports
  to another place of map 2 and goes on.

**What it keeps** is switches and variables: the battle's (which monster,
which battle, whose turn, which plate was chosen), the monsters' HP and
statistics in variables, the plates in each slot as switches. The game
names **1,051 distinct switches**, the highest 1,077, and 207 variables. It
has no `EnemyEncounter`, no picture and no loop to speak of (two
`BreakLoop` on map 1).

### What runs per frame

| where | what | operations per frame |
|---|---|---|
| map 1, `BackdropSetter` (parallel) | 113 `if switch → ChangePBG`: the battle's backdrop | ~116: 113 `OP_IF`, one `OP_PANORAMA`, a jump and the end |
| map 1, event 29 (parallel) | calls `CalculateHPPercents` (common 38): `v = HP; v *= 100; v /= max HP`, three times | ~11: three multiplications and three divisions among them |
| map 2, event 38 (parallel) | turns switch 186 on | 2 |
| map 3, map 14 | nothing | 0 |

There are no parallel common events; the only automatic one is the pause
menu (15). The rest runs **in bursts**: the setup page tests over a hundred
and fifty conditions before its first message, and a round runs tens to a
few hundred operations between two message boxes. A burst that goes past a
frame costs a frame in which the screen is still, which is not seen.

**The interpreter, by hand**: an `OP_IF` on a switch is about **180 CPU
cycles** —the dispatch in `run_code` (~30), `op_if` and `switch_on`— and,
with the bytecode read from WRAM, about **1,150 master cycles, 0.85 of a
scanline**. That is an estimate counted from the code, not measured; the
nearest measurement is that of
[`race-2-at-60-frames`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/race-2-at-60-frames.md),
**about 1.2 lines per operation** averaged over `OP_VAR` and `OP_IF_VAR`, before
the general improvements of that same work. With a still map's frame at
around 90 of its 262 lines (map 51 of A Blurred Line measured 94 with
thirteen small parallel pages), **some 150 to 200 simple operations fit in
a frame**.

So `BackdropSetter` alone would take **about 100 lines of every frame**,
four tenths of it, for the whole battle. And event 29 writes variables 174
to 176 every frame, which the meters' page conditions read: the compiler
marks those writes with `VAR_REFRESH`, and the runtime then refreshes every
page of the map, **every frame** (`var_write` raises `refresh` whether the
value changed or not). That cost was not measured on map 1, but it has a
precedent: on A Blurred Line's map 8, a refresh per frame over 68 events and
106 pages **did not fit in a frame**, and the port ran at 30 frames per
second there until the bit existed (the comment on `VAR_REFRESH` in the
compiler). Map 1 has 48 events and 165 pages.


## The limits, ranked

By what they block, first what keeps the combat from compiling at all.

| # | Limit | Whose | Measured | What it blocks |
|---|---|---|---|---|
| 1 | **`CallEvent` is pasted**, four levels deep | the compiler | map 1: 3,993,422 bytes; monster pages of 62,681 and 63,321; 74 pages with chains of four or more | map 1 cannot be carried in any memory; its round page and `MonsterData2` go past 64 KB |
| 2 | **A page's jumps are absolute 16-bit offsets** | the bytecode | `CombatController` page 6 pasted: over 64 KB; the culprit chase names 195 `EndBranch` and 194 `ElseBranch`, the commands that patch a destination | "stops at the page as a whole" |
| 3 | **A map's bytecode lives in WRAM**, behind the grid | the runtime | 19,968 bytes fit (`LZ2_CAP_CODE`, the size of `CODE_CARRY`); map 2: 38,185; map 1 with calls: 69,227 to 90,339 | map 2 today; map 1 after #1 |
| 4 | **Switches past 1,023** | the runtime's table and the compiler | 1,051 named, the highest 1,077; the table is 128 bytes | 17 branches in `CombatController` page 1, 16 in `BackdropSetter`, 11 in `MonsterData2`; common events 23, 24, 26, 27, 36, 37 (Steal and Study); two monster pages ask for switch 1,024 and 1,059 |
| 5 | **The converter's hero-flash check** does not know a page goes on on another map | the converter | `Hero1ChoosesAnAction` (common 3) flashes the hero after `Teleport 3`: it runs on map 3 | the first thing that stops map 1's build |
| 6 | **`ChangeActorFace`** is not compiled | the compiler | 9 on map 1: `CombatController` page 6, `MonsterData1`, `MonsterData2` | three pages |
| 7 | **Call depth**: the compiler skips calls past `CALL_MAX` = 4 **without saying**; the runtime's stack has 3 levels | both | chains of 6 on map 1 (page 6), 5 on the monster pages | parts of a round would silently not run |
| 8 | **`ChangePBG` keeps the map's picture** | the runtime (VRAM) | 17 backdrops of 640×320, `DarkPanTest` the map's own | every battle with the same backdrop |
| 9 | **Sprite palettes and slots** | the console (CGRAM, VRAM) | 55 graphics from 25 CharSets on map 1, 29 of them drawn with another's palette; up to 31 events in view by where they start, and 18 slots | wrong colours on most monsters; some drawn late |
| 10 | **A route's graphic changes**: a table of 8 | the runtime (VRAM) | map 2: 20 changes ignored with a warning (the plates) | the plates do not show on their slots |
| 11 | **Variables of sixteen bits** | the runtime | `CalculateHPPercents`: 944 HP of 944 gives 34 | the HP meters past 327 HP |
| 12 | **A refresh of every page, every frame**, and the CPU of `BackdropSetter` | the runtime | the refresh not measured here (on A Blurred Line's map 8 one per frame did not fit); `BackdropSetter` ~100 lines of 262, estimated | the battle screen may run at 30 frames per second; nothing breaks |
| 13 | A box with letters the font does not have | the compiler | common 23's garbled statistics of the Lackey ("HP: 9?27?3") | one message branch of Study |

**And what is not a limit**, measured: the events per map (48 and 51 of
120), the pages (map 2 has 425; map 3 already carries 413), the parallel
pages (48), the route slots (12; no warning), the variables (207 slots of
256), the text block (about 68 KB of 262 with both maps), the ROM (54 free
banks), the pictures (none), constants past 32,767 (none), multiplications
(three in the whole game).

### The runtime

* **Interpreter speed**: above. It is not what blocks.
* **Parallel interpreters, event and page tables, route slots, pictures,
  message window**: inside their caps (above).
* **Switches**: `SWITCH_BYTES` = 128. The game needs 135 bytes. The low
  RAM has **20 bytes** free in Frozen World's cartridge, so seven more fit;
  the save grows by as much. The compiler's `SWITCH_MAX` and the page
  conditions go with it: the existing drafts
  [`branches-and-switch-commands-past-switch-1023`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/branches-and-switch-commands-past-switch-1023.md)
  and
  [`page-conditions-on-switches-past-1023-read-other-ram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/page-conditions-on-switches-past-1023-read-other-ram.md).
* **Variables**: 207 slots of the 256 an `OP_VAR` byte addresses. Sixteen
  bits: only the HP percentages overflow (#11). The damage formulas are
  additions, subtractions and random numbers: 2,016 `ControlVars` on map
  1, none multiplying.
* **`map_code` in WRAM**: #3. Behind it is `CODE_CARRY`, where a page that
  goes on after a teleport takes its map's code: map 2's slot pages
  teleport to map 2 itself and go on, and common 3 teleports from map 1 to
  map 3 and goes on. Code in the cartridge does not need carrying:
  `carry_one` already leaves alone a pointer outside bank `$7F`.
* **Far RAM**: 277 bytes free; the call stack needs 15 more for six
  levels.

### The tools

`just culprits` with maps 1 and 2 put back into a throwaway `release`, in
the ports at `0ddf815`:

| page | culprits |
|---|---|
| map 1, `CombatController` page 1 | 17 branches on a switch past 1,023 |
| map 1, `CombatController` page 6 | **the page as a whole** (#2); with calls, only `ChangeActorFace` |
| map 1, `BackdropSetter` | 16 branches on a switch past 1,023 |
| map 1, `MonsterData1` | `ChangeActorFace` ×2 |
| map 1, `MonsterData2` | **the page as a whole**; with every call as a call, `ChangeActorFace` ×6 and 11 switches past 1,023 |
| map 2 | none: every page compiles; what stops it is #3 |
| common events 23, 24, 26, 27, 36, 37 | a switch past 1,023 (and, in 23, #13): their calls are skipped |

**The converter stops on map 1 before anything else** at the flash
(#5), and with map 1 out, on map 2's code. **The text block** has room.
**The banks**: Frozen World's `release` uses 54 of 127.

### The console

* **CPU per frame**: about 100 lines for `BackdropSetter` and ~10 for event
  29, of 262, and a full refresh of the map's pages that was not measured
  (above).
* **VRAM**: the battle animations take 64 tiles from 320 on map 1; the
  panorama is in mode 3, at the 576 tiles a panorama gets
  ([Panoramas](2026-10-05-panoramas.md)). A per-battle backdrop is one of
  17 pictures of 640×320, of which 320×240 are seen (the map is the size
  of the screen): each would have to fit the same 576 tiles.
* **CGRAM**: eight sprite palettes for 55 graphics; a battle shows about ten
  of them at once —three monsters, the heroes, the meters— so it is the
  **whole map's** set that does not fit, not a battle's.
* **OAM**: up to 31 events in view, which OAM holds; the 18 slots of the
  sprite cache are what is short.
* **WRAM**: no room for 60 to 90 KB of code. The grid, the loading buffer
  and the battle scene own the upper halves of both banks
  ([The grid lives in WRAM](../optimizations/lossless/the-map/the-grid-in-wram.md)).
* **The screen is 256 wide and RM2k's 320**: map 1 is 20 cells across and
  the cartridge shows 16. The battle's people are between columns 2 and
  15, so it fits; the `CommandData` and removers stand at 17 to 19 and
  would not be seen (in RM2k they are seen at the edge). Not looked at
  further.


## The creative ways out

Each with what it buys, measured or estimated with its basis, and what it
costs.

### 1. A call is a call

**What**: `CallEvent` to a map's event compiles to a call into that page's
own code, which the map already carries because the page is also a page of
the map. A new opcode with the page's index (three bytes), `OP_DONE` that
returns when there is someone to return to (in RM2k the called event's end
returns, and so does `EndEventProcessing`, which only ends its own frame),
and a call stack of six levels instead of three. "This event" inside the
called page is already resolved against its owner, which is what RM2k
does.

**What it buys**, measured with a prototype of the compiler that emits a
three-byte placeholder instead of pasting:

| | pasted | as calls | and every common event called too |
|---|--:|--:|--:|
| map 1 (with #4 and #6 out of the way) | 3,993,422 | 90,339 | 81,772 |
| the same, identical pages once | 869,078 | 69,227 | 60,660 |
| map 2 | 38,185 | 38,185 | 38,522 |
| all of Frozen World's maps | 4,173,384 | 242,845 | 229,713 |
| A Blurred Line's maps (map 11) | 161,003 (10,555) | 153,562 (3,449) | — |

With calls, `CombatController` page 6 compiles at 5,177 bytes and page 1
at 1,584; the largest page of map 1 is `MonsterData2`, 4,355. The pages no longer go anywhere near 64 KB.

**What it costs**: the opcode and its runtime (the shared common bodies'
`call_enter` already does this with a body index; this one takes a page),
the deeper stack, and one decision the paste avoided: a call inside a
**parallel** page needs its own stack per interpreter, or not to wait inside
the callee. Map 1's two parallels do not wait. And it fixes #7 on the way:
with no paste there is no reason for `CALL_MAX`, only the stack's depth.

### 2. Identical pages once

The page table points each page at its code with a 24-bit pointer, so two
pages with the same bytes can point at the same code: **a converter-only
change**. Map 1's 52 monster pages are 52 copies; stored once, 90,339 →
69,227. In the whole game, 243 → 212 KB.

### 3. The code of the big maps, in the cartridge

**What**: a map whose code does not fit in its WRAM reservation keeps it
in the cartridge, uncompressed, and its pages point there; the others stay
as they are.

**What it buys**: maps 1 and 2 in. **It is the only way that fits them
without redesigning their events**, because neither of them fits in
19,968 bytes even after #1, #2 and the optimisations below. The cartridge
is also faster to read than WRAM: FastROM is 6 master cycles per byte,
WRAM always 8.

**What it costs**: about 110 KB of ROM (69 KB and 38 KB) of the 54 free
banks; in the converter, the placement of a code block bigger than a bank
(each page in one bank, which the 24-bit pointers already allow) and a
`map_code` entry that tells `lz2_grid` there is nothing to decompress; in
the runtime, nothing else: `carry_one` leaves cartridge pointers alone, and
the troops and the shared common events already run from the cartridge.
`test_decompressed_load.py` in the ABL port compares the code in WRAM and
would have to know.

### 4. Streaming from the MSU-1

**Not needed, and worse.** The MSU-1's data port is read one byte at a time
in sequence and would have to be copied to WRAM anyway, so it brings back
the WRAM limit it was meant to avoid. The cartridge has room (#3).

### 5. What a modern compiler would do

Each optimisation measured on this game's data:

| optimisation | what it finds here | payoff |
|---|---|---|
| **calls instead of pastes** (the opposite of inlining) | above | 44 times less on map 1 |
| **identical code once** (common subexpressions, at the page level) | 52 monster pages | 21 KB on map 1 |
| **empty `else`**: the compiler emits a 3-byte jump at every `ElseBranch`, even when the `else` is empty | 6,752 of 7,773 on the maps; 3,456 on map 1, 1,395 on map 2; in common events 196 of 454 | 3 bytes and a jump each: ~10 KB on map 1, 4.2 KB (11%) on map 2; in A Blurred Line, 997 of 1,498 |
| **run a parallel page only when what it reads changes** (hoisting invariant work out of the frame) | `BackdropSetter` reads 113 switches that only `PostBattleCleanup` (common 11) writes, nothing else on map 1 | ~100 lines per frame → once on entering the map |
| **refresh only when the value changes** | event 29 writes the same three variables every frame | a full refresh of map 1's 165 pages per frame, which on A Blurred Line's map 8 did not fit in one; equivalent, because a refresh with nothing changed changes nothing |
| **fuse multiply-then-divide** into one operation with a 32-bit intermediate | all 3 multiplications and all 3 divisions of the game: `CalculateHPPercents` | the meters right past 327 HP, with no RAM |
| **page templates** (rolling copies into a body and a table of numbers: the opposite of unrolling) | map 2: 12,225 commands in **14 shapes** (710 commands, one per shape); map 1: 28,989 in 29 (11,313) | map 2 would fit in WRAM (~10 KB estimated); needs bodies with parameters in the runtime |
| constant folding over switches nobody writes | **1** branch in the whole game | none |
| loop unrolling | 2 loops on map 1 | none |
| merging the monster pages' ten calls to the same page | they are under ten different switches, which the game keeps exclusive but nothing proves | none once calls cost three bytes |
| native 65816 for the hot spots | the only hot spot is `BackdropSetter`, which the row above removes | not worth it |

The 32-bit arithmetic, in taro's order of preference: **the carry register**
(a hidden high half, constant RAM) covers this game, because its three
commands are consecutive on the same variable and nothing runs between
them; **the synthetic command** (`set; multiply; divide` compiled as one
operation) covers it too and costs no RAM at all. Both are the same
pattern, and the second is a peephole on the representation below.

### 6. The intermediate representation

**Today** `compile_command` returns bytes, and `page` glues them in
`pieces` with the open branches patched to absolute offsets (`patch`,
`with_dest`). That is already half an IR —a list of pieces with symbolic
holes— and it is the natural place to start.

**What it would be**: a page compiles to a list of instructions with
**labels** for destinations, a call node for `CallEvent` (to a page, to a
common body) and typed nodes for what the passes look at —switches,
variables, branches—; everything else stays an opaque instruction that
carries its bytes. Passes run over it; the encoder chooses offsets at the
end.

**Incrementally**, each step testable on its own with the ROM byte for byte
equal until a step means to change it:

1. **Labels instead of offsets**, encoding at the end. Same bytes. It is
   what lets a later step widen a jump, or split a page, without touching
   the passes, and it removes the 64 KB wall from the compiler's side.
2. **Jump to the next instruction removed**: the empty `else`. The first
   pass that changes the ROM; the goldens say whether it is right.
3. **The call node**, with the decision of #1: pasted when the callee is
   small, called otherwise. Commons and map events alike.
4. **Peepholes on typed nodes**: multiply-then-divide, the `OP_CELL_TEST`
   fusion that today lives in the compiler as a special case.
5. **Read and write sets per page**, across the map and the common events
   it calls: the analysis behind "run only when what it reads changes",
   which extends Aguará's `commons::pure` to the map's parallel pages and to
   the Book of Three's `Reraise` of
   [`optimise-parallel-events-when-compiling`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/optimise-parallel-events-when-compiling.md).
6. **Templates**, if a map ever needs to fit in WRAM again.

Native 65816 for a hot path stays out: it would put a second back end
behind every opcode for a gain this game does not need.

### 7. Rethinking the events, still RM2k

Patches in the port, not edits to the game's zip, as with map 11. What each
would buy here:

* **`BackdropSetter`, once**: an `EraseEvent` at the end of its page. In
  RM2k the panorama stays; here it saves the ~100 lines per frame. The
  same as the compiler's #5 for this one page, for the price of a patch.
* **The monster pages' dispatch**: 195 commands that call the same page
  under ten switches can be one branch and one call. With calls as calls
  it saves about 20 KB of a map that already lives in the cartridge;
  **without them it does not save map 1**: each `CommandDataHero` page is
  48 KB pasted by itself.
* **Map 2's 24 pages per slot**: a slot's plate as a variable would need its
  graphic changed by a route, which is #10's table of eight. Not better.

**This game's patterns are the compiler's problem more than the events'**:
map 11 was a runtime cost per event; Frozen World is code that the
compiler multiplies. The patches are a complement, not the way in.

### 8. The rest

* **The flash check, aware of teleports**: the converter walks a page's
  bytecode as if it all ran on the map; after a `Teleport` the rest runs on
  the destination. On map 1 the hero is also given the CharSet `nobodyhere`
  by the setup's first route. Added to the existing draft
  [`flashing-hero-shares-a-palette-with-an-npc`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/flashing-hero-shares-a-palette-with-an-npc.md).
* **`ChangeActorFace` as a declared debt**: faces are not drawn, so doing
  nothing is what is seen.
* **The backdrop as a choice on entering the map**: `BackdropSetter` is a
  table "switch → picture" that only changes between battles. The converter
  could emit it as such and the map load pick the panorama from it, one of
  17, each converted like any panorama. VRAM is the panorama's as today;
  the ROM, 17 panoramas.
* **Palettes per battle**: a battle shows about ten graphics of the map's
  55. Palettes given when a page becomes active, like the sprite cache gives
  tiles, would fit each battle in eight. A runtime feature, the biggest of
  the fidelity ones.


## The recommendation, in phases

1. **Compile it** (tools and runtime, without touching the game):
   * `CallEvent` to a map event as a call, with `OP_DONE` returning and a
     stack of six levels (#1, #7). *Measured limit*: map 1 at 90,339 bytes,
     no page over 5.2 KB.
   * Identical pages once (#2 of the ways). *Measured*: 69,227.
   * The code of the maps that do not fit in WRAM, in the cartridge (#3).
     *Measured*: ~110 KB of 54 free banks.
   * Switches up to 1,080, the flash check aware of teleports, and
     `ChangeActorFace` as a debt (#4, #5, #6). Small, each with its draft.

   With that, maps 1 and 2 build and the 324 pages that teleport into them
   compile. **Then it is played**, which is what this research could not
   do: none of the measurements above ran a fight.
2. **Make it look like the original**: the backdrop chosen on entering the
   map (#8), the route graphics' table for the plates (#10), the fused
   multiply-then-divide for the meters (#11), palettes per battle (#9).
3. **The IR**, from labels to read/write sets (#6 of the ways): the empty
   `else` and the parallel pages that run only when what they read changes
   make the battle screen cheaper, and every game gains from them. Of
   phase 3, **refreshing only when a value changes** is small and goes
   first if, played, the battle screen drops frames.

Not recommended: the MSU-1, native code, and rewriting the game's events
beyond a patch for `BackdropSetter`.


## How it was measured

* **The structure**: the dump read with throwaway scripts —per event, per
  page, the trigger, the condition, the number of commands and a histogram
  of them; the pages printed as indented listings; who calls whom and how
  deep; who writes the switches a page reads; the shapes of the pages with
  their numbers taken out—.
* **The culprits**: maps 1 and 2 taken out of `excluded` in a throwaway
  copy of `frozen-world/rm2k-snes.toml`, `just cartridges release` (which
  stops at map 1, after leaving the compiler's request), then `just
  culprits`. The converter's lines about maps 1 and 2 (palettes, slots,
  route graphics) are from that build's `converter.log`.
* **The bytecode sizes**: `rm2k-snes-events compile` with that request,
  reading the size of each page's `code` in `events.json`. The prototypes
  are two environment switches in the compiler, built locally and never
  installed: one makes `CallEvent` emit three bytes instead of pasting (for
  map events, or for every call); the other compiles `ChangeActorFace` as
  nothing and lets branches on switches up to 2,047 through, so that the
  pages that would compile after #4 and #6 are counted. Without the
  switches the local build gives the same sizes as the installed tools.
  A Blurred Line's sizes, with the request its cartridge was last built
  with.
* **The space**: `just space` in `frozen-world/`, with the maps as
  committed.
* **The interpreter**: cycles counted by hand over `run_code`, `op_if` and
  `switch_on` at `497be031`, with 6 master cycles for each code byte and
  internal cycle and 8 for each WRAM byte; it is an estimate, set against
  the 1.2 lines per operation measured in `race-2-at-60-frames`.
