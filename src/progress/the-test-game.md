# The test game

> **A progress page, kept up to date.** Born on 2026-10-15 with the test
> game's skeleton (Calandria), when phase 2 of
> [the research](../research/2026-10-02-the-test-game.md) started. Whoever
> moves a test into the test game, or adds to it what a test needs, updates
> **Where it stands**. The task is
> [`the-test-game-its-skeleton`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-test-game-its-skeleton.md).

The engine's ROM tests —the ones that build a cartridge, run it in an
emulator and compare what it draws— live in A Blurred Line's suite, because
until now there was no other game to run them on: most of them test what
RPG Maker 2000 does, using that game as a stage. That ties the tools to a
game that is not ours to publish, and a tool change is only verified by
running another repository's suite. The test game is a game of our own,
in the-advocate, with free assets, for those tests to come back to.

It is here, under progress and not under internals, because what matters
about it is how far it has got: it grows a test at a time, and each one
that moves out of A Blurred Line changes this page.

## Where it stands

**The skeleton**, 2026-10-15: one map, the hero and one NPC, and one test.

* **The game** is `test-game/` in the-advocate: a Ditto exact dump written
  by hand —liblcf's names, enums by name, defaults left out— and each map's
  tile layers as a **sketch**, a grid of characters with a legend of the
  tiles each one stands for. `rm2k-sketch`, a new tool in `rm2k/`, makes a
  sketch into the dump's `.tiles`; `ditto pack` makes the RM2k files, which
  open in the editor; and the cartridge is built from them like a port's,
  with the installed tools.
* **The assets** are EasyRPG's RTP, unchanged: the Exterior ChipSet (Jason
  Perry, CC0), the People1 CharSet (VictorSena, CC BY 4.0) and the System
  (andwhyisit, CC BY 4.0). Its `AUTHORS.md` carries each one's line, and a
  test of the tools fails if a picture has none. The System is the RTP's
  because nothing can be drawn in a window without one, and the console's
  limits on it are the converter's to meet: it merges what does not fit and
  says so in the build.
* **The cartridge** is built with no RTP —an empty `--rtp-dir`— and without
  a title screen, and the SoundFont comes in `SOUNDFONT` like for the audio
  tests: once the game has music, its samples go into the cartridge, so it
  has to be a free one.
* **The test**, `test_meadow.py`: the cartridge boots on the meadow, the
  hero walks up to the elder, A starts his page and his message is
  composed; two goldens, the map and the message, in snes9x and in bsnes.
  The harness is a small one of its own and the core driver a copy of A
  Blurred Line's.
* **What moved out of A Blurred Line**: nothing yet.

Of the seven assumptions about A Blurred Line the research found in the
tools when it first wrote a game from scratch, four are gone —a debug map
the project had to carry, a single-map game not building, a fallback
backdrop that had to exist, a System with too many colours for the
window—; one is still there —the cartridge has to be called `release`—,
and two were not measured again, because the way the game is built does
not reach them. The task says which.

## What is next

In the order the research gives, each a task of its own:

1. **The harness**: the generic part of A Blurred Line's —the console and
   the clock, the drawing comparisons, the cartridges, the menus and
   screens, the models— as one Python package in the-advocate, imported by
   both games; then the copy of the core driver goes. What stays with A
   Blurred Line is its walkthrough and its places.
2. **The cases**: the test game's own `cases/`, and the tests of
   `tests/rpgmaker/` in A Blurred Line moving over one by one, each with
   goldens born anew —and looked at once, since a new golden defends
   whatever the ROM drew that day—.
3. **What the moved tests need**, as they need it: more maps, a title,
   battles —with backdrops and enemies made for it—, music from
   public-domain scores.
