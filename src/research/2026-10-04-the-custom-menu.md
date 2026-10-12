# The custom menu: the portable console as data and not as pictures

> **Written on 2026-10-04 at `43b552f5`** (snes-rm2k), by Lagartija, with
> ABL at `5b29ba9`. It is a snapshot: the numbers are from that day and this
> file is not updated. How to redo each count is at the end, in "How it was
> measured". The captures of the original and the mockups were delivered
> separately: see `workflow/tasks/*/el-menu-custom-de-la-consola.md`.

## Summary

* **The console is not needed to progress, but it is needed to play well.**
  The fifteen common events that make it up (39, 40, 21 to 31, 48 and 49)
  only use jumps, switches, variables, pictures, messages, sounds and
  `KeyInputProc`: no item, party, skill or teleport. They write 17 switches
  and 10 variables and **nobody outside them reads any of them** —measured
  over the common events, the 2,656 places in the maps and the troops—. What
  is lost without it is information: each character's guides and the
  counters —how many times Talan absorbed each technique and how many he has
  left, Sern's souls, Saldra's and Lerle's techniques—. Auras **are not
  chosen** there: the table only reads variables 70 to 122, which battles
  write.
* **Almost everything is text.** Of the 61 pictures, 13 are pages of white
  text on black, 6 are aura tables with the names and the "how many are
  needed" painted in, 26 are the tables' numbers, and 3 are the window and
  its highlights. **Real art is 10 portraits**: the other three (Radin,
  Drago and Sern) are a "Picture Unavailable" sign.
* **The proposal**: an engine screen, **a custom menu described as data**
  —System windows, composed variable-width text, lists with a cursor,
  numbers that come from variables, and the actor's face or a portrait—,
  opened from **one more option in the pause menu** and **always full
  screen**, like the items menu. The game declares it in a file of its own
  named by `rm2k-snes.toml`, and it hooks into the event logic from two
  sides: it replaces the common event that opened the picture menu —so item
  81 keeps working— and it can run a common event before drawing a page, for
  the counts that common events 48 and 49 do today.
* **It costs little**: a few KB of text and tables, about 2 KB of code
  —estimated— that reuses the text layer and the screens' windows, and
  **zero or 48 KB of art**, depending on whether the faces the cartridge
  already carries are used or the ten portraits at 4bpp. The console's
  pictures were **128 to 208 KB**
  ([`2026-10-01-el-sistema-de-imagenes.md`](2026-10-01-el-sistema-de-imagenes.md)).

## 1. The inventory

Looked at in the original, with the 2015 RPG_RT running under Wine on a
copy of the game whose map 4 builds a party of four —Talan, Sern, Emily and
Arden—, turns on 133, sets a few aura counters and Sern's souls to 42, and
opens the console in Talan's apartment. And by reading the common events in
the dump.

### How it works

Item 81, *Portable Console*, is a switch item: it turns on 710, which
triggers common event 39, an autostart. 39 is a state machine made of
`Label`/`JumpToLabel` and `KeyInputProc`, which draws a window over the map
—the map can still be seen around it— with three pictures:

    17  NewMenu<name>     the portrait on the left and the "Skills" and
                          "Tutorials" labels, at 50%
    18  SkillSelect or    a red rectangle at 50% over the chosen label
        TutorialSelect
    19  ArrowTest         two arrows: ↑↓ on the right and → at the bottom

* **Left and right** go through the characters **in the party**, in an
  order fixed by the common event —Kersh, Manta, Core, Talan, Saldra, Arden,
  AG7-17, Dalia, Radin, Lerle, Sern, Drago, Emily, Kersh2—; each one turns
  on its switch (712 to 725). Left actually does nothing: it only makes a
  sound.
* **Up and down** choose "Skills" (856) or "Tutorials" (857).
* **A** opens the page; **B** closes the console (`EraseAllPictures` and
  710 off).
* **When coming back from a page** the common event jumps to label 20 and
  from there to 15, which **chooses the party's first character again**:
  after reading Emily's guide, the console is on Talan again. It shows in the
  captures; it does not look intended.

