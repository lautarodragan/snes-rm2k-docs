# The Book of Three and The Frozen World: what is left out

> **Measured on 2026-10-14**, by Calandria, with the tools at `14e200fc`
> (the-advocate) and the ports at `f775b66` (the-advocate-ports), over each
> game's `release` cartridge and its `culprits.json` (what `just culprits`
> writes). It is a snapshot: the numbers are from that day and this file is
> not updated; how to redo each count is at the end. The task is
> [`book-of-three-and-frozen-world-what-is-left-out`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-and-frozen-world-what-is-left-out.md).
> Nothing was changed in the tools or in the games; the only builds run were
> two throwaway ones with an exclusion removed, to see if it still holds.

taro's question, after the same one for A Blurred Line: what is left out of
these two games, by which variant of each command, and what fixing it would
take. The culprits report says which **command** keeps a page out; the
compiler's refusal says nothing, so each group below was found by reading
the arm of `compile_command` (or `branch_bytes`, `compile_number`, the choice
code) against the operands the report lists, and checked against the dump.
The pages that are in and have a parameter nothing reads are the other
research, [What the compiler ignores silently](2026-10-14-what-the-compiler-ignores-silently.md);
its rows for these two games are at the end.

## Summary

* **The Frozen World is a game whose combat is on its maps, and the
  cartridge has none of it.** Maps 1 ("Battle Screen") and 2 ("Plate
  Placement") are the combat engine: 29,000 and 12,000 commands of events
  on 48 and 51 events. Both are still out, for the reasons written in the
  project, and **324 pages on 72 other maps** teleport into them (the
  monsters on the maps are) and are left out with them, plus the common
  events that only they call: the level-ups, the steal and study skills, the
  party statistics. The game has **no encounter at all**: 0
  `EnemyEncounter`, and its 80 troops are 80 empty pages. What is left out
  by the *commands* is small by comparison —68 map pages and 11 common
  events—, and almost all of it is part of the same combat.
* **The Book of Three's maps are almost whole** (9 pages of 1,282), and what
  it loses is in its battles and in two common events. Three things matter:
  the **two scripted fights** that end by an animation and `TerminateBattle`
  (the three Cauldron-Born at map 26, the Horned King with Dyrnwyn at map
  78), whose pages do not compile, so those fights have no ending but
  winning or losing; the **party's three special commands** (Taran's Last
  Stand and Cash Reward, Eilonwy's Absorb Essence), which are a page each in
  52 troops and do nothing; and the **random gold of the chests**, 82 calls
  to one common event that a random range of 1,500 keeps out.
* **The "trigger the ROM cannot look at" is not a trigger.** All 95 (Book of
  Three) and all 80 (Frozen World) troop pages that the report counts under
  that name are pages **with no condition at all and no command**: in RM2k a
  page without a condition never runs, so nothing is lost. It is the
  report that is misleading (a draft).
* **A bug, not a hole: `ControlSwitches` past switch 1,023 is not
  refused.** The ROM keeps 1,024 switches; the branch on one is refused, but
  the command that sets one compiles, and `set_switch` writes the bit
  beyond the 128-byte table, into the RAM that follows. The Frozen World has
  78 such commands (28 map pages and three common events in the cartridge;
  map 19's event 12 compiles to `OP_SWITCH $041B`, switch 1,051, as its first
  command); Vampires Dawn 1,014. The existing draft about page conditions
  past 1,023 says the compiler refuses these; it does not.
* **Thirteen causes in the table below, eight of them tiny or small.** Seven
  would also help another game: `ControlVars` multiply and divide and from
  an item count, `ChangeItems` by a variable, the switches past 1,023, the
  five-option choice, `ChangeMapTileset` and `ChangeActorFace` reach
  Vampires Dawn, and the first four and the choice also Sunset.

## The causes, ranked

By what a player misses, first what can block the story. "Size" is a guess
from reading the arm: **tiny** is a few lines and a test, **small** an arm in
the compiler with its test, **medium** a runtime change as well, **large** a
new subsystem. The counts are uses in the data of all eight games, whether
the page compiles or not (how, at the end).

| # | Game | Cause | Count | What it does | Size | Elsewhere |
|---|---|---|---|---|---|---|
| 1 | Frozen World | Maps 1 and 2 are not in the cartridge, and 324 pages teleport into them | 324 pages, 72 maps; the combat engine | **blocks every fight** (the game has no other combat) | large (two existing drafts) | Vampires Dawn's map 1 (the second draft) |
| 2 | Frozen World | `ControlSwitches` on a switch past 1,023 **compiles and writes outside the switch table** (the branch on one is refused) | 78 `ControlSwitches` (28 map pages and commons 11, 69, 70 compile); 63 branches | **corrupts the RAM after the table** on 31 pages that are in the cartridge; 6 map pages and 6 common events are left out by the branches | medium | Vampires Dawn: 1,014 and 39 |
| 3 | Book of Three | `ShowBattleAnimationB` in two troop pages (96 and 136) | 2 pages, 56 uses | **probably soft-locks two story fights**; not played | tiny as a debt, large for real | none |
| 4 | Book of Three | The party's special commands: `ControlVars` multiplied by a variable, `ChangeItems` and `ChangeMonsterHP` by a variable, and the animation | 152 troop pages (52 + 52 + 48, on troops 83 to 135) | degrades combat: three commands do nothing | small, three arms | `ChangeItems` by a variable: Vampires Dawn 81 |
| 5 | Book of Three | A random range wider than 255 in `Random Chest List` | 82 calls skipped, 16 maps | degrades: the chests' random loot | tiny | none |
| 6 | Frozen World | A literal backslash `\\` in a message | 320 lines; 7 common events and 38 map pages (map 3: 18, map 1: 17, map 14: 3) | degrades: the combat's stat readouts; **behind #1** | small | none |
| 7 | Frozen World | `\V[n]` in a choice option, and in a box before an `InputNumber` | 6 shop pages + 5 `InputNumber` pages | degrades: 3 merchants (they sell the plates); the use-item menu | small to medium | none |
| 8 | Both | `ControlVars` operations multiply and divide | Book of Three 53, Frozen World 6 | degrades: #4, a parallel common event, the HP percentages | small | Sunset 4, Vampires Dawn 7 |
| 9 | Both | `ControlVars` from an item count | Book of Three 5, Frozen World 13 | degrades: the use-item menu, Eilonwy's upgrades | small | Vampires Dawn 47 |
| 10 | Book of Three | A choice with more than four options | 1 common event, 5th option (6 calls skipped) | degrades: choosing among five Dreams | medium | Sunset 21, Vampires Dawn 21 |
| 11 | Frozen World | `ChangeMapTileset` | 10 uses, 8 pages on 5 maps | degrades: those pages never run | large | Vampires Dawn 10 |
| 12 | Frozen World | `ChangeActorFace` | 13 uses, 7 pages | none: faces are not drawn | tiny | Vampires Dawn 5, Dooms 2 1 |
| 13 | Both | The report counts empty troop pages as a bad trigger | 95 and 80 | nothing lost; a misleading count | tiny | the same in every game |
| — | Book of Three | The hero's diagonal steps and "face away" in a route | 2 map pages | one of them is Hen Wen's second talk | existing | [`route-the-missing-moves`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/route-the-missing-moves.md) |
| — | Book of Three | An actor's HP branch; `ControlVars` from an item count | commons 18 and 21 | Reraise and Eilonwy's upgrades never run | existing | [`book-of-three-reraise-and-eilonwy-dont-compile`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-reraise-and-eilonwy-dont-compile.md) |

Rows 8 and 9 span the two games; row 4 is three causes with one effect and
has one draft for the two that are not in another row. Row 2 is the odd one:
the others are pages that are left out, and this one is pages that are in.
The drafts are listed at the end.

## The Book of Three

Maps 1,273 of 1,282 pages; common events 20 of 25; troops 497 of 746.

### The maps: nine pages

| page | what stops it |
|---|---|
| map 4, event 4, page 2 | `MoveEvent` on the hero with a "face away from the hero" step (22), which is only done on events |
| map 22, event 2, page 1 | `MoveEvent` on the hero with four diagonal steps, "through" on and off (36, 37) |
| maps 31, 42, 46, 52, 86, 87 (one page each) | `ChangeItems` with the **amount in a variable** (24, "AmountAbsorbed"), of an Essence of Fire, Water or Thunder |
| map 89, event 2, page 1 | `ControlVars` setting a variable from the **number of an item held** (126, Denner's Tail) |

The two hero routes are the existing
[`route-the-missing-moves`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/route-the-missing-moves.md)
and [`book-of-three-hen-wens-second-talk-does-nothing`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/book-of-three-hen-wens-second-talk-does-nothing.md).
The essence pages are where the player gathers essences, and are the same
`ChangeItems` as the troop pages below.

### The common events: five

| common | trigger | what stops it | what it does |
|---|---|---|---|
| 9 "All Five Dreams" | called 7 times | a choice with **five options** (`ShowChoiceOption` 4; the window holds four) | the 6 calls from maps 24, 53, 62, 63, 80 are skipped: the page goes on without choosing |
| 13 "Glory Hound" | parallel, switch 95 | `ControlVars` multiplied by a variable | never runs |
| 18 "Reraise KO'd chars" | parallel | an actor's **HP branch** (`[5, actor, 3, 1, ...]`, actors 10 to 15) | never runs; existing draft |
| 19 "Random Chest List" | called 82 times | **two `ControlVars` randoms**: 100 to 500 and 1000 to 2500 (a range over 255) | all **82 calls are skipped**, on 16 maps (20, 21, 26, 27, 28, 41, 44, 47 to 50, 53, 55, 62 to 64): the chests' random loot |
| 21 "Eilonwy's Upgrades" | parallel | `ControlVars` from an **item count** (essences 128, 129, 130 and 237) | never runs; existing draft |

Common 19 is the cheapest thing in the game: the compiler keeps the random
range to 255 (`b - a < 256`, the ROM draws a byte), and the two ranges are
401 and 1,501 wide. A random of a word, or a draw summed from two, gets 82
calls back. Common 9 is the other that is called: its fifth option is the
"cancel" branch of a five-way choice.

### The troops: 154 pages, three families

Of the 746 troop pages, **95 have nothing in them** (next section), 497
compile, and 154 are left out by a command. They are not scattered: they are
the same three or four pages on each of the troops 83 to 135, which are the
random battles from Yern's Forest on, and the two scripted fights.

| family | trigger | commands that stop it | pages |
|---|---|---|---|
| **Last Stand** (Taran's) | switch 96, `LastStandON` | `ControlVars` set to a random, `ShowBattleAnimationB`, `ChangeMonsterHP` with the **damage in a variable** (6, "LastStandRandom") | 52 |
| **Cash Reward** (Taran steals silver) | switch 92, `CashRewardON` | `ControlVars` **multiplied by a variable** (8 by 9) | 52 |
| **Absorb Essence** (Eilonwy) | switch 270, `AbsorbEssenceON` | `ChangeItems` with the **amount in a variable** (24, "AmountAbsorbed"), of Essence of Fire, Water or Thunder | 48 |
| the scripted ends | turn 6 (troop 96); enemy HP (troop 136) | `ShowBattleAnimationB` (the Blazing Star, 128 to 130; Dyrnwyn, 117) | 2 |

The first three are battle commands the player picks, and they are the whole
of the "special" side of this game's combat. Without the pages the command
is chosen and nothing happens. They are also where three of the causes meet:
the multiplication, the variable amounts, and the animation on a monster. The
Last Stand page also needs the animation, so it is not freed by the other
two.

The last row is the one that may matter for the story:

* **Troop 96, three Cauldron-Born** (map 26, event 10, a fixed fight). Page
  8 gives them back their HP every three turns (unless switch 282 is on), page 9 has Gwydion say that
  they cannot be killed, and **page 11, at turn 6**, is Gwydion's Blazing
  Star, ends with `TerminateBattle`. That page is the one that does not
  compile. With it gone the fight cannot be won by attacking and cannot be
  ended by the story. *This was read in the dump, not played*: whether
  fleeing is allowed in that fight was not looked at.
* **Troop 136, the Horned King with Dyrnwyn** (map 78, event 6, the scene
  that opens with Eilonwy telling that "it was no use"). Page 1 triggers on
  the enemy's HP, speaks, plays Dyrnwyn's animation and ends the battle; the
  battle can still be fought without it, but it is the story's way out.

Both are the same command, `ShowBattleAnimationB`, which is not in
`TROOP_COMMANDS`. Accepting it **as a declared debt** (no animation, a wait
instead) would let both pages in and end both fights, at the cost of the
animation; doing it for real needs the battle scene to play an animation on a
monster, which today it does not for anything (the skills' own are the
existing [`animations-in-battle`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/animations-in-battle.md)).

### The 95 pages "with a trigger the ROM cannot look at"

All 95 are the single, empty page of a troop: no condition flag set (no
switch, no variable, no turn, no HP) and no command. `trigger()` in
`troops.rs` returns `None` for "looks at nothing", and the report counts that
under the same name as the real refusals (a fatigue condition, a number out
of range). An RM2k troop page without a condition **never runs**
(`AreConditionsMet` is false right away), so the cartridge loses nothing, and
the real troop pages that carry a condition and compile are 497 of the 651
that carry anything. No real "trigger" is refused in this game: the page
conditions it uses are switch (470), turn (87), and an enemy's HP (93 plus
one with a switch).

## The Frozen World

Maps 3,823 of 3,891 pages; common events 89 of 100; troops 0 of 80. The
report's "pages" counts maps 1 and 2 as if they were in the cartridge.

### The combat is on the maps

The game has 155 maps and none of its fights is a battle in the RM2k
sense: **0 `EnemyEncounter`** in the whole dump, and 80 troops that are one
empty page each. The fights are run by events:

* map 1, **Battle Screen**: 48 events, 165 pages, 28,989 commands; one of its
  events, `CombatController`, is a page of 1,801 commands (223 branches, 147
  common-event calls);
* map 2, **Plate Placement**: 51 events, 425 pages, 12,225 commands;
* map 3, **Command Grid** and map 14, **Use Menu**: the menus of a turn;
* common events 20, 21, 25 (the three heroes' level-ups), 23, 24, 37
  (Study), 26, 27, 36 (Steal), 31 (Party Statistics) and 38 (the HP
  percentages) are called from map 1 and map 14 and from nothing else; 15
  (BringUpMenu) is the pause menu, a parallel event.

A monster on a map is an event whose page tints the screen and **teleports to
map 1**: one read (Sandflower, map 12) sets a tint, a flash and a teleport
to map 1 on event touch. Of the game's 1,486 `Teleport` commands, 328 go to
map 1 and 363 to map 2 (these last almost all from inside maps 1, 2 and 3).
The pages that do not compile for it are the 324 that `converter.log` lists
"because of a teleport to a map that didn't make it into the ROM", on 72
maps, 198 of them map 3's (the command grid's own events). Of the 365 pages
in the dump that teleport to 1 or 2, 248 are triggered by the action key, 92
by an event's touch, 19 by the hero's touch and 6 are automatic; only
one monster page was read, so that every monster works that way is
inferred, not checked.

**Is the exclusion still true?** Both, yes, with the same message as in the
project (two builds, one for each map brought back):

* **Map 1**: `a page makes the hero flash, and actor 11 is drawn with
  rangedmelee[0], which an NPC of the map also uses`. The build stops there,
  at the first thing it checks, so what comes after (the 1.8 MB of code the
  re-sweep of 2026-10-10 mentioned) is not known; at 29,000 commands that
  number is hard to believe, but it was not checked. The cause is the
  existing draft [`flashing-hero-shares-a-palette-with-an-npc`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/flashing-hero-shares-a-palette-with-an-npc.md).
* **Map 2**: `a stream of map_code is 38179 bytes and 19968 fit in WRAM`.
  The existing draft
  [`map-streams-that-dont-fit-in-wram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/map-streams-that-dont-fit-in-wram.md).

Nothing in the game can be fought until at least these two are in. The
other causes below are the second step, and most of them live in map 1's own
neighbourhood.

### "Stops at the page as a whole"

Still one, and it is in map 1: event 7, page 6, `CombatController` (the 1,801
commands). The chase takes out its one culprit, `ChangeActorFace` (11, 9),
and the page still does not compile without any command to blame. **This is
a guess, not measured**: the page after the common events are compiled in
place is large, and every jump in the bytecode is an absolute 16-bit offset,
which a page of that size may not fit. It only matters when map 1 is in.

### The maps: 68 pages, six causes

| cause | pages | where |
|---|---|---|
| a literal backslash `\\` in a box | 38 (3 alone) | map 1 (17), **map 3 (18 pages: the stat readouts)**, map 14 events 8 to 10 |
| `\V[n]` in a box before an `InputNumber`, and `ControlVars` from an item count in the same pages | 5 | map 14 events 3 to 7 (the use-item menu: "[1] Health Candy (have \V[0103])") |
| `\V[n]` in a **choice option**, "[Keep Lutine's \V[0126] gold]" | 6 | maps 50 (2), 51, 128 (3): **three merchants** (consumables, "plates") |
| a branch on a switch past 1,023 | 6 (5 alone) | map 1 (3), map 14 event 15, map 153 event 6 (2 pages) |
| `ChangeMapTileset` | 8 alone | maps 9, 47, 99, 129 (4 pages), 149 |
| `ChangeActorFace` | 7 (5 alone) | maps 1 (3), 72, 76, 82, 120 |

The literal backslash is `\\` in RM2k text: a backslash on screen. It is
used as a separator in the stat readouts ("HP: \V[0031] \\ \V[0032]"), 320
lines in the game, and `escape_tail` keeps any backslash that is not one of
its escapes as a refusal (whether the console font has the glyph was not
looked at). The `\V[n]` case is
different: `\V` is turned into a mark only in the `ShowMessage` arm, and a
choice's options and the box in front of an `InputNumber` go through
`messages.add` as they are, so the escape stays in the text and the box is
refused. That is the shops: "Keep Lutine's gold" is the last option of every
one.

The branch on a switch past 1,023 is refused by `branch_bytes`; **the
command that sets one is not**. `ControlSwitches` has no such check, so 34
map pages (28 of them in the cartridge, on maps 19, 27, 31, 76 to 79, 86 to
89, 105 to 107, 111, 128, 131, 135, 138, 140, 143, 147, 151 and 154) and
the common events 11, 69 and 70 compile with an `OP_SWITCH` on a switch up
to 1,077, and `set_switch` indexes the 128-byte table with `n / 8`: up to
seven bytes of the low RAM that follows are written (Vampires Dawn goes up to
switch 1,643, eighty bytes). Map 19, event 12, page 1 starts
with `OP_SWITCH $041B, on` (switch 1,051). Read from the compiler and the
compiled output; the ROM was not run, and what sits after the table depends
on the linker.

### The common events: eleven

Called only from map 1 and map 14 (above): 20, 21, 25 and 31 stop at the
backslash alone; 23, 24 and 37 at
the backslash and a branch on a switch past 1,023 (1,059, 1,024, 1,025); 26,
27 and 36 only at that branch; 38 at `ControlVars` multiplied and divided
(`CalculateHPPercents`, called 11 times). The converter lists 15 and 31 as
"left out, not compiling" for the shared bodies; 15 is the pause menu and
teleports to 1, 2 and 14.

### The troops

80 of 80 "with a trigger the ROM cannot look at" are the same empty pages as
in the Book of Three; the game uses none. See above.

## Other games: the same causes, by count

Uses in the dump of all eight games, counting every page whether it
compiles or not (the commands the compiler refuses by variant; zero is not
shown):

| variant | Book of Three | Frozen World | Sunset | Vampires Dawn | others |
|---|--:|--:|--:|--:|---|
| `ControlVars` multiply | 53 | 3 | 4 | 1 | |
| `ControlVars` divide | | 3 | | 6 | |
| `ControlVars` from an item count | 5 | 13 | | 47 | |
| `ControlVars` random wider than 255 | 2 | | | | |
| `ControlVars` from an actor property other than HP and SP | | | | 163 | |
| `ControlVars` from a character's other property | | | | | Desert Nightmare 5 |
| `ControlVars` from "other" (not gold or timer) | | | | 11 | |
| `ControlVars` with a range or an indirect target | | | 1 | 1 | |
| `ChangeItems` item or amount from a variable | 54 | | | 81 | |
| `ChangeMonsterHP` amount from a variable | 52 | | | | |
| `ShowBattleAnimationB` | 56 | | | | |
| `ConditionalBranch` actor: HP / level / state | 6 / | | | / 321 / 9 | |
| `ConditionalBranch` switch past 1,023 | | 63 | | 39 | |
| `ControlSwitches` past 1,023 | | 78 | | 1,014 | |
| a choice's fifth option | 5 | | 21 | 21 | |
| `\V[n]` in a choice option | | 6 | | | |
| a literal backslash in a box | | 320 | | | |
| `ChangeActorFace` | | 13 | | 5 | Dooms 2 1 |
| `ChangeMapTileset` | | 10 | | 10 | |
| a letter outside ASCII in a box | | | 11 | 794 | Desert 13, El Dorado 1 |

A Blurred Line and El Dorado have none of the command variants (A Blurred
Line has the two `InputNumber`s that compile). The table counts a *command's*
variant, not the pages it keeps out: one page can have several. Where a
cause is already a task, it is in the next section.

## Silent holes: the rows for these two games

From [What the compiler ignores silently](2026-10-14-what-the-compiler-ignores-silently.md),
and measured again where that page did not say:

| hole | Book of Three | Frozen World | matters? |
|---|---|---|---|
| `PlayBGM`'s fade-in is dropped | 1 command | — | no: a fade on one track |
| a forced route's repeat flag is dropped | — | 1 command | not looked at |
| the timer's "also in battle" flag | 0 | 0 | no |
| `EnemyEncounter`'s first strike | 0 | 0 | no |
| `ShowInn`'s type | 12, all type A | — | nothing lost today |
| a map's save and escape flags | 0 maps forbid either | 0 maps forbid either | no (measured resolving the tree) |
| `overlap_forbidden` pages | 0 | 0 | no |
| translucent pages drawn opaque (a divergence) | 40 | 1 | cosmetic, known |
| **the elemental attributes are not applied in battle** | **66 of 80 enemies** | 38 of 45 | **Book of Three: yes**, its damage is the engine's. **Frozen World: no**, there is no engine battle, the maps' events compute the damage |

So the only silent hole that weighs in these two games is the elemental
attributes in the Book of Three. Everything else is a few commands or
nothing.

## What the existing tasks already cover

* Frozen World's map 1 and map 2: the two drafts above. Their texts said
  that what the exclusion loses "was not looked at"; it is this section.
* `route-the-missing-moves`, `book-of-three-hen-wens-second-talk-does-nothing`
  and `book-of-three-reraise-and-eilonwy-dont-compile` for the rows marked
  "existing".
* `page-conditions-on-switches-past-1023-read-other-ram`: the *condition* of
  a page past 1,023, which reads the wrong bit. It says the compiler refuses
  the commands that touch such a switch; only the branch is refused, and
  the new draft is about the commands (the branch refused, the `ControlSwitches`
  not).
* `monster-conditions-and-flashscreen-in-battle` and `release-troop-events`
  (done) are the earlier rounds of the troop pages.

## The drafts that came out of it

One for each cause not covered:

* `controlvars-random-ranges-wider-than-255` (row 5)
* `controlvars-multiply-and-divide` (row 8)
* `controlvars-from-an-item-count` (row 9)
* `changeitems-and-changemonsterhp-by-a-variable` (row 4)
* `show-battle-animation-b-in-troop-pages` (row 3)
* `a-choice-with-more-than-four-options` (row 10)
* `variables-in-a-choice-option-and-before-an-input-number` (row 7)
* `a-literal-backslash-in-messages` (row 6)
* `branches-and-switch-commands-past-switch-1023` (row 2)
* `changemaptileset-is-not-compiled` (row 11)
* `changeactorface-is-not-compiled` (row 12)
* `culprits-counts-empty-troop-pages-as-a-bad-trigger` (row 13)

And a "Known issues" line in each game's page for what a player sees.

## What this cannot see

* **Anything played.** All of this is read from the dump, the compiler and
  the report. Whether the Cauldron-Born fight can be left, whether the
  Frozen World's story is blocked by the missing combat or only by the
  first fight, and what the shops' absence costs, were not played.
* **What is behind a stop.** A page that fails at one command may fail at
  another after it: the report chases them one by one, but a build with map
  1 brought back stops at the first check, so what comes after the flash is
  unknown. The same for the Last Stand page: three commands in a row.
* **The "whole" page** is a guess (a page of that size and 16-bit offsets).
* **Counts of uses** are over the dump, by operand, by a script that repeats
  the checks of `compile.rs` for the commands listed, not by the compiler:
  they match the report's culprit uses where both exist (Book of Three
  `ChangeItems`, 54, `ChangeMonsterHP`, 52; Frozen World `ControlVars` item
  counts 13), but the table is not the compiler's.

## How to redo it

`just culprits` in each game writes `build/release/culprits.json`: its
`pages` list has every page that does not compile with its culprits (the
`parameters` are the operands the groups above are read from), its
`skipped_calls` the calls to a common event that does not compile, and its
`commands` the per-command totals. The converter's own list of pages cut for
a teleport to an excluded map is in `build/release/converter.log` ("because
of a teleport to a map that didn't make it into the ROM").

To see whether map 1 or map 2 of Frozen World still stops, remove one at a
time from `excluded` in `frozen-world/rm2k-snes.toml` of the ports and run
`just cartridges release` there (about forty seconds).

The troop pages: for each troop in `data/db/troops.json`, a page with no
`flags` set and no command other than the closing one is the "bad trigger".

The use counts: sweep every `event_commands` of the maps, the common events
and the troops of each game's `data/` and apply, to the commands named in the
table, the same checks as `compile_command` (the operation, the operand
kind, the range, the option index).
