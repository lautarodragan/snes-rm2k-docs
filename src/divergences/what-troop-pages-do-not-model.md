# What troop pages do not model

## What

Troop event pages run with the RM2k conditions and commands that the
battles in `release` ask for —see the task [`release-troop-events`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/release-troop-events.md)—
and the ones the characters' systems use —the task
[`troop-events`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/troop-events.md), both in `tasks/` in the-advocate-work—, with
these differences.

**An actor's HP, only if they are fighting.** A page's `actor_hp` condition
is met only if the actor is in the party: their HP and maximum are at hand in
battle, and those of one who is not fighting are not —the maximum comes from
their level—. In RM2k `Game_Actors::GetActor` answers for anyone. The game's
two pages that look at it belong to the Lazer Teeth battle (troop 86) and
look at Talan; if Talan were not in that battle, in RM2k their messages could
come out and here they could not. See `ba_page_met` and
`batalla.PaginaDeTropa`.

**`ShakeScreen` shakes the scene and not the text.** It is what
`Spriteset_Battle` runs with `GetShakeOffsetX` —the background and the
battlers—; RM2k's windows stay still, and here the lines, which are BG2, do
too. What the ROM does not do is shake whatever is drawn as objects: in
battle there is nothing.

**A page's `PlaySound` is requested and does not play**, unless its effect
is in `troop_effects_in_package` (`[sound_effects]` in the project file):
the battle's package has no room without lowering the battle theme's sample
rate, and that is taro's rule for effects. Today there is only one, the
`Thunder9` of the takeoff in the agents' battle; the numbers are next to the
list.

**A page's `PlayBGM` is done since 2026-09-30, at lower quality.** It is the
one in `Play Radio` (the system on 809), which plays one of three themes
—`dd2shad2`, `patchb` and Ryan Bury's—. They go **separately** in the
battle's package: they are not uploaded with the battle theme, their
`PlayBGM` uploads them on their own together with the package's effects, so
the battle theme does not degrade. What degrades is what they share with
other themes: with three more themes, the sample bank has fewer entries left
for copies, and several samples of other themes stay at the rate of the
worst package. It was measured by the task [`common-35-and-the-radio-music`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/common-35-and-the-radio-music.md), in
`tasks/` in the-advocate-work. With MSU-1 the three have their own track and
play whole.

**Whoever joins the party in battle takes the place of whoever left.** In
RM2k `RemoveActor` takes the actor out of the party list and `AddActor` puts
the new one at the end, so the battle window rearranges itself. Here the
battle's places do not move —everything pending in the turn, the commands,
the order and the targets, points at them—: the one who leaves leaves their
line empty and the one who joins goes to the first empty one. With the
game's summons, which take Lerle out and put the summon in, it shows as the
summon on Lerle's line and not at the very bottom, and it gets to give
commands in that order. The saved party does end up in RM2k's order:
`party` is changed by the same opcodes as on the map. See `ba_sync_in`.

And from that comes another, smaller one: **an enemy that had already chosen
the one who left hits the one who joined in their place**, if they joined on
that same turn. In RM2k the target no longer exists and the action is
retargeted to the first in the party. Measured in the summon's test: the
Giant hits the droid on the turn it joins, which in RM2k would have been
Kersh. The model does the same as the console, so the test does not catch
it.

**`ChangeMonsterCondition` gives the enemy the condition** since
2026-10-12 —before that it was a declared debt, for a day—, and what the
battle does with it, and what it does not, is in
[What battle conditions do not model](what-battle-conditions-do-not-model.md).
The pages of Talan's `Inscribe` (switch 799) and `ControlMachines` (803)
are the game's that use it.

**`FlashScreen` and `TintScreen` reach the scene and nothing else**, which is
RM2k's own rule: `Spriteset_Battle` gives the screen's tone to the
background and the battlers, and the flash is drawn under the windows. On
the console both are the map's transform of the palette, run over the
scene's —the background's colours and the battlers'—, so the windows and the
text are left alone. Compared with the original under Wine on 2026-10-12,
with `Inscribe`'s wall of bark: the scene goes the flash's colour and back,
and the empty message window stays black. What is not the same:

* **The plain background does not flash**: a battle with no background has
  colour 0 behind the battlers, which is also the text's, and it stays black.
* **`TintScreen` in battle is applied at once**, without its gradient, as on
  the map: see `TINT_SCREEN` in the event compiler. The page's wait is
  respected.
* **A flash still going when the battle ends is cut**; in RM2k it would
  finish over the map. The tint does carry on, both ways: the battle starts
  with the map's —the agency captain's battle (troop 240) is fought after a
  `TintScreen` to black, which its turn 0 page undoes— and the map comes
  back with the one a page left.
* **The message window empties two frames after the flash shows**: it is
  the text layer's, which takes that long to clear a box. In RM2k both
  happen in the same frame.

**`TerminateBattle` ends the battle with no victory**, as RM2k's `Abort`: no
experience, no gold, no end screen, and the map's page goes on past the
`EnemyEncounter`'s handlers, whichever there are. The battle leaves with its
usual mosaic, from the screen it was showing.

**What the pages change in the party they change in the saved game, between
stretches.** The console keeps the battle's HP in `BA_ONE`; before each
stretch of a page it copies them to `FAR_HP` and afterwards brings them
back, so the map's opcodes —`ChangeHP`, `FullHeal`, the `ChangeCondition`
that revives, the `ControlVars` with an actor's HP— work without knowing
there is a battle. In RM2k there is no copy because there is a single
`Game_Actor`. The difference does not show except in the map's
`CheckGameOver`, which the console does not do: in battle it is not needed,
because losing belongs to the battle.

## How to reproduce it

`tests/rpgmaker/test_troop_events.py` in the ABL port
(the-advocate-ports/abl), with the `battle-86` and `battle-102` cases; and
`tests/rpgmaker/test_troop_systems.py` in the ABL port, with
`battle-summon` and `battle-radio`; and
`tests/rpgmaker/test_battle_flash_golden.py` in the ABL port, with
`battle-inscribe` and `battle-captain`.
