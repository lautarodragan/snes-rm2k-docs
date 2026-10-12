# The Frozen World

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **Maps 1 ("Battle Screen") and 2 ("Plate Placement") are not in the
  cartridge**, and an event page that would take the hero to one of them
  is left out whole. What of the game that loses was not looked at.
  Drafts: [`flashing-hero-shares-a-palette-with-an-npc`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/flashing-hero-shares-a-palette-with-an-npc.md) (map 1) and
  [`map-streams-that-dont-fit-in-wram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/map-streams-that-dont-fit-in-wram.md) (map 2).

## What it leaves out (2026-10-11)

Two maps, and the project now takes every map of the game:

- **1**: "a page makes the hero flash, and actor 11 is drawn with
  rangedmelee[0], which an NPC of the map also uses. On the console they
  share a palette and both would flash".
- **2**: "a stream of map_code is 38179 bytes and 19968 fit in WRAM".

The cap on the maps (`below`), which the survey set because the sample
directory went past 255, is gone: that limit degrades now. Since later
on 2026-10-11 it builds with its own System, `thunter`: its gradient is
fused where the banks don't hold it —[A window with a gradient is fused
until it fits](../../decisions/una-ventana-con-degrade-se-funde-hasta-que-entra.md)—.
Since 2026-10-12 `thunter`'s windows are drawn over the average colour of
its gradient —[The windows' background is the project's, by System](../../decisions/the-windows-background-is-the-projects-by-system.md)—, until the runtime draws the gradient, and none of
its screens is fused any more.

## As of 2026-10-10

> Measured again on 2026-10-10 ([Other games, measured again](../../research/2026-10-10-otros-juegos-de-nuevo.md),
> with the tools of the-advocate `1afe6457` and the ports at `951471f`),
> without fixing anything. What follows the next heading is the snapshot
> of 2026-10-06, kept as it was.

- **The cartridge builds** with A Blurred Line's System; with its own,
  "the window needs 266 tiles of 256", as on 2026-10-06. It starts without
  a title screen: the title doesn't fit in VRAM, and that only warns.
- **It only needs maps 1 and 2 out**: map 2's code is 38,179 bytes and
  19,968 fit in WRAM; map 1 asks for 1.8 MB of code alone, and with the
  others, its hero flash shares a palette with an NPC. The committed
  project still leaves out 69 and 84 too, which build now.
- **Each map**, next to the start map: 153 of 155.
- **The pages that compile**: 3,819 of 3,891 on the maps (3,554 on
  2026-10-05), 88 of 100 common events, 0 of 80 troop pages. What is left:
  messages, `ChangeMapTileset`, `ShowChoice`, and switches past 1,024.

## As of 2026-10-06

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of the-advocate) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `frozen-world/` in the-advocate-ports, without MSU-1 and
without tests (see [Ports](../README.md)).

## The game

155 maps, in English, with 73 MIDI themes and no `Harmony.dll`. It uses
500 variables and 1,500 switches. No DynRPG, no custom fonts, an RM2k
database.

## What the survey found (2026-10-05)

- **Crutches**: its own System reduced to 12 colors, because it doesn't
  fit the window's palette, in a copy of the game; and no title screen,
  because its title —a photographic picture, 800 unique tiles at 8bpp—
  doesn't fit in VRAM next to the menu.
- **Each map alone**: 151 of the 155 build a cartridge; the window doesn't
  fit in 2, the map's code doesn't fit in WRAM in 1, and `ROUTE_GFX_MAX`
  cuts 1.
- **The cartridge**: starting on map 7, 130 of the 155; out are those with
  id 135 or more, and 1, 2, 69 and 84: with more maps the sample directory
  goes over 255 entries (`SRCN` is one byte).
- **Boot**: of the maps that build alone, 126 of 151 would need more than
  the 44 frames of `BOOT_FRAMES` if they were the starting map.
- **The pages that compile**: 3,554 of 3,891 on the maps, 88 of 100 common
  events, 0 of 80 troop pages. Almost everything that doesn't compile is
  `\N[n]` (an actor's name) in the messages, 696 boxes; also
  `ChangeMapTileset` (8 pages) and `InputNumber` with a variable.
- **Next to the original**: the beginning is the same, frame by frame,
  except for the color of the text (the reduced System); without a title
  screen it goes straight into the wizard's scene. With the survey's four
  recommended fixes, it is one of the three that would have a playable
  cartridge without crutches.

## What changed after it (to 2026-10-06)

- **`\N[n]` in the messages**: the actor's name from the database is baked
  into the text when no `ChangeHeroName` can change it. Rebuilt, Frozen
  World gets past the black screen and shows the DARK WIZARD. (Task
  [`n-n-in-messages`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/n-n-in-messages.md).)
- **The window with more than 15 colors**: Adeleine reduces it, 16 colors
  down to 15, but then the message window asks for 266 tiles of 256, and
  its System has 17 colors in the 8bpp windows of the text screens. (Task
  [`window-with-more-than-15-colors`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/window-with-more-than-15-colors.md).)
- **Choosing another System from the project**: built with the original
  game and `system = "ablskin.png"` (A Blurred Line's System), it starts.
  (Task [`choose-another-system-from-the-project`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/choose-another-system-from-the-project.md).)
- **The title that doesn't fit**: the converter starts without a title
  screen, with a warning, instead of stopping; it builds without
  `--no-title`. (Task [`degrade-instead-of-failing`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/degrade-instead-of-failing.md).)
- **Decorative events as background**: 117 candidates, measured without
  looking at the drawing. (Task [`decorative-events-into-the-background`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/decorative-events-into-the-background.md).)

The tasks named here are in `tasks/testing/` in the-advocate-work.
