# Lossy: pictures and animations

## Battle animations on the map, shrunk to a box

A battle animation on the map is shrunk, whole and keeping its
proportions, to a 64x64 box, and without alpha: an object is opaque or not
there. If the space they need in the sprite bank is the only thing that
does not fit, the map is built without them.

- **Loses**: big animations look small; a fading cell disappears at once.
- **Where**: `fit_size` in `rm2k-snes/images/src/animation.rs`.
- **More**: [The shrunk battle animation](../../divergences/the-shrunk-battle-animation.md),
  [Seven palettes on a map with animations](../../divergences/seven-palettes-on-a-map-with-animations.md).

## Pictures in sprites: scaled, fifteen colours

A small `ShowPicture` picture goes in sprites, with one sprite palette, and
one tied to the screen is scaled from RM2k's 320x240 to the console's
256x224.

- **Loses**: gradients band; the scaling; transparency in three steps.
- **Where**: `rm2k-snes/images/src/show_picture.rs`; `runtime/picture.s`.
- **More**: [What pictures as sprites do not model](../../divergences/what-pictures-as-sprites-do-not-model.md).

## Big pictures in mode 1, 105 colours

A picture that covers the screen goes in BG1 at 4 bits, in seven palettes
of fifteen that Adeleine distributes per 8x8 cell.

- **Loses**: gradients in photos.
- **Where**: `rm2k-snes/images/src/fullscreen.rs`; `runtime/big_picture.s`.
- **More**: [What large pictures do not model](../../divergences/what-large-pictures-do-not-model.md),
  [Large pictures in mode 1](../../decisions/large-pictures-in-mode-1.md).

## The zoom in mode 7, with a 255-tile texture

A big picture that a `MovePicture` scales does the zoom in mode 7, whose
texture holds 256 tiles: each place in the picture shows the closest of
them. Still, it is shown at full resolution in mode 1.

- **Loses**: during the zoom, noisy photos show pieces of other tiles, and
  the grain flickers as it shrinks.
- **Where**: `runtime/big_picture_zoom.s`; `rm2k-snes/images/`.
- **More**: [What large pictures do not model](../../divergences/what-large-pictures-do-not-model.md).

## The title at 16 colours a tile when it does not fit

If the title's picture does not fit in VRAM next to the menu at 8 bits, it
goes at 4 bits in mode 1, in seven palettes Adeleine chooses for it, where
it always fits.

- **Loses**: colours of the title picture.
- **Where**: `compressed_4bpp` in `rm2k-snes/convert/src/fullscreen.rs`;
  `title_upload` in `runtime/title.s`.
- **More**: [The VRAM split](../../internals/vram.md#the-title-screen-doesnt-use-the-layout).

## Light battle backdrops in the ROM

The ROM carries the backdrops at half size and 4 bits, 16 colours, which
the console doubles; the `.msu` carries them whole, at 8 bits.

- **Loses**: without MSU-1, the backdrops' resolution and colours.
- **Where**: `scene.rs` in `rm2k-snes-convert`.
- **More**: [The `.msu` file](../../internals/the-msu-file.md).
