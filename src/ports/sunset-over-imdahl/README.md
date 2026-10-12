# Sunset Over Imdahl

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **On a painted map, an event "above the hero" is drawn over the roofs.**
  The guard at (13,23) on the square, map 2, shows over the roof that
  should hide him. Draft: [`events-above-the-hero-over-the-painted-roofs`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/events-above-the-hero-over-the-painted-roofs.md).
* **On the square, some roof edges cover too much or too little.** The
  square has more roof edges than the cartridge keeps, and the rest are
  left out. A guard at (36,13) has his legs over a roof's edge, likely
  one of those; not checked. Draft: [`roof-edges-that-dont-fit-in-the-127`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/roof-edges-that-dont-fit-in-the-127.md).
* **Characters are not shaded or lit** by the painted shadows, lights and
  fogs, which only touch the painting.
* **Turning back while walking on a square can drop a frame**, when the
  camera reverses while a row of the painting is still being uploaded.
  Measured, not noticed in play. Draft:
  [`camera-turning-back-over-a-half-uploaded-row-loses-a-frame`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/camera-turning-back-over-a-half-uploaded-row-loses-a-frame.md).
* **The menu and the other screens keep the game's first System.** The
  opening scene (map 11) switches to `SaveMeny`, and only the message
  window follows: the dialogue comes out in its white text, the menu in
  `System`'s white windows. See [What `ChangeSystemGraphics` does not model](../../divergences/what-changesystemgraphics-does-not-model.md).
* **Coloured words in messages come out in the plain colour.** Task:
  [`message-colours-and-speed`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/message-colours-and-speed.md).

## The painted maps, in mode 1 (2026-10-11)

taro, after the captures of the pictures: "it really isn't playable",
and to try mode 1 and colour math. What was measured is in
[Mode 1 for the painted maps](research/2026-10-11-mode-1-for-the-painted-maps.md): the
mosaic of the squares was the tile budget, and twice the tiles did not fix
it —the error per pixel went from 10.5 to 9.4— while one tile per cell
took it to 2.3. So `[graphics] painted_maps = true` in its project: the 60
maps whose panorama is the map go painted —mode 1, the painting in BG1 a
tile per cell, uploaded as the camera moves; see [the VRAM
split](../../internals/vram.md#a-painted-map-keeps-only-what-the-screen-shows)—,
and the roofs' edges go exact in BG2. Colour math did not go in: it does
not reach the characters drawn with object palettes 0 to 3, and there is no
VRAM left for its mask. What stays lost: seven palettes of fifteen colours
per map, and the characters are not shaded.

## The pictures, drawn into the map (2026-10-11)

taro decided its pictures are not left out: "it is a very artistic game;
without those pictures it probably loses all its charm". How the game uses
them, group by group, is [the study](research/2026-10-11-the-pictures-over-the-map.md).
The first version, `[graphics] map_pictures = true` in its project: the
pictures that stay put on a map —roofs and ceilings, lights, shadows and
mists, 183 of them on 64 maps— are drawn into the panorama, and the roofs
go in front of the hero by the priority of the panorama's cells. What it
does not do is in [Pictures drawn into the map](../../divergences/pictures-drawn-into-the-map.md).
The opening scene on 22 runs over the painting, with its mist.

What it shows next to it: **the large maps were already grainy**. The
squares (40x30) and the streets (20x30) carry a painting of 2,000 to 4,800
distinct cells in the panorama's 576 tiles, and the grouping shows —on
the squares the water channel and the pavilion come out broken— with or
without the pictures. That is the panorama's tile budget, not this.

## The opening scene in black (2026-10-11)

After the title, map 11 tints the screen black and jumps to map 22, where
the first scene —the captain and the general looking at the city— runs
from an autorun page (event 1). On the console it stayed black, with or
without the `party = [1]` crutch. Two causes, one behind the other:

- **The page did not compile.** It asks `ChangeScreenTransitions` for the
  cut (19) when showing, which the converter did not take, so the whole
  page was left out and the black tint of map 11 stayed. Fixed: the cut
  for showing compiles and the ROM does it —see
  [The teleport transitions](../../divergences/the-teleport-transitions.md)—.
- **Its mist hides the map.** With the page running, it shows
  `WinterMist`, a 320x240 mist at 100 % transparency that a `MovePicture`
  takes to 95 %, over the panorama. The console carries it as a big
  picture, which goes in place of the map, and its transparency darkens
  towards black: the scene is still black. **Not fixed** that day —it is
  since, see "The pictures, drawn into the map"—: the game draws
  its roofs, ceilings, lights, shadows and mists this way on nearly every
  map —about 140 screen-sized pictures—, and putting them over the map is
  a feature of its own. See
  [What large pictures do not model](../../divergences/what-large-pictures-do-not-model.md).

Measured on a cartridge of maps 11, 22, 21, 23 and 10, with snes9x: taking
the page's `ShowPicture` and `MovePicture` out of the dump by hand, the
scene runs whole —panorama, tint, messages, and the jump to the command
tent on 21—, so nothing else is behind it. The original, under Wine,
shows the panorama in the rain and the mist coming in.

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

- **The cartridge builds with every map**, its own System and the same
  crutch: `party = [1]`; without it, "the party is empty".
- **Each map**, next to the start map: 65 of 65.
- **The pages that compile**: 1,266 of 1,369 on the maps (as on
  2026-10-06), 6 of 8 common events, 0 of 1 troop page. What is left is
  mostly routes —the hero's diagonal moves—, then `FlashSprite` and
  `PanScreen`.
- **It takes hours to build**: 138 big pictures in the background layer,
  minutes each; about 2 h 40 min that day, with other runs on the machine.
- **What degrades**: 43 maps don't draw some of their pictures.

## As of 2026-10-06

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-other-games.md),
> measured on `24e0223e` of the-advocate) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `sunset-over-imdahl/` in the-advocate-ports, without MSU-1 and
without tests (see [Ports](../README.md)).

