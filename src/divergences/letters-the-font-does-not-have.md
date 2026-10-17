# Letters the font does not have

## What

RM2k's font has Latin-1 —`é`, `ñ`, `¿`, `ü`, `ß`— and RPG_RT draws
Windows-1252's few extras too, like the ellipsis `…` and the curly quotes.
The console's font draws printable ASCII and, since 2026-10-16, Latin-1 in
the message boxes:

* **A message box draws the Latin-1 letters its game uses**, with their own
  glyphs —an accented letter is the font's letter with the accent on top—.
  The cartridge carries only the ones its boxes use, at most 32 —how many,
  its `MESSAGE_PAIR_FIRST` in the build's `mapdata.inc` says, minus 96—; a
  game in English carries none, and its cartridge is the same as before
  there were any.
* **Any other letter is shown as its plain ASCII stand-in**, the one a
  reader would write without the key: `é` as `e`, `ß` as `ss`, `¿` as `?`,
  `…` as `...`, `Œ` as `OE`. That is every letter in a box past the 32, in a
  font that does not draw it —RM2k's own fixed-width ones, a game's sheet
  without Latin-1, and the four `low-variable` leaves out, `®`, `¾`, `Ø`,
  `ø`—, every Latin-1 letter in a **troop page's box** —the battle draws
  those with the text screens' glyphs, so in Zounds every battle's talk is
  plain—, and the characters past Latin-1, like Sunset's `…`.
  Each command whose box shows one is listed in the build's
  `degradations.json` as a `letter-plain` loss, with the letters and what is
  drawn for each, and the converter prints one `WARNING, letter-plain` line
  with all of them.
* **The text screens show the stand-ins**: the menu, the shops, the battle,
  the slot screen and a name written when a box opens —`\N[0]`, a renamed
  actor— draw ASCII, so Zounds' hero, Unamë, is Uname there. A name baked
  into a box —see [What names in messages do not model](what-names-in-messages-do-not-model.md)—
  is part of the box's text, and keeps its `ë`.
* **A character with no stand-in** —a katakana, a symbol outside
  Windows-1252— still leaves its page out, as until 2026-10-16 any letter
  outside ASCII did.

## Why

Until 2026-10-16 a box with a letter the font did not have left its whole
page out. It was chosen on 2026-10-05, when the only such letter known was
Sunset over Imdahl's `ô`: one page out was better than stopping the
conversion. Measured on the nine games, it was most of the talk of the ones
in Spanish and German —950 map pages of Zounds and 166 of Vampires Dawn—,
and it was where Zounds' intro stopped, on a talk with `é`, `¿`, `¡` and
its hero's `ë`. taro's rule for the ports is to unblock the whole game
first, so the stand-ins came first, and the glyphs after, the same day.

The cap of 32 is the composer's: a letter's index has to stay below 128,
because the second letter of a pair waits in `FAR_MSG_SECOND` with bit 7
set. Each letter carried takes one value
of the pair table, so a game with letters writes its text with a few pairs
fewer, and its window's tables grow by the letters' glyphs.

## How it applies

The stand-ins are `plain` in `rm2k-snes-text`, and the glyphs the last six
rows of `low-variable.png`, derived from EasyRPG's `rmg2000` by the rules of
the rest of the sheet —see the fonts' README in `rm2k-snes-text`—. A font
says which it draws with `Font::latin_letters`, and the converter hands them
to the event compiler with the message window. The compiler's first pass
draws all of them and counts which the boxes use
(`Messages::letters_used`); the second draws those —`Window::carrying`—, and
`Messages::store` stands the plain ones in for the rest before trimming the
line. The letters go to the screens stage in `messages.letters`, whose
glyphs `font_bytes_with` puts after the console's 96 in the message
window's tables, and the pairs start after them, `MESSAGE_PAIR_FIRST`.
Tested by the test game's `test_plain_letters.py`, a box with letters drawn
and letters plain, and the ports' `test_zounds.py`, the talk with the
guards on map 8 that goes on to map 9. Task:
[`latin-1-letters-stop-a-box`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/latin-1-letters-stop-a-box.md).
