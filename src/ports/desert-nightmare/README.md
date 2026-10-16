# Desert Nightmare

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **Coloured words in messages come out in the plain colour**: the console
  drops RM2k's `\c[n]`. Task: [`message-colours-and-speed`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/message-colours-and-speed.md);
  see [What message escapes do not model](../../divergences/what-message-escapes-do-not-model.md).
* **The start menu ("With Intro / No Intro / Quit") shows over a pattern of
  garbage** instead of the burning face behind it. Draft:
  [`desert-nightmare-start-menu-over-garbage`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/desert-nightmare-start-menu-over-garbage.md).
* **The hero walks through some walls.** On eight maps —2, 4, 5, 14, 61,
  62, 66 and 172— more events than the console holds are left out, and
  among them are invisible walls. Draft: [`invisible-walls-lost-when-trimming-events`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/invisible-walls-lost-when-trimming-events.md).
* **In the gas station's toilet (map 7) the room goes dark for about eight
  seconds**: a light mask that the original lays over the room at 35 %
  replaces the map. Seen on 2026-10-06, not checked since. Draft:
  [`pictures-that-go-over-the-map-outside-sunset`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/pictures-that-go-over-the-map-outside-sunset.md).
* **The menu and the other screens keep the intro's System** for the whole
  game: the original switches to `Systemset_Spiel` in its common event
  `Init`, and only the message window follows. See [What `ChangeSystemGraphics` does not model](../../divergences/what-changesystemgraphics-does-not-model.md).
* **Messages show no faces, and coloured words come out in the plain
  colour.** Tasks: [`draw-the-faces`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/draw-the-faces.md)
  and [`message-colours-and-speed`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/message-colours-and-speed.md).

## What it leaves out (2026-10-11)

No map: the whole release builds. What stopped twelve maps on 2026-10-10
degrades now, with a warning: past 120 events the ones left out lose only
their looks or an invisible wall, past 104 drawn events the rest aren't
drawn and still run, and the panoramas are drawn flattened or in mode 1. None of those
maps was looked at in an emulator.

Since later on 2026-10-11 it builds with its own System: End Game's
colours are merged until its pairs fit the palette —[A window with a
gradient is fused until it fits](../../optimizations/lossy/tiles/a-window-with-a-gradient.md)—.

## The empty party (2026-10-10)

The `party = [1]` crutch is gone: the game starts with the party its
database gives, which is nobody, as in RM2k. The hero isn't drawn until
someone joins, and still walks, collides and touches events; the pause
menu grays Items and Equipment while the party is empty. Built without
the crutch, the whole release builds.

## As of 2026-10-10

> Measured again on 2026-10-10 ([Other games, measured again](../../research/2026-10-10-other-games-measured-again.md),
> with the tools of the-advocate `1afe6457` and the ports at `951471f`),
> without fixing anything. What follows the next heading is the snapshot
> of 2026-10-06, kept as it was.

- **The cartridge builds** with A Blurred Line's System and
  `party = [1]`. With its own System, "the End Game screen uses 18 pairs of
  colours and a 4bpp palette has 16"; with an empty party, "the party is
  empty".
- **It needs twelve maps out, not twenty-four**: the six panoramas without
  a VRAM layout, the three with more than 104 NPCs, the two with more than
  120 events and map 182's tile animation. The committed project still
  leaves out the survey's twenty-four.
- **Each map**, next to the start map: 177 of 189, the same twelve.
- **The pages that compile**: 7,277 of 7,340 on the maps (7,150 on
  2026-10-06), 28 of 30 common events, 0 of 100 troop pages. What is left
  is mostly `ControlVars` reading an event's screen position.
- **What degrades**: 136 maps don't draw some of their pictures.

## As of 2026-10-06

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-other-games.md),
> measured on `24e0223e` of the-advocate) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `desert-nightmare/` in the-advocate-ports, without MSU-1 and
without tests (see [Ports](../README.md)).

## The game

189 maps, in English. It has no battles, and it starts with an empty
party. Its music is MP3, through Ineluki's Harmony patch v1.1.1 with
links: fifteen text `.link.wav` files (`..\mp3\Credits.mp3` and `loop`)
that its Harmony turns into an MP3 track. The port doesn't read them:
those themes don't play. It is the only thing from outside RM2k that
changes what is heard, and the MSU-1 would be the natural way to carry it;
without MSU-1, it would take getting a MIDI or silencing them. No DynRPG,
no custom fonts, an RM2k database.

