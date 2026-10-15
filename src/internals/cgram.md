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
fit](../fitting.md)).

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
