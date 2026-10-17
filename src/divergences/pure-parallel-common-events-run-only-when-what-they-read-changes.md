# The pure parallel common events run only when what they read changes

Until 2026-10-12 this page was "The equipment's common events run when the
menu closes": the ROM ran no parallel common event but ABL's 37, from the
menu. Since then it runs them all, and what is left of that path is this.

## What

In RM2k a parallel common event runs **every frame** while its switch is
on, or always if it has none. The ROM does the same —`compar_tick`, in
`runtime/common_events.s` in the-advocate—, except for the **pure** ones:
those that only read switches and what an actor has equipped, and only
write skills and the three permissions (save, menu, escape) —`pure` in
`rm2k-snes/events/src/commons.rs`—. A pure one runs:

* on the frame its switch turns on —or the first frame, if it has none—;
* on the frame after something it reads or writes changes: any switch
  written (`set_switch`), the pause menu closing —where the equipment
  changes—, `ChangeEquipment`, and a page's `ChangeSaveAccess`,
  `ChangeMainMenuAccess` or `ChangeEscapeAccess`.

Between those moments it would give the same result every frame, so not
running it does not change what is seen.

**A map's parallel page follows the same rule** since 2026-10-17, when it
is pure the same way or also sets the panorama (`ChangePBG`) —`pure_page`
in the same file; the console has it in bit 7 of the page's trigger—. It
runs on the frame after any of the above, after a `ChangePBG` from
anywhere else, and after every refresh, which is when it may have become
the active page. The Frozen World's `BackdropSetter`, on its battle screen,
is one. In ABL there are three:
2 `DisableSaving`, 8 `EnableSaving` and 37 `UpdateAG7 Skills`.

## Why

The cost. 37's body every frame was measured on 2026-09-27 at about an
eighth of the frame, and with 2 and 8 running every frame the race lap
went 53 hardware frames over its 976 ticks, past the 5% the suite allows.
As pure ones, a frame where none of them runs costs some two scan lines
for the whole table.

## What is still different

* **An actor that learns, by levelling up, a skill a pure one takes
  away keeps it until the next run.** In RM2k 37 would take it away on the
  next frame. AG7-17 does not learn any of its seventeen by level.
* **Something a pure one reads changed by a path other than those** would
  not wake it until the next switch is written. None is known: a loaded
  game wakes them on its first frame, as a reset does.

## Measured

It is enforced by ABL's `tests/rpgmaker/test_parallel_commons.py` (2
and 8: saving prohibited with 236 off, enabled with it on even after a
page's `ChangeSaveAccess`, and prohibited again when 236 turns off) and
`test_ag7_and_the_plant.py` (37: on joining, after changing the weapon and
closing the menu, and nothing with the switch off), in the ABL port.

## How it looks today

The same as in RM2k: you equip a piece, leave the menu, and in battle its
skill is there; and the menu's Save is grey until the game turns 236 on,
as in the original.

## When it stops being enough

A pure common event whose result depends on something that changes
without going through those paths; or one that is pure by its commands but
expensive enough to matter on the frames it does run.

## As an optimization

What it saves, and where it lives in the code: [The pure parallel common events run only when what they read changes](../optimizations/lossless/events.md#the-pure-parallel-common-events-run-only-when-what-they-read-changes), in Optimizations.
