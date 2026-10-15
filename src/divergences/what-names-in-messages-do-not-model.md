# What names in messages do not model

## What

A message's `\N[n]` writes actor `n`'s name, and `\N[0]` the party leader's.
The console does it in two ways:

* **Baked**: an actor no `ChangeHeroName` of the game renames always has
  the database's name, so the converter writes it into the text, letter by
  letter, and the ROM never knows there was an escape.
* **Written when the box opens**: `\N[0]`, and the `\N[n]` of an actor some
  `ChangeHeroName` renames. The text carries a mark and the actor, and the
  composer hands the name's letters out of the cartridge's text table, as it
  does a variable's digits for `\V[n]`. With an empty party `\N[0]` writes
  nothing, as easyrpg's `PendingMessage::DefaultCommandInserter` does.

`ChangeHeroName` compiles since 2026-10-15. Every name it can give is a
literal of the command, so they are all known when building: the converter
numbers them and writes them as texts, and the ROM keeps one byte per
renamed actor —which of them it carries, zero for the database's—, which
travels in the saved game. The menu, the battle, the equipment and skills
screens and the level up show the new name; the slot screen shows the
leader's name **as it was saved**, as RM2k's save screen does.

What does not come out as in RM2k:

* **The line is not measured with the name.** The converter reflows a box
  for the console's window, narrower than RM2k's, before it knows any name:
  a `\N[0]` counts there as the five letters of its escape, and when the box
  opens the line takes the name's real width. A long name can push the end
  of its line past the window's edge, where the composer cuts it. RM2k does
  not wrap a line a name makes long either, but its window is wider.
* **A name longer than 32 letters is cut** in a message, so that the line's
  length still fits in its byte. No line that long fits the window anyway.
* **A letter the console's font does not have** —RM2k's has Latin-1, the
  console's only ASCII— is a `?` in a name written when the box opens, as in
  the menu. A baked name with one leaves its page out, like any other text
  with a letter the font lacks.
* **The menu and the slot screen cut a renamed name** to the cells they
  give a name, the same as the database's.
* `EnterHeroName`, the screen where the player types a name, is still not
  done, and its page is left out. A name typed there would not be one of the
  literals the cartridge knows, so it needs the name to live in RAM.

## Why

Writing every `\N[n]` at run time would have cost the same on the ROM's
side, but the baked ones cost nothing at all and are almost all of them: of
the eight games ported or surveyed on 2026-10-15, none wrote `\N[0]`, the
only `\N[n]` were The Frozen World's and Doom's Day 2's, of actors nobody
renames, and the only `ChangeHeroName`s were two in Sunset over Imdahl,
which renames its hero so that RM2k's save screen reads "Completed Game".
Keeping a name per actor in RAM, as RM2k does, would take far RAM that the
console does not have to spare, for names that are known when building.

## How it applies

The mark is `NAME` in `messages.rs` of the event compiler, and
`with_names`, in its `compile.rs`, decides which names are baked;
`OP_CHANGE_NAME` is in `rm2k-snes-bytecode`. In the runtime, everything is in
`actor_names.s`: `actor_name_txt` for the screens that draw from the text
table, `actor_name_row_now` and `actor_name_row_saved` for the menu and the
slot screen, `msg_name_mark` for the message; a troop page's box writes them
in `ba_page_message`, in `battle_troop.s`. Tested by the test game's
`test_leader_name.py`: the leader before and after the party is reordered,
a renamed actor, the menu, an empty party, and the rename through a save and
a reset. Task:
[`n-0-and-renamed-actors-in-messages`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/n-0-and-renamed-actors-in-messages.md).
