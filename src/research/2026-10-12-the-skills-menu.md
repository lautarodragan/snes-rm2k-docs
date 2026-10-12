# The skills menu

> **Measured on 2026-10-12** by Mulita. The tools of the-advocate at
> `28e66b35`, the ports at `c97a0dd` (A Blurred Line's `abl.sfc`
> `e13ea666be9dc5ed`), easyrpg-player at `9e67927`. The original is the
> 2015 RPG_RT running under Wine on a retouched copy of A Blurred Line. It is
> a snapshot: the numbers are from that day and this file is not updated.
> How each number was obtained is at the end. The task is
> [`the-skills-menu`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-skills-menu.md).

taro, on 2026-10-12: "make the skills menu work. In ABL it's always
disabled. We could start by showing the skills, their descriptions and the
selector, but not implementing being able to use skills on the map, and
then implement that in a second phase." This is the first phase: what the
original does, what easyrpg says RM2k does, what the port already has, and
a plan for the other two, with what is going to bite.

## Summary

* **Tech Skill is grey because the runtime does not do it, not because of
  the game.** In the original it is enabled from the first step the player
  takes —the intro's rooftop, with Kersh, Core and Manta—, and Kersh's
  Healing Syringe already heals from it. The port greys every pause menu
  command the converter does not list as done (`MENU_DONE` in
  `rm2k-snes-screens`, `menu_enabled` in `runtime/menu.s`).
* **In ABL it matters more than it looks**: four of the game's systems are
  opened **only** from Tech Skill. Radin's Mix Formula and Field/Battery
  Repair, Sern's Weapon Forging and Emily's Change Tape are switch skills
  usable only on the map, and no event in the game turns on their switches
  —734, 979, 859 and 805—: their common events (42, 50, 44, 43) are reached
  by no other door. Today, in the port, those four systems cannot be
  entered. That is phase 3's first step, and the cheapest.
* **The data is already in the cartridge.** Every (actor, skill) pair the
  compiler knows of has its bit in `FAR_SKILL`, and every skill some actor
  can know —of type normal or switch, with a cost of up to 99— has its name,
  description, cost, type, scope, switch and effects in the converter's
  `skill_*` tables and in the text block, because the battle uses them.
  What phase 2 adds to the ROM is code and a few bytes per skill, not text.
* **It does not fit in the items screen's VRAM; it fits in the custom
  menu's.** ABL's widest page of the list —eight rows of two columns, the
  description in two lines and the status line— asks for some 336 tile
  pairs of the text layer with ABL's spacing; the items screen leaves 184,
  and the custom menus, which take the whole VRAM, 447. The skills screen is
  a full screen like the custom menus, and comes back to the map the way
  they do.
* **Bank 0 pays almost nothing**: the pause menu's dispatch, some twenty
  bytes, of the 1,467 the tightest cartridge has. The rest goes outside,
  about 1.2 KB for phase 2 and 1 KB for phase 3 —estimated from the
  comparable routines—, against 3,384 bytes left in bank 1 and 3,477 in
  bank `$C0` in the tightest games.
* **Six of the eight games use it**: A Blurred Line, Book of Three, Vampires
  Dawn and Frozen World teach dozens of skills, some usable on the map;
  Dooms 2 and El Dorado, two to four. Desert Nightmare and Sunset over
  Imdahl teach none. No game has a teleport or an escape skill an actor can
  learn, so phase 3 can leave those two types out.

## 1. Why Tech Skill is grey

In the port: `menu_enabled` looks up the command in `menu_done`, a table
the converter emits from `MENU_DONE` —Items, Equipment, Save and End
Game—, and greys what is not there; A over a grey command does nothing.
Skills was never in the list, so it is grey with any party, at any point
of any game. The pause menu's bank already carries the label in both
colours —`slots.rs` draws every option white and grey—, so enabling it
costs no tiles there.

