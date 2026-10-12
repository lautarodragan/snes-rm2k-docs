# What collision with events does not model

## What

Collision with events **is there** —see its row in the mechanics table of
`docs/port/events.md` in the-advocate— and it leaves out four things RM2k does:

* **`overlap_forbidden`**, which is 17 pages of the game;
* the **conflict of an event with a tile graphic against its own block**;
* that **a touch event on the hero's layer fires when it bumps into him**
  —`CheckCollisonOnMoveFailure`—;
* that a non-skippable forced route **retries** the blocked step instead of
  skipping it. That one has a page of its own, with what was measured and the
  golden that freezes it today:
  [A blocked step in a forced route](a-blocked-step-in-a-forced-route.md).

## Measured

Of the first three, the one closest to showing is the retry —the fourth, the
one with its own page—: **in the opening, collision stops no step**,
measured, but **the droid on map 2 depends on it**.

## How it looks today

It is not seen: no test fails because of this, and no page that compiles
today exercises the first three. The first two points are also noted in the
comment on `cell_blocked`, in `runtime/event_pages.s` in the-advocate,
which is where the mechanic lives: the `overlap_forbidden` field is read and
ignored, it is not that the page fails to compile.
