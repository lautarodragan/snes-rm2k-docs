# Boot is sized for the boot package

## What

**Boot is sized for the audio package of the boot map**, not for a full
ARAM: `BOOT_FRAMES` (in `runtime/far_ram.s` in the-advocate) covers
loading the map, the driver and the directory through the IPL, and that
package, with a margin. **And the converter stops if it doesn't fit**: the
calculation is `boot_frames` in
`rm2k-snes/rm2k-snes-audio/src/emit.rs`, and the converter does the
comparison.

It replaces "boot is sized for the ARAM ceiling", which left it at 112
frames —1.9 s of frozen map at power-on— so that filling the ARAM cost
nothing. taro asked for it to be brought under one second on 2026-09-26.

## Why

The ceiling made sense when the whole bank was uploaded at boot, byte by
byte through the IPL. Since the per-map packages, the IPL uploads only the
driver and the directory, and the samples go through the driver's command
3, three bytes at a time: the "four-port loader" that the old decision
said would buy it back already existed. What is uploaded at power-on is a
single package, so boot can be measured against it.

What it costs: if the boot map's package grows —another track on map 4, a
split that gives more to `hzstream`—, the converter warns and the number
has to be raised by hand. And the tests read it from the symbol table, so
moving it doesn't move any golden: that was verified when it was lowered
from 112.
