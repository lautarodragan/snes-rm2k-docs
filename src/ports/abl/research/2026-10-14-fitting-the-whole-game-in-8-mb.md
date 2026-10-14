# Fitting the whole game in 8 MB

> **Measured on 2026-10-14**, by Carpintero, with the tools at `51b4b1b2`
> (the-advocate) and ABL at `d91049e` (the-advocate-ports), on the
> cartridge with every map of [what still blocks the
> end](2026-10-14-what-still-blocks-the-end.md) and that study's four
> throwaway patches. It is a snapshot: the numbers are from that day and
> this file is not updated. What a cartridge has left **today** is said by
> `just space`. How each number was obtained is at the end. The task is
> [`abl-the-whole-game-does-not-fit-in-8-mb`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-the-whole-game-does-not-fit-in-8-mb.md).

The question: with every map, ABL asks for **8,426,177 bytes** of data and
the 127 data banks of the 8 MB cartridge hold **7,700,480**: 726 KB over.
taro decides between compressing (or losing) things and making the MSU-1
required for this game. This measures what each way out saves and costs.
Nothing here is implemented.

## Summary

* **It fits without MSU-1 and without losing anything.** Three
  deduplications that only touch the emitter —identical samples stored
  once per key, per-map actor tables that are the same table 307 times,
  per-map NPC pose tables— save **459 KB** and change nothing the console
  does. With the poses stored **without their empty tiles** (52% of the
  tiles of the poses are empty) another **571 KB** go, and a walking step
  uploads fewer bytes than today. Together: 7,394,638 bytes asked, **about
  300 KB free** before the packing's own loss.
* **More margin, also lossless**, if wanted: songs whose repeats may nest
  (−124 KB), the panoramas' tiles in LZ2 (−85), the sprite banks from a
  shared pool of tiles (−133) and the NPC tables per entry (−74 more):
  **about 730 KB free** with everything.
* **The quality cuts are not needed.** The effects at 6 kHz (−176), an
  instrument ceiling and the backgrounds per ChipSet (−710 to −840, from
  the [count of 2026-10-01](2026-10-01-the-whole-game-without-msu-1.md))
  stay as the reserve that study said they were.
* **What is not worth it**: LZ2 per pose (−652 KB, but ~13% of a frame per
  pose decompressed, measured on 2026-10-11), LZ2 per song (it needs the
  whole song in WRAM, up to 57 KB), sharing background tiles between maps
  without merging colours (9% of the tiles repeat), and a better compressor
  for those tiles (xz, which the console cannot run, takes off 7% more than
  LZ2).
* **The MSU-1 required** builds today: the ROM asks for 4,238,894 bytes
  —66 of the 127 banks— and **4,189,665 bytes** of map tiles, samples,
  panorama and sprite tiles, grids, pictures, battlers, backdrops and
  bytecode travel in the `.msu`, which grows from 7.8 to 12.2 MB. The ROM
  is still 8 MB.
