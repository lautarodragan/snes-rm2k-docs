# Move route command 34 on the hero

## What

**Move route command 34 —change graphic— is also done on the hero**, since
2026-09-12.

## Why

What kept it out turned out not to hold: the hero's graphic comes from the
actor table, but **the actor's twelve poses are written in the same shape**
as an entry of `npc_poses`, so the ROM moves the `hero_poses` pointer and
`place_hero` doesn't even notice.

Measured: **+30 pages** of the game —from 2835 to 2865— and 16 autorun
pages, among them the three of `EV0047` on map 8, which taro was never able
to interact with, and the one of the `Hover-Tram` on map 9, which changes
the hero's graphic to board it.

## What it costs, declared

* **While the change is in effect, the hero is drawn with the new graphic's
  palette**, which is one of the map's eight sprite palettes, and not with
  the leader's own slot. `hero_cgram` is switched off on the change: leaving
  it on would write Talan's fifteen colors over the graphic's palette,
  because `apply_tint` uploads them **into the row `hero_pal` says**.
  Since 2026-10-11 that holds only for a graphic some event also gets: one
  only the hero shows goes in the leaders' slot with colours of its own —see
  [The graphics only the hero shows go in the leaders' slot](the-graphics-only-the-hero-shows.md)—.
* **It doesn't survive a map change.** The poses live in the map's sprite
  bank, so the graphic from over there doesn't exist here; the ROM restores
  it in `pick_hero_graphic`. In RM2k `Game_Player` carries it along. It
  isn't noticeable: the only page in the game that changes the hero's
  graphic and then teleports puts it back in the command right after the
  teleport.
* **In the cartridge**, measured on `abl`: the graphic a route changes the
  hero to goes into the map's sprite bank, like any event's. On map 9 that
  is two more —`Future2:7` and `Future1:0`— and with them an event drawn
  with a chipset tile has to hang on to someone else's palette. Map 9's
  battle animations **weren't being drawn before either**: the control run
  without command 34 gives the same warning, so that map filled the eight
  palettes on its own.

It is covered by `grafico-heroe` and `heroe-invisible`, one per branch: the
graphic that is seen, and `nobodyhere`, which hides the hero the way it
hides an event.

## And on events

On events command 34 was already done before, and what it was worth is
measured too: **+25 pages**. For a while that number lived under a heading
that said it was missing.
