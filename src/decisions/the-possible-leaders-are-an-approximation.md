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
the files is not the order of play (Kersh, in ABL's opening). Each map is
played three ways, and whoever leads after any batch of consecutive
`ChangePartyMembers` counts: all its pages in file order on one party; each
page on its own from the cartridge's party; and each page on its own from
an empty party, if some page ends with nobody in it. The last two came on
2026-10-16 with Dooms 2: its first map is a row of alternatives —each
candidate's page takes the narrator out and puts its character in, or takes
him out alone and teleports, and the character joins an empty party on
their first map—, and played only in file order every story's hero but one
walked undrawn
([the task](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/dooms-2-the-hero-is-not-drawn-on-some-maps.md)).

Counting too many is not free either: a leader that stands as an event on
a map takes a sprite palette of its own there, and the other events may
lose theirs. That is why the empty start asks for a page that **ends**
empty —ABL's car chase empties the party and fills it again in the same
page— and why the parties the test pages start with are played in file
order only: played the other two ways they made leaders of actors the game
never puts first, and the Paradise celebration lost the colours of three
villagers. Counting too few is a hero drawn without a graphic.
