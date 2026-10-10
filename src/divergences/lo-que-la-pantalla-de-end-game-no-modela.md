# What the End Game screen does not model

## What

End Game, the last command of the pause menu, opens `Scene_End` in RM2k:
the question —the `exit_game_message` term— and "Yes"/"No" in two windows
over black. "Yes" fades the theme and the screen and goes to the title; "No"
or cancel go back to the menu.

Since 2026-09-28 the ROM does it —see `tools/runtime/end_game.s` in
the-advocate and the `end_game.rs` of `rm2k-snes-screens`—, with the System's
windows, text and bar on the same pixels as the original, shifted to the
center of 256x224. Until that day the command was grayed out and did
nothing.

What is still different:

* **It opens and closes without a fade.** RPG_RT fades the menu and fades
  the End Game screen on the way in, about six frames each; the ROM switches
  from one to the other at once, as it does with all the menu screens.
* **The system sound effects do not play**: not the cursor's, not decide's,
  not cancel's. They do not play in the rest of the menu either.
* **It opens with the cursor on "Yes"**, which is what the 2015 RPG_RT does.
  easyrpg-player opens on "No" (`SetIndex(1)` in `Scene_End`). The 2000
  RPG_RT, the one the author used, could not be looked at: under Wine it
  crashes when changing the video mode.
* **The screen fades in 20 frames** along a brightness ramp; the theme in
  400 ms, which is easyrpg's `BgmFade(400)`. The 2015 RPG_RT takes about
  330 ms to reach black, measured with captures every 18 ms.
* **The lettering and the background strip** are those of `ventana.py` and
  the port's font, which apply to every window: compared against the
  original's capture at 320x240, a couple of glyphs differ —the "g"— and the
  light strip of the stretched background lands a few rows off.

## Measured

With the 2015 RPG_RT running under Wine, on a copy of the game whose map 4
starts with Kersh and Core in the party: the question in a 70x32 window at
(125, 72), "Yes" and "No" in a 34x48 one at (143, 120), the cursor on "Yes"
on the way in, B and "No" back to the menu with the cursor on End Game.
The drawing from `fin_del_juego.dibujar` at 320x240 lands in those same
boxes.

It is covered by `pruebas/rpgmaker/test_fin_del_juego.py` in the ABL port
(the-advocate-ports/abl) —the screen against `fin_del_juego.render` with the
cursor on each command, "No", B, and "Yes" all the way to the `titulo`
golden— and by the `fin` and `fin-no` goldens of `test_menu_golden.py`.

## When it stops being enough

A game with a longer question: the window is as wide as the text, and at six
pixels per letter 40 fit in the screen's 256. The converter stops if it does
not fit.
