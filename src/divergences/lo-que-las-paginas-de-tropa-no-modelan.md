# What troop pages do not model

## What

Troop event pages run with the RM2k conditions and commands that the
battles in `release` ask for —see the task [`eventos-de-tropa-de-release`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/eventos-de-tropa-de-release.md)—
and the ones the characters' systems use —the task
[`eventos-de-tropa-en-la-pelea`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/eventos-de-tropa-en-la-pelea.md), both in `tasks/` in the-advocate-work—, with
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
worst package. It was measured by the task [`el-comun-35-y-la-radio`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/el-comun-35-y-la-radio.md), in
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

`pruebas/rpgmaker/test_eventos_de_tropa.py` in the ABL port
(the-advocate-ports/abl), with the `pelea-86` and `pelea-102` cases; and
`pruebas/rpgmaker/test_sistemas_de_tropa.py` in the ABL port, with
`pelea-invocacion` and `pelea-radio`.
