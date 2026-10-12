# What battle conditions do not model

## What

Since 2026-10-12 the battle keeps RM2k's conditions —the database's
states— on the enemies, as `Game_Battler` does: a troop page's
`ChangeMonsterCondition` gives one or takes it away, and from then on it
counts its turns, wears off on its own when `hold_turn` and
`auto_release_prob` say so, is released by a hit with `release_by_damage`,
restricts what its holder does —it does nothing, or attacks a random one of
its own side or of the other— and halves the attack, defense, spirit or
agility it says, and lowers its holder's hit chance with
`reduce_hit_ratio`. Its two messages come out: `message_affected` when its
holder's turn comes, and `message_recovery` when it goes. *A Blurred Line*
asks for two, both from Talan's systems: `Control` (22), from
`ControlMachines`, and `BarkWall` (23), from `Inscribe`. See
`runtime/battle_states.s` in the-advocate, and `Held` in
`rm2k-snes/battle/src/simulate.rs`, the model that rolls the same dice in
the same order. What is not the same:

* **Only enemies have conditions, and only a troop page gives them.** No
  skill, attack or item gives or takes one, on either side: a skill whose
  only effect is a condition does nothing, and the enemies' AI discards it
  —see [What the enemies' AI does not model](lo-que-la-ia-de-los-enemigos-no-modela.md)—;
  an item that only cures conditions is not in the battle's list. The actors
  never have one in battle: a troop page's `ChangeCondition` that adds one
  does not compile, and their status says `normal_status` or the dead one.
* **No HP or SP each turn.** `hp_change_*` and `sp_change_*` —poison,
  regeneration— are not applied (`ApplyConditions`), and a condition does
  not seal skills (`restrict_skill`, `restrict_magic`). The game's two do
  neither.
* **Taking the dead condition away from an enemy does not compile**: in
  RM2k it gets up with 1 HP, and the scene does not draw again one it
  erased. No game asks for it. Adding it kills, without a message or a
  sound, as RM2k —Book of Three does it on troop pages—.
* **Four at once per enemy.** A fifth is not given. No game comes near.
* **What a hit releases is said in a window of its own**, after the hit's,
  and only the first if one hit releases two; RM2k writes it as a third
  line under the damage, one per condition.
* **The holder does not flash white** when its turn comes with a
  condition's message —`ProcessBattleActionBegin`'s `Flash`—: the message
  comes out, in a window of its own before the action, as in RM2k.
* **A physical skill's hit chance does not look at conditions**, as it does
  not look at agility either: it is the skill's `hit`. RM2k lowers it with
  `reduce_hit_ratio` and always hits one that cannot act when the skill's
  `failure_message` is 3. A normal attack does both.

The randomness is the battle's own, as everywhere else in it: see
[What the enemies' AI does not model](lo-que-la-ia-de-los-enemigos-no-modela.md).

## Measured

On 2026-10-12, against the model, turn by turn —the HP of everyone, each
enemy's conditions with their count, its parameters and the conditions'
messages—, in the two battles where the game gives them: the Scrapped
Droid and the GiantRat with `Control` (troop 111), and the Lumbering Giant
with `BarkWall` (troop 128).

## How to reproduce it

`pruebas/rpgmaker/test_condiciones_de_pelea_golden.py` in the ABL port
(the-advocate-ports/abl), with the cases `pelea-controlar` and
`pelea-inscribir`.

## When it stops being enough

When a game's battles rely on skills, weapons or items that give
conditions, or on poison: then conditions go to the actors too, with their
status window, and stay after the battle when their `type` says so.
