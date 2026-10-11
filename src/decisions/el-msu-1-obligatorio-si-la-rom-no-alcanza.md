# The MSU-1 is required only when the ROM does not reach

## What

**A game whose ROM does not reach may require the MSU-1**: what does not
fit travels in its `.msu`, and without it the cartridge shows a screen that
says so and does not start. The game asks for it in its project file,
`[rom] msu = "required"`; without the setting it is `"optional"`, which is
what every game is, and the cartridge is byte for byte the one from before
the setting existed.

**The converter does not decide it by itself** when the ROM runs out: a
game that does not fit says so, as always, and someone decides.

**The mechanism is the same for every game**: which data may travel in the
`.msu`, how the packing chooses it and how the ROM reads it are in [the
`.msu` file](../internals/msu-datos.md), "What does not fit in the ROM".
What is particular to a game is only that its ROM does not reach.

## Why

From taro, on 2026-10-11, about Vampires Dawn, which does not fit in the
8 MB even compressing what is reasonable: rather than two cartridges —saves
to migrate, and nothing guarantees splitting it gracefully—, the MSU-1
required **for that game**. And when confirming it: "let's go with the msu,
but let's keep the code of the runtime and the tools as generic as
possible, always aiming at every game having optional msu". A compression
chip, no, while the MSU-1 is optional in general.

The converter does not decide it because **requiring the MSU-1 changes what
the player needs** —a console or an emulator that has it, and the `.msu`
next to the ROM—, and one map more must not change that without anyone
deciding it. Measured against [the game is playable without
MSU-1](el-juego-se-juega-sin-msu-1.md), it is the exception, and an
exception is written down.

## How it applies

- **The goal is still that each game fit without the MSU-1.** A game that
  requires it should go back to `"optional"` the day its ROM reaches.
- **Only what is read when a map or a battle loads may go**, never what is
  read on every frame: in Mednafen each seek costs one or two frames. That
  is why the poses, the biggest thing there is, stay in the ROM.
- **The packing sends the fewest it can**, and the ROM keeps the rest.
- **A Blurred Line does not require it**, and its tests run this path on a
  cartridge built to: `test-msu`, with the converter's `--msu-everything`.
