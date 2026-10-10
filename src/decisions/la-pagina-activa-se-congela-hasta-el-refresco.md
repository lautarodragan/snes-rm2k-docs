# The active page is frozen until the refresh

## What

**An event's active page is frozen until the refresh.** It isn't
recomputed every time someone asks.

## Why

It is `Game_Event::page`, and only `Game_Map::Refresh()` rewrites it, at
the start of `Game_Map::Update`. The ROM does it by storing it in the NPC's
row.

A rule follows for any loop that bails out by hand: **don't bail out with a
refresh pending**, because the next frame does do something.
