# Other games, measured again

> **Measured on 2026-10-10** by Aguará, without MSU-1, with the tools of
> snes-rm2k `1afe6457`, the ports at `951471f`, this book at `ff908ad` and
> snes-rm2k-work at `e959c97`. It is a snapshot: the numbers are from that
> day and this file is not updated. How to redo each count is at the end, in
> "How it was measured".

[The survey](2026-10-05-otros-juegos.md) measured the seven games on
2026-10-05, and the tasks of 2026-10-06 changed a lot of what it found:
limits that stopped a whole game now degrade with a warning, the window goes
through Adeleine, encounters take two bytes, decorative events can be
background. This is the same measurement again, with the tools of today and
**without fixing anything**: what got better, and what was behind it.


## Summary

* **Six of the seven build a cartridge, as before, and all six now need
  fewer maps left out.** El Dorado and Sunset build every map; Book of Three
  leaves out 1 map instead of 4, Dooms 2 4 instead of 7, Frozen World 2
  instead of 25, Desert Nightmare 12 instead of 24. The exclusions committed
  in the ports are the survey's and are now larger than they need to be.
* **The crutches are the same ones**: four games still need another System
  —A Blurred Line's, through `[graphics] system`— because their own does
  not fit (Book of Three, Dooms 2, Frozen World, Vampires Dawn) or because
  of the End Game screen (Desert); and two still need `party = [1]`
  (Sunset, Desert). The window's "doesn't fit" numbers are the ones the
  tasks of 2026-10-06 wrote down.
* **The pages that compile went up since the survey in every game but Book
  of Three** (on the maps; its troops went up on 2026-10-06): the maps of
  El Dorado, Dooms 2, Frozen World and Desert are now above 96 %. Sunset and
  Vampires Dawn are where the tasks of 2026-10-06 left them. The table is in
  section 3.
* **Vampires Dawn still builds nothing, and two game-wide limits showed up
  behind the ones the tasks of 2026-10-06 removed**: its `Music/` has 281
  songs and the track number is a byte; and with that out of the way, its
  troops take 470 members where the table is one byte. Its start map, 3, no
  longer fits `BOOT_FRAMES` either (46 of 44 frames).
* **Sunset Over Imdahl takes hours to build.** It carries 138 big pictures
  in the background layer, and each one takes minutes in
  `rm2k-snes-images background`. Nothing fails; it is only slow.


## 1. Each one's cartridge

First as each port has it committed —its `rm2k-snes.toml`, with the
survey's crutches—, then removing the crutches one at a time:

| game | as committed | own System | without exclusions (with the committed System) | empty party |
|---|---|---|---|---|
| El Dorado | **builds**, 13 of 13 | it is its own | — (none committed) | it is its own |
| Sunset Over Imdahl | **builds**, 65 of 65 | it is its own | — (none committed) | "the party is empty: there is nothing to draw the hero with" |
| The Book of Three | **builds**, 85 of 89 | the window needs 267 tiles of 256 | builds leaving out only 46 (88 of 89) | it is its own |
| Dooms 2 | **builds**, 86 of 93 | the actor choice's windows reach `$4840` and their tilemap is at `$4800`; with map 1 in, the slot screen and the menu gather 482 tiles of 448 | map 1 stops it: the slot screen and the menu gather 524 tiles of 448; leaving out 1, 10, 14 and 63, it builds (89 of 93) | it is its own |
| The Frozen World | **builds**, 151 of 155 | the window needs 266 tiles of 256 | builds leaving out 1 and 2 (153 of 155) | it is its own |
| Desert Nightmare | **builds**, 165 of 189 | the End Game screen uses 18 pairs of colours and a 4bpp palette has 16 | builds leaving out the twelve of the sweep (177 of 189) | "the party is empty" |
| Vampires Dawn | `map 15: this map can't carry a message window` | the window needs 262 tiles of 256 | see below | it is its own |

"Its own" is that the port does not change that knob. Dooms 2 starts on
map 2, as committed, because map 1 does not build.

**Vampires Dawn**, step by step:

