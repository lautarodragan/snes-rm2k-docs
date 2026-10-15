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

The `npc-toward-hero` case covers it. It is left out of **a page's own
routes**, of which there are two on map 105 and no test gets there; see
`ruta_propia`.

## Since then

The other nine were out because in ABL they paid nothing, and the other
games turned that around. The random step, moving away from the hero and
facing away came in on 2026-10-06, on events; **forward and the five turns
in place on 2026-10-14**, on events and on the hero, with the hero's
diagonals —see [Diagonals went on events, until the other
games](diagonals-go-on-events.md)—, and the own routes take all of them since
that day. On the hero, the commands that look at the hero look at himself:
`route::on_hero` in the compiler writes them as the move or the face down or
up they are. The task is
[`route-the-missing-moves`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/route-the-missing-moves.md).
