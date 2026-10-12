# Other games: the survey

> **Measured on 2026-10-05 at `24e0223e`** (snes-rm2k), by Aguará, without
> MSU-1. It is a snapshot: the numbers are from that day and this file is not
> updated. How to redo each count is at the end, in "How it was measured".

Until today the engine had ported a single game. taro left seven more RPG
Maker 2000 games to see how general it turned out —El Dorado, Sunset Over
Imdahl, The Book of Three, Dooms 2, The Frozen World, Desert Nightmare and
Vampires Dawn—, with one request: find what they have in common before
fixing anything.


## Summary

* **Six of the seven build a cartridge that boots**, and in three of them
  the beginning plays almost the same as in RM2k (Book of Three, Frozen
  World, Dooms 2: see the sheets). Vampires Dawn builds none: it uses more
  variables than the 256 the engine has.
* **But four of the six need a crutch that is not the game's**: the
  System —the windows' skin— does not fit in the 15-color palette of the
  engine's window, and the survey replaced it with a reduced copy. **It is
  the first thing to fix**: without it no game with a gradient System
  reaches the screen.
* **What repeats the most**, ordered by how many games it unblocks:

  | fix | games | what it does today |
  |---|:-:|---|
  | the window with more than 15 colors | 5 | stops the whole game |
  | more than 8 command-34 graphics per map (`ROUTE_GFX_MAX`) | 5 | stops the map |
  | message escapes (`\C`, `\N`, `\.`, `\!`, `\|` mid-box) | 4 | the page does not compile: thousands |
  | troop pages with a condition the ROM does not check | 5 | the page does not compile |
  | `ConditionalBranch` on an event's direction | 3 (+ ABL) | the page does not compile |
  | faces in messages | 2 | the page does not compile: thousands |
  | `EraseScreen`/`ShowScreen` | 2 | the page does not compile |
  | `EraseEvent` | 2 (+ ABL) | the page does not compile |
  | the title that does not fit in VRAM | 2 | stops the whole game |
  | the empty party at the start | 2 | stops the whole game |

* **Setting up a new project is costly**: sixteen sections of ABL's
  `rm2k-snes.toml` that the tools ask for even if the game does not use
  them, plus an empty case. A `rm2k-snes-project new` is needed, and the
  neutral keys need default values.
* **Eight small, general things were fixed on the branch**, each with its
  test: four of the seven ABL assumptions that
  [`2026-10-02-el-juego-de-pruebas.md`](2026-10-02-el-juego-de-pruebas.md)
  had listed, and four new ones. None of them moves ABL.
* **Where to go next**: the window through Adeleine, `ROUTE_GFX_MAX`, the
  message escapes and `rm2k-snes-project new`, in that order. See section 6.


## 1. The seven

| game | maps | language | music | Harmony.dll | what is odd about it |
|---|--:|---|---|---|---|
| El Dorado | 13 | German | 3 MIDI | Ineluki's v1.2, with keys | |
| Sunset Over Imdahl | 65 | English | 8 MIDI | RM2k's | upper-case files; a single item in the database |
| The Book of Three | 89 | English | 67 MIDI | none | RTP System; invisible hero |
| Dooms 2 | 93 | English | 53 MIDI | none | three BMPs; a `PlayMovie` |
| The Frozen World | 155 | English | 73 MIDI | none | 500 variables and 1,500 switches |
| Desert Nightmare | 189 | English | MP3 through Harmony | Ineluki's v1.1.1, with links | no battles; empty party |
| Vampires Dawn | 440 | English | 274 MIDI | RM2k's | nested folder, with its installer |

None uses DynRPG or its own fonts. All seven are RM2k games (no 2003
`ldb_id`).

**What is outside RM2k**, with the DLLs compared by their fingerprint: the
473,600-byte `Harmony.dll` is RM2k's —it is in Sunset and Vampires Dawn, and
as `oldharmony.dll` in El Dorado and Desert—. The other two are **Ineluki's
patches**:

