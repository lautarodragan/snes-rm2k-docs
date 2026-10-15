# Lossy: colours

## Adeleine merges the least visible colours

A map or a System with more colours than its palettes hold has its least
visible colours merged into their nearest, by how many pixels each covers.
A lone tile with more than fifteen colours cannot fit a 4-bit palette
however many there are, so this is the only way out for it.

- **Loses**: a shade here and there, chosen where it covers the fewest
  pixels.
- **Where**: `reduce_colors` in `snes/adeleine/src/pack.rs`; what it
  decided stays in the game's patches.
- **More**: [The CGRAM split](../../internals/cgram.md).

## The message window takes its colours from every background

The message window lives in CGRAM palette 0, which in mode 3 is also the
background's, so its colours —background, frame, text, shadow, the arrow
and the cursor— come out of every map's budget, and a map that needed
those entries merges colours.

- **Loses**: on some maps, a shadow takes the shade next to it.
- **Where**: `window_colors`, counted by `rm2k-snes-screens window`;
  `cgram_reserved` in `rm2k-snes/wally/src/background/layers.rs`.
- **More**: [The window takes thirteen colors from every background](../../divergences/the-window-takes-thirteen-colors-from-every-background.md).

## An event without a palette borrows one

Every event is drawn: one that does not get its own palette takes the one
it is missing the fewest colours from, each missing colour going to the
nearest by luma.

- **Loses**: some colours of the borrowing graphic.
- **Where**: `drawable_npcs` in `rm2k-snes/wally/src/sprites/split.rs`.
- **More**: [Every event is drawn](../../decisions/every-event-is-drawn.md),
  the principle; [A graphic that doesn't fit isn't drawn](../../decisions/a-graphic-that-doesnt-fit-isnt-drawn.md).

## The timer borrows a character's palette

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
- **More**: [The timer and its neighbor share colors](../../divergences/the-timer-and-its-neighbor-share-colors.md);
  the idea of reserving a palette only while the timer runs, in the task
  [`timer-palette`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/timer-palette.md).

## Seven palettes on a map with battle animations

The battle animation's box needs a sprite palette to itself, so on maps
that show animations the characters share seven.

- **Loses**: a merged colour or two in those maps' characters.
- **Where**: `palette_cap` in `rm2k-snes/wally/src/map.rs`.
- **More**: [Seven palettes on a map with animations](../../divergences/seven-palettes-on-a-map-with-animations.md).
