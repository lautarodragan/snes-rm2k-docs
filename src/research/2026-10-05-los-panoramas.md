# Panoramas

> **Written on 2026-10-05 at `9b180286`** (snes-rm2k), by Cardón, with ABL
> at `a94288b`. It is a snapshot: the numbers are from that day and this
> file is not updated. How to redo each count is at the end, in "How it was
> measured".

The panorama is RM2k's parallax background: an image behind the map that
shows wherever the lower layer doesn't draw, and that moves on its own or
with the camera at a different speed than the map. In the port it comes
out black. taro, on 2026-10-05: some can be solved with patches —the
emitter room, the director's office window—, but others "are pretty
important … especially when they do have a parallax effect and move at a
different speed than the map": the bridge from above, the one from below,
the Lashe City rooftop and the intro with Kersh.

The assignment: measure every map with a panorama, get the two bridge ones
working —the one from above with path A, the one from below with B—,
measure the rooftop and the intro, and say what it costs. Without taking it
to the whole game.

## Summary

* **Of the 45 maps with a panorama, 4 never show it and 9 barely do** (a
  window, a gap), and another 4 don't move against the map: 17 that don't
  ask for a layer. See "The 45".
* **Both bridge ones work**, on Cardón's branch: the one from above (259)
  in mode 3 with the panorama in BG2 at 4 bits, the one from below (255) in
  mode 1 with the panorama in BG3 at 2 bits. They move like
  `Game_Map::Parallax`, and 259's **lands on the same pixel as in the
  original** —measured against RPG_RT under Wine—. The captures accompany
  this study in that day's delivery, `2026-10-05-panoramas`.
* **What limits is not the layer but the colors and the tiles.** A
  panorama brings between one and four thousand distinct tiles and VRAM
  leaves it 576 (A) or 768 (B): similar ones are grouped (Adeleine,
  `group_tiles`), and it shows in the grain, slightly. And the RTP ones
  have 8x8 cells with up to 50 colors: **at 4 bits they end up with about
  15** and look almost the same; **at 2 bits they end up with 4** and the
  clouds flatten.
* **So B, as requested, works for 255 and not for the RTP ones.** For the
  maps that draw something above the hero there is a better path almost
  always: **mode 3 with the above-hero part drawn below**, when that is
  little —two cells on the Lashe rooftop, fourteen on the overlooks—. And
  for the ones that don't move, **bake the panorama into the background**,
  with no layer. See "Better than A and B".
* **The rain already coexists**: it is made of objects, and touches
  neither the layers nor the lower half of CGRAM. Tried with the intro: it
  rains over the panorama. The only thing that had to be done was to raise
  its priority in mode 1.
* **The cost**, with the two bridge ones: 41 KB of uncompressed ROM, 224
  bytes of far RAM, about 100 bytes of bank 0 and 1.6 KB of `FAR2`. See
  "The cost".

## What RM2k does

`Game_Map::Parallax`, in `easyrpg-player`, in its units: the panorama's
position, `pan_x`, is in 1/32 of a pixel, and on screen the panorama
starts at its pixel `pan_x / 32`.

* **One that loops on an axis** starts at the camera's position and adds
  what the camera moves: since the camera is in 1/16, the panorama goes
  **at half**. If it also moves on its own, each frame adds
  `-(1 << speed)` —or `1 << -speed`—: speed 1 is 1/16 of a pixel per
  frame, 8 is 8 pixels.
* **One that doesn't loop** goes from its first pixel to its last while
  the camera goes from one edge of the map to the other: `min(w, width -
  320) * camera / w`, with `w` what the camera travels. On a one-screen
  map it doesn't move.
* **It has no transparent color**: index 0 is drawn, unlike a ChipSet.
  Until it was loaded that way, 259 came out with a strip of black dots.
