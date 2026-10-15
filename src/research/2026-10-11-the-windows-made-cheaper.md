# The windows, made cheaper

> **Measured on 2026-10-11** by Tijereta. The tools of the-advocate at
> `fc6f7456`, the ports at `a85b7e3` (A Blurred Line's `abl.sfc`
> `27d989db75901791`): each of the eight games built from its
> `rm2k-snes.toml`, and its screens drawn again by `rm2k-snes-screens` of
> that commit with retouched copies of its System and its faces. The HDMA
> prototype ran in the libretro cores of snes9x, bsnes and Mesen-S. It is a
> snapshot: the numbers are from that day and this file is not updated. How
> each number was obtained is at the end.

The question is taro's, on 2026-10-11, after designing the hero name
screen —`EnterHeroName`, which only Dooms 2 uses, once—: if that screen can
be made cheap with a background of its own, the cursor in sprites and the
face out of BG1, *can all the windows of the engine be made cheaper the
same way?* "If we can make the windows, in general, more efficient, it is a
win everywhere."

What they settled before measuring, and this study takes as given:

* **No detection of gradients.** A setting of the project replaces the
  System's background with one of the project's own —a colour, or a
  gradient—; with it, the System gives only the frame, the cursor, the
  arrow, the digits, the icons and the text colours. Which value each game
  takes is decided once, by hand, not by a tool.
* **A face does not have to be pixel perfect**: it may shrink to round to
  8 pixels or to save a row or a column of tiles.
* **Code per game** —`.ifdef` on the setting, as `paint_table` and
  `MSU_REQUIRED` already do— is not ruled out, but it is more surface for
  bugs.

The six ideas they asked to measure, in order: the setting; the message
window as a band of the screen switched by HDMA or IRQ; the cursor in
sprites; the faces out of BG1; whether A Blurred Line fits one 16-colour
palette; and code per game.


## Summary

* **The setting is the big one, and it is cheap.** On the three Systems
  with a gradient —The Book of Three, The Frozen World, and Vampires Dawn's
  own— a background of one CGRAM entry takes every screen back inside its
  bank without fusing anything: The Book of Three's actor choice goes from
  193 tiles to 65 of 64, its shop from 245 to 24 of 96, its battle windows
  from 168 to 46 of 192. The message window gives back 8 colours to every
  map of The Frozen World (15 to 7). A gradient costs one CGRAM entry and
  one HDMA channel per group of windows that share lines, and nothing else.
* **The band idea has no VRAM to win**, and its palette half is blocked by
  the windows without a background. What it is good for is narrower and
  real: the gradient itself, and later a face's palette in the message
  window. HDMA, not IRQ: the IRQ belongs to `irq_music`.
* **The cursor in sprites** is what saves Dooms 2's actor choice (69 tiles
  of 64 down to 27), and halves what is left everywhere else once the
  background is flat. It works on the screens that have their sprites off;
  on the message window it runs into the object mask.
* **The faces are the menu bank**: between 0 (Sunset) and 216 (Vampires
  Dawn) of its 448 tiles. In the message window they are not drawn today,
  and three games ask for them thousands of times: they fit in the text
  area's own cells, with their palette written by HDMA on the window's
  lines.
* **A Blurred Line**: its message window fits one palette (13 colours, 12
  with a flat background); all of its windows with the four text colours do
  not (33). Declaring its background flat removes a near-black line nobody
  has noticed, and buys 17 pairs of item text that its build already warns
  about.
* **Code per game: data, not `.ifdef`**, except for whole subsystems. The
  setting changes tables, and a table with no entries switches the path
  off; what no game in the test suite exercises is the risk.

The value of the setting for each game, and the order to build it in, are
at the end.


## What the windows are today

Every screen keeps its windows in a bank of fixed size, and the bank is
what overflows:

