# Move route command 9, towards the hero

## What

**Move route command 9, `move_towards_hero`, is walked** since 2026-09-12.
The other nine missing movement commands —random, away from the hero,
forward and the five turns in place— **are not**.

## Why

It isn't a new command: `UpdateMoveRoute` does
`TurnTowardCharacter(hero)` and then `Move(GetDirection())`, that is,
command 21 and a `move_*` glued together, so it is solved with what was
already there.

Measured over the whole game: **+33 pages** —from 2802 to 2835—, and it is
the only one that paid off. **The other nine add up to +1 among all of
them**, and that is why they are still out.

The `npc-hacia-heroe` case covers it. It is left out of **a page's own
routes**, of which there are two on map 105 and no test gets there; see
`ruta_propia`.
