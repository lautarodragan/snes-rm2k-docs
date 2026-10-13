# The zoom, baked at run time

> **Measured on 2026-10-12** by Carpintero. A Blurred Line's `release`
> cartridge built from the ports at `0bf10fd` with the tools of the-advocate
> at `65885882` (`abl.sfc` `417978e33580d361`); the cycle counts in the
> snes9x and bsnes libretro cores; RM2k's zoom read in easyrpg-player at
> `9e67927`. It is a snapshot: the numbers are from that day and this file
> is not updated. How each number was obtained is at the end.

The question is taro's, on 2026-10-12, in the task
[`the-zoom-baked-at-run-time`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-zoom-baked-at-run-time.md):
the Diff photos already zoom in mode 7, from textures the converter bakes.
*Could the screen we are showing in mode 3 be baked into mode 7 at run
time* —both layers and the sprites, merged into mode 7's only layer—,
without going over VRAM or the 256 tiles, and in less than half a second?
And could the SA-1 do it in its own RAM while the main CPU carries on?

It matters because the database of all eight ports erases the map with the
zoom (16) to start a battle and shows it with the zoom when the battle
ends. Today the way in is the mosaic, by taro's choice, and the way back is
the fade: see [The way into battle, in mosaic](../divergences/the-way-into-battle-in-mosaic.md)
and [The teleport transitions](../divergences/the-teleport-transitions.md).


## Summary

**It can be done on the plain CPU, and the SA-1 is not worth it for
this.** The measured limit:

* **Full resolution fits for nine screens in ten.** Over 126 map screens of
  A Blurred Line, the composed screen has a median of **140 distinct 8x8
  tiles**, and 113 of the 126 fit in mode 7's 256 (over the walkthrough's
  49 goldens, Hornero counted a median of 170 and 38 of 49). **Half
  resolution always fits**: 203 tiles at most, against the 224 cells it
  has. What goes over 256 is, above all, **a message window with text**,
  and then panoramas.
* **Composing costs about a quarter of a second**, median, at full
  resolution: **15.9 frames** on the main CPU, 31.0 at p90; at half
  resolution, 10.5 and 14.9. RM2k's battle start spends **20 frames of
  flashes** before the zoom, during which the CPU has nothing else to do:
  composed there, **the way into battle adds no time on 98 of the 126
  screens**, and at most 17 frames (0.3 s) on the worst, with half
  resolution whenever the screen goes over 256 tiles.
* **The cost is the planar-to-chunky conversion**: 31,245 master cycles
  —23 lines— per 8bpp tile of the map. Nothing in the console does it but
  the CPU, and neither does the SA-1.
* **Getting mode 7 into VRAM is about 17 KB**, three vblanks, but it lands
  on the half of VRAM that the mode 3 screen on display is using. Done in
  one go it is **64 lines of forced blank in one frame**; done without any
  black it needs free room in that half, which is likely at half
  resolution and not measured.
* **The SA-1 would make composing ~3 times faster**, on a step that is
  already hidden behind the flashes, and costs the cartridge's memory map
  —ExHiROM at 8 MB does not exist on its board—, its RAM is the save's,
  and it cannot read VRAM either.

The recommendation, with phases, is at the end.


## How RM2k draws it

`Transition::Draw` in easyrpg-player, `TransitionZoomIn` and
`TransitionZoomOut`:

* **41 frames**, the default of every transition but the fade (35) and the
  cut (1). Erasing zooms in; showing is the same backwards, from the new
  screen magnified down to its size.
* **It does not fade.** On frame `f` the source rectangle is
  `256 × (40 − f) / 40` by `224 × (40 − f) / 40`, stretched over the whole
  screen with no filter: the magnification is `40 / (40 − f)`, 2x at frame
  20, 4x at 30 and 40x at the last one, after which the screen is erased.
  Half the transition is spent below 2x.
* **The centre is the hero** on a map —its screen position, 8 pixels up—,
  clamped to the middle half of the screen (64 to 192 across, 56 to 168
  down), with a correction near the edges that slides the rectangle so it
  never leaves the screen. Elsewhere it is the centre of the screen.
