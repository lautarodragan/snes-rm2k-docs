# ChipSets

**ChipSets are not tilesets.** The left half of the 480x256 image is
autotiles: border blocks the engine combines according to the neighbors.
The editor stores in the map the ID of the already computed combination, so
to render it you have to pre-generate the 1419 possible combinations in a
32x45 atlas and index it by ID. `tools/rm2k/rm2k-render/src/chipset.rs`, in
snes-rm2k, is a port of `lmu2png/src/chipset.cpp` from EasyRPG Tools, which
is where all the magic offsets are.

**There are two layers**, and the drawing order between them depends on the
chipset's passability flags (`0x30` in the lower layer, `0x10` in the upper
one mark what goes above the player). Events are interleaved according to
their own layer: lower tiles → events in layers 0 and 1 → upper tiles →
events in layer 2.
