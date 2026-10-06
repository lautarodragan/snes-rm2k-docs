# From a game to a ROM

```text
RPG Maker 2000 project
        │  ditto unpack
        ▼
   JSON dump (maps, database, tree)
        │  the converter asks each stage, in order
        ▼
   wally (maps) · events · battle · screens · images · audio
        │  mapdata writes what they answered
        ▼
   .inc files for the assembler
        │  ca65 + ld65, with the runtime
        ▼
   cartridge (.sfc)
```

1. **Ditto** reads RPG Maker's binary formats and writes them out as JSON:
   one file per map, plus the database and the map tree. Everything after
   this step reads the JSON, never the original files.
2. **The converter** asks each stage what the cartridge needs, and hands
   each one what the others answered. A stage knows one subject: the
   maps, the event pages, the battles, the text screens, the pictures, the
   music.
3. **The emission** writes the answers as assembler include files, next to
   the cartridge being built.
4. **ca65 and ld65**, from the cc65 project, assemble the runtime together
   with those files and pack everything into banks.

Each game is a directory with an `rm2k-snes.toml`, which the tools look for
from where they run upwards, the way cargo finds its `Cargo.toml`. Where
the original game, the RTP and the SoundFont live is passed to them as
flags.
