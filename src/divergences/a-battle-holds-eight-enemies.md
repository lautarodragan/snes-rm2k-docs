# A battle holds eight enemies

## What

A troop with more than eight members is cut to eight by the converter,
which leaves out the ones its pages only use as scenery. RM2k's data has no
limit: liblcf reads as many members as the database holds, and
easyrpg-player sets them all up in the battle.

Which ones go, by what the troop's pages do with each member, from the
highest place down within each kind:

1. one hidden that no page ever shows: nobody sees it;
2. one hidden that every page that shows it also kills —a
   `ChangeMonsterCondition` with the death, after the `ShowHiddenMonster`,
   in the same page—: a figure that crosses a scene and is not fought;
3. only if there are still too many, the last places. That battle may not
   be the game's, and the converter says so.

A member that a page condition or a battle branch asks about is never
taken as scenery. The pages are renumbered to the places that are left:
the commands about a member left out run as nothing, and a
`ShowBattleAnimationB` on it goes to the whole troop. Each cut is in the
cartridge's `degradations.json`, as `troop-members-left-out`.

See `rm2k-snes/battle/src/fit.rs` in the-advocate.

## Why

The console's battle has eight places for the troop, and they are not one
number: the combatants live at fixed places of the battle's far RAM, forty
bytes each, and the scene's masks, the table of hidden members and the
drawing order are a byte per troop. A ninth place widens the battle for
every game, and its RAM was not there when it came up: on 2026-10-15 the
far RAM the linker places had less left than one combatant takes.

The one troop of the eight games with more than eight members is The Book
of Three's troop 83, whose first page plays a scene with nine and leaves
one standing to fight. Of the nine, five appear together at most, so
leaving out one of the scene's figures keeps the battle the game's; until
then the cut took the first eight, and with them it lost the one that is
fought ([the task](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-a-troop-of-nine.md)).
