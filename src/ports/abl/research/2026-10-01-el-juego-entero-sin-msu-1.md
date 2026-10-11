# The whole game without MSU-1: the count

> **Measured on 2026-10-01 on `6a83e2c5`** (snes-rm2k), by Tucu-tucu. It is
> a snapshot, like Lechuza's that it continues
> ([the maps through the MSU-1](2026-10-01-los-mapas-por-el-msu-1.md)): the
> numbers are from that day and this file is not updated. What says how
> much each cartridge has left **today** is `just espacio`. The counts of
> the whole game came from throwaway scripts; how to redo them is at the
> end, in "How it was measured".

The question is taro's, after reading Lechuza's study and deciding that
the whole game is played without MSU-1 ([the game is played without
MSU-1](../../../decisions/el-juego-se-juega-sin-msu-1.md)): *"if we move to
8 MB and optimize the resources a bit, compress everything we can
compress, and maybe lower the quality of one thing or another in the ROM
without MSU-1, could we make it?"*

## Summary

- **In 4 MB it doesn't fit, in any way.** With everything in this study
  —every compression, every quality cut, the S-DD1 on the poses and
  without the pictures— about 4,300 KB remain against the 3,968 of data
  the cartridge has. What is left over is not one more cut: it is the
  game.
- **In 8 MB it fits, without lowering the quality of anything.** The whole
  game with what was missing is about **8,070 KB**: it falls just short of
  the ~8,000 of data of an ExHiROM. With the three lossless compressions
  —LZ2 where things go raw, DTE in the texts and jumps in the sequences— it
  goes down to about **7,150 KB**, and **~850 KB are left free, about 26
  banks of 32 KB**.
- **Lechuza's count counted the samples too many times.** Her 2,120 KB of
  samples came from adding up eleven runs, and each run builds its own bank
  with other rates: the same sample at four rates counted four times.
  Compiling the whole game's audio at once —the 103 themes, the 135
  effects and the 322 packages— the bank weighs **520 KB** and the effects
  **532 KB**: 1,052 KB, **1,068 less**. The whole game as it is today is
  about **7,450 KB**, not 8,514.
- **What was missing** adds about 630 KB to the ROM: the `ShowPicture`
  pictures that today aren't drawn (~430 KB, estimated), the five maps
  that don't fit in VRAM (~105) and the sound effects of the battle
  animations (92). **The battle animations add nothing**: they go only in
  the `.msu`, and they are 84 that no event shows, 462 KB. The
  **panoramas** are left out: mode 3 has nowhere to draw them.
- **Backgrounds quantized per ChipSet** are the quality cut that gives the
  most: the background tiles of the whole game go down from 41,968 to
  15,097, about **840 KB less**. It costs colors in 94 of the 323 maps —in
  the worst, from 97 to 51— and to the eye it is hardly noticeable; and a
  map's tile load doubles. **With 8 MB it is not needed**: it is kept for
  when space gets tight.

## 1. Lechuza's count, corrected

Lechuza measured the whole game by converting it in eleven runs and adding
up what came out different in each. For almost everything that is the
right rule —a map comes out the same in two runs, and counts once—, but
**not for the samples**: the sample bank is a single one per cartridge and
each sample carries the rate its tightest package allows, so the same
sample comes out at another rate in each run, with other bytes, and the
sum counts it once per rate. From the converter's logs of the eleven runs
come **648 versions of only 178 distinct instruments and hits**.

Compiling the whole game's audio at once —an audio job that is the union
of the eleven: 103 themes, 135 effects, 322 packages—:

```text
item                                   Lechuza    at once
sample bank (instruments)                          520 KB   235 samples
sound effects                                      532 KB   135 effects
samples, both                         2,120 KB   1,052 KB
sequences                             1,399 KB   1,399 KB   103 themes
```

The sequences come out the same both ways, which is the proof that the
union of the jobs is the whole game. **The whole game, converted as today,
is 8,514 − 1,068 = 7,446 KB**, 233 banks of 32 KB.

