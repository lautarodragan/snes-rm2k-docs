# A full inspection of the repository

**Date:** 2026-09-28  
**Tree evaluated:** `e06740a` (snes-rm2k, where A Blurred Line still lived)
plus this inspection  
**Scope:** architecture, sources, data, build process, tests,
documentation, maintainability, dependencies, operation and risks. It is a
snapshot: the numbers in this document describe that tree and must not be
updated.

## Executive verdict

The repository is **technically solid and exceptionally aware of its own
failure modes**. The architecture is explained, the hard decisions have an
owner, the state of the work isn't mixed with the stable documentation, and
the tests exercise both internal state and the visual result. In
particular, the single source of opcodes, the per-cartridge build, the
deliberate goldens, the comparison between cores and the memory checks are
specific defenses against errors that already happened, not a generic layer
put there out of habit.

I wouldn't yet rate it as a project easy to reproduce outside its usual
environment, nor as a simple base to bring in collaborators. The biggest
risks are operational and of concentration:

1. **There is no declarative install of the Python environment nor a
   preflight check.** On a machine with Python and pytest, collection fails
   only when importing Pillow; `just` isn't necessarily available either.
   The README lists families of tools, but doesn't pin or verify the
   installable set.
2. **The full test suite doesn't run in CI in this tree.** There is no
   versioned CI configuration. Quality depends on the development
   environment keeping tools, external assets, patched cores and
   operational knowledge.
3. **The converter is too concentrated.** `tools/port/snes_convert.py` has
   9,322 lines and `tools/port/eventos.py`, 5,515; the backlog itself
   already acknowledges both the mixed responsibilities and the colliding
   globals.
4. **Full validation was blocked in this inspection by the environment,
   not by an observed failure of the product.** Syntax and the Rust
   projects could be checked, but the ROM could not be built or run.
5. **There is no visible license or distribution policy.** This doesn't
   affect operation, but it does make reuse of the code ambiguous and
   requires a separate review of the status of data, patches and captures
   derived from the game.

The recommendation is **not to rewrite the architecture**. It is best to
keep the current defenses and tackle reproducibility first, then split the
converter along boundaries already identified, and only then widen scope or
optimize.

## How it was inspected

The following were read: `README.md`, `AGENTS.md`, `DITTO.md`, the READMEs
of `workflow/`, `docs/`, `tools/`, `data/` and `pruebas/`, the `justfile`,
`pruebas/UNTESTED.md`, the Rust manifests, the state of tasks, decisions
and divergences, and the recent history. The inventory of files and sizes
was walked, and explicit debt markers were searched for.

Commands of the snapshot:

```sh
git status --short --branch
git log -12 --format='%h %ad %s' --date=short
git ls-files
git ls-files '*.py' '*.rs' '*.s' | xargs wc -l
find workflow/tasks/doing workflow/tasks/testing -maxdepth 2 -type f -print
find workflow/tasks/todo workflow/tasks/wishlist workflow/divergencias \
    -maxdepth 1 -type f -print
python3 -m compileall -q tools pruebas
python3 -m pytest pruebas --collect-only -q
git diff --check
cargo fmt --all -- --check
```

For each of `tools/protocol`, `tools/gunter`, `tools/ditto`,
`tools/voodoo` and `tools/lz2` the following was also run:

```sh
cargo test --locked
```

`just pruebas` was not called: the `just` executable wasn't installed, and
direct pytest collection stopped earlier on `ModuleNotFoundError: PIL`.
Neither were `ca65`, `ld65` nor a libretro core visible in the places
checked. That is why this evaluation doesn't claim that the observed tree's
ROM builds nor that the suite is green.

## Architecture and boundaries

### What is best solved

- **The pipeline has recognizable layers.** RPG Maker is transformed only
  once into readable data; rendering, audio, conversion, assembly and
  emulation have their own folders. The projects that don't know the game
  are isolated as Rust tools.
- **The JSON files are an auditable build source.** The resolved dump
  keeps every consumer from reimplementing the format's defaults, while
  the exact view keeps the way back byte for byte.
- **Hardware decisions are localized.** LoROM, mode 3, data bank, blocks
  that must not cross banks, VRAM, CGRAM and WRAM don't appear as
  disconnected magic constants: there is documentation and associated
  validation.
