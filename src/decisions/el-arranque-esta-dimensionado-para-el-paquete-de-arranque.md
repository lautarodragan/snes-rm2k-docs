# Boot is sized for the boot package

## What

**Boot is sized for the audio package of the boot map**, not for a full
ARAM: `BOOT_FRAMES` covers loading the map, the driver and the directory
through the IPL, and that package, with a margin. The calculation is
`boot_frames` in `rm2k-snes/rm2k-snes-audio/src/emit.rs` in the-advocate.

**Each cartridge carries its own** since 2026-10-11: `rm2k-snes-audio
cartridge` writes `BOOT_FRAMES` into the cartridge's `musicdata.inc` as
`BOOT_FRAMES_FLOOR` —a constant of the runtime, in `runtime/far_ram.s`—
or the estimate rounded up, whichever is larger. Until that day
`BOOT_FRAMES` was that constant and the converter stopped if the estimate
went over it.

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
split that gives more to `hzstream`—, that cartridge's boot grows with it,
by itself and without warning. The tests read it from the symbol table, so
moving it doesn't move any golden: that was verified when it was lowered
from 112.

## Why per cartridge, with a floor

The constant was one number for every game. Vampires Dawn's boot map asks
for 46 frames, and raising the constant for it would have moved the frame
on which every other cartridge's loop starts, A Blurred Line's included.
The floor is what keeps a cartridge with a small package —A Blurred
Line's estimates 40.5— on the frame it always started on, with a
byte-for-byte identical ROM; a large package gets the frames it needs
instead of not building. The only ceiling left is the byte the ROM counts
boot frames in: past 255, the cartridge doesn't build.

The floor lives in the runtime and not in each game's `rm2k-snes.toml`:
what it protects is the runtime's —the loop starting on the same frame
whatever small data goes in—, and a knob per game would be one more with
no game asking for it.
