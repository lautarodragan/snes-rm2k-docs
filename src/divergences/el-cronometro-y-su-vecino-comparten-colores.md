# The timer and its neighbor share colors

## What

The timer's digits share a palette with a character —see
[The timer has no palette of its own](../decisions/el-cronometro-no-tiene-paleta-propia.md)—,
and if the character has one of their two colors, black or pure red, **both
use the same CGRAM entry**. While the timer is visible, that entry goes
untinted, because in RM2k the digits are not tinted; so that color of the
character is not tinted either.

The rest of the character is, and with no timer on screen, all of it: this
is done by `upload_timer_pal`, which uploads untinted only the digits'
entries and only while they are visible.

## Measured

In `release`, on 2026-09-25, the character shares the black on maps 2 and
10, and both colors on 11, 17, 21 and the six with the save point (8, 20,
23, 26, 28, 32). It changes with the palette distribution: the table and how
it was obtained are in
`tasks/testing/el-tinte-no-tine-al-que-comparte-paleta-con-el-cronometro.md`
in the-advocate-work.

Which tint exposes it:

* **the black**, only one that lightens a channel —above 100—: darkening and
  desaturating leave black as black;
* **the pure red**, almost any: darkening, desaturating or shifting the red.

In the game, the timer coincides with a tint twice: Talan's alarm clock runs
with saturation at 40 through map 7 and Lashe City up to 16 —the save point
on map 8 keeps its red—, and the burning forest's runs over (120, 50, 50) on
312, which is not in `release`.

## How it looks today

No test looks at it: the test run builds without the timer, and the `timer`
case runs on map 6, where the digits share a color with nobody.

## When it stops being enough

If it shows. The fix is for the digits to have **entries of their own** even
when the color is already in the palette: two entries instead of the ones
that are missing. It is not a palette, but the save point uses fifteen
colors and on map 8 the eight palettes are full, so there someone would have
to give up colors.