### Page by page

Fixed means painted in the picture; variable, that it comes from the state.

**The main window** (`NewMenu<name>`, 302x202 at 50%):

* art: the portrait, about 150x188 pixels of the original; ten characters
  have it, Radin, Drago and Sern have the sign;
* fixed: "Skills", "Tutorials" and the arrows;
* variable: which character (those in the party) and which label.

**The guides** ("Tutorials", `<name>Tutorial1`, 301x202 at 100%, white on
black, they cover almost the whole screen):

* all fixed: a paragraph of four to twelve lines. There are ten —Talan,
  Arden, Emily, Lerle, Radin, Sern, Saldra, Kersh2, AG7-17, and a second one
  for Talan—;
* variable: **which one**. Talan has two and chooses by switch 133: without
  it, it says he "does not have special systems"; with it, it explains
  DETECT AURA and ABSORB AURA. Manta, Core, Drago and Dalia have none: a
  message says "There is no tutorial screen available for MANTA at the
  current time."

**The skills** ("Skills"), which are five different things:

* **Talan, with 133 on**: the aura table, common event 21. Six tables, one
  per color —Blue, Red, Green, Yellow, Black, White—, gone through with left
  and right, in a circle. Each one is a full-screen picture with the title,
  eight technique names and "/ N", what is needed to learn it —fixed—, and
  on top of it eight 12x13 numbers in separate pictures: **how many times he
  absorbed it**, one variable per technique (70 to 77 the blue one, 79 to 86
  the red one… up to 115 to 122 the white one). From 0 to 24 it draws the
  number; **99 draws a dash**, which is what the game sets when the
  technique is already his. B goes back.
* **Talan without 133**: a fixed page, "TALAN does not have any skills."
* **Emily and Arden**: a fixed page each —Emily's per-tape radio effects,
  Arden's per-level techniques—.
* **Sern, Saldra and Lerle**: a message with a variable. Sern's says his
  souls, 173, which battles write. Saldra and Lerle **compute it when
  opening**: common events 48 and 49 count how many of certain techniques
  the actor knows —with "knows the skill" `ConditionalBranch`es— and put it
  in 195 or 196: "SALDRA has learned 3 of the 8 skills necessary…".
* **The rest**: a message, "There is no skill screen available for RADIN at
  the current time."

No counter is written from the console: it reads them. The only state the
console keeps is where the cursor is, in its own switches.

## 2. The design

### What taro decided

* **It is one more option in the pause menu**, next to Items, Skills,
  Equipment, Save and End Game, with the label the game declares
  ("Console", "Guide"…): "having it in the menu already would make it more
  unified and maybe simpler, too".
* **Always full screen**: "this system does not allow rendering over the
  map. That way we solve VRAM challenges etc." Like the pause menu, which
  already covers the map and restores it when it closes.
* It is an engine feature, of RPG Maker 2000 PLUS
  ([`decisiones/rm2k-plus.md`](../decisions/rm2k-plus.md)): ABL uses it, any
  game can use it.

### What it is: a screen the engine walks through

A custom menu is a **short tree of declared screens**, which the engine
draws and navigates on its own, with the rules of the screens it already
has:

    menu            the label in the pause menu, when it appears, which
                    common event it replaces
      subjects      a list: who or what is looked at —an actor in the
                    party, or a fixed entry—, with its art and its condition
        tabs        what can be looked at for each subject: "Skills", "Guide"
          page      what is seen: the first in its list whose condition
                    holds; none, and the tab comes out grey

**A page is of one of three kinds**, which are what ABL's console and the
known picture menus use:

* **text**: a paragraph, which the converter splits to the window's width
  with the game's font —the same it does with messages—, with `\V[n]` for a
  variable and `\N[n]` for an actor's name. If it does not fit, it scrolls
  with up and down.
