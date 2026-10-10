# Sunset Over Imdahl

## As of 2026-10-10

> Measured again on 2026-10-10 ([Other games, measured again](../../research/2026-10-10-otros-juegos-de-nuevo.md),
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
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
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
  `ignorar-changesystemgraphics.md`.)
- **Faces and wait escapes**: `\.`, `\!` and `\|` in the middle of a box
  are dropped, as a debt. (Task `las-caras-y-los-escapes-de-espera.md`.)
- **Color codes ignored**, as a debt (`\c[n]`, `\C[n]`, `\s[n]`): map pages
  that compile went from 898 to 1,151 of 1,369. (Task
  `ignorar-los-codigos-de-color.md`.)
- **`ROUTE_GFX_MAX` degrades instead of failing**: Sunset builds without
  exclusions. (Task `degradar-en-vez-de-fallar.md`.)
- **Four shortcuts**: the condition on direction (111 pages). Map pages
  went from 1,151 to 1,266 of 1,369. What kept the routes with orders
  36/37 out wasn't those orders but **the hero's diagonal moves** (orders
  4 to 7), which the compiler rejects on purpose: about 51 pages, the most
  left out after this; and the hero's relative turns (16 to 20) and
  stepping forward (11), about 8. (Task
  `cuatro-atajos-para-los-otros-juegos.md`.)
- **Decorative events as background**: 209 candidates, measured without
  looking at the drawing. (Task `los-eventos-decorativos-como-fondo.md`.)

The tasks named here are in `tasks/testing/` in the-advocate-work.
