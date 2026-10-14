# What the compiler ignores silently

> **Measured on 2026-10-14**, by Cardón, with the tools at `14e200fc`
> (the-advocate) and ABL at `f775b66` (the-advocate-ports), over `release`'s
> 308 maps, the 60 common events and the 300 troops of ABL's dump, and over
> the other seven games' data. It is a snapshot: the numbers are from that
> day and this file is not updated; how to redo each count is at the end. The
> task is
> [`what-the-compiler-ignores-silently`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/what-the-compiler-ignores-silently.md).

taro's question: "that's what I want to know: what is in those silent
holes". [The missing commands](2026-10-05-the-missing-commands.md) and the
culprits report say what keeps a page **out** of the cartridge. This is the
other kind: a page that is **in**, compiles, and has a field or a parameter
that nothing reads, so a feature is simply not there. Two were found the
hard way in the same week: the event's touch (`trigger` 2), whose pages
compiled to nothing, and the movement types 1 to 5, ignored. Nothing was
changed, built or run but the installed `rm2k-snes-events`.

## Summary

* **Page fields: nothing is left silent that ABL uses with a value other
  than the default.** Every field of an event page that ABL sets is read
  somewhere. The one exception, `overlap_forbidden` (17 pages), never
  belongs to an event that moves, so nothing is seen. Both holes of the
  week were of this kind and are closed.
* **Command parameters: three are new** that ABL sets to something other
  than the default and nothing reads: the **fade-in of `PlayBGM`** (3
  commands), the **repeat flag of a forced route** (6) and the **"also in
  battle" flag of the timer** (1). Everything else the probe found silent
  is either **declared** —in a comment, in the culprits, in the book—, or a
  slot that RM2k itself ignores.
* **The two that are worth the most are not commands.** A **map's own
  "can save" flag is never read**: in ABL it forbids saving on **75 of the
  308 maps** (the Kingdom of Surl and everything under it), and the pause menu follows only
  `ChangeSaveAccess`. And the **elemental attributes are not applied in
  battle**: **74 of the 100 enemies** the cartridge can fight take other
  than normal damage from an attribute the party carries, and the
  battle model (`rm2k-snes/battle` in the-advocate) has no attributes.
* **Sixteen silent things were already known** and the probe or the reading
  found them again, which is the evidence it sees what it should (list below).
* In the other seven games the same probe adds only things already known in
  the commands, but the new holes weigh more there: the can-save flag
  forbids saving on **all 430 maps of Vampires Dawn** and 88 of Dooms 2's
  92; the fade-in is used 46 times; the forced routes' repeat flag, 31.

## How it was measured

Three tools, because no one of them sees everything.

**A mutation probe, for the commands.** The event compiler reads the whole
game from the dump and answers with an `events.json`. For every
`(command code, parameter index)` that the cartridge's pages, the common
events and the troops use —272 pairs in ABL, 117,417 commands—, the probe
changes that parameter **in every command at once**, runs
`rm2k-snes-events compile` with the cartridge's own request, and compares the
answer's hash with the unchanged one. Two changes per pair (plus one, and
zero-or-one); an answer that does not move is a parameter **nothing read**.
For each value ABL actually uses it then tries four changes (plus one, to
zero-or-one, plus 37, minus one) on that value alone, 4,212 runs, so "read"
means "read for this value" and not "read for some other". An error counts as
read: it is loud, which is the other kind of problem. The three forks and the
new map the request carries are mutated too, or the pages in them would look
unread. The same probe ran over each of the other seven games' own request.

**Reading, for what the probe cannot tell.** An answer that does not move has
four causes and only one is a hole: nothing reads it; RM2k itself ignores the
slot; two values the compiler folds into one (every transition past the
fade is the fade); or a command inside a page that does not compile at all
(loud, and `culprits` says so). Each of the 23 unread pairs in ABL was read
against its arm in `compile.rs` and against easyrpg's interpreter, the book's reference for RPG_RT.

**Counting, for the fields the compiler does not look at.** The page fields,
the map's own flags and the database fields are read by other stages —Wally,
the converter, the battle model—, outside the event compiler's answer. For
those the method is a search of the Rust for the field, a read of what the
hit does, and a count of the values ABL uses over the cartridge.

## The page, field by field

ABL's 5,531 pages in the cartridge. "Read" means a line of code that acts on
it, not only copies it.

