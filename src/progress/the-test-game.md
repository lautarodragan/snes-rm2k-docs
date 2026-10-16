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

**The skeleton**, 2026-10-15: one map, the hero and one NPC, and its first
tests.

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
* **The cases**: `test-game/cases/`, one JSON per test page, like a
  port's; the harness chooses one by the case variable before the first
  game frame, the way A Blurred Line's does.
* **What moved out of A Blurred Line**: switches past 1023, on 2026-10-15
  —`test_switches_past_1023.py`: a page conditioned on 1100, a
  `ControlSwitches` and a branch on it, and the page not running before
  its switch is on—. In A Blurred Line it needed a fork of its map 348,
  since that game names no switch past 1008, and the cartridge taro plays
  carried it; here the meadow carries the event, invisible. The task is
  [`switches-past-1023-tested-in-the-test-game`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/switches-past-1023-tested-in-the-test-game.md).
* **What was born here, on 2026-10-15**: the faces of the message window
  —`test_faces.py`, the case `faces`: Actor1's face from the RTP on the
  left, on the right and mirrored, kept over a box with no command, changed,
  and cleared; five goldens—. None of the three games that show faces has a
  page that does all of it, and A Blurred Line shows none. The task is
  [`draw-the-faces`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/draw-the-faces.md).
* **And on 2026-10-16, the first picture**: the lantern, map 5, where a
  parallel event lays `Picture/Night` —a near-black mask with a cone of
  light, ours, drawn by a script— over the map at transparency 35, fixed
  to it, the way Desert Nightmare lights its interiors; the project has
  `[graphics] map_pictures`, so it is drawn into the map, its layer above
  included —`test_map_picture.py`, the case `lantern`: in the dark, and
  under the lantern with the camera scrolled; two goldens—. A Blurred
  Line has the knob off, and Sunset Over Imdahl's maps are paintings, so
  the ChipSet side of the rule runs only here. The task is
  [`pictures-that-go-over-the-map-outside-sunset`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/pictures-that-go-over-the-map-outside-sunset.md).

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
2. **The cases**: the tests of `tests/rpgmaker/` in A Blurred Line
   moving over one by one into the test game's `cases/`, each with
   goldens born anew —and looked at once, since a new golden defends
   whatever the ROM drew that day—.
3. **What the moved tests need**, as they need it: more maps, a title,
   battles —with backdrops and enemies made for it—, music from
   public-domain scores.
