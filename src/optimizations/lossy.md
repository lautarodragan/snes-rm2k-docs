# Lossy optimizations

What **trades fidelity for fit**: something RM2k draws or plays is drawn
or played a little differently so that the game fits the console. The
rule behind all of them is in [When a game doesn't fit](../fitting.md):
lose the least, say so, and keep building. Each one warns in the build
when it applies, and what each map lost is in the converter's log or in
the game's `build/<cartridge>/adeleine/` images.

## Colours

### Adeleine merges the least visible colours

A map or a System with more colours than its palettes hold has its least
visible colours merged into their nearest, by how many pixels each covers.
A lone tile with more than fifteen colours cannot fit a 4-bit palette
however many there are, so this is the only way out for it.

- **Loses**: a shade here and there, chosen where it covers the fewest
  pixels.
- **Where**: `reduce_colors` in `snes/adeleine/src/pack.rs`; what it
  decided stays in the game's patches.
- **More**: [When a game doesn't fit](../fitting.md),
  [The CGRAM split](../internals/cgram.md).

### The message window takes its colours from every background

The message window lives in CGRAM palette 0, which in mode 3 is also the
background's, so its colours —background, frame, text, shadow, the arrow
and the cursor— come out of every map's budget, and a map that needed
those entries merges colours.

- **Loses**: on some maps, a shadow takes the shade next to it.
- **Where**: `window_colors`, counted by `rm2k-snes-screens window`;
  `cgram_reserved` in `rm2k-snes/wally/src/background/layers.rs`.
- **More**: [The window takes thirteen colors from every background](../divergences/the-window-takes-thirteen-colors-from-every-background.md).

### An event without a palette borrows one

Every event is drawn: one that does not get its own palette takes the one
it is missing the fewest colours from, each missing colour going to the
nearest by luma.

- **Loses**: some colours of the borrowing graphic.
- **Where**: `drawable_npcs` in `rm2k-snes/wally/src/sprites/split.rs`.
- **More**: [Every event is drawn](../decisions/every-event-is-drawn.md),
  [A graphic that doesn't fit isn't drawn](../decisions/a-graphic-that-doesnt-fit-isnt-drawn.md).

### The timer borrows a character's palette

The timer's digits go into the palette of a character with thirteen
colours or fewer; on a full map a character is lowered to fourteen, and if
not even that, the timer is lent the palette whose colours change the
digits the least.

- **Loses**: the colours the character shares with the digits go untinted
  while the timer is visible; in the last case, the digits' exact colours.
- **Where**: `drawable_npcs` in `rm2k-snes/wally/src/sprites/split.rs`,
  `timer_digits` in `rm2k-snes/wally/src/sprites/extras.rs`;
  `upload_timer_pal` in `runtime/tint.s`.
- **More**: [The timer has no palette of its own](../decisions/the-timer-has-no-palette-of-its-own.md),
  [The timer and its neighbor share colors](../divergences/the-timer-and-its-neighbor-share-colors.md).

### Seven palettes on a map with battle animations

The battle animation's box needs a sprite palette to itself, so on maps
that show animations the characters share seven.

- **Loses**: a merged colour or two in those maps' characters.
- **Where**: `palette_cap` in `rm2k-snes/wally/src/map.rs`.
- **More**: [Seven palettes on a map with animations](../divergences/seven-palettes-on-a-map-with-animations.md).

## Tiles

### Similar background tiles are fused, as a last resort

A map with more distinct tiles than any VRAM layout holds has its most
similar tiles fused until it fits, only after everything else that could
make room.

- **Loses**: detail where two tiles were almost the same.
- **Where**: `fuse_lower` in `rm2k-snes/wally/src/background/fuse.rs`,
  over Adeleine's `snes/adeleine/src/fuse.rs`.
- **More**: [When a game doesn't fit](../fitting.md).

### A window with a gradient is fused until it fits

A System whose stretched background is a gradient is a different cell on
every row of every window. The message window fuses the background seen
through its frame into bands; the screens that cut their windows into a
bank merge their least visible cells one at a time until the bank holds
them; End Game merges colours.

- **Loses**: the gradient goes in bands, first where it shows least.
- **Where**: `fit_frame` in `rm2k-snes/screens/src/message_window.rs`,
  `fit.rs` and `end_game.rs` in `rm2k-snes/screens/`; Adeleine's
  `group_tiles`, `merge_least_visible_tiles` and `merge_until`.
- **More**: [A window with a gradient is fused until it fits](../decisions/a-window-with-a-gradient-is-fused-until-it-fits.md).

### The windows' background, a colour of the project's

A game can fill a System's windows with one colour —or a vertical
gradient— of its own: each window's inside is then one cell and one CGRAM
entry, and nothing has to be fused. It is the game's choice, per System.

- **Loses**: what the System's background had besides its colours —a
  dither, a stroke near the edges—; a gradient is drawn as its average
  until the runtime draws gradients.
- **Where**: `windows.rs` in `rm2k-snes-project`; `--window-background` in
  `rm2k-snes-screens`.
- **More**: [The windows' background is the project's, by System](../decisions/the-windows-background-is-the-projects-by-system.md),
  [The windows, made cheaper](../research/2026-10-11-the-windows-made-cheaper.md).

### A panorama's similar tiles are grouped

A panorama brings far more distinct tiles than its layer has room for, so
similar ones are drawn with a single one; at 4 or 2 bits its colours are
merged too.

- **Loses**: the grain, slightly; at 2 bits, gradients flatten.
- **Where**: `group_tiles` in `snes/adeleine/src/tiles.rs`, used by
  `rm2k-snes/wally/src/background/panorama.rs`.
- **More**: [Panoramas](../research/2026-10-05-panoramas.md).

### A ChipSet animation that does not fit in WRAM stands still in part

The drawings of the water and the animated tiles have a fixed WRAM area;
a map whose drawings take more keeps moving the tiles that cover the most
cells, and the rest stay on their first drawing.

- **Loses**: some water cells stand still, mostly at the edges.
- **Where**: `rm2k-snes/mapdata/src/animation.rs`; `ANIM_DRAWINGS` in
  `runtime/far_ram.s`.
- **More**: [A ChipSet animation that does not fit in WRAM](../divergences/a-chipset-animation-that-does-not-fit-in-wram.md).

## Events

### Translucent events are baked

The blend of a translucent page is computed in the converter against the
layer below its cell and stays in the graphic: no colour math, no
dithering.

- **Loses**: nothing is seen through them; over an animated tile the
  blend is right for one frame; two over different backgrounds are two
  graphics.
- **Where**: `rm2k-snes/wally/src/sheets.rs`, with `translucent` from
  `rm2k-render`.
- **More**: [Translucent events are baked](../decisions/translucent-events-are-baked.md),
  [Translucent events end up opaque](../divergences/translucent-events-end-up-opaque.md).

### Decorative events become background

With `[graphics] decorative_events`, an event that is only a drawing is
painted into the background and stops being an event.

- **Loses**: its animation follows the ChipSet water's rhythm and phase;
  a translucency that does not fit gets dithered; blocking moves to the
  grid.
- **Saves**: sprite tiles, rows and slots.
- **Where**: `rm2k-snes/wally/src/decor.rs`.
- **More**: [Baked decorative events](../divergences/baked-decorative-events.md).

### More than four still events that animate

A still event that animates needs all twelve of its poses, like a walker.
Past a cap per map, none of that map's still events animate.

- **Loses**: on those maps, still events stand still.
- **Where**: `animates_still` in Wally, `rm2k-snes/wally/src/sprites/npc.rs`.
- **More**: [More than four still events that animate](../divergences/more-than-four-still-events-that-animate.md).

## Pictures and animations

### Battle animations on the map, shrunk to a box

A battle animation on the map is shrunk, whole and keeping its
proportions, to a 64x64 box, and without alpha: an object is opaque or not
there. If the space they need in the sprite bank is the only thing that
does not fit, the map is built without them.

- **Loses**: big animations look small; a fading cell disappears at once.
- **Where**: `fit_size` in `rm2k-snes/images/src/animation.rs`.
- **More**: [The shrunk battle animation](../divergences/the-shrunk-battle-animation.md),
  [When a game doesn't fit](../fitting.md).

### Pictures in sprites: scaled, fifteen colours

A small `ShowPicture` picture goes in sprites, with one sprite palette, and
one tied to the screen is scaled from RM2k's 320x240 to the console's
256x224.

- **Loses**: gradients band; the scaling; transparency in three steps.
- **Where**: `rm2k-snes/images/src/show_picture.rs`; `runtime/picture.s`.
- **More**: [What pictures as sprites do not model](../divergences/what-pictures-as-sprites-do-not-model.md).

### Big pictures in mode 1, 105 colours

A picture that covers the screen goes in BG1 at 4 bits, in seven palettes
of fifteen that Adeleine distributes per 8x8 cell.

- **Loses**: gradients in photos.
- **Where**: `rm2k-snes/images/src/fullscreen.rs`; `runtime/big_picture.s`.
- **More**: [What large pictures do not model](../divergences/what-large-pictures-do-not-model.md),
  [Large pictures in mode 1](../decisions/large-pictures-in-mode-1.md).

### The zoom in mode 7, with a 255-tile texture

A big picture that a `MovePicture` scales does the zoom in mode 7, whose
texture holds 256 tiles: each place in the picture shows the closest of
them. Still, it is shown at full resolution in mode 1.

- **Loses**: during the zoom, noisy photos show pieces of other tiles, and
  the grain flickers as it shrinks.
- **Where**: `runtime/big_picture_zoom.s`; `rm2k-snes/images/`.
- **More**: [What large pictures do not model](../divergences/what-large-pictures-do-not-model.md).

### The title at 16 colours a tile when it does not fit

If the title's picture does not fit in VRAM next to the menu at 8 bits, it
goes at 4 bits in mode 1, in seven palettes Adeleine chooses for it, where
it always fits.

- **Loses**: colours of the title picture.
- **Where**: `compressed_4bpp` in `rm2k-snes/convert/src/fullscreen.rs`;
  `title_upload` in `runtime/title.s`.
- **More**: [The VRAM split](../internals/vram.md#the-title-screen-doesnt-use-the-layout).

### Light battle backdrops in the ROM

The ROM carries the backdrops at half size and 4 bits, 16 colours, which
the console doubles; the `.msu` carries them whole, at 8 bits.

- **Loses**: without MSU-1, the backdrops' resolution and colours.
- **Where**: `scene.rs` in `rm2k-snes-convert`.
- **More**: [The `.msu` file](../internals/the-msu-file.md).

## Audio

### Each sample at the rate its worst package allows

Each package with its effects has to fit in the 64 KB of ARAM, so a sample
gets the rate its fullest package leaves; where a package lacks some of
the tracks that use a sample, those play a copy that does not pay for it.

- **Loses**: instrument brightness where packages are full.
- **Where**: `allocate` and `copies` in `bank.rs` of
  `rm2k-snes/rm2k-snes-audio/`.
- **More**: [A single sample bank](../decisions/a-single-sample-bank.md).

### Past 256 samples, the least used are dropped

The SPC700 indexes its samples with one byte; past that, the least used
are dropped and the notes that needed them are silent.

- **Loses**: those notes.
- **Where**: `compile.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [When a game doesn't fit](../fitting.md).