In the original nothing greys it. RM2k's `Scene_Menu` only refuses Skills
with the party empty (easyrpg `scene_menu.cpp`, `GetActors().empty()`),
and A over an actor that cannot act —dead, or under a state that forbids
acting— buzzes. ABL never disables the menu at the start: its
`ChangeMainMenuAccess` commands are on maps 49, 53, 277 and 285. So:

* **At the intro**, the first moment the player walks, the party is
  Kersh, Core and Manta. Kersh starts at level 20 and knows Healing Syringe
  —a heal on an ally, 10 SP— and Agency Badge —on an enemy, grey on the
  map—; Core and Manta know only battle skills, all grey.
* **Then Talan**, alone, knows nothing: his list opens empty, with the bar
  on an empty first row. He learns his auras later, from common event 7
  (`AbsorbAuraAbilities`), with `ChangeSkills`: up to 54.

### ABL's Console is something else

The Console —a custom menu since 2026-10-04, see
[The custom menu](2026-10-04-el-menu-custom.md)— has a "Skills" tab too,
and they must not be confused. The Console's tab is the **game's own
bookkeeping**: Talan's aura tables are counters in variables 70 to 122
("how many times he absorbed it / how many are needed"), Sern's souls a
variable, Saldra's and Lerle's a count a common event makes. Tech Skill is
**the engine's list**: the skills the actor knows in the database's sense,
with their SP cost and description, which is what the battle offers. They
meet in one place: when Talan's counter reaches its cap, common event 7
teaches the skill with `ChangeSkills`, and from then on it shows in Tech
Skill —and the Console draws the dash for it—. They share no code beyond
the text layer and the full-screen VRAM layout, which the custom menu is
the template for (section 5).

## 2. What the original does

Captured with the 2015 RPG_RT, which is not the runtime the author used
but draws the same menu; the 2000 one was not run. On a copy of the game
whose map 4 —where a new game starts— builds a party of Kersh, Talan
(given 27 skills, to scroll), Radin (with his SP at 0) and Emily, hurts
Kersh and Talan, and takes it to Talan's apartment; and, separately, on the
untouched game, at the intro. Twenty-six captures, delivered with the
task.

**The screen**, at 320x240:

* **Top, the help window**, 32 pixels: the description of the skill under
  the cursor, one line, whole —the longest in ABL is 50 letters and fits in
  RM2k's 6-pixel font—.
* **Below, the status window**, 32 pixels: the name, "L" and the level,
  the condition ("Normal"), HP current/max and SP current/max, the terms in
  the system's red.
* **The list**, the rest: **two columns, ten rows**, each entry the name
  and, right-aligned, "- cost" —the dash is `easyrpg_skill_cost_separator`'s
  default, the number three digits wide—. **In the actor's order, which is
  skill-number order** (Heal 36, Advanced Heal 37, Cure 39, Antidote 42,
  Raise 45, Blind 51, Silence 52…), whatever order they were learned in.
* **Grey** what cannot be used here: battle-only skills (Agency Badge,
  Fire, Silence…), field skills whose SP the actor does not have (Radin's
  Dig Ingredients, 4, with 0 SP) —and a cost-0 one stays white with 0 SP
  (Mix Formula)—. Antidote, which cures a state that persists, is white
  even with nobody poisoned.
* **Scrolling**: the cursor moves by rows and columns, the window scrolls
  one row at a time when the cursor leaves it, and a small arrow at the
  bottom edge says there is more.
* **A name wider than its column runs over the cost**: "Field/Battery
  Repair- 0".
* **An actor with no skills** gets an empty list, the help empty, and the
  bar on the first row.

**Choosing**: from the pause menu, Tech Skill and then the actor, on the
same menu, like Equipment. B in the list goes back to the command column
with the cursor on Tech Skill.