* **table**: rows of *name, value and cap*: the value is a variable, the cap
  a constant or another variable, and the table declares what is written in
  place of a special value —the auras' 99 as "Learned"—. A table can have
  **sheets**, gone through with left and right: the six aura colors are a
  table of six sheets, each with its title and its font color.
* **counters**: two or three rows of "label … number", above a text. It is
  Sern's page; with a common event before, Saldra's and Lerle's.

**The colors are the System's**, as on every screen: red for labels —the
color of "HP" and "L" in the menu—, grey for what is not there —the
technique already learned, the tab without a page—, and the rest for
whatever the game wants, like each aura's title in its color.

### How it is navigated

Like the original, which is what ABL's player already knows, and with the
pause menu's keys:

* **Left and right**: the previous and the next subject —in a table with
  sheets, the sheet—. The header says "< 2 / 4 >".
* **Up and down**: the tab, with the System's bar; on a long page, it
  scrolls.
* **A**: opens the page. **B**: goes back one level; from the subjects, to
  the pause menu, with the cursor on the option.
* **When coming back from a page it stays on the same subject**: which is
  what the original did not do.

### How a game declares it

**In a file of its own, named by `rm2k-snes.toml`**:

    [menus]
    # Each custom menu, by the file that describes it. See
    # docs/research/2026-10-04-el-menu-custom.md.
    console = "menus/consola.toml"

And the file, abridged:

    label = "Console"
    # It appears in the pause menu only with item 81 in the inventory: that
    # is when the original lets the console be used —the game takes it away
    # and gives it back around Radin's and Sern's menus—.
    visible = { item = 81 }
    # The common event that opened the picture menu: opens this one.
    replaces_common = 39

    [[subject]]
    actor = 14                      # Talan; shows up if he is in the party
    art = "picture:NewMenuTalan"    # or "face", the actor's
    crop = [6, 6, 150, 188]

    [[subject.tab]]
    label = "Skills"
    [[subject.tab.page]]
    when = { switch = 133 }
    table = "auras"
    [[subject.tab.page]]
    text = "TALAN does not have any skills."

    [[subject.tab]]
    label = "Guide"
    [[subject.tab.page]]
    when = { switch = 133 }
    text = """TALAN can equip clubs and other similar weapons. …"""

    [[table.auras.sheet]]
    title = "Red"
    color = 1
    rows = [["Candle Flame", "v79", 5], ["Minor Fire", "v80", 5], …]
    special = { 99 = "Learned" }

    [[subject]]
    actor = 17                      # Saldra
    [[subject.tab]]
    label = "Skills"
    [[subject.tab.page]]
    before = { common = 48 }        # counts the techniques into 195
    counters = [["FD techniques", "v195", 8]]
    text = "SALDRA can learn more techniques by reading …"

The conditions are **those of RM2k's pages** —switch, variable `>=`, item
in the inventory, actor in the party—, which the event compiler already
knows how to compile: there is no new condition language.

**Why a file of its own and not something else**:

* **Not in `rm2k-snes.toml`**: it is dozens of paragraphs of text, and that
  file is for knobs and short lists. Only which menus there are goes there.
* **Not in the common events**, as comments or new commands the editor does
  not know: the game would have to rewrite its state machine to draw text
  instead of pictures, and navigation would again be in the hands of each
  game, which is what made the original ugly. And the dump is derived: what
  is ours lives next to it (`parches/README.md` in ABL).
* **TOML**, like the rest of the project, and the game **transcribes** the
  text of its pictures: it is the only step that is not automated, because
  reading text from an image is guessing. For ABL it is thirteen pages and
  six tables.

### How it connects to the events

* **The replaced common event** (`replaces_common = 39`): the compiler does
  not compile its body, but a new opcode, `OP_MENU_OPEN menu`, and **turns
  off its switch**, because an autostart that does not turn it off runs
  forever. Item 81 turns on 710 as always, and 710 opens the custom menu:
  the item still works, and the pause menu option is the other door. That
  way no patch of the item is needed, and a game that does not declare
  `replaces_common` touches no event.
