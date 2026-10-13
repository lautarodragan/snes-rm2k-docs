# The tools split from ABL, into two repos

From taro, on 2026-09-28, on reading the study
[the map of the Python tools](../research/the-map-of-the-python-tools.md)
(Quebracho), which has the six-step plan and the questions with their
options.

- **The plan is the study's six-step plan.**
- **The split happens before the golden game**, which is option b) of
  question 1: the tools repo leaves without ROM tests of its own, and the
  ABL repo runs them until the golden game exists. The study recommended
  waiting for the golden game to make the cut; taro chose not to wait.
- **The game-agnostic side is a single repo**: the RM2k tools, the
  converter and the SNES engine together.
- **The tools repo is in English**, like the Rust projects. When it gets
  translated —before the cut or as each part is rewritten— hasn't been
  decided yet.
- **The engine limits measured on ABL stay fixed** (`ITEMS_N`, `ENC_RATE`,
  `FADE_TOTAL`, the widths…), with a comment saying they were measured
  against A Blurred Line. In a second stage they become parameters, and a
  tool measures them on the game already dumped to JSON. taro's idea is
  that **the estimate doesn't separate from the implementation**: if a
  binary is the one that decides how to split palettes, the measurement
  comes out of that same binary, and not from a separate "measure-game"
  that duplicates the rule. It is "Parse, Don't Validate" applied to
  something more complex.
- **The git history is kept if it is free.** If it costs, it is discussed.
- **How ABL consumes the tools**: first, everything in the same repo with
  two roots (step 5 of the plan). Later, the stable parts as executables on
  the PATH. **Git submodules, never**: taro doesn't like them. Besides,
  today there is no good way to associate one working environment with two
  repos.
- **The engine travels with the tools, at the same version.** taro decided
  it on 2026-09-29. Conceptually it is RM2k's RPG_RT.exe, with one
  difference: it can't be distributed assembled, because it is assembled
  together with each game's `.inc` files, which define constants and flags
  the code depends on. That is why it is distributed as source inside the
  suite's package: as data files of the package and, once the assembling
  tool is in Rust, embedded in that binary, which writes it to the build
  directory before calling `ca65`. taro's idea is that a `pacman -S` is
  enough, with no git and no downloads.
  - **It isn't versioned separately:** the converter and the engine share a
    contract (the format of the `.inc` files and the opcodes of
    `rm2k-snes-bytecode`), so an old engine also needs the converter of its
    time.
  - **The game declares which suite version it is built with**, in its
    project file (the one from step 3), and the tools refuse to build with
    another. That is what ties ABL's goldens to an engine version.
  - **A version manager in the style of nvm or rustup is left for when
    there is more than one game**, and it will install whole suites, not
    loose runtimes.
  - Whatever a game wants to deviate from RM2k still goes through flags,
    which move to the project file.
- **The engine is called the runtime and moves to `runtime/`; `rom/`
  becomes the root of A Blurred Line**, with `data/`, `patches/`,
  `tests/` and `build/`. taro decided it on 2026-09-29: the generic
  runtime is told apart from the project. ABL doesn't need the `.s` files,
  and the runtime doesn't need the graphics or audio `.inc` files. The root
  is left with `rom/`, `tools/`, `docs/` and `workflow/`. **The order:**
  first a `justfile` with the tools' recipes, then step 2 of the plan
  (a single place that knows where everything is), and only then the move,
  in a mechanical commit with the ROMs byte for byte identical.
- **Installing belongs to the tools; verifying belongs to ABL.** Talked
  over with taro on 2026-09-29. `herramientas` and `herramientas-locales`
  go in `justfile`: installing from source requires knowing where
  everything is in `tools/`, which is what ABL can't know. It is a
  project's `make install`, or `npm link`. What ABL needs is **to know it
  has what it needs, at the version it declares**: a recipe of its own, for
  example `verificar-herramientas`, once the project file with the version
  exists. The guard that stops a worktree without its `bin/` is the first
  piece.
- **`rm2k-render` owns everything that is drawing RPG Maker graphics,
  knowing nothing about the SNES.** Talked over with taro on 2026-09-29.
  Today it draws a map's layers and the ChipSets; it will grow with the
  CharSets (poses, translucent events), the battle animations, the enemies
  and battle backgrounds, the FaceSets, the System and the `ShowPicture`
  sign, which today the converter draws in Python. They share a base
  —loading an RM2k image with its color key, alpha blending, cutting
  sheets— that is already in its `picture.rs`. It isn't split into one
  project per asset: that would need another crate for the base, and it
  would be several small ones where one is enough. Its limit is the layer:
  no 16-color palettes or 8x8 tiles, which belong to Adeleine and to
  `voodoo`.
- **The allocator is called Adeleine.** From taro, on 2026-09-29, while
  discussing whether it made sense to separate it from Voodoo (it does: it
  is the rule in `AGENTS.md` that Voodoo doesn't decide colors). It is a
  crate of its own, `snes/adeleine/`, next to Voodoo and not inside
  it, since 2026-09-29; the converter calls it through
  `tools/port/adeleine.py` and leaves what it decided in
  `rom/build/<cartridge>/adeleine/`.
- **ABL only knows executables on the PATH, not `tools/`.** It is taro's
  idea for the first step: the `justfile` doesn't know Python exists, and
  the `.py` files that get executed become real executables, with a
  hashbang and `chmod +x`. A simple test with grep makes the test run fail
  if anything on ABL's side names the `tools/` path.
- **The engine's comments that name ABL stay for now**, out of caution.
  What is emitted into the `.inc` and the `help=` strings aren't touched
  yet either.

What was left open:

- **`cartridges.py`** (question 6): taro doesn't see a clear responsibility
  in that file. It mixes ABL data, which could go in a `.toml`, with the
  cache key and test things. They think it shouldn't exist: it would be
  replaced by a couple of `justfile` recipes, the data in a `.toml`, and a
  cache key that doesn't depend on a binary's hash but on its version (for
  example, each binary printing it, or storing `gunter --version`). Along
  the same line, `tiles_bin.py` and `comprimir.py` look like wrappers of
  `voodoo` and `lz2` without much point. Still to decide is whether it
  moves up to the root and is taken apart later, or the other way around.
- **`decisiones/` and `divergencias/`** (question 8): some belong to ABL
  and others don't. They have to be reviewed one by one.