| field | ABL, other than the default | read? |
|---|---|---|
| `trigger` | touch 1,036 · event's touch 64 · auto 513 · parallel 351 | read; the event's touch since 2026-10-14 |
| `move_type` | 1: 4 · 2: 6 · 3: 17 · 4: 106 · 6: 38 pages with a route | read; 1 to 5 since 2026-10-14 |
| `move_frequency`, `move_speed` | 170 and 412 | read (`route::own`, the page table) |
| `animation_type` | 1: 231 · 2: 5 · 3: 258 · 4: 802 · 5: 4 | read (`turns`, `route::own`, Wally) |
| `layer` | 0: 2,611 · 1: 2,901 · above the hero: 19 | read (Wally, the table's layer) |
| `character_direction`, `character_pattern` | 1,971 and 472 | read (`rm2k-rules`, Wally) |
| `translucent` | 70 | read; drawn opaque, see [Translucent events end up opaque](../divergences/translucent-events-end-up-opaque.md) |
| conditions: switch A / B, variable, item, actor, timer | 2,196 · 298 · 14 · 52 · 30 · 1 | read (`pages.rs`) |
| `move_route.repeat`, `skippable` of a page's own route | 0 and 8 | read |
| **`overlap_forbidden`** | **17** | **not read** |

`overlap_forbidden` is RM2k 2003's "forbid overlap" and `WouldCollide` in
easyrpg is where it acts: it makes two events collide even on different
layers. None of ABL's 17 pages walks (`move_type` 0 all of them, and 15 have
no graphic), so there is nothing to collide with; Sunset Over Imdahl has 8
such pages and Vampires Dawn 32.

The route commands inside a page's own route and inside a `MoveEvent` are
decoded with their operands. Of the 31 codes the 3,515 forced routes of the
dump use (and the 37 own routes of the cartridge), every one is walked, folded or refused loudly, except the
ones listed under "Known" below (the transparency, the sound inside a page's
own route, and one change of graphic that does not fit in a map's table, which
the converter warns about).

## The commands: what the probe found silent

Of the 272 pairs, **240 moved the answer** for both changes. Nine moved it for
only one of them (booleans: `1` to `2` is `1`), and **23 never moved it**. The 23, after reading each:

| command · slot | ABL uses | what it is | where it stands |
|---|---|---|---|
| `ConditionalBranch` 5, `BattleConditionalBranch` 5 | 2,185 and 7,260 | the "has an else" flag; the compiler uses the `Else` command | not a hole |
| `ControlVars` 2 | 4,372 | the end of the range, with the range type off | RM2k ignores it too |
| `OpenShop` 3, `ShowInn` 2, `MovePicture` 4 and 7 | 43, 17, 33, 33 | slots RM2k's interpreter never reads | not a hole |
| `ShowChoice` text, `Comment` ×2 | 99, 33, 181 | the options come from `ShowChoiceOption`; a comment is a comment | not a hole |
| `MoveEvent` 3 | 3,333 (75 set) | the route's "skippable" | **known**: [A blocked step in a forced route](../divergences/a-blocked-step-in-a-forced-route.md) |
| `ChangeSystemBGM` ×6 | 130 | every operand | **known**: a declared debt, [The missing commands](2026-10-05-the-missing-commands.md) |
| `ChangeHeroTitle` ×2 | 11 | every operand | **known**: same |
| `ChangePBG` text | 8 | the panorama's name; its scroll is read | **known**: same |
| **`PlayBGM` 0** | **588 (3 set)** | **the fade-in, in milliseconds** | **new** |
| **`TimerOperation` 4** | **18 (1 set)** | **"also in battle"** | **new** |
| `EnemyEncounter` 5 | 51 (0 set) | the first strike | new, but ABL sets none; see the other games |