- **The two-sided generation of the protocol eliminates drift.** The TOML
  declaration produces constants for Python and assembly and, for events,
  the jump table. It is a small, verifiable boundary between two
  languages.
- **The split assembly keeps the physical order.** Having `main.s` include
  the subsystems keeps a textual reorganization from turning into an
  accidental ROM move.

### Concentration and coupling

The main structural debt is in `tools/port/`. Its README declares three
import cycles and that the owner of several responsibilities hasn't been
decided yet. The measured size confirms the cost: the converter
concentrates 9,322 lines and the event compiler 5,515. It isn't just an
aesthetic matter: one change can affect graphics allocation,
serialization, audio, events and memory layout from the same module.

The backlog already contains the tasks
[`las-responsabilidades-de-snes-convert`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/las-responsabilidades-de-snes-convert.md) and
[`las-variables-globales-chocan`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/las-variables-globales-chocan.md). They are the right direction. The split
should be done in two commits per stage: first a mechanical extraction with
an identical ROM, then changes of interfaces or criteria. The boundaries
with the best likely return are:

1. an immutable model of the input and the cartridge options;
2. resource planning (banks, VRAM, CGRAM, audio);
3. emission of tables and assets;
4. build report/diagnostics.

It isn't advisable to start with an abstract hierarchy or by moving loose
helpers: that would spread the file around without removing the cycles or
the globals.

### Data and size of the tree

In the snapshot there were 120,182 lines among Python, Rust and assembly:
56,464, 20,808 and 42,910 respectively. The largest versioned file was
`data/db/troops.json` (9.1 MB) and `data/` took 31 MB. This is consistent
with the decision to version a readable representation of the game, but it
has two consequences:

- reviews need to tell apart source changes, derived changes and
  deliberate snapshot changes;
- any future automation must avoid mass-regenerating `data/`, patches or
  goldens as a side effect.

The current policy already does this well: each family has an explicit
command and the diff is the artifact to review.

## Tests and quality

### Coverage design

The strategy is a central strength. There are complementary nets:

- state tests over WRAM, VRAM, SRAM, ARAM and registers;
- visual tests against frozen goldens;
- comparisons against drawings produced by tools;
- properties and round trips of converters;
- snes9x against bsnes to discover dependence on uninitialized memory;
- a long playthrough and alternative playthroughs of the game;
- unit tests of the Rust tools.

`pruebas/README.md` also works as an index required by a test: it keeps
the coverage documentation from silently drifting from the files.
`pruebas/UNTESTED.md` is short and concrete: it lists real paths, why they
aren't covered and which case would allow covering them.

The discipline of not updating goldens automatically and of comparing at
15 bits is correct. It reduces both false positives from representation and
the risk of accepting a visual change just because both sides of an
implementation shared the same error.

### Result of this inspection

- `python3 -m compileall -q tools pruebas` finished fine.
- `git diff --check` finished fine.
- The five Rust projects finished their tests with `cargo test --locked`.
- The five Rust projects have differences against this environment's
  `rustfmt`; the format check isn't clean today, nor is it a gate of the
  repo. It may be version drift of the formatter, so no sources were
  reformatted as part of this documentary evaluation.
- `python3 -m pytest pruebas --collect-only -q` didn't get to collect:
  Pillow was missing.
- The build and execution of the ROM couldn't be evaluated in this
  environment.

This is enough to state that no syntax errors were found and that the Rust
tools are healthy under their locked toolchain. **It is not enough to
state effective coverage or health of the whole product.**

### Gaps and risks

1. The comparison between cores is probabilistic by design: it is worth
   repeating it several times in a periodic run, without turning the whole
   fast suite into a slow test.
2. Goldens protect against regression, not against an initially wrong
   implementation. Manual play of the tasks in `testing/` is still a
   necessary stage, not a ceremonial one.
3. The final audio still requires a human ear; the tests cover structure,
   DSP writes, peaks and voice assignment, but not perception.
4. `UNTESTED.md` records uncovered paths. Each one should become a task
   when the necessary content goes into a cartridge, not before.
5. There is no automatic gate external to the maintainer's environment. A
   commit can end up shared without another system confirming the suite.

## Detailed inspection of the current tests

### Inventory and shape