* **A heal** (Healing Syringe, scope ally) opens the target window: on the
  left the skill's name and "Cost 10", on the right the party with the bar.
  A heals the chosen one —Kersh from 18 to 84 HP, SP 168 to 158— **and stays
  there**, as with a medicine; on a full-HP target nothing happens and no SP
  is spent (the buzzer). B goes back to the list with the cursor where it
  was.
* **A switch skill** (Change Tape, Mix Formula) closes the whole menu at
  once and its common event runs on the map: Emily's asks with a
  `ShowChoice` which tape; Radin's teleports to his own menu, a map with
  the ingredients.
* **A grey one**: A buzzes, nothing else.

## 3. What easyrpg says RM2k does

The files are `scene_skill.cpp`, `window_skill.cpp`,
`window_skillstatus.cpp`, `window_help.cpp`, `scene_actortarget.cpp`,
`window_targetstatus.cpp`, and the rules in `algo.cpp`, `game_actor.cpp`,
`game_battler.cpp` and `game_party.cpp`.

* **`Window_Skill`**: two columns; the actor's skill list as is
  (`GetSkills()`, which `LearnSkill` keeps sorted); on the map, every skill
  goes in —`CheckInclude` only filters in battle, and only in RM2k3—; an
  empty list is one empty row. Each entry is drawn grey or white by
  `CheckEnable`: learned **and** `Game_Actor::IsSkillUsable`.
* **`IsSkillUsable`, on the map**, in the order it looks:
  * the weapon requirement (`Game_Actor`): a skill with physical attributes
    and without `affect_attr_defence` needs a weapon with them;
  * **the cost**: SP below `sp_cost` is grey (HP cost is easyrpg's own);
  * **the states**: one with `restrict_skill` or `restrict_magic` greys the
    skills at or above its level;
  * **the type** (`Algo::IsSkillUsable`): escape and teleport need their
    access on, a target set and not to be flying; a **switch** skill, its
    `occasion_field`; a **normal** one, not to target enemies, and to touch
    HP or SP or **cure a state that persists** (`Persistence_persists`).
* **`Scene_Skill` on A**, if enabled: a switch skill plays its sound,
  `UseSkill` —switch on, SP spent— and `PopUntil(Map)`; a normal one opens
  `Scene_ActorTarget`; teleport, `Scene_Teleport`; escape, the escape
  target and a fade. Disabled: the buzzer.
* **`Scene_ActorTarget` for a skill**: the help window with the name,
  `Window_TargetStatus` with the `sp_cost` term and the cost, the party on
  the right. Scope **self** puts the cursor on the user and nowhere else;
  **party**, on everyone (`SetIndex(-100)`). A: if the user cannot pay,
  buzzer; else `Game_Party::UseSkill`, which spends the SP **only if it was
  of use**, plays the animation's sound, and refreshes. It does not leave.
* **`Game_Battler::UseSkill` outside battle**: the effect is
  `CalcSkillEffect` —power, attack by the physical rate over 20, spirit by
  the magical over 40, with the variance—; it cures the states it lists
  (death included: a revived one at 0 HP, without `affect_hp`, gets the
  effect as a percentage); and it raises HP or SP **only if not full and
  not dead**. `was_used` is what decides the SP and the buzzer.
* **`Scene_Menu`**: Skills asks for an actor that `CanAct()`.

**RM2k against RM2k3**, for what the eight games are —all RM2k—: RM2k3
adds the SP cost as a percentage (`sp_type`), the battle's skill subsets
by battle command (`CheckInclude` with `subset`), the subskill types
(treated as normal) and a configurable menu. On the map the two draw and
use the list the same way. Nothing of 2k3 is needed here.

## 4. The eight games

Measured over each game's dump: the skills some actor can know, by its
learning table or by a `ChangeSkills` to a fixed actor (none teaches by
variable or to the whole party); which of them the map can use by the rule
above, without SP or states; and the most one actor can know.

| game               | label        | known | usable on the map                       | most per actor     |
|--------------------|--------------|------:|-----------------------------------------|--------------------|
| A Blurred Line     | "Tech Skill" |   231 | 38: 33 heals and cures, 5 switch        | 54 (Talan)         |
| Book of Three      | "Special"    |   125 | 28: 22 heals and cures, 6 switch        | 22 (Fflewddur)     |
| Vampires Dawn      | "Skill"      |   102 | 21: 6 heals and cures, 15 switch        | 37 (Valnar)        |
| Frozen World       | "Tech Skill" |    52 | 12 heals and cures                      | 16                 |
| Dooms 2            | "Tech Skill" |     4 | 1 (First aid)                           | 2                  |
| El Dorado          | "Tech Skill" |     2 | none                                    | 2                  |
| Desert Nightmare   | (empty)      |     0 | —                                       | —                  |
| Sunset over Imdahl | (empty)      |     0 | —                                       | —                  |

The counts of "known" include actors that never join a party —RM2k's
sample actors are in several databases—; the per-actor maximum is what the
list has to hold.

* **No game teaches a teleport or an escape skill.** ABL (71, 72 and 149)
  and Book of Three (71 and 72) have them in the database, but no actor
  learns them.
* **Vampires Dawn is the one that leans on switch skills**: fifteen, its
  summons and transformations, each to a common event. Book of Three's six
  play a sound effect each (`Monster1`, `Cold3`…); ABL's play none.
* **Two of Vampires Dawn's skills cost 100 or more** (Apocalypse 100,
  Vampire Healing 120): the battle does not carry them —its list writes two
  digits, and `skill_usable` in `rm2k-snes-battle` leaves them out—, so
  today they are missing from the battle, and would be missing from the
  menu.
