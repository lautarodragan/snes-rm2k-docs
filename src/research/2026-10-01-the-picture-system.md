# The picture system and the portable console

> **Measured on 2026-10-01 at `76d98bed`** (snes-rm2k), by Jilguero. It is
> a snapshot: the numbers are from that day and this file is not updated.
> The counts came from throwaway scripts over `rom/data/` and the game's
> images; how to redo them is at the end, in "How it was measured". How
> much each cartridge has left **today** is what `just espacio` says.

## Summary

* **The game has 348 `ShowPicture`, 33 `MovePicture` and 162
  `ErasePicture`, with 97 distinct images.** Split by system:

      system                  ShowPicture  images    where
      portable console            262         61     11 common events, one autostart
      cutscenes                    28         18     21 pages of 19 maps
      counter (Fortitude)          35         11     map 95 and common events 9 and 10
      old menu, dead               23          7     common events 11 to 20 and 34

  Three quarters are the portable console's, and nearly all of those
  —208— are the aura numbers: 25 images of 12x13 that are positioned by
  variable.
* **The portable console is not needed to play.** It writes 17 switches
  and 10 variables and **nobody outside it reads any of them**: it shows
  tutorials, skill screens and Talan's aura count, and changes nothing in
  the game. It is opened by item 81, *Portable Console*, which the game
  gives in the first cutscene.
* **What it asks for besides pictures** is four things, and none of them
  is ABL's: **autostart** common events (parallel ones are not needed),
  `Label`/`JumpToLabel`, a **shared** `CallEvent` instead of one pasted in
  place —pasted, the menu is **140,193 commands**—, and `\V[n]` in
  messages. `KeyInputProc` already compiles the way it uses it.
* **taro's idea is confirmed, with a nuance.** Of the 21 situations with a
  picture in the cutscenes, **18 freeze the hero** and in **12 the map is
  not even visible**: the cutscene tints the screen black before showing
  the picture, and in RM2k pictures are not tinted. The three with the
  hero free are small pictures —smoke, a "Ready" sign, the counter—. The
  whole console is an autostart page: it freezes the hero, but the map
  **is** visible around its window.
* **No single option is enough, and two together cover almost
  everything.** Sprites can't handle anything larger than 256x128 pixels
  —the 512 object tile limit is the hardware's— and 27 of the 90 pictures
  are nearly full-screen. What is recommended is **two planes**:
  **objects** for the small things over the map —with the events hidden
  when the map leaves no room—, and **BG1 in mode 1** for the large ones
  with the map hidden, which costs no VRAM because it uses the map's and
  leaves BG2 —the message window— as it is. They cover 20 of the 21
  situations and the whole console; what remains is translucent pictures
  over the map, which go down as debt.
* **Space fits comfortably**: all the pictures in use, at 4 bpp and with
  LZ2, are **about 330 KB** (cutscenes 203, console 128, counter 1), **5
  or 6 of the 46 free banks**. Tucu-tucu estimated ~430 KB over the 97
  with 15 colors; with 15 colors in the text pages too it is 413 KB. What
  inflates it is the rescaling of the text, not the size.
* **Cutscenes first, then the console.** The cutscenes are story —"One
  year previously", "Meanwhile in Lashe City", the instructions of two
  minigames, the ending sign— and ask little of the engine; the console
  asks for four interpreter pieces and doesn't change the game.

## 1. Actual use

### The cutscenes

