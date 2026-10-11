# El Dorado

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **The screen is not blanked where the original goes black**: on eleven
  maps a page erases and shows the screen, and the cartridge leaves the
  map in sight. Task: `todo/eraseScreen-y-showscreen`.

## As of 2026-10-10

> Measured again on 2026-10-10 ([Other games, measured again](../../research/2026-10-10-otros-juegos-de-nuevo.md),
> with the tools of the-advocate `1afe6457` and the ports at `951471f`),
> without fixing anything. What follows the next heading is the snapshot
> of 2026-10-06, kept as it was.

- **The cartridge builds with every map and no crutch**: its own System,
  no exclusions. As committed it is the same.
- **Each map**, next to the start map: 13 of 13 (9 of 13 on 2026-10-05).
- **The pages that compile**: 966 of 972 on the maps, 10 of 10 common
  events, 0 of 80 troop pages (all with a condition the ROM doesn't check).
  What is left on the maps is six pages, one command each.
- **What degrades**: the route graphics table of 8 is full in all 13 maps,
  and 13 maps don't draw some of their pictures.
- Boot: 19 of the 44 frames.

## As of 2026-10-06

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of the-advocate) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `el-dorado/` in the-advocate-ports, without MSU-1 and without
tests (see [Ports](../README.md)).

## The game

13 maps, in German, with 3 MIDI themes. It ships Ineluki's Harmony patch
v1.2 with key support ("mit KeySupport"), but it has no `.script` file: it
doesn't use it. No DynRPG, no custom fonts, an RM2k database.

## What the survey found (2026-10-05)

- **Each map alone**: 9 of the 13 build a cartridge; the other 4 are cut by
  `ROUTE_GFX_MAX`, the cap of 8 graphics that order 34 of a move route can
  switch to in one map. Map 8 builds alone but not with the others.
- **The cartridge**: starting on map 8, 8 of the 13 maps; out are 4, 5, 6,
  11 and 12, for `ROUTE_GFX_MAX` (with 12 in, map 8 also goes over 8).
- **Boot**: of the maps that build alone, 7 of 9 would need more than the
  44 frames of `BOOT_FRAMES` to upload their audio package if they were the
  starting map.
- **The pages that compile**: 698 of 972 on the maps, 9 of 10 common
  events, 0 of 80 troop pages. What blocks them: `ConditionalBranch` on an
  event's direction (176), `EraseScreen` and `ShowScreen` (270, always with
  `PlayerVisibility`), `EraseEvent` (3), and troop pages with conditions
  the ROM doesn't check.
- **Next to the original**: the title screen is the same; map 8, choosing
  the difficulty, is shown without its two signs —they are pictures, and
  the map has no sprite palettes left for them: the converter warns about
  it—.
- **Its own**: the signs of map 8 could become map tiles instead of
  pictures, as a patch of the game. And the German text: the console's
  font is ASCII; a font with Latin-1 is drawing work.
- Its System graphic fits the message window.

## What changed after it (to 2026-10-06)

- **`ROUTE_GFX_MAX` degrades instead of failing**: the order 34 graphics
  that don't fit are ignored with a warning. El Dorado builds without
  exclusions. (Task `degradar-en-vez-de-fallar.md`.)
- **`EraseEvent` for real**: its three pages that were out only for that
  now compile. (Task `eraseevent-de-verdad.md`.)
- **Four shortcuts**: the condition on direction (23 pages), moving away
  from the hero (order 10, 9 pages) and `PlayerVisibility` (170 pages).
  Map pages that compile went from 710 to 963 of 972, and common events
  from 9 to 10 of 10. With all that El Dorado stopped building: map 7
  asked for nine substituted blocks and the table held eight, so
  `SUB_MAX` went from 8 to 16. (Task
  `cuatro-atajos-para-los-otros-juegos.md`.)
- **Decorative events as background**: 26 candidates, measured without
  looking at the drawing. (Task `los-eventos-decorativos-como-fondo.md`.)

The tasks named here are in `tasks/testing/` in the-advocate-work.
