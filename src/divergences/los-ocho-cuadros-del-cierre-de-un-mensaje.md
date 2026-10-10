# The eight frames of a message closing

## What

In RM2k the message stays **"active" while the closing animates** —about
eight frames, easyrpg `window_message.cpp:379-403` and
`window_message.h:216-218`— and during that time the hero does not look for
events, a waiting `KeyInputProc` does not read the pad, and the parallel
event that opened it stays stopped.

**Here the window switches off at once.** What was copied is that **the A
that closes it** is not seen by anyone else: `wait_button` consumes it, and
the tests in `pruebas/abl/test_piedras.py` in the ABL port
(snes-rm2k-ports/abl) enforce it. What is left out is that **a new A**
pressed within those eight frames does count here —it talks to whoever is in
front, or pulls a stone— and in RM2k it does not.

## Measured

For a person that is **two presses within 130 ms**, so it is not noticeable
while playing.

## How it looks today

Nothing tests it.
