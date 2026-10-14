# What walking by a movement type does not model

## What

A page whose movement type is random, vertical, horizontal, toward the hero
or away from him —RM2k's `MoveType_random` to `MoveType_away`— walks on its
own since 2026-10-14: the compiler gives it a route of a single command the
ROM repeats, and each time the event has stood still long enough the ROM
decides one step the way `Game_Event::UpdateSelfMovement` does. See
`runtime/walk_by_type.s` and `route::own` in the compiler, in the-advocate,
and [`events.md`](../internals/events.md).

What differs from RM2k:

* **The draws are not RM2k's.** The probabilities are —of ten draws, three
  straight on, two to each side, one back and two standing still; the wait
  after a random step, three to six fifths of a step's—, but they come from
  a xorshift of the walkers' own, seeded at reset, and not from RM2k's
  generator: a random walk is random, not the same walk. Its own and not
  the map's, which is `ControlVars`'s, so that a page's random numbers do
  not depend on how many walkers the map has.
* **"On screen" is the console's screen.** Toward and away look at the
  hero only while the event is on screen or within two cells of it, and off
  it they walk at random. The screen is 256 by 224 and not RM2k's 320 by
  240, so the same walker gives up on the hero a little closer.
* **The first step after the page arrives** comes after a turn's wait, as
  in a page's own route, and not after a step's.
* **The pause of a random walker** stands still a random part of a freshly
  drawn wait, not of the one left by its last step: the same distribution.
* **Frequency 1 waits 255 frames after a step**, not 256: the ROM's wait
  is a byte. A route that goes down to 1 is still rejected; a page that
  walks by a type at 1 —Sunset over Imdahl's ravens— walks a frame early
  rather than stand still. Its random waits, three to six fifths of that,
  are held at 255 too.
* **Twelve route slots, and four kept for forced routes.** A walker by type
  takes one of the ROM's twelve route slots, which are also those of the
  pages' own routes and of `MoveEvent`. It only takes one while at least
  four others are free —the page that sends the most events walking at once
  in ABL moves four—, so a map with more walkers than that has the rest
  standing at their cell; and a walker never gives its slot to a forced
  route that finds none, as an own route does not. See
  [Finished routes give up their slot](finished-routes-give-up-their-slot.md).

## Measured

In A Blurred Line `release` carries pacers only: Marcy in the mayor's house
(70), the cook in the deli (73), the one in Yun Town (67) and two in Sector
34 (38). Against the original with Wine, Marcy goes from one end of her row
to the other and back in about two and a half seconds; the port takes 166
frames, the same. `tests/abl/test_walkers.py` in the ABL port walks the
pacers and the stop while a page runs; the ports' `tests/test_walkers.py`
walks The Book of Three's random animals and Vampires Dawn's figures that
flee.

The maps that have more walkers than slots: Tasgarde Mainframe in ABL
(285), which the cartridge does not carry, with 27 skeletons that run at
the hero; and nine of Vampires Dawn, up to 56 on Limm (141).

## When it stops being enough

On a map with more walkers than slots —Vampires Dawn's towns—, where the
ones that find none stand still. And when a scene sends one of them walking
with `MoveEvent` on a map whose slots are all taken: the route is lost, as
always.
