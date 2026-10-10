# The Book of Three

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of snes-rm2k) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `book-of-three/` in snes-rm2k-ports, without MSU-1 and
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
  yet. (Task `la-ventana-con-mas-colores.md`.)
- **Choosing another System from the project**: the `[graphics] system`
  knob. Built with the original game and `system = "ablskin.png"` (A
  Blurred Line's System), it starts. (Task `elegir-otro-system.md`.)
- **Four shortcuts**: `Comment` in troop pages is ignored as on the maps;
  troop pages that compile went from 206 to 359 of 746. (Task
  `cuatro-atajos-para-los-otros-juegos.md`.)
- **Decorative events as background**: 87 candidates, measured without
  looking at the drawing. (Task `los-eventos-decorativos-como-fondo.md`.)

The tasks named here are in `tasks/testing/` in snes-rm2k-work.
