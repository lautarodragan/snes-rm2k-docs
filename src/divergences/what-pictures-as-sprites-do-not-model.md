# What pictures as sprites do not model

## What

The `ShowPicture` pictures that go in sprites —see
`runtime/picture_far.s` and `rm2k-snes/images/src/show_picture.rs` in the-advocate— do
not do everything they do in RM2k:

* **Transparency comes in three steps**: at 76 % or more it is not visible,
  from 25 % to 75 % it blends half and half with what is underneath —the
  console's color math, which blends at 50 % or adds, and nothing in
  between—, and below that it is opaque. The smoke on 207 (40 %) comes out
  at 50 %, and the shadow on 311 appears all at once halfway through its
  one-second fade, already at 50 %. While there is a blended one, the
  characters the map has in sprite palettes 4 and 5 are blended too, and so
  is the battle animation's box if it lands there: the hardware blends
  palettes 4 to 7 entirely. It is the `pic_blend` experiment, in
  `runtime/picture.s`, and it comes out with its commit.
* **`MovePicture` neither moves nor enlarges**: it changes tone and
  transparency. One that asks for another place or another zoom does not
  compile and is accepted without being done.
* **Two at a time**, one per number, the first two the map shows: the third
  is not drawn.
* **No rotation or waving, no enlarging, no saturation**, and nothing larger
  than 256x128: those belong to the BG1 plane (phase 3).
* **Fifteen colors**, those of one sprite palette, counted by use: gradients
  get banded.
* **They go above the message window**: object priority 3, which is the one
  from before. In RM2k the window covers the pictures.
* **The ones tied to the screen are scaled to 256x224, the map's are not**:
  on the console the map is not shrunk, so a picture attached to it keeps
  its pixels and only its zoom is applied.
* **The screen shake** moves the map's pictures —`screen_x` is subtracted
  from them, as from the characters— but not the screen's.
* **A page that goes on after a `Teleport`** and shows a picture uses the
  table of the map it was compiled in: the destination's may be another.
  Measured over the game's maps: only one page does it, the one on 288, and
  its two pictures are large ones.

## Measured

On the `release` cartridge, on 2026-10-01: the sign on 4, the one on 81, the
Fortitude's label on 95 and the shadow on 311 are drawn. The shadow lands in
the same place on the map as in RPG_RT under Wine: its box gives
(39,59)-(140,179) there and (40,60)-(138,178) here, in map pixels. The
`ABLrec` on 45 is not drawn because the map uses seven character palettes
and the battle animation's box the eighth.

## When it stops being enough

When 207 gets into the cartridge —the smoke is the only translucent one
that is looked at up close— or the portable console, which shows nine at
once.

## As an optimization

What it saves, and where it lives in the code: [Pictures in sprites: scaled, fifteen colours](../optimizations/lossy.md#pictures-in-sprites-scaled-fifteen-colours), in Optimizations.
