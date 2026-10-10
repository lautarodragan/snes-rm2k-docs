# The converter decides the VRAM split

The 64 KB can't be split any way one likes: the base of the sprite tiles
goes in steps of 16 KB, that of each background in steps of 8 KB, and that
of each tilemap in steps of 2 KB. Every map carries the message window,
which asks for 8 KB of tiles and 2 KB of tilemap of its own —the tilemap
holds two planes of ten rows, the window and the window without a frame,
and which one is seen and on which lines is said by HDMA: see
`message_place.s`—, and the tilemap of the layer above is fixed at the end.
With that there is no layout that serves every map: which one applies is
decided by the converter —along with the ready-made values of `OBSEL` and
`BG12NBA`, and since 2026-09-25 the address of the background tilemap— and
travels in the `.inc`. The ROM chooses nothing. Why the background is
8-bit to begin with: [Mode 3, always](../cartridge/mode-3.md).

There are six, and `vram_layout` returns **the first one that fits**, so
adding one at the end doesn't change the layout of any map that already
had one. There are two more, the panorama ones —see below—, which
`vram_layout` never returns:

```text
window         sprites 448 | window_map | bg 448 | map $5800 | above 128 | window 256
window+bg      sprites 256 | bg 480  | window_map | map $5800 | above 128 | window 256
window+sprite  sprites 512 | bg 384  | window_map | map $5800 | above 128 | window 256
window+both    sprites 384 | map $1800 | bg 480  | window_map | above 128 | window 256
window+ceiling sprites 256 | bg 544  | window_map | map $5800 | above 128 | window 256
window+above   sprites 384 | map $1800 | bg 384  | above 256 | window 256 | window_map
```

In the code they are `LAYOUT_WINDOW`, `LAYOUT_WINDOW_BG`,
`LAYOUT_WINDOW_SPRITE`, `LAYOUT_WINDOW_BOTH`, `LAYOUT_WINDOW_BG_CEILING` and
`LAYOUT_WINDOW_ABOVE`.

The details, with the addresses, are in `LAYOUT_WINDOW*` in `vram.rs` of
`tools/rm2k-snes/mapdata/`, and `check_splits` checks that each one
respects the hardware's alignments and what the ROM assumes. The long
reasoning behind each layout stayed in the history of
`tools/port/vram.py`, where they lived until 2026-10-01.

"+sprite" is asked for by **Delcentric Factory**, the road to the
auditorium: it spends 217 background tiles and **475 sprite tiles** —26
NPCs with a CharSet are 28 slots, that is exactly 448 tiles, and on top
come the 8 glyphs of the timer and the 19 raindrops—. The 512 is not a
choice: it is the hardware's ceiling, because the name field of OAM has
nine bits and with `OBSEL`'s name select at zero the two tables are stuck
together.

"+both" is asked for by **`Sector 34 With Car`**, map 38: 476 background
tiles and 347 sprite tiles. In bytes it fit in the other three; what didn't
allow it was the background tilemap nailed at $5800, which cuts BG1's bank
at 448 tiles. It is the only layout that moves it: it brings it down to the
2 KB left between the sprites and the background, and the ROM reads it
from `FAR_VRAM_MAP` when building rows and columns.

## Where the ceiling is

Enumerating every base the hardware allows —with the layer above and the
window stuck together, and the tilemap of the layer above at $7800—, the
maximum of background tiles for each sprite cap is:

```text
sprites      256   320   384   448   512
background   544   512   480   448   416
```

And it is the same with the background tilemap free or nailed at $5800:
moving it doesn't shift the ceiling. What does change is which layouts
respect the save-slot screen, which overwrites $2000..$4000 and counts on
`load_map` to restore it: with the tilemap at $5800, 347 sprites leave 448
for the background; moving it, 480. That is what it was moved for.

Two of the layouts are below the ceiling —"+bg" could give 544 and
"+sprite" 416—. Raising them would change the layout of the maps that
already use them.

"+bg" was asked for by **the world**, map 66: 527 background tiles and 222
sprite tiles. Instead of raising "+bg", "+ceiling" was added at the end,
which is "+bg" with the 544: the maps that were already there stay where
they were. And 544 tiles of 8bpp are 34 KB, more than the LZ2 load buffer,
so that background travels in two streams: see `lz2_backdrop` in
`tools/runtime/decompress.s`.