* **RM2k's camera is not the console's.** RM2k puts the hero nine cells
  from the left edge and seven from the top
  (`Game_Player::GetDefaultPanX`) on a 320x240 screen; the console centers
  it on 256x224. The prototype places the panorama **behind RM2k's
  camera** and shifts it by how far the console's is from that one: that
  way it stays behind the map where RM2k puts it, and a capture of the
  original matches the piece the console shows.
* **`ChangePBG` changes the panorama mid-map.** Only one page in the game
  uses it, the Hover-Tram trip (13). The prototype doesn't do it: it is
  still accepted and dropped.

## A correction to the assignment

Path A said "the lower layer uses only colors 128 to 255". **The upper half
of CGRAM belongs to the sprites** (`docs/port/cgram.md` in snes-rm2k): the
8-bit background could read those entries, but it would have to settle for
the characters' colors. What A splits is the lower half, as today between
the background and the upper layer: **the background chooses first** the
palettes it needs and the panorama gets the ones left over. On 259 the
background has 18 colors and the panorama is left with three palettes,
which are enough for its 30 colors without merging any.

## The 45

Measured with the prototype's converter on each map, even if it is not in
`release` ("out"). The columns:

* **moves**: "x ½" is looping with the camera, at half; "x own +3" is also
  its own speed; "with the camera" is no loop, end to end.
* **visible**: what part of the lower layer is transparent, that is, where
  the panorama peeks through. Zero means it is never visible.
* **above**: how many tiles the above-hero part has; zero means the map
  fits in A.
* **background**: tiles and colors of the lower layer, without the
  panorama.
* **mode**: the one the prototype chose: 3 if there's nothing above, 1 if
  there is.
* **panorama**: tiles left out of the distinct ones it has —counting
  flipped ones as one—, and colors left out of the ones it brings.

