# The hero's speed with L and R

## What

R raises the speed at which the hero walks and L lowers it, one step at a
time, between RM2k's 1 and 6. RM2k has nothing like it: it is taro's, from
2026-09-30 —"being able to increase or decrease the hero's speed with the R
and L buttons"—. Like the X autofire, **it only adds**: in RM2k there is no
button that corresponds to L or R. It is in
`tools/runtime/hero_speed_keys.s` in the-advocate.

What was decided, and is commented there:

* **It is not the game's speed but an offset on top of it.** The game's
  —the one route commands 28 and 29 raise and lower, and the one that
  travels in the save— is not touched: L and R move another byte, and the
  hero walks at the sum, capped at 1 and 6. With the offset at zero
  everything is RM2k frame by frame.
* **A forced route on the hero walks at the game's speed**, without the
  offset, while it lasts —its last step included—, and the pad goes back to
  the offset on the first step the player takes. If the route changed the
  game's speed, the offset is added to the new one.
* **It carries over when changing maps and is not saved in the game**: it is
  a preference of whoever plays, not state of the world. Reset clears it.
* **It is only read while the player has the hero**: no route, no message,
  no page running in the foreground and no events waiting to start, which
  are the same guards as walking. The menu, the battle, the shop and a
  teleport's fade have their own loop or freeze the main one, so it is never
  read there. A press that lands where it is not read is lost.
* **A press from the cap already changes it.** The offset is recomputed from
  what the hero walks: with the game at 6 and two Rs that did nothing, one L
  already gives 5.
* **It is switched off without touching the runtime**, with
  `--no-speed-keys` in a cartridge's `flags`: the converter emits
  `HERO_SPEED_KEYS = 0` and the loop does not read them. `test-special`
  carries it, so that the switched-off path has its test.

## Measured

At each speed the hero crosses a cell in 64, 32, 16, 8, 4 and 2 frames.
`pruebas/rpgmaker/test_velocidad_con_l_y_r.py` in the ABL port
(the-advocate-ports/abl) measures it with the pad: touching nothing, 8; R once,
4; twice, 2; five times, still 2; L once, 16; three times, 64; five times,
still 64. Also: the press from the cap, that it carries over after a
teleport, that `ruta-vel` with an offset of +2 walks its steps at 4, 4, 4, 8
and 8 frames —those of speeds 5 and 4, as without it— and the pad afterwards
at 2, that R with a message open does nothing, and that `test-special`,
built without L and R, does not read them.

## How to reproduce it

On any map, press R and walk.
