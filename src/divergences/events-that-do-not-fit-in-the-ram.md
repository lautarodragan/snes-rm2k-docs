# Events that do not fit in the RAM

## What

Every event of a map is a row of three tables in bank 0's RAM —its cell,
its flags and its active page—, and there are `EV_MAX` rows
(`rm2k_snes_mapdata::record::EV_MAX` in the-advocate). In several places of
the runtime an event's index is a byte, and the RAM is full: raising the cap
is not an option. In RM2k there is no such cap.

A map with more events than that used to stop the build. Now the converter
decides, before any stage reads the map, which events the console keeps
(`trim.rs` in `rm2k-snes-convert`), in two steps.

**First, the twins share a row, and nothing is lost.** Events whose pages
are the same, field by field, that draw nothing, never move, are not on the
hero's layer and that nobody names, keep only the row of the one with the
lowest id. The others are a cell in a table in ROM, behind the map's
positions, which the runtime looks at when no row is on the cell the hero
steps on or faces (`twin_in_cell` in `runtime/action_key.s`): the cell
fires the first one's page, which is the same page. That is what most of
those maps have too many of: a strip of seventy invisible touch events
along an edge, each a `Teleport` to the same place. What can not be a twin,
because it would be done on the first one and in RM2k it is its own: a
page that is autostart or parallel —it runs once per event—, that erases
its own event, or that names "this event".

**Then, if that is not enough, the rest is left out**, and an event left
out **stops existing** for the cartridge: the map is read without it by the
converter, the event compiler and Wally, so the indices agree; a page that
names it does not compile, as with any event that does not exist. The
converter says which ones, map by map, with what each one loses, in a
WARNING.

## Which ones go

From what loses the least to what loses the most: the ones that do
nothing —no command, nobody names them, they draw nothing and do not
block—; the ones that are only seen; invisible walls on the hero's layer;
the ones that are seen and block; the ones with pages that run; and last
the ones something names (`MoveEvent`, `SetEventLocation`, `FlashSprite`, a
variable that reads their cell, a `CallEvent` of theirs…), whose loss
takes those pages along. Within each class, the highest id first —the
events placed last in the editor—: a rule anyone can redo by reading the
map. A first one of twins that goes takes its twins with it.

## Measured

On 2026-10-10 the cap stopped 38 maps of Vampires Dawn and 11 of Desert
Nightmare, from 121 events to 328. With the rule alone, 22 maps of Vampires
Dawn lost events with pages that run —most of them map exits—. With the
twins no map of either game loses a page: 24 maps of Vampires Dawn fit,
and the other 14 lose decoration only —two events of map 164 also block—;
2 maps of Desert Nightmare fit, and the other 9 lose decoration and, in 8
of them, invisible walls. A Blurred Line has no map over the cap.

## How to reproduce it

`trim.rs` has the rule's tests; `events/tests/command_line.rs` and
`wally/tests/too_many_npcs.rs` check that a stage reads the map without
the events left out. A Blurred Line's suite has `test_gemelos.py`, on a
cartridge that tells the converter the RAM holds 16 events
(`--test-events-max`): the bridge of map 255 keeps two rows for its 61
creaking boards —one of them is named by a common event—, and stepping on
one that has no row still counts.

## When it stops being enough

When what is left out is decoration that matters, or a wall. Both have an
answer that loses nothing and is not done: the walls could go to the map's
passability, and the decoration could be baked into the background, as
`decorative_events` does (see
[Baked decorative events](baked-decorative-events.md)); but the
cut happens before Wally sees the map, so an event left out is not baked
either.
