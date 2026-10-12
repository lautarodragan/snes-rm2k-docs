# `ChangeSystemGraphics` changes the message window

## What

**`ChangeSystemGraphics` switches the message window to the System it
names, and nothing else.** From then on its frame, its background —the
project's `[windows.background]` for that System, if it has one—, its text
colours, its arrow and a choice's bar are the new System's, and the System
travels in the save, as in RM2k. The pause menu, the slot screen, the item,
equipment and shop screens, End Game, the battle's windows and the title
keep the System the game starts with. Since 2026-10-12, the first version
of what taro asked for: "podríamos implementar ChangeSystemGraphics y verlo
andar (con distintos colores planos)?".

Two rules about colour come with it:

* **The text takes the same palette entries in every System.** Each glyph
  row gets one entry, split as finely as any of the Systems splits its
  text gradient; a System whose text is one colour repeats it in each.
* **A System the game switches to fits in the entries the starting one
  takes.** If it brings more —its frame, its cursor, its text—, it is
  reduced like any window that does not fit, and what it lost goes to the
  game's patches.

## Why

**The message window is what a switch is for, and it is cheap.** Of the
three games that switch, Sunset Over Imdahl and Desert Nightmare do it to
change how their dialogue looks, and Vampires Dawn does it around its
signs and graves and to let the player pick a style for its messages. Each
System's window is a few frame tiles, a palette, its two planes of cells
and the text area's background and bar: some 14.6 KB of ROM when its text
area is one colour —20 KB when it is not—, 26 bytes of far RAM for the
whole cartridge, and about a window line of DMA in the vblank after the
command. The other screens
are drawn into their banks once, by the converter, each with its own
palettes and tiles; carrying them once per System is the whole screens
stage again per System, and it was left for when a game needs it.

**One set of text entries, because the font's composed tables carry
indices and not colours.** They are eight tables of some 14 KB each, one
per position a letter can start at in a cell —`font_prerender`—, and with
the text at the same entries in every System they are carried once: a
System is then only its palette and its tiles. The price is entries: a
starting System whose text is one colour takes one more for each class of
rows the other splits it into. Sunset Over Imdahl's `System`, whose text
is black, went from 7 entries to 14 against `SaveMeny`'s gradient: the
five of its 65 maps that are not painted have seven colours fewer.

**The starting System's count, because the maps start right after the
window.** Every map's background is placed from `CGRAM_BASE` up, and its
patches —which colour was merged with which— are decided with it. If a
second System could grow the window, a game that adds one switch would
change every map's colours, and A Blurred Line's suite would see its map
patches move for a test cartridge. Reducing the second System loses a few
of its frame's colours, once, where the switch is.

## How it applies

* The converter lists the Systems: the starting one and every one a
  `ChangeSystemGraphics` of the cartridge's pages names, by name without
  regard to case —`systems.rs` in `rm2k-snes-convert`—; one the game and
  the RTP do not have is left out with a warning, and so is the page that
  asks for it.
* `rm2k-snes-screens window`, with the others in its request, answers the
  text rows, the count and each other System's window; `convert` draws the
  starting one with the same rows.
* The event compiler emits `OP_CHANGE_SYSTEM` with the System's index; a
  cartridge whose commands all name the starting System carries one window
  and the opcode changes nothing.
* The emission writes one window per System with the text area at the same
  tile —the largest frame's—, and `window_systems`, a pointer per piece and
  System. The runtime copies the current one's to `WINDOW_NOW` at each
  map's load and when the command runs, and everything that draws the
  window reads it —`window_system.s`—. A cartridge with one System
  assembles none of it.
* The command's stretch is heard once, from the first command that names
  the System; a System's background with an entry in `[windows.background]`
  is one colour and does not care. Its font parameter is not heard: the
  console has one font.