The sixth, "+above", was asked for by **Sorbe Village**, map 69: 157 tiles
in the layer above, and the other five give it 128. It raises no
background or sprite ceiling: **it moves BG2's base** from $6000 to $5000,
and with that the layer above has 256 tiles and the window starts at index
256 of BG2 instead of 128. Since the window's cells carry that index baked
in, the cartridge carries two planes of the window —640 bytes each— and
`stamp_window` chooses its own by the distance between the window and
BG2's base. `vram_layout` has since also looked at the layer above; the
maps that already converted all fit in 128, so none changed layout.

## When no layout is enough: the still ones take turns

The ceiling above is the hardware's, and **Distant Paradise**, map 108,
goes over it: 462 background tiles —only "+bg", "+both" and "+ceiling"
serve it— and 42 sprite slots, 696 tiles, against the 24 the best one
leaves. Almost all of that is still poses —fifteen neighbors facing three
or four ways—, and on screen there are never more than half.

So in a map that fits in no layout, and **only there**, the still ones that
are never on screen together share a slot even if they show different
poses, and the ROM uploads the pose of the one that comes on screen. Who
takes turns with whom is decided by `wally` —`plan_sharing` in its
`map.rs`, with the coloring of `share` in its `sprites` module—, the table
is emitted by `share_table` in `rm2k-snes-mapdata`, and what the ROM does
is in `tools/runtime/shared_poses.s`. Map 108 ends up with 22 slots, 376
tiles, and fits in "+both". The other maps convert as always: `wally`
first tries without turns and only if that doesn't fit converts again with
them.

## When not even taking turns is enough: a slot cache

**ParadiseFarmland**, ABL's map 127, doesn't fit even that way: the
celebration puts twenty-nine people on one screen, sixteen of whom the
scene makes jump and spin, and the map asks for 41 slots against the 32
the best layout gives. Taking turns doesn't help, because the still ones
are all together.

So in a map that doesn't fit even with turns, and **only there**, nobody
has a slot: whoever comes on screen asks for one, the ROM uploads their
pose, and a slot that has gone two frames without being drawn can be taken
by someone else. The still ones that show the same pose share theirs, as
always; the one that walks has its own while it is seen. `wally` decides it
—`Mode::Cache` in its `map.rs`, with the count in `sprites::cache`—, and
gives the cache all the blocks that fit in the best layout for its
background; the table is emitted by `cache_table` in `rm2k-snes-mapdata`,
and what the ROM does is in `tools/runtime/cache_slots.s`. Map 127 ends up
with the hero, the spin slot and 30 in the cache: 32 blocks, 512 tiles, in
"+sprite".

What is seen at once in map 127 can't be counted by the converter: the
celebration and the dance that follows are never together, but by where
the events start they add up to 33 on one screen, and `wally` warns about
it. The console does know, because a row that isn't drawn asks for
nothing: in the celebration they are 26. The measurement of the whole game,
and which aids were tried, in the task `la-cache-de-ranuras.md` in
the-advocate-work.

## A big picture doesn't use the layout

A `ShowPicture` picture that covers the screen goes in BG1, in mode 1, with
the map hidden —[big pictures in mode
1](../decisions/las-imagenes-grandes-en-modo-1.md)—, and **takes the same
place in all six layouts**: its 4bpp tiles from word 0 up to $3FFF —the
1024 a tilemap entry can name—, over the sprites and the map tiles, and its
tilemap at $4000. The window tilemap falls in that range in "window"
($1C00), so while the picture lasts it moves to $4800, which in none of
them belongs to anything used meanwhile —in some they are map tiles, which
are reloaded—; the tiles of BG2 and of the window are from $5000 upwards in
all of them. What it overwrites is restored, when it is erased, by the same
load as returning from a battle: see `tools/runtime/big_picture.s`.

## A big picture with zoom uses the other half

Mode 7 owns words `$0000` to `$3FFF` —its 128x128 map in the low bytes and
its 256 tiles in the high ones— and can't be moved. So a big picture that a
`MovePicture` enlarges or shrinks, and which therefore carries a mode 7
texture, is shown still **in the upper half**: its tiles from `$4000` —up
to 960— and its tilemap, one 32x32 screen, at `$7C00`. While it is still,
the texture is uploaded to the lower half one piece per vblank, over the
sprites and the map tiles, which aren't visible. That overwrites the window
and BG2's tiles, which were up there in all six layouts: with mode 7 on
screen the upper half is left free and the window goes back there, also in
pieces. Erasing it restores everything with the same load as returning
from a battle, which overwrites the same words. See
`tools/runtime/big_picture_zoom.s`.

## A map that shows its panorama uses one of its own