Every map page that shows a picture, grouped by situation. "Black" means
the page tints the screen to (0, 0, 0) beforehand, or that the map is the
black of the boot: the map is not visible and the picture is, because RM2k
does not tint pictures —`affected_by_tint` is off by default in
`Game_Pictures::ShowParams`, in easyrpg-player—.

    map   picture              trigger      behind   on the console options
     4    Oneyearprev          autostart    black    186x29         tone 0→100→0   (the one already drawn)
    81    MeanwhileLashe       autostart    black    214x31         tone 0→100→0
   295    SevDaysPrev          autostart    black    199x30         tone 0→100→0
   309    ABLEndBox8           autostart    black    124x212        tone, the end of the game
    49    EscapeInst           autostart    black    221x191        waits for a key: instructions
   285    AdvoInstr            autostart    map      240x224        rises 100 px in 4 s: instructions
   285    Ready                parallel     map      63x31          the minigame, hero free
   212    PhoneCallDiff        autostart    black¹   256x224        zoom 100→0 in 2 s
   213    SurlBroDiff          autostart    black¹   256x224        same
   214    SurlGravesDiff       autostart    black¹   256x224        same
   216    ThreeRubbleDiff      autostart    black¹   256x224        same
   217    the four *Diff*      parallel     map      256x224        50% translucent, one every 6 frames
   208    GTest4               action       black    256x224²       waves, saturation 200, with messages
   267    GTest4               parallel     black    256x224²       waves, saturation 200, with messages
   288    ShipFlash, GTest4    autostart    black    256x224²       waves, saturation 200, with messages
    45    ABLrec               parallel     map      51x60          blinks: "REC" of the security video
    98    ABLrec               parallel     map      51x60          same
   207    smoke1, smoke2       parallel     map      25x59          with the map, by variable, 40% translucent
    32    hovertram2           touch        map      132x141        with the map, and right after a Teleport
   311    hovershadow          touch/auto   map      112x119        with the map, transparency 100→50 in 1 s
    95    Fortitude + 2 digits touch        map      88x23 + 2      the counter, hero free

¹ The picture is a photo of the screen, opaque and whole: 15 frames later
the page tints to black and shrinks it to zero in two seconds.
² The original picture is 389x414 and overflows the screen; the 256x224
is what is visible.

"On the console" is the size at the console's scale: x 256/320 in width,
x 224/240 in height, which is what `picture.py` does with the one already
drawn.

**How many at once, at most:** three, on map 95 (the label and two
digits). Everywhere else, one.

**Map 208's** is an event called `Disabled`, action-triggered and without
a graphic. Whether it can be stepped on was not checked; it is counted.

### The portable console

It is a menu made of pictures and `KeyInputProc`, and it works like this:

1. Item 81, **Portable Console**, is a switch-type item used from the
   menu: it turns on 710. The game gives it on map 4, the first cutscene,
   and takes it away and gives it back around Radin's and Sern's menus
   (common events 42 and 44, maps 298 and 321).
2. 710 triggers **common event 39, `NewMenuActivated`**, autostart: a
   window with the character's portrait (picture 17, `NewMenu<name>`,
   302x202 shown at 50%), two labels "Skills" and "Tutorials" with a
   translucent red highlight over them (picture 18, `SkillSelect`, a
   single-color rectangle at 50%) and some arrows (picture 19,
   `ArrowTest`, almost all transparent). Left and right switch among
   thirteen characters; up and down, between labels.
3. With the action key, depending on the character and the label: a
   **text page** covering almost the whole screen (picture 17 at 100%,
   301x202: `<name>Skill1` or `<name>Tutorial1`, white on black), a
   message ("There is no skill screen available for…") or a count in a
   message (common events 48 and 49, with `\V[n]`).
4. For Talan, with switch 133 on, "Skills" opens **common event 21,
   `ManageAuraMenu`**: one table per aura color (picture 1,
   `Aura<color>Menu`, 320x203, full-screen) with eight numbers on top
   (pictures 2 to 9, `Aura0`…`Aura24`, placed by each
   `DisplayAuraNums[n]`, common events 23 to 31, with the position in
   variables 67 and 68). Left and right change color.

Measured on the console:

* **How many at once:** nine in the aura table (the table and eight
  numbers); three in the main window; one in the text pages.
* **The 61 pictures**: thirteen portraits (from 39 to 256 colors),
  thirteen text pages (2 colors), six aura tables (7 or 8 colors), 26
  aura numbers (2 colors) and the three pieces of the window.
