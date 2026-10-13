# The way into battle, in mosaic

## What

When a battle starts, the map goes to black **in mosaic**: after the two
flashes, the blocks grow from 2 to 16 while the brightness goes down, with
the same ramp, frame by frame, the battle uses to go away when it ends. See
`battle_fade_in` in `runtime/battle_fade.s` in the-advocate.

RM2k does what the database's `System` says, and *A Blurred Line* asks for
something else to cover the map: `battle_start_fadeout = 16`, which in the
table of easyrpg-player's `Game_System::GetTransition` is the zoom
(`TransitionZoomIn`). The other three are the mosaic or the zoom the ROM
already did: `battle_start_fadein = 17` (the battle comes out of the
mosaic), `battle_end_fadeout = 17` (it goes away in mosaic) and
`battle_end_fadein = 16` (the map comes back with a zoom).

The console does not do the zoom —bringing the map closer is mode 7, and the
map is in mode 3—, and until 2026-09-30 it was a fade, as taro decided on
2026-09-26 for all the ones that cannot be done. That day they asked for the
mosaic: "let's make the transition into battle the same as the one out —the
squares one—". So **the `System` is not read**: the way in is the mosaic for
any game, and it is a design change, not a fix.

The rest of the mosaic is as always (see
[The teleport transitions](the-teleport-transitions.md)): **it
darkens**, because the loading of the audio package has to land on black,
and **sprites are not pixelated**: the hero and the events stay whole while
the map turns into blocks. The message window that opened the battle, if
there is one, does: it is a background layer.

**The way back to the map is still a fade**, which is what the zoom of
`battle_end_fadein` had been. taro did not mention it.

## Measured

`test_the_entrance_covers_the_map_with_the_exits_mosaic`, in
`tests/rpgmaker/test_battle_fade.py` in the ABL port
(the-advocate-ports/abl), measures the size of the blocks on each frame
**by looking at the screen** —in which columns each line's color changes—
and requires the map's ramp down on the way in to be the same sequence as
the battle's on the way out. With the fade it found the way in empty.

## How it looks today

Talk to the droid in the `linkage` case: two flashes, the map and the
message break into blocks toward black with the hero sharp on top, and the
battle comes out of the blocks.

## When it stops being enough

A game whose `System` asks, to cover the map, for a transition the ROM does
do and that is not the mosaic —the cut, for example—: there it would have to
be read, and the mosaic would remain for the ones the console does not do.
