# Lossless optimizations

What saves ROM, RAM, VRAM, CGRAM, ARAM or CPU time **without changing
what is seen or heard**. Where an entry has a narrow exception —a case
where something does change— it says so; a full trade goes in
[Lossy](lossy.md).

## The map

### The 16x16 block grid

The map is not stored as a tilemap but as a grid of RM2k's 16x16 cells,
each pointing to a **block** that carries its four background cells, its
four cells of the layer above and its passability. Blocks repeat a lot,
and identical ones are stored once. Expanded, a big map's tilemap would
not fit in the cartridge at all.

- **Saves**: ROM —one grid entry per 16x16 cell instead of four tilemap
  entries per layer—; and since passability travels in the block, **the
  whole collision table** —one byte per cell— is gone.
- **Where**: `materials.rs` in `rm2k-snes/mapdata/`; the readers, `ptr_more`
  and `ptr_minus` in the runtime.
- **More**: [Maps](../internals/maps.md).

### A pointer that walks with the hero

Where the hero is in the grid is a 24-bit pointer that moves one cell or
one row per step, not an index: nothing multiplies or builds an address
from scratch, even though the grid crosses banks.

- **Saves**: CPU on every step and every passability question.
- **Where**: `ptr_more` and `ptr_minus`, the only routines that know how
  the grid crosses a bank.
- **More**: [Maps](../internals/maps.md).

### The grid, its blocks and the bytecode, in LZ2 and decompressed into WRAM

The grid travels in the cartridge as LZ2 and is decompressed whole into
the upper halves of the two WRAM banks when the map loads; the block
table, its passability and the event bytecode go right behind it, in the
same load. The upper half of two consecutive WRAM banks has the shape of
two LoROM banks, so the readers did not change.

- **Saves**: ROM, most of the grids' weight, keeping direct access cell
  by cell.
- **Costs**: 32 KB of far RAM in `$7E`, and the decompression on every map
  load and on returning from a battle.
- **Where**: `GRID` in `runtime/far_ram.s`, `lz2_grid` in
  `runtime/decompress.s`, `map_ram_pointers` in `record.rs` of
  `rm2k-snes/mapdata/`.
- **More**: [The grid lives in WRAM](the-grid-in-wram.md), with what it
  costs, how to know it needs reverting and how;
  [Maps](../internals/maps.md).

### The map's tiles in LZ2

The tiles of the background, of the layer above, of the sprite bank and
the drawings of the ChipSet animation travel as LZ2, are decompressed into
a WRAM buffer and uploaded with the same DMA as before. A background too
big for the buffer goes in two streams.

- **Saves**: ROM.
- **Where**: `materials.rs` in `rm2k-snes/mapdata/`; the format and the
  compressor, `snes/lz2/`; `lz2_backdrop` in `runtime/decompress.s`.
- **More**: [Maps](../internals/maps.md), [The VRAM split](../internals/vram.md).

### Only the tiles the map draws go to VRAM

The ROM does not take the whole ChipSet to VRAM, as RM2k does, but the
unique 8x8 tiles of what the map draws: the converter renders the map and
takes the tiles from there. An expanded ChipSet is hundreds of 8x8 tiles,
and they do not fit in what is left for the background next to the
message window. Nothing changes on screen: each map draws as in RM2k.

On 2026-09-07, counting only the ids some map of ABL uses, `ChipSet3`
gave 420 tiles and `BLchp1` 523; map 1 drew 341 and map 2, 278, against
the 420 of the ChipSet they share, and the pool of the two, 437, fit in no
VRAM layout of that day. The full count is in [the study on RM2k graphics
on the SNES](../research/graphics-and-sound-from-rm2k-to-the-snes.md),
"Sharing tiles between maps".

- **Saves**: VRAM.
- **Costs**: two maps with the same ChipSet do not share their tiles,
  which would save cartridge bytes and the VRAM reload between them.
- **When it stops being enough**: a game whose maps use more distinct
  background tiles than any layout holds. No layout saves that: VRAM would
  have to be reloaded while the map scrolls, a different engine from this
  one —except for a painted map, below—.