The rest of her table stays as it is. One difference that changes
nothing: adding up the background labels run by run —tiles of the
background, of the ChipSet animation and of the layer above, and their
colors— gives 1,624 KB and not her 1,494; the rule of deduplicating by
content is not the same as adding up by run, and with 130 KB of difference
no conclusion below moves.

## 2. What was missing from the count

### The battle animations

Today the ROM carries only the animations the map events show
(`rom_animations` in `tools/port/battle_animations.py`): 21 in `release`.
The battle shows none. What the whole game's battle asks for, with the rule
of EasyRPG's `Game_BattleAlgorithm` —the `animation_id` of a normal skill,
the weapon's, and the actor's `unarmed_animation` without a weapon—, over
the skills that can really be had (the ones the actors learn, the ones the
enemies use, those of the special items and those of `ChangeSkills`):

```text
what                            animations  frames   as today   LZ2
the ones the battle asks for       111       2,285    570 KB   214 KB
  through skills                   101
  through weapons                   29
  through unarmed actors            18
the ones in cutscenes               42         787    168 KB    56 KB
the ones of the battle that no      84       1,804    462 KB   180 KB
  event shows
both                               126       2,591    630 KB   236 KB
```

"As today" is how `release` stores them: each frame without its empty
tiles (`frame_without_gaps`), plus its pointer, its entry in the table and
its palette. Raw, at 2 KB per frame, they would be 5.3 MB. Three of the
111 have no sheet (empty `Battle/`) and weigh nothing.

**The 84 that only the battle uses go only in the `.msu`** (taro's
decision): **zero bytes of ROM**. The **42 of the cutscenes stay in the
ROM**, and are already inside Lechuza's count —each run converts them with
`rom_animations`—: **at most 168 KB**, or 56 with LZ2 per whole
animation. The biggest, number 72, is 23 KB decompressed: it fits in the
LZ2 buffer.

### The sound effects of those animations

The `timings` of the 111 battle ones ask for 106 effects. **39 aren't
carried by the whole game**, and converted as today —6 kHz, up to
0.75 s— they are **92 KB**. The 42 of the cutscenes ask for 37 and one is
missing (1.4 KB).

Without MSU-1 there is no animation, but **the sound can go anyway**: it is
what the ROM did with the map animations between 2026-09-11 and 12, when
they sounded and flashed without a drawing. The count adds them; if they
don't go, it is 92 KB less.

### What the ROM doesn't draw and has data for

- **The `ShowPicture` pictures**: the whole game shows **97 distinct
  ones** in 311 places, and the ROM draws only the ones that fit in a row
  of objects 32 pixels tall (`picture.fits`): **49 are taller**. At the
  console's scale, in 15 colors and at 4 bpp, the 97 are 1,158 KB raw and
  **~430 KB with LZ2**. It is an upper bound: some are already in the ROM
  and in Lechuza's count, and drawing the full-screen ones asks for a
  design that doesn't exist (the wishlist task
  [`sistema-de-imagenes`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/sistema-de-imagenes.md) in snes-rm2k-work). The count adds them whole.
- **The panoramas**: 19 distinct ones in 44 maps, **~770 KB with LZ2** at
  4 bpp. **They are left out**: in mode 3 both background layers belong to
  the map, and the converter drops them (the comment of `ChangePBG` in the
  event compiler, and the wishlist task [`panorama-del-mapa-2`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/panorama-del-mapa-2.md)). It
  doesn't add them.
- **Movies**: none.
- **The five maps that don't fit in VRAM** (108, 127, 148, 250 and 285, see
  Lechuza): at the 20.8 KB per map of her study, **~105 KB**. They are
  added, because they are work anyway.
- **The pages that don't compile** because a teleport leads to a map that
  isn't in the cartridge disappear by themselves with the whole game. The
  [divergences](../../../divergences/README.md) are about behavior, not
  data: none adds bytes that can be counted.

## 3. What shrinks it

### LZ2 where things go raw, and DTE in the texts