## The game

65 maps, in English, with 8 MIDI themes and RM2k's own `Harmony.dll`. Its
files are in upper case, and its database has a single item. It starts
with an empty party. No DynRPG, no custom fonts, an RM2k database.

## What the survey found (2026-10-05)

- **Ditto** brings it back byte for byte once it looks for `RPG_RT.LDB`
  without minding the case: a fix of the survey, in its own commit.
- **Each map alone**: all 65 build a cartridge (the `ô` stopped them before
  its fix).
- **The cartridge**: starting on map 11, 60 of the 65 maps; out are 34,
  47, 56, 57 and 63, for `ROUTE_GFX_MAX` (the cap of 8 graphics order 34
  can switch to in one map). It needed a crutch: `party = [1]`, because
  RM2k starts with nobody and no visible hero and the converter asks for a
  leader to draw.
- **The pages that compile**: 896 of 1,369 on the maps, 4 of 8 common
  events, 0 of 1 troop page. What blocks them: the message escapes —`\C[n]`
  (690 boxes with only `\C`), and `\.`, `\!` and `\|` in the middle of a
  box (667 boxes with `\!`)—, `ConditionalBranch` on an event's direction
  (153), and `ChangeSystemGraphics`.
- **Next to the original**: the title screen is the same; the
  introduction, which in the original is pictures fading into each other,
  stays blank with the hero the survey gave it.
- **Fixed in the survey's branch**: an item that isn't in the database
  isn't carried, and a letter the font doesn't have stops the page instead
  of the game. The items the database lacks are an oddity of the game, and
  they no longer stop anything.
- **From outside RM2k**: the `ô`. The console's font is ASCII; a font with
  Latin-1 is drawing work.
- Its System graphic fits the message window.

## What changed after it (to 2026-10-06)

- **`ChangeSystemGraphics` accepted without doing anything**, as a debt:
  the boot event of map 11 now runs (the title fade, and a black screen at
  15 s like the original); at 30 s the original shows a picture and the
  cartridge stays black, which wasn't investigated. (Task
  [`ignore-changesystemgraphics-for-now`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ignore-changesystemgraphics-for-now.md).)
- **Faces and wait escapes**: `\.`, `\!` and `\|` in the middle of a box
  are dropped, as a debt. (Task [`faces-and-wait-escapes-in-messages`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/faces-and-wait-escapes-in-messages.md).)
- **Color codes ignored**, as a debt (`\c[n]`, `\C[n]`, `\s[n]`): map pages
  that compile went from 898 to 1,151 of 1,369. (Task
  [`ignore-the-color-codes-in-messages-for-now`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ignore-the-color-codes-in-messages-for-now.md).)
- **`ROUTE_GFX_MAX` degrades instead of failing**: Sunset builds without
  exclusions. (Task [`degrade-instead-of-failing`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/degrade-instead-of-failing.md).)
- **Four shortcuts**: the condition on direction (111 pages). Map pages
  went from 1,151 to 1,266 of 1,369. What kept the routes with orders
  36/37 out wasn't those orders but **the hero's diagonal moves** (orders
  4 to 7), which the compiler rejects on purpose: about 51 pages, the most
  left out after this; and the hero's relative turns (16 to 20) and
  stepping forward (11), about 8. (Task
  [`four-shortcuts-for-the-other-games`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/four-shortcuts-for-the-other-games.md).)
- **Decorative events as background**: 209 candidates, measured without
  looking at the drawing. (Task [`decorative-events-into-the-background`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/decorative-events-into-the-background.md).)

The tasks named here are in `tasks/testing/` in the-advocate-work.