Since 2026-10-05, the maps whose panorama Wally gives a layer of its own
—see `Way` in `background/panorama.rs`—. There are four, and a map takes
the first one of its mode where its background, its sprites and its
panorama fit: Wally converts the panorama with the tiles left by the first
one that is enough for the background.

```text
panorama                 sprites 384 | map $1800 | bg 256 | panorama 256 | window 256 | window_map | panorama 320 | its tilemap $7800
panorama_m1              sprites 256 | map $1000 | window_map | bg 512 at 4 bits | panorama 768 at 2 bits | its tilemap $5800 | above 128 | window 256
panorama_bg              sprites 384 | map $1800 | bg 384 | panorama 256 | window 256 | window_map | panorama 64 | its tilemap $7800
panorama_bg_sprite       sprites 256 | map $1000 | window_map | bg 384 | panorama 256 | window 256 | panorama 128 | its tilemap $7800
panorama_bg_ceiling      sprites 256 | map $1000 | window_map | bg 448 | window 256 | panorama 256 | its tilemap $7800
```

In the code they are `LAYOUT_PANORAMA_MODE3`, `LAYOUT_PANORAMA_MODE1`,
`LAYOUT_PANORAMA_MODE3_BG`, `LAYOUT_PANORAMA_MODE3_BG_SPRITE` and
`LAYOUT_PANORAMA_MODE3_BG_CEILING`.

**The last one moves BG2's base**, which is at `$5000`, inside the
background tiles: BG2's first 128 belong to the background, and nobody in
BG2 names them —the window is at 128, as in "window", and the panorama
after it—. That is why `load_above` uploads nothing to BG2's base in a map
with the panorama in mode 3.

**In mode 3 the panorama is BG2**, so it has to fit, together with the
window, in what BG2's ten bits reach from its base: it goes before and
after the window, and the window stays at index 256, from `$5000` upwards,
where a big picture doesn't overwrite it. Its tilemap is that of the layer
above, which the map doesn't use. **In mode 1 it is BG3**, with its own
base and tilemap, and the background goes at 4 bits: its `tiles` is
counted in 64-byte units, like the 8-bit one, so its 256 are 512 tiles.

In both, the panorama tiles that fall after BG1's come back with
`load_above` —`pano_load`— just as BG1 does with `load_map`, so the screens
can overwrite them. The details, in `LAYOUT_PANORAMA_MODE*` in `vram.rs`.

## Battle doesn't use the layout

A battle overwrites the whole VRAM and `back_from_battle` restores it:

```text
word 0 .. $1FFF       the text, in BG2: 255 pairs of 4bpp tiles
$2000 .. $37FF        the windows, 8bpp tiles of BG1 (192 fit)
$3800 .. $3BFF        BG1's tilemap: the scene and the windows
$3C00 ..              the text tilemap, `SLOT_MAP`
$4000 .. $7FFF        the scene, 512 tiles of 8bpp
```

**The scene and the windows are the same layer**, BG1 in mode 3: the scene
takes the first sixteen rows of the tilemap, and the windows below —and the
description one, which covers the top four while a list is open— go in the
rows that are left, with tiles numbered from the scene's base, which wrap
around to `$2000` (768 onwards). Their colors are the last battler palette,
entry 240 onwards, and that is why a troop shows seven distinct battlers at
most. See `battle.rs` in `rm2k-snes-screens` and `ba_win_tick` in
`tools/runtime/battle_scene.s`.

**Mode 1 in the bottom strip was ruled out, without writing it.** It asks
for a BG1 palette between 0 and 7, and in battle they are all taken: 0 and
1 are the text's and 2 to 7 are the 96 colors of the backdrop, which are
still on screen while the strip is drawn. In 8bpp a pixel is its CGRAM
entry, and the last battler palette is spare. With mode 3 there is no need
to change the mode or the bases by HDMA: the only thing that goes by HDMA,
channel 5, is BG1's horizontal scroll per strip, so that the screen shake
moves the scene and not the windows.

**The text has 255 pairs**, from word 0 to `$1FFF`. From the morning of
2026-10-04 until that afternoon they were 447, up to the scene's tilemap,
because the skill list over the scene, with the party and the commands
below, used up the 191 that `SLOT_VRAM` left, and later the 255 with
`letter_spacing` 2. With the windows in the strip the battle writes much
less —the description and five lines— and the converter warns against the
255. Word 0 is the transparent tile of the scene and the blank pair of the
text at the same time: see `battle_bank_upload` in
`tools/runtime/screen_bank.s`.
