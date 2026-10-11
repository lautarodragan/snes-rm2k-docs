# The pipeline

What each step does and why the tools read a JSON dump is in [From a game
to a ROM](../pipeline.md). This is the same road with the names of the
binaries and what each one leaves behind:

```text
--game-dir (.lmu .ldb .lmt)       --ditto unpack---------------->  data/ (JSON)
data/ + parches/manual/
+ images, MIDI and WAV            --rm2k-snes-convert-----------> build/<rom>/
  (--game-dir, --rtp-dir)           (and its stages: wally, events,   mapdata.inc, musicdata.inc,
                                     screens, images, battle,
                                     mapdata, patches, audio)
                                                                  <rom>.msu (battle backdrops),
                                                                  parches/ (decisions)
runtime/*.s + those .inc    --rm2k-snes-assemble----------> <rom>.sfc + <rom>.sfc.sym
                                    (bank packing, ca65 + ld65)   and, with [rom] msu = "required",
                                                                  what does not fit, behind <rom>.msu
<rom>.sfc + MIDI or replacements  --rm2k-snes-msu---------------> <rom>-N.pcm
                                    (fluidsynth, ffmpeg)
```

The paths on the right belong to the game's project —where its
`rm2k-snes.toml` is, which declares them—, and `<rom>` is its
`[rom] name`. `rm2k-snes-cartridges` runs all of that for each cartridge
the project declares. How A Blurred Line calls it, with which recipes and
which flags: [its pipeline](../ports/abl/pipeline.md).

## When a cartridge is rebuilt

`rm2k-snes-cartridges` rebuilds a cartridge only when its stamp
—`sello.txt`, next to the ROM— no longer matches: the cartridge's converter
flags, its test cases, and a **fingerprint** of everything else that goes
into the ROM. The fingerprint looks at contents, never at dates:

- the whole `runtime/`, and the binaries that build: `ca65`, `ld65`, the
  converter and the stages it runs, and `rm2k-snes-assemble`;
- the game's dump, `data/`, whole, and its hand-made patches, its project
  file and the files that file names —custom menus, its own font—;
- **the original game's resources**: every file below `--game-dir` with an
  extension the stages read —`.png`, `.bmp`, `.xyz`, `.mid`, `.wav`—, with
  its name. Not the `.lmu`, `.ldb` and `.lmt`, which reach the ROM through
  the dump, nor the saves, which change whenever someone plays the
  original. It is what the stages *can* read, not what they read: a
  resource the game ships and never uses goes in too.

**A game or an RTP that is a `.zip` goes in by the `.zip`'s content**,
whole: hashing even the biggest of the ported games takes tens of
milliseconds.

**The RTP and the SoundFont, as directories, go in by their path, not
their content**:
they are not edited, and hashing them would read them on every run. If one
is changed in place, `rm2k-snes-cartridges --force` rebuilds the cartridges
named —or all of them— without looking at the stamp. The MSU-1 tracks do
not need it: they are outside the stamp, and their own cache keys on the
SoundFont's content.

Whoever asks whether a cartridge is up to date computes the same
fingerprint, so it needs the same machine flags: `rm2k-snes-space` takes
those of `rm2k-snes-cartridges`, and a game's tests pass them to
`--list --json`. Without `--game-dir` the fingerprint is an error, not a
guess.

## A game or an RTP as a `.zip`

`--game-dir` and `--rtp-dir` take a directory or a `.zip` of one, with the
game's files at the root of the archive. Nobody reads inside the `.zip`:
the lookups are several, in several processes, and some hand a path to
`fluidsynth` or `ffmpeg`. Instead, every tool that reads the game calls
`Environment::unpack`, in `rm2k-project`, right after reading its flags;
that unpacks the `.zip` once into `zip/` in the project's cache, named by
its content, and from there on the value is that directory —also for the
tools it runs—. A tool that forgets to call it gets an error, not an empty
game: a lookup that finds nothing in the game falls back to the RTP without
a word.

Whoever reads the game and is not a tool of the suite —Ditto in a game's
`datos` recipe, a game's tests— asks `rm2k-snes-project --game-dir X
--unpacked game_dir` for the directory, and gets the same copy.

A `.zip` is what keeps the original game untouched: what the port changes
goes in its patches, not in the game.
