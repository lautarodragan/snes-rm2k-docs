# The test page switches itself off

## What

**The test page switches itself off**, by turning on switch 1023 in its
first command, with a second, empty page that requires it. Its event is the
map's first free index, not a high number.

## Why

It is the idiom with which the game's pages deactivate themselves, and
nothing exercised it. Without it, now that autorun pages repeat, the test
page would restart its own route forever.

As for the index: the ROM's sweeps go from zero to `ev_total`, so a high
number would be left out.
