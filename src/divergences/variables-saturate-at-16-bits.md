# Variables saturate at sixteen bits

## What

The console keeps RM2k's variables in **sixteen bits, signed**: from
-32,768 to 32,767, against RM2k's ±9,999,999. A `ControlVars` that **sets**
a constant outside that range is compiled as setting the nearest edge:
999999 becomes 32,767. Adding or subtracting a constant outside the range
still does not compile, and its page is left out, because the ROM's sum
wraps around instead of capping.

## Why

The one command that asks for it is common event 45 of A Blurred Line,
`SimClearTweenRooms`, which sets six variables to 999999 as "no cell"; the
rooms of Eisen's simulation call it 47 times. While it did not compile, each
of those calls was skipped ([A skipped call](a-skipped-call.md)) and the
variables stayed at whatever they had.

Those six variables are only compared for equality against an event's or
the hero's cell, and only moved by one after being set from a cell. A cell
never reaches 32,767, so the ceiling says "no cell" the same way 999999
does. Widening every variable to 32 bits would double their RAM and the
cost of every operation for one sentinel.

## How it applies

* What is lost is the exact value: a game that sets 999999 and then shows
  it with `\V[n]`, or compares it against something above 32,767, sees
  something else. No page of A Blurred Line does.
* The gold copied into a variable was already capped at 32,767 —`op_var`,
  in `runtime/interpreter_variables.s` in the-advocate—, for the same
  reason: Sern's forge, which keeps the party's gold in a variable while
  it lends forge points, loses whatever is above that.
* The compiler is `ControlVars` in `compile.rs` of `rm2k-snes/events/` in
  the-advocate; the test is `test_poner_mas_que_la_palabra_satura` in A
  Blurred Line's suite.
