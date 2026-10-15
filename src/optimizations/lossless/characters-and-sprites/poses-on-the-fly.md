# Poses are uploaded on the fly

A lossless optimization —see [Lossless](../../lossless.md)—: how the characters fit in the 512 object tiles the PPU addresses.

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

What it costs: a few DMAs per pose that changes, with a cap per vblank
—whatever is left over waits for the next one—, and the queue has to upload
the pose in the same vblank as the OAM that already counts on it. How, in
`vram_queue` and `vram_drain` (`runtime/load_graphics.s` in the-advocate)
and its queue in `runtime/low_ram.s`.

**When the queue does not fit, it is an NPC who waits, never the hero**
(2026-10-13). The hero is always on screen and always moving, and he is
the last to queue in a frame: in The Book of Three's Caer Dallben East
the walkers filled the queue every frame and Taran walked with a single
pose. So the last entry is kept for him and his pose goes at the front
—`vram_queue_hero`—, uploaded in the next vblank whatever the NPCs asked
for. The task:
[`book-of-three-the-hero-freezes-in-caer-dallben-east`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-the-hero-freezes-in-caer-dallben-east.md).

## And a pose goes up without its empty tiles

From taro, on 2026-10-14, so that ABL's whole game fits in 8 MB without
losing anything: 52% of the poses' 8x8 tiles are fully transparent —the
24x32 character padded to a 32x32 object, and the air above its head—, and
the cartridge stored them all. Now **a pose is a 16-bit mask of the tiles
that draw something, and only those tiles**: 571 KB less in the whole
game, 395 KB in `release`. Measured in
[the research of that day](../../../ports/abl/research/2026-10-14-fitting-the-whole-game-in-8-mb.md).

The object still reads its sixteen tiles, so **an empty one is zeroed in
the slot**, not skipped: skipping it would mean smaller objects, which is
what the 128 OAM entries ruled out above. Nor is it enough to clear a slot
once: a tile drawn in one pose and empty in the next would keep the old one.
So each 32x32 block of the sprite bank remembers which of its tiles may
hold something, and the upload zeroes those the slot drew and the new pose
does not, besides the drawn ones, in runs along each row. What each block
holds when a map loads comes from the converter, with the bank: without it,
each walker's first step zeroed all its empty tiles and the vblank ran over.

**It must not cost more than uploading the poses whole**, because that was
already at the vblank's edge: five of Lashe City's walkers stepping on the
same frame ended the message window's line 0.1 lines before the screen came
back. Measured in bsnes over every map of `release`, the worst frame —five
poses— went from 9,069 dots to 7,475, and a walking step from 1,990 to
1,618 on average; the worst single pose costs 4% more than a whole one —a
step that zeroes and uploads in several runs—. The hero still goes first.

What it costs instead: 64 bytes of bank 0's RAM, one word per block. How,
in `vram_drain` and `pose_record` (`rm2k-snes-mapdata`), and in the task
[`poses-without-their-empty-tiles`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/poses-without-their-empty-tiles.md).

## And distant still characters take turns on one slot

From taro, on 2026-10-01, so that Distant Paradise (108) fits: on a map
that doesn't fit in any VRAM split, and only there, still characters that
no camera position shows together share a slot even if they show different
poses, and the pose is uploaded when the one that needs it comes on screen,
through the same queue. Only those nobody moves and that show a single
graphic. It was Puma's option A in the task [`world-7-the-road-to-paradise`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/world-7-the-road-to-paradise.md)
in the-advocate-work; option B —all of a character's still copies facing the
same way— changed what is seen. How, in `runtime/shared_poses.s` and
in the task [`108-with-shared-poses`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/108-with-shared-poses.md).

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
—the mirrors, the margin in cells—, in the task [`sprite-slot-cache`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/sprite-slot-cache.md)
in the-advocate-work.