1. As committed, the first error is a map's (15, the window). Each map
   next to the start map (section 2) shows the real wall: **`Music/ has
   281 songs and the track goes in a byte`**, in 387 of the 440. It is a
   limit of the whole game: `rm2k-snes-audio` numbers every file of
   `Music/` as an MSU-1 track, used or not, also with `--without-tracks`.
   The survey did not see it because the variables stopped everything
   first; the tasks of 2026-10-06 presumably did not because some map's
   error came out first, which is what happens with the committed project
   too —it was not checked—.
2. With a copy of the game whose `Music/` has only the 125 songs some page
   or the database names, **the start map, 3, does not fit the boot**: its
   package and the driver need 46 frames of the 44 of `BOOT_FRAMES`.
3. Starting on map 8 —which does fit— and leaving out the 81 maps the
   sweep stops, map 165 (Uruya) does not fit in VRAM next to the others;
   leaving it out too, **"the cartridge's troops don't fit in one-byte
   tables: 234 troops, 470 members"**. The troop index takes two bytes
   since 2026-10-06; the members table does not. That is where it stopped.

### What each cartridge degrades

Since 2026-10-06 a limit that used to stop a map warns and drops what does
not fit. Counted from the converter's log of each committed cartridge, in
maps:

| game | what degrades the most |
|---|---|
| El Dorado | the route graphics table of 8 is full (13 maps); pictures not drawn for lack of VRAM or palettes (13); `ShowPicture`/`MovePicture`/`EraseScreen`/`ShowScreen` accepted undone (11-12) |
| Sunset Over Imdahl | pictures not drawn (43 maps); the route graphics table full (8) |
| The Book of Three | one map without its pictures; the names "DUMMYHERO" cut in the slot screen and in battle |
| Dooms 2 | "the raindrops don't fit in the sprite palettes and it doesn't rain here" (82 maps, though the game sets the weather on five); faces accepted undone (13) |
| The Frozen World | the title screen doesn't fit in VRAM and the game starts without it; one map without its pictures |
| Desert Nightmare | pictures not drawn (136 maps); the route graphics table full (22); `EraseScreen`/`ShowScreen` and faces accepted undone (13-14); the title screen doesn't fit |

**The boot**, as committed, fits in all six: from 11 frames (Sunset) to
35 (Book of Three) of the 44.

**Space** is still not the problem: from 26 banks (El Dorado) to 86
(Desert, 23 of them slow), and 98 for Desert without the survey's extra
exclusions.

**Build time** is the new one. With other agents' runs on the same machine:
El Dorado 5 s, Book of Three 35 s, Frozen World 2 min, Desert 6 min,
Dooms 2 11 min, and **Sunset about 2 h 40 min**. Sunset carries 138 big
pictures in the background layer, and a single one of them, converted
alone with the request the converter wrote, took 4 minutes. Desert carries
285 and takes 6 minutes, so it is not the count: it is something about
Sunset's pictures. Adeleine's choice of colours by tile group
(`27a28646`, 2026-10-06) is the change nearest to it, and **it was not
checked** whether that is the cause.


## 2. Each map, next to the start map

One cartridge per map, with `maps = [start, m]` over the committed
project, crutches included. This is **a different method from the
survey's**: the survey built each map alone, as its own start map, with
`BOOT_FRAMES` raised to 255 in an uncommitted working tree. Next to the
start map no map has to fit the boot, and nothing in the runtime has to
change; a map's limits are counted the same, but the start map's and the
pair's together, which can stop a few that would build alone.

| game | build | before (2026-10-05, alone) | what stops the rest |
|---|--:|--:|---|
| El Dorado | 13 of 13 | 9 of 13 | — |
| Sunset Over Imdahl | 65 of 65 | 65 of 65 | — |
| The Book of Three | 88 of 89 | 85 of 89 | tile animation in WRAM: 10,432 bytes of 8,192 (46) |
| Dooms 2 | 89 of 93 | 89 of 93 | a song with more than 255 sounds: 291 or 414 (10, 14, 63); the menu's names (1) |
| The Frozen World | 153 of 155 | 151 of 155 | the map's code in WRAM: 38,179 bytes of 19,968 (2), and 1,842,300 (1) |
| Desert Nightmare | 177 of 189 | 177 of 189 | panoramas without a VRAM layout (2, 4, 14, 59, 61, 66); more than 104 NPCs in OAM (5, 62, 172); more than 120 events (43, 68); tile animation in WRAM (182) |
| Vampires Dawn | 0 of 440 | 0 of 440 | `Music/` has 281 songs (387); see below |