- **Where**: Wally, `rm2k-snes/wally/`; the layout, `vram_layout` in
  `vram.rs` of `rm2k-snes/mapdata/`.
- **More**: [The VRAM split](../internals/vram.md).

### The VRAM layout is chosen map by map

There is no single split of the 64 KB that serves every map, so the
converter picks, for each map, the first of a fixed list of layouts where
its background, its sprites and its layer above fit, and emits the
register values ready-made. New layouts go at the end, so no map that
already fit changes.

- **Saves**: VRAM —each map gets the split it needs, within the
  hardware's alignments—.
- **Where**: `vram_layout` and `LAYOUT_WINDOW*` in `vram.rs` of
  `rm2k-snes/mapdata/`.
- **More**: [The VRAM split](../internals/vram.md).

### The CGRAM split is chosen map by map, background first

The lower half of CGRAM is shared by the 8-bit background and the 4-bit
layer above. The converter decides the cut for each map: the background
keeps the palettes it needs, and the layer above takes what is left.

- **Saves**: CGRAM —no fixed cut serves every map—; merging colours only
  where nothing else is left.
- **Where**: `convert_with` in `rm2k-snes/wally/src/background/layers.rs`.
- **More**: [The CGRAM split](../internals/cgram.md).

### Opaque fixed events baked into the map

An event drawn with a ChipSet tile that is also opaque and never moves is
painted into the map, and its row is hidden from the sprite pass.

- **Saves**: sprite tiles, OAM entries and CPU in `build_oam`.
- **Where**: `baking::bakeable` in Wally (`rm2k-snes/wally/src/baking.rs`);
  `build_oam` skips the hidden row.
- **More**: [Events](../internals/events.md).

### A painted map keeps only what the screen shows

A map whose panorama *is* the map goes in BG1 in mode 1, one tile per 8x8
cell, and VRAM holds only the cells the screen can show, in a ring of
slots that the camera fills as it moves. A spare row uploaded ahead keeps
the vblank short.

- **Saves**: VRAM —a painted map has far more distinct cells than any
  layout holds—.
- **Where**: `runtime/painted.s`, `paint_table` in `panorama.rs` of
  `rm2k-snes/mapdata/`. Only a cartridge with a painted map assembles it.
