# Lossless optimizations

What saves ROM, RAM, VRAM, CGRAM, ARAM or CPU time **without changing
what is seen or heard**. Where an entry has a narrow exception —a case
where something does change— it says so; a full trade goes in
[Lossy](lossy.md).

One page per part of the port:

## [The map](lossless/the-map.md)

* [The 16x16 block grid](lossless/the-map.md#the-16x16-block-grid)
* [A pointer that walks with the hero](lossless/the-map.md#a-pointer-that-walks-with-the-hero)
* [The grid, its blocks and the bytecode, in LZ2 and decompressed into WRAM](lossless/the-map.md#the-grid-its-blocks-and-the-bytecode-in-lz2-and-decompressed-into-wram)
* [The map's tiles in LZ2](lossless/the-map.md#the-maps-tiles-in-lz2)
* [Only the tiles the map draws go to VRAM](lossless/the-map.md#only-the-tiles-the-map-draws-go-to-vram)
* [The VRAM layout is chosen map by map](lossless/the-map.md#the-vram-layout-is-chosen-map-by-map)
* [The CGRAM split is chosen map by map, background first](lossless/the-map.md#the-cgram-split-is-chosen-map-by-map-background-first)
* [Opaque fixed events baked into the map](lossless/the-map.md#opaque-fixed-events-baked-into-the-map)
* [A painted map keeps only what the screen shows](lossless/the-map.md#a-painted-map-keeps-only-what-the-screen-shows)
* [A panorama gets only the layer it needs](lossless/the-map.md#a-panorama-gets-only-the-layer-it-needs)

## [Characters and sprites](lossless/characters-and-sprites.md)

* [Poses are uploaded on the fly](lossless/characters-and-sprites.md#poses-are-uploaded-on-the-fly)
* [A pose goes up without its empty tiles](lossless/characters-and-sprites.md#a-pose-goes-up-without-its-empty-tiles)
* [Distant still characters take turns on one slot](lossless/characters-and-sprites.md#distant-still-characters-take-turns-on-one-slot)
* [The sprite slots as a cache](lossless/characters-and-sprites.md#the-sprite-slots-as-a-cache)
* [The possible leaders share one CGRAM slot](lossless/characters-and-sprites.md#the-possible-leaders-share-one-cgram-slot)
* [The graphics only the hero shows go in the leaders' slot](lossless/characters-and-sprites.md#the-graphics-only-the-hero-shows-go-in-the-leaders-slot)
* [Finished routes give up their slot](lossless/characters-and-sprites.md#finished-routes-give-up-their-slot)
* [Battle animations: one box for the whole ROM](lossless/characters-and-sprites.md#battle-animations-one-box-for-the-whole-rom)

## [Events](lossless/events.md)

* [A common event's shared body, called with `OP_CALL`](lossless/events.md#a-common-events-shared-body-called-with-op_call)
* [`CallEvent` pasted in place, with no interpreter stack](lossless/events.md#callevent-pasted-in-place-with-no-interpreter-stack)
* [Identical pages are stored once](lossless/events.md#identical-pages-are-stored-once)
* [The pure parallel common events run only when what they read changes](lossless/events.md#the-pure-parallel-common-events-run-only-when-what-they-read-changes)
* [The refresh runs at three moments](lossless/events.md#the-refresh-runs-at-three-moments)
* [One dispatch table for the opcodes](lossless/events.md#one-dispatch-table-for-the-opcodes)

## [Text and windows](lossless/text-and-windows.md)

* [A repeated box is stored once](lossless/text-and-windows.md#a-repeated-box-is-stored-once)
* [DTE in the messages](lossless/text-and-windows.md#dte-in-the-messages)
* [Glyphs pre-rendered in the cartridge](lossless/text-and-windows.md#glyphs-pre-rendered-in-the-cartridge)
* [The message window's text area from one line](lossless/text-and-windows.md#the-message-windows-text-area-from-one-line)
* [One tilemap, two planes, placed by HDMA](lossless/text-and-windows.md#one-tilemap-two-planes-placed-by-hdma)

## [Battle](lossless/battle.md)

* [The scene and the windows are one layer](lossless/battle.md#the-scene-and-the-windows-are-one-layer)
* [Each distinct troop page once](lossless/battle.md#each-distinct-troop-page-once)
* [The battlers and the light backdrops in LZ2](lossless/battle.md#the-battlers-and-the-light-backdrops-in-lz2)
* [Encounters and experience, precomputed](lossless/battle.md#encounters-and-experience-precomputed)
* [The battlers in the grid's half of `$7E`](lossless/battle.md#the-battlers-in-the-grids-half-of-7e)

## [Audio](lossless/audio.md)

* [The stream is per note, with repeats](lossless/audio.md#the-stream-is-per-note-with-repeats)
* [A note names its sound in one byte](lossless/audio.md#a-note-names-its-sound-in-one-byte)
* [A single sample bank, uploaded in packages per map](lossless/audio.md#a-single-sample-bank-uploaded-in-packages-per-map)
* [Effects share places in the directory](lossless/audio.md#effects-share-places-in-the-directory)
* [Identical samples share their entry](lossless/audio.md#identical-samples-share-their-entry)
* [With MSU-1, the themes with a track upload no samples](lossless/audio.md#with-msu-1-the-themes-with-a-track-upload-no-samples)
* [Boot is sized for the boot package](lossless/audio.md#boot-is-sized-for-the-boot-package)

## [CPU time in the frame](lossless/cpu-time-in-the-frame.md)

* [The hottest NPC code in bank 1, unrolled](lossless/cpu-time-in-the-frame.md#the-hottest-npc-code-in-bank-1-unrolled)
* [The tint's tables are copied, not rebuilt](lossless/cpu-time-in-the-frame.md#the-tints-tables-are-copied-not-rebuilt)
* [A DSP write the register already has is skipped](lossless/cpu-time-in-the-frame.md#a-dsp-write-the-register-already-has-is-skipped)

## [The cartridge](lossless/the-cartridge.md)

* [Identical blocks are stored once](lossless/the-cartridge.md#identical-blocks-are-stored-once)
* [Tables of pointers, stored once by their text](lossless/the-cartridge.md#tables-of-pointers-stored-once-by-their-text)
* [The fast half first](lossless/the-cartridge.md#the-fast-half-first)
* [What does not fit, in the `.msu`](lossless/the-cartridge.md#what-does-not-fit-in-the-msu)

<script>
// Until 2026-10-15 this was one page, and its anchors are linked from
// outside the book: each one goes on to the page it moved to.
const moved = {"a-common-events-shared-body-called-with-op_call": "events.html#a-common-events-shared-body-called-with-op_call", "a-dsp-write-the-register-already-has-is-skipped": "cpu-time-in-the-frame.html#a-dsp-write-the-register-already-has-is-skipped", "a-note-names-its-sound-in-one-byte": "audio.html#a-note-names-its-sound-in-one-byte", "a-painted-map-keeps-only-what-the-screen-shows": "the-map.html#a-painted-map-keeps-only-what-the-screen-shows", "a-panorama-gets-only-the-layer-it-needs": "the-map.html#a-panorama-gets-only-the-layer-it-needs", "a-pointer-that-walks-with-the-hero": "the-map.html#a-pointer-that-walks-with-the-hero", "a-pose-goes-up-without-its-empty-tiles": "characters-and-sprites.html#a-pose-goes-up-without-its-empty-tiles", "a-repeated-box-is-stored-once": "text-and-windows.html#a-repeated-box-is-stored-once", "a-single-sample-bank-uploaded-in-packages-per-map": "audio.html#a-single-sample-bank-uploaded-in-packages-per-map", "audio": "audio.html", "battle": "battle.html", "battle-animations-one-box-for-the-whole-rom": "characters-and-sprites.html#battle-animations-one-box-for-the-whole-rom", "boot-is-sized-for-the-boot-package": "audio.html#boot-is-sized-for-the-boot-package", "callevent-pasted-in-place-with-no-interpreter-stack": "events.html#callevent-pasted-in-place-with-no-interpreter-stack", "characters-and-sprites": "characters-and-sprites.html", "cpu-time-in-the-frame": "cpu-time-in-the-frame.html", "distant-still-characters-take-turns-on-one-slot": "characters-and-sprites.html#distant-still-characters-take-turns-on-one-slot", "dte-in-the-messages": "text-and-windows.html#dte-in-the-messages", "each-distinct-troop-page-once": "battle.html#each-distinct-troop-page-once", "effects-share-places-in-the-directory": "audio.html#effects-share-places-in-the-directory", "encounters-and-experience-precomputed": "battle.html#encounters-and-experience-precomputed", "events": "events.html", "finished-routes-give-up-their-slot": "characters-and-sprites.html#finished-routes-give-up-their-slot", "glyphs-pre-rendered-in-the-cartridge": "text-and-windows.html#glyphs-pre-rendered-in-the-cartridge", "identical-blocks-are-stored-once": "the-cartridge.html#identical-blocks-are-stored-once", "identical-pages-are-stored-once": "events.html#identical-pages-are-stored-once", "identical-samples-share-their-entry": "audio.html#identical-samples-share-their-entry", "one-dispatch-table-for-the-opcodes": "events.html#one-dispatch-table-for-the-opcodes", "one-tilemap-two-planes-placed-by-hdma": "text-and-windows.html#one-tilemap-two-planes-placed-by-hdma", "only-the-tiles-the-map-draws-go-to-vram": "the-map.html#only-the-tiles-the-map-draws-go-to-vram", "opaque-fixed-events-baked-into-the-map": "the-map.html#opaque-fixed-events-baked-into-the-map", "poses-are-uploaded-on-the-fly": "characters-and-sprites.html#poses-are-uploaded-on-the-fly", "tables-of-pointers-stored-once-by-their-text": "the-cartridge.html#tables-of-pointers-stored-once-by-their-text", "text-and-windows": "text-and-windows.html", "the-16x16-block-grid": "the-map.html#the-16x16-block-grid", "the-battlers-and-the-light-backdrops-in-lz2": "battle.html#the-battlers-and-the-light-backdrops-in-lz2", "the-battlers-in-the-grids-half-of-7e": "battle.html#the-battlers-in-the-grids-half-of-7e", "the-cartridge": "the-cartridge.html", "the-cgram-split-is-chosen-map-by-map-background-first": "the-map.html#the-cgram-split-is-chosen-map-by-map-background-first", "the-fast-half-first": "the-cartridge.html#the-fast-half-first", "the-graphics-only-the-hero-shows-go-in-the-leaders-slot": "characters-and-sprites.html#the-graphics-only-the-hero-shows-go-in-the-leaders-slot", "the-grid-its-blocks-and-the-bytecode-in-lz2-and-decompressed-into-wram": "the-map.html#the-grid-its-blocks-and-the-bytecode-in-lz2-and-decompressed-into-wram", "the-hottest-npc-code-in-bank-1-unrolled": "cpu-time-in-the-frame.html#the-hottest-npc-code-in-bank-1-unrolled", "the-map": "the-map.html", "the-maps-tiles-in-lz2": "the-map.html#the-maps-tiles-in-lz2", "the-message-windows-text-area-from-one-line": "text-and-windows.html#the-message-windows-text-area-from-one-line", "the-possible-leaders-share-one-cgram-slot": "characters-and-sprites.html#the-possible-leaders-share-one-cgram-slot", "the-pure-parallel-common-events-run-only-when-what-they-read-changes": "events.html#the-pure-parallel-common-events-run-only-when-what-they-read-changes", "the-refresh-runs-at-three-moments": "events.html#the-refresh-runs-at-three-moments", "the-scene-and-the-windows-are-one-layer": "battle.html#the-scene-and-the-windows-are-one-layer", "the-sprite-slots-as-a-cache": "characters-and-sprites.html#the-sprite-slots-as-a-cache", "the-stream-is-per-note-with-repeats": "audio.html#the-stream-is-per-note-with-repeats", "the-tints-tables-are-copied-not-rebuilt": "cpu-time-in-the-frame.html#the-tints-tables-are-copied-not-rebuilt", "the-vram-layout-is-chosen-map-by-map": "the-map.html#the-vram-layout-is-chosen-map-by-map", "what-does-not-fit-in-the-msu": "the-cartridge.html#what-does-not-fit-in-the-msu", "with-msu-1-the-themes-with-a-track-upload-no-samples": "audio.html#with-msu-1-the-themes-with-a-track-upload-no-samples"};
const to = moved[decodeURIComponent(location.hash.slice(1))];
if (to) location.replace('lossless/' + to);
</script>