The maps that the survey lost to `ROUTE_GFX_MAX` and to the window are
back: the first degrades now, and the second is the committed System.
**What stops them now is the same family as on 2026-10-05**: WRAM
reservations for LZ2 streams, OAM, the 120 events, the panoramas, and a
song's sound index. None of those has changed.

Frozen World's map 1 asks for 1.8 MB of map code, which looks like
something being unrolled rather than a big map; **it was not looked at**.

**Vampires Dawn**, with the copy of the game whose `Music/` has only the
songs it names and starting on map 8 (map 3 does not fit the boot):
**359 of 440**.

| what stops it | maps |
|---|--:|
| a song with more than 255 sounds | 28 |
| more than 104 NPCs in OAM | 25 |
| more than 120 events | 15 |
| does not fit in any VRAM layout (57, 95, 99, 225, 399) | 5 |
| tile animation in WRAM (1, 195, 236, 351) | 4 |
| panoramas without a layout (28, 402, 403) | 3 |
| the message window does not fit (15) | 1 |

The OAM and the 120 events are what tasks already open on 2026-10-10 are
about.


## 3. The pages that compile

`rm2k-snes-events culprits --every-map`, with the request of each committed
cartridge —for Vampires Dawn, that of the last attempt in section 1, which
got as far as compiling—:

| game | maps 2026-10-05 | maps 2026-10-06 | **maps 2026-10-10** | common events | troops |
|---|---|---|---|---|---|
| El Dorado | 698 of 972 | 963 | **966** of 972 | 10 of 10 (was 9) | 0 of 80 |
| Sunset Over Imdahl | 896 of 1,369 | 1,266 | **1,266** of 1,369 | 6 of 8 (was 4) | 0 of 1 |
| The Book of Three | 1,271 of 1,282 | — | **1,271** of 1,282 | 19 of 25 | 359 of 746 (was 206) |
| Dooms 2 | 341 of 496 | — | **482** of 496 | 10 of 10 | 1 of 82 |
| The Frozen World | 3,554 of 3,891 | — | **3,819** of 3,891 | 88 of 100 | 0 of 80 |
| Desert Nightmare | 5,190 of 7,340 | 7,150 | **7,277** of 7,340 | 28 of 30 (was 24) | 0 of 100 |
| Vampires Dawn | — | 21,272 (a scan) | **21,272** of 22,977 | 14 of 52 | 0 of 362 |

The "2026-10-06" column is what the tasks of that day wrote down, where
they measured it.

What is left, by game, with the commands that are all that keeps a page
out ("alone" in the report):

* **El Dorado**: six pages: two routes (`MoveEvent`), one message, one
  `ControlVars`, one `ChangeSpriteAssociation`, one `TileSubstitution`.
  The troops: all 80 have a condition the ROM does not check.
* **Sunset Over Imdahl**: routes (70 pages alone), most of them the hero's
  diagonal moves that the 2026-10-06 task already pointed at;
  `FlashSprite` (5), `PanScreen` (4), `ControlVars` and messages (4 each).
* **The Book of Three**: on the maps, `ChangeItems` (6) and
  `ChangeEquipment` (2); in the troops, `ChangeMonsterCondition` (91),
  `ControlVars` (52), `ChangeItems` (48) and `TerminateBattle` (42), plus 95
  with a trigger the ROM cannot look at.
* **Dooms 2**: `ChangeScreenTransitions` (6, transition 19), routes (3),
  and one each of `ChangeActorFace`, `ChangeSystemSFX`, `EnterHeroName`,
  `PlayMovie` and a `Loop`.
