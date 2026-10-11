# The `.msu` file: data the MSU-1 serves to the ROM

The MSU-1 has two parts: the audio tracks (`<rom>-N.pcm`, see
`rm2k-snes-msu`, in `rm2k-snes/rm2k-snes-audio/src/tracks.rs`) and a
**data port** that reads `<rom>.msu` as a stream. Until 2026-09-25 the
`.msu` was empty and only served to turn the MSU-1 on. Since that day it
carries **the battle backdrops**, which started as a pilot, and since
2026-09-27 **all of the game's**, whether or not they are in the
cartridge's maps: see "The backdrops" below. And since 2026-09-26, behind
them, **the quality sound effects** of each audio package: see "The
effects" below.

The ROM carries the backdrops the cartridge's battles ask for, and **light
ones**: 128x64 at 4bpp and 16 colors, which the ROM doubles in size,
against the 256x128 at 8bpp and 96 colors of the `.msu` —see `scene.rs` in
`rm2k-snes-convert`—. That way you can tell by eye which side the backdrop
came from, and each one costs in the ROM an eighth of what it weighs in the
`.msu`. A battle whose backdrop the ROM doesn't carry uses, without MSU-1,
a fallback one.

## The rule

**Without MSU-1 the game works the same.** taro plays in Mednafen, which
doesn't have it (in its default module; see [the
emulators](../reference/snes/emulators.md)). So what comes from the `.msu`
**replaces** something the ROM already has, never adds it: without MSU-1,
with a `.msu` from another build, empty or truncated, or if the MSU-1
doesn't finish seeking in time, the ROM uses its own.

## The port, from the console's side

```text
$2000..$2003  write: the position, 32 bits little-endian. The write
              to $2003 is the one that seeks.
$2000         read: bit 7 set while seeking ("data busy")
$2001         read: the next byte; advances by itself
```

It is read by DMA with the source **fixed** at `$00:2001` —bit 3 of
`DMAP`—, which runs at the speed of any DMA, 8 master cycles per byte:
32 KB are about three quarters of a frame, the same as from ROM. Which
emulators implement it: in [the emulators](../reference/snes/emulators.md).

## The format

`rm2k-snes-audio` builds it, in `msu_data.rs`, and its documentation is the
reference: an 8-byte signature (from the sha256 of what follows), `"ABLD"`,
the version, an index of `(position, length)` per entry, and the entries.
Each backdrop is two: its 512 tiles of 8bpp and its 96 colors, exactly as
they go to WRAM and CGRAM. The ROM has something else in `backdrop_dir` and
`backdrop_cgram`: the light fallback, which `scn_fill` and `scn_double`
expand to 8bpp and double in size.

The layout, since version 2 (2026-09-27):

```text
$000000  the header and the index, padded with zeros up to $10000
$010000  the game's backdrops, by number: backdrop k takes $8200
         bytes from $10000 + k × $8200 —its tiles, and $8000
         further on its colors; the rest is padding up to the
         512-byte sector—
behind   the effects, from the end of the last backdrop place
```

