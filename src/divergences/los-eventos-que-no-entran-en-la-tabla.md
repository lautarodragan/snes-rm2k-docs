# Drawn events that do not fit in the table

## What

The console keeps one row per **drawn event** of the map —every event with a
CharSet or a tile in some page, on screen or not— in a table in bank 0's
RAM, and the table has `NPC_MAX` rows (`wally::sprites::npc::NPC_MAX` in
the-advocate). OAM would take a few more; the RAM is what sets the cap, and it
is full. In RM2k there is no such cap.

A map with more drawn events than that used to stop the build. Now Wally
keeps `NPC_MAX` rows and the rest **lose their row, not their event**: their
pages still run, they still block on the hero's layer and they still
trigger, because the console reads all of that from the page tables, not
from the row. They behave like an event whose page draws nothing. What is
lost:

* **Seeing them**, on every page: a page that would switch one to a graphic
  shows nothing.
* **The passage a tile imposes.** An event drawn with an upper-layer tile
  carries that tile's passage bits in its row; without the row the cell
  only has the map's own.

The converter says which ones, map by map, in a WARNING.

## Which ones go

First the ones whose loss is only that they are not seen: no page has a
command or a way of moving, no command of the map, the common events or the
test pages names them (`MoveEvent`, `SetEventLocation`, `FlashSprite`…),
nobody makes them walk, and they impose no passage. Then the rest. Within
each group, the highest table index first —the events placed last in the
editor—. It is a rule anyone can redo by reading the map, and it needs no
guess about what matters on screen.

The cut happens before poses, slots and palettes are counted, so what is not
drawn takes no room in the sprite bank either. A map that fits never goes
through it.

## Measured

On 2026-10-06 the cap stopped 24 maps of Vampires Dawn and 3 of Desert
Nightmare; Desert had others over it that a different limit stopped first.
On 2026-10-10, converting the maps with more than `NPC_MAX` events: 24 of
Vampires Dawn and 9 of Desert Nightmare go over, from 105 drawn events
(Vampires Dawn's 332, which loses one row) to 258 (its 429, which loses
154). Since what is cut takes no sprite tiles, Desert's map 2 now fits a
VRAM layout it did not fit before. A Blurred Line has no map over the cap:
its cartridge came out byte for byte the same.

## How to reproduce it

`wally/tests/too_many_npcs.rs` in the-advocate builds a map over the cap and
checks which rows stay. In a game, converting Vampires Dawn's map 409 says
in its WARNING which events are not drawn.

## When it stops being enough

A map where something that matters is among the ones left out: a visible
event with no commands that the player has to see —a sign, a door drawn
as an event— in a map full of decoration. There the answer is not a better
rule but fewer rows: baking the decoration into the background
(`decorative_events`, see [Baked decorative events](los-eventos-decorativos-horneados.md))
takes those events out of the table before this cut.

And this is not the last limit of those maps: most of them also have more
events than the console's event table holds (`EV_MAX`, also bank 0's RAM),
which still stops the build.