* **The Frozen World**: messages (37 pages alone; `\N` and `\V` are among
  the culprit boxes, and so are boxes without any escape, whose reason the
  report does not say), `ChangeMapTileset` (8), `ShowChoice` (6), and `ConditionalBranch`
  (5) on switches past 1,024, which is the ROM's bitmap.
* **Desert Nightmare**: `ControlVars` (48), almost all of them reading an
  event's screen X or Y; messages (10); `InputNumber` (2).
* **Vampires Dawn**: `ControlVars` (521 alone), most of them plain sets and
  additions —consistent with the variables that were left without a slot
  since 2026-10-06, though **that was not checked one by one**—; routes
  (254), `ShowChoice` (210), messages (162), `ConditionalBranch` (80) and
  `Loop` (40). In the troops, faces (23) and conditions.


## 4. What got better, and what appeared behind

**Better**, by what did it:

* **The degradations** (`ROUTE_GFX_MAX`, `EraseScreen`/`ShowScreen`, the
  title that does not fit): El Dorado and Sunset build every map, and
  Frozen and Desert boot without `--no-title`.
* **`[graphics] system`**: Book of Three, Dooms 2, Frozen World and Desert
  build with A Blurred Line's System instead of a retouched copy of the
  game. It is still a crutch: none of them builds with its own.
* **The four shortcuts, `EraseEvent`, the color codes and `\N`**: the page
  counts above.

**Behind**, in the order a fix would unblock the most:

1. **The window and the 8bpp screens with a game's own System** (4 games,
   and Desert's End Game): the numbers are the same as on 2026-10-06 —267,
   266 and 262 tiles of 256; the actor choice past `$4800`; End Game with
   18 pairs of colours—.
2. **The LZ2 reservations in WRAM**: tile animation (Book of Three 46,
   Desert 182, four of Vampires Dawn) and map code (Frozen 1 and 2).
3. **A song's sound index is a byte** (Dooms 2, 3 maps; Vampires Dawn,
   28).
4. **OAM and the 120 events** (Desert 5, Vampires Dawn 40): already tasks.
5. **Vampires Dawn's game-wide limits**: 281 files in `Music/`; the
   members of its troops; a start map that does not fit the boot.
6. **The empty party** (Sunset, Desert): unchanged.
7. **Sunset's build time**.

**The committed exclusions are now stale**: Book of Three excludes 44, 69
and 74 too, Dooms 2 45, 58 and 59, Frozen World 69 and 84, and Desert
twelve maps more than it needs. Nothing was changed in the ports: this is a
snapshot.


## How it was measured

With the tools installed from snes-rm2k `1afe6457`, Don Miguel's RTP and
the usual SoundFont, in a worktree of the ports at `951471f`, without
changing anything in either repository. The scripts were throwaway and
were not versioned.

* **The cartridge as committed**: `just cartuchos` in each game. A wrapper
  for `rm2k-snes-events` earlier in the `PATH` copied the request of
  `compile` as the converter passed it.
* **Without crutches**: a copy of each `rm2k-snes.toml` without `system`,
  without `excluded`, or with `party = []`, one knob at a time, built with
  `rm2k-snes-cartridges --project <copy> release`; when the error named a
  map, that map was excluded and it was built again. For Desert and
  Vampires Dawn the loop was seeded with the maps the sweep stops.
* **Each map**: one copy per map with `maps = [start, m]` and
  `excluded = []`, six at a time.
* **Vampires Dawn**: a copy of the game where `Music/` has only the songs
  whose name appears in the dump (125 of 281), and `start_map = 8`, the
  first map the sweep built.
* **The pages**: `rm2k-snes-events culprits --every-map` with each saved
  request. The families of section 3 come from grouping the culprits in
  `culprits.json` by code and parameters.
* **What degrades**: the `WARNING` lines of each `conversor.log`, grouped
  by text.

What was **not** measured: nothing was run in an emulator —nobody looked
at these cartridges, not even their first seconds—; not the battles, not
the music. The survey's captures were not repeated.