```text
screen              layer              bank                         colours
message window      BG2, 4bpp          16 frame/arrow + 240 text    palette 0, entries 1..15, taken
                                                                    from every map's background
actor choice        BG1, 8bpp          64 tiles, $4000..$4800       entries 128..143
items, equipment    BG1, 8bpp          what the item text leaves    after the text palettes
shop                BG1, 8bpp          96 tiles                     after the text palettes
battle windows      BG1, 8bpp          192 tiles                    entries 240..255
End Game            BG2, 4bpp          its own                      one palette
slots, pause menu   BG2, 4bpp          448 tiles, with the faces    palettes 0..7
```

Everything a screen writes has to fall in the BG1 bank of every map layout,
because closing it restores the map by reloading that bank and nothing
else (`checks.rs` in `rm2k-snes-screens`). And the background of a
window is stretched as RM2k stretches it, so a gradient is a different
cell on every row of every window: that is what made the four surveyed
games fuse their windows ([A window with a gradient is fused until it
fits](../optimizations/a-window-with-a-gradient.md)).

The Systems of the eight games, as their windows use them:

```text
game                System            background                  window colours
A Blurred Line      ablskin           black, with a (15,15,15)    13
                                      line on two edges
The Book of Three   Royal (RTP)       vertical gradient, 27       23, reduced to 15
                                      colours with some dither
Desert Nightmare    Systemset_Intro   solid black                 15 (its text is a
                                                                  14-colour gradient)
Dooms 2             Dooms             solid (24,24,24)            18, reduced to 15 (its
                                                                  cursor has 38 colours)
El Dorado           Hernando          solid (5,5,5)               8
The Frozen World    thunter           vertical gradient, 15       16, reduced to 15
Sunset Over Imdahl  System            solid (250,250,255),        7
                                      no frame
Vampires Dawn       ablskin today;    vertical gradient, 9        39, reduced to 15
                    VDBlutsys its own
```

"Window colours" is what `rm2k-snes-screens window` counts for the message
window —background, frame, text, shadow, arrow and cursor— before Adeleine
reduces it to the 15 a palette holds. Three games also change System
during play with `ChangeSystemGraphics` —Desert Nightmare once, at start,
to `Systemset_Spiel`, also solid black; Sunset 5 times, Vampires Dawn
16—, which the engine accepts and ignores.


## 1. A background of the project's own

### What it saves

The screens were drawn again with each System's background replaced by
one colour —its middle row—, which is exactly what a gradient by HDMA
costs in tiles: one entry, one cell. Tiles each screen needs as RM2k draws
it, against its bank; `*` is a screen that today is fused to fit:

```text
                       message frame  actor choice  items/equip   shop      battle
                       (16)           (64)          (its bank)    (96)      (192)
A Blurred Line  today  16             62            24            39        34
                flat   12             36             7             7        12
Book of Three   today  27*            193*          238* (26)     245*      168
                flat   15             65*           24            24        46
Frozen World    today  26*            96*           109* (59)     112*      87
                flat   12             30             9             9        16
Vampires Dawn,  today  28*            158*          151* (31)     166*      122
VDBlutsys       flat   16             50            18            18        39
Vampires Dawn,  today  16             60            24            39        34
ablskin         flat   12             34             7             7        12
```

Desert Nightmare, Dooms 2, El Dorado and Sunset already have a flat
background: the setting changes no tile of theirs. Their numbers are in the
next section.

In colours, the message window and the battle windows —each colour the
message window drops is one more entry for **every** map's background,
because they share CGRAM in mode 3, see [The window takes thirteen colours
from every background](../divergences/the-window-takes-thirteen-colors-from-every-background.md)—:

```text
                       message window (15)   battle windows (16)   End Game: colours merged
                       today -> flat         today -> flat         today -> flat
A Blurred Line         13 -> 12              4 -> 3                0 -> 0
Book of Three          23 -> 12              16 -> 10              13 -> 2
Frozen World           16 -> 7               16 -> 7               5 -> 0
Vampires Dawn (own)    39 -> 33              16 -> 16              20 -> 13
```

Two things the table says beyond the tiles. **Vampires Dawn could go back
to its own System**: with a gradient background every screen of
VDBlutsys fits its bank —the message frame in exactly its 16—; it keeps
A Blurred Line's today for a reason that is not the windows (the ROM is one
64 KB piece short). Its frame alone has 21 colours, so the window is still
reduced to 15 by Adeleine. And **A Blurred Line's item text has room it
lacks**: its build warns today that the busiest item list asks for 200
pairs of tiles and the windows leave 167; flat, they leave 184.

