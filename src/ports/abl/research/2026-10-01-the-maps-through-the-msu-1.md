# The maps through the MSU-1: how far the cartridge reaches

> **Measured on 2026-10-01 on `37ea12fc`** (snes-rm2k, where A Blurred
> Line still lived as `rom/`), by Lechuza. It is a snapshot: the numbers
> are from that day and this file is not updated. What says how much each
> cartridge has left **today** is `just espacio`; how long the data port
> takes, `just msu-puerto`. The counts of the whole game came from
> throwaway scripts; how to redo them is at the end, in "How it was
> measured".

## Summary

- **The whole game, converted as today, is 8,514 KB of data, 8.3 MB**: 266
  banks of 32 KB against the 124 that fit. It is twice and a bit more what
  the cartridge has, and **it doesn't fit in 8 MB either**, of ExHiROM or
  of a chip with a mapper: it confirms, with the number, what taro said on
  2026-09-27.
- **Four out of every ten bytes are music**: 1.4 MB of sequences and 2.1 MB
  of BRR samples, 3.4 MB between the two. With MSU-1, the music already
  plays from the tracks and the quality effects already come from the
  `.msu`: that weight exists only to play **without** MSU-1. Another
  1.9 MB is what a map uploads on entering —tiles, colors, grid, sprite
  tiles—, which can be read from the `.msu`.
- **Taking out those two things, the ROM of the whole game weighs about
  3.0 MB**, and it fits in the 124 banks with 0.9 MB free. What stays in
  the ROM is what the CPU reads while the game is played: the poses, which
  are uploaded on the fly; the bytecode; the texts; the battle; the
  screens.
- **Reading a map from the `.msu` is faster than decompressing it from the
  ROM**: the port gives 2.60 MB/s —42 KB per frame, measured in snes9x,
  bsnes and mesen-s—, and raw there is nothing to decompress. A typical
  map's load goes from about 5 frames to half of one; the heaviest's, from
  22 to less than 2. **The fade gets shorter, not longer**, except for
  whatever the real cartridge takes to seek, which **is not measured**: a
  test ROM for the FX Pak is left for that.
- **Without MSU-1 there is no whole game in any way.** The recommendation
  is **two cartridges from the same converter and the same runtime**:
  `release`, as today, without MSU-1 and as far as it fits; and a new one
  with the whole game, which requires MSU-1. The phases, at the end.

## 1. How much the whole game weighs

### The count

The game has **328 maps** in the tree (`rom/data/maps.json`, the ones of
map type). `release` carries 93. The converter can't build the 328 in one
run —see "What it doesn't convert" below—, so it was converted in **eleven
runs** that split the maps among them, each with its own project file, and
added up:

- what comes out **identical** in two runs that share maps —a map's tiles,
  a pose, a battler, a sample— is counted once;
- what depends on the run even if the map is the same —the bytecode, which
  carries global variable and text numbers; the sprite tiles, which depend
  on the leader candidates; the single-instance tables— is added per run,
  subtracting the base they all carry;
- the music sequences, by theme name.

Done over `release` alone, the count gives its exact 3,913,695 bytes, which
is what `just espacio` calls 120 banks used. (The samples are instruments
and effects together: in `release`, the effects are 458 KB of the 925,
according to `conversor.log`.)

```text
item                                     release      whole game
BRR samples (instruments and effects)     925 KB         2,120 KB
music sequences                           634 KB         1,399 KB   103 themes
sprites: poses                            473 KB           941 KB
sprites: per-map tiles and tables         239 KB           562 KB
background: tiles and colors              543 KB         1,494 KB
grid, blocks and collision                162 KB           400 KB
events: bytecode and pages                204 KB           466 KB
battle: battlers, animations, backdrops   269 KB           547 KB
texts                                     170 KB           311 KB
the rest: screens, fonts, tables          202 KB           274 KB
total                                   3,822 KB         8,514 KB
                                       (120 banks)      (266 banks)
```

**The fixed part is small**: screens, fonts and tables are 274 KB.
Everything else grows with the content, but in two different ways:

- **per map**: background, grid, sprite tiles, bytecode and texts. From
  `release` to the whole game they grow from 1,318 to 3,233 KB, about
  **8.5 KB per map** of the 226 missing;
- **per what the map brings**: a new theme, a new CharSet, a new enemy. The
  samples, the sequences, the poses and the battle grow from 2,301 to
  5,007 KB, about **12 KB per map** on average, but in jumps.