* **A battle starts with two white flashes**, 10 frames each, before the
  transition (`Scene_Map::TransitionOut`: `PrependFlashes(31, 31, 31, 31,
  10, 2)`). The runtime already does them, with the fixed colour —see
  `battle_fade_in` in `runtime/battle_fade.s` in the-advocate—, and
  **they are 20 frames in which the main loop is frozen**.

In mode 7 this is the matrix: A and D at `(40 − f) / 40` in 8.8, B and C at
zero, and the centre where the hero is. It is what `big_m7_matrix` in
`runtime/big_picture_zoom.s` already does for the Diff photos, and its
caveat applies as is: the PPU's multiplier is the matrix while mode 7 is
on, so `irq_music` multiplies by hand.


## What a composed pixel is

**It is already a CGRAM index, and mode 7 reads the same CGRAM: there is
nothing to remap.** In mode 3 BG1 is 8bpp and a pixel is its CGRAM entry;
BG2 is 4bpp and its pixel is `palette × 16 + colour`, with its palettes in
the lower half; the sprites are 4bpp and their pixel is `128 + palette × 16
+ colour` (see [The converter decides the CGRAM split](../internals/cgram.md)).
Mode 7 without direct colour reads entry `pixel` of the 256. Colour 0 is
transparent in all of them, and in mode 7 too: what is under it is the
backdrop, entry 0, as in mode 3. The tint and `FlashScreen` are CGRAM
transforms —`tint.s`, `screen_flash.s`— so they keep working over the
composed screen.

What does not carry over is **colour math**:

* **A picture at half transparency** is drawn by adding the subscreen at
  half (`picture.s`); composed, it would be opaque or not be there. No new
  index can hold the blend.
* **The battle start's flash** adds the fixed colour to every layer except
  the sprites with palettes 0 to 3 —the hardware's rule—, so in mode 3 the
  hero flashes less than the map. Composed, everything is one background
  and flashes the same, which is what RM2k does. It does not matter here
  anyway: the flashes come before the zoom.


## Where the sources are read from

**From VRAM, by DMA, in vblank.** VRAM cannot be read while the screen is
drawn, but in vblank or with the screen off it is read at the same 8 master
cycles per byte as it is written, through `$2139`; a vblank of 37 lines
gives about 6.3 KB. It is the only source that is always right, because it
is what the screen is showing:

* **the map's tiles are LZ2 in the ROM**, one stream per block, with no
  way to reach tile N without decompressing what is before it; and the
  sprite poses are uploaded on the fly, so VRAM is where both are whole;
* **the tilemaps** are in VRAM —the map window is a torus the runtime
  builds a row and a column at a time— and the **OAM** has its shadow in
  WRAM, `build_oam`'s;
* the **message window, the timer, the rain and the small pictures** are
  in VRAM too, as BG2 or as sprites, so the same code composes them.

What has to be read is the two tilemaps (2 KB each), the map tiles the
screen uses (a median of 100, 6.4 KB) and the sprites' and BG2's. That is
**two to three vblanks**, eight on the worst screen, and the flashes give
twenty. At the battle's end the screen is black and the map has just been
reloaded, so it is read with the screen off in under a frame.

