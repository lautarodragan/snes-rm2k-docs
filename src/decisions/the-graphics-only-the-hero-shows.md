# The graphics only the hero shows go in the leaders' slot

## What

**A graphic that only the hero ever shows is drawn like a possible leader**:
in the leaders' CGRAM slot, with colours of its own that the console
uploads when the hero takes it. Since 2026-10-11.

"Only the hero" means no move route gives it to an event: the graphics of
`ChangeSpriteAssociation`, and those of move route command 34 on the hero.
The event compiler's scan says which graphics a route gives an event
(`graphics_on_events`), and the converter hands the rest to Wally as
`hero_graphics`. One that an event of the map also draws as a page graphic
is left out: that one needs its colours in the map's palette.

## Why

Before, they were split among the map's eight sprite palettes like any
other graphic of command 34, "while they fit". Two things came out of that,
both measured on Vampires Dawn on 2026-10-11:

* **The cartridge carried one pose bank per map for each of them.** A pose
  bank is the twelve poses of a character as one map quantized them, and
  the cartridge keeps one per distinct quantization —see
  [Poses are uploaded on the fly](poses-are-uploaded-on-the-fly.md)—. The
  compiler reserves the graphics of `ChangeSpriteAssociation` in the
  graphics table of **every** map, and in most maps they didn't fit: they
  were drawn with someone else's palette, quantized to its nearest
  colours, a different palette in each map. Six of them —Valnar's and
  Asgar's transformations— were 367 of the 513 extra banks: 75 banks for
  `Extra2:2` alone.
* **They were seen with the wrong colours** in most maps: `Extra2:2` was
  drawn with someone else's palette in 224 of 426 maps.

In the leaders' slot the bank is the same in every map —the indices are the
character's own palette, sorted— and they take no palette from the map, so
the events and tiles that were lent one get theirs back.

Measured on the emission request of Vampires Dawn with the eleven maps that
were out for the ROM put back: 1,498 pose banks to 1,163, 10,095 distinct
poses to 6,717 —4.93 MB to 3.28 MB of what can't go to the `.msu`—, and
the maps with some graphic drawn with someone else's palette from 365 to
77. The eleven maps went back in.

## How it applies

* Wally puts them in `own`, like the leaders that share the slot, when
  there is a leader that isn't also an event of the map; and every graphic
  of command 34 that ends in a leaders' palette brings the colours its pose
  bank was drawn with —its own, or the palette's—.
* `rm2k-snes-mapdata` writes those colours once for the whole cartridge,
  in `hero_colors`, and one byte per graphic behind `route_graphic`: its
  entry, from 1, or 0.
* The runtime copies those bytes to `route_gfx_colors`;
  `hero_poses_of_graphic` points `hero_cgram` at the entry, and
  `graphic_hero` —command 34 on the hero— runs `apply_tint` so they reach
  CGRAM. `ChangeSpriteAssociation` already ran it.

It changes the first cost of
[Move route command 34 on the hero](move-route-command-34-on-the-hero.md): a
graphic only the hero shows is no longer drawn with one of the map's
palettes.

What is left of the same problem is smaller and spread out: 168 extra
banks, about 0.7 MB at most, from characters quantized differently in a
handful of maps each —a different set of visible poses, a palette shared
in another order, the timer's cap—.
