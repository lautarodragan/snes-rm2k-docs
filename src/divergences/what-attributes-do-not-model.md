# What attributes do not model

## What

Since 2026-10-15 the battle applies RM2k's attributes —the database's
`Attribute`s, Sword, Flame and the rest— as easyrpg-player's
`ApplyAttributeMultiplier` does for RPG Maker 2000. Of the attributes a hit
carries, the target's rank in each, `A` to `E`, gives that attribute's
rate —`a_rate` to `e_rate`—; within a kind, physical or magical, the best
rate counts, and with both kinds the effect goes through both,
`magical * (physical * effect / 100) / 100`. It is applied after the base
damage and before the critical and the variance. A skill carries its
`attribute_effects`; an actor's normal attack, the `attribute_set` of the
weapons in its first two slots; an enemy's attack, nothing. An enemy's rank
is its `attribute_ranks`; an actor's, its own, one step up if any armor it
wears carries the attribute. A healing skill from the menu goes through the
same, on the actor it heals. See `rm2k-snes/battle/src/attributes.rs` in
the-advocate, the model, and `runtime/battle_attributes.s`, the console.
What is not the same:

* **No skill shifts a rank.** A skill with `affect_attr_defence` lowers or
  raises its target's rank in its attributes for the rest of the battle
  (`Game_Battler::ShiftAttributeRate`); here it does its damage or healing
  and the ranks stay. *A Blurred Line*, *The Book of Three*, *El Dorado* and
  *The Frozen World* have two —Heat Barrier and Cold Barrier—, and
  *Vampires Dawn* six.
* **A skill with a physical attribute does not ask for the weapon.** In
  RM2k an actor cannot use one —it is grayed out— unless a weapon it holds
  carries that attribute (`Game_Actor::IsSkillUsable`), except for those
  with `affect_attr_defence`; here it is offered as any other. In *A
  Blurred Line* that is Saldra's Trip, which her Bent Staff does not carry
  (Martial), and AG7-17's ArmLaser and TillTheyGlow with the ArmCannon,
  which carries no Ray.
* **An effect past 32,767 before the variance is held there**: the console
  multiplies in thirty-two bits and keeps sixteen. No game comes near: the
  damage's cap is 999.

## How it applies

The tables are the converter's (`attributes` in `emit.rs` of
rm2k-snes/mapdata), outside bank 0, and only for the attributes a carried
skill or weapon can carry; the scratch is the zero page's, so it takes no
far RAM. The test is `tests/rpgmaker/test_battle_attributes.py` of A
Blurred Line, against the model and against easyrpg's arithmetic. The task
is
[`elemental-attributes-are-not-applied-in-battle`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/elemental-attributes-are-not-applied-in-battle.md).
