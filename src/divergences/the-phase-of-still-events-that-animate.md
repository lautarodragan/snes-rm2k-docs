# The phase of still events that animate

## What

RM2k's `animation_type` 1 and 3 —"Continuous" and "Fixed Dir/Continuous"—
make the event run through its walking cycle without moving; the save point
in Lashe City is of the second type. In RM2k each character carries its own
counter, which starts at zero when the map creates it.

Here the counter is **global**: the column comes from dividing the game tick
by the speed's `ANIM_CONTINUA`. An event that appears in the middle of the
game comes in with the cycle already started at any point. The reason —there
is no per-event byte to keep it in— is in `animate_still` in
`runtime/animated_stills.s` in the-advocate.

## Measured

Nothing to measure: the cycle has four steps, and the only thing that changes
is which one each event starts on.

## How it looks today

Nothing that can be seen on a still screen.