| map | | size | panorama | moves | visible | above | background: tiles, colors | mode | panorama: tiles of distinct, colors |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Introduction; rain | 100x100 | Night1 640x480 | x own +3 | 23% | 52 | 338, 49 | 1 | 729 of 862, 4 of 58 |
| 2 | Linkage Block | 100x100 | screen 320x240 | y own +4 | 28% | 63 | 272, 60 | 1 | 725 of 806, 5 of 11 |
| 3 | Emitter Room; patch: emitter | 75x75 | Weird 640x480 | y own -6 | 0% | 16 | 256, 75 | 1 | 617 of 4800, 4 of 254 |
| 6 | CoreRetro II | 100x100 | Night2 640x480 | with the camera | 74% | 22 | 78, 39 | 1 | 715 of 1814, 4 of 40 |
| 8 | Lashe City - 34,35 | 75x75 | Planet1 320x240 | with the camera | 0% | 0 | 400, 63 | 3 | 419 of 938, 17 of 227 |
| 13 | Hover-Tram; ChangePBG | 20x15 | Evening2 640x480 | x own +5 | 1% | 0 | 42, 22 | 3 | 576 of 1441, 15 of 157 |
| 16 | Running To Work Scene | 75x75 | Evening1 640x480 | with the camera | 22% | 0 | 332, 62 | 3 | 576 of 1058, 15 of 136 |
| 19 | Talan and the Director; patch: director's window | 20x15 | OfficeView 640x320 | with the camera | 5% | 0 | 134, 51 | 3 | 575 of 1195, 20 of 168 |
| 32 | Sector 27 Warehouse | 50x50 | Dawn1 640x480 | with the camera | 42% | 4 | 210, 58 | 1 | 726 of 935, 4 of 79 |
| 33 | Escape From 27 Scene | 50x50 | Dawn1 640x480 | with the camera | 14% | 5 | 222, 54 | 1 | 726 of 935, 4 of 79 |
| 34 | AfterGettingCarCutscene; patch: director's window | 20x15 | OfficeView 640x320 | with the camera | 5% | 0 | 154, 62 | 3 | 575 of 1195, 20 of 168 |
| 43 | Vidcasts (Office); patch: director's window | 20x15 | OfficeView 640x320 | with the camera | 5% | 0 | 154, 62 | 3 | 575 of 1195, 20 of 168 |
| 45 | Security Footage; patch: director's window | 20x15 | OfficeView 640x320 | with the camera | 5% | 0 | 134, 51 | 3 | 575 of 1195, 20 of 168 |
| 51 | Jumping the Bridge | 200x40 | lashepan 640x320 | x own -4 | 57% | 0 | 217, 58 | 3 | 573 of 3154, 20 of 179 |
| 64 | Leaving Lashe City Scene | 20x15 | lashepan 640x320 | with the camera | 43% | 0 | 100, 34 | 3 | 559 of 1182, 17 of 133 |
| 76 | Sorbe Mountain | 30x50 | Morning1 640x480 | with the camera | 0% | 55 | 164, 59 | 1 | 621 of 663, 4 of 89 |
| 82 | Director'sOfficeNextStep; patch: director's window | 20x15 | OfficeView 640x320 | with the camera | 5% | 0 | 134, 51 | 3 | 575 of 1195, 20 of 168 |
| 94 | Missiles On Their Way1 | 20x15 | pan2 640x480 | y own +8 | 100% | 0 | 1, 0 | 3 | 576 of 947, 17 of 51 |
| 95 | Into The Machine | 50x50 | TasgardePan 640x320 | with the camera | 50% | 3 | 160, 39 | 1 | 765 of 1084, 4 of 7 |
| 96 (out) | Backup | 20x15 | Dawn1 640x480 | with the camera | 1% | 12 | 96, 60 | 1 | 218 of 232, 4 of 79 |
| 99 | Missiles On Their Way2 | 20x15 | pan2 640x480 | y own +8 | 100% | 0 | 1, 0 | 3 | 576 of 947, 17 of 51 |
| 104 (out) | Overlook Memory | 20x30 | Night1 640x480 | x own -2 | 40% | 8 | 120, 14 | 1 | 729 of 862, 4 of 58 |
| 105 | Mountain Path | 70x30 | Evening1 640x480 | x own +2 | 41% | 55 | 72, 44 | 1 | 724 of 1058, 4 of 136 |
| 109 | Paradise Overlook | 20x30 | Night1 640x480 | y ½ | 40% | 8 | 120, 14 | 1 | 417 of 433, 4 of 57 |
| 126 | OverlookAtDay | 20x30 | Morning1 640x480 | x own +1, y ½ | 40% | 8 | 120, 14 | 1 | 721 of 903, 4 of 89 |
| 167 (out) | Outside the Bandit HQ | 20x40 | Evening1 640x480 | y ½ | 0% | 0 | 40, 43 | 3 | 458 of 522, 15 of 136 |
| 175 | Mountain Flashback | 20x15 | Night1 640x480 | with the camera | 23% | 0 | 101, 12 | 3 | 218 of 217, 15 of 56 |
| 176 | Overlook | 20x15 | Night1 640x480 | with the camera | 80% | 0 | 19, 21 | 3 | 218 of 217, 15 of 56 |
| 203 (out) | Up The Overlook | 20x30 | Night1 640x480 | y ½ | 40% | 8 | 120, 14 | 1 | 417 of 433, 4 of 57 |
| 205 (out) | Beach Scene | 20x30 | Night1 640x480 | with the camera | 10% | 0 | 49, 51 | 3 | 433 of 433, 15 of 57 |
| 224 (out) | Overlook Memory; rain | 20x30 | Night1 640x480 | y ½ | 40% | 8 | 120, 14 | 1 | 417 of 433, 4 of 57 |
| 227 (out) | Leaving Lashe Memory | 20x15 | lashepan 640x320 | with the camera | 43% | 0 | 100, 34 | 3 | 559 of 1182, 17 of 133 |
| 228 (out) | Assassination Memory; patch: director's window | 20x15 | OfficeView 640x320 | with the camera | 5% | 0 | 134, 51 | 3 | 575 of 1195, 20 of 168 |
| 236 (out) | Kersh On The Overlook | 20x30 | Night1 640x480 | y ½ | 40% | 8 | 120, 14 | 1 | 417 of 433, 4 of 57 |
| 241 (out) | Tram to Prima | 20x15 | PrimaTunnel2 640x480 | x own -7 | 25% | 0 | 109, 45 | 3 | 576 of 1393, 17 of 63 |
| 255 | Under the Bridge | 75x25 | undrbrdgpan 640x320 | x own +1, y own +1 | 56% | 8 | 66, 39 | 1 | 768 of 1760, 4 of 6 |
| 259 | Northern Highway Bridge | 70x15 | seapan 640x320 | with the camera | 82% | 0 | 16, 18 | 3 | 576 of 1435, 30 of 30 |
| 260 (out) | Surl Highway | 70x15 | desertpan 640x320 | with the camera | 80% | 0 | 21, 10 | 3 | 576 of 1840, 13 of 13 |
| 267 (out) | Kersh and the Droid Army | 70x15 | desertpan 640x320 | with the camera | 80% | 0 | 21, 10 | 3 | 576 of 1840, 13 of 13 |
| 268 (out) | Emitter Room; patch: emitter | 20x15 | Weird 640x480 | y own -6 | 1% | 8 | 128, 60 | 1 | 666 of 2400, 4 of 254 |
| 300 (out) | Missiles2 | 20x15 | pan2 640x480 | y own +8 | 100% | 0 | 1, 0 | 3 | 576 of 947, 17 of 51 |
| 301 (out) | The Overlook | 20x30 | Dawn1 640x480 | x own -1 | 40% | 8 | 120, 14 | 1 | 726 of 935, 4 of 79 |
| 303 (out) | Tram to Prima | 20x15 | PrimaTunnel2 640x480 | x own -7 | 25% | 0 | 109, 45 | 3 | 576 of 1393, 17 of 63 |
| 306 (out) | Outside Ship | 20x40 | starpan 640x320 | y own +7 | 80% | 0 | 109, 41 | 3 | 51 of 50, 15 of 15 |
| 313 | Agency Tram | 20x15 | woodspan 640x320 | y own +3 | 39% | 0 | 118, 32 | 3 | 25 of 24, 7 of 7 |