In ROM the setting is worth little —A Blurred Line's screens go from
680 KB to 660 KB, The Book of Three's from 370 to 340, The Frozen World's
from 357 to 322— and the message window's `window_backdrop`, 7,680 bytes,
becomes one line repeated.

### What it costs

**A flat colour costs nothing at run time**: the background is one CGRAM
entry, the same one on every line.

**A gradient costs one CGRAM entry and one HDMA channel per group of
windows that share lines**, whose table writes that entry on each line —
`CGADD` twice and `CGDATA` twice, DMA mode 3 on `$2121`—. On the message
window the entry is already the window's —entries 1 to 15 are taken from
every map—, so the channel only writes on the window's lines and restores
nothing. On the screens:

```text
screen            windows sharing lines              entries and channels
message window    one                                1
items, equipment  help, list —one below the other—   1
actor choice      the two on the left and the party  2
shop              the status and the gold windows    2
battle            the windows of the strip           2 or 3, not measured
```

Channels are not short. On a map 1, 2 and 3 are the message window's,
4 the big picture's wave, 6 BG1's mask under the window in a panorama or
painted map, and 0 is the one general DMA uses: **5 and 7 are always
free**. The screens turn HDMA off when they open (`stz HDMAEN`), so they
have six; the battle uses 5 for the shake.

