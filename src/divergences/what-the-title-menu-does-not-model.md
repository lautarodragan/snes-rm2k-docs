# What the title menu does not model

## What

RM2k's title, `Scene_Title`, draws its menu as a window of the game's
System: the `new_game`, `load_game` and `exit_game` terms, the System's bar
on the chosen one, `load_game` greyed when there is no save, as wide as the
longest term plus the borders and with its bottom edge at 53/60 of the
screen's height. Since 2026-10-13 the ROM draws it the same way —see
`title.rs` in `rm2k-snes-screens` and `runtime/title.s` in the-advocate—,
for every game with its own System. Until that day it was the two first
terms in bare text over the picture, with a `>` as the cursor, and no
third option.

What is still different:

* **`exit_game` fades out and stops.** On a PC the program closes; a
  console has nothing to close. The ROM does what the player sees of it:
  the song and the screen fade like End Game's "Yes" —20 frames to black,
  the song in 400 ms— and the CPU stops (`stp`). Reset or the power switch
  is what comes next. Leaving the option out was the other choice, and it
  was not taken: the window would be a line shorter than the original's,
  and the term is the game's.
* **The system sound effects do not play**: not the cursor's, not
  decide's, and not the buzzer of choosing a greyed `load_game`, which
  does nothing, as in RPG_RT.
* **It appears without the opening animation.** easyrpg opens the window
  in eight frames (`SetOpenAnimation(8)`); it was not measured against
  RPG_RT.
* **Its place is the same fraction of a shorter screen**: the bottom edge
  at 53/60 of 224, row 197, and centred in 256. The picture behind is
  scaled from 320x240, so the window keeps its place over it within a few
  pixels, and is a little wider than the original's where the port's font
  is wider than RM2k's.
* **Its colours are fifteen**, BG2's palette 0 —the picture takes the rest
  of CGRAM—. A System with more —a gradient behind the window, a disabled
  colour with its own gradient— is reduced by Adeleine, the least visible
  colour into its nearest, and the converter warns how many were merged.
  The background follows `[windows.background]`, as every window does: in
  *A Blurred Line* the stretched background's light strip is not drawn.
* **The bar does not alternate its two drawings**, as in every window: see
  [The choice bar does not alternate its two drawings](the-choice-bar-does-not-alternate-its-two-drawings.md).
* **It keeps the starting System** after a `ChangeSystemGraphics` and a
  reset: see [What `ChangeSystemGraphics` does not model](what-changesystemgraphics-does-not-model.md).
* **A save from another build is no save**: the slot looks empty on the
  slots screen, and on the title `load_game` stays greyed if it is the only
  one.

What is the same, and was measured: both the 2000 and the 2015 RPG_RT open
the menu on `new_game` even with a save, and the ROM does too. easyrpg
opens it on `load_game` when there is one (`SetIndex(1)`). The cursor goes
onto the greyed `load_game`, and up and down wrap around. Cancelling the
slots screen comes back with the bar on `load_game`.

## Measured

On 2026-10-13, with *A Blurred Line* under Wine, the 2015 and the 2000
RPG_RT: at 320x240 the window is 112x64 at (104, 148), the bar 104x16 at
(108, 156 + 16 per option), and the text 8 pixels in from the window. With
a save made by the game itself, `load_game` comes out in the text's colour
and the bar still on `new_game`. `exit_game` fades to black in about half
a second and the program closes. The other seven games' titles were
captured the same way, with the 2015 RPG_RT, and the port's look like them.

It is covered in the ABL port by `test_title_golden.py` —the title with and
without a save, the bar on each option, A on the greyed one, the slots and
the way back, in 8 and 4 bits per pixel— and by `test_title_drawing.py`,
which compares the menu against `rm2k-snes-screens render` with the screen
`title`, with and without a save, and checks that `exit_game` leaves the
screen black and the game not started. The other games are covered only by
`tests/test_boot.py` at the root of the ports, which passes the title by
its first option.

## When it stops being enough

A game whose longest term does not fit in 256 pixels: the converter stops.
And a System whose window loses a colour that is seen: the warning says how
many were merged, and Vampires Dawn's is the System that loses the
most.