Grouped by what they ask for:

* **Never visible** (0%): 3, 8, 76 and 167. The large emitter room (3) has
  the exterior in an opaque black tile, not a transparent one. Nothing to
  do, unless some event uncovers something.
* **Visible through a gap** (5% or less): the director's office —19, 34,
  43, 45, 82, 228: the window—, the small emitter room (268), the
  Hover-Tram (13) and 96. These are the ones taro said to solve with an ABL
  patch: the emitter as an animated tile or CharSet, the office window as
  a ChipSet. **Baking them** —see below— does the same without a patch,
  except 13, which moves on its own and changes panorama.
* **Still** —one RM2k screen, no speed of their own—: 64, 175, 176 (and
  227 out). They don't ask for a layer: they get baked.
* **They move and have nothing above**: 16, 51, 94, 99, 259, 313 (and out
  205, 241, 260, 267, 300, 303, 306). They are A.
* **They move and have something above**: 1, 2, 6, 32, 33, 95, 105, 109,
  126, 255 (and out 104, 203, 224, 236, 301). B, or better something else.

## Colors and tiles

**The tiles.** A 640x320 panorama with grain has more than a thousand
distinct tiles even counting flipped ones as one —seapan 1435, lashepan
3154, Weird 4800— and VRAM leaves it 576 in A and 768 in B. So similar
ones are drawn with a single one: a k-means over the tiles averaged two by
two, and each group with the one that most resembles the rest, which is
what `rm2k-snes-images` already did for the mode 7 textures. It ended up in
Adeleine as `group_tiles`, because it changes what is seen. On 259 it shows
in the grain of the sea and the clouds, and not at all in the shape: see
`capitulo-259-llegada.png` in the captures.

