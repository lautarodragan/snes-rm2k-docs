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
tools/runtime/*.s + those .inc    --rm2k-snes-assemble----------> <rom>.sfc + <rom>.sfc.sym
                                    (bank packing, ca65 + ld65)
<rom>.sfc + MIDI or replacements  --rm2k-snes-msu---------------> <rom>-N.pcm
                                    (fluidsynth, ffmpeg)
```

The paths on the right belong to the game's project —where its
`rm2k-snes.toml` is, which declares them—, and `<rom>` is its
`[rom] name`. `rm2k-snes-cartridges` runs all of that for each cartridge
the project declares. How A Blurred Line calls it, with which recipes and
which flags: [its pipeline](../ports/abl/pipeline.md).
