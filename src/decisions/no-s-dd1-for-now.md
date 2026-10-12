# No S-DD1, for now

## What

**The cartridge does not use the S-DD1**, the compression chip of Star
Ocean and Street Fighter Alpha 2, even though it would compress the poses
better than LZ2 and decompress them on the DMA path without CPU. The
mapper stays the one without chips —see [the cartridge goes to 8
MB](el-cartucho-pasa-a-8-mb.md)—, and what does not fit in a game's ROM
goes to its `.msu`, as [the MSU-1 required only when the ROM does not
reach](el-msu-1-obligatorio-si-la-rom-no-alcanza.md) says.

**The door stays open**: it is "not now", not "never".

## Why

From taro, on 2026-10-12, after [the
measurement](../research/2026-10-11-el-s-dd1.md): we already have the
MSU-1 for what does not fit, and the extra complexity is not worth it, for
now.

What the measurement gave, which is what makes it not worth it today:

- **A Blurred Line does not need the space**: it uses 86 of the 127 banks.
  The poses in LZ2 cost it frames, but none of its tests or its play shows
  it.
- **Vampires Dawn does not fit even with it**: the S-DD1 wins ~3.46 MB
  against the 3.75 it is short, before waste. It goes with the MSU-1
  required either way.
- **It is expensive**: the S-DD1 takes away banks `$40`–`$7D`, and the upper
  4 MB are seen through four 1 MB windows switched by registers. That is a
  new mapper, window switches in the runtime and pages per map in the
  packer; and on real hardware, the S-DD1 with the MSU-1 has not been tried
  with our ROM.

Earlier, on 2026-10-11, taro had already said they would avoid another
chip while the MSU-1 is optional, for the complexity; the measurement was
to decide it with numbers.

## How it applies

- **The poses stay in LZ2**, decompressed by the CPU.
- **It is reopened if a game needs it**: a game whose poses' LZ2 costs
  visible frames, or one that should fit without the MSU-1 and only the
  S-DD1 would make fit. The numbers, the disposable compressor and how it
  was verified are in the research; the task is
  [`s-dd1-for-the-poses-measure-before-deciding`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/s-dd1-for-the-poses-measure-before-deciding.md).
