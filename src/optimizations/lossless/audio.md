# Lossless: audio

## The stream is per note, with repeats

A theme travels as notes, releases and waits, which the 65816 expands
into DSP writes; what a theme plays the same is said once with an
`OP_REPEAT` that goes back and reads the bytes again.

- **Saves**: ROM in the music.
- **Where**: "the per-note format" and "repeats" in `stream.rs` of
  `rm2k-snes/rm2k-snes-audio/`; `irq_music` in `runtime/music.s`.
- **More**: [Audio](../../internals/audio.md).

## A note names its sound in one byte

A note names its sound by an index into the theme's table of sounds, and
a theme with more than 256 pages through them with `OP_SOUND_PAGE`.

- **Saves**: ROM in the music.
- **Where**: `stream.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../../internals/audio.md).

## A single sample bank, uploaded in packages per map

The tracks share one sample per General MIDI program and per drum hit,
and what goes to the ARAM is a package per map: each package with its
effects has to fit in the 64 KB, not the whole bank.

- **Saves**: ROM and the one-byte SRCN; the ARAM is spent on what the map
  plays.
- **Where**: `Bank` and `allocate` in `bank.rs` of
  `rm2k-snes/rm2k-snes-audio/`; `package_load` in
  `runtime/audio_package.s`.
- **More**: [A single sample bank](audio/the-sample-bank.md).

## Effects share places in the directory

Two sound effects that never go in the same package go to the same place
in the SPC700's directory, so the directory needs as many effect places as
the fullest package has effects.

- **Saves**: directory entries, which are one byte's worth.
- **Where**: `effect_places` in `bank.rs`; `record_effect` in
  `runtime/audio_package.s`.
- **More**: [Audio](../../internals/audio.md).

## Identical samples share their entry

Two keys whose samples come out the same —the same BRR and loop— are
stored and uploaded once.

- **Saves**: ROM and directory entries.
- **Where**: `Bank::directory` in `bank.rs` and `merge_identical` in
  `compile.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../../internals/audio.md).

## With MSU-1, the themes with a track upload no samples

A package does not upload the samples of the themes the MSU-1 plays,
unless the track is missing from the card; the effects then get the ARAM
the music left.

- **Saves**: ARAM and loading time.
- **Where**: `song_per_msu` in `runtime/audio_package.s`;
  `rates_per_package` in `effects.rs`.
- **More**: [Audio](../../internals/audio.md), [The `.msu` file](../../internals/the-msu-file.md).

## Boot is sized for the boot package

Boot waits for loading the map, the driver and the directory through the
IPL, and the boot map's audio package, with a margin —not for a full
ARAM—. Since the per-map packages, the IPL uploads only the driver and the
directory, and the samples go through the driver's command 3, three bytes
at a time, so what goes up at power-on is a single package and boot can
be measured against it. It replaced a boot sized for the ARAM ceiling,
which froze the map at power-on for almost two seconds.

**Each cartridge carries its own** `BOOT_FRAMES`, since 2026-10-11: the
estimate for its boot package, or `BOOT_FRAMES_FLOOR`, whichever is
larger. The floor keeps a cartridge with a small package on the frame it
always started on, with a byte-for-byte identical ROM; it lives in the
runtime and not in each game's project because what it protects is the
runtime's —the loop starting on the same frame whatever small data goes
in—. The only ceiling left is the byte the ROM counts boot frames in.

- **Saves**: frames at power-on.
- **Costs**: if the boot map's package grows, that cartridge's boot grows
  with it, by itself. The tests read it from the symbol table, so it moves
  no golden.
- **Where**: `boot_frames` in `rm2k-snes/rm2k-snes-audio/src/emit.rs`,
  which `rm2k-snes-audio cartridge` writes into the cartridge's
  `musicdata.inc`; `BOOT_FRAMES_FLOOR` in `runtime/far_ram.s`.
- **More**: [Audio](../../internals/audio.md).
