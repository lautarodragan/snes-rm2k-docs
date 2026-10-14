# The quarry's timer stays in Paradise

## What

**The quarry's timer is drawn on Paradise (108), and not in the maps
Paradise leads to.** The defender's job (150, event 4) starts a
five-minute timer; Talan can walk out of the job to 108, and there the
timer is on screen, as in the original. It is
`timer_stays_in = [108]` in ABL's `rm2k-snes.toml`: the converter gives
the digits to 108, and its walk does not carry them on from there.

On 108, with every map of the game in the cartridge, the eight sprite
palettes are full, so the timer **is lent one**: black is drawn as
itself and the System's red, (31,0,0), as the nearest red of the
palette, (28,5,6). Nobody loses a color for it.

It is Chajá's, from 2026-10-14, when the whole game was first built; the
task is
[`abl-the-quarry-timer-does-not-fit-on-108`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-quarry-timer-does-not-fit-on-108.md).

## Why

The original was looked at first: under Wine, with the job started, the
exit at (19,2) of 150 takes Talan to 108 and the timer is there, counting.
When it reaches zero, common event 36 brings Talan back to the quarry
from wherever he is. So leaving 108 out —the first proposal, 108 in
`timer_never_runs_in`— would have lost something the original shows.

The walk that hands out the digits follows every `Teleport` of the pages
of a map the timer reaches, without looking at switches. From 108 that is
every cutscene that leaves the town, which is the rest of the game: the
digits went to 283 maps instead of 64 —a row of sprite tiles in each one,
and in seventeen of them a character brought down a color to make room—,
and Lashe City (13) did not fit them. Stopping the walk at 108 keeps what
is seen and drops what is not.

## What is lost

* **The timer in Paradise's houses.** If Talan enters one during the job
  it is not drawn there; it still runs, and still ends the job. The town
  is not left during it: from switch 396 on, the exit to the tunnel only
  says "I don't need to go back through the tunnel".
* **The red of the digits on 108**, a little darker than the System's,
  only while every leader of the game is in the cartridge.