**The backdrop region is fixed**: backdrop k is at the same byte in the
`.msu` of any cartridge, because a backdrop's number comes from the game
and not from the maps that are carried (see "The backdrops"). In version 1
they went right behind the index, and the index grows with each
cartridge's effects: a backdrop's place moved with any audio change. How
many backdrops there are and how much the `.msu` weighs is printed by the
converter, in `conversor.log` ("`.msu:` N fondo(s) y M efecto(s) en B
bytes", that is, N backdrop(s) and M effect(s) in B bytes).

The converter writes it —it is the one that has the bytes and decides the
order—, next to each `.sfc` and with its name: `rm2k-snes-cartridges`
passes it `--msu`. Both cartridges carry it, and the test of the MSU-1 path
runs on `release`, which is the ROM that is played.

## How the ROM knows the `.msu` is its own

The converter emits in the `.inc` the signature it wrote
(`msu_data_signature`) and where each backdrop ended up
(`msu_backdrop_pos`, by backdrop number: it is the arithmetic above, in a
table so the ROM doesn't multiply). When a battle with a backdrop starts,
`msu_data_valid` —in `runtime/msu1.s`— seeks position 0 and compares
the 8 bytes; if they match, `scn_fill` and the colors of `scene_upload`
—in `runtime/battle_scene.s`— read from the `.msu`, and `SCN_MSU` is
left at 1.

**The signature is of the content, not of the commit**: a `.msu` from
another build with the same backdrops is accepted, and that is fine,
because they are the same bytes in the same positions. (The light
fallback, "The light fallback", didn't change the `.msu`: the quality one
is the one from before, byte for byte, and with it the signature.) What it
does **not** cover: a `.msu` with the header intact and the data damaged.
The ROM can't hash 32 KB per backdrop at the start of each battle.

The positions come from the `.inc` and not from the file's index: once the
signature is accepted they are the same data, and reading the index would
be one more seek per battle. The index stays for the tools
(`rm2k-snes-audio msu-index`) and for adding entries without changing the
format.

## The backdrops

**The game's backdrops** are all the ones a battle can ask for: the ones
named by the `EnemyEncounter` and `ChangeBattleBG` commands of the whole
game, those of the map tree and those of the terrains. They are sorted by
name ignoring case, which is how RM2k looks them up, and each one's place in
that list is its **number**: `scene.game_backdrops`. A name that is in
neither the game nor the RTP (`RTP_DIR`) doesn't go in; that battle
goes without a backdrop, as in RM2k.

Which backdrop a battle asks for is RM2k's rule —`Game_Map::SetupBattle`
and `Spriteset_Battle` in easyrpg-player—: the one the `EnemyEncounter`
names; or, if it is a random encounter or the command asks for "the one of
the place", the map's, going up the tree; and if the map names none, **the
one of the terrain of the cell the hero stands on**. The ROM resolves that
one when the battle starts (`scn_terrain`, in
`runtime/battle_scene.s`), with `backdrop_terrain`. That is how the
battles in the world come out.

**The ROM carries all the ones the cartridge's battles can ask for**: the
ones the troops name, those of the maps with random encounters and those of
the terrains of those maps when they name none —see `scene.rs` in
`rm2k-snes-convert`—. Without MSU-1, a battle whose backdrop the ROM
doesn't carry uses **the fallback**, `[battle] fallback_backdrop` in the
project file —why that one, in its comment—: `backdrop_fallback` says, by
backdrop number, which of the ROM's is drawn. taro asked for it on
2026-09-27, because the battles in the world came out black, and black is
confusing; the same day he asked for the ROM to carry all of `release`'s,
and since then the fallback is left for a troop that fights "of the place"
in a map without encounters, where the converter can't know what terrain
the hero will be standing on. With MSU-1 each battle reads its own from the
`.msu`. The ROM carries two numbers per battle: `SCN_BACKDROP`, the game's,
which is the one looked up in the `.msu`, and `SCN_FALLBACK`, the ROM's.

What each backdrop the ROM carries costs is printed by the converter
("fondo de batalla … en la ROM … B"): 4,096 bytes of tiles and 32 of
colors, which is a property of the format, plus 4 of pointer.

## How long it takes

It is measured with `SCN_FRAMES`, which `scene_upload` leaves in RAM when
opening the battle: `pruebas/abl/test_msu_datos.py` in the ABL port builds
both paths, and reading it there is one line. In snes9x and in bsnes the
`.msu` takes **less** than the ROM —measured in the droid battle—: both are
DMA at the same speed and seeking is instant there, but the fallback takes
one DMA per tile for the fixed planes and is then enlarged by the CPU,
pixel by doubled pixel: about four frames more than when it was 256x128
—measured with `SCN_FRAMES` in the world battle, on 2026-09-27—.

**Mednafen is the only emulator in which seeking takes time**
(`-force_module snes_faust`; what each one does, in [the
emulators](../reference/snes/emulators.md)): each seek costs one or two
frames, and there are four per battle —the signature, the colors and the
tiles for each of the two WRAM buffers—. Measured on 2026-09-26 in the
droid battle, played from the title screen with the map's track playing:
`SCN_FRAMES` at 11 with the `.msu`, against 5 without it in Mednafen and 4
with it in snes9x and bsnes. That is about seven frames of waiting, a little
over a tenth of a second. Mednafen's RAM is read by saving the state (F5):
the `.mc0` in `~/.mednafen/mcs/` is a gzip, and the WRAM goes whole in its
`WRAM` entry.

On the FX Pak seeking inside its 16 KB buffer is immediate, and outside it
means reading the SD card —`prepare_data` in `src/msu1.c` of sd2snes, its
firmware—. That is **not measured**. The cap on the wait —`MSU_WAIT`, in
`runtime/msu1.s`— is about ten times what Mednafen takes.

If a seek doesn't arrive in time, what was already read from the `.msu` is
the quality backdrop and what follows would come from the light one, and
they share neither colors nor tiles: `scene_upload` notices and redoes the
whole backdrop from the ROM. No emulator takes long enough to cut the wait,
so that path **is not run by any test**.

## The effects

Behind the backdrops go the sound effects of each audio package, whole and
each at the rate that package allows with ARAM free of music —the split
belongs to `rm2k-snes-audio`, in its `msu.rs` and `rates_per_package`—: by
package, in the order of the table, and inside each one in SRCN order,
which is how `upload_placed` uploads them. That way the ROM **seeks once
per package** and reads straight through; an effect that is in two packages
goes twice. `cartridge::msu` in `rm2k-snes-audio` writes it, and also emits
what the ROM needs: `se_msu_pkg` and `se_msu_rows` —where each effect of
each package is and how long it is— and `se_msu_pitch_pkg` and
`se_msu_pitch` —the pitch of each sound with each package's version, only
for the sounds whose effect comes from there, and two packages with the
same list share it—, and next to it a readable `efectos.json`.

The signature is the same as the backdrops' and is checked once per
power-on, at the first package load (`se_msu_prepare`, in
`runtime/msu_effects.s`). Without the signature, the effects come
from the ROM as always. A seek that doesn't arrive in time leaves that
effect not uploaded: it doesn't sound, because the ROM's version has a
different pitch. `pruebas/abl/test_msu_efectos.py` in the ABL port covers
it, except for that wait, for the same reason as the backdrops'.

## How it is tested

The test suite runs without MSU-1, so its battle goldens are the light
fallback. `pruebas/abl/test_msu_datos.py` in the ABL port runs both paths
in snes9x and bsnes and compares **each one against its golden**
—`msu-datos-rom` and `msu-datos-msu`— and the clean backdrop in WRAM
against the bytes the converter builds: the quality one as is and the
light one expanded to 8bpp and doubled. The same with a battle in the
world, whose backdrop is that of the terrain the hero stands on
—`msu-mundo-rom`, its fallback, and `msu-mundo-msu`, the quality one—, and
that each backdrop is in its fixed place with the same bytes in the `.msu`
of every cartridge. The fallback is covered by
`test_escena_una_pelea_cuyo_fondo_no_esta_usa_el_reemplazo`, in
`pruebas/rpgmaker/test_batalla_escena_dibujo.py` in the ABL port.

**The wait is not covered by the test suite**, because the three libretro
cores the suite uses seek instantly, and the harness can't simulate the
delay: it sees memory, not the bus, so it has no way to answer anything
else when the ROM reads `$2000`. What exercises it is Mednafen, by hand: a
cartridge that opens the battle when the game starts —the flags of
`release` with `batalla-droide` as page 0—, Xvfb and `xdotool` to get past
the title screen, F5 in the battle, and reading `SCN_MSU` from the `.mc0`.
That is how it was verified on 2026-09-26, and also by playing up to the
droid with the test suite's save loaded into Mednafen's SRAM. Putting it in
the suite would cost one more cartridge and a test that runs in real time
against an emulator with a window; it wasn't done. What still nobody runs
is the cut by the cap, above.