At the level of each value ABL uses, the answer never moved for these, after
the same reading: the pictures the map does not carry (`ShowPicture` 157,
`MovePicture` 17, `ErasePicture` 86 commands: a declared debt, their
position, size and effect with them); the operand slots that the target type
makes meaningless (`ChangeHP`, `ChangeCondition` and `FullHeal` take the actor
only when the target is not the whole party; `ChangeEquipment`'s item when it
unequips; `ControlVars`' second operand; `TimerOperation`'s seconds on a
stop); `EnemyEncounter`'s escape mode 2 and defeat mode 1, which both mean "the
handler decides" and the page's own blocks already say it; the labels' numbers, which only have to agree among
themselves; every `ChangeScreenTransitions` value past the fade, which is the
fade (the [teleport's transitions](../divergences/the-teleport-transitions.md));
and one more that **is** a hole: **`MoveEvent` 2, the route's "repeat"**, set
in 6 of 3,327 forced routes.

### What is not seen

* **`PlayBGM` fade-in**: 3 commands, on maps 16 and 18 (a 1,000 ms fade-in of
  a theme). The compiler reads the volume, the tempo and the balance and
  emits `OP_BGM` without a fade: the track starts at once. Elsewhere: Sunset
  Over Imdahl 25, Vampires Dawn 16, Dooms 2 4, The Book of Three 1.
* **The repeat flag of a forced route**: RM2k loops a route for ever when it
  is set; `OP_ROUTE` has no such bit, so the route runs once. ABL's 6 are the
  traffic on maps 8 and 9, in parallel pages that issue the route again every
  time they run, which hides it. Elsewhere: Vampires Dawn 27, Dooms 2 3,
  Frozen World 1.
* **The timer's "also in battle" flag**: RM2k keeps a timer counting through
  a battle when it is set, and pauses it otherwise. The compiler drops the
  bit with a comment that says there are no battles; there are. ABL's one is
  the quarry job's timer, on map 150. No other game sets it.
* **`EnemyEncounter`'s first strike**: ABL sets none. Dooms 2 sets 2 and
  Vampires Dawn 2.

## What is not in the pages

**Maps' own flags.** The tree's `teleport`, `escape` and `save` are
tri-states (inherit, allow, forbid) and nothing reads them: `rm2k-rules`'
tree resolves a map's music and battle background by inheritance, and stops
there. Resolved over the parents, **ABL forbids saving on 75 of the 308
maps** —all of them under "The Kingdom of Surl" (Memnosyne's Adobe, the Surl
roads and ruins, and the rest of that tree)— and escaping on 1 (map 105). The pause menu's Save follows `ChangeSaveAccess` and nothing
else. Dooms 2 forbids saving on 88 of 92 maps; Vampires Dawn forbids saving
on 430 of 430, escaping on 377 and teleporting on 422.

**Elemental attributes in battle.** The enemies' `attribute_ranks`, the
skills' `attribute_effects` and the weapons' `attribute_set` are not read by
the battle model or by anything else; `simulate.rs` says so in a comment
("what is missing: attributes, rows and the double attack") and no page of
the book does. Of the 100 enemies the cartridge can fight, **74** have a rank
other than neutral on an attribute the party's skills (39 of the 134 it
learns) or weapons (153) carry. A Flame skill on a Flame-weak enemy does
normal damage. The same data is in book three (66 of 80 enemies), El Dorado
and Frozen World (38 of 45 each) and Vampires Dawn (141 of 163).

**Smaller, measured, not worth a draft.** `bush_depth` (the hero's legs sunk
in a forest tile): 149 cells on map 5. A terrain's `encounter_rate`: no
cartridge map with random encounters walks on a terrain that changes it.
`skill_failure_message` of the usable skills (25) and the state messages
(`message_actor`, `message_enemy`, 18 and 20 states): the battle shows none,
and no skill gives a state in the model, which is [known](../divergences/what-battle-conditions-do-not-model.md).
The system's four menu sounds (cursor, decision, cancel, buzzer) are not read
by any tool; whether the runtime plays fixed ones was not checked.
`enemies.levitate` (3 of the 100): easyrpg does nothing with it either.
`hp_change_*` of the states: all thirty states have the type "none", so
nothing is lost.

## Known, and found again

The probe and the reading found these already written down, which is the
check that they see what they should:

1. `MoveEvent` skippable: 75 ([divergence](../divergences/a-blocked-step-in-a-forced-route.md)).
2. `ChangeSystemBGM`: 130 ([the missing commands](2026-10-05-the-missing-commands.md)).
3. `ChangeHeroTitle`: 11 (same).
4. `ChangePBG`'s picture: 8 (same).
5. `ShowPicture`, `MovePicture` and `ErasePicture` of a picture the map does
   not carry: 157, 17 and 86 ([large pictures](../divergences/what-large-pictures-do-not-model.md),
   [pictures as sprites](../divergences/what-pictures-as-sprites-do-not-model.md)).
6. Transparency in routes, `40` and `41`: 92 in the data (task
   [`route-transparency`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/route-transparency.md)).
7. Sound in a page's own route: 1 (task
   [`sounds-inside-move-routes`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/sounds-inside-move-routes.md)).
8. A route's change of graphic that does not fit in the map's table: 1, map
   207, which the converter warns about.
9. `WeatherEffects`: 18 (draft
   [`abl-it-does-not-rain-in-paradise`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-it-does-not-rain-in-paradise.md)).
10. `ChangeScreenTransitions` and `EraseScreen`: the transitions past the
    fade are the fade ([divergence](../divergences/the-teleport-transitions.md)).
