# Large pictures in mode 1

## What

**Large `ShowPicture` pictures are drawn on BG1 in mode 1, only while they
are shown with the map covered.** The map always stays in mode 3, and
BG2 —the upper layer and the message window— doesn't change, because in
mode 3 it is already 4 bits.

## Why

From taro, on 2026-10-01, with option E of
[the picture system study](../research/2026-10-01-el-sistema-de-imagenes.md)
in front of him: "I'm OK with using mode 1". It doesn't contradict the
decision of 2026-09-05 that ruled out mode 1 **for the map** (the 256-color
background stays; see [Mode 3, always](../cartridge/mode-3.md)): here the
map isn't visible. It is the same thing that was evaluated for the menu in
mode 5.

## How it applies

The converter picks each picture's plane: small ones over the map go in
objects; large ones, with the map covered, on BG1 in mode 1, and when they
are erased it goes back to mode 3, reloading whatever it needs of the map.

Since 2026-10-03, one that a `MovePicture` scales up or down **does the
zoom in mode 7**, with a texture of 255 similar tiles, and when still it
stays here, in mode 1 at full resolution: it is the hybrid vq variant taro
chose in the pilot. See the task `las-fotos-en-modo-7.md` in
the-advocate-work.