A walk over the AST of `pruebas/**/test_*.py` found, in this snapshot, 113
files and 569 functions whose name starts with `test_`; 86 functions are
parametrized and there are 1,418 syntactic `assert`s. These numbers don't
measure quality or the number of effective cases —a parametrization
produces several cases and a helper can do a check without `assert`—, but
they help understand the shape of the set. They were obtained with:

```sh
python3 - <<'PY'
import ast, pathlib
archivos = list(pathlib.Path("pruebas").rglob("test_*.py"))
arboles = [ast.parse(p.read_text()) for p in archivos]
tests = [n for a in arboles for n in ast.walk(a)
         if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
print(len(archivos), len(tests),
      sum(isinstance(n, ast.Assert) for a in arboles for n in ast.walk(a)))
PY
```

The distribution is reasonable: `rpgmaker/` tests the engine's semantics,
`abl/` tests playthroughs and content, `herramientas/` tests the pipeline
without emulating, and `arnes/` concentrates the interaction. There is no
proliferation of mocks: most checks go through real data, a real ROM or
real formats. It is a good choice for a port whose main risk is at the
boundaries.

### Concrete defects and blind spots

#### A new playthrough capture may compare nothing

`Recorrido.foto` saves the capture and calls `_contra_golden`, but if the
corresponding golden doesn't exist, `_contra_golden` returns without
failing. There is a defense against numbering shifts —it fails if it finds
the same name with another number—, but there is no manifest that tells
"capture pending blessing" apart from "golden deleted or never added". In
both cases the test stays green.

This was an explicit decision to allow adding milestones before blessing
their images, not an accident. Even so, it is the most important blind
spot of the harness: a playthrough test can appear to have visual coverage
and be looking only at its state. The fix is not to force regenerating
goldens, but to make the state explicit:

- a versioned list of pending captures, allowed only in tasks in
  `testing/`; or
- a `--permitir-goldens-faltantes` (allow missing goldens) option for the
  creation flow, with the normal suite failing if any is missing.

A reverse check for orphan goldens is also needed. The current index
checks `test_*.py` files against the README, but not cases against tests
nor goldens against consumed names.

#### Two tests skip depending on the artifacts present

The only direct `pytest.skip` calls found are in `test_fork_mapas.py`: one
if there are no forked maps and another if a generated PNG doesn't exist.
The second is inside the loop over chipsets; the first missing file skips
the whole function, even if there were other artifacts that could have been
checked. In the expected environment they are probably all there, but the
result "green with skips" doesn't prove the same as "fully green".

It is worth separating the two intentions:

- if the artifact is a requirement of the normal recipe, its absence must
  fail with the command that produces it;
- if the test is truly optional, it must carry a stable marker and the
  official suite must fail on unexpected skips or publish their count
  visibly.

It isn't advisable to replace those skips with `xfail`: the absence isn't a
known defect of the product; it changes what got checked.

#### The comparison between cores has probabilistic detection

The snes9x-against-bsnes test is well designed for uninitialized memory,
but a single run doesn't guarantee finding it: the file itself documents
that the garbage has to land on a harmful value. The set picks high-value
cases —movement, messages, transitions, scenes and battles—, although
there is no repetition or seed recorded as part of the test's interface.

The fast suite can keep a single pass. A periodic job should repeat this
subset, record how many runs it did, and keep the first seed or state that
diverged. "It repeated N times" must come from the command or the report,
not stay as a permanent number in living documentation.

#### The drawing tests share part of the oracle with the producer

Several `*_dibujo.py` tests compute the expected image with modules from
`tools/port/` (`titulo`, `pantallas`, `escena`, `batalla`). This is useful:
it compares the 65816 execution against a Python implementation and
localizes differences better than a golden. But it isn't an independent
reference when that same module also decides or prepares the data that
goes into the ROM. A shared wrong rule can give green on both sides.

The repository already mitigates this with goldens and manual play. The
recommendation is not to duplicate the whole renderer, which would recreate
the problem of two implementations that have to be moved together. Each
drawing test should declare which of these things is its oracle:

1. **format/hardware:** a small expected value written by hand or derived
   from a specification;
2. **game data:** an expected value computed from the LDB/LMU but without
   calling the production function under test;
3. **consistency between implementations:** Python model against ROM,
   always complemented by a golden or an initial manual observation.

