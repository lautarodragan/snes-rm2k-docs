# The teleport transitions

## What

`ChangeScreenTransitions` changes which transition the teleport uses to
erase the screen and which one to show it again. In RM2k they are the twenty
of the `fades` table of `Game_System::GetTransition`; the ROM does three,
and the converter decides —`CHANGE_SCREEN_TRANSITIONS` in
`tools/port/eventos.py` in the-advocate—:

* **the mosaic** (17), with the PPU's MOSAIC register, tied to the
  brightness ramp. See `runtime/teleport_transition.s` in the-advocate;
* **the fade**, which is also what is used for **the ones the console does
  not do**, like the zoom (16): bringing the map closer is mode 7, and the
  map is in mode 3. taro decided it on 2026-09-26, the same as for the
  battle;
* **the cut** (19) for erasing: black in one frame, like RM2k's
  `TransitionCutOut`, and the map is loaded there. Since 2026-09-27, because
  of Eisen's story. "None" (20) for erasing also compiles to the cut.
* **the cut** (19) for showing: the new map at full brightness on the tick
  of the load, with no ramp back up, like RM2k's `TransitionCutIn`, which
  lasts one frame. Since 2026-10-11, because Sunset Over Imdahl asks for it
  in the page that opens the game (event 1 on its map 22): while it did not
  compile, the whole page was left out and the scene stayed in the black
  tint of map 11. "None" (20) for showing also compiles to the cut: in
  RM2k it lasts zero frames instead of one, and nothing on the console
  tells the two apart.

What is still different from the original:

* **The mosaic darkens.** In RM2k the blocks grow over the whole image and at
  the end it is erased; here the brightness goes down at the same time, as
  in battle, because the map load has to land inside the black (see
  `battle_fade.s`).
* **Sprites are not pixelated.** The PPU's mosaic belongs to the
  backgrounds: the hero and the events stay whole while the map turns into
  blocks.
* **The zoom is the usual fade.**
* **The transition does not travel in the save**, and in RM2k it does: see
  `TRANSITION_ERASE` in `runtime/far_ram.s` in the-advocate.
* **Erasing with "none" is the cut.** In RM2k it does not touch the screen,
  so the fade back goes from the old map to the new one (`screen1` and
  `screen2` of `Transition`); the console has nothing to blend two frames
  with, and the map load writes VRAM with the screen off. Map 93 asks for it
  when jumping to 95: there you see the control room dissolve into the
  corridor, here a black frame and the usual fade.
* **The battle ones do not compile**: the page that asks for them does not
  run. The ROM always uses the database's.

## Measured

The game uses it in Boss Wick's hideout: zoom to go to the vidcasts (page 1
of event 7 on 40), mosaic inside (page 1 of event 2 on 42), the erase back to
the fade in the video (on 45) and everything back to the fade in the favor
(page 4 of event 7 on 40). And in Eisen's story: "none" for erasing when
going down to the minigame (page 1 of event 4 on 93), the cut when leaving
it (event 55 on 95), the mosaic to enter the throne simulation (event 1 on
101) and everything back to the fade in Sorbe (page 5 of event 6 on 81). In
the whole game 15 pages ask for it; the ones that use the cut for showing or
7 (from the edges to the center) are on maps that do not fit. Of the other
ports, Sunset Over Imdahl, Dooms 2 and The Frozen World show with the cut
(1, 8 and 2 commands).

It is covered by `test_transicion` in `pruebas/rpgmaker/test_comandos_golden.py`
in the ABL port (the-advocate-ports/abl) —goldens halfway through the mosaic
and halfway through the zoom—, by `test_borrar_con_el_corte` in the same
file —brightness at zero and the map loaded on the first tick of the fade,
against the fade's whole ramp—, by `test_mostrar_con_el_corte`, also
there —the fade over and full brightness on the tick of the load, with a
golden of the next one—, by the mosaic and the zoom in
`test_cores.py` too, and by `test_recorrido_lashe_wick_golden.py` and
`test_recorrido_capitulo_golden.py`, which check through RAM what each page
leaves chosen.

## How it looks today

Entering the vidcasts is a fade; from there to the video, each jump turns
into blocks as it goes dark and dissolves back as it lights up, with the
hero sharp on top.

## When it stops being enough

A game that uses the block, blind or wipe transitions, or the zoom as an
effect that has to be seen: see
[`las-otras-transiciones-de-rm2k`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/las-otras-transiciones-de-rm2k.md) in the-advocate-work.
