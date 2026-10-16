# What faces do not model

## What

`ChangeFaceGraphic` gives the message window a face —48x48 out of a
FaceSet, on the left or on the right, mirrored or not— and every box from
then on draws it, until another command changes or clears it. Since
2026-10-15 the console draws it:

* **Its tiles go in the window's own text cells**, where RM2k draws it:
  cells 1 to 6 of text rows 1 to 6 on the left, 23 to 28 on the right. The
  text starts 72 pixels in with a face on the left —RM2k's `LeftMargin +
  FaceSize + RightFaceMargin`— and stops where the face starts with one on
  the right. The composer copies the face's tiles into the line's buffer
  after priming its background, as it composes a letter. A face costs the
  window no VRAM.
* **Its colours go in BG palette 1, on the window's lines only.** The text
  is palette 0 and the map owns every other entry, so an HDMA channel
  writes the face's fifteen colours on the window's first fifteen lines,
  one a line, before the face starts, and puts the map's own back on the
  fifteen lines after it ends, from the shadow of the colour memory, tinted
  as they are on screen. A face costs the map no colour.
* **Each face the game names is drawn once by the converter**: cut from its
  FaceSet, mirrored if the command asks, reduced to fifteen colours the way
  the slot screen reduces an actor's face, 1,152 bytes of tiles and 30 of
  palette. Vampires Dawn's 88 faces are 104 KB of an 8 MB cartridge.
* **A box compiled after a face is set is laid out for the room the face
  takes**, 168 pixels a line instead of 240: a box that no longer fits in
  one window becomes two, one key press each, as any box the console's
  narrower window splits.

What does not come out as in RM2k:

* **A face in a window without its background recolours the map under
  it.** With a background, nothing of the map shows on the window's lines
  and the palette swap shows nowhere. Without one the map is visible on
  those lines, and whatever pixels of it use colour entries 17 to 31 take
  the face's colours for the 80 lines of the window. Desert Nightmare asks
  for 7 bare windows in all, Dooms 2 for 3, Vampires Dawn for 37.
* **The face's transparent pixels do not show the window behind them.** A
  4bpp cell is one palette, and the face's cells are palette 1: a
  transparent pixel takes the colour the window's background has where
  RM2k draws the face, and is then one of the fifteen. Over a window with a
  background it looks the same; over a bare one it is a square of the
  background's colour instead of the map.
* **A face has fifteen colours**, and a FaceSet face can have a hundred:
  Adeleine merges them, the least visible first, as for the slot screen.
  The RTP's faces have 125 to 150 colours each, and lose their finest
  shades.
* **The box's width is decided when building, and the face when playing.**
  RM2k's face is one state the whole game shares, and a page that shows a
  box without naming a face shows whatever the last page left. The
  compiler walks each page in order and knows the face after a
  `ChangeFaceGraphic` in it; before any, it does not. In a game that shows
  faces at all it lays those boxes out for a face anyway —in Vampires Dawn
  2,160 of the 2,686 pages with a face command end with one still set, so
  the leaked face is the likely one—, and a box that in RM2k had the whole
  line comes out laid out for 168 pixels: more boxes, nothing lost. A page
  that cleared the face gets the whole line. The other way round, a face
  set in one arm of a branch and not in the other leaves the compiler with
  the last one it saw: a line laid out for the whole window under a face is
  cut at the window's edge, where the composer cuts every letter that would
  paint past it.
* **The face does not travel in the saved game.** RM2k saves `Game_System`'s
  face; here a loaded game starts with none, until the next
  `ChangeFaceGraphic`. The window's other options do not travel either.
* **The colours written back after the face are the ones on screen when the
  box opened.** A tint that changes while a box with a face is up —a
  parallel event's— reaches the map above and below the window at once, and
  the window's lines at the next box.
* **A choice's highlighted bar runs under the face**, since the bar is the
  line's background and the face is copied over it: with a face on the
  left, the bar shows in the cell before the face and from the text on. RM2k
  starts the cursor after the face. `InputNumber`'s digits do not move for a
  face either.
* **`ChangeActorFace` changes nothing**: it is accepted as a debt, so its
  page runs —Frozen World's 7 pages, Vampires Dawn's 5, Dooms 2's 1—, and
  the slot screen and the menu keep showing the database's face, which they
  bake into their bank per actor. It is `actor-face-not-changed` in the
  cartridge's degradations.
* **A FaceSet that is neither the game's nor the RTP's** gives a face of the
  window's background alone, blank, with the text still moved over for it,
  and a `face-missing` degradation.
* **Writing the colour memory in the horizontal blank is "fragile" on the
  real console** (fullsnes's word): one colour a line, which is what this
  does, is what commercial games did; the prototype that measured it in the
  research wrote up to eight in snes9x, bsnes and Mesen-S. It is not yet
  seen on taro's console.

## Why

No game of the eight puts the face on the right or mirrors it —measured
over every page of their dumps on 2026-10-15—, and three use it at all:
Desert Nightmare on 1,848 boxes, Dooms 2 on 717, Vampires Dawn on 8,100.
The window's 256 tiles are fixed in every VRAM layout and its palette has
no room, so a face had to cost neither: the text cells it covers are free
because the text moves over, and the window's lines are the only place
where the map's colours can be borrowed without showing. The alternatives
—sprites, hidden on the window's lines by the object mask that keeps the
characters under the window; a reserved palette, which eleven of A Blurred
Line's maps already lose colours to the window for— cost VRAM or colours
on every map for three games. The measurement is in section 4 of [The
windows, made cheaper](../research/2026-10-11-the-windows-made-cheaper.md),
and the task is
[`draw-the-faces`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/draw-the-faces.md).

## How it applies

`OP_FACE` is in `rm2k-snes-bytecode`, and its arm in the event compiler's
`compile.rs`, with `Ctx::face` and `box_faced` deciding the width; the
faces are swept by `indices::faces`, drawn by `faces.rs` in
`rm2k-snes-screens` and emitted as `message_face_N` and `message_face_ptr`
by `rm2k-snes-mapdata`. In the runtime everything is in `message_face.s`,
with hooks in `messages.s`, `vblank.s`, `interpreter_message.s` and the
reset. The test game's `test_faces.py` shows the five boxes.