- **More**: [The VRAM split](../internals/vram.md#a-painted-map-keeps-only-what-the-screen-shows).

### A panorama gets only the layer it needs

For each map the tools choose how to show its panorama: not at all if it
is never seen, baked into the background if it does not move against the
map, in the second layer if the map draws little above the hero, or with
the map in mode 1 and the panorama on a third layer.

- **Saves**: VRAM and a background layer, in the maps that do not need
  one.
- **Where**: `Way` in `rm2k-snes/wally/src/background/panorama.rs`;
  `runtime/pano.s`.
- **More**: [Mode 3 by default](../internals/mode-3.md),
  [Panoramas](../research/2026-10-05-panoramas.md).

## Characters and sprites

### Poses are uploaded on the fly

One pose per character lives in VRAM; the twelve poses of each one that
changes pose live in the cartridge, and the current one goes up by DMA in
vblank, as FF5 does. Still characters share a slot per (CharSet, index,
pose). An RM2k character is 192 object tiles with every pose resident,
and the PPU addresses 512.

- **Saves**: VRAM.
- **Costs**: DMA in vblank, with a cap per frame; when the queue is full
  an NPC waits, never the hero.
- **Where**: `vram_queue`, `vram_queue_hero` and `vram_drain` in
  `runtime/load_graphics.s`.
- **More**: [Poses are uploaded on the fly](poses-on-the-fly.md).

### A pose goes up without its empty tiles

A pose is stored as a 16-bit mask of the 8x8 tiles that draw something,
and only those tiles. The slot remembers which of its tiles may hold
something, and the upload zeroes only those the old pose drew and the new
one does not.

- **Saves**: ROM —the padding of a 24x32 character in a 32x32 object, and
  the air above its head—; and fewer bytes per walking step in vblank.
- **Costs**: one word of bank 0's RAM per 32x32 block of the sprite bank.
- **Where**: `vram_drain` in `runtime/load_graphics.s`; `pose_record` in
  `rm2k-snes/mapdata/`.
- **More**: [Poses are uploaded on the fly](poses-on-the-fly.md#and-a-pose-goes-up-without-its-empty-tiles).

### Distant still characters take turns on one slot

On a map that fits in no VRAM layout, and only there, still characters
that no camera position shows together share a slot even with different
poses, and the pose of the one that comes on screen is uploaded.

- **Saves**: sprite VRAM on the maps that would not fit otherwise.
- **Where**: `plan_sharing` in `rm2k-snes/wally/src/map.rs`, `share_table`
  in `rm2k-snes/mapdata/`, `runtime/shared_poses.s`.
- **More**: [The VRAM split](../internals/vram.md#when-no-layout-is-enough-the-still-ones-take-turns).

### The sprite slots as a cache

On a map that does not fit even with turns, and only there, nobody owns a
slot: whoever comes on screen asks for one, and a slot not drawn for two
frames goes to the next. The exception: if the cache is full, the one
asking waits without being drawn until someone leaves the screen.

- **Saves**: sprite VRAM on crowded scenes.
- **Where**: `Mode::Cache` in `rm2k-snes/wally/src/map.rs`, `cache_table`
  in `rm2k-snes/mapdata/`, `runtime/cache_slots.s`.
- **More**: [The VRAM split](../internals/vram.md#when-not-even-taking-turns-is-enough-a-slot-cache).

### The possible leaders share one CGRAM slot

Only one leads at a time, so giving each possible leader a palette of
its own would keep it taken by someone who is not on screen: they share
one, and the console uploads the colours of whoever leads. The exception
is a leader who is also an NPC on that map —Kersh on ABL's maps 1 and 6,
Talan on 3—, who gets their own, because both rows are in use at once.

- **Saves**: sprite palettes.
- **Where**: `drawable_npcs` in `rm2k-snes/wally/src/sprites/split.rs`.
- **More**: [The possible leaders are an approximation](../decisions/the-possible-leaders-are-an-approximation.md),
  who counts as one.

### The graphics only the hero shows go in the leaders' slot

A graphic only the hero ever shows is drawn like a possible leader: in
the leaders' CGRAM slot, with colours of its own that the console uploads
when the hero takes it. Since 2026-10-11. "Only the hero" means no move
route gives it to an event: the graphics of `ChangeSpriteAssociation`, and
those of move route command 34 on the hero; the event compiler's scan says
which graphics a route gives an event (`graphics_on_events`), and the
converter hands the rest to Wally as `hero_graphics`. One that an event of
the map also draws as a page graphic is left out: that one needs its
colours in the map's palette.

Before, they were split among each map's eight sprite palettes like any
other graphic of command 34, and two things came out of that, measured on
Vampires Dawn on 2026-10-11: the cartridge carried **a pose bank per map**
for each of them —a pose bank is the twelve poses as one map quantized
them—, and they were seen with the wrong colours in most maps. In the
leaders' slot the bank is the same in every map, and they take no palette
from the map. On that day's emission request of Vampires Dawn: 1,498 pose
banks to 1,163, and the maps with some graphic drawn with someone else's
palette from 365 to 77.

- **Saves**: ROM —a pose bank for the whole cartridge instead of one per
  map— and sprite palettes in every map; and the graphic is seen with its
  own colours.
- **Where**: `own` in Wally, and the colours of every graphic of command
  34 that ends in a leaders' palette; `hero_colors` and `route_graphic` in
  `rm2k-snes/mapdata/`; `route_gfx_colors`, `hero_poses_of_graphic` in
  `runtime/party.s`, and `graphic_hero`, which runs `apply_tint`.
- **More**: [Move route command 34 on the hero](../decisions/move-route-command-34-on-the-hero.md).

### Finished routes give up their slot

The ROM has twelve slots for event routes. When none is free, the first
one whose route has finished goes to the event that asks: the cap is
twelve moving at once, not twelve on the whole map.

- **Saves**: bank 0 RAM, which is full.
- **Where**: `reclaim_slot` in `runtime/event_pages.s`.
- **More**: [Finished routes give up their slot](../divergences/finished-routes-give-up-their-slot.md).

### Battle animations: one box for the whole ROM

A battle animation on the map is drawn in a box that is the same for
every map —a row of the sprite bank, four 32x32 objects—, so its frames
are converted once and every map that shows it shares them in the
cartridge. What the box costs in fidelity is in
[Lossy](lossy.md#battle-animations-on-the-map-shrunk-to-a-box).

- **Saves**: ROM —one copy of each animation's frames, not one per map—.
- **Where**: `rm2k-snes/convert/src/animations.rs`.
- **More**: [The shrunk battle animation](../divergences/the-shrunk-battle-animation.md).

## Events

### A common event's shared body, called with `OP_CALL`

A common event called from the foreground has one body in the cartridge,
called with `OP_CALL` instead of pasted in place, when the body compiled
with the map is byte for byte the one without it.

- **Saves**: ROM and WRAM —a deep chain of calls pasted in place does not
  fit at all—.
- **Where**: `OP_CALL` in `rm2k-snes/bytecode/src/events.rs` and its
  `op_call` in the interpreter; `refresh` in `compile.rs` of
  `rm2k-snes/events/`.
- **More**: [CallEvent: a shared body, or pasted in place](common-event-calls.md).

### `CallEvent` pasted in place, with no interpreter stack

What does not go to a shared body —parallel pages, bodies that depend on
the map, calls to map events— is pasted in place: the callee runs whole
before the caller continues, so no stack of interpreters is needed.

- **Saves**: RAM —no interpreter per call— and the cost of a call in
  parallel pages.
- **Where**: the event compiler, `rm2k-snes/events/`.
- **More**: [CallEvent: a shared body, or pasted in place](common-event-calls.md#pasted-in-place).

### Identical pages are stored once

Two pages of a map whose compiled bytecode is the same point at the same
code in the map's block, and so do two identical own routes: the page
table already carries a 24-bit pointer per page. A battle screen made of
one page per monster, all with the same commands, is the case it was made
for.

- **Saves**: WRAM, where the map's bytecode is decompressed; ROM only a
  little, because LZ2 already finds most of the repetition. How much, per
  map: the `map_code` table of the cartridge's `mapdata.inc`.
- **Only within a map**: each map's block is its own stream, decompressed
  alone.
- **Where**: `lay_out_code` in `convert.rs` of `rm2k-snes/convert/`.
- **More**: [Events](../internals/events.md); measured in
  [Frozen World's battle system](../research/2026-10-15-frozen-worlds-battle-system.md).

### The pure parallel common events run only when what they read changes

A parallel common event that only reads switches and equipment, and only
writes skills and the three permissions, runs when its switch turns on and
on the frame after something it reads or writes changes, instead of every
frame. Between those moments it would give the same result.

- **Saves**: CPU —a body that took about an eighth of the frame—.
- **Where**: `pure` in `rm2k-snes/events/src/commons.rs`; `compar_tick` in
  `runtime/common_events.s`.
- **More**: [The pure parallel common events run only when what they read changes](../divergences/pure-parallel-common-events-run-only-when-what-they-read-changes.md).

### The refresh runs at three moments

The active pages are recomputed when the interpreter lets go, at the
start of the frame, and the expensive half —OAM rows and route slots— on
the next frame; not before every command, as EasyRPG does, because no
opcode reads which page is active.

- **Saves**: CPU —it is what makes the frame fit in cutscenes that turn
  switches on by the bunch—.
- **Where**: `pick_pages` and `apply_pages` in `runtime/event_pages.s`.
- **More**: [The refresh runs at three moments](../decisions/the-refresh-runs-at-three-moments.md).

### One dispatch table for the opcodes

`run_code` dispatches with one `jmp (table, x)`, built from the bytecode's
declaration, instead of a chain of comparisons.

- **Saves**: CPU on every opcode.
- **Where**: the `EVENT_HANDLERS` macro, from `rm2k-snes/bytecode/src/events.rs`.
- **More**: [Events](../internals/events.md).

## Text and windows

### A repeated box is stored once

`OP_MESSAGE` carries an offset into one block of text for the whole
cartridge, not the text itself, so a box the game repeats —whole boxes
repeat often— is stored once: the content is the key.

- **Saves**: ROM in the messages.
- **Where**: `rm2k-snes/events/src/messages.rs`.
- **More**: [Events](../internals/events.md).

### DTE in the messages

The byte values the text never uses each stand for a pair of letters, one
level only, so a box is still read on its own.

- **Saves**: ROM in the messages.
- **Where**: `rm2k-snes/events/src/messages.rs`; the ROM side,
  `runtime/message_letter.s`.
- **More**: [Events](../internals/events.md),
  [The whole game without MSU-1](../ports/abl/research/2026-10-01-the-whole-game-without-msu-1.md).

### Glyphs pre-rendered in the cartridge

The variable-width font is stored already shifted to every phase of a
tile, so composing a letter is copying, not shifting pixels.

- **Saves**: CPU while text is written —it costs ROM instead—.
- **Where**: `font_prerender` in `rm2k-snes/screens/src/message_window.rs`;
  `compose_char` in `runtime/messages.s`.
- **More**: [Events](../internals/events.md).

### The message window's text area from one line

When every line of the message window's text area comes out the same, the
cartridge carries one line and `prime_line` copies it under each.

- **Saves**: ROM.
- **Where**: `prime_line` in `runtime/messages.s`.
- **More**: [The windows' background is the project's, by System](../decisions/the-windows-background-is-the-projects-by-system.md).

### One tilemap, two planes, placed by HDMA

The message window's tilemap holds two planes of ten rows —with frame and
without—, and HDMA says which one is seen and on which lines.

- **Saves**: VRAM —one 2 KB tilemap for every position and style of the
  window—.
- **Where**: `runtime/message_place.s`; `build_hdma` and `msg_hdma_build`.
- **More**: [The VRAM split](../internals/vram.md).

## Battle

### The scene and the windows are one layer

In battle the scene and the windows share BG1 in mode 3, the windows in
the rows below the scene, so only BG1's horizontal scroll goes by HDMA and
no mode or base changes mid-frame.

- **Saves**: VRAM and HDMA channels.
- **Where**: `battle.rs` in `rm2k-snes/screens/`; `ba_win_tick` in
  `runtime/battle_scene.s`.
- **More**: [The VRAM split](../internals/vram.md#battle-doesnt-use-the-layout).

### Each distinct troop page once

A game copies its battle systems' pages into every troop, so the troops'
pages are compiled and deduplicated by their bytecode: each distinct body
is stored once, and every troop that has it points to it.

- **Saves**: ROM in the troops' bytecode.
- **Where**: `rm2k-snes/events/src/troops.rs`.
- **More**: [What troop pages do not model](../divergences/what-troop-pages-do-not-model.md).

### The battlers and the light backdrops in LZ2

The troop's battlers and the backdrops the ROM carries travel as LZ2 and
are decompressed when the battle starts.

- **Saves**: ROM.
- **Where**: `rm2k-snes/convert/src/scene.rs`; `runtime/battle_scene.s`.
- **More**: [The `.msu` file](../internals/the-msu-file.md#what-does-not-fit-in-the-rom).

### Encounters and experience, precomputed

The encounter odds are integer arithmetic the converter prepares: the
reciprocal of each map's `encounter_steps`, in 1/65536, and the step at
which each row of the table is crossed; the ROM does not divide. And a
victory's experience comes summed per troop, since every enemy in a
victory is dead.

- **Saves**: CPU —no division on the console—.
- **Where**: `base` and `step_thresholds` in
  `rm2k-snes/battle/src/encounters.rs`, read by `runtime/encounters.s`;
  `troop_exp` in `rm2k-snes/battle/src/rules.rs`, read by `ba_exp_allocate`
  in `runtime/battle_loop.s`.
- **More**: the comments of those routines.

### The battlers in the grid's half of `$7E`

The troop's battlers are decompressed into the half of `$7E` the grid
uses, since `back_from_battle` decompresses the grid again anyway.

- **Saves**: far RAM.
- **Where**: `SCN_BATTLERS` in `runtime/battle_scene.s`.
- **More**: [The grid lives in WRAM](the-grid-in-wram.md#what-is-lost).

## Audio

### The stream is per note, with repeats

A theme travels as notes, releases and waits, which the 65816 expands
into DSP writes; what a theme plays the same is said once with an
`OP_REPEAT` that goes back and reads the bytes again.

- **Saves**: ROM in the music.
- **Where**: "the per-note format" and "repeats" in `stream.rs` of
  `rm2k-snes/rm2k-snes-audio/`; `irq_music` in `runtime/music.s`.
- **More**: [Audio](../internals/audio.md).

### A note names its sound in one byte

A note names its sound by an index into the theme's table of sounds, and
a theme with more than 256 pages through them with `OP_SOUND_PAGE`.

- **Saves**: ROM in the music.
- **Where**: `stream.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../internals/audio.md).

### A single sample bank, uploaded in packages per map

The tracks share one sample per General MIDI program and per drum hit,
and what goes to the ARAM is a package per map: each package with its
effects has to fit in the 64 KB, not the whole bank.

- **Saves**: ROM and the one-byte SRCN; the ARAM is spent on what the map
  plays.
- **Where**: `Bank` and `allocate` in `bank.rs` of
  `rm2k-snes/rm2k-snes-audio/`; `package_load` in
  `runtime/audio_package.s`.
- **More**: [A single sample bank](the-sample-bank.md).

### Effects share places in the directory

Two sound effects that never go in the same package go to the same place
in the SPC700's directory, so the directory needs as many effect places as
the fullest package has effects.

- **Saves**: directory entries, which are one byte's worth.
- **Where**: `effect_places` in `bank.rs`; `record_effect` in
  `runtime/audio_package.s`.
- **More**: [Audio](../internals/audio.md).

### Identical samples share their entry

Two keys whose samples come out the same —the same BRR and loop— are
stored and uploaded once.

- **Saves**: ROM and directory entries.
- **Where**: `Bank::directory` in `bank.rs` and `merge_identical` in
  `compile.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../internals/audio.md).

### With MSU-1, the themes with a track upload no samples

A package does not upload the samples of the themes the MSU-1 plays,
unless the track is missing from the card; the effects then get the ARAM
the music left.

- **Saves**: ARAM and loading time.
- **Where**: `song_per_msu` in `runtime/audio_package.s`;
  `rates_per_package` in `effects.rs`.
- **More**: [Audio](../internals/audio.md), [The `.msu` file](../internals/the-msu-file.md).

### Boot is sized for the boot package

Boot waits for loading the map, the driver and the directory through the
IPL, and the boot map's audio package, with a margin —not for a full
ARAM—. Since the per-map packages, the IPL uploads only the driver and the
directory, and the samples go through the driver's command 3, three bytes
at a time, so what goes up at power-on is a single package and boot can
be measured against it. It replaced a boot sized for the ARAM ceiling,
which froze the map at power-on for almost two seconds.

**Each cartridge carries its own** `BOOT_FRAMES`, since 2026-10-11: the
estimate for its boot package, or `BOOT_FRAMES_FLOOR`, whichever is
larger. The floor keeps a cartridge with a small package on the frame it
always started on, with a byte-for-byte identical ROM; it lives in the
runtime and not in each game's project because what it protects is the
runtime's —the loop starting on the same frame whatever small data goes
in—. The only ceiling left is the byte the ROM counts boot frames in.

- **Saves**: frames at power-on.
- **Costs**: if the boot map's package grows, that cartridge's boot grows
  with it, by itself. The tests read it from the symbol table, so it moves
  no golden.
- **Where**: `boot_frames` in `rm2k-snes/rm2k-snes-audio/src/emit.rs`,
  which `rm2k-snes-audio cartridge` writes into the cartridge's
  `musicdata.inc`; `BOOT_FRAMES_FLOOR` in `runtime/far_ram.s`.
- **More**: [Audio](../internals/audio.md).

## CPU time in the frame

### The hottest NPC code in bank 1, unrolled

What runs for every NPC row on every frame lives in bank 1, run from the
fast mirror, because bank 0 had no room to make it faster: hiding the 128
objects at the start of each frame is unrolled, and a row that moved is
moved to its place in the sorted table in one search and one block move
—`mvn`/`mvp`—, instead of re-sorting the table or swapping one place at a
time.

- **Saves**: scan lines of every frame, on every map.
- **Where**: `oam_hide` and `fit_far` in `runtime/far_npcs.s`.
- **More**: the header of `runtime/far_npcs.s`.

### The tint's tables are copied, not rebuilt

While a flash lasts, the palette is rebuilt every frame; the tint's three
channel tables —products and divisions— are kept in a pristine copy and
restored by copying it, and the flash's own table saves the tint's
computation per entry. A picture's tint reuses the same tables and
restores them the same way.

- **Saves**: CPU on every frame of a flash or a tinted picture.
- **Where**: `tint_tables`, `restore_tables` and `flash_channel_table` in
  `runtime/character_flash.s`; `pic_palette` in `runtime/picture.s`.
- **More**: the comments of those routines.

### A DSP write the register already has is skipped

The music decoder keeps a copy of what it wrote to each DSP register, and
does not write again a value the register already holds.

- **Saves**: writes through the SPC700's ports, every music frame.
- **Where**: `mus_write` and `MUS_SHADOW` in `runtime/music.s`.
- **More**: [Audio](../internals/audio.md).

## The cartridge

### Identical blocks are stored once

Every data block the converter emits —tiles, grids, block tables,
bytecode, and the rest— has an identity of its own, `<class>_<n>`, and
the map stores which one it points to: two maps with the same bytes in a
class share the block.

- **Saves**: ROM, wherever maps repeat data.
- **Where**: `Materials::store` in `rm2k-snes/mapdata/src/materials.rs`.
- **More**: [Graphics and sound, from RM2k to the SNES](../research/graphics-and-sound-from-rm2k-to-the-snes.md).

### Tables of pointers, stored once by their text

A table whose bytes are pointers the linker sets cannot be compared by
its bytes, so it is shared by its text, which names the same labels when
it points to the same things. The per-map leader table and the per-map
table of the poses of each character that changes pose go this way: most
maps bring one another map already brought.

- **Saves**: ROM.
- **Where**: `Materials::store_text` and `Materials::store_symbolic` in
  `rm2k-snes/mapdata/src/materials.rs`; `actor_table_asm` and
  `npc_poses_asm` in `record.rs`.
- **More**: [Fitting the whole game in 8 MB](../ports/abl/research/2026-10-14-fitting-the-whole-game-in-8-mb.md),
  the research that measured them.

### The fast half first

Only the first 4 MB of an ExHiROM cartridge are FastROM, so the packer
fills those first.

- **Saves**: CPU on reads from ROM.
- **Where**: `banks.rs` in `rm2k-snes/cartridge/src/`.
- **More**: [ExHiROM, 8 MB](../internals/exhirom.md).

### What does not fit, in the `.msu`

A game whose ROM does not reach declares `[rom] msu = "required"`, and the
data read when a map or a battle loads —LZ2 streams, panorama and picture
tiles, samples— travels in the `.msu`. Nothing is lost, but the game needs
the MSU-1.

- **Saves**: ROM.
- **Where**: the `.msu` in front of a `.block`, marked by each emitter;
  `lz2_msu` and `msu_dma0` in `runtime/decompress.s`.
- **More**: [The `.msu` file](../internals/the-msu-file.md#what-does-not-fit-in-the-rom),
  [The MSU-1 is required only when the ROM does not reach](../decisions/the-msu-1-is-required-only-when-the-rom-does-not-reach.md).
