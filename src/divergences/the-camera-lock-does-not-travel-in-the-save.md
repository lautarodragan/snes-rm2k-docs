# The camera lock does not travel in the save

## What

`PanScreen`'s lock keeps the camera where it is while the hero walks, until
an unlock; RM2k keeps that state —`pan_state`— in the save. The cartridge
does not: **a game saved with the camera locked loads with it following
the hero**. The rest is as in RM2k: a pan still moves a locked camera, the
lock survives a map change and the camera is centred on the hero on
arrival, and after an unlock the camera does not jump back to the hero but
follows him only as he walks away from its centre. See `pan_lock_set` and
`pan_follow` in `runtime/camera.s` in the-advocate.

## Measured

On 2026-10-16, when the lock started to compile: Sunset over Imdahl locks
the camera on seven pages and Zounds on two, all in scenes that take
control away and unlock it —or teleport— before giving it back, so no save
can happen in between. ABL never locks it.

## When it stops being enough

When a game gives control with the camera locked and lets the player save
there.
