# Escape is the fifth command

## What

The battle does not have the party menu that comes before the commands
—Engage, Automatic, Escape—: each character chooses among **Attack,
Special, Defend, Use Item and Escape**, and Escape comes fifth **only in a
battle you can run from**. It is an addition of RPG Maker 2000 PLUS, chosen
by taro on 2026-10-04.

Fleeing still belongs to the party, as in RM2k, whoever chooses it: if it
works, the battle ends; if it fails, the commands given by the ones before
are forgotten —a chosen item, which is spent when chosen, goes back to the
inventory—, the failed escape message is shown and the turn belongs only to
the enemies, which is `ProcessSceneActionEscape` with `eFailure`. See
`ba_flee_failed` in `runtime/battle_run.s` in the-advocate.

You can flee, as in easyrpg (`args.allow_escape`), from a random encounter
and from an `EnemyEncounter` with `escape_mode` other than 0. Mode 0 is
given by `OP_BATTLE`'s escape destination, `BATTLE_NO_ESCAPE`: see
`compile.rs` in `rm2k-snes-events`.

## What RM2k does

The party menu appears at the start of each turn: Engage asks for the
commands, Automatic picks them by itself and Escape attempts to flee, which
in a battle without escape is grayed out. Each character has four commands.

## What is not there

* **Automatic**: there is no automatic battle.
* Fleeing from the party menu **before** anyone gives a command: here it is
  chosen from a character's command, after the ones that already gave
  theirs. What they ordered is lost, the same as in RM2k, where they never
  got to order.

## Measured

With the 2015 RPG_RT under Wine, on 2026-10-04, the battle test with troops
82 and 87: the party menu at the start of each turn, with Escape in white
—the battle test always allows fleeing—. Where the captures are is said by
the task, [`battle-menu-like-rm2k`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/battle-menu-like-rm2k.md) in `tasks/` in the-advocate-work.

ABL's test run covers it in `test_huir_es_del_grupo` —the failed escape,
with the HP checked against the model— and in
`test_sin_huida_no_hay_escape`.
