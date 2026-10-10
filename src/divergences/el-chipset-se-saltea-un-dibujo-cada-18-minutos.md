# The ChipSet skips a frame every 18 minutes

## What

The two clocks of the ChipSet animation —the water and the animated tiles—
do not keep a counter of their own: they come from dividing `ticks`, the
game tick, by the hardware divisor. `ticks` is sixteen bits wide and neither
24 nor 6 divides 65536, so **every 65536 ticks —eighteen minutes of play—
the count wraps around and the cycle skips a frame**. In RM2k the counter is
thirty-two bits wide and that does not happen.

The reason is in `anim_advance` in `tools/runtime/chipset_animation.s` and in
`TICK_MASCARA` in `tools/rpgmaker/rm2k.py`, both in snes-rm2k: the animation
does not spend a byte of RAM, which was needed because the BSS was full.

## Measured

Nothing: it is arithmetic. A jump of one water frame, once every eighteen
minutes.

## How it looks today

Nobody sees it, and no case in the test run lasts eighteen minutes.

## When it stops being enough

If `ticks` ever becomes thirty-two bits wide —because the game clock needs it
for something else— this goes away on its own.
