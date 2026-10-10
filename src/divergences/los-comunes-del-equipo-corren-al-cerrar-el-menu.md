# The equipment's common events run when the menu closes

## What

Common event 37, `UpdateAG7 Skills`, is **parallel with switch 150**: in
RM2k it runs every frame while AG7-17 is in the party, removes its seventeen
skills and gives it the one for each piece it has equipped. The ROM does not
run parallel common events, and this one it runs **at the two moments when
its result can change**:

* when the switch turns on: the converter pastes the body after the
  `ControlSwitches` that turns it on, as if a `CallEvent` followed it;
* when the pause menu closes, which is where equipment is changed:
  `equipment_commons`, in `tools/runtime/equipment_from_events.s` in
  the-advocate, from `menu_screen`.

It applies to any parallel common event, with a switch, that has nothing but
`ChangeSkills` and "has such item equipped" branches:
`eventos.COMUNES_DEL_EQUIPO`. In the game there is only one.

What is still different:

* **In RM2k it runs on the frame after the switch; here, on the same one.**
  It does not show: nothing looks at the skills in between.
* **A page's `ChangeEquipment` does not run it again.** In the game there is
  none on actor 18.
* **Turning the switch off takes nothing away**, same as in RM2k: the event
  stops running and the skills stay as they were.

## Measured

The general approach —one more interpreter running the parallel common
events every frame, like the maps' parallel pages— was measured on
2026-09-27 against this:

* **The per-frame loop.** With throwaway cases that ran the body of 37 N
  times in a row in one page, 0, 10, 20 and 30 times took 63, 64, 66 and 67
  frames: **about 0.13 frames per pass**. As a parallel event, close to an
  eighth of each frame's CPU, on every map, from the moment AG7 joins the
  party.
* **What else it would turn on.** Number 2 (`DisableSaving`) is parallel
  **without a switch** and disables saving whenever 236 is off; 3
  (`Raining`, switch 94) and 8 (`EnableSaving`, switch 236) also compile.
  Doing the general thing changes `release` far beyond AG7.
* **This**: 8 bytes of bank 0 (the call from the menu and the bridge to
  `run_code`), 117 of bank 1, no bytes of RAM, and no cycles per frame. The
  compiled body is 307 bytes in RODATA and as many again pasted into page 5
  of event 2 on map 57.

It is enforced by the three AG7 cases in
`pruebas/rpgmaker/test_ag7_y_la_planta.py` in the ABL port
(the-advocate-ports/abl): on joining it knows its weapon's skill, changing it
and closing the menu changes it —checked red without the call from the
menu—, and with the switch off closing the menu touches nothing.

## How it looks today

The same as in RM2k: you equip a piece, leave the menu, and in battle its
skill is there.

## When it stops being enough

A parallel common event that looks at something other than equipment —a
variable, the map, time—, or that does something more than change skills:
that one needs the real interpreter. Or a page that changes the equipment of
the actor the event looks at.
