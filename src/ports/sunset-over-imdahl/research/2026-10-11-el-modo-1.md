# Mode 1 for the painted maps (2026-10-11)

> **Measured on 2026-10-11** by Mulita, on the game's dump in
> the-advocate-ports `36adb9a`, with the tools of the-advocate `06b8321f`
> and the branch that followed. It is a snapshot: the numbers are from that
> day and this file is not updated.

After [the pictures went into the map](2026-10-11-las-imagenes.md), taro
looked at the captures: "it really isn't playable. It isn't a good game to
port to the SNES, but I would try mode 1 and colour math before anything
else". This is what each of the two buys, measured.

## What weighs most: the mosaic

The squares (40x30 RM2k cells) and the streets (20x30) are paintings of
2,000 to 4,800 distinct 8x8 cells. In mode 3 the panorama got 576 tiles,
and Adeleine's grouping drew most cells with somebody else's: a mosaic of
the wrong pieces. Mode 1 puts the painting in BG1 at 4 bits, where it could
get close to a thousand tiles; uploading only what the screen shows gives
each cell its own.

Mean error per pixel —the three channels' absolute differences at 5 bits,
summed— against the panorama file, and the share of cells with more than 8
pixels off by more than 6, converted by the real Adeleine and Voodoo:

| panorama | 576 grouped | 960 grouped | one tile per cell |
|---|---|---|---|
| TownSquareSpring, 640x480 | 10.53 · 85.6 % | 9.45 · 82.1 % | 2.30 · 20.7 % |
| TownSquareWinter | 8.59 · 72.7 % | 7.57 · 66.3 % | 2.12 · 8.9 % |
| TownSquareSummer | 10.83 · 89.4 % | 9.92 · 84.7 % | 2.56 · 21.7 % |
| TownSquareAutumn | 8.59 · 78.2 % | 7.71 · 70.6 % | 1.88 · 6.5 % |
| TheStatueBeoyondSeasons, 320x480 | 4.91 · 42.9 % | 3.24 · 26.8 % | 0.92 · 0.4 % |
| GateStreet, 320x480 | 5.15 · 40.0 % | 3.37 · 24.7 % | 0.94 · 0.3 % |
| InnSpring, 320x240 | 3.36 · 30.7 % | 1.62 · 6.2 % | 1.59 · 4.6 % |
| BarSpring, 320x240 | 3.06 · 28.7 % | 1.35 · 3.0 % | 1.35 · 2.7 % |

* **Twice the tiles does not fix the squares**: 10.5 to 9.4. It does fix
  the interiors of one screen, which have about 1,200 cells.
* **A tile per cell fixes everything**, and what is left —2 per pixel— is
  the colours: seven palettes of fifteen for the whole map, 85 to 102 kept
  of 800 to 1,600.

So only the second went in: [the painted maps](../../../internals/vram.md#a-painted-map-keeps-only-what-the-screen-shows),
for every map whose panorama is the map, 60 of the 65, the interiors too.

## The roofs

In mode 3 what goes in front of the hero went by whole 8x8 cells. In mode
1 there is a layer for the edges: BG2 at priority 1, with the painting's
own cell and only the roof's pixels, in its palette, so it costs no colour.
BG2 has 127 tiles for it; the maps with more edges send the rest by whole
cells. Of 1,586,793 pixels in front of the hero over the 60 maps, 34,895
end up on the wrong side (2.2 %); on the spring square, 2,250 of 84,145,
against 5,831 by whole cells.

## Colour math: where it would go, and why it did not

The study proposed colour math for the shadows and the lights, so that
they reach the characters. Measured against what the hardware does:

* **It does not reach every character.** Colour math applies to objects
  only with palettes 4 to 7, and Sunset's maps use all eight: on the
  spring square, at frame 240 of the capture, objects with palettes 0, 3,
  6 and 7 are on screen. A shadow would darken some characters and not
  others.
* **There is no VRAM for its mask.** A shadow is a shape, so it needs a
  layer —BG3 at 2 bits, on the subscreen— with its tilemap and its tiles.
  With the painting's slots the layout has 1,024 words left, $5C00 to
  $5FFF: a 32x32 tilemap and no tiles, or tiles and no tilemap.
* **The painting does not need it.** The shadows, lights and mists are
  blended into the painting before it is converted, and now that every
  cell is its own they come out as they are.

What is lost is what [Pictures drawn into the map](../../../divergences/las-imagenes-dentro-del-mapa.md)
says: the characters are neither shaded nor lit, and nothing changes over
time. To shade them, the converter would have to give the characters
palettes 4 to 7 on these maps, and the roofs' edges would have to give up
half of BG2's tiles for the mask's.

## How it was measured

* The table: a throwaway example of Wally that runs `panorama::mode3` with
  576 and 960 tiles and `painted::painted` on the panorama files, and
  compares each decided picture with the file.
* The roofs: the converter's own count, "its pictures put N pixels in front
  of the hero, and M go to the wrong side of him", over the `release`
  cartridge.
* The objects' palettes: the OAM of a capture cartridge on the spring
  square.
