# The window without a background does not cover the characters

## What

`MessageOptions` without a background leaves the text over the map, with
its shadow, where the window would go. In the ROM that has two differences
from RM2k, and both come from the same thing: the window is **BG2**, the
same layer as the one above the map, and mode 3 does not have a third.

* **The characters go over the text.** In RM2k the window is above
  everything —`Priority_Window` is 130, and the characters go from 30 to
  70—. Here the text is BG2 with priority 1, and the hero and the events are
  objects with priority 2, which in mode 3 go in front. With a background it
  does not show because HDMA hides the objects on the window's lines
  —`mask_*`, in `message_place.s` in snes-rm2k—; without a background they
  cannot be hidden, because they have to be seen.
* **The layer above the map is not visible on the window's 80 lines.** On
  those lines BG2 shows the window's tilemap —the plane without a frame,
  with the cells that are not text left blank—, so roofs, treetops and
  everything the chipset puts on top disappear from that strip while the
  message lasts. The lower layer and the characters are visible.

And one that is not about the layer: the red "continue" arrow RM2k draws at
the foot of the window is not there, with or without a background. It
predates this.

## Measured

Against the original under Wine, on 2026-10-04, with the page from
`ventana-medio-sin-fondo` placed in a copy of the game: the text lands in
the same place and with the same shadow, and the only difference on screen
is that the hero covers "Ready". The captures from that comparison were
kept outside the repositories, for review.

ABL asks for the window without a background in more than a third of its
`MessageOptions`, almost always in cutscenes over the black screen or a
picture, where neither difference shows.

## When it stops being enough

In a game that talks without a background over a map with roofs or trees in
the window's strip, or with characters walking through it. Fixing it means
drawing the text with something other than BG2: with objects it does not
fit —a line of text is 30 tiles wide and the PPU draws 34 per line among
all of them—, and mode 3 has no more layers.