**Keeping a chunky copy of the map tiles in the ROM** would take the
conversion out —the cost below halves—, but it is **1.25 MB** for A Blurred
Line (19,998 tiles of 64 bytes, every map's), against the 2 MB the
cartridge has free (`rm2k-snes-space` on the same ROM: 23 whole banks and
18 halves). It does not pay.


## What composing costs

A throwaway cartridge times each piece with the PPU's H/V counters, eight
times in a row, from FastROM code with the data in WRAM and the direct page
at zero, and checks its output against a model of the planar formats. The
two cores give the same numbers to the cycle:

```text
piece                                              master cycles   lines
an 8bpp planar tile into 64 chunky bytes                 31,245    22.9
a 4bpp planar tile over a chunky one (BG2, a sprite)     20,319    14.9
the same two at half resolution (16 texels)              12,527 /  8,330
a chunky tile flipped horizontally (mode 7 has no flip)   5,913     4.3
a 64-byte tile's hash and compare against another         4,687     3.4
64 bytes copied with MVN                                  3,142     2.3
64 bytes from ROM into WRAM by DMA, set-up included         977     0.7
a cell's key —its BG1 and BG2 entries— in a hash table      478     0.35
```

A frame is 357,368 master cycles. The 8bpp conversion is the straight one:
each pixel takes one bit of each of the eight planes, shifted into the
accumulator —`asl dp` and `rol a` eight times, then a store—, 61 cycles a
pixel. A table per plane, ORed into 16-bit accumulators, comes out a little
slower on paper (about 528 cycles a row against 488), and nothing in
the console converts planar to chunky: the SA-1's character conversion and
the Super FX go the other way.

**The order that minimises it** is to look at keys first and at pixels
last. Each cell's key is what its tilemap entries say —the BG1 tile and its
flips, the BG2 tile, palette and flips— and two cells with the same key are
the same tile, so the pixels are done once per distinct key: each distinct
map tile is converted once, the cells with nothing over it reuse it, and
only the distinct cells with BG2 or a sprite over them get a copy and an
overlay. The sprites are not aligned to the cells, so their cells always
count as distinct. Mode 7 has no flips: a flipped map tile is a tile of its
own.


## The screens

The capture is the ROM itself: 126 map screens of A Blurred Line —each
map entered at the destination of the first `Teleport` that points at it,
150 frames after arriving— captured five times, with all the layers, with
BG1 alone, BG2 alone, the sprites alone and none, to know which layer
touches which cell. Some have a message open: an autorun page that talks
on arriving. Pixels compared at 15 bits:

```text
                                         median   p75   p90    max
distinct 8x8 tiles, full resolution         140   198   259    627
distinct tiles, half resolution (224)        70    93   123    203
distinct map (BG1) tiles                    100   148   188    692
cells BG2 touches (of 896)                   34   143   336    896
cells the sprites touch                      16    24    48    135
colours on screen                            62    87   116    160
```

113 of the 126 fit in 256 tiles at full resolution, 125 in 512, and all of
them at half. The BG1 count is by screen cell, so on a screen whose scroll
is not a multiple of 8 it counts a tile once per offset: composing on the
map's own grid, which mode 7's scroll allows, gives fewer. The 692 is one
of those.

The cost of each screen, adding up the pieces with those counts:

```text
frames per screen                        median   p75   p90    max
full resolution                            15.9  22.4  31.0   88.6
half resolution                            10.5  12.6  14.9   37.3
full if it fits in 256, half if not        14.8  18.8  25.0   37.3
```

And what that adds to a battle:

* **Into battle**, composing during the 20 frames of the flashes: with
  "full if it fits, half if not", **98 of 126 screens add nothing**, p90
  adds 5 frames and the worst 17. Always at half, 125 of 126 add nothing.
* **Out of battle**, the screen is black and nothing hides it: the median
  is 15 frames of black before the zoom, the worst 37 (0.6 s). That is the
  case where taro's half second is tight.


## More than 256 tiles

When a screen goes over, mode 7 has to merge or the screen has to go to
half resolution. The mock-ups —the real frame, full resolution merged and
half resolution, still and at frames 0, 10, 20 and 30 of the zoom— went to
taro with the task. Pixels that change, against the real frame:

```text
map   tiles   merged, nearest tile   merged, nearest mean colour   half res
 13    264          0.3%                     0.5%                   27.0%
 86    337          7.0%                     9.4%                   52.6%
 95    383          6.9%                    10.5%                   39.1%
259    434         12.5%                    13.9%                   32.5%
255    627         17.8%                    21.8%                   31.2%
```

* **What is merged matters more than how.** Keeping the most used tiles
  throws out the hero first —a sprite's cell is used once—; keeping the
  ones nearest the zoom's centre keeps the hero, and the cells that go are
  the ones that leave the screen first. Merged that way, a message's text
  turns into wrong letters at the edges of the window.
* **Nearest tile is the converter's way** —`mode7` in rm2k-snes-images
  does it for the photos— and **costs too much on the 65816**: comparing a
  tile against 256 by colour is millions of cycles per tile. Nearest mean
  colour is affordable —about 3 frames for the 256 means and 20,000 cycles
  per merged tile, around 9 frames on these screens— and loses a little
  more.
* **Half resolution loses detail everywhere**, 21% of the pixels even on a
  screen that fit (map 40), but it loses nothing in particular: the hero,
  the text and the edges are all there, at half. It is visibly coarser
  than RM2k on the first frames, and from frame 20 —2x— the difference
  is small, because RM2k does not filter either.

So the fallback is half resolution, and merging is a later phase, if taro
wants it after seeing it.


## VRAM: getting mode 7 in, and the map back

Mode 7 owns words `$0000` to `$3FFF`, and there the mode 3 map has its
sprites and its tiles in every layout (see
[The converter decides the VRAM split](../internals/vram.md)). What mode 7
needs is **256 tiles of 64 bytes in the high bytes —16 KB— and only the
map entries the screen shows in the low ones**: 32 by 28, or 33 by 29 on
the map's grid, under a kilobyte. The zoom never shows past them, since it
only magnifies. That is **17.3 KB at full resolution, 14.6 at half**:
three vblanks of 6.3 KB, or 101 and 85 lines of DMA.

The problem is not the time but the place: those words are being used by
the screen on display.

* **In one go**: the screen off for the DMA, which past the vblank's 37
  lines is **64 lines of black in one frame** at full resolution, 48 at
  half. The flashes do not help: their peak is a white frame, and the
  screen off is black.
* **Without black**: mode 7's tiles can go in any of the 256 slots and its
  map anywhere in the 128x128 plane, so they can be uploaded in normal
  vblanks into the 128-byte windows of VRAM that the mode 3 screen on
  display does not use, and the mode switched in one vblank. Whether
  there are enough depends on the screen: the screen uses a median of 100
  map tiles —at most 100 windows, of two tiles each— of the 384 to 544
  loaded, plus its sprites' slots.
  At half resolution, with a median of 70 tiles to place, it is likely; at
  full resolution, with 140, less so. **Not measured.**
* **At the end of the zoom out** the map has to come back to mode 3, and
  the same applies backwards: what mode 7 overwrote is restored —from the
  read-back copy, or by decompressing the map tiles during the 41 frames
  of the zoom, in which the CPU is idle— with the same black or the same
  windows.

At the start of the zoom out the screen is black and the upload is free.


## What is on screen when a battle starts

* **The map, the characters, the timer and the rain** —the timer's glyphs
  and the raindrops are sprites—: all composed the same way.
* **A message window**, if the page that started the battle showed one:
  the runtime keeps it on screen, as the mosaic page says. It is BG2 with
  a tilemap that HDMA switches on its lines, so the compositor has to know
  the window's lines, from the same state `message_place.s` uses. Its text
  is what most often goes over 256 tiles.
* **Small pictures** are sprites, and compose; the ones at half
  transparency lose it.
* **A big picture** puts the console in mode 1 with the map hidden: it
  needs a second path, 4bpp BG1 over palettes, or the fade. The same goes
  for **the maps in mode 1** —the panorama in BG3, the painted maps—.
* **The tint and the screen flash** are the palette, and come along.


## The SA-1

What the 2026-09-26 study measured —the task
[`expansion-chips-sa-1-and-s-dd1`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/expansion-chips-sa-1-and-s-dd1.md)—
holds, and here is what it means for this:

* **Speed.** The 8bpp conversion is about 4,600 CPU cycles a tile —31,245
  master cycles at 6.75 per cycle on the main CPU, between FastROM and
  WRAM—. On the SA-1, at one cycle per ROM or I-RAM access and two per
  BW-RAM one, it is about 9,500 master cycles: **3.3 times faster**, and
  half that if the main CPU is running code from ROM at the same time,
  because they fight over it. The median screen would go from 16 frames to
  about 5.
* **Parallelism buys nothing here**: during the flashes the main CPU has
  nothing to do. The SA-1 would shorten the tail —p90 and the way back
  from battle—, which half resolution already shortens without a chip.
* **It does not see VRAM either.** The main CPU would DMA the sources
  from VRAM into the SA-1's memory and the result back, the same three
  vblanks each way.
* **Its RAM is the save's.** BW-RAM is the battery SRAM; the FX Pak writes
  the SRAM to the card when it changes, so working in it means a write to
  the SD card on every battle. Its I-RAM is 2 KB: enough to compose a tile
  at a time and have the main CPU take each one, which avoids BW-RAM at
  the price of a pipeline between the two CPUs.
* **The memory map.** The cartridge is ExHiROM at 8 MB
  ([The cartridge goes to 8 MB](../decisions/the-cartridge-goes-to-8-mb.md));
  the SA-1's board shows the ROM through four windows of 1 MB, so past
  4 MB it switches banks, and every address the converter and the runtime
  compute changes. That is the "step zero" of the 2026-09-26 study, and
  bigger now than then. FastROM with the SA-1 is still unclear on the real
  chip, and the MSU-1 with it exists only on the FX Pak Pro.

**For the zoom alone, no.** It would be worth asking again only if the SA-1
came for something else —the race's parallel pages were that study's
candidate—, and then the compositor is a natural second job for it.


## The recommendation

**Do it on the main CPU, full resolution when the screen fits in 256 tiles
and half resolution when it does not, reading the sources back from VRAM.**
The measured limit: composing takes 15 frames on the median screen and 37
on the worst; into battle that hides behind the flashes on four screens in
five; out of battle it is black time, 15 frames median.

What would be lost against RM2k:

* half resolution on one screen in ten —the ones with a message, the
  busiest maps and the panoramas—, visible on the first 20 frames of the
  zoom;
* half transparency of pictures, while the zoom lasts;
* on maps and screens in mode 1, the zoom until a second path exists;
* and, unless free VRAM windows turn out to be enough, **one frame with
  about a quarter of it black** when mode 7 comes in and again when the
  map comes back.

**Phases**, each one to be seen by taro before the next:

1. **The way back from battle** (`battle_end_fadein`), which today is a
   fade. The screen is black when it starts, so the upload is free and
   only the composing time shows; the swap back to mode 3 at the end is
   the first place where the black frame, or the windows, get tried on the
   FX Pak.
2. **The way into battle** (`battle_start_fadeout`), composing during the
   flashes. That replaces the mosaic taro chose on 2026-09-30, so it is
   theirs to decide whether the `System` is read again.
3. **The zoom of `ChangeScreenTransitions`** and of `EraseScreen` and
   `ShowScreen`, with the same code: the teleports of Boss Wick's hideout
   ask for it.
4. **Merging instead of half resolution**, by nearest mean colour, if half
   resolution is not good enough: about 9 more frames on the screens that
   need it.

What this does not answer, and the first phase has to measure: the real
cost with the message window's lines and the sprites' priorities in the
compositor; how much room the free windows leave on real screens; and how
the black band, if it stays, looks on the console.


## How it was measured

* **The cycles**: a 32 KB LoROM cartridge of its own, assembled with `ca65`
  and `ld65`, that runs each piece eight times between two latches of the
  H/V counters (`$2137`, `$213C`, `$213D`) with NMI off, and subtracts an
  empty run. FastROM on, code in bank `$80`, data bank `$7E`, direct page
  at zero. Its last step runs each conversion once more and the harness
  compares the bytes with a model of the PPU's planar formats; the three
  conversions and the flip came out equal. Run in snes9x and bsnes through
  the ports' `retro.py`.
* **The screens**: `release` with "Begin the Story", 600 frames, the
  harness's `ir_al_mapa` to each map —a door's fade, done by the ROM— and
  150 frames more; one process per layer setting, with snes9x's
  `snes9x_layer_*` options, because the libretro core is one per process.
  A cell "has" a layer if any of its pixels differs from the capture with
  no layers. Of the cartridge's 129 maps, 127 are a `Teleport`'s
  destination, and one of those came out all one colour and was left out.
* **The time per screen**: the costs above, per screen, as `distinct BG1
  tiles × the conversion + 896 cells × the key + (the distinct cells with
  BG2, or the cells with BG2 if fewer, + the cells with sprites) × (copy +
  overlay + compare)`; at half resolution the half-resolution pieces and
  224 tiles assembled from four quarters (1,500 cycles each, estimated, not
  measured).
* **The merges and the mock-ups**: a Python model over the 15-bit
  captures, tiles compared by their 64 colours; the zoom with easyrpg's
  geometry and nearest neighbour.
* **The chunky copy's size**: the raw map tiles the converter leaves in
  the build for every map of `release`.