* **Healing on the map also unlocks the special items**: ABL has 18 items
  that cast a skill (its potions), Book of Three 15 and Vampires Dawn 4;
  today the items screen greys them. Phase 3's effect is what they need.

## 5. What the port already has

**Which skills each actor knows, now**: `FAR_SKILL`, one bit per (actor,
skill) pair, set from the learning table at reset, by leveling and by
`ChangeSkills`, and saved. `skill_pair_init` and `skill_pair_n` say where
each actor's pairs start and how many there are; they are contiguous and in
skill-number order, which is RM2k's list order. `skill_pair_k` gives each
pair its row in the converter's skill tables, or `$FF` if the battle does
not carry it.

**The skill tables** (`emit.rs`, outside bank 0): `skill_txt` and
`skill_desc` —the name and the description, whole, in the text block—,
`skill_sp`, `skill_type`, `skill_scope`, `skill_switch`, `skill_power`,
`skill_phys`, `skill_mag`, `skill_var`, `skill_hit` and `skill_affects`
(HP, SP, the four parameters, "targets enemies"). **Missing for the map**:
`occasion_field`, whether a state it cures persists, the sound effect, and
the weapon attributes. The first two fold into one precomputed bit per
skill —"the map can use it"—; the weapon requirement no skill of these
games was checked for.

**The battle's skill list** (`battle_skills.s`, bank `$C0`): `ba_skill_list`
walks the actor's pairs and keeps only the visible page in
`BA_SKILL_LIST` —it counts them all, `BA_SKILL_N`—, `ba_skill_see` scrolls
the way `Window_Selectable` does, and `ba_skill_window` writes each row as
the name **by reference** (`TL_BY_REF`: six bytes in the row's record,
however long the name), a dash and the cost, grey if the SP do not reach.
It is five rows of two columns, names cut at 11 cells (88 pixels) in
pixels, and the description one line, cut at 30 cells. The walk is what
the menu needs; it reads the actor from the battle's combatant record, so
it has to take the LDB actor as an argument to be shared.

**The pause menu** (`menu.s`, bank 0): the dispatch by command, the actor
choice on the menu itself (`menu_choose`, for Equipment), the return to the
command's row, and `CM_DIRTY`, with which a screen that overwrote the whole
VRAM gets the map back through `big_back_far` when the menu closes.

