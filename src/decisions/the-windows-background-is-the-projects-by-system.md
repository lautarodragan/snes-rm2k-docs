# The windows' background is the project's, by System

## What

**A game can replace what fills its windows under the frame with a colour
or a vertical gradient of its own, one per System**, in its
`rm2k-snes.toml`. Since 2026-10-12, taro's:

```toml
[windows.background]
ablskin = "#000000"                          # one colour
Royal = ["#783f31", "#5a231f", "#421d2d"]    # a gradient, top to bottom
```

The key is the System's name as RM2k names it —the database, and
`ChangeSystemGraphics`—, without its extension and without regard to case;
for a picture of the project's own in `[graphics] system`, the stem of its
file. **A System with no entry keeps its own background**, stretched or
tiled as the database says, which is RM2k's behaviour. With an entry, the
System gives everything else: the frame, the cursor, the arrow, the
digits, the icons and the text colours.

The value is chosen once, by hand, for each System: nothing looks at a
System and guesses whether its background is a gradient. A list is a
gradient whose stops are spread evenly from each window's first line to
its last, as RM2k stretches the System to each window's height. No
horizontal gradient: none of the games surveyed has one, and the console
changes a colour only between lines.

## Why

The windows' background is what makes them expensive. RM2k stretches the
System's 32x32 square over each window, so a gradient is a different cell
on every row of every window, and the screens' banks of tiles overflow:
that is what had to be fused in [A window with a gradient is fused until
it fits](una-ventana-con-degrade-se-funde-hasta-que-entra.md). Over one
colour each window's inside is one cell and one entry of colour memory,
and a gradient costs one more entry written line by line, not one cell per
row. What it saves for each game was measured in [The windows, made
cheaper](../research/2026-10-11-las-ventanas.md).

**By System and not one value per game**, because a game changes System
while it plays: Desert Nightmare once, Sunset Over Imdahl a few times,
Vampires Dawn dozens. Each System has its own background, so whoever draws
a window looks up the System that is current then.

What is lost is what the System's background had besides its colours:
Royal's dither, the line at the top of The Frozen World's, the faint
stroke near two edges of A Blurred Line's.

## How it applies

* `rm2k-snes-project` reads and checks it —`windows.rs`—; the converter
  stops if a key names a System the game and the RTP do not have, because a
  misspelt name would leave its windows as they were without a word.
* `rm2k-snes-screens` takes the colour as `--window-background` and fills
  the System's background square with it, so every window drawn from the
  System gets it: the message window, the screens, the battle.
* **Until the runtime draws gradients, a gradient is drawn as its average
  colour** —the mean of the line its stops draw—.
* **Every screen is drawn with the System a game starts with, and the
  message window also with each one `ChangeSystemGraphics` switches to**,
  each over its own entry: see [`ChangeSystemGraphics` changes the
  message window](change-system-graphics-changes-the-message-window.md).
* The message window's text area, when all its lines come out the same,
  goes in the cartridge as one line that `prime_line` copies under each of
  them.
