# Lossy: audio

## Each sample at the rate its worst package allows

Each package with its effects has to fit in the 64 KB of ARAM, so a sample
gets the rate its fullest package leaves; where a package lacks some of
the tracks that use a sample, those play a copy that does not pay for it.

- **Loses**: instrument brightness where packages are full.
- **Where**: `allocate` and `copies` in `bank.rs` of
  `rm2k-snes/rm2k-snes-audio/`.
- **More**: [A single sample bank](../lossless/audio/the-sample-bank.md).

## Past 256 samples, the least used are dropped

The SPC700 indexes its samples with one byte; past that, the least used
are dropped and the notes that needed them are silent.

- **Loses**: those notes.
- **Where**: `compile.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../../internals/audio.md).

## A package whose music would go below 6 kHz is relieved

A map whose package only fits in the ARAM with its music below 6 kHz
—the sound effects' own rate— is relieved instead: its songs are uploaded
when a `PlayBGM` asks for them, with a pause, and the last effects of its
list are left out until the music fits at 6 kHz next to the rest. The
Frozen World's map 1, with 41 sound effects and six songs, did not fit
even at the lowest rate; A Blurred Line's map 3 did, with `evilrhys` at
4.5 kHz, and since 2026-10-16 it is relieved too —taro's, by ear: "4k is
too little"—.

- **Loses**: a pause at those `PlayBGM`s, and the effects left out, each
  named in `degradations.json`.
- **Where**: `relief.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../../internals/audio.md).
