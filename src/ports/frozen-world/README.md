# The Frozen World

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of snes-rm2k) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `frozen-world/` in snes-rm2k-ports, without MSU-1 and
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
  `el-nombre-del-heroe-en-los-mensajes.md`.)
- **The window with more than 15 colors**: Adeleine reduces it, 16 colors
  down to 15, but then the message window asks for 266 tiles of 256, and
  its System has 17 colors in the 8bpp windows of the text screens. (Task
  `la-ventana-con-mas-colores.md`.)
- **Choosing another System from the project**: built with the original
  game and `system = "ablskin.png"` (A Blurred Line's System), it starts.
  (Task `elegir-otro-system.md`.)
- **The title that doesn't fit**: the converter starts without a title
  screen, with a warning, instead of stopping; it builds without
  `--no-title`. (Task `degradar-en-vez-de-fallar.md`.)
- **Decorative events as background**: 117 candidates, measured without
  looking at the drawing. (Task `los-eventos-decorativos-como-fondo.md`.)

The tasks named here are in `tasks/testing/` in snes-rm2k-work.