**The colors.** ABL's panoramas have few —seapan 30, desertpan 13,
woodspan 7, undrbrdgpan 6— and fit whole at 4 bits. The RTP ones are
gradients: 8x8 cells with 34 to 50 colors. At 4 bits a cell has 15, so
Adeleine merges until they fit, and they end up with about 15 in total;
**they look almost the same**, because they are neighboring grays and
blues. At 2 bits they end up with 4 —three per palette and the screen's
backdrop color—, and **the clouds flatten**: `rtp-night1-8-4-2-bits.png`
and `rtp-evening1-8-4-2-bits.png`, the original, at 4 and at 2.

And in B the map goes at 4 bits, with palettes of 15 per cell, and it also
merges: 255 from 39 to 22 —neighboring dark browns, which don't show—, the
intro from 49 to 20, the emitter from 75 to 19.

## Better than A and B

**Mode 3 with the above-hero part drawn below.** When what goes above the
hero is little, it is drawn in the background and the map fits in A. What
is lost is the hero passing behind those cells: on the Lashe rooftop there
are two (33), on the overlooks fourteen, on 255 the chains. Measured
forcing mode 3:

| map | mode 1: background, panorama | mode 3 with the above part below: background, panorama |
|---|---|---|
| 1 Introduction | 20 of 49, 4 of 58 | 55 of 55, 15 of 58 |
| 2 Linkage Block | 20 of 60, 5 of 11 | 69 of 67, 6 of 11 |
| 3 Emitter Room | 19 of 75, 4 of 254 | 78 of 78, 15 of 254 |
| 6 CoreRetro II | 28 of 39, 4 of 40 | 42 of 42, 15 of 40 |
| 32 Sector 27 Warehouse | 24 of 58, 4 of 79 | 60 of 60, 15 of 79 |
| 33 Escape From 27 Scene | 21 of 54, 4 of 79 | 54 of 54, 15 of 79 |
| 76 Sorbe Mountain | 19 of 59, 4 of 89 | 60 of 60, 15 of 89 |
| 95 Into The Machine | 30 of 39, 4 of 7 | 39 of 39, 7 of 7 |
| 96 Backup | 29 of 60, 4 of 79 | 60 of 60, 15 of 79 |
| 104 Overlook Memory | 14 of 14, 4 of 58 | 14 of 14, 15 of 58 |
| 105 Mountain Path | 22 of 44, 4 of 136 | 46 of 46, 15 of 136 |
| 109 Paradise Overlook | 14 of 14, 4 of 57 | 14 of 14, 15 of 57 |
| 126 OverlookAtDay | 14 of 14, 4 of 89 | 14 of 14, 15 of 89 |
| 203 Up The Overlook | 14 of 14, 4 of 57 | 14 of 14, 15 of 57 |
| 224 Overlook Memory | 14 of 14, 4 of 57 | 14 of 14, 15 of 57 |
| 236 Kersh On The Overlook | 14 of 14, 4 of 57 | 14 of 14, 15 of 57 |
| 255 Under the Bridge | 22 of 39, 4 of 6 | 43 of 43, 6 of 6 |
| 268 Emitter Room | 23 of 60, 4 of 254 | 61 of 61, 16 of 254 |
| 301 The Overlook | 14 of 14, 4 of 79 | 14 of 14, 15 of 79 |