`test_batalla_escena_dibujo.py` is a good partial example: it rewrites the
drawing order instead of asking `escena.orden_de_dibujo`, and explains why.
That criterion should be applied only to the rules under test, without
reflexively copying stable decoding helpers.

### Architectural flaws of the harness

#### The tests aren't packages and there was already a real collision

`pytest.ini` inserts `pruebas/arnes` and `tools` into `sys.path`, while the
test directories have no `__init__.py`. `conftest.py` documents a failure
that already happened: two conftests were loaded with the same name and one
shadowed the other. Also, several tests import helpers directly from other
`test_*` modules, for example troop events from `test_tropa` and
`test_victoria`, and the playthroughs chain constants and functions across
test files.

This creates invisible dependencies between collection units: renaming a
test, selecting only one folder or introducing two equal names can break
imports without the tested behavior having changed. The fix is to move
**only the truly shared helpers** into `arnes/` modules by domain
(`batalla`, `menu`, `recorrido`, MSU) and to import those modules with an
unambiguous name. Turning each test into a class or creating a helper for
every three-line function would be unnecessary abstraction.

#### `Partida` concentrates too many domains

`pruebas/arnes/consola.py` has 1,127 lines and `Partida` knows about boot,
title screen, slots, SRAM, clock, input, actors, inventory, maps, audio,
pages and performance measurements. This concentration makes writing a
test comfortable, but also turns the harness into a second monolithic API
of the game: a change of representation can force touching tests of
unrelated domains.

There is no need to hide `Partida` behind generic interfaces. It is worth
extracting stateless readers and narrow facades that already show up as
natural groups:

- `EstadoPartida`: switches, variables, actors, inventory and map;
- `AudioROM`: sample directories, themes, streams and expected writes;
- `Guardado`: SRAM, signature and slots;
- leaving in `Partida` the clock, console, input and high-level navigation.

Those facades must share `Consola` and `Simbolos`, not create consoles of
their own. The goal is to reduce reasons for change, not to add layers at
run time.

#### There are three clocks, but waiting has no common interface

The tests correctly tell apart game ticks, hardware frames and battle
turns. However, many files reimplement `for range(limit)` loops, a
condition check, one frame of advance and an `AssertionError`. The limits
get large in the playthroughs, and the final message depends on each copy.
There are good helpers (`Recorrido.esperar`, `Pelea.esperar`), but they
don't reach hardware and transition tests.

The missing abstraction is not a `wait_until` that hides the clock. It
should be two explicit primitives:

```python
esperar_ticks(partida, condicion, tope, descripcion)
esperar_cuadros(consola, condicion, tope, descripcion, antes_de_cada=None)
```

The battle can wrap the second to add its mode. That way each call says
what time it consumes, keeps specific messages and keeps a test from
mistakenly using `Partida.correr` when the tick is frozen. The
playthroughs, given their complexity and autofire, should keep their
specialized helper.

#### An executable classification by cost and requirements is missing

The recipes split by domain (`rpgmaker`, `abl`, `herramientas`), but pytest
hardly uses markers to distinguish fast tests, ROM, two cores, audio,
external assets or the long playthrough. Even `pruebas-herramientas`
depends on `cartuchos` because one bank test reads a build. This makes the
feedback unit larger than necessary and makes it hard to express a public
CI without assets.

It is worth adding a few capability markers, not an extensive taxonomy:

- `rom`: needs a built cartridge and a core;
- `dos_cores`: needs snes9x and patched bsnes;
- `corpus`: needs the game/RTP;
- `lenta`: useful for local selection, never as a synonym of optional.

The markers must be verified: a test that opens a ROM or queries
`GAME_DIR` without declaring it should fail an architecture check. Then
there can be a hermetic tools suite that doesn't build cartridges and an
integral one that excludes nothing.

### Duplication: which to remove and which to keep

The AST analysis found only one exactly duplicated helper body:
`_msu_del_cartucho` in `test_msu_efectos.py` and `test_msu_datos.py`. This
indicates there is no mass literal copying. The repeated names (`entrar`,
`palabra`, `esperar`) generally represent different domains or receivers
and don't justify an abstraction by themselves.

There is conceptual duplication in three places:

