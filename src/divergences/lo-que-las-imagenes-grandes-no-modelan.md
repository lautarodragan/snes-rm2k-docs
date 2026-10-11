# What large pictures do not model

## What

The `ShowPicture` pictures that cover the screen go in BG1, with the console
in mode 1 while they are shown —see `runtime/big_picture.s` and
`tools/port/picture.py` in the-advocate, and
[Large pictures in mode 1](../decisions/las-imagenes-grandes-en-modo-1.md)—,
and they do not do everything they do in RM2k:

* **Zoom is done in mode 7, with a 255-tile texture**, since 2026-10-03
  —see `runtime/big_picture_zoom.s` in the-advocate and the task
  [`picture-zoom-in-mode-7`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/picture-zoom-in-mode-7.md) in `tasks/` in the-advocate-work—. Still, the
  picture is at full resolution in mode 1, like any large one; when the zoom
  starts it switches to mode 7, and there each place in the picture shows
  the closest tile out of the 255 that fit —in noisy photos, sometimes a
  piece of a tree or a tombstone that is not its own—. Mode 7 does not
  filter: as it shrinks, the grain flickers. What does not fit in that —a
  picture of more than 960 tiles or more than 32 rows— still fades to black
  instead of shrinking, as before: what reaches transparency is what remains
  of its area.
* **The point that stays still in the zoom of a cropped picture is the
  center of the screen**, not RM2k's center of the picture, which falls
  outside what is visible (in `PhoneCallDiff`, 24 pixels to the left and 8
  up). What shrinks is what is visible, not the whole 320x240 photo. It is
  what taro saw in the pilot.
* **With a picture with a still texture there are no messages**: the window
  lives in the half of VRAM the picture occupies while the texture is
  uploaded. It comes back during the zoom, so messages over the black after
  a zoom to zero are visible; **in mode 7 there is no second layer**, and a
  message during the zoom, or with the picture still at another size, is
  not visible. No scene in ABL does either of those.
* **Transparency darkens.** Under the layer there is only the backdrop
  color, which is black, so a picture at 50 % is a picture at half its
  color: exact over the black screen, which is where the game shows them.
  With a tone that lightens and transparency at the same time it is an
  approximation, which no picture in the game asks for.
* **The map is not visible while it is there**: not its layers, not the
  characters, not the timer, not the small pictures. The instructions on
  285, which in RM2k go over the map with the map around them, here go over
  black. And the menu does not open.
* **A picture that goes over the map hides it.** Sunset Over Imdahl draws
  its roofs, ceilings, lights, shadows and mists as screen-sized pictures
  over the map —about 140 of them, most with the transparent colour
  covering half or more of the image, or shown at 45 to 95 %
  transparency—. Each is a big picture here: the map goes, what RM2k shows
  through it is the black backdrop, and a mist at 95 % transparency is a
  black screen. Measured on its map 22 on 2026-10-11: see
  [Sunset Over Imdahl](../ports/sunset-over-imdahl/README.md). Since the
  same day a project can have the ones that stay put on a map drawn into
  the map instead —[Pictures drawn into the map](las-imagenes-dentro-del-mapa.md)—;
  Sunset does, and the rest of its pictures are still big ones.
* **Showing it and erasing it turn the screen off**: measured, two frames
  when showing one and fourteen when erasing it, which reloads the map like
  the return from battle. The game's appear and go away over the black
  screen, except the photo on 212, which appears over the map with a
  flicker.
* **The screen flash is not visible over it**, nor the tint —which RM2k does
  not apply to pictures either—: both are the map's palette, and the
  picture's is another one. The white on 213, 214 and 216, which starts
  right before the photo, is cut when it appears.
* **It does not move sideways**: its place is where the conversion drew it.
  `MovePicture` moves it up or down —the layer is taller than the screen if
  the picture is— and changes its tone, transparency, saturation and waves.
* **Waves show the edges mirrored**, if the picture goes past the sides of
  the screen: RM2k shows what the picture has beyond them, and the console
  has no room for that. `GTest4` is 389 wide. If it does not go past them,
  like `ShipFlash`, what is outside is black, the same as in RM2k.
* **A cropped picture is only the console's window.** The ones the game
  asks for in `[graphics] cropped_pictures` —in ABL, the Diff photos, which
  are captures of the map— are not scaled: the 256x224 screen is cut out of
  them from the pixel the game says, which is where the ROM's camera is
  when they are shown. What RM2k shows outside that window is not in the
  cartridge, and the crop is the same wherever the `ShowPicture` puts it. A
  `MovePicture` that moves it up or down shifts it with the scaled ones'
  arithmetic —14 console lines for every 15 of RM2k—, not line by line: no
  cropped picture moves in the game.
* **105 colors**: seven palettes of fifteen, distributed per 8x8 cell by
  Adeleine. The photos and `GTest4` lose gradients.
* **Only one at a time**, and the ones tied to the map only if they cover
  the whole screen, which are drawn as if they belonged to the screen. The
  hovertram on 32, attached to the map and with the scene around it, is
  still not drawn.
* **The montage on 217** —the four photos at 50 %, one every six frames,
  with a white flash— loads each photo with the screen off: five frames of
  photo and three of black, without the white. The other option, only the
  flashes without photos, is captured for taro to choose: see the task named
  below.

## Measured

On the `release` cartridge, on 2026-10-02, with the test pages of
`test_imagenes_grandes_golden.py`, against captures of the six scenes from
the 2015 RPG_RT under Wine: see the task [`large-pictures-on-bg1-in-mode-1`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/large-pictures-on-bg1-in-mode-1.md),
in `tasks/` in the-advocate-work.
