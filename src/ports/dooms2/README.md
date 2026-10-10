# Dooms 2

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of snes-rm2k) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `dooms2/` in snes-rm2k-ports, without MSU-1 and without
tests (see [Ports](../README.md)).

## The game

93 maps, in English, with 53 MIDI themes and no `Harmony.dll`. It has
three BMP images and one `PlayMovie`. No DynRPG, no custom fonts, an RM2k
database.

## What the survey found (2026-10-05)

- **Crutches**: its own System reduced to 12 colors, because it doesn't
  fit the window's palette, and the BMPs turned into PNGs (RM2k accepts
  BMP; `rm2k-render` refused it on purpose, for lack of anything to test it
  against), both in a copy of the game.
- **Each map alone**: 89 of the 93 build a cartridge; a theme with more
  than 255 sounds cuts 3, and the names of the menu cut 1, the starting
  one.
- **The cartridge**: starting on map **2**, 86 of the 93; out are 1, 10, 14,
  45, 58, 59 and 63. Map 1, choosing a character, doesn't build: it asks
  for more names than the menu's bank holds. With neighbors, maps 2 and 3
  go over `ROUTE_GFX_MAX`.
- **Boot**: of the maps that build alone, 30 of 89 would need more than
  the 44 frames of `BOOT_FRAMES` if they were the starting map.
- **The pages that compile**: 341 of 496 on the maps, 10 of 10 common
  events, 1 of 82 troop pages. What blocks them: the faces
  (`ChangeFaceGraphic`, 831 uses, which drag along the page's messages),
  `\N[n]` and the escapes `\.`, `\!` and `\|` in the middle of a box,
  `PlayMovie` and `EnterHeroName`.
- **Next to the original**: it starts on map 2 because 1 doesn't build,
  and the title screen is the same as the original. With the survey's four
  recommended fixes, it is one of the three that would have a playable
  cartridge without crutches.
- **Its own**: map 1 could be split by a patch of the game.

## What changed after it (to 2026-10-06)

- **The window with more than 15 colors**: Adeleine reduces it, 18 colors
  down to 15, but the actor choice goes past `$4800`, and its System has 26
  colors in the 8bpp windows of the text screens. (Task
  `la-ventana-con-mas-colores.md`.)
- **Faces and wait escapes**: `ChangeFaceGraphic` is accepted as a debt,
  without drawing the face, and the escapes in the middle of a box are
  dropped. The opening scene of map 2 now runs (Jack's dialogue), **but**
  with more pages compiling the sample directory went over 255 entries
  (263) and the cartridge didn't build: maps 40 to 93 were excluded in the
  project to build it. (Task `las-caras-y-los-escapes-de-espera.md`.)
- **The samples left over don't sound**: past 255 samples the least used
  are left out with a warning. The real cause in Dooms 2 wasn't that —it
  had 247 keys or fewer— but the copies filling the directory; with that
  fixed it builds with maps 40 to 93, starts and shows the dialogue. (Task
  `las-muestras-que-sobran.md`.)
- **Color codes ignored**, as a debt, `\S[n]` among them. (Task
  `ignorar-los-codigos-de-color.md`.)
- **The names that don't fit in the menu's bank**: not done; degrading
  them is deciding what is cut or left out. (Task
  `degradar-en-vez-de-fallar.md`.)
- **BMP images**: the task to read them is open. (Task
  `las-imagenes-en-bmp.md`.)
- **Decorative events as background**: 39 candidates, measured without
  looking at the drawing. (Task `los-eventos-decorativos-como-fondo.md`.)

The tasks named here are in `tasks/testing/` in snes-rm2k-work.
