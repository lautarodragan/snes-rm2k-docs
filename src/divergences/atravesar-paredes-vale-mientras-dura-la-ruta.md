# Walking through walls lasts as long as the route

## What

Route command 36 —`walk_everywhere_on`— is **sticky** in RM2k: it writes
`Game_Player`'s `move_route_through`, which is a field of the saved game
—`SaveMapEventBase` in liblcf— and which nobody resets, not
`CancelMoveRoute`, not `ForceMoveRoute`, not `MoveTo` on changing maps. A
page that turns it on and does not turn it off leaves the hero walking
through everything until the end of the game.

Here the flag counts **only while the step is given by the forced route**.
The reason, with the symptom that gave it away, is in `cell_blocked`
(`runtime/event_pages.s` in the-advocate), which is where `crossing` is
read and not the sticky `route_crosses`.

For the reverse question —an event walking into the hero— the sticky one,
`route_crosses`, is still what is checked. It is an asymmetry, and it stays
because no route in the game exercises it: it would take an event walking
over the hero right after a page that left 36 on.

## Measured

Over the whole game: of the 153 pages that move the flag, **4 leave it on**,
and two of those —the Hover-Tram on map 13, `EV0028`, and map 14— are on the
main path. With RM2k's rule, anyone who walks into Sector 30 steps on the
chests they should not.

## When it stops being enough

A game that uses 36 on purpose to leave the hero walking through things
beyond the route. In this one the four that leave it on are oversights in the
original.