The CPU time is what HDMA steals: per line 8 master cycles when any channel
is on, 8 per active channel and 8 per byte (bsnes's `dma.cpp`). A gradient
over the 80 lines of the message window, writing every line, is
80 × 40 = 3,200 master cycles of the frame's 357,368: **0.9%**, and
less if it writes only where the colour changes.

### What looks different

* **A gradient is smoother than RM2k's.** RM2k stretches the System's 32
  rows, so it shows bands; the setting interpolates its stops one colour
  per line, at the console's 15 bits. Four games had theirs fused into
  bands since this morning: any gradient is closer to RM2k than that.
* **What the System's background had besides its gradient is lost**:
  Royal's dither, the one-row (0,8,0) line at the top of The Frozen
  World's, the two (15,15,15) lines of A Blurred Line's —which at 15 bits
  are (1,1,1) over black, and show on screen as a faint grey stroke near
  the right and bottom edge of every window—. A tiled background
  (`message_stretch` 1, or `ChangeSystemGraphics` asking for it, as Desert
  Nightmare does) is not a gradient, and the setting replaces it too.

The comparison, drawn by `rm2k-snes-screens render`, is the item and actor
choice screens of A Blurred Line, The Book of Three, The Frozen World,
Vampires Dawn with VDBlutsys and Dooms 2, today and with one colour; the
gradient would sit between the two. They were left for taro to look at.

### The setting

```toml
[windows]
# What fills a window under its frame. Without it, the System's own
# background, stretched or tiled as the database says: today's path.
background = "#000000"                          # one colour
# background = ["#783f31", "#5a231f", "#421d2d"]  # a gradient, top to bottom
```

A list is a vertical gradient: its stops evenly spread from each window's
first line to its last —every window stretches it to its own height, as
RM2k stretches the System—, linear in between and quantized to 15 bits.
One string is a colour. No horizontal gradient: none of the eight has one,
and HDMA can only change a colour between lines. The converter reads it
through `rm2k-snes-project` like any other setting; `rm2k-snes-screens`
draws the windows over a one-entry background and says which entry;
the emission writes the stops, and the runtime builds the HDMA tables from
them for the windows that are open.


## 2. The message window as a band

A window with a background covers whole lines of the screen —80 of them,
at 0, 72 or 144—, so taro's question was whether the console can switch
mode or palettes on its first line and back on its last.

### What it can do: the cycles are there

A prototype —mode 3, eight vertical stripes of CGRAM entries 1 to 8, and
*K* HDMA channels each rewriting one of them on every line— drew every
line with the colour its table wrote, with *K* from 1 to 8, **in snes9x,
in bsnes and in Mesen-S**: 0 wrong lines of 224 per stripe, the eight
channels writing 32 bytes per line. bsnes models that the PPU ignores
CGRAM writes between H=88 and H=1096 of a drawn line, and HDMA starts at
H≈1104: the hblank leaves about 340 master cycles, and eight channels of
four bytes take 8 + 8 × 40 = 328. **So the limit is the channels, not the
time**: one colour per channel and line. On real hardware, writing CGRAM
in the hblank is known to work and to be fragile when pushed (fullsnes
calls it "fragile timings"); one or two colours per line is what commercial
games do, and the rest is for taro's FX Pak.

Switching mode is one byte of `BGMODE` per channel on the line where it
changes, which games have always done.

### What it would win, and what blocks it

* **VRAM: nothing.** The window's 240 text tiles have to stay resident
  —they are the composer's—, and switching mode does not make them
  smaller: they would only shrink at 2 bits, in mode 1's BG3, and A
  Blurred Line's text alone is 5 colours plus the shadow.
* **CGRAM: the window's colours back to every map, in principle.** With
  two free channels, two colours per line: the frame's top row has 8
  lines before the text starts, so 16 colours could be swapped in there and
  restored in the bottom row's 8. **The windows without a background block
  it**: over a bare window the map stays visible on the same lines as the
  text, so the text's colours and the map's cannot share entries. A Blurred
  Line asks for a bare window in 388 of its 1,110 `MessageOptions`. What
  could still be swapped —the colours of a window with a background that a
  bare one never uses— is a few entries, for the eleven A Blurred Line maps
  that lose colours to the window today, a few pixels each.
* **The cursor and the arrow in sprites, on the window's lines**: blocked
  by the object mask, see section 3.

What the band *is* good for is narrower: **the gradient** of section 1,
which needs no restore because its entry is already the window's, and **a
face's palette** in the message window, section 4.

### Not by IRQ

The IRQ is `irq_music`'s: once per frame, on line 112
(`IRQ_LINE`), however long the loop takes. The middle window spans lines
72 to 151, so a window edge by IRQ would share the vector with the music
and could land while the music tick runs, late by however long the tick
takes —not measured—. HDMA needs no CPU, so it does not touch the music,
the vblank where the poses go up, or the wave and mask channels.

### What it touches

* **The bare window** (`MSG_BARE`) draws no background: its gradient table
  is empty.
* **Sunset's painted maps run in mode 1**, where the window is the same
  BG2 at 4 bits on palette 0; the gradient's entry is in palette 0 in both
  modes, and channel 6 keeps masking BG1.
* **Colour math** is unused ([Translucent events don't use colour
  math](../optimizations/tried-and-left-out.md#colour-math-for-translucent-events)), and none of this
  needs it.


## 3. The cursor in sprites

Today the cursor is baked: for each position the screens keep the cells
that change, and the cartridge copies them into the tilemap (`borders.rs`,
`target_bar` in `actor_choice.s`, `window_bar` in the message window).
Drawing the screens again with the cursor reduced to one pixel gives what
it costs:

```text
                     actor choice   items/equip   shop      battle     message window colours
                     (64)                         (96)      (192)      (of 15)
A Blurred Line       36 -> 24       7 -> 6        7 -> 6    12 -> 9    12 -> 11
Book of Three        65 -> 30       24 -> 15      24 -> 15  46 -> 30   12 -> 11
Desert Nightmare     24 -> 11       17 -> 11      17 -> 11  30 -> 18   15 -> 13
Dooms 2              69* -> 27      23 -> 12      23 -> 12  37 -> 17   18 -> 12
El Dorado            36 -> 25       12 -> 11      12 -> 11  22 -> 18   8 -> 7
Frozen World         30 -> 22       9 -> 7        9 -> 7    16 -> 11   7 -> 7
Sunset Over Imdahl   13 -> 3        6 -> 3        6 -> 3    10 -> 4    7 -> 3
Vampires Dawn (own)  50 -> 33       18 -> 16      18 -> 16  39 -> 31   33 -> 29
```

All with the background already flat, so this is what the cursor adds on
top. **Dooms 2 is the one it saves**: its background is already flat,
and its 38-colour cursor is what pushes the actor choice to 69 tiles and
the message window to 18 colours.

As sprites the cursor is a nine-slice of the System's: four corners, four
edges and the middle repeated, 16 4bpp tiles per drawing. Its colours go in
one sprite palette; Dooms 2's 38 do not fit one, and would need Adeleine or
a palette per piece —not measured—. The limits:

* **Per line**: the widest bar is the pause menu's, 104 pixels. With 32x32
  sprites it is 4 across, 16 slivers of the 34 a line holds.
* **The OAM on the pause menu**: the experience line already uses 120 of
  the 128 sprites (`menu_experience.s`); the bar in 32x32 sprites is 8 more,
  exactly 128. The actor choice, items, equipment and shop turn their
  sprites off, so all 128 are free there.
* **Where their tiles live**: a screen can only overwrite what closing it
  restores. Sprites can name the menu bank's tiles —the experience does,
  with `OBSEL` at `SLOT_VRAM`—, so the cursor's 4bpp tiles would cost the
  448-tile menu bank what they save the 8bpp banks, at half the bytes.
* **The message window**: blocked by the object mask. On the window's
  lines every object is hidden, so the characters do not show through the
  window ([The window without a background does not cover the
  characters](../divergences/the-window-without-a-background-does-not-cover-the-characters.md)).
  Window 2 could open a hole in the mask where the cursor is (mask = W1
  XOR W2), but then the map's characters show through the cursor's
  transparent pixels; with a flat background the cursor can be made opaque
  —its transparent pixels painted the background's colour—, and then it
  works. It wins the cursor's colours in the window palette: one for A
  Blurred Line, six for Dooms 2.

The per-line limits count masked sprites too: a cursor or face on the
window's lines has to be at the lowest OAM indices to survive a crowded
line.


## 4. The faces out of BG1

### In the menu bank

The slot screen and the pause menu keep their faces in the 448-tile menu
bank, at 4bpp. Drawing them with every FaceSet blank:

```text
                     menu bank (448)   without faces   faces
A Blurred Line       381               256             125
Book of Three        240               184              56
Desert Nightmare     114                78              36
Dooms 2              354               148             206
El Dorado            222               210              12
Frozen World         229               138              91
Sunset Over Imdahl    69                69               0
Vampires Dawn        386               170             216
```

The bank is not the only limit: its palettes are. BG2 has eight, the first
two are the text's and the disabled commands', and A Blurred Line already draws 8 of its 14 faces with
another face's palette. In sprites, faces get the eight sprite palettes
(128 to 255) besides —two are the menu bar's and the experience's—, so
twelve faces could have their own. In tiles they only leave the bank if
their sprites name tiles outside it, in the map's sprite area, which
closing the menu would then have to reload the way coming back from a
battle does.

A FaceSet face is 48x48, six cells by six: it needs no rounding to the
8-pixel grid. What the menu crops of it —twelve pixels on the left— is
the only shrinking it has today.

### In the message window

**Faces are not drawn in the message window** (`ChangeFaceGraphic` is
accepted and does nothing). How many times each game asks for one:

```text
                     ShowMessage   ChangeFaceGraphic with a face   FaceSets
Desert Nightmare     2,354         1,848                            7
Dooms 2              1,609           722                            9
Vampires Dawn        17,363        8,195                           15
the other five       —             0                                —
```

The window cannot take 36 more tiles —its 256 are fixed in every
layout—, but **it does not need to**: with a face, RM2k moves the text to
the right of it, so the 36 text-area cells under the face are free, and
the face can be written into them like a letter, once per page. What it
needs is a palette: the window's has no room, and another BG palette's
entries are the map's. That is where the band of section 2 is useful:
palette 1, entries 16 to 31, written by HDMA in the 8 lines of the
window's top frame row and restored in the bottom one, two channels of two
colours a line. Over a bare window it would recolour the map's pixels on
those lines; Desert Nightmare asks for 7 bare windows in all, Dooms 2 for
3, Vampires Dawn for 37.

The line loses what the face takes: at 256 pixels the text goes from 240
to about 184, and `refit` reflows what no longer fits.

### The hero name screen

The design in the wish list —the System alone in BG1 at 8 bits, the face
in BG2 or sprites, the cursor in sprites, the background by HDMA— is the
same three pieces, and gets cheaper with each of them. With the background
flat, a window is nine frame cells and one background cell whatever its
size, so the runtime can draw it itself: see the order below.


## 5. A Blurred Line, in one palette

**The message window fits**: background, frame, text, shadow, arrow and
cursor are 13 colours of the 15, and 12 with the background flat.
**All its windows together do not**: text colours 1, 2 and 3 —the red of
the terms, the "goes up" colour and the grey of what cannot be done— are
gradients of 8 colours each, and with them it is 33. Today each ink has
its palette on the text layer (the item screen's four), and that keeps
working.

What declaring "one flat colour" lets the engine assume, beyond the tiles
of section 1:

* **A window is ten cells.** Nine of frame and one of background, at any
  size: the runtime can draw windows instead of copying baked tilemaps,
  which is what a hero name screen, a custom menu or a new shop layout
  needs.
* **The message window's text area starts from one cell**, not from the
  7,680-byte `window_backdrop` table `prime_line` copies a line at a time.
* **Sprites over a window can be made opaque**, which is what the cursor
  and a face need on the message window's lines (sections 3 and 4).

What it changes on screen: the faint (1,1,1) strokes near the right and
bottom edge of each window go. Every golden with a window would move by
those pixels, and nothing else.


## 6. Code per game

The setting is **data**. What changes per game is what the converter
emits —the windows' tiles, the window palette, a list of gradient stops—,
and the runtime can take the same path for all of them: a gradient table
with no stops is a channel that is never turned on, and a flat colour is a
gradient of one stop that needs no channel. That costs bytes, not
branches, and every path is the same code.

An `.ifdef` is worth it for **a whole subsystem most cartridges do not
carry**, as `painted.s` is under `paint_table`: there it saves ROM in every
other game and the cartridge without it comes out byte for byte the same.
None of the six ideas is that size.

The risk is not the `.ifdef`; it is **a path no test runs**. The ROM tests
are A Blurred Line's suite, and the other seven only check that they build
and reach their first map (`just arrancan`, which passes messages and
choices but has no goldens of screens). Whatever A Blurred Line does not
use —a gradient, a cursor of 38 colours, a face in a message— runs nowhere
but in taro's hands. So: give A Blurred Line the setting too (one flat
colour), and give the suite a test cartridge with a gradient, so that the
HDMA path has a golden.


## The setting for each game

```text
game                 [windows] background                           what changes on screen
A Blurred Line       "#000000"                                      the (1,1,1) strokes go
The Book of Three    ["#783f31", "#5a231f", "#421d2d"]              Royal's dither; no more fused windows
Desert Nightmare     "#000000"                                      nothing (Intro and Spiel are both black)
Dooms 2              "#181818"                                      nothing
El Dorado            "#050505"                                      nothing
The Frozen World     ["#000030", "#000078"]                         the one-row line at the top; no more fused windows
Sunset Over Imdahl   "#fafaff"                                      nothing
Vampires Dawn        "#000000" with ablskin, as today;              with its own, no more fused windows
                     ["#18085a", "#180894"] with VDBlutsys
```

The gradients are each System's middle column, with its first rows left
out —The Frozen World's (0,8,0), Vampires Dawn's (8,16,74)—, which are
lines under the top edge of the frame more than part of the gradient.


## The order to build it in

Each step verifiable with A Blurred Line's suite and `just arrancan`, in
the ports.

1. **The setting, and a flat colour in the converter only.** `[windows]
   background` in `rm2k-snes-project`; `rm2k-snes-screens` draws the
   windows over one entry. No runtime change. A Blurred Line *without* the
   setting comes out byte for byte the same; the four games that are
   already flat, too. Then A Blurred Line with `"#000000"`: the goldens
   with windows move by the (1,1,1) strokes and nothing else, in their own
   commit.
2. **The message window's text area from one cell.** `prime_line` fills
   the line instead of copying `window_backdrop` when the background is
   flat. A Blurred Line byte for byte the same on screen: the suite stays
   green with no golden moved.
3. **The gradient on the message window.** One entry of palette 0 and
   channel 7, its table built by `msg_hdma_build` for the window's
   position. A test cartridge of A Blurred Line with a gradient, and its
   golden; The Frozen World and The Book of Three through `arrancan`, with
   captures for taro.
4. **The gradient on the screens**: items and equipment (one channel),
   then the actor choice and the shop (two), then the battle. Each screen
   one step, with its capture.
5. **The cursor in sprites**, on the screens whose sprites are off —actor
   choice, items, equipment, shop—; then the pause menu, against the
   experience's 120 sprites; Dooms 2 is the check. The message window's
   cursor last, with the mask's window 2.
6. **Windows drawn by the runtime** from the frame's nine cells and the
   background's one, first for a screen that does not exist yet —the hero
   name screen— so nothing that works is touched.
7. **Faces**: in the message window, into the text cells, with palette 1
   by HDMA (Desert Nightmare, Dooms 2, Vampires Dawn); in the menu, in
   sprite palettes, when a game runs out of BG2 palettes.

Steps 1 and 2 are worth doing even if nothing else is: they are the
converter and one routine. With them a game with a gradient can already
stop fusing by taking one colour; steps 3 and 4 give it its gradient back,
and step 5 is what Dooms 2's actor choice needs.


## What was not measured

* **Real hardware.** The HDMA prototype ran in three emulators, which
  agree; CGRAM in the hblank is where emulators are least trusted.
* **How long `irq_music` takes**, which is what an IRQ at a window edge
  would wait for.
* **The battle windows' gradient groups**: how many windows of the strip
  share lines in each layout.
* **Dooms 2's cursor in one sprite palette**, and whether a nine-slice
  split keeps each piece within 15 colours.
* **The tiles of the cursor in sprites, net**: the 8bpp tiles it saves
  were measured, the 4bpp tiles it would add to the menu bank were
  counted by hand (16 per drawing).
* **The faces in sprites**: only what they free in the menu bank, not
  where their tiles would go or what reloading the map's sprites costs.
* **What a smoother gradient looks like next to RM2k's bands**: the
  captures show today against one flat colour.


## How it was measured

* **The builds.** Each game's `release` built in a worktree of the ports
  at `a85b7e3`, with a wrapper in front of `rm2k-snes-screens` that kept
  every request the converter made to it.
* **The variants.** `rm2k-snes-screens window` and `convert` run again on
  those requests, with `--system` pointing at a retouched copy of the
  game's System: its background's 32x32 filled with its middle pixel
  ("flat"); its two cursors cleared to one pixel in the corner (a cursor
  that draws nothing is refused); or both. For the faces, a copy of the
  game's folder and of the RTP with every FaceSet blank. `cgram_reserved`
  was recomputed from each variant's window colours, as the converter
  does. Tiles are the length of each screen's `tiles` in `screens.json`,
  or, for a screen that was fused, the count its warning gives "as RM2k
  draws them". Vampires Dawn was measured with the `ablskin` its project
  sets and with its own `VDBlutsys`.
* **The Systems.** Read from each game's `.zip` and the RTP's: kind of
  background by whether every row, or every column, of its 32x32 is one
  colour; colours by piece.
* **The counts of commands.** `ChangeFaceGraphic` (10130) with a face name,
  `ShowMessage` (10110) and `MessageOptions` (10120) with its first
  parameter at 1, over each game's `data/`.
* **The prototype.** A 32 KB LoROM assembled with ca65: mode 3, BG1 with
  eight stripes of entries 1 to 8, and channels 0 to *K* − 1 each writing
  its entry with DMA mode 3 on `$2121`, red = line and blue = entry; after
  ten frames, each stripe compared line by line with what its table wrote.
* **The ROM sizes** are the bytes of data in each `screens.json`, an
  approximation of what the cartridge carries of its screens.
