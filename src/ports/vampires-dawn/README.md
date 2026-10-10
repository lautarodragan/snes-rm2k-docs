# Vampires Dawn

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of snes-rm2k) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `vampires-dawn/` in snes-rm2k-ports, without MSU-1 and
without tests (see [Ports](../README.md)). **As of 2026-10-06 it doesn't
build a cartridge.**

## The game

440 maps, in English, with 274 MIDI themes and RM2k's own `Harmony.dll`.
It comes in a nested folder, with its installer. No DynRPG, no custom
fonts, an RM2k database.

## What the survey found (2026-10-05)

- **It builds no cartridge**: it uses more variables than the engine's
  256. The compilation of its pages stops there, so their count doesn't
  get measured.
- **Each map alone**: 0 of the 440: more than 256 variables (290 + 92), the
  window (19), OAM (19), battle animations (7), more than 120 events (7).
- **The window**: its System isn't in the game's copy; the survey used the
  RTP's, reduced.
- **The recommendation** put it last: it asks for redoing how the
  variables live —256 one-byte slots and 512 bytes of far RAM— for a
  single game.

## What changed after it (to 2026-10-06)

- **More than 256 variables degrade**: the ones without a slot leave the
  list with a warning, and the pages and events that use them stay out.
  Vampires Dawn gets past this (it names 600 variables). It still doesn't
  build, for other limits: maps with a panorama that doesn't fit, battle
  animations without room in the sprite bank (twenty-five excluded and
  more keep appearing) and the message window, which asks for 262 tiles
  against 256. (Task `degradar-en-vez-de-fallar.md`.)
- **Map 1 without its animation box**: a map whose battle animation box
  doesn't fit in any VRAM layout is converted without it, with a warning.
  But that wasn't what stopped map 1: it is 300x300 and its background has
  597 unique 8x8 tiles, against the 544 of the biggest layout. (Task
  `el-mapa-1-de-vampires-dawn.md`.)
- **Fusing similar tiles**: 18 maps go over the ~544 background tiles (the
  biggest, Uruya, 817; the world, 597). With the fusion the background no
  longer blocks any of them, but what cuts is the sprite bank and the
  layer above —maps 15, 57, 95, 99, 150, 165 (Uruya), 225 and 399—, the
  mode 1 panels of maps 28, 402 and 403, and then the encounters. (Task
  `fusionar-tiles-parecidos.md`.)
- **Encounters with two-byte indices**: it has 779 troops and 136 zones,
  which didn't fit one-byte tables. With that the battle conversion passes
  (with maps excluded); next come the maps with more than 104 NPCs in OAM,
  and then map 1: "a stream of anim_tiles is 27264 bytes and 8192 fit in
  WRAM". (Task `los-encuentros-en-dos-bytes.md`.)
- **Uruya in 4bpp**, a throwaway experiment: map 165 alone, in mode 1 with
  both layers at 4bpp, fits in VRAM with room to spare (878 tiles); with
  Adeleine's palettes it keeps 19 distinct colors, with clustering by
  tile 73. (Task `uruya-en-4bpp.md`.)
- **Decorative events as background**: in map 95 (Weg), 209 translucent
  `water1` events paint a river and took the whole sprite bank; baked into
  the background, with a knob. 5,483 candidates in the game, measured
  without looking at the drawing. (Task
  `los-eventos-decorativos-como-fondo.md`.)
- **Four shortcuts**: the condition on direction (37 pages) and the random
  step and moving away from the hero (16 and 48). Map pages that compile,
  from a scan and not a cartridge, went from 21,214 to 21,272 of 22,977;
  what is left in `MoveEvent` is the hero's diagonal moves, about 45
  pages. (Task `cuatro-atajos-para-los-otros-juegos.md`.)
- **Parallel common events** don't run in the engine: Vampires Dawn has 35.
  (Task `el-tablero-contra-rm2k.md`.)

The tasks named here are in `tasks/testing/` in snes-rm2k-work.