1. **Entering and handling a battle.** Several tests implement "run frames
   until it opens", besides `Pelea.abrir` and the helpers in
   `arnes/batalla.py`. It is worth offering an entry that accepts whether
   it starts by talking, by page or by encounter, and keeping each case's
   specific setup outside.
2. **Reading bytes and words.** There are versions in `Partida`, `Pelea`
   and loose tests. The difference between bus address, WRAM offset and
   symbol is important; they should be unified by type of address, not in
   one function that guesses what it received.
3. **Menu screens.** Items, equipment, shop and End Game repeat "enter,
   move cursor, compare". `arnes/menu.py` is already the right place for
   the common moves; the expected image and the domain assertions should
   stay in each test.

It isn't advisable to deduplicate narrative playthroughs just because they
repeat the road to a map. Their shared helpers (`de_stash_a_ag7`, branch
constants) are useful for run time, but they make a change to the prologue
able to alter many tests. Each playthrough helper should end in a checked
state and document which preconditions it leaves; if it only saves lines
and doesn't establish a contract, it is better to repeat the relevant
steps.

### Unnecessary or risky abstractions

No class hierarchies, generic factories or complex mocks to spare were
found. The risk of over-abstraction lies ahead:

- don't create a single DSL for events, menus, battle and playthrough;
  their clocks and termination conditions are different;
- don't encapsulate memory addresses to the point of making it invisible
  whether ROM, WRAM or ARAM is read: that difference is part of what is
  tested;
- don't parametrize narrative tests just to reduce functions if that makes
  it opaque which branch failed;
- don't move expected constants into production code: a single definition
  is desirable for the protocol, but wrong for an independent oracle.

The most questionable abstraction today isn't in pytest but in reusing
tests as an API: `video.py` discovers functions of
`test_recorrido_golden.py` and runs them with `python -O` to strip their
asserts. It is explained and avoids duplicating plays, but it couples a
delivery tool to test names and to the global effect of `-O`. In the
medium term, the plays should be functions without asserts in a scenarios
module; the tests call and verify them, and the video calls and records
them. That keeps a single playthrough without turning the test file into a
public library.

### What is especially good and must not be "cleaned up"

- A new console per test avoids contamination and makes xdist safe.
- `Cartucho` rejects stale builds instead of producing irrelevant results.
- The symbols come from the assembler: there are no RAM addresses copied
  by hand.
- The autouse test for identical captures detects cases that seem to
  advance and exercise nothing; its exceptions are justified one by one.
- The tests that depend on game data first pin their preconditions (troop,
  members, pages, actions), so a change in the corpus fails close to the
  cause.
- The separation between exact comparison in the suite and tolerance in
  the playthrough reflects different determinism; unifying their
  thresholds would lose information.
- The cases that read WRAM and the ones that look at pixels are
  deliberate and valuable redundancy, not accidental duplication.

### Recommended order to improve the suite

1. Make every playthrough capture have a golden or an explicit, temporary
   exception; also check for orphan goldens.
2. Turn skips due to missing artifacts into diagnostic failures or verified
   markers, and make the official suite's skips visible.
3. Move helpers imported from `test_*` into `arnes/`, starting with battle
   and the shared playthroughs; don't move helpers used by a single file.
4. Add explicit waits by ticks and by frames, and migrate only the loops
   that repeat exactly that protocol.
5. Split audio and save readers out of `Partida`, without changing the
   tests' API in the same mechanical commit.
6. Add minimal markers and a truly hermetic suite without a ROM.
7. Extract the plays `video.py` uses into reusable scenarios.
8. Add a repeated two-core job and, later, focused mutation testing on
   event compilation, page conditions and battle arithmetic.

I wouldn't prioritize a line coverage metric for the assembly: it would
say little about hardware paths. Selective mutation testing or
instrumentation of executed opcodes would better answer which branches are
never exercised.

## Reproducibility and operation

### Current state

There are good foundations: the five Rust projects have a `Cargo.lock`,
the tools are consumed from `PATH`, the build rejects misplaced generated
files, the cartridges declare their content in one place, and the cache
includes the fingerprint of the producers.

The gap is in preparing a new machine. There is no `pyproject.toml`,
requirements file or lock of the Python environment; there is also no
diagnostic recipe that lists, without building, what is missing. The
README mentions Python, a core, cc65 and the repo's tools, but the suite
also needs modules like Pillow and pytest-xdist, plus audio utilities for
certain paths.

