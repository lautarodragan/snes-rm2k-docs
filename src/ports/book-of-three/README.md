# The Book of Three

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **A skill that turns a switch on, used from the pause menu, is
  silent**: the original plays its sound effect. Draft:
  [`switch-skills-from-the-menu-play-no-sound`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/switch-skills-from-the-menu-play-no-sound.md).
* **Gwydion's Blazing Star and Dyrnwyn are not drawn**, in the fights
  against the three Cauldron-Born (map 26) and the Horned King (map 78),
  and neither is Taran's Last Stand: the battle pauses for as long as the
  animation would last, and then the page goes on as in the original. See
  [What troop pages do not model](../../divergences/what-troop-pages-do-not-model.md).
* **Part of the lava tunnels' animation stands still** (map 46): it does
  not fit in WRAM. See
  [A ChipSet animation that does not fit in WRAM](../../divergences/a-chipset-animation-that-does-not-fit-in-wram.md).

Found on 2026-10-15 by comparing the port with the original, played to the
end under Wine (see "Its walkthrough"):

* **One horseman fewer in Yern's woods** (map 16): the procession that
  rides through the scene inside the horsemen's battle has four riders,
  not five. Its troop has nine members and a battle holds eight, so the
  converter leaves out one the scene only shows and takes away; the one
  that stays to be fought is there, and the battle plays to its end. See
  [A battle holds eight enemies](../../divergences/a-battle-holds-eight-enemies.md).
* **Characters that walk into a scene are missing**: whoever a scene places
  and dresses with a move route, on an event with no graphic of its own,
  is never drawn, though their lines and moves go on. It shows around
  Gurgi (map 21), at the river (22), before the ambush (26), in the cell
  (32), at the way out of the Tylwyth Teg (83) and on about ten more maps.
  Draft:
  [`characters-a-route-gives-a-graphic-are-not-drawn`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/characters-a-route-gives-a-graphic-are-not-drawn.md).
* **The story's battles all play the default battle theme**: the original
  sets each scripted fight's own music and victory music. Draft:
  [`book-of-three-story-battles-play-the-default-theme`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-story-battles-play-the-default-theme.md).
* **Fades are cuts**: where a scene fades the screen to black, to night or
  back to day, the port jumps to the end of the fade and waits its time.
  Draft:
  [`tint-screen-snaps-instead-of-fading`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/tint-screen-snaps-instead-of-fading.md).
* **A night's rest has no fade or jingle**, in scenes and at the free
  resting places: the party is healed at once. Draft:
  [`book-of-three-inns-in-scenes-are-not-staged`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-inns-in-scenes-are-not-staged.md).
* **The closing pictures are not drawn** (maps 69 and 72): those moments of
  the ending are a plain or black screen for as long as they last. Draft:
  [`book-of-three-the-last-pictures-are-not-drawn`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-the-last-pictures-are-not-drawn.md).
* **Looking at the map shows nothing**: its sound plays and it waits for a
  key, over the screen as it was. Draft:
  [`book-of-three-the-map-item-shows-nothing`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-the-map-item-shows-nothing.md).
* **The opening's flames stand still** (map 3). Draft:
  [`book-of-three-the-intros-torches-stand-still`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-the-intros-torches-stand-still.md).
* **Some places' music plays louder than in the original**: the South
  Mountains and the northern map ask for their song at 70%, the hills and
  the Eagle Mountains at 50%, and the port plays it at full volume. Draft:
  [`a-maps-own-music-ignores-its-volume-and-tempo`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-maps-own-music-ignores-its-volume-and-tempo.md).
* **One song starts at full volume** instead of fading in (map 21). Draft:
  [`playbgm-fade-in-is-dropped`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/playbgm-fade-in-is-dropped.md).

## Its walkthrough

`tests/test_book_of_three.py`, at the root of the-advocate-ports, plays
the game from the start: Caer Dallben, Coll's forge and its fire —the
sword, the practice battle, Coll and Dallben—, Dallben's cottage, the
Book of Three, Hen Wen's escape, Caer Minule and its item shop, and Yern's
woods through the horsemen's battle, with a golden at each milestone, in snes9x and
bsnes against the same one. It runs with `just boot`. It was born on
2026-10-12, when taro played up to the forge and found the game stuck
there: the fire's page puts a weapon on Taran, which did not compile
([the task](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-the-forge-and-a-walkthrough.md)).
The goldens up to the forge are what taro played.

The rest of the game, to its end, is `tests/test_book_of_three_milestones.py`:
twenty milestones, each started from a case —the switches, party and level
a player has at that point, and a teleport to where its scene starts— and
then played with A taps until control comes back. The same cases started
the original under Wine, and on 2026-10-15 every milestone was compared by
eye with it, as were the walkthrough's goldens after the forge
([the task](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-against-the-original.md)).
What the cases jump over is not played: the walks between milestones
—the overworld, the dungeons, Spiral Castle's halls, the Tylwyth Teg's
maze— and the optional places.

## What it leaves out (2026-10-11)

No map: the whole release builds. Maps 44, 69 and 74, which the survey left
out, build now, and map 46 came back on 2026-10-10 with part of its tile
animation standing still.

Since later on 2026-10-11 it builds with its own System, Royal: its
gradient is fused where the banks don't hold it —[A window with a gradient
is fused until it fits](../../optimizations/a-window-with-a-gradient.md)—, with a warning for the message window,
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
