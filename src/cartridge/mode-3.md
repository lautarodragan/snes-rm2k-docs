# Mode 3 by default

**This is the choice that fit A Blurred Line, not a rule of the engine.** It
was made for that game's maps, and the engine already uses mode 1 where a
map needs it (see below). A game whose maps ask for another mode, or for
color math, can have it: what matters is what that game needs.

Maps are drawn in **mode 3, with 8 bits per pixel**. Every pixel of the
background is a direct index into the color memory (CGRAM), so there are
no per-tile palettes to juggle.

That was not a matter of taste: RPG Maker tiles with 16, 17 and 19 colors
exist, and no number of 15-color palettes fits them.

What it costs:

- **Twice the video memory per tile**: 64 bytes instead of 32. A map with
  many distinct tiles runs out of VRAM sooner.
- **Only two background layers**: the map, and the layer above the hero
  together with the message window. Anything that would need a third one
  has to find another place.
- **Sprites stay at 4 bits**: 15 colors and transparency per palette.

The exception is the **panorama** (a map's parallax background). For
each map, the tools choose how to show it: not at all if it is never seen,
baked into the background if it doesn't move against the map, in the
second layer if the map draws little above the hero, or with the map in
mode 1 at 4 bits and the panorama on a third layer.
