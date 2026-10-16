# What `ChangeMapTileset` does not model

## What

`ChangeMapTileset` (11710) has RPG_RT draw the map, from that command until
the next map is loaded, with another ChipSet: the same cells, with that
ChipSet's graphics, its passability, its layer above the hero and its
animated tiles —`Game_Map::SetChipset` in EasyRPG—. On the console **the
command is dropped**: the map keeps the ChipSet it was converted with, the
page goes on, and each use is listed in the build's `degradations.json` as
a `tileset-not-changed` loss, with the ChipSet it asked for. The converter
also warns about it map by map when it is on an automatic page.

What that loses depends on what the game swaps the ChipSet for. In the two
games that use it today:

* **The Frozen World** swaps it for a copy of the place with time stopped
  —the water and the waterfalls drawn still, without their animation— and
  back, on maps 9 and 149 (the bazaar, for half a second between a flash
  and a teleport) and 47 and 99 (the temple, during a scene with an
  earthquake). On the console the place stays as it was, its water moving.
  On map 129 it swaps it for one that differs only in passability, for a
  route that walks through anyway: nothing is lost there.
* **Vampires Dawn** swaps it, on five maps, for the bat's: the same
  graphics with every cell open and nothing above the hero, while the hero
  is a bat, and back when it is not. On the console the bat would keep the
  ground's passability. Today it does not show: the transformation itself
  does not compile.

## Why

Until 2026-10-16 the command had no arm in the event compiler and its whole
page was left out. In The Frozen World the intro's step on map 9 is one of
those pages: the game stopped there, with the hero —the game's empty
"DummyHero"— walking the bazaar. taro's, from 2026-10-15, for anything the
console does not do yet: the command degrades, and the build says so,
instead of taking its page with it.

Doing it for real is converting each map with every ChipSet its pages ask
for, over the same grid, and swapping the blocks, tiles, palettes and
passability when the command runs. What that costs was measured on
2026-10-16 in the task
[`changemaptileset-is-not-compiled`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/changemaptileset-is-not-compiled.md).

## How it applies

The command's arm in `compile_command`, in `compile.rs` of
`rm2k-snes-events` in the-advocate, and its place in `ACCEPTED_UNDONE`
there. The test game's case `tileset` calls a common event that asks for
another ChipSet and then turns a switch on: `test_tileset.py` reads the
switch and the build's `degradations.json`.
