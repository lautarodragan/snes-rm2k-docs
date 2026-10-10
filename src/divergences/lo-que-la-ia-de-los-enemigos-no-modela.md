# What the enemies' AI does not model

## What

Since 2026-09-27 the enemies choose what to do like `Game_Enemy`: the LDB's
action list, each action's `rating` and easyrpg's
`SelectEnemyAiActionRpgRtCompat` —each candidate weighs
`max(0, rating - maximum + 10)`— and they use skills. It is decided by
`batalla.accion_del_enemigo` and copied by `ba_enemy_action`
(`tools/runtime/battle.s` in snes-rm2k). What is still different:

* **With a single weighted action the die is not rolled.** RM2k rolls
  `rand(0, sum - 1)` anyway. It is the same distribution, and it leaves the
  randomness of the battles that already existed —enemies that only
  attack— exactly as it was: without it every hit of every battle in
  `release` changed. RPG_RT's generator is not ours either.
* **Only the basic attack and skills.** Defending, charging,
  self-destructing, fleeing, doing nothing, transforming and the double
  attack drop out of the list, as if their condition were not met. Switch
  skills, too.
* **Only the "always" condition.** Those on turn, HP, SP, number of enemies,
  party level and party fatigue take the action out of the list.
* **The switches an action turns on or off when chosen** (`switch_on`,
  `switch_off`) take the action out of the list.
* **Statuses do not exist**, so a skill that only adds or removes statuses
  does nothing, and the AI discards it the way easyrpg discards one that has
  nobody to affect.
* **No animation.** `ShortCircuit` carries number 62 and it is not drawn,
  same as the party's skills: see `tasks/wishlist/animaciones-en-la-pelea.md`
  in snes-rm2k-work.

If an enemy has no action left, it attacks, which is what they all did until
that day.

## Measured

On 2026-09-27, over the troops in `release` (`troop_id` in `mapdata.inc`),
16 enemies carried something besides the plain attack. With RM2k's weights
**four use a skill**: the Tangle Wire (`ShortCircuit`, half the time), the
KingRat of the Rat Tracks (`RoyalRatBite`, half: its double attack is
turn-based and drops out of the list), the Risen Dead (`PowerDrain`, a
third) and the Securibot Type I (`Static Shielding`, on itself, half). The
others carry one with ten or more points less than the attack, and would
never use it: the Scrapped Droid, the Trash Hauler and the plant's Junkbot,
among them.

It is enforced by `test_la_tropa_es_la_que_se_espera` and
`test_el_tangle_wire_usa_short_circuit_y_deja_el_hp_del_modelo`, in
`pruebas/rpgmaker/test_ag7_y_la_planta.py` in the ABL port
(snes-rm2k-ports/abl), and by `test_la_pelea_de_la_planta` in
`test_cores.py`.

## How it looks today

In the plant, the Tangle Wire alternates between hitting and "ShortCircuit";
the other three in the plant only hit, which is what they would do in RM2k.
The boss of the Rat Tracks bites.

## When it stops being enough

An enemy whose battle depends on a condition —a boss that changes actions by
turn or when low on health— or that defends or flees.
