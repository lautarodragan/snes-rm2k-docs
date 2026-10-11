# The missing commands

> **Written on 2026-10-05 at `6094a205`** (snes-rm2k), by Aguará, with ABL at
> `b28864d`. It is a snapshot: the numbers are from that day and this file is
> not updated. How to redo each count is at the end, in "How it was
> measured".

taro's question: "which event system commands are we still missing?".
Measured over **the whole game**: the 5,601 pages of the 328 maps, the 60
common events and the 4,588 troop pages, and not just what `release`
carries.

## Summary

* **Very little is missing on the maps.** Of 5,601 pages, **5,565**
  compile. The 36 that do not compile are blocked by **seven things**, and
  each page has only one: there is none that needs two different commands.
  None is in `release`.
* **Thirty-one of those 36 are a single variant**: `ConditionalBranch`
  asking which way the hero is facing, in the rooms of Eisen's simulation
  (maps 281 to 344). The other five are one-offs.
* **What blocks the next day is `EraseEvent`**, twice: the start of the job
  at the quarry (map 150, event 4) and the common event that keeps its time
  (36, `ManageQuarryTimer`). The quarry one is the only missing command in
  everything reachable from the farm: the other maps that 108, 114, 117 and
  127 jump to —142, 152, 158, 160— already compile whole.
* **More is missing in battle**, and it is more expensive:
  `ChangeMonsterCondition` leaves out 164 troop pages, 140 of them together
  with `FlashScreen`. They are two whole skills, Talan's `Inscribe` (switch
  799) and `ControlMachines` (803), and both are already used in the
  battles of `release`.
* **What is lost without a page dropping** —a call to a common event that
  does not compile, which is skipped— is today **47 calls**, all to common
  event 45 from the same simulation rooms, because of a `ControlVars` with a
  constant that does not fit in 16 bits.
* **Where to start**: the two quarry `EraseEvent`s, because they are the
  only thing between the farm and the next day; then, in a single batch, the
  five small ones on the maps; and battle —`FlashScreen` in the scene and a
  decision about conditions— as its own job. See "Recommendation".

## How it was counted

