# A Blurred Line

A port of *A Blurred Line*, a game made in RPG Maker 2000, to the Super
Nintendo. It is the game the project was born porting, and still the one
that is ported for real: the others are measured against it (see
[Ports](../README.md)).

It lives in `abl/` in the-advocate-ports. That directory is **the game**: its
dump into a format that can be looked at (`data/`), what was decided about
it while porting it (`parches/`), which cartridges are built and with which
knobs (`rm2k-snes.toml`), its tests with their goldens (`pruebas/`) and the
test ROMs that were built to decide something (`experimentos/`).

What sets it apart from the other ports:

- **The test suite and its goldens.** `pruebas/` runs the cartridges in
  snes9x and bsnes through libretro and compares the screen, pixel by
  pixel at 15 bits, against frozen captures (see [How it is
  tested](../../testing.md)). Almost all of `pruebas/rpgmaker/` is what RM2k
  does, using ABL as the stage: **until there is a test game, these are the
  only ROM tests of the engine**, and a change in the tools is verified by
  running this suite with the tools of the change.
- **MSU-1.** The release cartridge carries MSU-1 tracks for every theme,
  and an `abl.msu` with the quality battle backdrops and sound effects
  ([the `.msu` file](../../internals/msu-datos.md)). Without MSU-1 the game
  works the same: what comes from the `.msu` only replaces something the
  ROM already has.
- **`just entregar`**, which hands over a build to be played.

What is **not** here:

- **the tools and the runtime** —what converts the game and the engine
  that runs it on the console—, which live in their own repository,
  the-advocate, and are consumed from the PATH. The architecture decisions
  —mode 3 always, the ExHiROM cartridge, the tables in bank 0— are in
  [The cartridge](../../cartridge/README.md), how each part of the port
  works in [Internals](../../internals/README.md), the console in
  [Reference](../../reference/README.md), and where the ROM doesn't do what
  RM2k does in the [divergences](../../divergences/README.md);
- **the history up to 2026-10-02**: ABL's repository was born that day
  from scratch, with the files from the-advocate, and the earlier `git log`
  stayed there. What lived at `rom/X` there is `X` here —and since
  2026-10-10, when ABL moved into `abl/` in the ports, `abl/X` in the
  repository—;
- **where the work stands**: the tasks and the decisions, this game's too,
  live in their own repository, the-advocate-work, since 2026-10-10, to have
  a single board. A `workflow/…` in one of this game's files is the same
  path there, without the prefix. How things got here is told by the
  `git log`.

## The original game

**It is not in the repository**: it is read from the folder `GAME_DIR`
says —which the `justfile` passes to the tools as `--game-dir`—, and from
there come the maps (`.lmu`), the database (`RPG_RT.ldb`), the map tree
(`RPG_RT.lmt`), the pictures, the MIDIs and the WAVs. What the game
doesn't bring is supplied by Don Miguel's RTP, which isn't ours to
redistribute either: see [its RTP](rtp.md).

The game's starting map is 4, an empty room that only teleports. The first
real map is 1.

## The data in a versionable format

```sh
just datos         # the game -> data/ and build/ditto-exacto/, with Ditto
```

`data/` has the same data as the `.lmu` files but in a format git can
really version: you can see what changed, review it and edit it by hand.
And **it is where the port reads the game from**: the converter, its
stages and the tests look at these files and not at the binaries. The one
that writes it is **Ditto**, one of the tools, which also knows how to go
back: `ditto pack` rebuilds the game's files byte for byte from the exact
dump, which the same run leaves in `build/ditto-exacto/` and which isn't
versioned; `just datos-vuelta` checks it on this game. The reason for the
decision is in [data is the resolved
view](../../decisions/data-es-la-vista-resuelta.md), and what is inside,
in `data/README.md`.

## How it is built

**The tools have to be installed**, from their repository —`just -f
tools/justfile install`, in the-advocate—, and with them a libretro core,
`ca65` and `ld65`: what each one needs, in that repository's README.

```sh
just cartuchos     # builds the ROMs: release and the test ones
just pruebas       # the whole suite; builds first whatever is needed
```

The ROM that is played comes out at `build/release/abl.sfc`, with its
`abl.msu` and the MSU-1 tracks next to it. Which ROMs there are and which
test covers what, in `pruebas/README.md`; what else can be run, in the
`justfile`, with its reasons. The road from the game to those files, with
each recipe: [the pipeline](pipeline.md).

## How ABL finds the tools

ABL doesn't know where they live: it knows executables on the PATH, and
nothing in this repository names the path of the other one —
`pruebas/herramientas/test_lado_de_abl.py` makes sure of it—.

- **The executables**, by name: `rm2k-snes-cartridges`, `ditto`,
  `rm2k-snes-patches`… They find this project by looking for
  `rm2k-snes.toml` from where they run, and what belongs to the machine
  reaches them through flags, which the `justfile` sets.
- **The runtime** is built by `rm2k-snes-cartridges` from the checkout of
  the tools it was installed from.
- **What the tools know about the project** —where each folder is, where
  the runtime is, what `rm2k-snes.toml` says— the harness asks
  `rm2k-snes-project`, another executable of the suite: see
  `pruebas/arnes/proyecto.py`. The harness imports nothing from the tools:
  the emulator, `pruebas/arnes/emulator/`, has been its own since
  2026-10-02.

So **to run ABL with other tools** —those of a checkout where someone is
changing them— it is enough to put them first on the PATH: the `justfile`
builds its own from the one it receives. How, in the `AGENTS.md` of
the-advocate-work, which since 2026-10-10 is a single one for all the
repositories: a "see AGENTS.md" in a file of this repository means that
one.

## What is missing

It isn't written here, because here it went stale without anyone noticing:

- what is decided and not started is in `tasks/todo/` in the-advocate-work,
  and what we would like and nobody is doing in `tasks/wishlist/`;
- where the ROM doesn't do what RM2k does, in the
  [divergences](../../divergences/README.md);
- and what no test looks at, in `pruebas/UNTESTED.md`.

## The pages of this port

- [The pipeline](pipeline.md): this game's road to the ROM, **today**.
- [The RTP](rtp.md): the RTP this game uses, and where to get it.
- **Research**, dated studies: "on such a day, with such a commit, we
  measured this".
  - [A full inspection of the
    repository](research/inspeccion-integral-del-repo.md) (2026-09-28)
  - [The maps through the MSU-1: how far the cartridge
    reaches](research/2026-10-01-los-mapas-por-el-msu-1.md) (2026-10-01)
  - [The whole game without MSU-1: the
    count](research/2026-10-01-el-juego-entero-sin-msu-1.md) (2026-10-01)
- **Decisions** about its content and its cartridge, in
  [decisions](decisions/README.md).

The rest —the format of RPG Maker 2000, the console and its emulators, how
each part of the port works— belongs to the tools and is in the rest of
this book. The studies that were written about this game before
2026-10-02 came with it; the ones about the engine, even if they measured
it on ABL, stayed with the tools.

The difference that matters is between the pipeline page and the
research:

- **A page about the port today has to be up to date, or it lies.** That
  is why it is best kept short and pointing at the code instead of
  repeating it. Whoever changes what such a page describes changes it in
  the same commit.
- **A study is a snapshot and is not touched.** At the top it says the
  date and the commit of what it measured, and its numbers are from that
  moment. If something changed, it is measured again and a new study is
  written; the old one stays as it was.

If a task ends in a document instead of code, the document goes to the
research and the task —in the-advocate-work— moves to `tasks/done/` pointing
at it.