## What the survey found (2026-10-05)

- **Crutches**: the RTP's System reduced to 12 colors, in a copy of the
  game, because its own didn't fit even reduced; `party = [1]`, because
  RM2k starts with nobody and no visible hero and the converter asks for a
  leader to draw; and no title screen, because its title doesn't fit in
  VRAM next to the menu.
- **Each map alone**: 177 of the 189 build a cartridge; panoramas with no
  VRAM layout cut 6, more than 104 NPCs in OAM cut 3, more than 120 events
  cut 2, and the tile animation in WRAM cuts 1.
- **The cartridge**: starting on map 1, 165 of the 189; out are 24: the
  ones of the sweep, and twelve more for `ROUTE_GFX_MAX` with neighbors.
- **The pages that compile**: 5,190 of 7,340 on the maps, 24 of 30 common
  events, 0 of 100 troop pages. What blocks them: `\C[n]` (2,144 boxes),
  the faces (2,049 uses of `ChangeFaceGraphic`), `ConditionalBranch` on an
  event's direction (354), `EraseScreen`/`ShowScreen` (698), `EraseEvent`
  (157 pages, 127 of them only for that), `ChangeSystemGraphics` and
  `InputNumber` with a variable.
- **Next to the original**: the picture menu ("With Intro / No Intro /
  Quit") comes out right, but **the background, a panorama in mode 3, is
  light-blue garbage**. It was a bug of the panoramas, merged that same
  day, in no golden because A Blurred Line has no such panorama; the
  survey put it first, before anything else.
- **Fixed in the survey's branch**: the fallback battle backdrop is asked
  for only if some battle needs it.

## What changed after it (to 2026-10-06)

- **The window**: its System's 15 colors fit; what stopped it was End
  Game, another limit. (Task [`window-with-more-than-15-colors`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/window-with-more-than-15-colors.md).)
- **Choosing another System from the project**: built with the original
  game and `system = "ablskin.png"` (A Blurred Line's System), it starts.
  (Task [`choose-another-system-from-the-project`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/choose-another-system-from-the-project.md).)
- **Color codes ignored**, as a debt (`\c[1]Sandra: \c[0]` in almost every
  message, 1,345 pages out): map pages that compile went from 5,738 to
  7,034 of 7,340. (Task [`ignore-the-color-codes-in-messages-for-now`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ignore-the-color-codes-in-messages-for-now.md).)
- **`EraseEvent` for real**: it was what kept the most pages out alone, and
  it no longer does; the 157 are parallel pages without a graphic. It was
  suspected of freezing the intro, and it wasn't that: the intro ends in
  black on the street (map 9) because its last page teleports to map 2,
  which the survey left out. What did change is the WC scene (map 7): a
  picture that RM2k shows as a dark mask at 35 % comes out opaque and
  covers the room for ~480 frames —it looks frozen, but it goes on—. That
  is the pictures' translucency, not the erasing. (Task
  [`eraseevent-for-real`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/eraseevent-for-real.md).)
- **`EraseScreen`/`ShowScreen` accepted without doing anything**, as a
  debt: the map stays visible where the original goes black, and the start
  menu comes out over VRAM garbage. The title that doesn't fit now
  degrades: it builds without `--no-title`. The survey's exclusions stay:
  it wasn't tested which depended on `EraseScreen`. (Task
  [`degrade-instead-of-failing`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/degrade-instead-of-failing.md).)
- **Four shortcuts**: the condition on direction (21 pages) and the random
  step (order 8, 39 pages). Map pages went from 7,034 to 7,150 of 7,340.
  (Task [`four-shortcuts-for-the-other-games`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/four-shortcuts-for-the-other-games.md).)
- **Decorative events as background**: 2,887 candidates, measured without
  looking at the drawing. (Task [`decorative-events-into-the-background`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/decorative-events-into-the-background.md).)
- **A ChipSet animation that doesn't fit in WRAM** (2026-10-10) keeps the
  tiles that cover the most cells moving and leaves the rest still: in map
  182, 9 of its 51 water tiles (44 of 1,469 cells). The map is back in the
  cartridge, which builds whole. (Task
  [`tile-animations-that-dont-fit-in-wram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/tile-animations-that-dont-fit-in-wram.md).)

The tasks named here are in `tasks/testing/` in the-advocate-work.