With a new tool, `rm2k-snes-events culprits` (see the crate's README), which
stays: the compiler says at which command a page that does not compile
stops, and the tool **chases** every page —notes the culprit, removes it,
compiles again— until it compiles. That yields every command that blocks it,
and from there what matters for choosing: **how many pages a command alone
leaves out**, which are the ones that would get in if it were done.

Each page is compiled the way the cartridge compiles it: map pages with
their map, like `scan`, and with the `TileSubstitution`s resolved the way
`compile` resolves them where the request carries them; common events as a
shared body —a call to another common event is a call, not its body pasted
in—; troop pages with the battle's command list and its window. A command
counts with its parts: an `else` or an end of block belongs to its branch,
an option belongs to its choice.

Two things in the count that are **not** commands, and were set apart:

* **A `Teleport` to a map the cartridge does not carry does not compile**,
  on purpose: with `--every-map` all maps are there, so it does not show up.
  In `release` it blocks 18 pages, and they are the frontier: the exits from
  the farm to the next day (108 → 150, 114 → 160, 117 → 142, 127 → 152 and
  158), and those of test maps 261 and 269.
* **137 troop pages have no condition at all**, and in RM2k a page like that
  never runs (`AreConditionsMet` returns false). Nothing is lost: it is an
  empty body copied into 137 troops.

## 1. Every command the game uses

Uses and pages by page type: maps / common events / troops. "Blocking uses"
is how many of those uses leave their page out. A command with "yes"
compiles in all its uses; "partly" means it compiles with some parameters
and not others —the variant is in section 2—.

Troops copy their systems' pages into every troop: the 4,588 pages are
**295 distinct bodies**, so their numbers are inflated by the copies, not by
variety.

| code | command | uses (m / c / t) | pages (m / c / t) | blocking uses (m / c / t) | compiles? |
|---|---|---|---|---|---|
| 10110 | ShowMessage | 6938 / 76 / 6888 | 2140 / 13 / 1742 | 0 / 0 / 0 | yes |
| 10210 | ControlSwitches | 1668 / 182 / 8291 | 1155 / 24 / 4445 | 0 / 0 / 0 | yes |
| 13310 | ConditionalBranchB | 0 / 0 / 7260 | 0 / 0 / 1322 | 0 / 0 / 0 | yes |
| 10330 | ChangePartyMembers | 429 / 40 / 5040 | 125 / 2 / 2520 | 0 / 0 / 0 | yes |
| 10220 | ControlVars | 1688 / 211 / 2451 | 597 / 28 / 1320 | 4 / 6 / 0 | partly |
| 11410 | Wait | 3562 / 6 / 0 | 813 / 2 / 0 | 0 / 0 / 0 | yes |
| 11550 | PlaySound | 1250 / 26 / 2242 | 819 / 5 / 422 | 0 / 0 / 0 | yes |
| 11330 | MoveEvent | 3444 / 6 / 0 | 1013 / 5 / 0 | 1 / 1 / 0 | partly |
| 12010 | ConditionalBranch | 1523 / 615 / 0 | 534 / 33 / 0 | 124 / 0 / 0 | partly |
| 10320 | ChangeItems | 509 / 21 / 706 | 321 / 5 / 310 | 0 / 0 / 0 | yes |
| 10120 | MessageOptions | 1099 / 11 / 0 | 404 / 5 / 0 | 0 / 0 / 0 | yes |
| 10810 | Teleport | 1069 / 10 / 0 | 958 / 5 / 0 | 0 / 0 / 0 | yes |
| 13110 | ChangeMonsterHP | 0 / 0 / 1045 | 0 / 0 / 410 | 0 / 0 / 0 | yes |
| 11040 | FlashScreen | 60 / 0 / 840 | 38 / 0 / 140 | 0 / 0 / 840 | not in battle |
| 10440 | ChangeSkills | 20 / 173 / 705 | 12 / 5 / 331 | 0 / 0 / 0 | yes |
| 10460 | ChangeHP | 11 / 1 / 829 | 7 / 1 / 549 | 0 / 0 / 0 | yes |
| 11030 | TintScreen | 826 / 0 / 2 | 400 / 0 / 2 | 0 / 0 / 2 | not in battle |
| 11340 | ProceedWithMovement | 818 / 2 / 0 | 370 / 2 / 0 | 0 / 0 / 0 | yes |
| 10860 | ChangeEventLocation | 749 / 0 / 0 | 276 / 0 / 0 | 0 / 0 / 0 | yes |
| 10450 | ChangeEquipment | 34 / 1 / 560 | 9 / 1 / 140 | 0 / 0 / 0 | yes |
| 11510 | PlayBGM | 168 / 0 / 420 | 117 / 0 / 140 | 0 / 0 / 0 | yes |
| 11210 | ShowBattleAnimation | 388 / 0 / 0 | 287 / 0 / 0 | 0 / 0 / 0 | yes |
| 11110 | ShowPicture | 34 / 314 / 0 | 23 / 18 / 0 | 0 / 0 / 0 | yes (see 3) |
| 12330 | CallEvent | 224 / 114 / 0 | 205 / 7 / 0 | 0 / 0 / 0 | yes (see 3) |
| 10480 | ChangeCondition | 16 / 0 / 280 | 16 / 0 / 280 | 0 / 0 / 0 | yes (see 3) |
| 13130 | ChangeMonsterCondition | 0 / 0 / 268 | 0 / 0 / 164 | 0 / 0 / 268 | no |
| 13120 | ChangeMonsterMP | 0 / 0 / 229 | 0 / 0 / 140 | 0 / 0 / 0 | yes |
| 10630 | ChangeSpriteAssociation | 212 / 0 / 0 | 103 / 0 / 0 | 0 / 0 / 0 | yes |
| 11130 | ErasePicture | 23 / 139 / 0 | 17 / 8 / 0 | 0 / 0 / 0 | yes (see 3) |
| 11060 | PanScreen | 135 / 0 / 0 | 72 / 0 / 0 | 0 / 0 / 0 | yes |
| 10660 | ChangeSystemBGM | 130 / 0 / 0 | 41 / 0 / 0 | 0 / 0 / 0 | yes (see 3) |
| 11320 | FlashSprite | 113 / 0 / 0 | 92 / 0 / 0 | 0 / 0 / 0 | yes |
| 10140 | ShowChoice | 98 / 1 / 0 | 70 / 1 / 0 | 0 / 0 / 0 | yes |
| 12120 | JumpToLabel | 8 / 86 / 0 | 8 / 3 / 0 | 0 / 0 / 0 | yes |
| 11520 | FadeOutBGM | 81 / 0 / 0 | 62 / 0 / 0 | 0 / 0 / 0 | yes |
| 10490 | FullHeal | 54 / 19 / 0 | 38 / 1 / 0 | 0 / 0 / 0 | yes |
| 11930 | ChangeSaveAccess | 70 / 2 / 0 | 70 / 2 / 0 | 0 / 0 / 0 | yes |
| 10830 | RecallToLocation | 60 / 0 / 0 | 60 / 0 / 0 | 0 / 0 / 0 | yes |
| 11840 | ChangeEscapeAccess | 58 / 0 / 0 | 38 / 0 / 0 | 0 / 0 / 0 | yes |
| 10310 | ChangeGold | 48 / 4 / 0 | 40 / 3 / 0 | 1 / 3 / 0 | partly |
| 10710 | EnemyEncounter | 51 / 0 / 0 | 40 / 0 / 0 | 0 / 0 / 0 | yes |
| 11610 | KeyInputProc | 32 / 17 / 0 | 31 / 4 / 0 | 0 / 0 / 0 | yes |
| 10720 | OpenShop | 43 / 0 / 0 | 40 / 0 / 0 | 0 / 0 / 0 | yes |
| 10870 | TradeEventLocations | 40 / 0 / 0 | 30 / 0 / 0 | 0 / 0 / 0 | yes |
| 11910 | OpenSaveMenu | 34 / 0 / 0 | 34 / 0 / 0 | 0 / 0 / 0 | yes |
| 11120 | MovePicture | 16 / 17 / 0 | 11 / 2 / 0 | 0 / 0 / 0 | yes (see 3) |
| 11050 | ShakeScreen | 29 / 0 / 2 | 17 / 0 / 2 | 0 / 0 / 0 | yes |
| 12110 | Label | 8 / 20 / 0 | 8 / 3 / 0 | 0 / 0 / 0 | yes |
| 12410 | Comment | 8 / 15 / 0 | 5 / 7 / 0 | 0 / 0 / 0 | yes |
| 10690 | ChangeScreenTransitions | 20 / 0 / 0 | 15 / 0 / 0 | 1 / 0 / 0 | partly |
| 11740 | ChangeEncounterSteps | 19 / 0 / 0 | 15 / 0 / 0 | 0 / 0 / 0 | yes |
| 10230 | TimerOperation | 16 / 2 / 0 | 7 / 1 / 0 | 0 / 0 / 0 | yes |
| 10730 | ShowInn | 18 / 0 / 0 | 18 / 0 / 0 | 0 / 0 / 0 | yes |
| 11070 | WeatherEffects | 16 / 2 / 0 | 12 / 1 / 0 | 0 / 0 / 0 | yes |
| 11750 | TileSubstitution | 10 / 0 / 0 | 5 / 0 / 0 | 0 / 0 / 0 | yes |
| 10620 | ChangeHeroTitle | 8 / 0 / 0 | 6 / 0 / 0 | 0 / 0 / 0 | yes (see 3) |
| 11720 | ChangePBG | 8 / 0 / 0 | 1 / 0 / 0 | 0 / 0 / 0 | yes (see 3) |
| 10820 | MemorizeLocation | 1 / 6 / 0 | 1 / 3 / 0 | 0 / 0 / 0 | yes |
| 12420 | GameOver | 6 / 0 / 0 | 4 / 0 / 0 | 0 / 0 / 0 | yes |
| 12320 | EraseEvent | 2 / 2 / 0 | 2 / 1 / 0 | 1 / 2 / 0 | partly |
| 11530 | MemorizeBGM | 4 / 0 / 0 | 4 / 0 / 0 | 0 / 0 / 0 | yes |
| 11540 | PlayMemorizedBGM | 4 / 0 / 0 | 4 / 0 / 0 | 0 / 0 / 0 | yes |
| 11960 | ChangeMainMenuAccess | 4 / 0 / 0 | 4 / 0 / 0 | 0 / 0 / 0 | yes |
| 13150 | ShowHiddenMonster | 0 / 0 / 3 | 0 / 0 / 3 | 0 / 0 / 0 | yes |
| 10150 | InputNumber | 2 / 0 / 0 | 2 / 0 / 0 | 0 / 0 / 0 | yes |
| 12510 | ReturntoTitleScreen | 2 / 0 / 0 | 2 / 0 / 0 | 0 / 0 / 0 | yes |
| 10910 | StoreTerrainID | 1 / 0 / 0 | 1 / 0 / 0 | 0 / 0 / 0 | yes |
| 11350 | HaltAllMovement | 1 / 0 / 0 | 1 / 0 / 0 | 0 / 0 / 0 | yes |
| 10470 | ChangeSP | 0 / 1 / 0 | 0 / 1 / 0 | 0 / 0 / 0 | yes |
| 13410 | TerminateBattle | 0 / 0 / 1 | 0 / 0 / 1 | 0 / 0 / 1 | no |

That is **70 commands**: of RM2k's ~130, the game does not use the rest —no
vehicle, no `Loop`, no shop with branches—. That a command the compiler does
not know (`Loop`, `ChangeBattleBG`) is not in the table means just that:
there is no use to bring over.

## 2. What is missing, ordered by pages it unblocks

"Alone" are the pages that would get in if that one were done and nothing
else; "with others", those that also need something else; "calls" are the
calls from a map to a common event that are skipped because of it. On maps
and common events there is no page "with others": each one has a single
culprit.

| what is missing | type | alone | with others | calls | where | on the path? | cost |
|---|---|---|---|---|---|---|---|
| `ChangeMonsterCondition`, putting a condition on an enemy | troops | 24 (3 bodies) | 140 (3 bodies), with `FlashScreen` | — | 164 troops | **yes**: at least 66 of those pages belong to troops of `release`'s random encounters | large |
| `ConditionalBranch` on a character's direction (type 6) | maps | 31 | 0 | — | 281–283, 324–340, 342–344: Eisen's simulation | no | small |
| `ControlVars` with a constant outside 16 bits (999999) | common events | 1 (common event 45) | 0 | **47** | the same simulation rooms | no | small, with a decision |
| `ChangeGold` by variable | maps and common events | 4 (map 321; common events 5, 6, 44) | 0 | — | Sern's forge; the bets | no | small |
| `EraseEvent` before a jump, for real | maps | 1 | 0 | — | 150, the quarry | **yes: the next day** | medium |
| `EraseEvent` in a common event —in RM2k it does nothing— | common events | 1 (common event 36) | 0 | — | the quarry's clock | **yes: the next day** | small |
| `ControlVars` with an event's screen position (type 6, fields 4 and 5) | maps | 1 | 0 | — | 207, Memnosyne's Adobe | no | medium |
| `ChangeScreenTransitions`, show with a cut (19) | maps | 1 | 0 | — | 302, Screen Adjust | no | small |
| `MoveEvent` with "move away from hero" (10) | maps | 1 | 0 | — | 330, Room J | no | small |
| `TintScreen` in battle | troops | 1 | 1, with `TerminateBattle` | — | 2 troops | unknown | medium |
| `FlashScreen` in battle | troops | 0 | 140, with `ChangeMonsterCondition` | — | 140 troops | **yes**, with the one above | medium |
| `TerminateBattle` | troops | 0 | 1, with `TintScreen` | — | 1 troop | unknown | small |

Common event 32 shows up in the report with a `MoveEvent` on event 2, which
does not compile without a map; it is called from 114 and compiles there. It
was discounted.

### The map ones, one by one

**`ConditionalBranch` on direction** (`[6, character, direction]`). The 31
are the same autostart copied into every room of Eisen's simulation:
depending on which way the hero is facing, it moves an event to the cell in
front. The ROM already has `hero_dir` and `OP_IF` already has classes; it is
one more class that reads the direction of the hero or of an event.
EasyRPG: `CommandConditionalBranch`, `case 6`. **Small.**

**`ControlVars` = 999999**, common event 45 (`SimClearTweenRooms`), which
those same rooms call 47 times: it sets the saved coordinates to 999999 as
"none". The ROM's variables are 16-bit and RM2k goes up to ±9,999,999. It is
small to do —saturating at the 16-bit ceiling— but it is a divergence that
has to be declared, and it is worth checking first that nobody compares
those variables against something greater than 32,767. **Small, with a
decision.** Without it and without the one above the simulation does not
work; with both, it gets in whole.

**`ChangeGold` by variable** (`[operation, 1, variable]`). The compiler's
comment says "not possible without variables": it predates them. It is one
more bit in `OP_GOLD` and the variable's slot. It is used by Sern's forge
—common event 44 and map 321 exchange gold for forge points and give it
back— and by the bets (common events 5 and 6, called by 35). Careful: the
forge stores gold in a variable, and the ROM's gold is 24-bit. **Small.**

**`EraseEvent` for real**, the one on map 150: Sern starts the quarry job,
the hero jumps **within the same map** and the event is erased. Today it
only compiles after a jump to another map, where RM2k erases nobody. Doing
it needs state in the ROM: one bit per event that loading the map clears and
that the page refresh looks at to leave it without a page; EasyRPG
(`CommandEraseEvent`) also cuts a parallel one dead. It does not travel in
the save, which today does not store events
([`divergencias/la-partida-no-guarda-los-eventos.md`](../divergences/la-partida-no-guarda-los-eventos.md)).
**Medium.**

**`EraseEvent` in a common event**, 36 (`ManageQuarryTimer`, parallel with
switch 450), which closes the job when time runs out. In RM2k it does
nothing: `GetThisEventId` gives 0 in a common event and `CommandEraseEvent`
returns without touching anybody. It is only the compiler's: accept it empty
when what is being compiled is a common event. Careful with the inlined
case: a common event called from a page is compiled today with that page's
context, and there the `EraseEvent` must not erase the caller either.
**Small.**

**`ControlVars` with an event's screen position** (`[…, 6, 10005, 4]` and
`5`): map 207 puts smoke with `ShowPicture` over an event. The ROM knows
where it draws each event, but the console's screen is not RM2k's, and the
picture has to land in the same place as the smoke —`ShowPicture` by
variables already compiles—: it has to be decided which coordinates are
spoken. EasyRPG: `ControlVariables::Event`, `GetScreenX`. **Medium.**

