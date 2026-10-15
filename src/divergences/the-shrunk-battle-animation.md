# The shrunk battle animation

## What

A battle animation on the map is drawn **shrunk, whole and keeping its
proportions, until it fits a 64x64 box**, and without transparency: a console
object is either opaque or not there. RM2k draws it at its size, with each
cell's alpha.

Where the box comes from, and the full list of what is lost —the rounded
alpha, the screen flash that does not reach it, the target without a row,
the `global` ones—, is in the module documentation of
`rm2k-snes/images/src/animation.rs` and `rm2k-snes/convert/src/animations.rs`
in the-advocate, which is where it is decided. taro accepted the price on
2026-09-12.

## Measured

How much each one shrinks is reported by the converter. On 2026-09-12: a
96x96 one ends up at 64x64, 67%; number 78 in the intro at 36%, and number
82, which measures 536x416, at 11%.

## How it looks today

The big ones in the intro look small. A cell that fades out disappears once
it passes the halfway point instead of going away little by little.

## When it stops being enough

A map that fills all eight sprite palettes and also needs the timer: there
the box is left without a palette, and the converter says so and does not
draw it. See
[Seven palettes on a map with animations](seven-palettes-on-a-map-with-animations.md).

## As an optimization

What it saves, and where it lives in the code: [Battle animations on the map, shrunk to a box](../optimizations/lossy/pictures-and-animations.md#battle-animations-on-the-map-shrunk-to-a-box), in Optimizations.