* **What grew since 2026-10-01** (783 KB over that day's "as today"): the
  panoramas, which that count left out (+518 KB), the fonts precomposed in
  eight phases for three inks (+351 KB, decided on 2026-10-03), the big
  pictures (+293), the per-map sprite tables (+184) and the poses (+129).
  The lossless cuts that study counted on mostly happened —the sequences
  went down 309 KB, the bytecode, grids, texts and battle 455— but the new
  things ate them.

## 1. Where the bytes are

The whole cartridge, by family of label, as `pack` receives it; LZ2 is
the installed `lz2` (the converter's parser) over each piece as it is
today, and xz a reference the console cannot run.

```text
family            bytes      LZ2 of what     xz      what it is
                             is there today
map_tiles_      1,452,401    1,454,254   1,347,028   8 bpp background, already LZ2
song_stream_    1,116,122      969,784     627,084   music, read by the IRQ
pose_           1,095,680      443,964     546,376   2,140 poses of 512 B, raw
sample_         1,068,201    1,062,016   1,040,248   BRR, 235 instruments + 138 effects
pano_tiles_       358,720      273,809     220,848   raw, one DMA at load
sprite_tiles_     305,506      306,157     296,284   per-map sprite bank, already LZ2
map_cells_        294,446      294,842     250,304   grids, already LZ2
actor_table_      229,636            —           —   per map: 99 KB of it are pointers
messages          218,450      158,036     115,608   already paired; read box by box
big_tiles_        201,536      180,205     164,936   big pictures
battler_          181,101      181,502     159,728   already LZ2
pages_            176,256       49,083      49,940   per-map page records, walked from ROM
pano_map_         169,600       69,038      54,376   read column by column while scrolling
npc_poses_        126,792            —           —   per map: all pointers
font_pre, slot_pre, scr_pre
                  359,424       60,516      40,036   precomposed letters, 8 phases each
backdrop_         103,411      103,581      96,048   already LZ2
the rest          968,895
total           8,426,177
```

## 2. The options

"Saves" is measured over these pieces unless it says otherwise. The cost
in cycles is a model —8 master cycles per byte of DMA, about 400 per
transfer set up, the LZ2 decompressor's 700 per command and 60 per byte
from `materials.rs`—, not a measurement on the console.

| option | saves | cost on the console | quality | work |
|---|---:|---|---|---|
| **identical samples once**: 17 groups of samples that are the same BRR, the same rate and the same loop, stored once per key (`MMBAS40` four times, `STRNG71B` fourteen, `CHH__60A` sixteen) | **205 KB** | none: two rows of `sample_table` point to one label | none | small, the audio emitter |
| **actor tables shared whole**: 307 per-map `actor_table_` and only 22 different | **213 KB** | none | none | small, the record emitter |
| actor tables per entry (29 different entries of 68 B), an index per map | 224 KB | one indirection at load | none | small, emitter and runtime |
| **NPC pose tables shared whole**: 307, 191 different | **41 KB** | none | none | small |
| NPC pose tables per entry: 3,522 entries of twelve pointers, 212 different, one byte each per map | 115 KB | one indirection at load | none | small, emitter and runtime |
| **poses without their empty tiles**: 17,989 of the 34,240 tiles are empty; a pose keeps its drawn tiles and a 16-bit mask, and the slot remembers its last mask so only the tiles that go from drawn to empty are zeroed | **571 KB** (~548 with a precomputed list of runs) | a walking step: 240 B and 3.5 transfers on average against 512 B and 4 today; the worst step, 8 transfers and ~6,500 master cycles against ~5,700 (+14%) | none | medium: Wally's pose bank, the record, `vram_queue` and `vram_drain`, a mask per slot |
| poses 24 px wide: the character at the object's left edge and drawn 4 px further right, 12 tiles and four 96-B transfers | 274 KB | fewer bytes per vblank than today | none | medium: every place that positions an object |
| poses 24 px wide, empty rows zero-filled | 382 KB | four transfers, as today | none | medium |
| poses in LZ2, one stream each | 652 KB | ~49,000 master cycles per pose, ~13% of a frame, in the main loop: the suite lost frames when Tijereta tried it ([the S-DD1](../../../research/2026-10-11-the-s-dd1.md)) | none | medium, and slow |
| sprite banks from a shared pool of tiles: 47,551 tiles in the per-map banks, 4,001 different; the pool raw (128 KB) plus each map's list in LZ2 (44 KB) | 133 KB | at load, ~180 tiles copied per map instead of one LZ2 stream | none | medium |
| **songs whose repeats may nest**: `OP_REPEAT` is one level today; a greedy encoder that may refer to stretches that hold repeats | 124 KB | none per event; a small return stack instead of one address | none | small-medium, encoder and `ev_repeat` |
| songs in LZ2 per song | 146 KB | the song has to be decompressed whole into WRAM: up to 57 KB, 22 songs over 16 KB | none | not viable |
| **panorama tiles in LZ2** (the largest is 18 KB, under the 24 KB of `LZ2_BUFFER`) | 85 KB | decompressing at load, about 3 frames for the largest; a `ChangePBG` in the middle of a map has to work around `CODE_CARRY`, which lives in that buffer | none | small |
| panorama maps in LZ2 | 100 KB | 9.6 KB of WRAM resident while the map is up: they are read column by column | none | needs WRAM nobody has |
| page records in LZ2, behind the grid | 127 KB | decompressing at load | none | medium, and whether they fit behind every grid was not measured |
| the three precomposed fonts sharing one ink layout | up to 234 KB | none, if the message window's palette were laid out like the text screens' | none | not measured: a CGRAM layout change |
| background tiles shared between maps, colours untouched | ~127 KB | a tile list per map | none | medium, for little: only 3,096 of 35,471 tiles repeat |
| effects that go whole, at 6 kHz (23 effects) | 176 KB | none | the 23 chosen by ear, as on 2026-10-01 | a number in the project |
| instrument ceiling at 12 kHz | 208 KB (120 with the samples deduplicated) | none | brightness of the instruments | a number |
| backgrounds per ChipSet | 710–840 KB (2026-10-01, not measured again) | a map's tile load doubles | colours in 50 to 94 maps | large |
| **the MSU-1 required** | 4,190 KB leave the ROM | a seek per map load and per package: one or two frames in Mednafen | none | built: `msu = "required"` |

What is **not** worth looking at again: the 8 bpp tiles compress almost
the same with anything —xz takes 7% off LZ2—, so the background shrinks
only by having fewer tiles, which means fewer colours or the `.msu`; the
messages are already paired and read box by box; and the samples have no
silence at the end to trim (1.2 KB over 373).

## 3. The combinations

The pieces with each option's measured saving, packed first-fit
decreasing into the 108 banks of 64 KB and the 19 halves the cartridge
has for data. The real packer (`pack` in `rm2k-snes/cartridge`) loses
more: on the MSU-1-required cartridge it left 86 KB of gaps in the banks
it used. So from "free" below, take about 90 KB.

```text
combination                                             asks        free
today                                                 8,426,177    726 KB over
the three deduplications (samples, actor, NPC whole)  7,966,018    265 KB over
  + poses 24 px wide                                  7,692,098      8 KB
  + poses 24 px, empty rows zero-filled               7,582,958    118 KB
  + poses without their empty tiles                   7,394,638    306 KB
    + NPC per entry, sprite pool, nested repeats,
      panorama tiles in LZ2                           6,966,629    734 KB
the deduplications + effects at 6 kHz                 7,789,704     89 KB over
  + instrument ceiling at 12 kHz                      7,669,829     31 KB
only quality: effects, ceiling, per ChipSet           7,314,373    386 KB
```

**The smallest combination with margin is the three deduplications and the
poses without their empty tiles**: lossless, no frame lost —a walking step
is cheaper than today—, about 300 KB free by this count and some 210 after
the packer's loss. It is two pieces of work: the emitter's three
deduplications, which are small and can be checked byte for byte against
the ROM's behaviour (the same suite, the same goldens), and the poses,
which touch Wally, the record and the vblank's queue.

If more margin is wanted before the rest of the story's pictures and maps
arrive, the next ones, in order of saving per work: nested repeats in the
songs (−124), the panorama tiles in LZ2 (−85), the NPC tables per entry
(−74 more) and the sprite pool (−133). None loses quality. The quality
cuts are left for when those run out.

## 4. The MSU-1 required, with its numbers

The same cartridge with the converter's `--msu-everything` builds:

```text
ROM data asked                    4,238,894 B
banks used                        66 of 127, 86 KB of gaps in them
free                              42 whole banks of 64 KB and 19 halves
to the .msu instead               1,747 pieces, 4,189,665 B
  map tiles 1,452 KB, samples 1,068, panorama tiles 359, sprite tiles
  306, grids 294, big pictures 202, battlers 181, backdrops 103,
  bytecode 95, ChipSet animation tiles 60, upper-layer tiles 54
.msu                              12,238,592 B (7,824,157 with it optional)
ROM file                          8 MB: 4.24 MB of data does not go into a 4 MB
                                  ExHiROM either
```

It costs what [the MSU-1 is required only when the ROM does not
reach](../../../decisions/the-msu-1-is-required-only-when-the-rom-does-not-reach.md)
says —a console or emulator with MSU-1 and the `.msu` next to the ROM—, and
a seek at each map load. With the lossless combination above ABL's ROM
reaches, so by that decision's own rule it should stay `"optional"`.

## 5. What grew since 2026-10-01

That day's count put the whole game "as today" at 7,446 KB and planned to
bring it to 7,151 with LZ2, DTE and jumps in the sequences. Today it is
8,229 KB. By the same categories:

```text
category                                 2026-10-01    today    change
BRR samples (instruments and effects)       1,052       1,043       -9
music sequences                             1,399       1,090     -309   the jumps landed
sprites: poses                                941       1,070     +129
sprites: per-map tiles and tables             562         746     +184   actor tables
background: tiles and colours               1,494       1,557      +63
grid, blocks and collision                    400         327      -73
events: bytecode and pages                    466         317     -149   bytecode in LZ2
battle: battlers, animations, backdrops       547         367     -180
texts                                         311         258      -53   letter pairs
panoramas                                       —         518     +518   left out then
big pictures                                    —         293     +293   +430 estimated then
precomposed fonts, 8 phases, 3 inks             —         351     +351
the rest: screens, tables                     274         291      +17
total                                       7,446       8,229     +783
```

So the lossless plan of that day happened —about 760 KB went—, and the
whole game is still bigger, because three things that study did not count
came in: the panoramas, which it left out because mode 3 had nowhere to
draw them; the letters precomposed in eight phases, whose comment in
`messages.s` already says "the 117 KB went in: the cartridge is 8 MB", and
there are three of them; and the big pictures. The per-map actor tables
are the one growth that is pure waste: 22 different tables repeated 307
times.

## How it was measured

* **The cartridge**: Cardón's experiment diffs over the starting commits
  —every map reachable from the start, 108's fork set aside, and the four
  patches— in throwaway worktrees, and one more print in `pack`: with an
  environment variable it writes every piece it receives, whole. A Python
  parser turned that text back into bytes (its sizes match `pack`'s for
  all 7,338 pieces) and every number above comes from those bytes. A
  second cartridge, the same with `--msu-everything`, gave section 4, and
  `rm2k-snes-space` on it the banks and the gaps.
* **LZ2**: the installed `lz2 compress --no-increasing`, piece by piece in
  stretches of 64 KB; the streams already in LZ2 were decompressed with a
  Python decoder checked against `lz2` to count tiles.
* **The samples**: identical by content in the dump; the rates and the
  ceilings from the build's `audio.json`, as bytes times ceiling over rate
  in blocks of 9.
* **The tables**: whole tables and entries compared by their text in the
  `.inc` (pointers included), not by bytes.
* **The poses**: each 512-B pose decoded to pixels; empty tiles counted;
  the 24-px variant re-encoded from the pixels. The walking step: over the
  212 twelve-pose groups of the NPC tables, the steps 0-1-2-1-0 of each
  direction, uploading the drawn tiles and zeroing those drawn before and
  empty now.
* **The songs**: the stream parsed with the opcodes of `music.rs`, the
  repeats expanded, and a greedy encoder of 4-byte repeats (2 events or
  more, up to 255) that may refer back to anything already emitted.
* **The combinations**: first-fit decreasing over the 127 slots, a piece
  over 64 KB spilling across banks; the gaps of the real packer from the
  MSU-1-required build.
* **Not measured**: the cycles on a console or an emulator of any new
  upload or decompression; whether the page records fit behind every grid;
  the ink layouts of the three fonts; the backgrounds per ChipSet again.
