# Audio

Which piece does what, and where its reason is. Everything else lives in
the code.

Audio is handled by the **SPC700**, a separate processor with its own 64 KB
of ARAM; the 65816 doesn't touch the DSP, it only talks to the SPC700
through four ports. **The logic lives in the music compiler**,
`rm2k-snes-audio` —a Rust project in `rm2k-snes/rm2k-snes-audio/`,
which the converter runs from the PATH—: it decides which note goes to
which voice, with which sample and which envelope, and the console only
plays. The paths below that end in `.rs` are in its `src/`.

```text
MIDI + SoundFont  --rm2k-snes-audio-->  musicdata.inc: the bank, one stream
                                        per theme, the packages of each map
per-note stream   --music_frame-->      DSP writes, frame by frame
writes            --dsp_music-->        the SPC700 driver
```

- **Boot**: `spc_upload` (`runtime/spc700.s`) uploads through the
  IPL the driver and the sample directory, nothing else. What the driver
  serves —(register, value) pairs for the DSP, triples for ARAM, going back
  to the IPL— is in `DRIVER`, in `spc700.rs`. How long the ROM waits at
  power-on is `BOOT_FRAMES`, which each cartridge carries in its
  `musicdata.inc`: `BOOT_FRAMES_FLOOR` (`runtime/far_ram.s`) or the
  estimate for the boot map's package, whichever is larger. See [boot is
  sized for the boot
  package](../optimizations/lossless/audio.md#boot-is-sized-for-the-boot-package).
- **The stream is per note**: notes, releases, changes of volume or pitch,
  and waits, which the 65816 expands into the same writes that used to go
  in the stream. The format is in "the per-note format" in `stream.rs`, and
  the opcodes in `rm2k-snes/bytecode/src/music.rs`; `irq_music`
  (`runtime/music.s`) runs one music frame per video frame.
- **What a theme plays the same is said once**: an `OP_REPEAT` goes back,
  reads as many events as the stream already had and continues after the
  jump, one level only. They are the same bytes, so they write the same.
  See "repeats" in `stream.rs`.
- **A note names its sound in one byte**, out of the theme's table of
  sounds (pitch, sample, envelope and release). A theme with more than 256
  says `OP_SOUND_PAGE` before the notes that name the next 256, and the
  65816 moves `MUS_BASE` there; one with 256 or fewer never says it. The
  page is the decoder's state, like its register cache, so a repeat reads
  its bytes in the page the stream it stands for was in.
- **The eight voices belong to every channel** and are handed out note by
  note: a note takes a free voice or steals one by priority. See `assign`,
  `victim` and `frame_order` in `voices.rs`.
- **Volume has a ceiling per theme**, measured and versioned in
  `patches/auto/music/ceilings.toml` in the ABL port (`just ceilings`): see
  `ceilings` in `game.rs`.
- **The samples come from the SoundFont** the game was composed with
  (`samples.rs`; `SOUNDFONT` points to another), and Gunter, which the
  compiler uses as a library, turns them into BRR.
- **A single sample bank for the whole cartridge, uploaded in packages, one
  per map**, and each sample with the budget of its worst package: `Bank`
  and `allocate` in `bank.rs`, and the reason in [a single sample
  bank](../optimizations/lossless/audio/the-sample-bank.md). `package_load`
  (`runtime/audio_package.s`) uploads it while the music plays; if
  the theme that is playing and the new package don't fit together, the
  theme wins: [the playing theme wins and the effects
  wait](../decisions/the-playing-track-wins-and-the-sound-effects-wait.md).
- **A package that does not fit in the ARAM even with every sample at the
  minimum is relieved, not a stop** (`relief.rs`, since 2026-10-15): its
  songs go separate —each uploaded when its `PlayBGM` asks for it, with a
  pause, as `[music] apart_themes` does; all of them if none plays on
  entering, from the end of the list until the rest fits if the first does—,
  and then the sound effects at the end of its list are left out until the
  music fits at the effects' own rate, 6 kHz. A package that fits at the
  minimum is not touched, however low its music goes: how far a map's
  effects push its music down is the game's decision by ear
  (`paid_by_music`). Each relief is a loss in `degradations.json`
  —`songs-uploaded-on-play`, `sound-effects-left-out`,
  `package-waits-for-playbgm`—, which the converter reads from the stage's
  `audio.json`. The case is The Frozen World's battle screen: six songs it
  picks one of per fight and forty-one effects, ~89 KB of effects alone.
- **The SPC700 directory** has one entry per music sample —its number in
  the cartridge, which is the stream's SRCN— and behind them some **places
  the effects share**: two effects that never go in the same package go to
  the same place, so there need to be as many as the effects of the fullest
  package, and what is left of the directory is for the copies.
  `effect_places` in `bank.rs`; the ROM notes which effect it uploaded to
  each place in `FAR_EFFECT_IN` (`record_effect`, in
  `runtime/audio_package.s`).
- **Two keys whose samples came out the same share their entry**: a copy
  that reached the same rate as what it copies, or two keys of a program
  that pick the same zone, have the same BRR and loop, and they are stored
  and uploaded once. The tracks are built with one entry per key —the
  allocation, the copies and the ceilings' fingerprint count that way— and
  renumbered afterwards: `Bank::directory` in `bank.rs` and
  `merge_identical` in `compile.rs`, which checks that every track writes
  the same to the DSP with the same samples behind its SRCN. Until
  2026-10-14 each key had its own, and ABL's `release` stored 201 KB twice.
- **Sound effects** —`PlaySound`— steal two voices from the music while
  they last, the ones the voice assignment fills first with percussion:
  `runtime/sound_effects.s` and `effects.rs`. The ones that go whole
  and at a higher rate —`[sound_effects.whole]` in the project file,
  `rm2k-snes.toml`— are fitted into what the music leaves free in each
  package, so they don't lower the rate of any instrument. The ones in
  `paid_by_music` —the thunder of the opening and the ones taro chose whole
  even if they cost— are paid for by the music of their package: [the
  thunder goes whole and the rain pays for
  it](../ports/abl/decisions/the-thunder-plays-whole-and-pays-for-the-rain.md). One that
  sounds with another sample in one map is an alias: `per_map`. All three
  belong to the game, and each entry carries its reason in the file.
- **`FadeOutBGM` lowers the theme and nothing else**: the volume of each
  music voice, or that of the MSU-1 track, and never the DSP's master
  volume, which is also the effects'. `bgm_fade_tick`, in
  `runtime/music.s`.
- **The MSU-1**: every theme plays from a PCM next to the ROM, and the ROM
  silences the SPC700 meanwhile. The number of each track is the theme's
  place in the game's `Music/` —`track_numbers` in `game.rs`—, so it
  doesn't depend on the cartridge; `rm2k-snes-msu` builds them
  (`tracks.rs`). With MSU-1, a package doesn't upload the samples of the
  themes that have a track, unless the track was missing from the card:
  `song_per_msu`, in `runtime/audio_package.s`.
- **Effects with MSU-1**: while the SPC700 plays no music, the effects also
  get voices 0 to 5, and each `PlaySound` takes a free voice of the eight
  —a new copy of a sound still playing too, so copies overlap as in RM2k—
  and only steals, from the one with the fewest frames left, when all eight
  are busy (`se_msu_choose`). With the SPC700 playing music there are two
  voices, and a new copy of the same sound restarts the old one's voice.
  And if the `.msu` is this cartridge's, each package's effects are
  uploaded from there, whole and each at the rate the package allows now
  that the music isn't in ARAM —one version per package—: if they don't all
  fit, the one that loses the least of what is heard goes down first
  (`rates_per_package`, in `effects.rs`). Without MSU-1, or with another
  `.msu`, the usual. The split is in `msu.rs`; the ROM side, in
  `runtime/msu_effects.s`. See also [the `.msu` file](the-msu-file.md).

Which test covers what: `tests/rpgmaker/test_musica_*.py` in the ABL port
run the ROM —the writes, the voice assignment, the package, the ceilings—
and the tests of `rm2k-snes-audio` (`just crate-test
rm2k-snes-audio`, in the-advocate) look at the stream without a ROM.
