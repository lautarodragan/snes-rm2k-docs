# A window with a gradient is fused until it fits

## What

**A System whose windows don't fit their bank of tiles is drawn with
fewer tiles, and the game keeps its own System.** Since 2026-10-11.
It is what stopped four of the surveyed games —The Book of Three, The
Frozen World, Vampires Dawn and Dooms 2—, which until then built with A
Blurred Line's System instead of theirs.

The culprit is the window's background. RM2k stretches the System's 32x32
background over the whole window, so a gradient becomes a different 8x8
cell on every row of the window —and on every column, if it runs
sideways—, and so does the frame over it wherever the frame lets it
through. On the console those cells are tiles, and every screen keeps its
tiles in a bank of fixed size.

Each kind of screen gives way where it shows the least:

* **The message window.** Its text area already has a tile per cell —the
  cartridge writes the letters into them—, so what overflows is the frame
  and the arrow, which have 16 of the bank's 256. **The background seen
  through the frame** has its most alike cells fused —Adeleine's
  `group_tiles`—, as few as it takes, and the frame is laid over them as
  it is: the gradient behind the frame goes in bands, and the frame's
  ornaments and the gradient of the text area stay as RM2k draws them.
* **The screens that cut their windows into a bank at 8bpp** —the actor
  choice with the pause menu's bar, items and equipment, the shop, the
  battle—: their cells, cursors and text included, are merged **one at a
  time, the one that shows the least into its nearest** —Adeleine's
  `merge_least_visible_tiles`, mirrors included— until the bank holds
  them. Two rows of the gradient one step apart melt first; a letter, which
  is far from everything, last. The item and equipment windows also leave
  room below them for the text of the busiest item list.
* **End Game**, whose overflow is colours and not tiles: its pairs of
  colours are merged with `merge_until` until they fit its palette, black
  kept as the backdrop.

Every screen that gives way says so in a warning of the build. A System
that fits goes through none of it: A Blurred Line's cartridge came out
byte for byte the same.

## Why

Two other ways were tried and measured on 2026-10-11, with the four games:

* **A tiled background instead of a stretched one.** Not enough, and it
  shows more. With the background tiled, the message window's frame still
  had 14 to 16 distinct cells before the arrow's, for the 16 tiles it has
  —the gradient repeats every 32 pixels, and the frame lets it through at
  four offsets—, and a gradient repeated every
  32 pixels is a sawtooth all over the window, not bands at its edges.
* **Fusing whole windows with a k-means.** It fits, and it breaks frames:
  The Book of Three's ornate frame plus its cursor are 85 tiles of the
  actor choice's 64 even with a plain background, so the k-means had to
  take frame cells too, and it took corners and stretches of edge. Fusing
  only each window's background into bands, with the frame on top, has the
  same wall. Merging one tile at a time by how much it shows spends the
  loss on the gradient first, which is where the eye notices it least.

Fusing colours until the tiles fit was tried before, on 2026-10-05, and it
left The Frozen World's window with 4 colours and The Book of Three's with
2.

## How it applies

`rm2k-snes-screens`: `fit_frame` in `message_window.rs`, the module
`fit.rs` —which decides once, and both `convert` and `render` draw with
what it decided—, and End Game's colours in `end_game.rs`. The pieces
that change pixels are Adeleine's.

What still stops the four games after this is not the windows: see each
one's page under Ports.

Since 2026-10-12 a game can skip all of this for a System by giving it
a background of its own: see [The windows' background is the project's, by
System](the-windows-background-is-the-projects-by-system.md). The fusing
stays for the Systems that keep theirs.
