# What `ChangeSystemGraphics` does not model

## What

In RM2k, `ChangeSystemGraphics` changes the System of every window from
then on. The ROM changes **the message window's**: its frame, its
background, its text colours, its arrow and a choice's bar. What it does
not:

* **The other screens keep the starting System**: the pause menu, the slot
  screen, the item, equipment and shop screens, End Game, the battle's
  windows and the title's menu.
* **A switched-to System loses colours that the starting one does not**:
  it fits in the palette entries the starting one takes, with its text at
  the same entries, and what does not fit is merged —the converter writes
  it in the game's patches—. Royal against A Blurred Line's `ablskin`
  loses three, in its arrow and its corners.
* **Its stretch is heard once per System**, from the first command that
  names it; with a background in `[windows.background]` it makes no
  difference. **Its font parameter is not heard**: the console has one
  font.
* **A text row of more than one colour is drawn with the colour most of it
  has**: Vampires Dawn's `VDBlutsys2` has one.
* **A message window on screen at the moment of the switch** changes its
  frame and palette in the next vblank, and keeps the old System's
  background under the text it already composed until the next message.

## Why

See [`ChangeSystemGraphics` changes the message
window](../decisions/change-system-graphics-changes-the-message-window.md):
the message window is what the games switch for, and a System is cheap
there; the other screens are drawn into their banks once, and carrying
them per System is the screens stage again for each.

## How it looks today

Sunset Over Imdahl's dialogue switches from black text to `SaveMeny`'s
white with its shadow, over the painting, as in RM2k; its menu keeps
`System`'s white windows. Vampires Dawn's old man shows his three styles
and its graves come out in `Stone`; its menu keeps `VDBlutsys`. Desert
Nightmare's `Systemset_Spiel` differs from the intro's in two rows of its
text gradient, and that is what changes.

## When it stops being enough

When a game's menu or battle looks wrong next to its dialogue: Sunset's
`SaveMeny` is the System of its whole game after the opening. The way is
the screens stage once per System, each screen's bank and palettes in
`window_systems`' manner, and its loaders reading `WINDOW_NOW`.