**The items screen** (`items.s`, **in bank 0**): the list, the
description in two lines (`3k + 1` and `3k + 2` in `item_texts`), the
scroll, and a switch item that turns on its switch and goes straight to the
map. It is the closest in behaviour, but its 184 pairs do not hold a skills
page, and it is in bank 0: it is a model to copy, not code to extend.

**The custom menus** (`custom_menu.s`, bank `$C0`): a full screen with the
text from VRAM word 0 up to `SCENE_MAP` (447 pairs), the System's windows on
BG1 at 8bpp, and the map back with `big_back_far`. **This is the template
for the skills screen's VRAM.**

**The actor choice** (`target_screen` in `menu.s`, bank 0, with
`actor_choice.s` and `medicine_use` outside): `Scene_ActorTarget` for a
medicine —the name composed in two strips of the menu's bank, "Owned Items"
and the count—, which stays on A and refreshes the HP. For a skill it needs
the cost instead of the count, the `sp_cost` term instead of
`possessed_items`, the whole-party and self cursors, and an effect routine
instead of `medicine_use`. **The name does not need a new table**:
`tl_strip` reads letters from an address, and the skill's name is in the
text block.

**The effect's pieces**: `eq_parameter` (equipment screen, bank 1) gives an
actor's attack and spirit with its equipment at its level, which is what
`CalcSkillEffect` asks of the user; `medicine_use` has the HP and SP clamps
and the revive. The battle's `ba_skill_effect` and `ba_variance` work on
combatant records and are the battle's contract with the model in
`rm2k-snes-battle`; the map version has to keep the same formula and,
for exact tests, its own order of random rolls.

**States**: outside battle this port keeps none —`medicine_use` says it—,
so a fallen actor is one at 0 HP, the condition always reads "Normal", and
a skill that cures a state other than death is white in the list and, used,
does nothing (the buzzer), as an Antidote does today.

## 6. What does not fit, and what is going to bite

**The text layer's pairs.** Estimated with the font's advances over each
game's widest page: eight rows of two names cut at 88 pixels, each with its
cost, the description in two lines and the status line.

| game            | spacing | worst page, pairs |
|-----------------|--------:|------------------:|
| A Blurred Line  |       0 |               305 |
| A Blurred Line  |       1 |               336 |
| A Blurred Line  |       2 |               354 |
| Vampires Dawn   |       0 |               291 |
| Book of Three   |       0 |               236 |
| Frozen World    |       0 |               187 |

The items screen leaves **184**, the battle **255**, the custom menus
**447**. Only the last holds it, so the screen takes the whole VRAM. It is an
estimate of the layout, not a measurement in the ROM: the converter has to
count it the way it counts the battle's list, and warn against 447.

**The description is too long for one line.** With ABL's spacing 1, 82 of
its 231 skills have a description wider than the 240 pixels a line gives
(Thunder's is 252): the battle cuts them, and calls it debt. The menu has
the room for two lines, as the items screen does, if the list loses rows:
224 lines are a 48-line help window, a 32-line status window and eight rows
of 16 with their frame. RM2k shows ten rows and one line of help; eight and
two is a divergence to write down. The split does not need more text: the
converter emits, per skill, where the second line starts, and both lines go
by reference.

**Names wider than their column**: 27 of ABL's 231 with spacing 1 (Gamble
for Credits, Field/Battery Repair…), cut at 88 pixels as the battle does.
The original runs them into the cost; cutting is the same debt the battle
declared.

**Bank space**, measured on each game's `release` and on ABL's test
cartridges:

| what       | tightest                      | free     |
|------------|-------------------------------|----------|
| bank 0     | ABL's `change-system`         | 1,467 B  |
| bank 1     | Vampires Dawn                 | 3,384 B  |
| bank `$C0` | Sunset over Imdahl            | 3,477 B  |
| far RAM    | Vampires Dawn                 | 53 B     |
| data banks | Vampires Dawn: none free, 170 B of gaps |   |