* **Desert Nightmare** plays its music as MP3: fifteen text `.link.wav`
  files (`..\mp3\Credits.mp3` and `loop`) that its Harmony turns into an MP3
  track. The port does not read them: those themes do not play. It is the
  only thing from outside RM2k that changes what is heard, and MSU-1 would be
  the natural way to carry it; without MSU-1, a MIDI would have to be found
  or they would have to be silenced.
* **El Dorado** ships the keys patch (v1.2, "mit KeySupport"), but has no
  `.script`: it does not use it.


## 2. Setting up a project

Each one is its own repo, outside these two —where, the task says—:
`rm2k-snes.toml`, `justfile`, `data/` dumped with Ditto, `casos/nada.json`
and a README. The first one was put together by hand, against the tools'
"missing key" errors; the other six were copied by a seventy-line
throwaway script, which is what a `rm2k-snes-project new` would do.

**What had to be filled in without the game asking for it**:

* sixteen tables or keys that are ABL decisions and have an obvious neutral
  value —`[graphics] opaque = []`, `[music] apart_themes = []`,
  `[sound_effects.whole]` empty, `[events] counters = []`,
  `effect_slots_of_first_copies = 0`…—;
* `[cases] real_game` with its empty file, and `debug_map_entry`, the name
  of a case that does not exist;
* `[battle] fallback_backdrop`, which had to be one of the game's
  backdrops;
* a cartridge called `release`, with `cases = "all"` and
  `excluded_cases`.

**The proposal**: that keys with a neutral value have it by default
—`int_or` already exists for that—, and that `rm2k-snes-project new <game>`
writes what really is the game's: the name, the title, the signatures, the
tree's start map and `below`. It is little code and it is what any new game
is going to pay.

**Ditto**: all seven round-trip byte for byte (`just datos-vuelta` in each
project), after looking for `RPG_RT.LDB` case-insensitively.


## 3. How far each one gets

### Each map alone

