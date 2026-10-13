# A Blurred Line's pipeline

```text
$GAME_DIR (.lmu .ldb .lmt)    --ditto unpack (just dump)-->  data/ (JSON)
data/ + patches/manual/
+ images, MIDI and WAV            --rm2k-snes-convert-----------> build/<rom>/
  ($GAME_DIR, $RTP_DIR)     (and its stages: wally, events,   mapdata.inc, musicdata.inc,
                                     screens, images, battle,
                                     mapdata, patches, audio)
                                                                  abl.msu (battle backdrops),
                                                                  patches/ (decisions)
the runtime + those .inc          --rm2k-snes-assemble----------> abl.sfc + abl.sfc.sym
                                    (bank packing, ca65 + ld65)
abl.sfc + MIDI or replacements    --rm2k-snes-msu---------------> abl-N.pcm
                                    (fluidsynth, ffmpeg)

just cartridges release  everything, with the MSU-1 tracks, in build/release/
just patches            copies release's decisions to patches/auto/
```

The tools of each arrow and the runtime belong to the tools' repository,
the-advocate, and [Internals](../../internals/README.md) says how each one
works; the same road with generic names is [the
pipeline](../../internals/pipeline.md).