* **What 39 calls is left uncalled**: 40, 21 and 23 to 31 only drew. **The
  ones that compute** —48 and 49— are named as their page's `before`: the
  engine runs them with the same shared body common events already have
  (`OP_CALL`, `commons.rs` in `rm2k-snes-events`), without pictures or
  messages, and then draws.
* **The menu does not write game state**: it only reads. Switches 712 to
  725, 856 and 857 are left unused, which is the same that happened with
  the original for the rest of the game.

**Why the engine navigates and not the events.** The other option was to
leave the logic in the common events and add opcodes to draw text —a "text
picture", as other RM2k patches do—. It is discarded because the console's
state machine **has no game logic**: it only exists to imitate a menu with
`KeyInputProc`. Declared, the menu is navigated the same as the pause menu,
the cursor is not lost when coming back from a page, and another game uses
it without programming events. If a game needs an entry to **do**
something —a quest menu that marks one—, the next step is a row with
`action = { common = N }` that runs that common event on A: the same
mechanism as `before`. ABL's console does not ask for it.

### For other games

What the feature does not assume from ABL: subjects can be actors or fixed
entries —a bestiary, a diary, a quest menu—; the conditions are RM2k's; art
is optional; tables read any variables. What a game with a picture menu
does to port it is the same as ABL: transcribe the text, declare the pages
and name the common event it replaces.

## 3. Full screen: what the whole VRAM gives

With the map covered, the screen has the whole VRAM, like the pause menu and
battle, and when it closes the same load that comes back from the menu
restores it. That is enough for everything without splitting:

* **The text on BG2**, with the screens' text layer
  (`tools/runtime/text_layer.s`): up to 447 tile pairs, a screen with all
  its cells inked.
* **The windows on BG1**, with the System's frame and background at 8bpp,
  like the items' ones (`screen_bank.s`): the converter builds one tilemap
  per window layout —there are four: the subjects one, the text one, the
  table one and the counters one— and the cursor bar as today.
* **The art in objects**: the 512 object tiles belong to the menu while it
  is open, because the map's characters are not visible. A 96x120 portrait
  is 180 tiles; a 128x160 one would fit (320). And objects have **eight
  palettes** of 15 colors, which Adeleine distributes per block as it does
  for small pictures: a portrait of up to 120 colors without touching the
  windows' or the text's CGRAM.
* What is lost compared to the original: **the map is not seen around it**.
  That is the decision.

## 4. The mockups

Drawn with `rm2k-snes-screens` as a library —the window and the cursor of
ABL's System (`Skin::window`, `Skin::cursor`), its variable-width font with
spacing 1 (`Skin::draw_line`), and the pause menu from `render::menu`—, at
256x224 and at 15 bits, side by side with the capture of the original:

1. **The pause menu** with "Console" between Equipment and Save.
2. **The console on Talan**: the header with "< 1 / 4 >", the portrait on
   the left at 96x120, the name and the class, the tabs with the bar, and
   below, what there is in the chosen tab.
3. **Talan's guide**: `TalanTutorial2` as text, split to the window's width.
4. **The red auras**: "Aura skills - Red" with "< 2 / 6 >", the eight rows
   of *name, absorbed / needed*, 99 as "Learned" in grey.
5. **Sern's souls**: a counter and the text of the original message.

The numbers in the mockups are those of the test save, not of the game. The
technique names go separated ("Candle Flame") and not joined as in the
picture ("CandleFlame"): the game decides that when transcribing.

## 5. What it would cost

**ROM**:

* **Text and tables**: the thirteen pages are about 4 to 6 KB of letters,
  and the six tables about 700 bytes of names and caps —estimated over what
  was transcribed for the mockups, not measured in full—. Plus the tilemap
  of each window layout: 1,792 raw bytes each, which is a property of the
  screen —32x28 words—, and almost all repeated.