**`ChangeScreenTransitions` to show with a cut**, map 302. The compiler
already does the cut for erasing and leaves out the one for showing "because
no map used it": this one uses it. **Small.**

**`MoveEvent` with "move away from hero"** (10), map 330. "Move toward" (9)
already exists; moving away is the same computation with the opposite
direction (`Game_Character::MoveAwayFromCharacter`). **Small.**

### The battle ones

**`ChangeMonsterCondition`** with two conditions: 22, `Control` —"is being
controlled!", restriction 3, four turns, released by damage— and 23,
`BarkWall` —lowers attack, defense and agility, two turns—. Battle has no
conditions, and making them is a system: duration, restrictions, the
controlled one's AI, what each one changes. EasyRPG: `Game_Battler`'s
`AddState`. **Large.** There is a small way out: accepting it without doing
it, as debt, and thus unblocking the 24 pages of `ControlMachines` and, with
`FlashScreen`, the 140 of `Inscribe`, knowing that `Control` and `BarkWall`
do not happen. It is a decision for taro.

**`FlashScreen`** in battle, six per `Inscribe` page. It exists on the map;
in battle it "tints the map's palette and not the scene's"
([`eventos-de-tropa-en-la-pelea`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/eventos-de-tropa-en-la-pelea.md)). **Medium**, and
**`TintScreen`** in battle goes the same way. **`TerminateBattle`** is
ending the battle without a result: small, a single page.

