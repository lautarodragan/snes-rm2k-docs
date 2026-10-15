# The playing track wins, and the sound effects wait

## What

**When the track that is already playing and the new map's package don't
fit together in the ARAM, the track wins: the sound effects that didn't
fit wait for the next `PlayBGM`**, which silences the old track and
completes the package.

It is from 2026-09-26, with the per-package budget (see
[A single sample bank](../optimizations/lossless/audio/the-sample-bank.md)), and taro
decided it by choosing option A of step 6 of the task
[`quality-of-the-music`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/quality-of-the-music.md) in the-advocate-work.

## Why

Almost no map in the game brings its own track: a page turns it on, and
until then the previous map's track keeps going. `package_load_done`
doesn't move its samples —the music keeps going during the fade, and
overwriting a sample that is playing would be noise—, so the new package
is placed next to it.

Budgeting the whole inheritance, sound effects included, left the
polysynth of `escape_newyork` at 4 kHz and the strings and the square wave
at 6: worse than before the per-package budget, on the tracks that matter
most. Counting the inherited track **only as a track** is what makes the
per-package budget worth it. What is paid: the map's sound effects don't
play between arrival and the `PlayBGM`, and that `PlayBGM` freezes for as
long as it takes to upload what was missing. In the game, maps 2 and 3
turn on their track before using their sound effects.

Where it lives: the converter budgets each package with the tracks that
may be playing on arrival (`inherited_songs` in the `cartridge.rs` of
`rm2k-snes-audio`), the ROM notes `PKG_PARTIAL`, and `song_ensure`
completes the package. It is caught by
`test_the_package_that_did_not_fit_with_another_song_playing_completes`.
