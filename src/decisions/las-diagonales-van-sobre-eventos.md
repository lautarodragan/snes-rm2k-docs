# Diagonals go on events

## What

**Diagonal moves go on events and not on the hero**, and they stay that
way. The converter rejects a page that tries it.

## Why

The step is written once per direction, and **of the game's 26 routes with
diagonals, none is the hero's**: supporting it would be code that nothing
exercises.

What doing them was worth, measured: **+7 pages**. For a while that number
lived under a heading that said diagonals were missing, and they aren't:
they are move commands 4 to 7, and they are in `RUTA_DIAGONALES`, in
`tools/port/eventos.py`, and in the mechanics table of
`docs/port/events.md`, both in snes-rm2k.
