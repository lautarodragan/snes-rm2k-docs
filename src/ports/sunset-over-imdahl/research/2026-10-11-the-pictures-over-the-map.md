# The pictures over the map (2026-10-11)

> **Measured on 2026-10-11** by Mulita, on the game's dump in
> the-advocate-ports `b499ab4`, with the tools of the-advocate `6f933ff8`.
> It is a snapshot: the numbers are from that day and this file is not
> updated. How to redo each count is at the end, in "How it was measured".

Sunset Over Imdahl draws its roofs, ceilings, lights, shadows and mists
with `ShowPicture`. Until this study the console carried every one of them
as a big picture —BG1 in mode 1, with the map hidden—, so a scene with one
of them was black or showed the picture over black ([the opening scene,
2026-10-11](../README.md#the-opening-scene-in-black-2026-10-11)). taro
decided not to leave them out: "it is a very artistic game; without those
pictures it probably loses all its charm". This is how the game uses them,
grouped by use, and what each group would ask of the console.

## Summary

* **Sunset is a painted game.** Every map but the title one has a
  panorama the size of the map, fixed to it, and the ChipSet draws nothing
  on 63 of the 65 maps —the exceptions are the title map, 11, and the test
  map, 39—: the map *is* the painting. The converter already carries it
  that way —on 55 maps the panorama in BG2 at 4 bits with BG1 empty, on 8
  small ones baked into BG1 at 8 bits—, and without its pictures the game
  looks right except that **the hero walks over the roofs** and the
  lights, shadows and mists are missing.
* **The pictures are the map's other layers.** Following the `Teleport`s
  —the game shows the destination's pictures in the door event of the map
  it leaves, after the jump— **62 of the 65 maps** show pictures that stay
  put on the map for as long as one is there. They come in a fixed order:
  number 1 the roofs or the ceiling, 2 and 3 the shadows and lights, 3 to
  6 the mists.
* **The roofs are cut-outs of the panorama**: 83.7 % of their pixels are
  the same as the panorama under them —100 % on the town squares, the
  statue alley and the spring bar—. What they say is *which part of the
  painting goes in front of the hero*: RM2k's layer above the hero, for a
  painted map. On the console that is **the priority bit of the
  panorama's own cells**: no tiles, no colours.
* **Shadows and lights are flat masks** —3 to 8 colours, one shape— at 10
  to 35 % opacity, and **the mists are full-screen textures** at 2 to 55 %.
  In mode 3 there is no layer left for any of them: BG1 and BG2 are taken,
  the windows of colour can't draw the shapes and the objects can't cover
  the screen. What fits without changing the mode is **to blend them into
  the panorama**, which loses that the characters are not shaded and every
  change over time.
* **What a third layer would buy**, mode 1 for the painted maps, is in
  "Mode 1 for a painted map": exact roofs at no colour cost and shadows by
  colour math. It is an architecture decision, and it is taro's.

## How the game uses them

### What a map shows

The pictures that make a map's look are shown in three places:

* **in the door of the map one leaves**, after the `Teleport`: a touch
  event at the edge of the street jumps to the square and then shows the
  square's roofs, shadows and lights. 1,678 picture commands in all; most
  of the `ShowPicture`s are in pages of a map other than the one where
  they are seen;
* **in an automatic or parallel page of the map itself**, for the maps
  reached by a scene;
* **in the common events**, only the game's own menu (see "The menu and
  the boxes").

They are erased the same way, in the door, before the jump. Only 20
`ErasePicture` in the game run with no `Teleport` after them in their page,
and 12 of those are of picture 20, the upside-down text box.

### Where they land on the map

A picture fixed to the map takes its position on the screen at the moment
it is shown and then moves with the map (`Game_Pictures::OnMapScrolled` in
easyrpg). Taking RM2k's camera from the `Teleport` that comes before it in
the page, **every map-fixed picture of the game lands with its corner on
the map's corner** —the 640x480 roofs of the 40x30 squares, the 320x480 of
the 20x30 streets—, or centred on the map, the two mists 16 and 8 pixels
wider than it. The four that are shown with no jump before them (maps 10,
5 and 58) have no known camera; centred on the map they land where the
others do.

The ones fixed to the screen are of two kinds: on a map of one RM2k
screen, which RM2k's camera never scrolls, they are fixed to the map as
well (the interiors: 109 shows); on a map that scrolls they are the mists
(170 shows of the 242 mists), which go with the screen on purpose.

### By group

Counted by where each picture is seen (`Teleport`s followed). "Opacity" is
`100 - transparency` at the show and after the `MovePicture`s that follow
it in its page.

| group | files | shows | maps | colours | transparent colour | opacity | where |
|---|---|---|---|---|---|---|---|
| roofs and ceilings | 55 | 350 | 61 | 74-254 | 52-99 % of the picture | 100 % | map, or screen on a one-screen map |
| lights | 46 | 232 | 50 | 3-255 (most 3-8) | 0-99 % | 10-35 %, some 60 % | map, or screen on a one-screen map |
| shadows | 18 | 243 | 22 | 3-5 (one of 118) | 49-95 % | 10-30 % | map |
| mists | 8 | 242 | 38 | 5-255 | 0-65 % | 2-55 % | screen: 170 on maps that scroll |
| animated | 9 | 22 | 7 | 43-135 | 83-100 % | 100 % | map | 
| menu and boxes | 17 | 42 | 11 + common | 1-254 | 0-93 % | 50-100 % | screen |
| title, credits, scenes | 11 | 12 | 6 | 13-252 | 0-98 % | 0-100 % | screen |

**Roofs and ceilings** —`TownSquareSpringRoofs`, `BarSpringCieling`,
`TheStatueWinterRoofs`…— are always number 1 (number 2 or 5 on three
maps), opaque, with the transparent colour over half or more of the
picture. 311 of 350 shows are at the neutral tone; 29 appear black and a
`MovePicture` takes them to their colour in 0.5 to 2.5 seconds, with the
screen tint that the scene does at the same time (RM2k does not tint
pictures with the screen). They never move. Two variants of the same
place under one number appear in 4 maps —an inn with or without its
second ceiling, the square of the silhouette game—.

**Lights** are mostly a single flat colour —yellow, warm white— in 3 to 8
colours, the shape of the light from a window or a door, at 65 to 90 %
transparency; 78 shows brighten them with the tone `(200, 200, 180, 120)`.
A few are painted (`InnAutumnLight`, 193 colours, a whole room at 80 %).

**Shadows** are flat black or near-black in 3 to 5 colours, the shape of
the buildings' shadow, at 70 to 90 %. They are the most regular group: 234
of 243 shows are fixed to the map, at the neutral tone.

**Mists** are textures over the whole screen —`WinterMist`, `AutumnMist`,
`ThickWinterMist` (a frame with a hole), `SummerOverlay` (sun rays)—, at
45 to 98 % transparency. `SummerOverlay` waves (effect 2, strength 1) on 84
shows, at 95 to 100 %. Most are fixed to the screen on maps that scroll:
the mist does not move when the hero walks. Some fade in or out in 1 to 4
seconds when a scene starts or ends.

**Animated**: the flags of the town wall and the mass grave —three
pictures under one number, swapped by a parallel page—, the grass of the
field (34), which moves, the clouds of 58, which drift, and the hole in the
inn's floor (51).

**The menu and the boxes** are the game's own menu, drawn with pictures
from common events 15 to 20 —`Meny`, `ChoiseMeny…`, the season sign, the
glove— and the upside-down text box. They are small (at most 192x160) and
go to the objects, as ABL's signs do; whether they fit is the objects'
question, and today several maps say they don't. Not studied here.

**Title, credits and scenes**: the publisher's card and the title on 1,
the title on 11 —which zooms—, the credits over the ruins on 35, the
raspberry accident and the minigame's frame. They are what big pictures
were made for, except the credits, which in RM2k go over the map.

### What lives together

At most six at once, on the misty street (33): mist, mist, roofs,
shadows, dense light, light. The usual is three: roofs, shadows or lights,
and a mist. In RM2k they stack by number, higher on top, so the shadows
and lights fall on the roofs too.

## What each group asks of the console

The maps already take the two layers of mode 3: BG1 for the ChipSet's
lower layer —empty here— and BG2 for the panorama at 4 bits and the
message window. The VRAM of a map with its panorama in mode 3 is one of
the `LAYOUT_PANORAMA_MODE3*` ([the VRAM split](../../../internals/vram.md)):
256 to 448 tiles of 8 bits for BG1, 256 to 576 of 4 bits for the
panorama, with 576 the common one. CGRAM: the panorama takes up to seven
palettes of fifteen —today 61 to 83 colours kept of 230 to 256— and BG1,
being empty, one.

### Roofs and ceilings

* **What it needs**: what RM2k's layer above the hero is, for a painting.
  Since the roof is the painting itself, **setting the priority bit of
  the panorama's cells it covers** puts them in front of the hero —in
  mode 3 BG2 at priority 1 is in front of objects at 1—: no tiles, no
  colours, nothing in RAM. Where the roof is not the painting, it is
  drawn into it first.
* **What it costs**: nothing in VRAM or CGRAM. ROM: the same bytes.
* **What it loses**: the grain. A whole 8x8 cell goes in front of the
  hero or behind: measured with a cell in front when the roof covers half
  of it or more, **5 to 21 % of the roof's pixels go to the wrong side**
  (4.8 % on the statue alley, 6.9 % on the spring square, 21 % on the
  spring bar, whose beams are thin). Also, the events "above the hero"
  (objects at priority 2) are in front of the roof, which in RM2k they are
  not.
* **Exact**: the cells the roof covers only in part —40 to 395 per map—
  in BG1 at priority 1, with only the roof's pixels and the panorama's
  colour entries (an 8-bit pixel names any entry, so it needs no palette
  of its own). It costs those cells in BG1, 2.5 to 25 KB, which the
  layouts give BG1 (256 tiles of 8 bits); the two largest, the misty
  street and the square, would group some. And the mask of BG1 under the
  message window that a flattened map already uses.

### Shadows and lights

* **What it needs**: a darkening or a brightening by a fixed amount,
  inside a shape. The console does that with **colour math** —subtract or
  add, or half and half with a fixed colour— on what a layer marks. In
  mode 3 there is no layer left to mark it with; the **windows of colour**
  draw at most two spans per line, and a shadow has dozens; **objects**
  would need 1,200 of 16x16 for the 640x480 shadow of a square, against
  128. So in mode 3 the only place is **the panorama itself: the shadow
  blended into the painting** at its opacity, before it is converted.
* **What it costs**: nothing in VRAM or CGRAM; the panorama's colours and
  tiles absorb the blend —it already merges from 250 to 80 colours and
  groups 1,000 to 4,800 cells into 576—.
* **What it loses**: the characters are not shaded when they walk into a
  shadow, nor lit by a light; any change over time —a light that comes
  on in four seconds on 27 and 43, a shadow that fades out at the end of
  a scene— is not done; the picture is where it settles.

### Mists

* **What it needs**: a texture over everything, at 2 to 55 % opacity. The
  console blends only at 50 % or adds, and a texture would need a layer.
  A uniform haze —the average colour of the mist at its opacity— is
  almost what a mist at 90 % or more is, and could be done with the
  fixed colour of colour math and the screen's brightness, over
  everything including the characters; that is a project of its own.
* **In the first version**: blended into the painting like the shadows.
  The ones fixed to the screen on a map that scrolls **are repeated over
  the whole map** from where they are shown, so that wherever the camera
  goes there is mist, as in RM2k; the seam between repeats is at 2 to
  30 % opacity.
* **What it loses**: the mist moves with the map instead of staying on the
  screen, it does not cover the characters, and the wave of `SummerOverlay`
  is not done (at 95 % transparency it is hardly visible in RM2k either).

### Animated

* The flags and the hole in the floor would be **an animation of the
  panorama's tiles**, the machinery of the ChipSet's animated tiles —a run
  of tiles that a DMA replaces—, which today exists only for BG1. The
  grass and the clouds move whole pictures: they would be their own
  layer.
* **In the first version** the flags stay still in the frame shown most
  and the grass and the clouds stay big pictures.

### Title, credits and scenes

They stay big pictures, as in ABL. The credits on 35 go over the black
instead of over the ruins.

## Mode 1 for a painted map

**Not done: it changes [Mode 3, always](../../../internals/mode-3.md) and
[Color math isn't used](../../../decisions/translucent-events-dont-use-color-math.md), and
that is taro's to decide.** Written here because Sunset makes the case
for it.

Mode 3 is fixed because ChipSet tiles have 16 to 19 colours. A painted
map has no ChipSet tiles: its painting is already converted at 4 bits,
in palettes of fifteen —BG2 in mode 3—, and its 8-bit layer is empty. In
mode 1 it would lose nothing and gain a third layer:

* **BG1, the painting at 4 bits**, as today in BG2;
* **BG2, the roofs at 4 bits, with BG1's own tiles**: BG1 and BG2 can share
  a tile base, so the cells the roof covers whole are the same tiles —no
  extra ones— and only the edge cells, 40 to 395, are new, at half the
  bytes of an 8-bit tile. Same palettes, exact edges;
* **BG3 at 2 bits, the shadows or the lights**, as a mask for colour math:
  2 to 5 colours fit in 3, the 640x480 shadow of a square is 2,178 cells
  with something, 1,432 distinct, and a light 990 and 731; they would be
  grouped like the panorama's. Colour math subtracts or adds a fixed
  colour where BG3 draws, over the characters too; it does one of the two
  at a time, so one of shadows and lights would still be blended into the
  painting, and its strength is the fixed colour's, not a percentage.
* The message window, today in BG2, would have to share BG2 with the roofs
  —as it shares it with the panorama today— or go to BG3.

It is a new layout and a third way of drawing a map, next to mode 3 and
`panorama_m1`. Its cost and its gain should be measured on the squares,
which are the most demanding.

## What was chosen for the first version

The groups that weigh most are the roofs (61 maps), the lights (50) and
the mists (38). In mode 3 and with no new layer: the roofs as the
priority of the panorama's cells and everything translucent blended into
the panorama, for the pictures that stay put on the map; the rest as
before. See [Sunset Over Imdahl](../README.md).

## How it was measured

With throwaway scripts over the dump (`data/maps/*.json` and
`data/db/commonevents.json` of the port) and the game's `Picture/` and
`Panorama/` folders:

* **the commands**: every `ShowPicture` (11110), `MovePicture` (11120) and
  `ErasePicture` (11130) of every page, with the picture's file opened for
  its size, its colours and how much of it is index 0;
* **where it is seen**: walking each page in order, a `Teleport` (10810)
  changes the current map; the camera after it is RM2k's
  (`Game_Player::GetDefaultPanX`: the hero nine cells from the left and
  seven from the top, clamped to the map);
* **the groups**: by the file's name —`Roof`/`Cieling`, `Light`,
  `Shadow`, `Mist`/`Overlay`, and the menu's and the cards' by name—;
* **the roofs against the panorama**: each opaque one's non-transparent
  pixels compared one by one with the panorama of the map where it is
  seen, at the corner it lands on;
* **the grain**: per 8x8 cell of each roof, the pixels on the wrong side
  with a cell in front when half or more is roof;
* **the panoramas**: `conversor.log` of the `release` cartridge built with
  the tools named at the top, and the images Adeleine writes in
  `build/release/adeleine/`.
