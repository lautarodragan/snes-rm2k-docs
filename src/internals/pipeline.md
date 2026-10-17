# The pipeline

What each step does and why the tools read a JSON dump is in [From a game
to a ROM](../pipeline.md). This is the same road with the names of the
binaries and what each one leaves behind:

```text
--game-dir (.lmu .ldb .lmt)       --ditto unpack---------------->  data/ (JSON)
data/ + patches/manual/
+ images, MIDI and WAV            --rm2k-snes-convert-----------> build/<rom>/
  (--game-dir, --rtp-dir)           (and its stages: wally, events,   mapdata.inc, musicdata.inc,
                                     screens, images, battle,
                                     mapdata, patches, audio)
                                                                  <rom>.msu (battle backdrops),
                                                                  patches/ (decisions),
                                                                  degradations.json
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

## What the cartridge does with less than RM2k

Next to each ROM the converter writes `degradations.json`: **every place
where the cartridge runs something with less than RM2k does** —a command
accepted without being done, a parameter read and dropped, a graphic
change skipped, a teleport to a map the cartridge does not carry turned
into a message box, a ChipSet animation cut to fit, a map's rain or
battle animations not drawn—. A page left out whole is not in it: that is
`rm2k-snes-events culprits`. Nor are the colours the converter merged,
which are the patches' (`patches/`, above).

It is **complete by construction**: each entry is noted where the loss
happens, not kept in a list by hand. The event compiler notes the
commands, in the arm of `compile.rs` that compiles each one, and its
`losses.rs` keeps where it is; Wally notes what a map does not draw, the
emission what it cut, the screens what they cut or merged, the converter
its own decisions —the events left out for RAM, a hero's flash on a shared
palette—, and the audio stage what a package that did not fit in the ARAM
lost, which it leaves in its `audio.json` under `losses` because it runs
last; `degradations.rs` in `rm2k-snes-convert` gathers them and writes the
file after the music. A page that does not compile takes its losses
back, as it takes its texts back, so what is listed is what reaches the
cartridge.

Each entry has a `kind`, a stable slug to count by —`bgm-fade-in-dropped`,
`route-repeat-dropped`, `tint-gradient-dropped`…—, a `text` that says what
is lost, and where, as precisely as whoever lost it knows:

- **a map's page**: `map`, `event`, `page` (RM2k's numbers), the event's
  cell as `x` and `y`, and the index of the `command` in the page, with
  its `code` and `name`; `page` is null when a whole event is lost;
- **a pasted body**: a common event, or another event's page, that a
  `CallEvent` pastes into the page goes in `via`, with the command each
  one was at, under the call's command. A `CallEvent` compiled as a call
  —`OP_CALL`, `OP_CALL_PAGE`— has no `via`: the callee's losses are its
  own, under the common event or the page it is, and the call's own loss,
  if any, is at the call —a callee with no code, `call-skipped`; a chain
  deeper than the console's call stack, `call-stack-exceeded`—;
- **a common event** that runs as a shared body or a parallel one:
  `common` and its `command`, and the file's `commons` says how it runs
  —its trigger and switch— and which pages call it. An automatic one that
  shows pictures is also copied into each map with room for it, as the
  pages of an added event 0 (`common_pages.rs` in rm2k-snes-convert): what
  the copies lose is not listed again, it is the common event's;
- **a troop's page**: `troop` and `page`, and its `command` in RM2k's list;
- **a map**: only `map`, and `events` when it is about some of them;
- **the cartridge**: no place, for its screens and its battle text.

The list is sorted that way —the maps by map, event, page and command,
then the common events, the troops and the cartridge— and `counts` says
how many of each kind there are. The converter prints the total as it
writes it.

## When a cartridge is rebuilt

`rm2k-snes-cartridges` rebuilds a cartridge only when its stamp
—`stamp.txt`, next to the ROM— no longer matches: the cartridge's converter
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