11. A call to a common event that does not compile is skipped: 47
    ([divergence](../divergences/a-skipped-call.md)).
12. Translucent pages drawn opaque: 70 ([divergence](../divergences/translucent-events-end-up-opaque.md)).
13. The battle animations of skills, weapons and the unarmed attack
    (`animation_id`, `unarmed_animation`; task
    [`animations-in-battle`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/animations-in-battle.md)).
14. No skill gives or takes a condition ([divergence](../divergences/what-battle-conditions-do-not-model.md)).
15. The enemies' conditions other than "always" ([divergence](../divergences/what-the-enemies-ai-does-not-model.md)).
16. `ChangeFaceGraphic`, in the games that use it: a declared debt (task
    [`changefacegraphic-in-the-declared-debts`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/changefacegraphic-in-the-declared-debts.md)).

## The new holes, ranked

By what a player sees, then by ABL's count. Each has a draft.

| # | Hole | ABL | Other games | Draft |
|---|---|---|---|---|
| 1 | Elemental attributes are not applied in battle | 74 of 100 enemies; 39 skills, 153 weapons | 5 of the 7 | [`elemental-attributes-are-not-applied-in-battle`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/elemental-attributes-are-not-applied-in-battle.md) |
| 2 | A map's save and escape flags are never read | 75 maps (save), 1 (escape) | Dooms 2 88, Vampires Dawn 430 | [`a-maps-save-and-escape-flags-are-never-read`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-maps-save-and-escape-flags-are-never-read.md) |
| 3 | `PlayBGM`'s fade-in is dropped | 3 | 46 | [`playbgm-fade-in-is-dropped`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/playbgm-fade-in-is-dropped.md) |
| 4 | A forced route's repeat flag is dropped | 6 | 31 | [`a-forced-routes-repeat-flag-is-dropped`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-forced-routes-repeat-flag-is-dropped.md) |
| 5 | The timer's "also in battle" flag is dropped | 1 | 0 | [`the-timers-battle-flag-is-dropped`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-timers-battle-flag-is-dropped.md) |

Not drafted, listed above: `overlap_forbidden`, the first strike, the bush
depth.

## The other seven games

Run with the same probe and their own requests, and the unread parameters
that belong to compiled pages (not to a page `culprits` already keeps out).
Beyond what ABL showed, in the compiled pages of the others: the
declared `ChangeFaceGraphic` (Desert Nightmare 2,017 commands, Vampires Dawn
4,305) and `ChangeSystemGraphics` (Vampires Dawn 100), both known;
`ChangeSystemBGM` in Vampires Dawn (224); the screens' transition slot of
`EraseScreen` and `ShowScreen` in Desert Nightmare (695 and 636, all the
fade); the `ShowInn` type in The Book of Three (12, all set A, so nothing
lost today); and `CallEvent`'s page slot, always 0. **No other silent
parameter turned up.** The weight of the new holes in them is in the table
above.

## What this cannot see

* **A value ABL does not use.** The probe changes the values the game has. A
  parameter that is read for `0` and `1` and ignored for `2` is not found.
* **Anything the event compiler's answer does not carry.** The images, the
  maps' graphics, the battle model, the screens, the audio: they were
  searched for in the Rust, which finds a field nobody names but not a field
  somebody names and half-reads.
* **A command that compiles to the wrong thing.** The probe finds a
  parameter that changes nothing, not one that changes the wrong thing; that
  is the suite's job.
* **A page the compiler leaves out.** `culprits` counts those, and its report
  for ABL's cartridge is empty of them.
* **Whether any of this is seen playing.** The "what is seen" lines are what
  RM2k's interpreter does against what the compiler emits; none was played.

## How to redo it

The probe is a throwaway script, not kept; this is all it does. Copy the
game's dump, load every map, common event and troop of the cartridge, and
for each `(code, index)` write a copy of the dump with that parameter
changed in every command, and run

    rm2k-snes-events compile --data <copy> --request <the cartridge's events-request.json> --out <dir>

comparing the hash of `events.json` with the unchanged run. The request is
the one the build leaves with the cartridge; the forks it names in
`map_files` have to be copied and mutated too. 14 runs at a time, ABL's 272
pairs take about four minutes and the per-value pass about thirty. The
culprits are `rm2k-snes-events culprits` with the same data and request.
For a page's fields and the maps' flags: search the Rust for the name and
count the values over the dump. The attribute count crosses `troops` and the
cartridge's `encounter_troops` and `EnemyEncounter` commands for the enemies,
and the actors' skill lists and the weapon items for the party.
