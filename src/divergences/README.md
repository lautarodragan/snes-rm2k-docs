# Divergences: where the ROM does not do what RM2k does

One page per divergence: **what the ROM does, what RM2k does, what was
measured, and how to reproduce it**. It is description and not wish —what
we would like to do and nobody is doing is the wishlist, in `tasks/wishlist/`
in the-advocate-work—, and it is not an open red: none of these fails today.
Several come from the time when the Python reference existed, and since
2026-09-16 the golden is a capture of the ROM itself, so **it bakes in the
behavior the reference disputed**. That is, these are places where we know
the ROM differs and nothing catches it. They are written down for that
reason, and because the day one of them is fixed there are goldens that will
move and someone will want to know why.

What does **not** go here: what the test run does not look at but nobody
says is wrong, what is left to do in the port —that is `tasks/`, in
the-advocate-work— and the differences between emulators, which are not the
ROM's. Nor a divergence that is **decided and closed**, one the port allows
itself on purpose and has no plans to undo: those live where the decision
is, with the code or in [the decisions](../decisions/README.md). What goes
here are the ones still open, even if nobody is working on them.

**Except the ones that hold because *A Blurred Line* is the way it is.** The
horizon is a `migrar-rm2k-a-snes juego.zip juego.sfc` that works without
tightening any screws, and several of the port's choices are not general:
they work because of how this game is. Those go here even if they are
decided, with the number that justified them and a section **"When it stops
being enough"**, because if tomorrow this is pointed at another game they
are the first thing to look at again. Until 2026-09-25 they lived together
in `assets/LIMITACIONES.md`.