* **Art**, measured over the thirteen `NewMenu*` cropped to 96x120, in
  deduplicated 8x8 tiles, with the tilemap and the colors, with LZ2:

      no art, or the actor's face             0      the face already goes in
                                                     the cartridge, for the menu
      13 portraits, 4bpp, 15 colors       48 KB      1,974 tiles
      13 portraits, 8bpp, 96 colors      100 KB      2,017 tiles

  The three "Picture Unavailable" signs would not have to go in: a subject
  without art uses the face.
* **Code**: a new screen, which walks the pages, composes with the text
  layer and paints the bar with the items' code. For scale, the whole items
  screen is 618 bytes and the pause menu 641 (measured in `release`'s
  `.dbg`), so **about 2 KB** outside bank 0, with `jsl` like
  `screen_bank.s`. In bank 0, what adding an option to the pause menu adds:
  a few bytes, which have to be measured with `just espacio` because that
  bank is the tightest.
* Against **128 to 208 KB** for the 61 pictures in the ROM (the 2026-10-01
  study), or the `.msu`.

**RAM**: the screen's state —menu, subject, tab, sheet, first visible row
and which level it is at— is about 8 bytes, which can be the borrowed
`pick_*` as the items screen does, because no message is open with the
menu. The text layer uses its own (`FAR_TEXT_LAYER`) and its staging in
`ANIMB_BUF`, like any screen.

**VRAM**: all of it, while it is open, and nothing on the map.

**Opcodes**: one, `OP_MENU_OPEN`, for the replaced common event. The pause
menu option asks for none. `before` reuses `OP_CALL`.

**What is reused from the runtime**:

* the pause menu: `menu_screen`, its option list and the return to the map;
* the screens' text layer: `scr_text`, `scr_number` and the right-aligned
  number (`tl_right`), and composing only what changed;
* the windows and the cursor bar from `screen_bank.s`;
* the shared common events, for `before`;
* and the small pictures' object loading, for the art.

**What is reused from the converter**: the messages' box splitting for the
text (`boxes` and `refit` from `rm2k-snes-screens`), the windows as a
tilemap (`borders.rs`), Adeleine and Voodoo for the art, and `render` for
each page's golden, which is how the other screens are tested.

## What was not decided

* **The art: face or portrait.** The face costs nothing and is already seen
  in the pause menu; the portrait is the only pretty thing the original had.
  The mockups use the portrait.
* **The label**: the menu's column is nine cells, 72 pixels
  (`MENU_OPT_COLS`). With ABL's font and its spacing, "Console" measures 39
  and fits; "Portable Console" measures 88 and does not. "Guide" fits too.
  The converter already warns when a label is cut.
* **What happens with the option without subjects**: if the party has
  nobody the menu knows, the option could come out grey, like Tech Skill
  today.

## How it was measured

* **The common events**: a walk of the `CallEvent`s from 39 in ABL's
  `data/db/commonevents.json`, collecting the command codes, the switches
  and variables they write and the pictures they show.
* **Who reads what they write**: the maps' page conditions, the common
  events' triggers, the troops' conditions and, in all the commands of maps,
  common events and troops, switch and variable `ConditionalBranch`es, the
  `ControlVars` operands by variable, the indices by variable and `\V[n]`.
  With all switches and variables set as the target, the same walk finds
  2,656 places in the maps: the walk looks where it has to look.
* **The original**: the 2015 RPG_RT with Wine and Xvfb, over a copy of the
  game with map 4 rewritten with Ditto (an autostart page that builds the
  party, turns on 133, sets variables, gives item 81, takes you to map 7 and
  turns on 710), and `xdotool` for the keys.
* **The mockups**: a throwaway program with `rm2k-snes-screens` as a
  dependency, with ABL's dump and game and its `[text]`.
* **The art's weight**: each `NewMenu*` cropped to (6, 6, 150, 188),
  rescaled with LANCZOS to 96x120, reduced with Pillow's `quantize`
  (MEDIANCUT, no dithering) to 15 and to 96 colors, in unique planar 8x8
  tiles, with the tilemap and the colors, compressed with the installed
  `lz2`.
* **The code**: the `scope`s with `size` from `release`'s `abl.sfc.dbg`.
