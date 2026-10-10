# Finished routes give up their slot

## What

The ROM has twelve slots for event routes —`route_ev`, in bank 0's BSS,
which is full—. Until 2026-10-03 an event that got one kept it until the
next map, and the converter refused to build a map whose pages sent more
than twelve different events walking.

Since then, **when none is left free, the first one whose route has
finished** —no commands left to give, no step, wait or jump, no route of its
own: `route_busy`— **goes to the event that asks for it**. The cap is twelve
moving at once, not twelve on the whole map. The converter warns about it
instead of stopping. See `reclaim_slot` in `tools/runtime/event_pages.s` in
the-advocate.

What the event loses with its slot is what RM2k keeps for it after a route:
**the speed, the frequency and the flags** the route changed —walking
through walls, the fixed animation, the locked facing— go back to those of
its page. **Where it faces it does keep**: it is written into its row (+10),
which is where the new slot reads it from if it walks again.

## Measured

It was asked for by the farm in A Blurred Line (127): the celebration makes
Pierson and the people of the chosen profession jump in place —up to eight—,
and the dance that follows has six more with a route of their own. That is
eighteen different events with a route on the map, and never more than nine
moving at once. Without this the converter refused to build 127; with the
usual twelve and without giving slots up, two of the ones strolling in the
dance never move (enforced by `test_recorrido_granja_golden.py` in the ABL
port, which was seen red that way).

No map that already fit changes: they all send twelve or fewer walking, so
they never run out of free slots and `reclaim_slot` does not run.

## When it stops being enough

An event that a route leaves with its speed changed, or walking through
walls, and that after another one takes its slot walks on its own or gets
pushed: it would walk with what its page says. And a map with more than
twelve moving at once, where the route that finds no slot is lost without
warning, as always.
