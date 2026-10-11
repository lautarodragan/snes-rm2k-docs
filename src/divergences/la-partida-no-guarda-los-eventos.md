# The save does not keep the events

## What

RM2k saves, in each slot, the state of every map you visited: where each
event was left, which page it had active. The ROM's save **does not carry
where the events were left**; what it does save is listed by `save_table` in
`runtime/bank1.s` in the-advocate, and nothing more.

On loading, each map puts its events back where the cartridge says, the same
as when entering through a door. Switches do come back, so the active pages
are the right ones: an open door stays open if what opens it is a switch, and
goes back to its place if what moved it was a `MoveEvent`.

There are four slots, not fifteen: see `SRAM_SLOTS`.

## Measured

Saving the positions would be `EV_MAX * 8` bytes per visited map, which is a
different kind of save file.

## How it looks today

It is not seen as long as nobody saves in the middle of a scene that moved
events and did not turn on any switch.
