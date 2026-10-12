# What erasing an event does not model

## What

`EraseEvent` **is there** —`OP_ERASE_EVENT`, with `FLAG_ERASED` in
`ev_flags`—: the event that runs it is not drawn, does not block, and none of
its pages start, until the map is loaded again; if the one running it is a
parallel page, it ends there. And it leaves out what RM2k does do or does
take care of:

* **It does not travel in the save.** The erasure lives in `ev_flags`, which
  `clear_waits` clears on every map load, and loading a save loads the map:
  an erased event comes back. It is the same gap as
  [The save does not keep the events](the-save-does-not-keep-the-events.md).
* **A forced route that is already moving it is not cut.** The route of its
  page is taken away and its row is hidden, but a forced `MoveEvent` that
  was walking stays in its slot and draws it again.
* **An event without a graphic keeps occupying its cell** for whoever looks
  at `ev_pos_buf` —the action button looks at the cell and finds no page—;
  there is none in the game that needs it.
* **"This event" is erased and nothing else.** `EraseEvent` in RM2k takes no
  parameters, so that is all there is; in a common event it does nothing,
  same as there, and after a jump to another map neither.

## Measured

`rm2k-snes-events culprits --every-map` on Desert Nightmare: `EraseEvent` was
the command that left the most pages out on its own (127 of the 157 that use
it), and it no longer leaves any. All 157 are parallel pages without a
graphic.

## How it looks today

It is not seen. `pruebas/rpgmaker/test_borrar_evento_de_verdad.py`, in the
ABL port (the-advocate-ports/abl), enforces what the test event lets you look
at —that a foreground page keeps going, that the others do not start, and
that reloading the map brings it back—; what is drawn, what blocks and the
parallel page that gets cut are covered by playing the cartridge of a game
that erases events with a graphic.