One cartridge per map, with that map as the start map and no other. With a
caveat that matters: **a map alone compiles fewer pages** —those leading to
maps that are not there drop out—, so what stops with neighbors may not show
up here (El Dorado's map 8 builds alone and not with the others).

To see past what stops a whole game three crutches were used, noted in each
project: the System reduced to 12 colors (the game's own in Dooms 2 and
Frozen World; the RTP's, reduced, in Book of Three, Desert and Vampires Dawn,
because theirs does not fit even reduced), the BMPs converted to PNG
(Dooms 2), `party = [1]` (Sunset, Desert), and no title (Frozen, Desert).
`BOOT_FRAMES` went up to 255 only in the working tree, uncommitted.

| game | build alone | what stops the rest |
|---|--:|---|
| El Dorado | 9 of 13 | `ROUTE_GFX_MAX` (4) |
| Sunset Over Imdahl | 65 of 65 | — (the `ô`, before the fix) |
| The Book of Three | 85 of 89 | the window does not fit in VRAM (3); the tile animation in WRAM (1) |
| Dooms 2 | 89 of 93 | a theme with more than 255 sounds (3); the menu names (1, the start map) |
| The Frozen World | 151 of 155 | the window does not fit (2); the map's code in WRAM (1); `ROUTE_GFX_MAX` (1) |
| Desert Nightmare | 177 of 189 | panoramas without a VRAM layout (6); more than 104 NPCs in OAM (3); more than 120 events (2); tile animation in WRAM (1) |
| Vampires Dawn | 0 of 440 | more than 256 variables (290 + 92); the window (19); OAM (19); battle animations (7); 120 events (7) |

**The boot**: the start map's audio package has to upload in 44 frames
(`BOOT_FRAMES`). The five start maps of the cartridges fit, but of the maps
that build alone, more than 44 —if they were the start map— are needed by 7
of 9 in El Dorado, 126 of 151 in Frozen World and 30 of 89 in Dooms 2, up to
119 frames. It is sized for ABL's on purpose
([`decisiones/el-arranque-esta-dimensionado-para-el-paquete-de-arranque.md`](../decisions/el-arranque-esta-dimensionado-para-el-paquete-de-arranque.md));
for another game it would have to come from the cartridge.

### Each one's cartridge

With all the maps, and removing the ones that stop it, one at a time, until
it builds:

| game | start | maps | left out | why left out |
|---|--:|--:|---|---|
| El Dorado | 8 | 8 of 13 | 4, 5, 6, 11, 12 | `ROUTE_GFX_MAX`; with 12, map 8 also goes over 8 |
| Sunset Over Imdahl | 11 | 60 of 65 | 34, 47, 56, 57, 63 | `ROUTE_GFX_MAX` |
| The Book of Three | 1 | 85 of 89 | 44, 46, 69, 74 | the sweep's |
| Dooms 2 | **2** | 86 of 93 | 1, 10, 14, 45, 58, 59, 63 | map 1, character select, does not build; with neighbors, 2 and 3 go over `ROUTE_GFX_MAX` |
| The Frozen World | 7 | 130 of 155 | those with id 135 or more, and 1, 2, 69, 84 | with more maps the sample directory goes over 255 entries (`SRCN` is a byte) |
| Desert Nightmare | 1 | 165 of 189 | 24 | the sweep's, and twelve more for `ROUTE_GFX_MAX` with neighbors |
| Vampires Dawn | — | — | — | the variables |

**`ROUTE_GFX_MAX` is what leaves out the most maps**: twenty-three in five
games. It is 2 bytes of RAM per graphic (`route_gfx_buf`); the comment says
ABL asks for six at most. Raising it to 16 costs 16 bytes of low RAM, and
moves the `BSS` —that is, ABL's ROM—.

### Space

`just espacio` in each project, with the cartridges above: none goes over 78
of the 127 data banks, and banks 0 and 1 have room to spare in all of them.
**Space is not the problem** for any game; the limits that stop them are
VRAM, RAM, palettes and one-byte indices.


## 4. The pages that compile

`rm2k-snes-events culprits --every-map`, with each one's cartridge request
(and the crutches above):

| game | maps | common events | troops |
|---|---|---|---|
| El Dorado | 698 of 972 | 9 of 10 | 0 of 80 |
| Sunset Over Imdahl | 896 of 1,369 | 4 of 8 | 0 of 1 |
| The Book of Three | 1,271 of 1,282 | 19 of 25 | 206 of 746 |
| Dooms 2 | 341 of 496 | 10 of 10 | 1 of 82 |
| The Frozen World | 3,554 of 3,891 | 88 of 100 | 0 of 80 |
| Desert Nightmare | 5,190 of 7,340 | 24 of 30 | 0 of 100 |
| Vampires Dawn | does not get there: compilation stops on the variables | | |

What blocks them, by family and not by code:

* **Message escapes.** The engine understands `\V[n]` and, as the tail of
  the last line, `\|` and `\^`. Everything else leaves the page out: `\C[n]`
  (the color) in Sunset —690 boxes with only `\C`— and in Desert —2,144—;
  `\N[n]` (an actor's name) in Frozen —696— and Dooms 2; `\.`, `\!` and
  `\|` in the middle of the box in Sunset and Dooms 2 (667 boxes with `\!`).
  **Four games**, and in Frozen World it is almost everything that does not
  compile.
* **Faces**: `ChangeFaceGraphic` before a message. 831 uses in Dooms 2,
  2,049 in Desert Nightmare. It drags along the page's messages, which is
  why they show up as culprits "with others".
* **`ConditionalBranch` on an event's direction** (class 6): 176 in El
  Dorado, 153 in Sunset, 354 in Desert. It is the same family as the 31 ABL
  pages that ask which way the hero is facing
  ([`2026-10-05-los-comandos-que-faltan.md`](2026-10-05-los-comandos-que-faltan.md)).
* **`EraseScreen` and `ShowScreen`**, with the default transition or a fade:
  270 in El Dorado —always with `PlayerVisibility`— and 698 in Desert.
* **`EraseEvent`**: 157 pages in Desert, 127 on their own; 3 in El Dorado.
  It is the task that is already in `todo/` because of ABL.
* **Troops**: almost all their pages have a condition the ROM does not
  check —turns, an enemy's HP—. In Book of Three, which has many,
  `ChangeMonsterCondition`, `TerminateBattle` and the comments.
* One at a time: `ChangeMapTileset` (Frozen, 8 pages), `ChangeSystemGraphics`
  (Sunset, Desert), `ChangeEquipment` (Book of Three), `PlayMovie`
  (Dooms 2), `EnterHeroName` (Dooms 2), `InputNumber` with a variable
  (Frozen, Desert).


## 5. The capture next to the original

One sheet per game, where taro looks at captures (the task says where): on
top the original under Wine —the 2015 runtime, which does not use Harmony—,
below the cartridge in snes9x, at the same moments: the title, and 5, 15 and
30 seconds after accepting the first option. The ROMs, next to the builds,
one per game.

What is seen:

* **The Book of Three** and **The Frozen World**: the beginning is the same,
  frame by frame, except for the font color (the reduced System). Frozen,
  without a title, goes straight into the wizard's scene.
* **Dooms 2**: it boots on map 2 because map 1 does not build, and the title
  is the same as the original's.
* **El Dorado**: the title is the same; map 8, choosing difficulty, shows up
  without its two signs —they are pictures, and the map has no sprite
  palettes for them: the converter warns about it—.
* **Sunset Over Imdahl**: the title is the same; the introduction, which in
  the original is pictures fading into each other, stays blank with the hero
  the survey gave it (`party = [1]`).
* **Desert Nightmare**: the picture menu ("With Intro / No Intro / Quit")
  comes out right, but **the background, a mode 3 panorama, is light-blue
  garbage**. It is a bug in the panoramas, which were merged the same day:
  it is in no golden because ABL has none like it. It has to be looked at
  before anything above.
* **Vampires Dawn**: only the original.


## 6. What belongs to whom, and where to go next

### Fixed on the branch

Each in its own commit, with a test that was seen red:

| fix | games | was |
|---|---|---|
| Ditto looks for `RPG_RT.LDB` case-insensitively | Sunset | new |
| a game without a debug map loads | all | assumption 1 |
| a single-map cartridge does not pass an empty `--maps` | all | assumption 3 |
| the System, faces, title and pictures also from the RTP, case-insensitively | Book of Three | assumption 5 |
| a leader without a CharSet is a leader without a graphic | Book of Three, Vampires Dawn | new |
| an item that is not in the database is not carried | Sunset | new |
| the fallback backdrop is only asked for if some battle needs it | Desert | assumption 6 |
| a letter the font does not have stops the page and not the game | Sunset | new |

### The engine's, by how many games it unblocks

1. **The window with more than 15 colors** (5: Dooms 2, Frozen, Book of
   Three, Vampires Dawn, and Desert because of End Game). Assumption 7.
   Today the window's palette carries the background, the frame, the arrow,
   the cursor, the twelve rows of the font's gradient and the shadow; a
   System with a gradient goes over 30. Besides, the frame with a stretched
   background asks for more tiles than the bank has (Book of Three,
   Vampires: 259-261 of 256), and the actor choice two more tiles too many.
   **The way is for Adeleine to decide which colors are lost**, as with the
   maps —Voodoo does not decide colors—, and for it to be a versioned
   decision of the game. It is big and it is a judgment call: taro has to
   see how it looks.
2. **`ROUTE_GFX_MAX`** (5: El Dorado, Sunset, Dooms 2, Frozen, Desert;
   twenty-three maps). Small: a bigger `.res` and the constant. It moves
   ABL's ROM.
3. **Message escapes** (4). `\C` is the most requested and the cheapest of
   the visible ones; `\N` needs the name in the ROM, which is already there
   for the menu; the waits in the middle of a box belong to the composer.
4. **`rm2k-snes-project new` and the default values** (every game to come).
5. **Troop pages** (5): turn and HP conditions.
6. **`ConditionalBranch` on direction** (3 and ABL), **`EraseEvent`** (2
   and ABL), **`EraseScreen`/`ShowScreen`** (2), **faces** (2).
7. **The title in VRAM** (2: Frozen, Desert): photographic images of 800
   unique tiles at 8bpp against what the menu leaves.
8. **The empty party** (2: Sunset, Desert): RM2k starts with nobody and no
   visible hero; the converter asks for a leader to draw.
9. **`BOOT_FRAMES` per cartridge** (none needs it today, but any other start
   map does).
10. One at a time: the directory with more than 255 samples (all of Frozen),
    a theme with more than 255 sounds (Dooms 2), the menu names with many
    actors (Dooms 2), BMP (Dooms 2; RM2k accepts them and `rm2k-render`
    rejects them on purpose for lack of anything to test them against: now
    there is), the LZ2 reservations in WRAM, the panoramas without a layout,
    OAM and the 120 events (Desert, Vampires).
11. **The variables** (all of Vampires Dawn): 256 one-byte slots and 512
    bytes of far RAM. It is a redesign of how variables live, and the only
    thing it unblocks is that game.

### Each game's own, as its own patch

* **Dooms 2**: map 1, character select, asks for more names than the menu's
  bank has; a patch could split it.
* **El Dorado**: map 8's signs as map tiles and not as pictures.
* **Sunset**: the items the database does not have are an oddity of the
  game, and they no longer stop anything.

### From outside RM2k

* Desert Nightmare's MP3 music (Ineluki's Harmony): MSU-1, or silencing it.
* Sunset's `ô` and El Dorado's German: the console's font is ASCII. A font
  with Latin-1 is drawing work, taro's.

### The recommendation

First **look at Desert's panorama**, which is a bug in something already
considered done. Then, in this order: **the window through Adeleine**
—without it four of the seven cannot be seen without a retouched copy of the
game—, **`ROUTE_GFX_MAX`** —the cheapest fix that gives back the most
maps—, **the `\C` and `\N` escapes** —thousands of pages in four games— and
**`rm2k-snes-project new`**. With those four, Book of Three, Frozen World and
Dooms 2 would have a playable cartridge without crutches, and El Dorado and
Sunset almost all their maps. Vampires Dawn goes last: it asks for remaking
the variables for a single game.

And a process warning: **installing only some tools locally mixes two
runtimes**. Each binary reads `tools/runtime/` from the checkout it was
installed from (`suite::runtime`), so with `cartridge` local and
`rm2k-snes-audio` global, `BOOT_FRAMES` came from one tree and the assembly
from another. It did not bite here because it was seen right away; on a
branch that changes the runtime, it will. The way out is to install locally
everything that reads the runtime —`cartridge`, `convert`,
`rm2k-snes-audio`— whenever it is touched.


## How it was measured

With this branch's tools installed in `tools/.local-tools`, Don Miguel's RTP
and the usual SoundFont. The scripts were throwaway and were not versioned:

* **Ditto**: `just datos-vuelta` in each project: `unpack`, `pack` and `cmp`
  of every `.lmu`, `.ldb` and `.lmt`.
* **The sweep**: for each type-1 map in the tree, a `rm2k-snes.toml` copied
  from the project with `start_map` and `maps` set to that map, and
  `rm2k-snes-cartridges --project <copy> release`; eight at a time. The
  cause is the last line of the error. `BOOT_FRAMES = 255` in the working
  tree during the sweep, and each map's estimate from `conversor.log`.
* **The cartridge**: all maps except the sweep's, and removing the one the
  error names until it builds; in Dooms 2, adding one at a time from map 2;
  in Frozen World, the longest prefix by id, by bisection.
* **The pages**: the `rm2k-snes-events compile` request copied while
  building the cartridge —a wrapper in the PATH—, and `culprits
  --every-map`. Section 4's families come from grouping the culprits in
  `culprits.json` by code and parameters.
* **The captures**: Wine with the 2015 runtime and a prefix copied from
  ABL's, on its own Xvfb, Enter with `xdotool`; the cartridge with ABL's
  libretro harness (`retro.Console`), A at 4 s.

What was **not** measured: whether what compiles does what it should beyond
the first thirty seconds, nor battles, nor music: nobody played these
cartridges. The captures are the only thing that looked at the screen.
