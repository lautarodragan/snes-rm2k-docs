# What ChangeExp and ChangeLevel do not model

## What

Since 2026-10-04 `ChangeExp` and `ChangeLevel` compile: they are `OP_EXP`
and, with the message, `OP_LEVEL_PAGE` after it —see `exp_change` and
`level_page` in `tools/runtime/level.s` in snes-rm2k—. The level, the
experience, the skills, the HP and SP clipped when going down and the text of
each page are those of easyrpg's `Game_Actor::ChangeExp` and `ChangeLevel`.
What is not the same:

* **Two skills learned at the same level** come out in the message in the
  order of their pairs —by skill number— and not in the order of the LDB's
  table. The ROM goes level by level, like the victory page; the editor
  saves the table sorted by level, so between different levels the order is
  RM2k's.
* **On a troop page there is no message**: the battle's window is not the
  map's. The level changes anyway, and from what can be read in
  `ba_sync_in` the battle takes the new level's attack, defense, spirit and
  agility —`ba_reparam`— but not the maximum HP or SP. It was not measured:
  no troop in ABL does it.
* **A message of more than 73 lines** —the one for each level and the one
  for each new skill, adding up the whole party— loses the ones after that,
  which are learned anyway; and **a line of more than 48 letters** is cut
  there, though the window cuts it earlier.
* **The actor by variable does not compile**, as in `ChangeHP`.

## Measured

Against the battle model —`rm2k-snes-battle experience`, which is easyrpg's
in `rm2k-rules`— in `pruebas/rpgmaker/test_experiencia_de_eventos.py` in the
ABL port (snes-rm2k-ports/abl). It was not measured against RPG_RT: the game
does not use the commands, and the order of two skills at the same level
does not come up for any actor in ABL.

## How to reproduce it

A `ChangeLevel` with message on an actor whose table teaches two skills at
one level, the one with the higher number first.