For scale, from ABL's `.dbg`: the items screen is some 700 bytes
(`items_screen`, `items_compose`, `items_row_paint`, `items_build_list`),
the battle's skill window 257 and its list walk 125, `target_screen` 187,
`medicine_use` 724, `ba_skill_effect` 298. **Phase 2 is some 1.2 KB and
phase 3 some 1 KB**, estimated from those. The game that bites is **Vampires
Dawn**: its data banks have 170 bytes left, so anything per skill the
converter adds has to go in the code banks, which have room, or it does
not build: a byte per carried skill fits there; a name per skill in the
medicines' `target_names` format, 22 bytes each, would not, and is not
needed. Its 53 bytes of
far RAM rule out keeping the whole list: walk the pairs every time and keep
the page, as the battle does, and borrow the battle's `BA_SKILL_*`, which
nobody uses while the menu is open. **Sunset over Imdahl** has the least
in bank `$C0` and teaches no skills: if the screen goes there, it can be
left out of games without skill pairs.

**Sounds.** A switch skill plays its own sound effect, and a heal the first
sound of its animation. Book of Three's and Vampires Dawn's switch skills
have one; the menu runs on the map, so the sound has to be in what the map
carries, or it is silent —the same trap as the rain's
[`parallel-common-events-sound-only-where-the-map-carries-it`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/parallel-common-events-sound-only-where-the-map-carries-it.md)—.

**The battle offers what the map can only use.** Reading the code: the
battle greys a skill only by its SP (`ba_skill_reaches`), and the battle
stage carries every normal or switch skill without looking at its
`occasion_battle`. So Emily's Change Tape and Radin's Mix Formula, which
RM2k greys in battle, are offered there. Not run in the ROM; a draft:
[`battle-offers-skills-that-are-only-for-the-map`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/battle-offers-skills-that-are-only-for-the-map.md).
The precomputed bit phase 2 needs is the same that fixes it, the other way
round.

**Vampires Dawn's skills of three digits**, missing in battle and in the
menu: a draft,
[`skills-that-cost-100-or-more-are-left-out`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/skills-that-cost-100-or-more-are-left-out.md).

**The test game does not exist yet**: as everything of the engine, the
screen's goldens live in ABL's suite, and the reference is
`rm2k-snes-screens`' `render`, as for the items and the equipment.

## 7. The plan for phase 2: the list

Nothing is used: A over an enabled skill does nothing yet, and over a grey
one, the buzzer that is not modelled either.

1. **The layout, in `rm2k-snes-screens`**: the skills screen's geometry
   —help 48 lines with two of text, status 32, eight rows of two columns,
   the name at 11 cells, the dash and the cost right-aligned—, its windows
   as a BG1 tilemap at 8bpp (`borders.rs`), and its `render`, which is the
   reference the goldens are compared against. The converter splits each
   description at the line's width and counts the busiest page's pairs
   against 447, warning like the battle's list. The divergence —eight rows,
   two lines— goes to the book with it.
2. **The data, in `mapdata`**: per carried skill, one byte of flags —usable
   on the map by RM2k's rule without SP and states; needs a target; switch—
   and one of where the description breaks; `MENU_DONE` gains Skills. In
   the code banks, for Vampires Dawn's sake (section 6).
3. **The walk, shared**: `ba_skill_list`'s loop takes the LDB actor and the
   page size from its caller, so the battle and the menu walk the pairs the
   same way. The menu borrows `BA_SKILL_LIST` and its neighbours.
