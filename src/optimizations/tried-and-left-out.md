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

The compression chip of Star Ocean, which would decompress the poses on
the DMA path with no CPU. Measured, not built: it takes away banks
`$40`–`$7D` and sees the upper 4 MB through switched windows, which is a
new mapper under the whole runtime, and the game that needed the space
does not fit even with it. It is "not now", not "never".

- **More**: [No S-DD1, for now](../decisions/no-s-dd1-for-now.md),
  [The S-DD1, for the poses](../research/2026-10-11-the-s-dd1.md).

### Colour math for translucent events

Real transparency for translucent events, with the console's colour math.
It was implemented and verified —the `color-math` tag in the-advocate— and
rejected: the event leaves OAM and stops animating, and the hero is seen
through it. Translucent events are baked instead; translucent pictures do
use colour math.

- **More**: [Translucent events don't use color math](../decisions/translucent-events-dont-use-color-math.md).

### Fusing a gradient window's colours, or whole windows

Before [a window with a gradient is fused until it
fits](lossy.md#a-window-with-a-gradient-is-fused-until-it-fits), three
other ways were tried: fusing colours until the tiles fit, which left
windows with four colours or two; a tiled background instead of a
stretched one, which was not enough and drew a sawtooth all over the
window; and fusing whole windows with a k-means, which fit but broke
frames.

- **More**: [A window with a gradient is fused until it fits](../decisions/a-window-with-a-gradient-is-fused-until-it-fits.md#why).

### Calling every common event into a shared body

Parallel pages could call a shared body too, but a body compiled without a
map requests a refresh on every variable write, and in a page that runs
every frame that left half of Lashe City at thirty frames per second.
Parallel pages paste the body in place.

- **More**: [CallEvent into a shared body](../decisions/call-event-into-a-shared-body.md#why).

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
  [The map takes to VRAM only what it draws](../divergences/the-map-takes-to-vram-only-what-it-draws.md),
  [Fitting the whole game in 8 MB](../ports/abl/research/2026-10-14-fitting-the-whole-game-in-8-mb.md).
