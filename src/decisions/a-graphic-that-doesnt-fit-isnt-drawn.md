# A graphic that doesn't fit isn't drawn

> **Partly superseded**, noted on 2026-09-29 (Guayabo, while sorting the
> decisions by repo): since 2026-09-08 (`ac8f356b` in the-advocate) `fits`, in
> `tools/port/sprites.py`, **lends** a palette to these graphics, just as it
> does to events ([every-event-is-drawn](every-event-is-drawn.md)).
> A graphic is only left undrawn if every palette belongs to a leader, which
> is what [move-route-command-34-on-the-hero](move-route-command-34-on-the-hero.md) says.
> What still holds is the part below about the three maps: **they don't get
> a new palette opened for them**.

## What

**A graphic that doesn't fit in the eight sprite palettes isn't drawn.**
The converter decides it, with a single function.

## Why

It applies to events drawn with a chipset tile and, since move command 34,
to the graphics a route changes to: there the command hides the event
instead of changing it.

**Forcing them broke three maps** —108, 114 and 207—.
