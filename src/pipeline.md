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

## Why a JSON dump, and not the game itself

RPG Maker's binary formats leave a field out when it holds its default
value, so a reader has to know every default to read them right. Early on,
two readers of the same files each had their defaults written by hand, and
both were wrong the same way: an enemy whose hit points default to 10 came
out with 1, died in one blow, and no comparison between the two could
notice, because they agreed.

So the formats are read **once**, by Ditto, with the defaults taken from
the schema of [liblcf](https://github.com/EasyRPG/liblcf) instead of from
anyone's memory, and everything after reads the dump. Ditto writes it in
two views from the same run:

- **the resolved view**, which a game keeps in version control: every
  field written out, defaults applied, so whoever reads it needs to know
  nothing about the format;
- **the exact dump**, with the binary's own shape, which is the one Ditto
  can write back: unpacking a game and packing it again gives the same
  files, byte for byte.