* **Which options they use**: transparent color in 228 of 262; position
  by variable in 208 (the aura numbers); 50% zoom in 23 (the window);
  translucent in 7 (the highlight). **No** `MovePicture`: to move
  something the console shows it again. Nothing tied to the map, no waves
  or rotation, no tone.
* **What it covers**: the main window, 121x94 on the console, about 20% of
  the screen; the map is visible around it, untinted. The text pages,
  241x189, leave a map frame of 8 to 17 pixels. The aura table leaves
  only a strip at the top and bottom.
* **There is never a message open with a large picture**: before each
  `ShowMessage`, the console erases pictures 17 and 18.

### The old menu, which nobody opens

`CustomMenuHier1` (11), `DisplayNameMenu` (16), the four `CustomMenu*`
(12 to 15), `DisplayNameSlot*` (17 to 19), `GoToHier1` (20) and
`ExitTheMenu` (34) are **an earlier menu that the game no longer opens**:
it is triggered by switch 335, which is only turned on from inside those
same common events, or by item 150, which is called `SCRATCHEDOUT` and is
given by no event. They are 23 `ShowPicture`, 17 `MovePicture` and 7
pictures that are left out of all the counts below. `ManageAuraMenu` is
alive: the new console calls it.

## 2. What else the portable console asks for

Each common event was compiled as an autostart page of a test map, whole
and command by command, with the installed `rm2k-snes-events`. Today:

    common event               whole         what doesn't compile
    39 NewMenuActivated        no            Label/JumpToLabel; \V[0173] in a message
    21 ManageAuraMenu          no            Label/JumpToLabel
    48 All Saldra FDs?         no            \V[0195] in a message
    49 All Lerle Memorizes     no            \V[0196] in a message
    40, 22, 23, 25             yes           —
    (the rest of 24 to 31 are 23 with other variables)

Pictures compile because today they are accepted without being done
(`ACCEPTED_UNDONE`); `KeyInputProc` compiles the way the console uses it
—all 15 have five parameters, with wait—. What's missing, from smallest to
largest:

* **`Label` and `JumpToLabel`**: they have no arm in the compiler. The
  console is a state machine made of jumps: 15 labels in 39. In the game
  there are **8 more map pages** with labels. It is an `OP_GOTO`, which
  already exists, with the target resolved at compile time.
* **`\V[n]` in a message**: the value of a variable. `escape_tail` only
  accepts the two pauses at the end, and in the whole game there are three
  messages with `\V`, all three the console's (Sern's souls, Saldra's
  techniques and Lerle's).
* **Position by variable**: the aura numbers are placed with variables 67
  and 68, but each `DisplayAuraNums` loads them with constants right
  before (240 and 49 in the first). The compiler already tracks constants
  —the `constants` map in `compile.rs`—, so it is resolved at compile
  time.
