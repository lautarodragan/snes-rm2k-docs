# Events trigger with two bits

## What

**Events trigger with two bits each, not with a queue.** It is the
`waiting_execution` of `Game_Event`: `FLAG_AUTO` says whether the event's
active page is an autorun page that compiled, and `FLAG_WAIT` whether it has
a page waiting its turn —whether the autorun sweep, the action key or a
touch put it there—.

## Why

It replaced a queue of eight pointers that filled up and dropped entries,
and that past the eighth interaction read its own counters as bytecode.

Two things follow that didn't happen before, and that have to be kept in
mind when writing a page: **an autorun page repeats** as long as it is
still the active one, and **one that becomes active with the map already
loaded starts**. The second is what left the second half of CORE and
MANTA's memory scene dead.
