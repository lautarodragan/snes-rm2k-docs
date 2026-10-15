# The window takes thirteen colors from every background

## What

The message window lives in CGRAM palette 0, and in mode 3 those entries are
also the background's, which is 8 bits deep and addresses all of CGRAM. What
the window takes —`window_colors`, which `rm2k-snes-screens window` counts
from the game's System and the converter hands to `wally` and to the
emission— comes out of the budget of **every** map, and a map that needed
those entries merges colors of its background: Adeleine decides which ones,
and what it decided stays in the game's `patches/auto/maps/` as
`presupuesto`.

Since 2026-10-04 they are **thirteen and not eight**: besides its
background, its frame, the text and the shadow, the window carries the arrow
of a message waiting for a key and the System's cursor, the choice bar,
because both are drawn inside its tiles. With *A Blurred Line*'s System that
is four reds for the arrow and one for the bar.

RM2k does not have this: the window and the map do not share colors.

Since 2026-10-12 a game can fill its windows with one colour of its own
instead of the System's background —[The windows' background is the
project's, by System](../decisions/the-windows-background-is-the-projects-by-system.md)—,
and the colours the background brought go with it. *A Blurred Line* gives
`ablskin` its black, and loses the near-black of the stroke along two edges
of the System's background: one entry less, and every map gets it back.

## Why

The window is BG2 at 4 bits and the arrow and the bar go in its tiles, so
their colors have to be in the window's palette. The other way to draw them
without colors of their own —sprites— does not work: the object mask hides
them on the window's lines, so that events "above" are not seen through it
(see `build_hdma` in `messages.s` in the-advocate).

What was not tried: rewriting by HDMA, only on the window's lines, the
palettes of the upper layer —which is not visible on those lines, because
BG2 shows the window— with the arrow's and the bar's colors, and restoring
them below. It costs an HDMA channel and tables that follow the window; with
that the window would go back to eight.

## Measured

On 2026-10-04, comparing what Adeleine decided in `release` with eight and
with thirteen —the game's `build/<cartridge>/adeleine/` images, in RGB—: of
111 maps, **eleven** lose colors, between one and five each: 66, 67, 69, 70,
86, 112, 113 and 116 to 119. In the goldens it shows as a few pixels of a
neighboring shade: 120 out of 57,344 in the worst, map 119.

## How it looks today

On those eleven maps, some shadow of a barrel, a shelf or a wall takes the
shade next to it. No blotch or wrong color is visible.

## When it stops being enough

With a System that brings more colors: the whole window —background, frame,
text, shadow, arrow and cursor— has fifteen, and the converter refuses with
"the window, its arrow and its cursor use N colours and 15 fit". The RTP's
System no longer fits, with or without the arrow: its background and frame
alone have thirty. And with a game whose backgrounds are already tight,
each window color is one less for all of its maps. Since 2026-10-04 the
number comes from the game's window and is not a constant: a System with
fewer colors leaves more for each background.

## As an optimization

What it saves, and where it lives in the code: [The message window takes its colours from every background](../optimizations/lossy.md#the-message-window-takes-its-colours-from-every-background), in Optimizations.
