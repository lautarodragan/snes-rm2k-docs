# RAM is placed by the linker

## What

**A new variable of the runtime gets no address written by hand, and is
declared in the file of the subsystem that owns it**, with a `.res` in the
segment of its RAM:

```
.pushseg
.segment "FARBSS"        ; or "BSS", or "ZEROPAGE"
my_state: .res 2
.popseg
```

and `ld65` places it. For bank 0 —`ZEROPAGE` and `BSS`— that was already
how addresses were given; what is new is that the declaration leaves the
three global files of `runtime/` in the-advocate (`zero_page.s`,
`low_ram.s`, `far_ram.s`) for the subsystem's own. For far RAM, which
until then was a map of addresses written by hand, it is a new segment,
`FARBSS`, in an area of the `.cfg` that `rm2k-snes-assemble` writes
(`FAR_POOL_START` in `rm2k-snes/cartridge/src/banks.rs`).

What was already declared stays where it is. Decided on 2026-10-11, in
the task
[`global-variables-collide`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/global-variables-collide.md).

## Why

Two different collisions, and the second one was the dangerous one:

* **Two branches that each add a variable collided at the end of the same
  file**, even when they worked on subsystems that never touch: the split
  of `main.s` spread the code by subsystem, but not the memory. A
  declaration in the subsystem's file does not touch any line another
  branch touches.
* **Far RAM addresses were chosen as "the next free one"**, looking at
  each one's copy. Two branches could choose the same address and git saw
  nothing; the merge assembled and ran. It happened more than once —the
  picture on top of the MSU-1 state, which silenced the music; a call
  stack set aside inside the parallel interpreters' list—, and the
  workaround was handing out ranges in advance to every agent. With the
  linker, two variables in `FARBSS` cannot overlap by construction, and
  when the area is full the link fails instead of overwriting.

Leaving padding lines per subsystem, or keeping the files in alphabetical
order, would have spread the textual collisions, and left the far
addresses chosen by hand.

## How it applies

* **`FARBSS` is declared `far`**, so its labels carry bank `$7E`: read
  plainly, they are a long access, right whatever the data bank. Code that
  runs with the data bank at `$7E` takes `.loword(name)`, and so does a
  line of `save_table`, which is a `.word`. A label used **before** its
  declaration, in the order `main.s` includes the files, is taken as
  sixteen bits by `ca65`, and the link fails with a range error: that use
  goes with `f:`. The header of `far_ram.s` says the same.
* **The area is all of `$7E2000-$7E7FFF`**, since 2026-10-16: 24 KB
  between bank 0's low RAM, which the console mirrors below, and
  [the grid](../optimizations/lossless/the-map/the-grid-in-wram.md) in the
  upper half of `$7E`; `$7F` is shared in time by the battle and the loads.
  Until that day most of it was a map of addresses written by hand, with
  holes between its regions and regions sized for any game, and `FARBSS`
  was a stretch of it that grew by taking over its neighbours'; that day
  every region went into the segment, as the
  [measurement](../research/2026-10-15-the-wram-and-sram-map.md) suggested,
  and the switches' table, `SWITCHES`, went into the same area. `just
  space` prints what the whole area has left.
* **A region whose size the game decides is sized by the game**: its name
  and its why stay in `far_ram.s`, which comes before the cartridge's
  `.inc`, and its `.res` goes in `far_ram_game.s`, right after it
  —`ACTORS_N`, `VARIABLES_N`, `EXP_K`…—. That is also what keeps one table
  of a game with many actors from running into the next.
* **Many keep sixteen-bit names**: the code that runs with the data bank
  at `$7E`, or points the WMADD window at them, names them by their
  `.loword`, so the label is lowercase and the name the code uses is a
  constant: `far_battle` and `FAR_BATTLE = .loword(far_battle)`. A block
  walked as a range —what `clear_variables` clears in one pass, each line
  of `save_table`— is one `.res` with offsets, or several in a row with an
  `.assert` that they are adjacent: the linker places them in the order of
  the text, and nothing else promises it. A size the `.res` needs before
  the layout that defines it exists is written as a number, with an
  `.assert` that it is exactly that (`TL_BYTES`).
* **The same holds for what is in `low_ram.s` and `zero_page.s`**: it stays
  where it is.
* **What guards it**: ABL's `tests/tooling/test_wram_reservations.py`,
  in the-advocate-ports, looks in the runtime's source for a far address
  written by hand —a long one in the area, or a sixteen-bit one named
  `FAR_*`—, since in the symbol table a `.loword` of a label and a number
  written by hand look the same; and it checks that every long symbol in
  the area is a label of the segments or falls inside one.