### Priority recommendation

Add a **versioned preflight** and call it before the expensive work. It
should:

- check a compatible Python version and importable modules;
- check `ca65`, `ld65`, installed Rust tools and required cores;
- check `ABL_GAME_DIR` and `ABL_RTP_DIR` only for the recipes that use
  them;
- explain the install command or the missing variable;
- not hardcode paths specific to one environment;
- be runnable on its own, for example as `just diagnostico`.

Then, declare the Python dependencies with deliberate versions or ranges.
A reproducible lock is preferable, but even a minimal manifest would be a
substantial improvement. The decision that the game's scripts don't invoke
Cargo during a suite run must be kept.

## Documentation and process

The documentation is above the usual:

- it separates state, current decisions, divergences, dated studies and
  docs that must reflect the present;
- it explains where each truth lives and avoids duplicating changing
  metrics;
- recent commits are small, descriptive and link tasks;
- the `todo` → `doing` → `testing` → `done` flow explicitly acknowledges
  manual validation;
- the mechanical `git blame` and the split of `main.s` have reproducible
  instructions.

The cost is a high barrier to entry: `AGENTS.md` contains a lot of
essential operational knowledge and several rules born from incidents. I
don't recommend summarizing it at the cost of precision. It is worth having
a preflight and the commands encode everything verifiable; the document
should keep only decisions and traps a tool can't express.

In the snapshot there were tasks in the four active phases and a broad
backlog. That shows continuity, but it also makes it important to keep the
current rule: a task taken is marked before touching code, and finished
tasks that require play aren't presented as fully validated.

## Security, provenance and distribution

No hidden downloads or network execution were found in the inspected path;
the Rust dependencies are locked and the external assets aren't stored
next to the original game. Even so, this point wasn't a security audit of
the content or of each dependency.

Risks to resolve before publishing or accepting broad contributions:

- **License:** there is no `LICENSE`/`COPYING`; by default, third parties
  have no clear grant to reuse the code.
- **Provenance:** `data/`, `parches/` and the goldens may contain derived
  material. An explicit policy is needed saying what can be distributed,
  not only that the original game and RTP are outside the repo.
- **Supply chain:** cc65 and the cores are external executable pieces. The
  environment documents how they were obtained, but for strong
  reproducibility it would be worth pinning revisions and publishing
  verifiable fingerprints or a controlled build recipe.
- **CI with secrets/assets:** a future CI shouldn't upload the private
  corpus nor snapshots produced on failures as public artifacts by
  default.

## Proposed priorities

### P0 — make a new machine verifiable

1. Create the preflight and run it at the start of the relevant recipes.
2. Declare the Python dependencies.
3. Document precisely the installation of the runner (`just`) and of the
   cores.
4. Run from a clean environment: build, full suite, core repetition and
   `SIN_CACHE=1`, keeping the commands and results.

### P1 — lower the blast radius

1. Resolve `snes_convert`'s responsibilities with mechanical extractions
   verified by ROM identity.
2. Remove or encapsulate the colliding globals before parallelizing the
   converter further.
3. Introduce explicit data boundaries between planning and emission.
4. Keep every change of criteria separate from the mechanical move.

### P1 — external automation

1. A public or private CI for `compileall`, `git diff --check` and the
   five Rust projects, which don't require the game. That CI should pin
   the `rustfmt` version before applying its format.
2. A private CI or reproducible local job to build cartridges and run the
   suite with the necessary assets.
3. A periodic job that repeats the core comparison and reports
   instability.

### P2 — governance

1. Choose a license for our own code.
2. Document which derived artifacts can be redistributed.
3. Define a policy for updating dependencies and pinned cores.
4. Turn the gaps in `UNTESTED.md` into tasks only when they are
   executable.

## Conclusion

The project doesn't need more layers of process: it already has a coherent
working system and deep defenses. Its main problem is that a good part of
that quality can only be demonstrated inside an accumulated environment.
The investment with the highest return is turning that implicit
environment into diagnosable, reproducible requirements. With that done,
the next leap is reducing the converter's blast radius without altering
bytes. The rest —more content, optimizations and additional coverage— will
benefit directly from those two improvements.