**LZ2** is already measured by Lechuza: the block table, the bytecode, the
battlers, the cutscene animations, the font and the light battle
backdrops, **about 470 KB** in the whole game, without losing anything. The
poses and the sequences can't be, and why is in her section 5.

**DTE** —the byte values the text doesn't use come to mean a pair of
letters, one level only— over the `messages` block of the biggest run,
that of maps 1 to 119:

```text
172,482 B, 88 byte values used, 168 free
only pairs of letters or space          115,586 B with the table   -33 %
any pair                                111,054 B                  -36 %
```

The first is the one that can be done without splitting a control code
from its parameters. Over the ~255 KB of messages of the whole game it is
**about 85 KB**, without losing anything and without losing direct access
to each box. It is idea 3 of the task [`los-textos-sin-comprimir`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/los-textos-sin-comprimir.md) (in
snes-rm2k-work), which was unmeasured; the repeated messages (its idea 1)
would give something more and aren't measured.

### The music sequences

Ideas 2 and 3 of the task [`la-musica-pesa-789-kb`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/la-musica-pesa-789-kb.md) were measured on the
prototype's format, and today's is already per note. Measured again, over
86 of the 103 themes (1,184 KB; the other 17 carry references in the
`.inc` and couldn't be read as bytes):

```text
idea                                         left     saving    RAM
2. jump to what was already played, no       74 %     -26 %     5 B
   nesting (a 4 B jump instead of a
   repeat of 8 B or more)
3. LZSS with a 4 KB window                   54 %     -46 %     4 KB
LZ2 of the whole theme, for reference        56 %      —        the theme
```

Over the 1,399 KB of the whole game: **jumps, −367 KB; LZSS, −638 KB**.
Idea 3 asks for 4 KB of WRAM that keep playing for as long as the theme
lasts —also during a map load, when the LZ2 buffer is busy—, and Lechuza
found the WRAM all handed out. That is why the count uses idea 2, and 3 is
kept as one more step if that RAM appears. Idea 4 —not writing the notes
that never sound— is not measured again.

### The samples, by rate

Over the bank of the whole game compiled at once —235 samples, 520 KB, at
the rate each one's tightest package allows it today—, with a ceiling:

```text
ceiling   bank      saving
today     520 KB
16 kHz    401 KB    -119 KB
12 kHz    316 KB    -204 KB
10 kHz    271 KB    -249 KB
 8 kHz    225 KB    -295 KB
```

The **effects** almost all go at 6 kHz and up to 0.75 s: 112 of the 135,
271 KB. The other 23 are the ones the project asks for **whole**, at the
rate of their WAV (`[sound_effects.whole]`, chosen by ear): 262 KB. At
6 kHz they would be 86: **−176 KB**. Lowering all to 4 kHz would be 118
more, and 6 kHz is already little.

**With MSU-1 none of this is lost**: the music plays from the tracks and
the quality effects come from the `.msu`.

### The map backgrounds, per ChipSet

Today the background is quantized map by map (`layers.rs` in
`rm2k-snes-map-background`): each map has its color table and its tiles,
so two maps with the same ChipSet don't share a byte. taro's idea: without
MSU-1, one color table per ChipSet and a single pool of tiles for all its
maps; with MSU-1, the `.msu` carries the per-map version with all the
colors.

**What is baked doesn't break the reuse of the background**: baking puts
events in the **layer above**, not in the one below, so the 8 bpp
background depends only on the map and its ChipSet. And the layer above
weighs little —61 KB in the whole game—: it isn't worth sharing.

**How it was tested.** The game's 323 maps drawn with `rm2k-render
layers`, and the `layers.rs` count per map and per group: the colors at 15
bits, counted over the drawing and those of the ChipSet animation; if they
go over the cap, `adeleine merge` —the same the converter uses—; and the
unique 8x8 tiles, with mirrors reused as Voodoo does. Each map's cap is the
one the converter gave it in Lechuza's runs, and **a group's is that of
its tightest map**: in mode 3 the background addresses CGRAM directly, but
only the lower half —the upper one belongs to the sprites—, without the 9
entries of the window and without the palettes the layer above takes:
**103 at most** ([the CGRAM split](../../../internals/cgram.md)), and 55,
71 or 87 depending on the map. Per map, the count gives the converter's
tiles with differences of one or two.

```text
43 ChipSets, 12 of them with a single map
                            per map (today)  per ChipSet
background tiles               41,968          15,097
raw, at 64 B                   2,624 KB          944 KB
with LZ2                       1,656 KB          666 KB   in stretches
                                                          of 64 tiles
tile list per map                  —              82 KB   2 B per tile
total                          1,656 KB          748 KB   -55 %
```

Brought to what the converter spends today on those tiles in the whole
game —1,535 KB with LZ2, counting the labels of the runs—, it is **about
840 KB less, 26 banks**. The groups that give the most are the big ones:
ChipSet 23, 33 maps, from 6,331 tiles to 1,238.

**How the ROM would use them.** A ChipSet's pool doesn't fit in VRAM
—three go over 1,024 tiles, and the graphics study had already seen that
the pool of 1 and 2 together didn't fit in any layout—, so **each map
uploads only its own tiles**: it carries the list of which they are, and
VRAM stays as it is today, because merging colors can only bring tiles
together. The pool goes in LZ2 stretches ordered by which maps use each
tile, and a map decompresses the stretches it touches and uploads its own
from there. The size of the stretch is the price:

```text
stretch      LZ2 of the pool   what a map decompresses, against today
                               median    p90
64 tiles       666 KB          x2.3      x5.5
128            648 KB          x2.7      x10.7
256            631 KB          x3.3      x18.7
```

With 64, **a map's tile load doubles** in the typical map; and the tiles
are one part of how long it takes to load. The other way out is to carry
the pool **raw** and upload each tile by DMA straight from the ROM,
without decompressing anything: 944 + 82 KB, **about 580 KB less** than
today, and the load faster than today.

**What it costs in colors**, against today:

- **94 of the 323 maps lose colors**; 43 lose more than ten, and on average
  it is 3.9 per map. The ones that lose the most are those that share a
  ChipSet with a tight map: number 25 has a cap of 55 because of just one
  of its 14 maps.
- The ten that lose the most, and how many pixels change against the
  original:

  ```text
  map                      ChipSet  colors today -> per ChipSet  pixels
  139 Room7                   25        97 ->  51               3.3 %
  137 Room5                   25        90 ->  45               2.9 %
  117 House3                  24       103 ->  65               3.9 %
  144 Shop In Garagaraboren   24       103 ->  66               3.2 %
   66 Lashe Area              31        99 ->  67               0.1 %
  112 ParadiseInteriors       24       103 ->  72               4.5 %
  113 Emily's House           24       103 ->  72               2.3 %
  114 Talan's House           24        93 ->  63               2.0 %
  119 Weapons and Armor       24       103 ->  74               3.9 %
  168 The Line Narrows        24       103 ->  74               2.8 %
  ```

  The one that changes the most pixels is 215, 9.7 %, with 103 colors today
  and 81 per ChipSet. The side-by-side captures of the ten —today on the
  left, per ChipSet on the right, only the lower layer— were handed to
  taro. Looking at three (112, 117 and 139), the difference is hard to
  find: `merge` merges the colors that are seen the least.
- **A variant that loses less**: grouping by ChipSet **and** by cap, so a
  tight map doesn't lower the colors of the rest. 50 maps lose colors and
  not 94, 1.6 on average, and the saving drops to **about 710 KB**.

**What wasn't measured**: the backgrounds with what the project changes on
top of the dump —the forked maps in `parches/manual/`, six—, and the cost
in cycles of uploading a list of loose tiles instead of a block.

## 4. The final count

In KB. "Loses" says what is lost without MSU-1; with MSU-1, nothing of the
quality cuts is lost, because the `.msu` carries the good version.

```text
the whole game                                       KB      loses
as today, according to Lechuza                     8,514
the samples, counted at once                      -1,068
as today                                           7,446
+ the effects of the battle animations               +92
+ the ShowPicture pictures (upper bound)            +430
+ the five maps that don't fit in VRAM              +105
+ the battle animations                               +0     go only in the .msu
with what was missing                              8,073
- LZ2 where things go raw                           -470     nothing
- DTE in the messages                                -85     nothing
- jumps in the sequences                            -367     nothing
lossless                                           7,151
- the backgrounds per ChipSet                       -840     colors in 94 maps
- the whole effects, at 6 kHz                       -176     the 23 chosen by ear
- the sample bank with a 12 kHz ceiling             -204     brightness of the instruments
- without the effects of the animations              -92     the silent battle
with every quality cut                             5,839
```

Against the two cartridges:

```text
cartridge                       data       with what     lossless   with every
                                           was missing              cut
4 MB, LoROM, 124 banks          3,968 KB   no            no         no: 1,870 too many
8 MB, ExHiROM                  ~8,000 KB   no, by ~70    yes, ~850  yes, ~2,160
```

**In 4 MB it doesn't fit even with everything.** Adding also what this
study doesn't recommend —LZSS instead of jumps (−271), the bank at 8 kHz
(−91 more), all effects at 4 kHz (−118 more), the S-DD1 on the poses
(−640, see Lechuza) and without any picture (−430)— about **4,290 KB**
remain: 320 still too many. And that is already another game.

**In 8 MB it fits without losing anything**, with about 850 KB —26 banks
of 32 KB— of margin, which is what covers what this count estimates
instead of measuring: the pictures, the five maps, the packing into 64 KB
banks. The quality cuts are **another 1,300 KB of reserve**, and are used
only if needed.

## 5. What changes to move to 8 MB

**ExHiROM**, which the FX Pak supports (Lechuza, section 5): the same
addresses as HiROM for the first 4 MB, at `$C0-$FF`, and the other 4 at
`$40-$7D`, all in 64 KB banks. Broadly, what it touches:

- **The memory map and the header.** `memoria.cfg` stops being 124 areas
  of 32 KB at `$8000-$FFFF` and becomes ~126 of 64 KB from `$0000`; banks
  `$7E` and `$7F` are still WRAM, so those 128 KB of ROM are seen only
  through the upper half of `$3E` and `$3F`. The header goes at `$40FFB0`
  in the file, with map mode `$25` (`$35` with FastROM). **The bank packing
  (`banks.rs`) is already written for that**: what it assumes is the size
  and where the bank starts, and in 64 KB the DMA fits better.
- **Bank 0 and bank 1.** The interrupt vectors and the code that runs with
  the data bank at `$80` see `$80:8000-$FFFF`, the upper half of a 64 KB
  bank. **The tables in bank 0 don't gain room by themselves**: they are
  still 32 KB seen with absolute addressing, as today, and what doesn't fit
  there goes with a long pointer, as everything generated already does.
- **What crosses banks by hand** —what carries `.crossbank`, like the
  samples the driver uploads byte by byte (`emit.rs`)— assumes a bank ends
  at `$FFFF` and the next starts at `$8000`. In ExHiROM it starts at
  `$0000`: every routine that increments the bank by hand has to be found.
- **SRAM** moves from `$70:0000` (LoROM) to `$6000-$7FFF` of banks
  `$20-$3F` and `$A0-$BF`, 8 KB at a time: the four 2 KB slots fit in one
  window, but the routine that saves and the one that reads the slots
  change address.
- **Doesn't change**: WRAM or far RAM —they belong to the console, not to
  the cartridge—, the MSU-1 port at `$2000-$2007` and the `.msu`.
- **What isn't verified**: that Mednafen (`snes_faust`) maps ExHiROM; the
  harness's three cores have it (Tales of Phantasia is ExHiROM). FastROM
  stays: `$C0-$FF` and `$80-$BF` are the fast half.

The decision `el-cartucho-se-queda-en-4-mb.md` ("the cartridge stays at
4 MB") says that going past 4 MB "is changing how every address is
computed, with everything that breaks on hardware and not in the
emulator", and that it is reviewed on reaching 85-90 %: **`release` is
already at 120 of 124 banks, and with Tangle Forest at 124.** This study
recommends reviewing it: the whole game without MSU-1 doesn't fit in 4 MB
with any cut, and in 8 it fits without losing quality.

## 6. The recommendation, in phases

From what gives the most for the least cost to what gives the least. None
is implemented: the tasks come from here.

**Phase 1 — LZ2 where things go raw and DTE in the texts: −555 KB, without
losing anything.** It is the only thing that gives `release` room within
the 4 MB in the meantime —about seven banks at its scale, according to
Lechuza—, and it is worth the same in 8. It costs decompressing on
entering the map or the battle, and the WRAM behind the grid (Lechuza,
section 2).

**Phase 2 — ExHiROM, 8 MB: +4 MB.** It is what gives the most, and
without it there is no whole game. It costs the memory map, the SRAM and
what crosses banks by hand; **what settles it is the hardware**: a test
ROM on the FX Pak before moving the game, like the one for the MSU-1 port.

**Phase 3 — jumps in the sequences: −367 KB, without losing anything.**
The writes to the DSP are the same, and what proves it is decoding in
Python and comparing against today's, theme by theme. LZSS (−271 more)
only if 4 KB of WRAM that can keep playing during a load appear.

**Phase 4 — what was missing**, which are features and not space: the
five maps that don't fit in VRAM, the picture system and, if taro wants
the battle with sound without MSU-1, the effects of the animations. And
the battle animations from the `.msu`, which with MSU-1 cost zero bytes of
ROM (the wishlist task [`animaciones-en-la-pelea`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/animaciones-en-la-pelea.md)).

**Phase 5 — only if 8 MB gets tight: quality, in this order.**

1. The whole effects at 6 kHz (−176): a number in the project, and with
   MSU-1 they stay whole.
2. The backgrounds per ChipSet (−710 to −840): the one that gives the
   most, but it asks the converter to convert per group and not per map
   —the cache, the per-map tests, everything that today is one map per
   call— and a load of loose tiles in the ROM. First the variant per
   ChipSet and cap, which loses half the colors.
3. The rate ceiling of the bank (−119 to −295): taro chooses it by ear.

## How it was measured

- **The samples at once**: an audio job built from the union of the
  `audio-job.json` files of Lechuza's eleven runs —the themes by name, the
  packages by map, the inheritance—, without `emit`, and `rm2k-snes-audio
  compile` on it. Its `audio.json` brings each sample of the bank and each
  effect with its rate and its bytes; the ceilings were computed as bytes
  times ceiling over rate, in blocks of 9.
- **The animations**: what the battle asks for, from the dump (`skills`,
  `items`, `actors`, `enemies`, and the `ChangeSkills` and
  `ShowBattleAnimation` of the 328 maps, the common events and the troops);
  how much they weigh, with the converter's `animation.by_numbers` and
  `battle_animations.frame_without_gaps`, and the installed `lz2`. Their
  effects, from the `timings`, against the effects of Lechuza's audio jobs,
  and the duration of each WAV.
- **The pictures and the panoramas**: from the dump, their files reduced to
  15 colors with PIL at the console's scale, in 4 bpp tiles, and the
  installed `lz2`. It is an estimate of the order of magnitude, not a
  conversion.
- **The backgrounds**: `rm2k-render layers` over the 323 maps, and in
  Python the same as `layers.rs` —15 bits, `adeleine merge` with each
  map's cap from the converter's log, unique tiles with mirrors, the planar
  8 bpp format— per map and per group, with the installed `lz2`. The
  captures, the lower layer painted with both tables.
- **DTE**: greedy, most frequent pair first, over the `messages` block of
  the run of maps 1 to 119.
- **The sequences**: the `song_stream_N` of the runs, by theme name; the
  jumps and the LZSS, with a greedy test encoder that counts bytes and
  doesn't decode.
- **What was taken from Lechuza without measuring again**: the rest of her
  whole-game table, the LZ2 saving and the 20.8 KB per map.
