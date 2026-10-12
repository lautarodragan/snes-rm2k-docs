# Translucent events don't use color math

**This is a decision about one thing —A Blurred Line's translucent
events—, not a ban on color math.** It was rejected for what it costs
there, below; anything else that needs it can use it, and translucent
pictures already do.

## What

**Translucent events aren't drawn with the console's color math**, even
though it is implemented and verified in the `color-math` tag (in
the-advocate). They are baked: see
[translucent-events-are-baked](translucent-events-are-baked.md).

**Translucent pictures are**, since 2026-10-02: taro approved Gallareta's
experiment (the task [`several-pictures-in-sprites`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/several-pictures-in-sprites.md) in
the-advocate-work). The two objections below don't apply to a picture in
sprites: blending is turned on only in object palettes 4 to 7, so the hero
and the events in 0 to 3 stay opaque and animating, and the message window
isn't blended. What it does cost, and is in
[the divergences](../divergences/README.md): while there is a blended
picture, the characters in palettes 4 and 5 are blended too, and so is the
animation box if it falls there; and the console blends at 50% or adds, so
anything from 25 to 75% comes out at 50%.

## Why

taro tried it and rejected it for two reasons that aren't defects of the
implementation:

* **The object stops animating.** The translucent event leaves OAM and
  becomes BG2 tiles, which are uploaded once on entering the map, and
  almost all of the game's animate: they are the save point. Bringing it
  back to life requires uploading its tiles by DMA at the event's cadence,
  which is the machinery of the ChipSet's animated tiles.
* **The hero is seen through it.** Mode 3's ordering leaves no background
  layer slot between the floor and the hero, so the only one available is
  above. It is what FF5 does, and taro didn't like it.

## For whoever picks it up again

How it was done: `ppu_init` sets `TS` and `CGWSEL` once and for all, and
**`CGADSUB` alone** turns blending on and off, written from `flush_video`
with the per-map value the converter emits;
`render_map.dibujar_translucidos` puts the object inside the upper layer,
so it doesn't touch the VRAM split or the CGRAM one.

And two things that hold even if it doesn't go in:

* **The message window is also BG2**, so blending makes it
  semi-transparent. It is fixed with an HDMA channel that sets `CGADSUB` to
  zero on the window's lines.
* **snes9x rounds differently from the hardware in color math addition**:
  bsnes and mesen-s truncate, which is what the chip does, and snes9x
  rounds up when a channel's sum is odd. Since the goldens are snes9x
  captures, a case with color math goes into
  `pruebas/rpgmaker/test_cores.py` in the ABL port (the-advocate-ports/abl).
