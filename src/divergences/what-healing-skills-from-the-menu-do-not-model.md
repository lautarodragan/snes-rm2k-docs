# What healing skills from the menu do not model

## What

A healing skill used from the pause menu's skills screen —Tech Skill in A
Blurred Line, Skill or Special in other games— does what RM2k's
`Scene_ActorTarget` does with a skill: the actor choice with the skill's
name, the cost's term and its cost; the bar on the chosen row, on the user
for a skill on oneself, or over the whole party for one on the party; A
heals, **stays there**, and spends the SP only if it was of use; the fallen
are raised by a skill that cures death. Measured against the 2015 RPG_RT
under Wine and easyrpg-player's `Game_Party::UseSkill` and
`Game_Battler::UseSkill`. What it does differently:

* **The randomness is the battle's**, the sixteen-bit xorshift of
  `rm2k-snes-battle` with its own seed, and not RPG_RT's: a heal falls in
  the same range —the skill's power, the user's attack and spirit, the
  variance— but not on the same number. The console computes it with the
  battle's code, so `field-skill` of `rm2k-snes-battle` gives the exact
  number for a seed.
* **No sound.** RPG_RT plays the first sound of the skill's animation on a
  heal that was of use, and its buzzer when it was not; the port plays
  neither, as its menus play no system sound at all.
* **The party's rows show HP and not SP**: the choice is the medicine's,
  over the pause menu's party panel, which has no SP line. The SP the skill
  spent are seen back in the list's status line.
* **Attributes are not applied**: `CalcSkillEffect` multiplies by the
  target's rate for the skill's attributes; the port does not, as its
  battle does not. Of the healing skills the six games teach, only Book of
  Three's Slug Bug has an attribute, and no actor of that game has a rank
  other than the one that leaves it at 100%; equipment that changes a rank
  was not looked at.
* **States other than death are not kept outside battle**, so a skill that
  only cures them —Antidote, Medicine, Blessing— is of no use: nothing
  happens and no SP go, where RPG_RT cures a state that lasted past the
  battle.
* **The name goes in two lines** of eleven cells, as a medicine's, cut at a
  space where it fits, or in the middle of a word that does not
  ("LifeFromDec" and "ay"); RPG_RT writes it whole in one. **The cost has two
  places**, as in the list.

## How it applies

The choice is `target_screen` in `runtime/menu.s` and the skill's part of
it in `runtime/actor_choice.s`; the effect is `sk_heal_use` in
`runtime/skills_screen.s`, over the battle's `ba_skill_effect` and
`ba_variance`. The reference for the screen is `render` of
`rm2k-snes-screens` with a `skill`, and the tests are
`tests/rpgmaker/test_healing_skills.py` of A Blurred Line. The task is
[`healing-skills-from-the-menu`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/healing-skills-from-the-menu.md).
