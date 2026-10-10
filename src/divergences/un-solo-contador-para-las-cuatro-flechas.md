# One counter for all four arrows

## What

RM2k keeps a `press_time` per button —easyrpg, `src/input.cpp`—, so each
arrow has its own repeat delay. The ROM keeps **a single one for all four**,
`arrows_frames` in `arrows_repeat` (`tools/runtime/control.s` in
snes-rm2k): pressing a new arrow resets it to zero even if another one is
still held.

What looks different: holding down, with the repeat already running, tapping
right restarts down's delay, and it takes 23 frames to repeat again. In RM2k
down would keep going every 4 without noticing.

## Why

In single-column menus, which are almost all of them, right and left do
nothing, and nobody holds two arrows at once to go through a list. One per
button is three more bytes of RAM and a loop in `read_pad`, which runs every
frame on every screen.

## Measured

Nothing: there is no test that holds two arrows, and no case in the game
where it shows. If someone notices it while playing, the fix is a counter per
arrow in `arrows_repeat`; the screens do not need to know.
