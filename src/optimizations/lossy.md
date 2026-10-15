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
  project's](lossy/tiles.md#the-windows-background-a-colour-of-the-projects).
- **Decorative events as background**: see [decorative events become
  background](lossy/events.md#decorative-events-become-background). It is off by default,
  because it changes how those maps are drawn.

What is left out of an event page that uses a command the console can't
run yet is not an optimization but a gap: it is in [The engine against
RPG Maker 2000](../progress/engine-vs-rm2k.md), and the converter's report
lists, for every map, which commands keep which pages out.

One page per part of the port:

## [Colours](lossy/colours.md)

* [Adeleine merges the least visible colours](lossy/colours.md#adeleine-merges-the-least-visible-colours)
* [The message window takes its colours from every background](lossy/colours.md#the-message-window-takes-its-colours-from-every-background)
* [An event without a palette borrows one](lossy/colours.md#an-event-without-a-palette-borrows-one)
* [The timer borrows a character's palette](lossy/colours.md#the-timer-borrows-a-characters-palette)
* [Seven palettes on a map with battle animations](lossy/colours.md#seven-palettes-on-a-map-with-battle-animations)

## [Tiles](lossy/tiles.md)

* [Similar background tiles are fused, as a last resort](lossy/tiles.md#similar-background-tiles-are-fused-as-a-last-resort)
* [A window with a gradient is fused until it fits](lossy/tiles.md#a-window-with-a-gradient-is-fused-until-it-fits)
* [The windows' background, a colour of the project's](lossy/tiles.md#the-windows-background-a-colour-of-the-projects)
* [A panorama's similar tiles are grouped](lossy/tiles.md#a-panoramas-similar-tiles-are-grouped)
* [A map that shows its panorama gives up its layer above](lossy/tiles.md#a-map-that-shows-its-panorama-gives-up-its-layer-above)
* [A ChipSet animation that does not fit in WRAM stands still in part](lossy/tiles.md#a-chipset-animation-that-does-not-fit-in-wram-stands-still-in-part)

## [Events](lossy/events.md)

* [Translucent events are baked](lossy/events.md#translucent-events-are-baked)
* [Decorative events become background](lossy/events.md#decorative-events-become-background)
* [More than four still events that animate](lossy/events.md#more-than-four-still-events-that-animate)

## [Pictures and animations](lossy/pictures-and-animations.md)

* [Battle animations on the map, shrunk to a box](lossy/pictures-and-animations.md#battle-animations-on-the-map-shrunk-to-a-box)
* [Pictures in sprites: scaled, fifteen colours](lossy/pictures-and-animations.md#pictures-in-sprites-scaled-fifteen-colours)
* [Big pictures in mode 1, 105 colours](lossy/pictures-and-animations.md#big-pictures-in-mode-1-105-colours)
* [The zoom in mode 7, with a 255-tile texture](lossy/pictures-and-animations.md#the-zoom-in-mode-7-with-a-255-tile-texture)
* [The title at 16 colours a tile when it does not fit](lossy/pictures-and-animations.md#the-title-at-16-colours-a-tile-when-it-does-not-fit)
* [Light battle backdrops in the ROM](lossy/pictures-and-animations.md#light-battle-backdrops-in-the-rom)

## [Audio](lossy/audio.md)

* [Each sample at the rate its worst package allows](lossy/audio.md#each-sample-at-the-rate-its-worst-package-allows)
* [Past 256 samples, the least used are dropped](lossy/audio.md#past-256-samples-the-least-used-are-dropped)
* [A package that does not fit even at the minimum is relieved](lossy/audio.md#a-package-that-does-not-fit-even-at-the-minimum-is-relieved)

## [Tables of a fixed size](lossy/tables-of-a-fixed-size.md)

* [Graphics a move route switches to](lossy/tables-of-a-fixed-size.md#graphics-a-move-route-switches-to)
* [Variables](lossy/tables-of-a-fixed-size.md#variables)
* [A troop of more than eight enemies](lossy/tables-of-a-fixed-size.md#a-troop-of-more-than-eight-enemies)