In total, **20.8 KB per new map**, which is the number to keep at hand for
any "do N more maps fit?".

**The text block barely makes it**: the messages of the whole game take
about **255 KB** of the 262,144-byte block that `OP_MESSAGE`'s operand
allows in steps of 4 bytes. It fits, but with whatever any padding or any
test text adds it stops fitting; see the task [`uncompressed-texts`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/uncompressed-texts.md)
in snes-rm2k-work.

### What it doesn't convert

**Five maps don't fit in VRAM** with today's converter, and it is not a
problem of cartridge space:

```text
108 Distant Paradise     462 background tiles, 696 sprite: there is no room
127                      138 background, 696 sprite        left for the
148                      614 background, 211 sprite        message window
250                      621 background, 211 sprite
285                      shows battle animations and their 64-tile box
                         doesn't fit in the sprite bank
```

The five have to stay out for the count to run, and they are outside the
8,514 KB: they add little and don't change the conclusion. Also left out
are the five unreachable backups that `release` already excludes (46, 75,
96, 97 and 98).

And **three converter limits the whole game goes past**, which had to be
dodged by splitting the runs:

- **the encounters**: `rm2k-snes-battle` indexes the encounter troops with
  a byte, and the whole game has **365**. It is a 16-bit index;
- **the leader candidates** are computed over all the cartridge's maps, so
  with all of them together map 207 asks for 9 graphics of order 34 —the
  cap is 8— and map 288 adds actor 34, which has no CharSet. Each one alone
  converts;
- **a panic in `rm2k-snes-audio`**, at `msu.rs:116`, when a certain set of
  maps builds a package with an effect that has no rate in the `.msu`: it
  happens with 120 and 122 together, and not with each alone. I didn't
  follow it; it deserves a task.

And one run, **with `--no-timer`**: with the timer, Yun Town (67) doesn't
fit in the sprite palettes. It is 16 bytes per map.

## 2. What can be read from the `.msu`

### The port

The MSU-1 serves `<rom>.msu` as a stream: a 32-bit position is written to
`$2000-$2003`, one waits for bit 7 of `$2000` to clear, and `$2001` is
read, which advances by itself. **It is read by DMA with a fixed source**
—`scn_fill` already does it with the battle backdrops, see [the `.msu`
file](../../../internals/the-msu-file.md)—, and the destination can be
**anything on bus B**: VRAM through `$2118`, CGRAM through `$2122` or WRAM
through `$2180`. That is, raw tiles go **from the `.msu` to VRAM without
going through WRAM** or the CPU.

The `.msu` has no limit that matters —it is a file on the card—, so what
goes there goes **raw**: compressing it would save card space and cost CPU
on loading, which is exactly what we want to remove.

### Which part of a map

```text
what is uploaded on entering          where it goes   from the .msu?
background tiles and colors           VRAM, CGRAM     yes, directly
tiles of the layer above              VRAM, CGRAM     yes, directly
sprite tiles and their colors         VRAM, CGRAM     yes, directly
ChipSet animation drawings            WRAM $7F:6000   yes, through $2180
the grid (with collision inside)      WRAM $7E:8000   yes, through $2180

what the CPU reads while playing
block table and its passability       ROM             yes, if copied to WRAM
bytecode, pages, positions            ROM             yes, if copied to WRAM
the characters' poses                 ROM -> VRAM     no: uploaded on the fly,
                                                      by DMA in vblank
texts, battle, screens                ROM             not on entering the map
```

**Collision is not a separate item**: it travels in the block (see
[Maps](../../../internals/maps.md)), so it comes with the grid and the
block table.

**The poses can't come from the `.msu`.** They are uploaded when a
character changes pose, in vblank ([the poses are uploaded on the
fly](../../../optimizations/poses-on-the-fly.md)), and having
them at hand would require copying them to WRAM on entering: with 26 NPCs
of twelve poses that is hundreds of KB. They are 941 KB of the whole game
and they stay in the ROM.

### How much RAM there is

WRAM is **all handed out**. Playing `release` in snes9x —the title screen,
the opening with A and teleports to maps 66, 52, 38, 11, 69 and 1— and
noting which bytes are nonzero in some snapshot:

