# Tried and left out

Optimizations that were built or measured and then removed or not
adopted, with the reason, so that whoever thinks of them again starts from
what was found. Each points to the page that has the numbers; those are
dated snapshots.

### The poses in LZ2

Each pose compressed as its own LZ2 stream, decompressed by the CPU when
it goes up. It was built: the poses compress well, but decompressing one
costs a large slice of a frame in the main loop, and the test suite lost
frames —the race ran slower, and tests went red—. The poses stay raw, and
what was saved instead came from storing them [without their empty
tiles](lossless.md#a-pose-goes-up-without-its-empty-tiles).

- **More**: [The S-DD1, for the poses](../research/2026-10-11-the-s-dd1.md),
  [Fitting the whole game in 8 MB](../ports/abl/research/2026-10-14-fitting-the-whole-game-in-8-mb.md).

### The S-DD1, for the poses

The compression chip of Star Ocean and Street Fighter Alpha 2, which
would compress the poses better than LZ2 and decompress them on the DMA
path with no CPU. Measured, not built: taro, on 2026-10-12, "we already
have the MSU-1 for what does not fit, and the extra complexity is not
worth it, for now". The cartridge keeps the mapper without chips, and what
does not fit in a game's ROM goes to its `.msu`.

What the measurement gave, which is what makes it not worth it today: A
Blurred Line does not need the space; Vampires Dawn does not fit even with
it, and goes with the MSU-1 required either way; and it is expensive —it
takes away banks `$40`–`$7D`, and the upper 4 MB are seen through four
1 MB windows switched by registers, which is a new mapper, window switches
in the runtime and pages per map in the packer; and on real hardware the
S-DD1 with the MSU-1 has not been tried with our ROM—.

**The door stays open**: it is "not now", not "never". It is reopened if a
game's poses in LZ2 cost visible frames, or a game should fit without the
MSU-1 and only the S-DD1 would make it fit.

- **More**: [The S-DD1, for the poses](../research/2026-10-11-the-s-dd1.md),
  with the numbers, the disposable compressor and how it was verified; the
  task [`s-dd1-for-the-poses-measure-before-deciding`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/s-dd1-for-the-poses-measure-before-deciding.md).

### Colour math for translucent events

Real transparency for A Blurred Line's translucent events, with the
console's colour math. It was implemented and verified —the `color-math`
tag in the-advocate— and taro rejected it for two reasons that are not
defects of the implementation:

* **The object stops animating.** The translucent event leaves OAM and
  becomes BG2 tiles, uploaded once on entering the map, and almost all of
  the game's animate: they are the save point. Bringing it back to life
  requires uploading its tiles by DMA at the event's cadence, which is the
  machinery of the ChipSet's animated tiles.
* **The hero is seen through it.** Mode 3's ordering leaves no background
  layer between the floor and the hero, so the only one is above. It is
  what FF5 does, and taro did not like it.

Translucent events are [baked](lossy.md#translucent-events-are-baked)
instead. **It is a decision about that one thing, not a ban on colour
math**: translucent pictures in sprites use it, since 2026-10-02 —there
blending is on only in object palettes 4 to 7, so the hero and the events
in 0 to 3 stay opaque—; what that costs is in [What pictures as sprites do
not model](../divergences/what-pictures-as-sprites-do-not-model.md).

For whoever picks it up again: `ppu_init` set `TS` and `CGWSEL` once and
for all, and **`CGADSUB` alone** turned blending on and off, written from
`flush_video` with the per-map value the converter emitted; the object
went inside the layer above, so it touched neither the VRAM split nor the
CGRAM one. Two things hold even if it does not go in: **the message window
is also BG2**, so blending makes it semi-transparent —fixed with an HDMA
channel that sets `CGADSUB` to zero on the window's lines—; and **snes9x
rounds differently from the hardware** in colour math addition —bsnes and
Mesen-S truncate, which is what the chip does—, so a case with colour math
goes into `tests/rpgmaker/test_cores.py` in the ABL port.

### Fusing a gradient window's colours, or whole windows

Before [a window with a gradient is fused until it
fits](lossy.md#a-window-with-a-gradient-is-fused-until-it-fits), three
other ways were tried: fusing colours until the tiles fit, which left
windows with four colours or two; a tiled background instead of a
stretched one, which was not enough and drew a sawtooth all over the
window; and fusing whole windows with a k-means, which fit but broke
frames.

- **More**: [A window with a gradient, fused until it fits](a-window-with-a-gradient.md#the-ways-that-were-not-taken).

### Calling every common event into a shared body

Parallel pages could call a shared body too, but a body compiled without a
map requests a refresh on every variable write, and in a page that runs
every frame that left half of Lashe City at thirty frames per second.
Parallel pages paste the body in place.

- **More**: [CallEvent: a shared body, or pasted in place](common-event-calls.md#why).

### Refreshing before every command

EasyRPG refreshes the active pages before every command. Measured here,
it cost several frames in a cutscene that turns switches on by the bunch;
no opcode reads which page is active, so the port does not. It comes in the day
one does.

- **More**: [The refresh runs at three moments](../decisions/the-refresh-runs-at-three-moments.md).

### Sharing background tiles between maps

Two maps with the same ChipSet could share their tiles in the cartridge.
Measured: the converter already stores identical blocks once, and few
tiles repeat byte for byte between maps, because each map quantizes its
own palette; and a shared pool did not fit in any VRAM layout.

- **More**: [Graphics and sound, from RM2k to the SNES](../research/graphics-and-sound-from-rm2k-to-the-snes.md),
  [Only the tiles the map draws go to VRAM](lossless.md#only-the-tiles-the-map-draws-go-to-vram),
  [Fitting the whole game in 8 MB](../ports/abl/research/2026-10-14-fitting-the-whole-game-in-8-mb.md).
