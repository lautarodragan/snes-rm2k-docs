# What message escapes do not model

## What

A message's text carries RM2k's escapes, a backslash and a letter. The
console does some of them as RM2k does and **drops the rest**: the box
compiles without them, shows its text, and each one dropped is listed in
the build's `degradations.json` as a `message-escape-dropped` loss of its
command, with the escape as it was written.

Done as in RM2k:

* `\|` and `\^` at the end of the box —its tail—: a second's pause, and
  closing on its own. A `\^` anywhere else closes the box on its own too,
  at its end, which is where RPG_RT closes it wherever it is written.
* `\.`, `\|` and `\!` in the middle: a quarter of a second, a second and a
  key.
* `\\`, a literal backslash; `\V[n]`, a variable's value; `\N[n]`, an
  actor's name —see
  [What names in messages do not model](what-names-in-messages-do-not-model.md)—.

Dropped, and what is lost with each one:

* `\c[n]`, the text's color: the box is drawn in the System's text color.
* `\s[n]`, the text's speed: the box is drawn at the console's.
* `\$`, the gold window, which does not come up.
* `\>` and `\<`, the instant text: the box is drawn at its speed.
* `\_`, the half space: the letters on both sides of it come together.
* A `\V[n]` or `\N[n]` the converter cannot write —a variable inside a
  variable, an actor past 255—: the value or the name.
* Any other letter, and a backslash at the end of a line: RPG_RT draws
  nothing for them either, and they are listed so that a patch's code or a
  slip in the game is seen.

An escape that takes an argument drops it as RPG_RT reads it: up to the
next `]`, past a `\V[n]` inside it, or to the end of the line if there is
none; without a `[`, only the letter goes. A letter RPG_RT does not know
takes no argument, so in `\q[3]` the `[3]` is drawn, as in RPG_RT.

When the converter reflows a box for the console's window, what the box
drops goes at the start of its first box, where the compiler finds it to
list it: its place among the words does not survive the reflow.

## Why

Until 2026-10-15 any escape but the tail, the waits, `\c[n]` and `\s[n]`
left the whole page out, which kept a game from being played until each
escape was done: Vampires Dawn writes `\_` in hundreds of boxes. Drawing an
escape as its letters would show, so the choice was between leaving the
page out and losing what the escape does; taro chose losing it, as long as
the build says so: "that way it can be played without solving that
problem. I'd leave a compiler warning or whatever so we don't lose and
forget it."

## How it applies

The rule is `escape_tail`, in `refit.rs` of `rm2k-snes-text`, with its
cases in that crate's `tests/escapes.json`; what each escape loses is said
by `with_wait_marks` there. The event compiler notes the losses in
`Ctx::lose_dropped`, in `compile.rs`, with the text of `dropped_escape` in
`messages.rs`. Tested by the test game's `test_escapes.py`: a box with a
color, the gold window, instant text, a half space and an unknown letter
shows its text, and `degradations.json` lists each one. Task:
[`unknown-message-escapes-are-dropped-with-a-warning`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/unknown-message-escapes-are-dropped-with-a-warning.md).