(The background with the above part brings the colors of both layers:
that's why 2 ends up with more than it had.) It is in the branch —`"mode":
3` in `wally`'s request—, only for measuring: the cartridge doesn't ask
for it yet. The side-by-side comparison, in
`modo1-contra-modo3-con-lo-de-encima-abajo.png`: the rooftop (33), the
intro (1), the mountain path (105) and the daytime overlook (126), mode 1
on the left, mode 3 on the right. The above part could also be drawn with
objects instead of in the background, if there aren't many per screen
—on 255 there are 25, on the overlooks 12, in the intro 127—, but it
spends sprite palettes, which are already scarce.

**Bake the still ones.** On a one-screen RM2k map with no speed of its own
the panorama doesn't move against the map: it can be painted into the
lower layer at conversion time, and it asks for no layer and no mode. What
it costs is background:

| map | panorama | background tiles | background colors |
|---|---|---|---|
| 19 Talan and the Director | OfficeView | 134 → 200 | 51 → 131 |
| 34 AfterGettingCarCutscene | OfficeView | 154 → 213 | 62 → 136 |
| 43 Vidcasts (Office) | OfficeView | 154 → 213 | 62 → 136 |
| 45 Security Footage | OfficeView | 134 → 200 | 51 → 131 |
| 64 Leaving Lashe City Scene | lashepan | 100 → 612 | 34 → 155 |
| 82 Director'sOfficeNextStep | OfficeView | 134 → 200 | 51 → 131 |
| 175 Mountain Flashback | Night1 | 101 → 139 | 12 → 64 |
| 176 Overlook | Night1 | 19 → 215 | 21 → 77 |
| 227 Leaving Lashe Memory | lashepan | 100 → 612 | 34 → 155 |
| 228 Assassination Memory | OfficeView | 134 → 200 | 51 → 131 |

At 8 bits there are no per-cell palettes: the office keeps about 98 of
its 131 colors, against the 20 that A leaves it. The 612 tiles of 64 don't
fit in any layout and would ask for grouping. This also solves the
director's window, without a patch.

**Two more, untested.**

* **The panorama in BG2 at 4 bits and the above part in BG3 at 2 bits**,
  with BG3's priority above everything (bit 3 of `BGMODE`). The panorama
  doesn't flatten; the above part does, and it covers the message window,
  so an HDMA channel is needed to turn BG3 off on its lines. For the
  intro, which has 707 cells above, it's the one left.
* **The panorama in BG1 at 8 bits and the map in BG2 at 4 bits, with
  priority 1.** The panorama with all its colors, for the photographic
  ones —the office, lashepan—, in exchange for half the tiles and the map
  at 4 bits. The hero moves to priority 2, as in mode 1.

## The prototype

On Cardón's branch of the tools and on the `panoramas` branch of its ABL
clone, with `[maps] panoramas = [259, 255]` in `rm2k-snes.toml`. A map not
on that list converts as always, and a cartridge with none comes out with
the usual `.inc`.

**The converter.** `wally` receives in the request how many tiles each
mode leaves; it draws the lower layer transparent where there is nothing
(`render_over_panorama` in `rm2k-render`) and crops the panorama to what
the console can ever see —on 259, the top 240 rows—. If the map draws
nothing above the hero it goes in mode 3: the panorama takes the palettes
the background leaves, and they travel like the upper layer's, which is
what the register uploads, tints and restores (`background::panorama`). If
it does, it goes in mode 1: the map at 4 bits with its palettes from 2 on,
the above part as always, and the panorama at 2 bits in palettes 4 to 7 of
BG3 —entries 16 to 31—, with the color it draws most as the screen's
backdrop (`background::mode1`). Voodoo learned 2 bits. `rm2k-snes-mapdata`
has two new VRAM layouts, which `vram_layout` never gives to a map without
a panorama, and emits `pano_table`: per map, how it moves, its tiles and
its tilemap. See `panorama.rs`.

**The runtime**, `pano.s`:

* **The panorama is a ring.** It is 640 wide and the tilemap 512, so the
  console keeps a shifted position —`PANO_UX`—, which wraps where the
  tilemap and the panorama wrap at the same time, their least common
  multiple, and writes it as is into the scroll register. The tilemap has
  the 64 columns and 32 rows around, and each frame at most one column and
  one row are written, like the map's.
* **Where it goes** is `Game_Map::Parallax` with RM2k's camera, plus the
  distance to the console's. The quotient for the non-looping ones is
  exact: a 32-bit product and a long division.
* **Mode 3**: the panorama's tilemap is the upper layer's, and the ROM
  doesn't upload that layer's strips. BG2's scroll goes into the register
  and into the map stretches of the window's HDMA.
* **Mode 1**: `ppu_init` —which every return to the map goes through— and
  the load set mode 1 and BG3; the screens that open on top go back to 3
  (`slot_ppu_on`, `screen_ppu_on`, `target_ppu_on`). And the objects go up
  one priority, because in mode 1 the map is one step higher than in mode
  3: that way the order between map, hero, upper layer and window is the
  same.

**What was verified**, with the prototype's cartridges:

* **259 against the original**: with the hero where he arrives, the strip
  of the panorama that nothing covers is RM2k's shifted exactly to where
  the formula puts it —0 different pixels between RPG_RT and the panorama
  at pixel 320—, and the ROM's is what the converter decided at pixel 384,
  which is that one plus the 64 that the console's camera is shifted: 0
  different pixels. What differs from the original is the grouping.
* **The ring**: walking 259 end to end, and with 255 moving on its own,
  the tilemap the ROM built column by column is equal, entry by entry, to
  the one a teleport to the same place builds from scratch.
* **Lost frames**: none in 600 ticks walking 259 or standing still on 255;
  2 in 600 walking 255, where sometimes a column and a row of the panorama
  get built in the same frame as one of the map.
* **The ABL test suite**, whole: the five goldens of the two maps fail
  —the arrivals at 259 and 255, and the three of the sign under the
  bridge—, plus the patches one, because 255 merges new colors. Nothing
  else moved. **The goldens are not blessed**: they go side by side, with
  the original, in the delivery's captures.
* **The menu and a battle from 255**, with a throwaway case: both screens
  are drawn in mode 3 and on closing them the map goes back to 1 with its
  panorama (`modo1-menu-y-pelea-desde-el-255.png`).
* **What no test in the suite covers**: the panorama moving —the goldens
  are of the arrival—, the menu and the battle above, a `ChangePBG`, a
  large picture on a map in mode 1, and saving and loading.

## The Lashe City rooftop and the intro

**The rooftop.** Escaping from the agents is, judging by what it shows,
`Escape From 27 Scene` (33), with the same warehouse as 32: Dawn1, no
loop, with the camera, through 14% of the map. It has **two cells** above
the hero, so the prototype sends it to mode 1, and there the sunset ends
up with four colors and the map with 21 of 54. With the above part drawn
below it goes in mode 3: Dawn1 with 15, the whole map. It is the clearest
example of that path. (If the rooftop is the one in `Jumping the Bridge`
(51) —lashepan, on its own at -4, with nothing above—, it is A: 20 of 179
colors and 573 of 3154 tiles.)

**The intro** (1): Night1 with horizontal loop and speed 3, through 23% of
the map, with 52 tiles above the hero in 707 cells —127 on one screen—. It
goes in mode 1: the clouds in 4 grays, the map in 20 of 49. For the clouds
not to flatten the panorama is needed in BG2 at 4 bits and the above part
in BG3, which isn't there.

**The rain is already done** (`rain.s`) and **coexists with the
panorama**: it is objects, with one sprite palette and its tiles at the
end of the sprite bank, so it touches neither the layers nor the lower half
of CGRAM. I tried it by building the intro with its panorama: it rains over
the sky (`intro-con-panorama-y-lluvia-770.png`; it is not in the branch, it
was to look at). Only one thing had to be done: in mode 1 the drops go up
to priority 3, like all objects. What does compete is what already
competed: the mode 1 layout leaves 256 sprite tiles —the intro uses 222
with the drops— and the sprite palettes, where today the drops don't fit
on 2 and 3 and it doesn't rain, with or without a panorama.

## The cost

With the two bridge ones, measured with ABL's `just espacio release`
against the `release` of its `main`:

* **VRAM**: two new layouts, in `docs/port/vram.md` in snes-rm2k. In mode 3
  the panorama has 576 tiles of 4 bits and the map is left with 256 of
  background and 384 of sprites; in mode 1, 768 of 2 bits, and the map with
  512 of background at 4 bits and 256 of sprites. 259 and 255 fit with room
  to spare; a large map like 8 or 16, with 400 and 332 background tiles,
  doesn't fit in A as it is, and asks for another layout or shrinking the
  panorama.
* **ROM**: the tiles and the tilemap uncompressed. 259: 18 KB of tiles and
  4.7 KB of tilemap; 255: 12 KB and 6.3 KB. Compressed with LZ2 like the
  rest they would shrink, but the ring's tiles are read from the cartridge
  while building it and they'd have to be decompressed to WRAM.
* **RAM**: 224 bytes of the far one, `$7E7E00` to `$7E7EDF`, between the
  growth table and `CARRY_MAP`. There is an `.assert` so that the growth
  doesn't creep in: today it uses 216 of the 256 it had. Nothing of bank 0.
* **Bank 0**: about 100 bytes —the hooks in vblank, in `emit_object`, in
  the rain and in the load—. The rest, 1.6 KB, in `FAR2`.
* **Per frame**: computing the position —one long division per axis if it
  doesn't loop— and at most a column of 32 entries and a row of 64; in
  vblank, 64 and 128 bytes of DMA.
* **The converter**: `rm2k-render` (the transparent layer), Voodoo (the 2
  bits), Adeleine (`group_tiles`), `wally` (`background::panorama`,
  `background::mode1`, the request), `rm2k-snes-mapdata` (the layouts,
  `panorama.rs`, the ChipSet animation at 4 bits) and `rm2k-snes-convert`
  (the project's list and each map's layout). None changes anything for a
  map without a panorama, and a cartridge with none comes out with the
  usual `.inc`: that is guarded by the `rm2k-snes-mapdata` tests, which
  compare the whole emission against the one the Python wrote.

## What's missing to take it to the whole game

* **Choosing the path per map.** Today the prototype chooses on its own,
  based on whether there's something above; mode 3 with the above part
  below exists in `wally` but not in the project. And baking the still
  ones, which isn't there.
* **`ChangePBG`**, for the Hover-Tram: changing tiles, palettes and speed
  mid-map.
* **The save**: RM2k saves the panorama's position; the console doesn't,
  and on load it starts from zero.
* **The decisions in `parches/`**: the panorama's grouping and merging is
  not written there, only the map's merges.
* **What the test suite doesn't cover** —see above— and a test that looks
  at the panorama moving.
* **The tint** doesn't reach the screen's backdrop color in mode 1, which
  is part of 255's panorama.
* **Adeleine**: `try_pack` accepts a cell with more colors than a palette
  as a group of its own, and the palette overflows into the next one. The
  panorama is the first thing that has cells like that, and it sidesteps
  it with its own `pack`; if some current map has a 16-color cell in the
  upper layer, it happens to it. I didn't measure it.

## How it was measured

**A map**, with the branch's `wally`, even if it is in no cartridge:

    wally layers --data <dump> --search-dir <game> --search-dir <rtp> \
        --request pedido.json --out <dir>

with `{"map": N, "map_files": {}, "chipset_files": {}, "baked": [],
"window_colors": 13, "panorama": {"tiles_mode3": 576, "tiles_mode1": 768}}`
—and `"mode": 3` inside `panorama` to force it—. In `layers.json`,
`panorama` says the mode, the crop, the tiles and colors before and after;
`background`, the map's; and `background.png` is the lower layer, with
index 0 where the panorama peeks through. A cartridge's maps print it in
`conversor.log`: "panorama seapan: mode 3, …".

**The baked ones**: `background.png` over the panorama at `(0, 0)`,
counting 8x8 tiles and 15-bit colors.

**The original**: the 2015 RPG_RT under Wine, on a copy of the game with
the start on the map —`RPG_RT.lmt` rewritten with Ditto— and without the
arrival autostart, which moves the camera.

**Lost frames and the ring**: throwaway test suite cases, reading
`lost_frames`, the state of `pano.s` in far RAM and the panorama's
tilemap in VRAM before and after a teleport to the same place.
