# RPG Maker 2000 PLUS

## What

**The runtime and the tools are an "RPG Maker 2000 PLUS"**: they run RM2k
games as they are —backwards compatible— and add features RM2k doesn't
have. Those features go **into the central project**, available to any
game, and not as changes of each game's own.

## Why

From taro, on 2026-10-02: "any new feature should be added to the central
project, once we finish separating it from ABL. The idea isn't that each
game can introduce custom changes —though that wouldn't be bad, it's not
what I had in mind—, but to have a sort of RPG Maker 2000 PLUS, that is
backwards-compatible but adds features —something like 2003—, and that any
game can benefit from".

## How it applies

- **A feature RM2k doesn't have belongs to the engine**, even if ABL asks
  for it: the speed-up with L and R (which `--no-speed-keys` turns off), the
  custom menu from the wishlist, a font for high resolution. A game turns it
  on or off from its `rm2k-snes.toml`; it doesn't write it.
- **What belongs to a game** stays in its project: its patches, its test
  cases, its goldens, which maps it carries.
- **Adding a feature is adding opcodes** to the event bytecode, not
  declaring a new bytecode: the bytecode is this runtime's format, not
  RM2k's.
- See [the-tools-split-from-abl](the-tools-split-from-abl.md)
  and [the-game-is-playable-without-msu-1](the-game-is-playable-without-msu-1.md).
