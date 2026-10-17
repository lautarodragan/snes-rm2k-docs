# The converter decides the CGRAM split

The 256 CGRAM entries are cut in half: the upper half belongs to the
sprites. The lower half is shared by the background, which is 8-bit and
addresses CGRAM directly, and the layer above, which is 4-bit and
therefore counts its index inside a 16-color palette.

A fixed cut doesn't work: with two palettes nailed down for the layer
above, the maps whose layer above asks for three or more fall out, and they
are several dozen, the first three of the game among them. And there is a
cause that **no split fixes**: a lone 17-color tile doesn't fit in a
15-color palette no matter how many there are, and that is fixed by merging
colors: `adeleine.reduce_colors` (see [When a game doesn't
fit](../optimizations/lossy.md)).

So the converter decides the cut map by map, and **the background gets
first pick**: it keeps the palettes it needs for the colors it really uses,
and the layer above takes whatever is left —up to what it asks for, never
more— and merges if that isn't enough. It goes in that order because there
are 300 maps whose layer above asks for one or two palettes against a
handful that would ask for seven: serving the layer above first would take
colors from the background in all of them so that a few wouldn't merge.

The converter's report says it map by map: how many colors the background
kept out of how many there were, how many palettes the layer above took,
starting from which, and how many colors it had to merge.

Converting both layers together is not a convenience: neither one can
decide the cut on its own, so `convert_with`, in `rm2k-snes/wally/src/background/layers.rs`
in the-advocate, is the only place where it is written. Before, each caller converted one and then the other, and
whether the three copies of the order matched was a matter of luck —exactly
the kind of error that had already loosened the comparison once.

## A message's face borrows palette 1 on the window's lines

Since 2026-10-15, a box's face —`ChangeFaceGraphic`'s— takes **no entry
from any map**. The message window is palette 0 and every other entry below
128 is the map's, so the face's fifteen colours go in **palette 1, entries
17 to 31, only while the window's lines are drawn**: HDMA channel 5 writes
them on the window's first fifteen lines, one colour a line, before the face
starts on line 16, and writes the map's own back —from `cgram_shadow`,
tinted as they are on screen— on the fifteen lines after the face ends on
63. Over a window with its background no pixel of the map is on those lines,
so the swap shows nowhere; what shows in a bare window is in [What faces do
not model](../divergences/what-faces-do-not-model.md). The channel runs
in indirect mode: its tables are in ROM, one per window position, and what
one of the vblanks of the box's first lines fills is the 120 bytes of
colours they point at, in far RAM —`runtime/message_face.s`; a table with
the colours inline would have been 166, and A Blurred Line's release
cartridge had 12 to spare before the pool grew—; the
channel is one the map leaves free —the battle's shake uses it, with no
window up, and 7 is `vram_drain`'s general DMA every vblank—. One colour a
line is what commercial games wrote to CGRAM in the horizontal blank; what
the console can take was measured in section 2 of [The windows, made
cheaper](../research/2026-10-11-the-windows-made-cheaper.md).

## The small pictures take sprite palettes from the top

A `ShowPicture` picture that goes in sprites draws with a whole sprite
palette, counted **from the top** —7, then 6—: the map's characters take
theirs from the bottom, and 4 to 7 are the ones the console's colour math
can blend, which is what a half-transparent picture uses. How many the map
leaves is Wally's, which leaves the pictures out as a whole when they do not
fit.

Since 2026-10-16 **the pictures of a map share palettes**: the converter
puts a picture in the first palette that takes its colours —the ones it
has, the ones that fit in what is left of fifteen, and the rest within two
steps of 31 of one it has—, and each picture's entry in the map's table
says which; the colours go in the cartridge once per palette. **A number the
map tones** —a `ShowPicture` or `MovePicture` with a tone other than the
neutral, as the event compiler's scan writes it down— shares only with
itself, since the console tones a picture by toning its fifteen entries in
`cgram_shadow`, and the vblank uploads the palettes a picture or a ramp left
waiting. See `share_palettes` in `rm2k-snes/convert/src/pictures.rs` and
`pic_palette` in `runtime/picture.s`, in the-advocate. Until that day each
of the two slots the console had took a palette of its own, 7 and 6.