```text
region                 touched          gaps of 256 B or more
$7E:0000 BSS and stack  7,569 of 8,192   none
$7E:2000 far RAM       19,335 of 24,576  five, 1.8 KB among them,
                                         plus the 2 KB of ANIMB_BUF
                                         (the battle, which wasn't played)
$7E:8000 grid          32,464 of 32,768  none
$7F:0000 LZ2 buffer    20,357 of 24,576  none
$7F:6000 animation      6,916 of 8,192   none
$7F:8000 upper grid    32,336 of 32,768  none
```

That the grid region is touched whole **doesn't mean a map uses it
whole**: the title screen and other screens use it too, and the battle
overwrites the `$7F` half —that is why `back_from_battle` decompresses the
grid again—. **What a map needs while it is played** is its grid, and that
measures `MAP_BW × MAP_BH × 2` bytes:

```text
over the 319 maps      median    p90       maximum
grid                    600 B    5,000 B   40,000 B (map 49)
events (bytecode,     1,613 B    4,156 B   13,007 B (map 11)
  pages and tables)
grid + events                              43,250 B (map 49)
```

**No map goes over 64 KB with the grid, the bytecode and its tables
together**, so a map's bytecode and block table fit **behind its grid**, in
the same region. The price is the grid's: what the battle or a screen
overwrites is read again on returning, and from the `.msu` it costs a
third of a frame.

And the LZ2 buffer (`$7F:0000`, 24 KB) **is no longer needed to load a map
from the `.msu`**: the raw data goes straight to VRAM.

**What isn't measured**: reading the bytecode from WRAM is slower than
from ROM —8 master cycles per byte against 6 with FastROM—. It affects only
the reading of the bytecode, not the whole interpreter, but the race and
map 11 are already tight on CPU (see the wishlist task
[`expansion-chips-sa-1-and-s-dd1`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/expansion-chips-sa-1-and-s-dd1.md)).

## 3. How long it takes

### The port, measured

`just msu-puerto` builds a 32 KB ROM (`rom/experimentos/msu-puerto/`) with
a 1 MB `.msu` of pseudorandom bytes, seeks, reads 18 stretches of 32 KB by
DMA into WRAM —two of them after a far seek and 16 in a row, two DMAs back
to back at a time— and compares each stretch with its checksum. In the
harness's three cores:

```text
core      bad stretches   32 KB in        that is
snes9x    0 of 18         198.6 lines     2.60 MB/s, 42.2 KB per frame
bsnes     0 of 18         198.7 lines     2.60 MB/s, 42.2 KB per frame
mesen-s   0 of 18         198.7 lines     2.60 MB/s, 42.2 KB per frame
```

It is the ceiling of the bus: 8 master cycles per byte are 192 lines, plus
the DRAM refresh. All three **seek instantly**: the wait for bit 7 takes
one loop.

**Mednafen** (`snes_faust`, the only one with MSU-1) has the slow seek: 1
or 2 frames each, measured on 2026-09-26 with the battle backdrops ([the
emulators](../../../reference/snes/emulators.md)).

**The FX Pak is not measured**, and it is what matters. Its firmware
(`src/msu1.c` in sd2snes) has a 16 KB buffer in two halves; when the
console crosses into one half, the cartridge's processor refills the other
from the card. **There is no backpressure**: if the console reads faster
than the refill, it reads stale bytes and nobody finds out. That is why the
test ROM compares: on the console, the screen comes out **green** if the
576 KB arrived right, **red** if not and **blue** without MSU-1. The 512 KB
in a row are the worst case: 64 KB without a break, four times the buffer.

### What lengthens the fade

With the cost model of `materials.py` —700 cycles per LZ2 command and 60
per byte, on the high side— over `release`'s maps, against reading the
same raw at the measured speed:

```text
over the 93 maps      raw        today (LZ2 from ROM)   from the .msu, raw
median                17.3 KB     5.0 frames            0.40 frames
p90                   45.0 KB    13.2 frames            1.04 frames
map 66 Lashe Area     62.8 KB    22.3 frames            1.45 frames
map 52 the race       69.4 KB    17.0 frames            1.60 frames
```

And over the 319 of the whole game, a map's raw data has a median of
13.7 KB, a p90 of 30 KB and a maximum of 69.7 KB (map 52): **no map asks
for more than two frames of port**.

**It gets shorter**: four and a half frames in the typical map and twenty
in map 66. Added to that is **one seek per map** if each map's data is
contiguous in the `.msu` —zero in the harness's emulators, one or two
frames in Mednafen, and whatever the test ROM says on the FX Pak—, and
another on returning from a battle if the bytecode lives behind the grid.