4. **The screen, `skills_screen.s`, outside bank 0**: the custom menus' VRAM
   —text from word 0 to `SCENE_MAP`, windows on BG1— and `CM_DIRTY`, so the
   map comes back through `big_back_far` when the pause menu closes. The
   status line —name, level, "Normal", HP and SP—, the list by reference,
   grey by the flag and by the SP, the help in two lines by reference, the
   bar, up, down, left and right as `Window_Selectable` moves in two
   columns, the scroll of `ba_skill_see`, and the arrows if the screens
   stage gives them. B goes back to the menu on Tech Skill.
5. **The pause menu, in bank 0**: Skills needs a party, like Items; on A,
   `menu_choose`, an actor at 0 HP refused (`CanAct`), and the screen. Some
   twenty bytes.
6. **ABL's tests**: a case like the Wine copy's —Kersh, Talan with
   twenty-odd skills, Radin without SP, and someone with none—, and goldens
   of the list, the list scrolled, the grey ones and the empty one, each
   compared with `render` and looked at next to the captures of the
   original. And the space of every game, before merging.

## 8. The plan for phase 3: using them

In the order the games need it:

1. **Switch skills** —every one of ABL's map skills that opens a system,
   all of Vampires Dawn's summons—: SP spent, the skill's sound, the switch
   on, and straight to the map, as a switch item does today. Small, and it
   is what makes ABL's alchemy, forging, tapes and repairs reachable. Test:
   Mix Formula takes the party to Radin's map, Change Tape asks.
2. **Heals on one ally, on oneself and on the party**: `target_screen`
   generalised —or a twin outside bank 0— with the skill's name, the cost
   term and the cost, and the cursor on one, on the user, or on everyone; an
   effect routine with `CalcSkillEffect` from the user's `eq_parameter`,
   the variance, the HP and SP clamps and the revive of `medicine_use`, and
   the SP spent only if it was of use; it stays on the choice. Tests on the
   numbers, with the model's formula, as `test_curar.py` does for a
   medicine.
3. **The special items**, with the same effect: the items screen stops
   greying the potions that cast a skill. A task of its own.
4. **Teleport and escape**: no game needs them. Left grey, with a converter
   warning if a game ever teaches one.

## 9. Follow-up tasks proposed

Not created yet: they are for whoever decides the order.

* **The skills screen**, phase 2, section 7.
* **Switch skills from the menu**, phase 3.1: the one ABL needs to reach
  four of its systems.
* **Healing skills from the menu**, phase 3.2.
* **Items that cast a skill outside battle**, phase 3.3, for ABL's
  potions.
* The two drafts of section 6: the battle offering field-only skills, and
  Vampires Dawn's three-digit costs.

## How it was measured

* **The original**: the 2015 RPG_RT with Wine on its own Xvfb display, over
  a copy of ABL whose `Map0004.lmu` was rewritten with Ditto —one autostart
  page: `ChangePartyMembers`, `ChangeSkills`, `ChangeHP`, `ChangeSP` and a
  `Teleport` to map 7, (15, 7)—, and the untouched game for the intro;
  `xdotool` for the keys and ImageMagick for the captures, cut to 640x480
  and halved to 320x240.
* **Why it is grey**: `menu_enabled` and `menu_done` in the runtime and
  the converter, and the original's menu at the intro.
* **The eight games**: each `data/db` —actors' learning tables, skills,
  states, terms— and every `ChangeSkills` (code 10440) in maps, common
  events and troops; the map rule is easyrpg's `Game_Party::IsSkillUsable`
  without a target. Who turns on ABL's switch skills' switches: every
  `ControlSwitches` (10210) of maps and common events.
* **The pairs**: the advances of `low-variable.png` plus each game's
  `letter_spacing`, names cut at 88 pixels, two-digit costs at three cells,
  the widest description at two lines, and 26 pairs for the status line;
  per actor, the twenty widest of what it can know. An estimate of the
  layout, not of the ROM.
* **The space**: `rm2k-snes-space` over each game's `release` and ABL's
  test cartridges, as built from the commits at the top.
* **The code's sizes**: the `scope` sizes in ABL's `abl.sfc.dbg`.
