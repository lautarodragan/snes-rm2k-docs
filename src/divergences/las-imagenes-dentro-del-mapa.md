# Pictures drawn into the map

## What

A project with `[graphics] map_pictures = true` gets the `ShowPicture`
pictures **that stay put on a map** drawn into the map itself, when the
cartridge is built, instead of shown as pictures: see `map_pictures.rs` in
rm2k-snes-convert and in Wally (the-advocate). They are the ones a game
drawn as a painting uses for what goes in front of the hero, its lights, its
shadows and its mists. Over a panorama fixed to the map, each is blended
into the panorama, and what the opaque ones cover goes in front of the hero
by the priority bit of the panorama's cells, in mode 3. On a painted map
—`[graphics] painted_maps`, see [the VRAM split](../internals/vram.md#a-painted-map-keeps-only-what-the-screen-shows)—
the cells they cover whole go in front by BG1's priority, and the edges
exactly, in BG2. Their commands are accepted without being done: the
conversion did them.

What the ROM does not do that RM2k does:

* **The characters are not shaded nor lit.** A shadow or a light is part of
  the painting under them, so a character that walks into a shadow keeps
  its colours; in RM2k the picture is over him too. The same with the
  mists.
* **What goes in front of the hero goes by 8x8 cells** in mode 3: a cell
  goes in front when the opaque pictures cover half of it or more. On
  Sunset that put 5 to 21 % of a roof's pixels on the wrong side —the
  hero's head over a thin beam, or a corner of floor over him—. On a
  painted map the edges are exact while they fit in BG2's 127 tiles, and
  the rest go by cells: 2.2 % over Sunset's 60 painted maps. The converter
  says how many per map ("its pictures put N pixels in front of the
  hero").
* **Nothing changes over time.** Each picture is drawn with the tone and
  transparency its `MovePicture`s leave it at: a light that comes on in
  four seconds is on from the start, a roof that appears from black is
  there before, an `ErasePicture` on the map does not erase it, and of
  several pictures under one number on one map —the flags that wave, a
  room with or without a second ceiling— the one shown most is drawn.
* **The screen's tint tints them**, which RM2k does not do to pictures.
* **A mist that goes with the screen on a map that scrolls is repeated over
  the whole map**, from where it is shown, and moves with the map; its wave
  and its drift are not done.
* **The events "above the hero" go in front of the roofs**: they are
  objects at priority 2, in front of BG2.
* **A map with such pictures is not baked**: its panorama goes in BG2 at 4
  bits, or painted, even if it would fit at 8 in BG1, because baked the
  cells in front of the hero would also be in front of the message window.

## Measured

On 2026-10-11, on Sunset Over Imdahl, with captures of snes9x of maps 28,
2, 13, 33, 7 and 22 against the 2015 RPG_RT under Wine: see the task
[`sunset-the-pictures-over-the-map`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/sunset-the-pictures-over-the-map.md) in the-advocate-work, and the
study, [The pictures over the map](../ports/sunset-over-imdahl/research/2026-10-11-las-imagenes.md).
No test of the ROM runs it: A Blurred Line has it off.

## When it stops being enough

When a game moves those pictures —clouds that drift, grass that scrolls,
flags that wave— or shades its characters with them. Mode 1 gave the exact
edges; colour math for the shadows does not reach the characters drawn with
object palettes 0 to 3, and on a painted map there is no VRAM left for its
mask: see [Mode 1 for the painted maps](../ports/sunset-over-imdahl/research/2026-10-11-el-modo-1.md).