**If the FX Pak doesn't sustain 42 KB per frame**, it is read in smaller
pieces: at 8 KB per frame —half its buffer— the heaviest map takes nine
frames, which is still half of what it takes today.

## 4. What happens without MSU-1

Today the rule is that **without MSU-1 the game works the same**: what
comes from the `.msu` replaces something the ROM already has ([the `.msu`
file](../../../internals/the-msu-file.md)). With the whole game that can no
longer hold: the ROM without MSU-1 would have to carry the 8,514 KB.

**What fits without MSU-1** is what there is today: `release` uses 120 of
124 banks. With the cheap things left (section 5: about 7 banks at
`release`'s scale) it is **about 10 more maps**, at 20.8 KB per map. That
is, **without MSU-1 you get to a third of the game**, more or less as far
as it gets today.

### The options

**A. A single ROM**, which carries in the ROM the maps of the beginning
and of the rest only what can't be read from the `.msu`. Without MSU-1,
the game stops at the first door to a map the ROM doesn't have, with a
sign. The problem is the number: what can't be read from the `.msu`
—poses, bytecode, texts, battle, screens, tables— **of the whole game** is
3.0 MB, so what is playable without MSU-1 has to fit in 0.9 MB, **music
included**, and `release`'s music alone is 1.5 MB. **Without MSU-1 you
would get much less far than today**: less than half of `release`.

**B. Two cartridges from the same converter**: `release`, without MSU-1,
as today; and a new one —`completo`— with the whole game, which requires
MSU-1: the music only through the tracks, only the quality effects, and
loading the maps from the `.msu`. The runtime is the same, with both
loading paths, and the converter chooses per map where it comes from.

**C. Only with MSU-1**: one cartridge, the complete one. It leaves out
Mednafen with its default module, which is the one taro uses, and whoever
plays without MSU-1.

### What maintaining B costs

- **One more cartridge to build**: today `just cartuchos` builds three in
  46 seconds with the cache.
- **The test suite stays on `release`** and without MSU-1, as today:
  everything `release` carries is tested the same.
- **The `.msu` path is tested with goldens that already exist**: a map
  that is in both cartridges has to be drawn **the same pixel by pixel**
  loaded from the ROM or from the `.msu`. The harness's three cores have
  the data port, and the harness already builds consoles with MSU-1
  (`test_msu_datos.py`).
- **What nothing settles**: the slow seek. As today with the backdrops,
  only Mednafen has it and no test runs it.

## 5. The alternatives that aren't the MSU-1

### Compressing more with LZ2, without a chip

Today the tiles of the background, of the layer above, of the sprites, the
ChipSet animation and the grid go as LZ2. What goes raw, measured over
`release` with the tools' `lz2`, by the unit in which the ROM would use
it:

```text
what                        unit        raw         LZ2           zlib -9
poses                       512 B     484,352   197,082 (41 %)  (40 %)
block table                 map        99,824    53,945 (54 %)  (39 %)
block passability           map         6,240     2,289 (37 %)  (37 %)
bytecode                    map       120,300    75,410 (63 %)  (44 %)
battlers                    battler   126,043    76,920 (61 %)  (45 %)
battle animations           block      67,696    37,310 (55 %)  (51 %)
light battle backdrops      backdrop   65,536    47,857 (73 %)  (59 %)
font                        block      59,280     9,875 (17 %)  (13 %)
texts                       32 KB     143,114    82,917 (58 %)  (42 %)
music sequences             theme     649,208   369,828 (57 %)  (40 %)
BRR samples                 sample    923,292   917,527 (99 %)  (94 %)
```

**What of that can be used**, which is not the same as what compresses:

- **Not the poses**: they are uploaded in vblank when they change, and
  decompressing costs about 60 cycles per byte; twenty NPCs walking would
  be a frame and a half of CPU. It is exactly what the S-DD1 solves,
  below.
- **Not the sequences**: `irq_music` reads them from the ROM while they
  play, and the longest measures 68 KB, more than any gap in WRAM.
- **The texts, not with LZ2**: it breaks direct access to each box. Their
  study proposes DTE (the task [`uncompressed-texts`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/uncompressed-texts.md)).
- **BRR samples don't compress**: they are already a compressed format.
- **The rest, yes**: the blocks and the bytecode decompressed to WRAM on
  entering the map —behind the grid, see section 2—; the battlers, the
  animations and the backdrops when the battle starts, as the grid already
  goes; the font at boot.

Brought to the whole game, what is usable saves about **470 KB, 15 banks**:
the block table 120 KB, the bytecode 100, the battlers 95, the battle
animations 70, the font 50 and the light backdrops 30. **Against a
shortfall of 142 banks, it doesn't change the answer**; at `release`'s
scale, it is about seven banks, which is what section 4 adds to what fits
without MSU-1.

### The S-DD1

A decompressor in the cartridge that delivers the bytes **during DMA**,
without CPU: Star Ocean and Street Fighter Alpha 2. It is studied entirely
in the wishlist task [`expansion-chips-sa-1-and-s-dd1`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/expansion-chips-sa-1-and-s-dd1.md) —support, memory map, our own
compressor verified against snes9x's decoder—; here goes what was missing,
**against LZ2 and with today's data**:

```text
what                       sample                 raw       LZ2        S-DD1
background tiles, 8 bpp    12 maps of release   149,440    58 %        57 %
sprite tiles, 4 bpp        12 maps of release    83,040    25 %        24 %
poses, 4 bpp, 512 B each   119 of the 946        60,928    41 %        32 %
```

**On the tiles that already go compressed, the S-DD1 ties with LZ2.** What
it really gives is **decompressing without CPU**, and the only thing that
can't be compressed today because of that is the poses: 941 KB of the
whole game that would end up at about 300, **about 20 banks**. And it has
its own mapper, which goes past 4 MB without ExHiROM: Star Ocean uses
6 MB.

### The SPC7110 and the SA-1

- **The SPC7110** (three Hudson games) decompresses from a "data ROM"
  through a port (`$4800`), and its memory map is HiROM: 1 MB of program
  at `$C0-$CF` and the data ROM in 1 MB windows at `$D0-$FF`, switchable
  (`$4831-$4833`); the games reach 5 MB (fullsnes, "SNES Cart SPC7110
  Memory and I/O Map"). It requires moving the whole cartridge to HiROM.
  **The FX Pak doesn't support it**: sd2snes's `src/smc.c` detects it and
  answers `MENU_ERR_NOIMPL` (cloned at `cf7e21d`, v1.11.2). With that it is
  ruled out.
- **The SA-1** doesn't decompress: it is a second 65816 at 10.74 MHz. What
  it adds in space is its mapper, **up to 8 MB** in 1 MB windows, and in the
  memory map it moves SRAM to the BW-RAM at `$40` and puts FastROM in
  doubt. It is in the same wishlist study.

**Support**, from the same study and the cloned firmware:

```text
chip      FX Pak Pro                       snes9x  bsnes  mesen-s  MSU-1 together
S-DD1     yes, since v1.10.0               yes     yes    yes      yes on the FX Pak
SA-1      yes, since v1.9.0, up to 8 MB    yes     yes    yes      yes on the Pro (Mk3)
SPC7110   **no** (MENU_ERR_NOIMPL)         yes     yes    yes      —
```

The three cores have the three chips in the cloned code (`sdd1.c`,
`spc7110.c`, `sa1.cpp` in snes9x; `sfc/coprocessor/` in bsnes; `Sdd1.cpp`,
`Spc7110.cpp`, `Sa1.cpp` in mesen-s). **What wasn't verified from here** is
that the harness's installed binaries have them compiled in —no ROM with a
chip was run— nor anything on the FX Pak: that is seen by building the ROM
with the chip's header and running it, and on the FX Pak with its menu,
which says which chip it detected.

### ExHiROM, or a bigger cartridge

**Up to 8 MB**, and the FX Pak supports it (`src/smc.c`, map mode `$25`).
But the whole game is 8,514 KB of data plus the code, against 8,192: **it
doesn't fit**, and about 400 KB are missing before counting the packing.
And it changes how every address is computed (see the decision
`el-cartucho-se-queda-en-4-mb.md`, "the cartridge stays at 4 MB").

### All together

```text
path                           what it gains          enough for the game?
LZ2 where possible             ~470 KB, 15 banks      no
DTE in the texts               ~100 KB (estimated)    no
S-DD1 on the poses             ~640 KB, 20 banks      no; and changes chip
sharing tiles between maps     blocked by VRAM        no
                               (graphics study)
ExHiROM or SA-1, 8 MB          +4 MB                  no: ~400 KB missing
the maps through the .msu      1.9 MB                 not alone
music only through MSU-1       3.4 MB                 not alone
the maps and the music         5.3 MB: ROM at 3.0     **yes**, with 0.9 MB free
  through the .msu
```

**What would have to be reviewed of the 4 MB decision** if someday a chip
is chosen: it says that "going past that is ExHiROM", and with the S-DD1 or
the SA-1 it isn't —each brings its own mapper—. What doesn't change is the
conclusion: not even 8 MB is enough, and with MSU-1 there is no need to go
past 4.

## 6. The recommendation

**The whole game goes through the MSU-1, in a cartridge of its own, and
`release` stays as it is.** In phases:

**Phase 0 — measure the FX Pak.** `just msu-puerto` and take
`rom/build/msu-puerto/msu-puerto.sfc` with its `.msu` to the console:
green, red or blue. **It costs five minutes of taro's time**, and decides
whether phase 1 reads at full speed or 8 KB per frame. If it comes out red,
it is worth repeating with a pause between stretches to find out how much
it sustains.

**Phase 1 — the maps from the `.msu`, in a `completo` cartridge.** The
converter writes what is uploaded on entering each map —tiles, colors,
grid, ChipSet animation— raw into the `.msu`, in a fixed region per map,
like the backdrops; the ROM, for a marked map, seeks and reads by DMA
straight to VRAM and WRAM, instead of decompressing. Everything else stays
in the ROM. **The same runtime in both cartridges**; `release` doesn't
change a byte. The test: the maps that are in both are drawn the same by
both paths.

*Risks*: the FX Pak (phase 0); the slow seek, which as today no test
settles; and whatever the battle overwrites, which has to be read again.

**Phase 2 — the music only through MSU-1 in `completo`.** No sequences or
instrument samples in the ROM for the maps `release` doesn't carry, and
only the quality effects. It is what weighs the most (3.4 MB) and it is
almost all removal. With this **the whole game fits**: 3.0 MB of ROM.

*Risks*: a theme without an MSU-1 track doesn't play (the done task
[`every-theme-has-an-msu-1-track`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/every-theme-has-an-msu-1-track.md)); and the ARAM split, which
today counts on the ROM's samples.

**Phase 3 — whatever is needed after, in this order.** The converter
limits of section 1 —the encounter index, the leader candidates, the audio
panic— and the five maps that don't fit in VRAM, which are work anyway.
Then, if `completo` gets tight: the bytecode and the block table to WRAM,
behind the grid (−0.7 MB of ROM, and more CPU to read the bytecode:
measure it in the race). The S-DD1 only if with all that it isn't enough:
it changes chip to gain 20 banks.

**For `release`, without MSU-1**: the cheap things of section 5 —LZ2 on
blocks, battlers, animations and font; DTE in the texts— and the bank
packing give it about seven banks, ten maps. It is what Tacuarita is
already doing with Tangle Forest, and it is the ceiling of what is
playable without MSU-1.

## How it was measured

- **`release`'s space**: `just espacio`, and `rom/build/release/` built
  with `NO_CACHE` just like the test suite.
- **The whole game**: eleven copies of the project file, each with
  `[maps] below` at 400, `excluded` with the ranges that aren't its own and
  the five maps that don't fit, and `["--no-timer"]` in `flags`; maps 1 to
  10 in all of them. Each was converted with `rm2k-snes-cartridges
  --project <copy> --convert-into <dir> --without-tracks release`, and from
  each `mapdata.inc` and `musicdata.inc` the bytes of each label (`.byte`,
  `.word`, `.res`…) were added up with the rule of section 1. The runs
  were: 1 to 119, 120, 122, 123 to 126, 128 and 129, 130 to 139, 140 to
  249 without 148 and 207, 250 to 351 without 250, 285 and 288, 207 and
  288 alone, and the base with maps 1 to 10 and the test ones. None links
  —the one for 1 to 119 asks for 134 banks—, and it isn't needed: the size
  comes from the labels, before the packing.
- **Per map**: from the fields of `map_table` of each run (`MAP_TILES`,
  `SPRITE_TILES`, `MAP_BW`…) and from `crudos/`.
- **The RAM**: the harness (`tanda.partida`) over `release` in snes9x,
  with the WRAM read every 15 or 20 frames.
- **The port**: `just msu-puerto`.
- **LZ2**: the installed `lz2`, per unit, over `release`'s labels.
  **S-DD1**: the compressor from the chips wishlist, over `crudos/` and over
  one in every eight poses.
- **Today's load time**: the model in `materials.py`, with the LZ2 commands
  counted with `lz2 stats` over the same streams the converter builds.
