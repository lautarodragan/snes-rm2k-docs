# Desert Nightmare

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-otros-juegos.md),
> measured on `24e0223e` of snes-rm2k) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `desert-nightmare/` in snes-rm2k-ports, without MSU-1 and
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
  Game, another limit. (Task `la-ventana-con-mas-colores.md`.)
- **Choosing another System from the project**: built with the original
  game and `system = "ablskin.png"` (A Blurred Line's System), it starts.
  (Task `elegir-otro-system.md`.)
- **Color codes ignored**, as a debt (`\c[1]Sandra: \c[0]` in almost every
  message, 1,345 pages out): map pages that compile went from 5,738 to
  7,034 of 7,340. (Task `ignorar-los-codigos-de-color.md`.)
- **`EraseEvent` for real**: it was what kept the most pages out alone, and
  it no longer does; the 157 are parallel pages without a graphic. It was
  suspected of freezing the intro, and it wasn't that: the intro ends in
  black on the street (map 9) because its last page teleports to map 2,
  which the survey left out. What did change is the WC scene (map 7): a
  picture that RM2k shows as a dark mask at 35 % comes out opaque and
  covers the room for ~480 frames —it looks frozen, but it goes on—. That
  is the pictures' translucency, not the erasing. (Task
  `eraseevent-de-verdad.md`.)
- **`EraseScreen`/`ShowScreen` accepted without doing anything**, as a
  debt: the map stays visible where the original goes black, and the start
  menu comes out over VRAM garbage. The title that doesn't fit now
  degrades: it builds without `--no-title`. The survey's exclusions stay:
  it wasn't tested which depended on `EraseScreen`. (Task
  `degradar-en-vez-de-fallar.md`.)
- **Four shortcuts**: the condition on direction (21 pages) and the random
  step (order 8, 39 pages). Map pages went from 7,034 to 7,150 of 7,340.
  (Task `cuatro-atajos-para-los-otros-juegos.md`.)
- **Decorative events as background**: 2,887 candidates, measured without
  looking at the drawing. (Task `los-eventos-decorativos-como-fondo.md`.)
- **A ChipSet animation that doesn't fit in WRAM** (2026-10-10) keeps the
  tiles that cover the most cells moving and leaves the rest still: in map
  182, 9 of its 51 water tiles (44 of 1,469 cells). The map is back in the
  cartridge, which builds whole. (Task
  `las-animaciones-de-tiles-en-wram.md`.)

The tasks named here are in `tasks/testing/` in snes-rm2k-work.
