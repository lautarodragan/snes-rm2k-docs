# How it is tested

Nothing is considered right because it looks right. A test builds a
cartridge, runs it in an emulator, and **compares the screen pixel by
pixel at 15 bits**, which is the console's real color depth, against a
frozen capture (a *golden*).

Three rules come with that:

- **Changing a golden is deliberate.** It goes into version control, it is
  looked at, and the commit says why the picture changed.
- **A golden catches regressions, not birth defects.** A feature that is
  wrong from day one bakes its bug into its golden. What balances that is
  someone actually playing the game.
- **Two emulators, compared to each other.** One of them starts with
  garbage in work RAM and the other with zeros, so a difference between
  them means the ROM reads memory it never wrote.

## The test game

Most of those tests live in A Blurred Line's suite and test what RPG Maker
2000 does, using that game as a stage. They are moving to a game of our
own, in the-advocate, built from text with free assets and run with `just
test-game`; where that stands is [its progress
page](progress/the-test-game.md).

## The other games

A Blurred Line's suite runs only A Blurred Line, so a change to the tools
could break another port without anyone noticing. The root of
the-advocate-ports has a `justfile` of its own for that:

    just boot            # every port but A Blurred Line
    just boot -k sunset  # one of them

For each game it builds the cartridge from its `rm2k-snes.toml` —only if
it is stale— and plays it in snes9x and in bsnes until the player has
control: it presses A every few ticks while an event page runs, which goes
through the title screen, the intro, the messages and any question by its
first option. It fails if the game does not build, if the player never gets
control, if that happens on another map than the one recorded in the test,
if the hero cannot walk, or if the two emulators disagree. Beyond that it
does not look at how the maps are drawn: goldens of seven games would bake
their birth defects in and multiply what has to be reviewed.

The exception is the painted maps of Sunset Over Imdahl, the only game with
any: they are the only path of the engine A Blurred Line never runs, so a
square and a bar have goldens, still and walking with the camera moving.

It is not part of A Blurred Line's suite —one game alone takes a couple of
minutes to build from scratch—: it is run before handing a build over, or
after a large change to the tools.