## 3. What the compiler accepts and does not do

`IGNORABLE`, the list of what is accepted because doing nothing is not
visible, **is empty** since 2026-10-04. What there is are **debts**: commands
that do something the ROM does not do, accepted because otherwise the whole
page would drop. The named list is `ACCEPTED_UNDONE`, in `compile.rs`, and
the reason for each one is in its arm of `compile_command`:

| what | why it is accepted | what is lost |
|---|---|---|
| `ShowPicture`, `MovePicture`, `ErasePicture` of a picture the map does not carry | the map chooses which pictures it carries; stopping the page took away from the game pages that work today | the picture does not appear |
| `ChangeSystemBGM` (130 uses, 25 maps) | it is an audio feature, not a command: the system song would have to travel in the save and go into the packages | battle in those areas plays the LDB's song |
| `ChangeHeroTitle` (8 uses, all Talan's) | the port shows the title nowhere: there is no status screen | nothing visible today |

And outside that list, accepted empty on purpose:

* **`ChangePBG`**: the panorama. In mode 3 there is no free layer; a single
  page, map 13's Hover-Tram.
* **`Comment`**: it does nothing in RM2k either. It is not debt.
* **`EraseEvent` after a jump to another map**: in RM2k it erases nobody. It
  is not debt.
* **`ChangeCondition` removing a condition that is not death**: there are no
  conditions to remove. Adding a condition does not compile, and nobody asks
  for it on a map.
* **`TileSubstitution` of a tile the map does not draw**: there is no cell
  to change.
* **A call to an event that does not compile is skipped**
  ([`divergencias/llamada-salteada.md`](../divergences/llamada-salteada.md),
  which talks about 216; today they are the 47 above), and so is one that
  goes over the nesting limit.
* **Without a song registry** —the `scan`— `PlayBGM`, `PlaySound`,
  `MemorizeBGM` and `PlayMemorizedBGM` are accepted empty; in the cartridge
  they are done.
* In routes: **transparency** (40 and 41) is dropped, and so is **sound**
  inside a jump or in a page's own route.

## Recommendation

1. **The two quarry `EraseEvent`s, first**: the common event's (small, only
   the compiler) and the real one on 150 (medium, state in the ROM). They are
   the only thing missing between the farm and the next day, and the quarry
   job is the first scene of that day that asks for something that does not
   exist.
