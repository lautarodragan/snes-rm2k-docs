# Ports

RPG Maker 2000 games taken to the Super Nintendo with the tools. They live
in the the-advocate-ports repository, **one directory per game, and each one
is a whole project**:

- **`rm2k-snes.toml`**: what the game decides —its name and title, which
  maps go in which cartridge, the starting map, the knobs (see [What a game
  can choose](../fitting.md#what-a-game-can-choose))—. The tools find the
  project by looking for this file upwards from where they run, the way
  cargo finds its `Cargo.toml`, so everything is run from the game's
  directory.
- **`justfile`**: the recipes —dump the game, build the cartridges,
  measure the space, list which pages don't compile—. It translates the
  variables that say where the original game, the RTP and the SoundFont
  are (`GAME_DIR`, `RTP_DIR`, `SOUNDFONT`) into the tools' flags
  (`--game-dir`, `--rtp-dir`, `--soundfont`); the tools themselves come
  from the PATH. The game and the RTP can be a directory or a `.zip` of
  one: see [A game or an RTP as a
  `.zip`](../internals/pipeline.md#a-game-or-an-rtp-as-a-zip).
- **`data/`**: the game dumped to JSON with Ditto (`just dump`), which is
  where the port reads the game from (see [From a game to a
  ROM](../pipeline.md)). The original game isn't in the repository: it
  isn't ours to redistribute.
- **`build/`**: what the tools leave, cartridges included. It isn't
  versioned.

The ports:

| directory | game | |
|---|---|---|
| [`abl/`](abl/README.md) | A Blurred Line | the real port: the only one with the test suite and its goldens, MSU-1 and `just deliver` |
| [`book-of-three/`](book-of-three/README.md) | The Book of Three | from the survey |
| [`desert-nightmare/`](desert-nightmare/README.md) | Desert Nightmare | from the survey |
| [`dooms2/`](dooms2/README.md) | Dooms 2 | from the survey |
| [`el-dorado/`](el-dorado/README.md) | El Dorado | from the survey |
| [`frozen-world/`](frozen-world/README.md) | The Frozen World | from the survey |
| [`sunset-over-imdahl/`](sunset-over-imdahl/README.md) | Sunset Over Imdahl | from the survey |
| [`vampires-dawn/`](vampires-dawn/README.md) | Vampires Dawn | from the survey |

## The seven of the survey

Until then the engine had ported a single game. On 2026-10-05 taro left
seven more RPG Maker 2000 games to see how general it had turned out, with
one request: find what they share before fixing anything. The answer is
the study [Other games: the
survey](../research/2026-10-05-other-games.md).

Each of the seven is a project built that day for the survey, **without
MSU-1 and without tests**, with the minimal recipes: `datos` and
`datos-vuelta` (dump the game, and check that Ditto brings it back byte
for byte), `cartuchos`, `espacio` and `culpables` (which commands keep
which pages out). Each has `cases/`, with the empty case for page 0, and
the values the survey had to choose say "relevamiento" (survey) in their
comment in `rm2k-snes.toml`. What the survey sidestepped to get to a
cartridge —a reduced System graphic, BMPs turned into PNGs, maps
excluded, no title screen— is in the study, with the cause of each. Until
2026-10-10 each one was a repository of its own; that day they joined
the-advocate-ports, with their history.

**Their pages here are dated snapshots**: what the survey found on
2026-10-05 and what the tasks that followed it changed up to 2026-10-06.
They say nothing about the state of each port after that date; what is
true today is what their recipes print.

**They have tests since**: `just boot`, at the root of the ports, builds
the seven and plays each one up to its first map, in snes9x and bsnes. Two
of them go further, because taro asked: Sunset's painted maps, against
goldens, and The Book of Three, played from the start to past the forge
(see [its page](book-of-three/README.md)).
