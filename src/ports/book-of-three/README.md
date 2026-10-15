# The Book of Three

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **A skill that turns a switch on, used from the pause menu, is
  silent**: the original plays its sound effect. Draft:
  [`switch-skills-from-the-menu-play-no-sound`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/switch-skills-from-the-menu-play-no-sound.md).
* **Two of its parallel common events never run**: `Reraise KO'd chars`
  and `Eilonwy's Upgrades` do not compile. What that loses in play was not
  looked at. Draft:
  [`book-of-three-reraise-and-eilonwy-dont-compile`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-reraise-and-eilonwy-dont-compile.md).
* **Taran's Cash Reward does nothing in battle**: the page it runs, in
  52 of the troops, does not compile. Draft:
  [`controlvars-multiply-and-divide`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/controlvars-multiply-and-divide.md).
* **Gwydion's Blazing Star and Dyrnwyn are not drawn**, in the fights
  against the three Cauldron-Born (map 26) and the Horned King (map 78),
  and neither is Taran's Last Stand: the battle pauses for as long as the
  animation would last, and then the page goes on as in the original. See
  [What troop pages do not model](../../divergences/what-troop-pages-do-not-model.md).

## Its walkthrough

`tests/test_book_of_three.py`, at the root of the-advocate-ports, plays
the game from the start: Caer Dallben, Coll's forge and its fire —the
sword, the practice battle, Coll and Dallben—, Dallben's cottage and the
Book of Three, with a golden at each milestone, in snes9x and bsnes
against the same one. It runs with `just boot`. It was born on
2026-10-12, when taro played up to the forge and found the game stuck
there: the fire's page puts a weapon on Taran, which did not compile
([the task](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-the-forge-and-a-walkthrough.md)).
The goldens up to the forge are what taro played; the ones after it were
not compared against RM2k.

## What it leaves out (2026-10-11)

No map: the whole release builds. Maps 44, 69 and 74, which the survey left
out, build now, and map 46 came back on 2026-10-10 with part of its tile
animation standing still.

Since later on 2026-10-11 it builds with its own System, Royal: its
gradient is fused where the banks don't hold it —[A window with a gradient
is fused until it fits](../../decisions/a-window-with-a-gradient-is-fused-until-it-fits.md)—, with a warning for the message window,
the actor choice, the item and equipment screens and the shop.
Since 2026-10-12 Royal's windows are drawn over the average colour of its
gradient —[The windows' background is the project's, by System](../../decisions/the-windows-background-is-the-projects-by-system.md)—, until the runtime draws the gradient: Royal's dither
is lost, and of the fused screens only the actor choice still is, by one
tile, and End Game's colours.

## As of 2026-10-10

> Measured again on 2026-10-10 ([Other games, measured again](../../research/2026-10-10-other-games-measured-again.md),
> with the tools of the-advocate `1afe6457` and the ports at `951471f`),
> without fixing anything. What follows the next heading is the snapshot
> of 2026-10-06, kept as it was.

- **The cartridge builds** with A Blurred Line's System; with its own,
  "the window needs 267 tiles —27 of its frame and its arrow— and the bank
  has 256", as on 2026-10-06.
- **It only needs map 46 out** (its tile animation is 10,432 bytes of the
  8,192 reserved in WRAM); the committed project still leaves out 44, 69 and
  74 too, which build now.
- **Each map**, next to the start map: 88 of 89 (85 on 2026-10-05).
- **The pages that compile**: 1,271 of 1,282 on the maps, 19 of 25 common
  events, 359 of 746 troop pages, unchanged since 2026-10-06. In the troops,
  `ChangeMonsterCondition`, `ControlVars`, `ChangeItems` and
  `TerminateBattle`.
- Boot: 35 of the 44 frames.

## As of 2026-10-06

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-other-games.md),
> measured on `24e0223e` of the-advocate) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `book-of-three/` in the-advocate-ports, without MSU-1 and
without tests (see [Ports](../README.md)).

## The game

89 maps, in English, with 67 MIDI themes and no `Harmony.dll`. Its System
graphic comes from the RTP, and its hero is invisible. No DynRPG, no
custom fonts, an RM2k database.

## What the survey found (2026-10-05)

- **The window**: its System doesn't fit the message window's 15-color
  palette, not even reduced, so the survey built it with the RTP's System
  reduced to 12 colors, in a copy of the game. Besides the colors, the
  frame with a stretched background asks for more tiles than the bank has
  (259-261 of 256).
- **Each map alone**: 85 of the 89 build a cartridge; the window doesn't
  fit in VRAM in 3, and the tile animation doesn't fit in WRAM in 1.
- **The cartridge**: starting on map 1, 85 of the 89; out are 44, 46, 69
  and 74, the ones of the sweep.
- **The pages that compile**: 1,271 of 1,282 on the maps, 19 of 25 common
  events, 206 of 746 troop pages. Almost all troop pages have a condition
  the ROM doesn't check —turns, an enemy's HP—, and here also
  `ChangeMonsterCondition`, `TerminateBattle` and the comments. On the
  maps, `ChangeEquipment`.
- **Next to the original**: the beginning is the same, frame by frame,
  except for the color of the text (the reduced System). With the survey's
  four recommended fixes, it is one of the three that would have a
  playable cartridge without crutches.
- **Fixed in the survey's branch**: the System, the faces, the title and
  the pictures can also come from the RTP, in any case; a leader without a
  CharSet is a leader without a graphic.

## What changed after it (to 2026-10-06)

- **The window with more than 15 colors**: Adeleine reduces it instead of
  stopping, 23 colors down to 15, but the stretched frame still doesn't fit
  the tile bank (267 of 256): it doesn't start with its original System
  yet. (Task [`window-with-more-than-15-colors`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/window-with-more-than-15-colors.md).)
- **Choosing another System from the project**: the `[graphics] system`
  knob. Built with the original game and `system = "ablskin.png"` (A
  Blurred Line's System), it starts. (Task [`choose-another-system-from-the-project`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/choose-another-system-from-the-project.md).)
- **Four shortcuts**: `Comment` in troop pages is ignored as on the maps;
  troop pages that compile went from 206 to 359 of 746. (Task
  [`four-shortcuts-for-the-other-games`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/four-shortcuts-for-the-other-games.md).)
- **Decorative events as background**: 87 candidates, measured without
  looking at the drawing. (Task [`decorative-events-into-the-background`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/decorative-events-into-the-background.md).)
- **A ChipSet animation that doesn't fit in WRAM** (2026-10-10) keeps the
  tiles that cover the most cells moving and leaves the rest still: in map
  46, 9 of its 25 water tiles (25 of 115 cells) and 2 of its 22 animated
  ones (2 of 2,185). The map is back in the cartridge, which builds whole.
  (Task [`tile-animations-that-dont-fit-in-wram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/tile-animations-that-dont-fit-in-wram.md).)

The tasks named here are in `tasks/testing/` in the-advocate-work.
