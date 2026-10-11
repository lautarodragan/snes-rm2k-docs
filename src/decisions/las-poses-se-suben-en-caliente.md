# Poses are uploaded on the fly

## What

**One pose per character lives in VRAM.** The twelve poses of each
character that changes pose live in the cartridge, and the current one is
uploaded by DMA during vblank, as FF5 does. Still characters keep sharing a
slot per (CharSet, index, pose), because they don't change.

## Why

RM2k poses are 24x32 and the smallest object that covers them is 32x32: a
character is 192 object tiles, and the PPU addresses 512 —the two name
banks, a hardware limit and not a split of ours—. With every pose resident,
two and a half characters fit, and the opening scene —Core, Manta, the
droid and Kersh walking on the same map— asked for 768.

The other way out was to build each character out of twelve 8x8 objects so
tiles could be shared, and that blows the 128 OAM entries on any map with
people. taro chose uploading on the fly.

What it costs: one DMA per pose that changes, with a cap per vblank
—whatever is left over waits for the next one—, and the queue has to upload
the pose in the same vblank as the OAM that already counts on it. How, in
`vram_queue` (`runtime/load_graphics.s` in the-advocate) and its queue
in `runtime/low_ram.s`.

## And distant still characters take turns on one slot

From taro, on 2026-10-01, so that Distant Paradise (108) fits: on a map
that doesn't fit in any VRAM split, and only there, still characters that
no camera position shows together share a slot even if they show different
poses, and the pose is uploaded when the one that needs it comes on screen,
through the same queue. Only those nobody moves and that show a single
graphic. It was Puma's option A in the task [`mundo-7-camino-a-paradise`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/mundo-7-camino-a-paradise.md)
in the-advocate-work; option B —all of a character's still copies facing the
same way— changed what is seen. How, in `runtime/shared_poses.s` and
in the task [`el-108-con-poses-compartidas`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/el-108-con-poses-compartidas.md).

## And if not even that fits, nobody owns a slot

From taro, on 2026-10-03, for ABL's farm (127), which doesn't fit even with
the turns —"let's go with 1", Puma's option D—: on a map like that, and only
there, the slots are a cache. Whoever comes on screen asks for one, walking
or not; the pose is uploaded through the same queue; and the slot nobody
drew in two frames is taken by the next one. Still characters showing the
same pose share theirs. If the cache fills up, the one asking **waits
without being drawn** until someone leaves the screen: it doesn't hang, and
the one waiting is the last one `build_oam` reaches. How, in
`runtime/cache_slots.s`; what was measured and what was ruled out
—the mirrors, the margin in cells—, in the task [`la-cache-de-ranuras`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/la-cache-de-ranuras.md)
in the-advocate-work.
