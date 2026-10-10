# Autofire of A with X

## What

Holding X presses and releases A by itself: `pad_a` spends
`AUTOFIRE_FRAMES` rounds on and as many off, and since the game looks at A's
edge —RM2k closes the message with `Input::IsTriggered`—, each return to on
is a press. It is for going through text and repeating choices without
mashing the button. It is all in `read_pad` (`tools/runtime/control.s` in
the-advocate), which is the only place that reads the controller, so it works
on the map, in messages, in menus, in the shop, in battle and on the title
screen.

RM2k has nothing like this: it uses two buttons, and the SNES controller has
many more. It is a divergence that **only adds**, because in RM2k there is
no button that corresponds to X; it is written down so that nobody takes it
for a bug or "fixes" it. It is taro's idea, from 2026-09-25.

**Only A, with X.** An autofire for B was ruled out: on the map B opens the
pause menu and inside it B closes it, so holding it would open and close it
endlessly.

What was decided on the line, and is commented there:

* **The real A wins.** It is combined with an OR: A and X together is
  holding A, on and with no edges.
* **Releasing X leaves nothing stuck and does not press extra.** The next
  round writes only the real A, so at most it switches off a `pad_a` that
  was on.
* **The first frame with X already presses.** Releasing X resets the
  counter, so every time it is pressed it starts in the on phase.

## Measured

With `AUTOFIRE_FRAMES` at 4 it is four frames on and four off: 7.5 presses
per second. taro asked for between 3 and 4 to start with, and it is a named
constant to be tuned while playing; it has to be a power of two, and an
`.assert` guards that.

It is covered by `pruebas/rpgmaker/test_autofire.py` in the ABL port
(the-advocate-ports/abl): the rhythm frame by frame, that the real A wins,
releasing X in each of the eight phases, and the `autofire` case —five
messages in a row— closed entirely with X held and only one with A held.
`test_cores.py` runs the same case on both cores.

## How to reproduce it

In any message, hold X: they close one after the other.
