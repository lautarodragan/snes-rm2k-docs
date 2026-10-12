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
* **The area is small**: far RAM is nearly full. `$7E2000-$7E7FFF` is the
  map written by hand, with only small gaps; the upper half of `$7E` is
  [the grid](la-grilla-vive-en-la-wram.md), and `$7F` is shared in time by
  the battle and the loads. `FARBSS` lives in the unused end of the battle
  scene's reservation. `just espacio` prints what it has left. **It grows
  by taking over a stretch of the map written by hand**, moving whatever
  lived there into the segment: the area is moved in `banks.rs`, and what
  limited it gets an `.assert` against `__FARRAM_START__`, like the scene's
  state.
* **The map written by hand does not move**, because moving it moves the
  ROM and some of it is saved or cleared as a block. The same holds for
  what is already in `low_ram.s` and `zero_page.s`.
* **What guards it**: ABL's `pruebas/herramientas/test_reservas_de_la_wram.py`,
  in the-advocate-ports, fails if a symbol that is not a `FARBSS` label
  lands inside the area, with its bank or without it, which is what an
  address chosen by hand there would be. What it does **not** see is the
  map written by hand overlapping itself: that is guarded only by the
  `.assert`s each range already had.
