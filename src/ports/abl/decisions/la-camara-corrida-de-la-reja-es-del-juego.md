# The camera offset after the gate is the game's

## What

On leaving through the gate on map 12, Talan lands at (40,56) on map 8 and
**the camera ends up three cells lower than it should**: he is seen stuck
to the top edge with half a screen of map below him. **It isn't fixed.** It
is like this in the original game.

## Why

The game does it, not the port. The gate turns on switch 36, and with 36
on, the **Bum**'s page starts by itself —event 10 at (38,55), "Woah!
Where'd you come from, Mister?"—, which does a `PanScreen` scrolling three
cells down and **never returns it**: it doesn't have the return operation.

And the pan stays stuck because that is how RM2k works: the camera **keeps
carrying it while the hero walks** —`Game_Player::UpdateScroll` subtracts
the pan from the target, and only skips it if the pan is locked— and the
only thing that clears it is changing maps, in `PerformTeleport` with
`map_changed`. Both things are what `tools/runtime/camera.s` in snes-rm2k
does, so the port copies it correctly.

taro played it in the original RPG_RT on 2026-09-23 —the 2000 one, the one
that ships with the game, running under Wine— and the camera ends up just
as offset.

## What to do if it shows up again

Nothing. If someone sees the camera off-center after the gate and wants to
"fix" it, they are about to break fidelity. The symptom of a defect of
**ours** would be different: the drawn map not matching the collision
—walking on walls—, which is what `pruebas/rpgmaker/test_camara.py` in the
ABL port (snes-rm2k-ports/abl) guards.
