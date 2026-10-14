# What still blocks the end

> **Measured on 2026-10-14**, by Cardón, with the tools at `a7f278e6`
> (the-advocate) and ABL at `6a9d53c` (the-advocate-ports). It is a
> snapshot: the numbers are from that day and this file is not updated.
> What a cartridge has left **today** is said by `just space`; how to redo
> each measurement is at the end, in "How it was measured". The task is
> [`abl-what-still-blocks-the-end`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-what-still-blocks-the-end.md).

taro's question: "which blockers does it have today that stop it from being
played to the end? I suspect very little is missing."

## Summary

* **The ending exists, and it was found**: after Eisen's simulation and the
  Advocate's escape, map 277's last scene leads to 288 ("A Gain... and a
  Loss"), and 241 ("Tram to Prima") shows **"To be concluded..."**, offers
  to save the game for *Line's End* and plays the teaser trailer (256, 268,
  299 to 309), which returns to the title. In this cartridge, that whole
  chain plays from 277 to the title screen.
* **`release` stops at the first night in Paradise**, on purpose: 108's fork
  puts the end-of-demo sign where Emily says good night, and the project
  file carries the maps below 129. **About 180 maps of the story are not in
  the cartridge**, from the next day (Talan's house, 114, switch 396) to the
  teaser.
* **The events are no longer the problem.** With every map of the game,
  `rm2k-snes-events culprits` compiles **all 5,508 pages of the 307
  maps**, and every troop page that has a condition; of the 60 common
  events only 32 does not compile alone, and it compiles on its map. The
  seven commands that left 36 pages out on 2026-10-05 are all done. What
  the build still leaves out are common events 42 and 44, Radin's and
  Sern's menus, as shared bodies, and no step of the story needs them.
* **Taking the rest of the game in stops five times**, and none of them is
  a page. A cartridge with the 307 maps reachable from the start was
  built, with each stop patched in a throwaway copy of the tools to see the
  next one. In the order the build hits them: the timer digits do not fit
  on 108; the text block's measuring pass stops a common event; the slot
  screen has no room for the new leaders' names; the materials' table runs
  into the panorama's state in far RAM; and **the ROM does not reach: the
  whole game asks for 8.42 MB of data against the 7.70 MB the cartridge
  has, about 700 KB over**. With `--msu-everything` it builds, and two
  stretches were played in it: the next day, and the ending.
* So taro's guess is right about the engine and wrong about the cartridge:
  four of the stops are small (a line in the project file, or a
  few lines in the tools); **the one that is not small is the space**, and
  it asks for a decision.

## 1. The story's path

From the static walk over `data/` (teleports, autostart pages, the switches
each scene sets and the next one asks for). The story branches by the
profession Talan picks at the celebration (127, switches 385 defender, 386
farmer, 388 actor), and each branch has its own second and third day; the
rest is one line.

| stretch | maps | what carries it forward | in `release` |
|---|---|---|---|
| Lashe City to the first night | 4, 1… 108, 109–128 | — | **yes**, up to Emily's good night (108 event 47, switch 395) |
| the next day | 114 (event 10, 396) | 47 jumps to Talan's house, which the fork replaces with the end sign | no |
| the job | defender: 150, 151 (Sern, the quarry timer, common event 36, 521); farmer: 152–156 (510); actor: 117 (item 152) | each ends in 427, "one month later" | no |
| the bandits | 114 → 160 Fighting Bandits in Farm, 157 Bandit Raid, 118 (458) | | no |
| the second month | defender: 121, 165–167; farmer: 159, 178, 179; actor: 117, 142–144, 145, 146 (441) | each ends in 147 (492) | no (121 goes in as a test map) |
| the agency comes | 147, 149, 148 Paradise Burning | 148 event 77 | no |
| the line narrows | 168–174 (479–483) | autostarts, one after the other | no |
| the flight | 203, 204, 236, 205, 209, 206, 248 | 205 (604–609) | no |
| Surl and Memnosyne | 245, 246, 247, 207, 208; the memories 212–231, 239, 240, 243, 104, 189, 314–319, 349–351, 242, 244, 345, 347; 232–235, 237, 238, 254 | 208 (618), 217 (634), 207 event 24 (635) | no |
| back to Paradise | 249, 296, 250, 251, 252 (636, 656) | 252 returns to 208 (662) | no |
| the kingdom of Surl | 210, 257, 264–267, 270, 258, 271–273, 260 (658) | | no |
| the refinery | 261, 263, 289, 262, 290, 291 (693), 292–295 | 295 jumps to 253 | no |
| the Agency and the Advocate | 253, 277, 276, 278, 279, the catacombs 281–344, 323 (671); 284, 285, 286 (684); 287 (688, 690) | 277's five autostarts, one per switch | no |
| the ending | 277 → 288 → 241 → 256, 268, 299–309 → title | | no |

Two things on the way that look like walls and are not:

* **Eisen's simulation** (278 and its catacombs) closes with item 306 or
  with Eisen's password, 727 (278 event 8): either opens 671.
* **The Advocate's minigame** (285) offers "Give up." after three failures
  (286), and giving up goes on with the story.

## 2. What blocks

In the story's order, which here is the order in which taking the maps in
hits each one. Except the first, none is a page of the game: they are
limits the build stops at.

1. **The cartridge ends at the first night** — 108, event 47 of the fork,
   and `below = 129` in `rm2k-snes.toml`. It is the demo's cut, not a bug:
   it moves when the rest fits. *Size*: deleting the fork and widening the
   rule, once 2 to 6 are solved. Draft:
   [`abl-release-stops-at-the-first-night`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-release-stops-at-the-first-night.md).
2. **The quarry's timer stops the build on 108** — the defender's job (150,
   event 4) starts a five-minute timer, and the converter gives the digits
   to every map it reaches by walking: from 150 one walks out to 108, whose
   eight sprite palettes are full ("the timer doesn't fit"). It really
   happens in RM2k too: the job can be left. *Size*: one line —108 in
   `timer_never_runs_in`, which then stops the digits at the town: they
   reach 63 maps, the quarry's among them— and what it costs is a timer
   that does not show while Talan walks around town in the middle of the
   job. Draft:
   [`abl-the-quarry-timer-does-not-fit-on-108`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-quarry-timer-does-not-fit-on-108.md).
   (It also resolves
   [`abl-manage-quarry-timer-jumps-to-a-map-not-carried`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-manage-quarry-timer-jumps-to-a-map-not-carried.md),
   which is only that 150 is not carried.)
3. **The text block's first pass stops a common event** — with every map,
   the boxes without letter pairs pass 256 KB (262,207 bytes when common
   event 12 is reached), and the measuring pass, which is meant to have no
   cap, still writes each box's offset into a 16-bit operand: the box does
   not fit, the page "does not compile", and a common event that the plan
   said compiles stops the cartridge ("common event 12 compiled on its own
   and not with the cartridge's registries"). The block that goes into the
   ROM, with pairs, is far from the cap: 218,410 bytes counting by eight,
   less counting by four, against 262,144. It is a bug of the compiler, not
   of space. *Size*: small, in `rm2k-snes/events`. Draft:
   [`the-text-measuring-pass-stops-pages-past-256-kb`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-text-measuring-pass-stops-pages-past-256-kb.md).
4. **The slot screen has no room for the new leaders' names** — Royal Dalia
   (30), the Advocate (31) and "ABL 2.0 Save" (34), who lead the party in
   the last chapter and in the ending, ask for 48 tiles and the menu's bank
   leaves 44: `rm2k-snes-screens` stops. It is point 4 of the task that
   made the build degrade instead of stopping, the one left undone. *Size*:
   four tiles short; small to degrade —cutting the names that do not fit—,
   more to make room. Draft:
   [`abl-the-slot-screen-has-no-room-for-the-last-leaders-names`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-slot-screen-has-no-room-for-the-last-leaders-names.md).
5. **The materials' table runs into the panorama's state** — `FAR_GROWTH`
   is placed by hand in far RAM with room for 21 party actors, and with the
   whole game 23 can join (Drago, Royal Dalia, the Advocate, Kersh and "ABL
   2.0 Save" join the 18 of `release`): the assembler stops at the two
   asserts that guard it. *Size*: small, moving it to `FARBSS` like every
   new variable. Draft:
   [`the-materials-table-has-room-for-21-actors`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-materials-table-has-room-for-21-actors.md).
6. **The ROM does not reach** — the whole game asks for **8,419,280 bytes**
   of data and the 127 data banks hold **7,700,480**: about 700 KB over,
   before counting what the packing loses. `release` asks for 5,583,989.
   Where it goes, by family of label: the map tiles (1.45 MB), the song
   streams (1.12 MB), the poses (1.10 MB), the samples (1.07 MB) and the
   panoramas (0.53 MB, tiles and maps). On 2026-10-01 the count said the
   whole game fit with 850 KB to spare, and it did not count the panoramas
   (now drawn) nor the songs and maps that came after. With
   `--msu-everything` the ROM asks for 4.24 MB. *Size*: large, and a
   decision —what to compress or lose, or the MSU-1 required, which [the
   MSU-1 is required only when the ROM does not
   reach](../../../decisions/the-msu-1-is-required-only-when-the-rom-does-not-reach.md)
   allows and [the game is playable without
   MSU-1](../../../decisions/the-game-is-playable-without-msu-1.md) does
   not want—. Draft:
   [`abl-the-whole-game-does-not-fit-in-8-mb`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-whole-game-does-not-fit-in-8-mb.md).

With 2 to 6 out of the way —in the experiment, by patching each one— the
cartridge builds, and its bank 0, bank 1, `BSS` and `ZEROPAGE` are where
`release` leaves them: the map tables do not grow enough to matter (1,359
bytes left in bank 0, against 1,366 in `release`). No event is left out
for the console's RAM, and the game names 173 variables, under the 256 the
ROM keeps.

## 3. What degrades

What the build of the whole game says, on the maps `release` does not
carry, plus what is already known; none of it stops the story.

* **Background tiles fused**: 148 Paradise Burning (74) and 250 Return to
  Paradise (79) are drawn with tiles merged into the most similar ones.
* **Pictures not drawn**: the smoke on 207, Memnosyne's Adobe (no sprite
  palette left), and 'Ready' on 285 (no VRAM layout fits it); 286 erases a
  picture the map does not carry, which is harmless.
* **More walkers than route slots**: 207 sends 13 events walking and 285
  sends 48, against twelve slots; a route that finds them all busy is lost.
  On 285 they are the minigame's guards, which can be given up.
* **Songs that are WAV play only with MSU-1**: `USTravelling`, which plays
  in the ending (288), `ExplosForTeaser`, in the teaser, and `ocean`, on the
  beach; `nightbg` was already in `release`.
* **Names cut**: Royal Dalia, the Advocate and "ABL 2.0 Save" in the battle
  and the slot screen; and the item list, which asks for more than the
  windows leave, as in `release`
  ([`abl-item-text-doesnt-fit-in-what-the-windows-leave`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-item-text-doesnt-fit-in-what-the-windows-leave.md)).
* **The quarry's timer is not seen on 108**, if 2 is solved with the
  project file.
* Already known, and on the path: the agents on the road to Paradise do not
  come (105–107,
  [`abl-the-agents-on-the-road-to-paradise-do-not-come`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-agents-on-the-road-to-paradise-do-not-come.md),
  in progress); Radin's and Sern's menus do nothing, but no step of the
  story asks for them
  ([`radin-s-and-sern-s-menus-do-not-compile`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/radin-s-and-sern-s-menus-do-not-compile.md));
  the rain sounds of the port's known issues; `ChangeSystemBGM` on 312,
  accepted and not done.

## 4. What was played

In the experiment's cartridge, with the harness, from switches and a
teleport:

* **The next day**: 108 at night with 395 on, Emily's good night, the jump
  to Talan's house and the hero with control and 396 on.
* **The quarry**: Sern's job (150, event 4), the timer, common event 36
  closing it, Sern's page, "one month later" and the jump to 160 through
  114.
* **The ending**: 277 with 690 on, 288, 241 with "To be concluded..." and
  the save question (answered "No"), the fourteen maps of the teaser, and
  the title screen.

Not played: the other two professions, the second month, Paradise burning,
Surl, the refinery, Eisen's simulation and the minigame. The captures are
not goldens: the cartridge was built with patched tools.

## What the static walk does not see

* **Variables and items**: a page that waits for a variable to reach a
  value, or for an item, was taken as reachable. The minigames (the mines,
  the catacombs' pushing, the Advocate's guards, the quarry's count) are
  only known to compile.
* **What a page does once it compiles**: that is the suite and taro.
* **The menus**: a step that only a custom menu or a common event called
  from the menu opens would be missed; none was found.
* **Saving and loading on the way**, which does not keep the events
  ([the save does not keep the
  events](../../../divergences/the-save-does-not-keep-the-events.md)).

## How it was measured

**The path**: throwaway scripts over `data/` —a teleport graph from map 4
(conditions ignored), the autostart pages and the switches set and asked
for, map by map—.

**The whole cartridge**: in a worktree of the ports, one more cartridge in
`rm2k-snes.toml` with every map that graph reaches (307), `start_map = 4`,
and 108's fork set aside. `just cartridges <that one>` stops at each limit
of section 2; each was patched in a worktree of the tools —never
committed— to see the next: 108 in `timer_never_runs_in`; `MESSAGES_STEP` at
eight, with one more shift in `msg_start`; the slot screen's check skipped;
the two `FAR_GROWTH` asserts commented out; and `--msu-everything`. The
bytes asked for, by family, come from a print in the bank packing
(`rm2k-snes/cartridge`), on that cartridge and on `release`. A wrapper of
`rm2k-snes-events` on the PATH kept the request the converter sends, and

    rm2k-snes-events culprits --data <ABL>/data --request compile.json --out <dir>

on it gave section 1's "every page compiles". The stretches of section 4
were a throwaway test with the harness's `suite.session(None, on=<that
cartridge>, msu=True, switches=…)` and `play_case`.