* **Autostart common events**: 39 is one. Today the ROM runs no common
  event by its trigger; they are only compiled pasted where a `CallEvent`
  calls them, plus the equipment ones, which are a case apart. For 39 the
  **autostart** ones are enough: one body per common event, compiled once
  in the ROM —like `equipment_commons`, which already runs it with the
  24-bit pointer—, and the ROM checking its switch when refreshing pages.
  With that the other five live autostart ones turn on too: 7
  (`AbsorbAuraAbilities`), 42 and 44 (Radin's and Sern's menus, which
  teleport), 43 (Emily's tape) and 50 (`RadinUses`). **The parallel ones
  are not needed** for the console, and they are the ones that brought the
  known problem: 2, `DisableSaving`, is parallel with no switch (see
  `party_common_events` in `indices.rs`).
* **A shared `CallEvent`**: the compiler pastes the call in place
  ([decisiones/call-event-is-compiled-inline.md](../optimizations/lossless/events/common-event-calls.md#pasted-in-place)),
  and the console calls in cascade: 21 calls 25 eighteen times, which
  calls eight of 23 to 31 per color. **Pasted, 39 is 140,193 commands**;
  25 alone, compiled today, is 14,947 bytes. What's needed is an
  `OP_CALL` to a shared body with its return and a short stack —no call
  in the game is recursive, and nesting is capped at `LLAMADA_MAX`—.
  Without pasting, the console's common events add up to about 2,400
  commands.

**Is it needed to play? No.** What the console writes —switches 710, 712
to 725, 856 and 857; variables 63, 64, 66, 67, 68, 156, 167, 192, 195 and
196— is read by **no** other event, common event, troop or page condition
in the game: zero reads. The aura counts it shows —variables 70 onwards—
are written by the troops and map 13; the table only reads them. The only
thing lost without it is information: how each character's systems work
and how many techniques each one is missing.

## 3. How to draw them

### What freezes in RM2k

While an autostart, action or touch page runs, **the hero doesn't move**;
nor with a message open, even if a parallel one opens it. The rest
**goes on**: the routes of events nobody waits for, animated tiles,
parallel events and the timer. Pictures don't stop anything: they are one
more layer on top, and they erase themselves on a map change
(`erase_on_map_change`, on by default in RM2k 2000).

Over the 21 situations in the cutscene table —one per row—:

    freeze the hero                            18
      with the map black behind                 12   (4, 81, 295, 309, 49, 212, 213, 214, 216, 208, 267, 288)
      with the map visible                       6   (285 AdvoInstr, 217, 45, 98, 32, 311)
    with the hero free                          3   (207 smoke, 285 Ready, 95 counter)
    cover 70% of the screen or more             10   (49, 285 AdvoInstr, the four Diff, 217, 208, 267, 288)

The parallel ones of 45, 98 and 217 run alongside an autostart of the
same cutscene, and 267's opens messages: they freeze all the same. The
three with the hero free are small pictures: the largest, the counter's
label, at 88x23. The whole console freezes —it is autostart— and its map
is visible.

### The options

What rules is size. **The sprite limit is the hardware's**: 512 object
tiles (the two name banks, `docs/port/vram.md` in snes-rm2k), 128
objects, 32 per line. At 4 bpp, 512 tiles are 256x128 pixels: half a
screen. And **27 of the 90 pictures in use exceed that** —the 13 text
pages, the 6 aura tables, the 2 instruction screens, the 6 full-screen
ones—: they don't fit in sprites even removing all the events.

**A. Sprites always**, which is what `picture.py` does today with a
single one.

* Covers: the small ones. The three time signs (6 or 7 objects), Ready,
  ABLrec (two maps), the smoke, the counter, the shadow on 311 (16
  objects, 256 tiles); and the console's main window (12 objects, ~130
  tiles, plus ~6 objects of arrows and 2 of highlight) — **if the map
  has room**. That's 9 of the 21 cutscene situations, and the main
  window.
* Doesn't cover: the hovertram on 32 (25 objects, 400 tiles) nor
  ABLEndBox8 (28, 448) except on an almost empty map; no picture larger
  than half a screen: the instructions, the photos, GTest4, the console's
  pages, the aura table. Nor the waves.
* VRAM: whatever each map reserves from its sprite bank, which is already
  full on maps with many people (Delcentric Factory uses 475 of 512). The
  converter would have to reserve, per map, room for the pictures that map
  can show; the console, which opens on any map, has no guaranteed room on
  any of them.
* CGRAM: one sprite palette per picture, 15 colors. A 256-color portrait
  ends up with 15.
* ROM: a 32x32 object doesn't share tiles with another, so it is stored
  without deduplicating; for the small ones it doesn't matter.
* What looks different: the colors.

**B. No events, and the picture in the sprites** (taro's second idea).

* Covers A's **on any map**, because it takes the 256 to 512 tiles and
  the eight sprite palettes: the console's window can have up to 120
  colors split by object (Adeleine). It adds the hovertram on 32 and
  ABLEndBox8 in the layouts that give 448 tiles or more: 11 of 21.
* Doesn't cover: the same as A, anything over 256x128.
* VRAM and CGRAM: zero extra; when the picture is erased the poses of
  whoever was there are uploaded again, which is already what
  `vram_queue` does.
* What looks different: **with the map visible, the hero, the neighbors
  and the timer disappear** while it lasts. With the map black, nothing.

**C. Bake the picture into a map layer, on the fly.**

* Blending a picture with BG1's 8 bpp tiles is per-pixel work in planar
  format, on the CPU: hundreds of tiles for the console's window, dozens
  of frames. And it has to be undone on erase. **Not recommended.**
  Baking it in the converter only works for what doesn't move or change,
  and there is none of that in the game: the smoke alternates, the rest
  is shown and erased.

**D. Lend BG2** —the upper layer and the message window— to the picture.

* Covers: what fits in BG2's tiles: 384 tiles of 4 bpp in five of the six
  layouts, 512 in "+encima". Of the console's pages, 16 of 19 fit in 384
  (Radin, Saldra and Kersh2 don't) and 18 in 512. Of the cutscenes, 11 of
  21: the small ones, the signs, ABLEndBox8 and EscapeInst; not the
  full-screen photos, nor AdvoInstr, nor the ones that open messages with
  the picture up.
* VRAM: zero extra; on erase, the tiles of the upper layer and the window
  are uploaded again (about 12 KB).
* CGRAM: only the palettes the upper layer had, 1 to 7: the lower half is
  the background's, which is still visible.
* What looks different: **the upper layer disappears** —roofs, treetops—
  in the frame the picture doesn't cover. And **the message window can't
  open at the same time**: on the console it never happens, in the
  cutscenes it does (208, 267, 288, 311).

**E. Another mode while there is a picture: BG1 in mode 1.**

Mode 1 has BG1 and BG2 at 4 bpp. **BG2 is already 4 bpp in mode 3**, so
switching `BGMODE` from 3 to 1 changes nothing for the window or the
upper layer: it only makes BG1 be read at 4 bpp. With the map hidden, BG1
is free for the picture.

* Covers: **all the full-screen ones with the map hidden**: the 12
  situations with the map black, and AdvoInstr with a black frame, 13 of
  21. And the waves come out **exact**: they are a horizontal shift per
  line, an HDMA channel on `BG1HOFS`. Tone, the palette, as today.
* VRAM: **zero extra**. At 4 bpp, a 256x224 screen is 896 tiles, 28 KB,
  and the room for the background's tiles is 24 to 34 KB depending on the
  layout —768 to 1,088 4 bpp tiles—; deduplicating, they all fit except
  four in the 24 KB layouts: SurlBroDiff, SurlGravesDiff and
  ThreeRubbleDiff (896 unique tiles) and GTest4 (888). Those ask for a
  layout of 28 KB or more, or for taking the sprites' room too, which
  with the map black aren't needed. BG1's tilemap (2 KB) is already
  enough.
* CGRAM: the eight background palettes minus the window's: **105
  colors**, which Adeleine distributes per tile. At 8 bpp in mode 3 there
  would be 255, but only pictures under 384 to 544 unique tiles fit —the
  three signs, ABLEndBox8 and EscapeInst—; the other seven don't.
* The cost: when the picture is erased the map has to be reloaded: the 30
  KB and the two black frames of `back_to_map`. With the map black they
  aren't visible.
* What looks different: with the map visible (the console's pages,
  AdvoInstr), **the map frame around the picture comes out black**.

**F. Mode 7, for the zoom of the *Diff* photos.** Mode 7 scales, but its
map allows 256 tiles of 8 bpp: a whole photo needs 896. It would fit at
half resolution, enlarged to double at the start. For four two-second
cutscenes it is not worth the cost: **the recommendation is to replace the
zoom with a fade**, and declare it.

### What none of them covers

* **Translucent over the visible map**: the montage on 217 (four photos
  at 50% that change every six frames: 28 KB each, they can't be uploaded
  in six vblanks), the smoke on 207 at 40% and the shadow on 311. Color
  math is ruled out
  ([decisiones/translucent-events-dont-use-color-math.md](../optimizations/tried-and-left-out.md#colour-math-for-translucent-events)).
  The smoke and the shadow opaque; the montage, as white flashes without
  a photo. All three are debt.
* **The console's highlight** is a red rectangle at 50% over a label of
  picture 17, in two fixed places. It can be composed in the converter:
  two variants of the window, one per label. It is the only thing in the
  console that asks for something of ABL's.

### What each combination covers

    option                     cutscenes (21) console                         what looks different
    A sprites                      9          window, if the map has room     colors
    B no events + sprites         11          window                          the events go away
    D BG2 lent                    11          window; 16 of 19 pages          the upper layer goes away
    E BG1 in mode 1               13          pages and auras, black frame    black frame; map reload
    A + B + E (recommended)       20¹         everything²                     black frame on the pages

¹ Missing the montage on 217, which stays as flashes without a photo. And
with debts: the smoke on 207 and the shadow on 311 opaque, the zoom of the
*Diff* ones as a fade.
² The main window in objects —with the events hidden (B) when the map
leaves no room—; the pages and the aura table in BG1 (E).

## 4. Space

All the pictures in use, at the console's scale, in 4 bpp tiles
deduplicated with flips, with their tilemap, with LZ2:

                     pictures   4 bpp, 15 col.   4 bpp, own colors        8 bpp, 255 col.
    cutscenes           18         203 KB             203 KB                  421 KB
    portable console    61         208 KB             128 KB                  404 KB
    counter             11           2 KB               1 KB                    6 KB
    total               90         413 KB             332 KB                  831 KB

"Own colors" means that a 2-color picture is reduced to 2 and not to 15:
rescaling from 301 to 241 pixels puts grays into the text, which with 15
colors are distinct tiles. With 2, the text pages drop to half. The old
menu is not included: it is 7 pictures nobody shows.

**Against the 46 free banks of 64 KB, it is 5 or 6.** Tucu-tucu's
estimate, ~430 KB, was over the 97 and with 15 colors: it comes out the
same, and is confirmed as an order of magnitude.

**With the `.msu`, the better version** would be the 8 bpp, 255-color one
for the seven photos (the four *Diff*, GTest4, ShipFlash, AdvoInstr:
about 400 KB raw in the `.msu`, which take no ROM), read through the data
port like the battle backgrounds (`docs/port/msu-datos.md` in snes-rm2k):
the ROM still carries its 4 bpp version and uses the other only if it
finds it. For the text pages **the `.msu` improves nothing**: they are 2
colors. What would improve them is mode 5 —text without rescaling, at 512
pixels wide—, which is the idea of [`custom-menu-of-our-own-not-made-of-pictures`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/custom-menu-of-our-own-not-made-of-pictures.md)
and doesn't need MSU-1. Starting with the `.msu` is not recommended: 4 bpp
with 105 colors is enough for taro to judge by eye.

## 5. Recommendation by phases

**Cutscenes first.** They are story and ask little of the engine:
pictures, two planes and a couple of opcodes. The console additionally
asks for four interpreter pieces and doesn't change the game; it goes
after, on top of the cutscenes, and the custom menu in mode 5 after it.

**The converter chooses the plane, picture by picture**, the way it
chooses the VRAM layout: objects if it fits in the map's sprite bank (or
in the hidden events' one), BG1 in mode 1 if not. The ROM decides
nothing.

The generic goes in `tools/` —it knows nothing of ABL—; ABL's, in `rom/`:

1. **`Label` and `JumpToLabel`** (`tools/rm2k-snes/events/`). An
   `OP_GOTO` with a resolved target. Small, adds 8 map pages and belongs
   to the console.
2. **Several pictures, in objects** (`tools/rm2k-snes/images/`,
   `tools/port/picture.py`, `tools/runtime/picture.s`, `events.toml`).
   It generalizes the existing one: RM2k 2000's picture numbers (1 to 20)
   with a palette each, the ones each map shows reserved in its sprite
   bank, position —constant or resolved through constants—,
   `MovePicture` of position and tone, the transparent color, and erasing
   on a map change. It adds the signs on 81 and 295, Ready, ABLrec, the
   opaque smoke, the counter's label and the shadow on 311.
3. **The background plane: BG1 in mode 1** (`tools/runtime/`,
   `rm2k-snes-images` with Adeleine for the 7 palettes, the VRAM layout
   in `tools/rm2k-snes/mapdata/`). The large picture with the map hidden,
   reloading the map when it is erased, and the waves by HDMA. It adds
   ABLEndBox8, EscapeInst, AdvoInstr, the four *Diff* (with the zoom as a
   fade) and GTest4/ShipFlash. **With 2 and 3 every cutscene picture is
   drawn except the montage on 217**, with the translucency debts written
   in `divergencias/`.
4. **Autostart common events and the shared `CallEvent`**
   (`tools/rm2k-snes/events/`, `tools/runtime/interpreter*.s`). One body
   per common event in the ROM, the switch checked when refreshing pages,
   and `OP_CALL`/return with a short stack. Along the way it adds Radin's
   and Sern's menus and Emily's tape, if their maps are in the cartridge.
   The parallel ones are left for another task, because of
   `DisableSaving`.
5. **`\V[n]` in messages** (`tools/rm2k-snes/events/`, the runtime's
   text composed on the fly). Three messages, all three the console's.
6. **The portable console** (`rom/`: the highlight patch, the test case
   and its golden). With 1 to 5, it compiles on its own: the main window
   in objects —with the events hidden if the map leaves no room—, the
   pages and the aura table in the background plane with the black frame.
   A test that opens item 81 from the menu and walks through Talan, his
   auras and a tutorial.

After that, [`custom-menu-of-our-own-not-made-of-pictures`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/custom-menu-of-our-own-not-made-of-pictures.md): the same menu, described
as data and drawn in mode 5 with a font, which is what really fixes the
text pages.

## How it was measured

All with throwaway Python scripts, from the root of the repo:

* **The commands**: walking `rom/data/maps/Map*.json` (each page),
  `rom/data/db/commonevents.json` and `rom/data/db/troops.json` for codes
  11110, 11120 and 11130. The troops have none. The command names, from
  `tools/rpgmaker/event_codes.json`; the parameter indices, from
  easyrpg-player's `CommandShowPicture` and `CommandMovePicture`.
* **The pictures**: the ones in the game's `Picture` folder, with Pillow:
  size, distinct colors, fraction of pixels of index 0.
* **Who opens the console and who reads what it writes**:
  `ControlSwitches`, `ControlVars`, `KeyInputProc` of the console's common
  events against page conditions, `ConditionalBranch`, `ControlVars`
  operands and `\V[n]` in all the rest of the game; the switch-type items
  in `rom/data/db/items.json` and the `ChangeItems` of 81 and 150.
* **What compiles**: a fake `Map0004.json` with one autostart page per
  whole common event and one per each distinct command of each common
  event (branches with their closing), passed to `rm2k-snes-events scan`
  through `map_files`; the `compiled` field says it by event index, from
  0. The stray `ShowMessage_2` that don't compile are an artifact of the
  test.
* **The weight**: each picture at the zoom it is shown with, rescaled with
  LANCZOS to 256/320 x 224/240, cropped to the screen, reduced with
  Pillow's `quantize` (MEDIANCUT, no dithering), cut into unique 8x8 tiles
  with flips, at 4 or 8 bpp planar, with the 2-byte-per-cell tilemap, and
  compressed with the installed `lz2` in streams of up to 64 KB.
* **What freezes**: each page's trigger and, on the same page, the last
  `TintScreen` before the `ShowPicture`.