2. **The small map ones, in a batch**: `ChangeGold` by variable, the cut for
   showing, "move away from hero", the direction in `ConditionalBranch` and
   the 999999 constant. With that the maps are left with **a single page
   out**, 207's, which needs the screen coordinates decided. None is urgent
   —they are not on the path—, but together they cost little and leave the
   compiler with no pending map work.
3. **Battle, as a separate job**, starting with `FlashScreen` in the scene
   —which also serves any other troop page— and asking taro for the decision
   on `ChangeMonsterCondition`: real conditions (large) or declared debt. It
   is what unblocks the most pages, 164, and they are two skills already
   used in `release`'s battles that do nothing today.

## How it was measured

With the tools at `6094a205` and a clone of ABL at `b28864d`. The request is
the one the converter sends to `rm2k-snes-events compile` when building
`release` —it was copied with a wrapper in the PATH that saves each request
and calls the binary—, and with `--every-map` all of the game's maps are
looked at:

    rm2k-snes-events culprits --data <ABL>/data --request compile.json \
        --out <dir> --every-map

It prints section 2's table per page type —without grouping variants— and
writes `culprits.json`, with each page that does not compile, its culprits
and their parameters, and each skipped call. Section 1's table comes from
its `commands`; section 2 groups `pages`' culprits by variant by hand.

It was checked against what was already known: without `--every-map` and
with `scan`'s request, **2,913** map pages of `release` compile, the same
ones `scan`'s `compiled` lists; and the troop pages that get in, **4,285**,
are the ones [`eventos-de-tropa-en-la-pelea`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/eventos-de-tropa-en-la-pelea.md) gave on 2026-09-30.

What the count does **not** look at: whether a page that compiles does what
it should —the test suite and taro take care of that—, nor what the
converter decides apart from the compiler —which maps get in, which pictures
each one carries—.
