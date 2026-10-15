# A teleport to a map not carried

## What

When a `Teleport` names a map the cartridge does not carry, **it shows a
message box instead of going**: `Teleport to missing map N`, N being the map's
RM2k id. The hero stays where he is, and the page goes on after the box.

Until 2026-10-15 the whole page was left out. A game whose fighting happens on
maps that are excluded —The Frozen World's 1 and 2— lost every page that
could take the hero there, and with them everything else those pages did.

## Why

A page that does nothing is a hole nobody can see; a box says where the hole
is. The converter also warns, one line per map, with how many such teleports
there are and to which maps.

## How it looks today

The box is an ordinary `ShowMessage`, so its text goes to the text block like
any other. Nothing else about the teleport happens: no fade, no song change,
no new map. It is only the `Teleport`: `MemorizeLocation` names no map, and
`ChangeVehicleLocation` is not compiled at all.
