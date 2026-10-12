# A loop that never waits does not compile

## What

`Loop`, `BreakLoop` and `EndLoop` compile since 2026-10-12, as jumps:
without the Maniac patch RM2k keeps no state for a loop —easyrpg's
`CommandLoop`, `CommandEndLoop` and `CommandBreakLoop`—, so `EndLoop` goes
back to after the first `Loop` at its own indentation, and `BreakLoop` to
after the first `EndLoop` that follows it, whatever its indentation, which
is RPG_RT's bug and easyrpg copies it.

**A `Loop` whose body has nothing that lets a frame go by does not
compile** —a `Wait`, a message, a choice, a number to input, a
`KeyInputProc` that waits for a key, a `MovePicture` that waits for its
move—, and the page it is in is left out like any page with a command the
ROM does not do.

## Why

RPG_RT runs at most ten thousand commands of an interpreter per frame —it
is `loop_limit` in easyrpg's `Game_Interpreter::Update`— and then lets the
frame go by, so a loop that never waits slows the game down
but does not stop it. The ROM's interpreter has no such cap: the same loop
would never return, and the console would hang.

## How it looks today

Only Vampires Dawn has loops among the ported games, and almost all of
them wait: the rain, day and night, the mines, the clock, its menus. The
few that do not are left out, and the ones seen are loops whose every
branch ends in a `BreakLoop`, which never go round: a few custom-menu
common events and one map's page. A loop that waits only on some of its
branches compiles, and hangs if it takes the others forever.

## When it stops being enough

A game with a loop that does its work without waiting —counting through a
variable, walking a list— would need a cap on the interpreter's commands
per frame, like RPG_RT's.

## Measured

`a_loop_that_never_waits_does_not_compile`, with the two others on loops,
in `rm2k-snes/events/src/compile.rs` in the-advocate. No ROM test runs a
loop.
