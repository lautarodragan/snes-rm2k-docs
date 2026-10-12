# When a game doesn't fit

A game made for a PC asks for things a Super Nintendo doesn't have: more
colors in a window than a palette holds, more distinct tiles than video
memory, more sounds than the sound chip can index. The tools treat each of
those limits the same way: **lose the least, say so, and keep building**.
The build prints a warning naming what was lost, and what was decided is
written down next to the game, so it can be reviewed and changed.

Refusing to build would be the safer-looking answer, and the worse one: a
game that runs with a missing effect can be played, measured and fixed; a
game that doesn't build can only be guessed about.

## What gives way

- **Colors.** A window skin (the *System* graphic) or a map with more
  colors than its palettes hold has its least visible colors merged into
  their closest neighbors. Adeleine chooses which ones, by how many pixels
  each color covers, and those merges are saved with the game as patches,
  so a change in what is lost shows up in its history.
- **Window tiles.** A System whose stretched background is a gradient is
  a different cell on every row of its windows, more than their banks of
  tiles hold. The message window has the background seen through its frame
  fused into bands; the screens that cut their windows into a bank have
  their least visible cells merged, one at a time, until it holds them —see
  [A window with a gradient is fused until it fits](decisions/a-window-with-a-gradient-is-fused-until-it-fits.md)—.
- **Background tiles.** A map with more distinct tiles than any layout of
  video memory can hold has its most similar tiles fused until it fits.
  It is the last resort, tried only after everything else that could make
  room.
- **Battle animations on a map.** If the space they need in the sprite
  bank is the only thing that doesn't fit, the map is built without them.
- **Samples.** The sound chip indexes its samples with a single byte;
  past that, the least used are dropped, and the notes that needed them
  are silent.
- **The title screen.** If its picture doesn't fit in video memory next to
  the menu at 256 colours, it goes at 16 colours a tile, in seven palettes
  chosen for it, where it always fits.
- **Graphics a move route switches to.** A map holds a fixed number of
  them; the rest are ignored.
- **Variables.** The console keeps a fixed number of them. Event pages
  that need one that didn't get a slot are left out, and the build lists
  them.

## What a game can choose

Some of those choices belong to the game, not the tools, and are knobs in
its `rm2k-snes.toml`:

- **Another System graphic**, when the game's own is not the one the port
  should show, or costs what the cartridge doesn't have: one from the
  game, from the RTP, or one made for the port.
- **Decorative events as background.** Events that only exist to be
  looked at —one page, no commands, never moved— can be painted into the
  background instead of using sprites. It is off by default, because it
  changes how those maps are drawn.

## What is left out of an event page

An event page that uses a command the console can't run yet is either
compiled without that detail, declared as debt, or left out entirely. A
report lists, for every map, which commands keep which pages out: it is
the list of what to build next.
