# Baked decorative events

## What

With `[graphics] decorative_events = true`, an event that is only a drawing
—one page, with no commands or conditions, with a CharSet, with no movement
of its own and that **nobody names**— is painted into the background and
**stops being an event**: it has no row, no slot and no page in the table.
What changes with respect to RM2k:

* **The animation's rhythm is the ChipSet water's, not the event's speed.**
  RM2k runs it through the cycle 0, 1, 2, 1 at the pace of `move_speed`;
  here it is the `water` family, which changes every `WATER_FRAMES`. The
  cycle is the same; the step is not.
* **They all start in the same phase.** In RM2k each event starts on the
  column of its `character_pattern`; here frame 0 of the family is column 0
  for all of them.
* **A translucency that does not fit blended gets dithered.** Blending each
  frame of the event with what is behind it adds extra colors to the
  background —the river in Weg, 100—; if that costs the ground more than
  `GROUND_LOST_MAX` pixels of its own colors, the translucent ones switch to
  the dither pattern (`five_of_eight`) the sprites already use. And if even
  then it does not fit, those events remain objects.
* **A decorative event on the lower layer always stays under the objects**,
  also under an object on its same layer that is higher up on screen; RM2k
  sorts them by y.
* **Only the ones on the lower layer, and the ones on the hero's layer whose
  drawing does not stick out of its cell.** One that sticks out would be
  drawn behind a hero standing on the cell below, who covers it in RM2k.
  The ones on the upper layer remain objects.
* **Blocking moves to the grid.** One on the hero's layer closes its cell in
  the map's passability; it is no longer an event that blocks but a closed
  cell, so nothing in the game changes it either.

## Measured

Weg, map 95 of Vampires Dawn, with the water made of 183+24 translucent
`water1` events: 188 become background, 59 remain objects (the ones EV0016
moves, the waterfalls with turning, the ones on the upper layer and the ones
with conditions). Sprite tiles: 4096 before, 960 after; background tiles,
327 before and 394 after, 107 of them in the water's run.

## When it stops being enough

A background with its palette full —Uruya, map 165, with 8— does not take a
single color more without losing its own, and its decorative events remain
objects.

## How to reproduce it

`wally map` on the map's request with `"decorative": true`.

## As an optimization

What it saves, and where it lives in the code: [Decorative events become background](../optimizations/lossy/events.md#decorative-events-become-background), in Optimizations.
