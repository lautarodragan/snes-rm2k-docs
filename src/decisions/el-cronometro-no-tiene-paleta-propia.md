# The timer has no palette of its own

## What

**The timer has no palette of its own**: it goes into the palette of any
character that uses thirteen colors or fewer.

## Why

Having it separate cost an undrawn event on map 2 —the middle cell of the
door Core breaks—, and an event that isn't drawn still takes up room in
`npcs_dibujables`.

What this costs today, and the idea of reserving it only while the timer
runs, is in [`timer-palette`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/timer-palette.md) in the-advocate-work.

## When it stops being enough

On a map that fills the eight palettes at fifteen colors. There room is
made for it by lowering a character to fourteen —the one that moves the
fewest pixels, and never a leader—, and if not even that is enough the
converter stops and says so. See "the timer **before the events drawn with
a chipset tile**" in `drawable_npcs`, in `tools/port/sprites.py` in
the-advocate.

## What it requires of the ROM

Since the palette belongs to a character, **the tint can't skip it
whole**: the digits aren't tinted and the character is. `upload_timer_pal`
uploads untinted only the digits' entries, and only while they are
visible. Until 2026-09-25 it uploaded the whole palette, which was right
when the digits had it to themselves, and the character was left untinted.
The colors the character shares with the digits are still untinted while
the timer is visible: see
[el-cronometro-y-su-vecino-comparten-colores](../divergences/el-cronometro-y-su-vecino-comparten-colores.md).
