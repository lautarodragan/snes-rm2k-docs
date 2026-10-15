# Lossy optimizations

What **trades fidelity for fit**: something RM2k draws or plays is drawn
or played a little differently so that the game fits the console.

A game made for a PC asks for things a Super Nintendo doesn't have: more
colors in a window than a palette holds, more distinct tiles than video
memory, more sounds than the sound chip can index. The tools treat each of
those limits the same way: **lose the least, say so, and keep building**.
The build prints a warning naming what was lost, and what was decided is
written down next to the game —the converter's log, the game's
`build/<cartridge>/adeleine/` images, its patches—, so it can be reviewed
and changed.

Refusing to build would be the safer-looking answer, and the worse one: a
game that runs with a missing effect can be played, measured and fixed; a
game that doesn't build can only be guessed about.

## What a game can choose

Some of those choices belong to the game, not the tools, and are knobs in
its `rm2k-snes.toml`:

- **Another System graphic**, when the game's own is not the one the port
  should show, or costs what the cartridge doesn't have: one from the
  game, from the RTP, or one made for the port.
- **A background of its own for a System's windows**, a colour or a
  gradient: see [the windows' background, a colour of the
  project's](#the-windows-background-a-colour-of-the-projects).
- **Decorative events as background**: see [decorative events become
  background](#decorative-events-become-background). It is off by default,
  because it changes how those maps are drawn.

What is left out of an event page that uses a command the console can't
run yet is not an optimization but a gap: it is in [The engine against
RPG Maker 2000](../progress/engine-vs-rm2k.md), and the converter's report
lists, for every map, which commands keep which pages out.

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
- **More**: [The CGRAM split](../internals/cgram.md).

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
  the principle; [A graphic that doesn't fit isn't drawn](../decisions/a-graphic-that-doesnt-fit-isnt-drawn.md).

### The timer borrows a character's palette

The timer has no palette of its own: its digits go into the palette of
any character that uses thirteen colours or fewer. Having one cost an
undrawn event on ABL's map 2 —the middle cell of the door Core breaks—.

On a map that fills the eight palettes at fifteen colours, room is made by
lowering a character to fourteen —the one that moves the fewest pixels,
never a leader, and only in a palette with a single character—. If not
even that is enough —every palette full, and each shared or lent—, the
timer is **lent** a palette, as an event is: the one whose nearest colours
change the digits the least, each glyph colour drawn with its nearest, and
the converter says which in a warning. It only stops if all eight palettes
are the leaders'.

Since the palette belongs to a character, the tint cannot skip it whole:
`upload_timer_pal` uploads untinted only the digits' entries, and only
while they are visible.

- **Loses**: the colours the character shares with the digits go untinted
  while the timer is visible; when lent, the digits' exact colours.
- **Where**: the end of `drawable_npcs` in
  `rm2k-snes/wally/src/sprites/split.rs`, `timer_digits` in
  `rm2k-snes/wally/src/sprites/extras.rs`; `upload_timer_pal` in
  `runtime/tint.s`.
- **More**: [The timer and its neighbor share colors](../divergences/the-timer-and-its-neighbor-share-colors.md);
  the idea of reserving a palette only while the timer runs, in the task
  [`timer-palette`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/timer-palette.md).

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
- **More**: [The VRAM split](../internals/vram.md).

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
- **More**: [A window with a gradient, fused until it fits](a-window-with-a-gradient.md).

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

### A map that shows its panorama gives up its layer above

In mode 3 the panorama takes BG2, which is where the layer above the hero
would go. A map that does draw something above the hero has it
**flattened**: what it draws there goes into the background, and the 8x8
cells it covers at least half of go to BG1's priority 1, in front of the
hero. A map that would put too much on the wrong side of the hero that way
goes in mode 1 instead: the map at 4 bits in BG1 and BG2 and the panorama
at 2 bits in BG3.

- **Loses**: flattened, the hero's depth against what is above him is
  decided per 8x8 cell, not per pixel; in mode 1, the map's colours go to
  4 bits per tile, and the panorama's to 2.
- **Where**: `Way::Flattened` and `Way::Mode1` in
  `rm2k-snes/wally/src/background/panorama.rs`; `ABOVE_LOST_MAX` in
  `rm2k-snes/wally/src/layers.rs`.
- **More**: [Mode 3 by default](../internals/mode-3.md),
  [Panoramas](../research/2026-10-05-panoramas.md).

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

The blend of a page's "Trans" —RM2k draws the event at 160 out of 255— is
computed in the converter against the layer below its cell and stays in
the graphic: no colour math, no dithering, no separate palettes. It can be
done exactly because the translucent pages A Blurred Line has are all
static —`move_type` 0 and no route of their own—: if neither the object
nor what is behind it moves, the blend always gives the same result.

The other two ways are not enough there. Colour math applies to every
sprite in palettes 4 to 7 at once, and was tried and left out —see [Tried
and left out](tried-and-left-out.md#colour-math-for-translucent-events)—.
Dithering, which is what games of the era did, does not simulate
transparency over a dark background: the fires on ABL's map 9 sit on
almost pure black, and dithering punches holes in the flame.

- **Loses**: nothing is seen through them; over an animated tile the
  blend is right for one frame; two over different backgrounds are two
  graphics. The CharSets in the project's `[graphics] opaque` —the save
  point— go opaque instead.
- **Where**: `decorate_translucent` in `rm2k-snes/convert/src/game.rs`,
  which names the graphic; `rm2k-snes/wally/src/sheets.rs`, which draws it
  with `translucent` from `rm2k-render`.
- **More**: [Translucent events end up opaque](../divergences/translucent-events-end-up-opaque.md),
  the divergence, with what was measured and when it stops being enough.

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
  [Seven palettes on a map with animations](../divergences/seven-palettes-on-a-map-with-animations.md).

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
- **More**: [A single sample bank](the-sample-bank.md).

### Past 256 samples, the least used are dropped

The SPC700 indexes its samples with one byte; past that, the least used
are dropped and the notes that needed them are silent.

- **Loses**: those notes.
- **Where**: `compile.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../internals/audio.md).

### A package that does not fit even at the minimum is relieved

A map whose package does not fit in the ARAM even with every sample at its
lowest rate —The Frozen World's map 1, with 41 sound effects and six
songs— is relieved instead of refused: its songs are uploaded when a
`PlayBGM` asks for them, with a pause, and the last effects of its list are
left out until the rest fits.

- **Loses**: a pause at those `PlayBGM`s, and the effects left out, each
  named in `degradations.json`.
- **Where**: `relief.rs` of `rm2k-snes/rm2k-snes-audio/`.
- **More**: [Audio](../internals/audio.md).

## Tables of a fixed size

### Graphics a move route switches to

A map holds a fixed number of the graphics move route command 34 switches
to; the rest are ignored.

- **Loses**: those changes of graphic.
- **Where**: `ROUTE_GFX_MAX` in `rm2k-snes/events/src/registry.rs` and, the
  same number, in `rm2k-snes/mapdata/src/record.rs`.
- **More**: [Move route command 34 on the hero](../decisions/move-route-command-34-on-the-hero.md).

### Variables

The console keeps a fixed number of variables, each with a one-byte slot.
Event pages that need one that didn't get a slot are left out, and the
build lists them.

- **Loses**: those pages.
- **Where**: `variable_slot` in `rm2k-snes/events/src/compile.rs`.
- **More**: [Variables saturate at sixteen bits](../divergences/variables-saturate-at-16-bits.md).

### A troop of more than eight enemies

A battle holds eight enemies: each takes a fixed place in the battle's far
RAM, and the hidden and scene masks are a byte per troop. A troop with
more is fitted to eight, leaving out first the members no page shows, then
those every page that shows them also kills; never one a page condition
or a branch asks about.

- **Loses**: those members, in the scenes the troop's pages play.
- **Where**: `fit.rs` of `rm2k-snes/battle/`.
- **More**: [A battle holds eight enemies](../divergences/a-battle-holds-eight-enemies.md).
