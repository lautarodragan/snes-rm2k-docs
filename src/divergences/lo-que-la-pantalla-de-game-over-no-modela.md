# What the Game Over screen does not model

## What

An `EnemyEncounter` with `defeat_mode` 0 that is lost, a lost random
encounter, or a `GameOver`, send RM2k to `Scene_Gameover`: the project's
Game Over picture, its theme, and on pressing a key the title screen.

Since 2026-09-28 the ROM does it —see `tools/runtime/game_over.s` in
the-advocate—: the picture named by the LDB's `System`, looked up in the game's
`GameOver/` and then in the RTP's (`ABL_RTP_DIR`), the system's Game Over
theme, 80 frames of fade-in and 80 of fade-out, and the title screen. Until
that day it went back to boot with a `jml reset`, with no picture or theme:
that was this page, under another name.

What is still different:

* **The Game Over theme does not play on the defeat message.**
  `Scene_Battle_Rpg2k::ProcessSceneActionDefeat` starts it before showing
  "defeat", **whether or not the battle has a defeat handler**; the ROM
  keeps the battle theme until the screen. Starting it there would need its
  theme in the battle's package, which is already full —see
  `PAQUETE_BATALLA` in `tools/port/eventos.py` in the-advocate—.
* **The picture is scaled to 256x224**, the same as the title's: the aspect
  ratio is not the original's. See `titulo.py`.
* **START also closes it**, besides A, as on the title screen: on a console
  you go past a screen with START.
* **The map fades in 32 frames and not 35**: two per brightness level, of
  which there are sixteen.

## Measured

The picture: `System.gameover_name` in ABL is `GameOver`, and the game ships
a single file in `GameOver/`, `ablgameover.png`, **which nobody names**. So
RM2k shows the RTP's `GameOver.png`: checked in the original under Wine on
2026-09-28, with a starting map that calls `GameOver` —the original's capture
looks the same as the `game-over` golden, except for the scaling—.

The theme, `GameOver3`, is also from the RTP: since that day music is looked
up in the game and then in the RTP, as in RM2k, and the MSU-1 tracks for the
RTP themes the `System` names are numbered after the game's: see
`track_numbers` in `tools/rm2k-snes/rm2k-snes-audio/src/game.rs` in
the-advocate.

It is covered by `pruebas/rpgmaker/test_game_over.py` in the ABL port
(the-advocate-ports/abl) —the three paths, the golden, the key and the title—
and by `test_game_over` in `test_cores.py`.

## When it stops being enough

A game where losing is part of the plot, with the Game Over theme playing on
the defeat and the story going on through the handler: there the defeat
message plays with the battle theme.
