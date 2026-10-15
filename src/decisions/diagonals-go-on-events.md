# Diagonals went on events, until the other games

## What

**Diagonal moves go on events and on the hero**, since 2026-10-14. Until
that day they went on events only, and the converter rejected a page that
gave one to the hero; that was this decision, and it was taken for ABL.

## Why

The step was written once per direction, and **of ABL's 26 routes with
diagonals, none is the hero's**: supporting it would have been code that
nothing exercised. What doing them was worth in ABL, measured: **+7 pages**,
all of them events'. For a while that number lived under a heading that said
diagonals were missing, and they weren't: they are move commands 4 to 7.

The other games changed the count. Vampires Dawn gives the hero a diagonal
in 219 pages, Sunset over Imdahl in 65, Dooms 2 in 3 and The Book of Three in
one, the scene on the riverbank that leads to the next map. Measured with `just
culprits` on 2026-10-14, the hero's diagonals, his relative turns and moving
forward brought back 69 map pages of Sunset, 97 of Vampires Dawn and 2 of The
Book of Three. The task is
[`route-the-missing-moves`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/route-the-missing-moves.md).

## How it applies

The hero's diagonal is `try_diagonal` in `runtime/hero.s` in the-advocate:
the same two L-shaped legs as an event's, asked of `cell_allowed_diag` as the
walker on the hero's layer, and the step the straight ones take, which
already moved both axes. Its comment says what it does with the facing and
with RM2k's `direction`.
