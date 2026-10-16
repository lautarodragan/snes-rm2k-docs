# The possible leaders are an approximation

## What

**The possible leaders are an approximation.** The converter simulates the
`ChangePartyMembers` of the pages that compile to know which actors can be
first in the party.

## Why

There is no static way to know it exactly, and which actors get a palette
reserved depends on it. **If a character is ever drawn without graphics,
this is the first place to look**; `tests/tooling/test_leaders.py`
in the ABL port (the-advocate-ports/abl) guards the part that already failed
once.

## How it applies

The party is reset to the cartridge's at each map, because the order of
the files is not the order of play (Kersh, in ABL's opening). Within a map,
each batch of consecutive `ChangePartyMembers` counts three ways: in file
order on the map's party, on its own from the cartridge's party, and on its
own from an empty party, if some batch can empty it. The last two came on
2026-10-16 with Dooms 2: its first map is a row of alternatives —each
candidate's page takes the narrator out and puts its character in, or takes
him out alone and teleports, and the character joins an empty party on
their first map—, and played only in file order every story's hero but one
walked undrawn
([the task](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/dooms-2-the-hero-is-not-drawn-on-some-maps.md)).

Counting too many costs each extra leader its twelve poses in the
cartridge and a row in each map's actor table; counting too few is a hero
drawn without a graphic. So the approximation leans to too many.
