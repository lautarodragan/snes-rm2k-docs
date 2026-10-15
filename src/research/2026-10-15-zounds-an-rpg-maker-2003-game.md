# Zounds, an RPG Maker 2003 game

> **Measured on 2026-10-15** by Aguará, with the tools of the-advocate at
> `91d55d39`, the ports at `8a9ab73` and liblcf at `6854310`, over the
> game as cloned from `lautarodragan/zounds` at `5fa54e6`. It is a
> snapshot: the numbers are from that day and this file is not updated.
> The cartridge it mentions was built from a retouched copy of the game,
> to measure, and is not a build to play. How each number was obtained is
> at the end.

taro's question, on 2026-10-15, in the task
[`port-zounds-an-rpg-maker-2003-game`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/port-zounds-an-rpg-maker-2003-game.md):
Zounds is their own game, unfinished, made in **RPG Maker 2003**, and
every tool here reads RPG Maker 2000. How much of it works today, what
does 2003 add that the tools do not read, which commands are missing, and
—the question with the most weight— what is lost if its battles are
fought with the 2000 battle the engine already has, "as a middle ground or
as final": how easy degrading is, and the impacts that are not obvious.

The survey of the other games is
[Other games: the survey](2026-10-05-other-games.md); what the compiler
leaves out and how it is counted is
[What the compiler ignores silently](2026-10-14-what-the-compiler-ignores-silently.md).


## Summary

* **The 2003 part of Zounds is small, and the 2000 battle covers it.**
  Of 28,187 commands in 6,217 pages, the only RM2k3-only commands are
  two, both in troop pages: `ForceFlee` (36 uses) and `CallCommonEvent`
  (19). The 36 are the game's own Escape command, which never failed; the
  19 are the steal mechanic, a switch skill that calls a common event.
  Its side-view battlers are the RTP's generic sets, no actor or class
  has a command the 2000 battle lacks, no class learns a skill, and
  `ChangeClass`, `ChangeBattleCommands` and `ToggleAtbMode` are never
  used. **Degrading costs two compiler cases and loses an escape that
  always succeeded and the ATB's pacing.**
* **Ditto drops the 2003 flag bits, and that is the one trap.** Its
  generator skips liblcf's 118 `Is2k3` rows and the 15 2003 bits of the
  flag fields. The chunks come back raw and whole; the flags do not: a
  2003 troop page condition has 10 bits in 2 bytes and Ditto reads 7 in
  1. The round trip over Zounds is 188 of 190 files; and the resolved
  view says the 36 pages conditioned on "Escapar" have **no condition**,
  so a compiler that took them as written would end every battle at its
  first frame. Reading the 2003 fields is the generator's flag plus a
  version-aware width for two flag fields.
* **What stops the build today is not 2003's**: the images are XYZ (186
  files, RM2k3's zlib format, which nothing here decodes), the repository
  lacks 197 of the assets the data references (108 of them the RM2k3 RTP,
  which `~/assets` does not have; 55 are nowhere), a 215-colour gradient
  under the System's frame, a 200x200 map, and a debug troop with 32-bit
  numbers. With a retouched copy the converter builds an 8 MB cartridge
  with 54 of 127 data banks used, it boots, and the harness reaches map
  106 —the picture intro— where nothing moves.
* **The compiler's own gaps weigh more than 2003's.** 3,514 of 4,495 map
  pages with code compile (78%); 920 of the 981 that do not are kept out
  by their **messages alone**, 678 of them only by the colour escape
  `\c[n]`, which Zounds writes in 2,604 of its 7,102 lines. After that:
  `TileSubstitution`, `ShowChoice` inside those boxes, a vehicle, 32-bit
  money. Of 69 common events 41 compile; of 105 troop pages 18 —64 carry
  the trigger Ditto misreads—.
* **What is Zounds-specific and large**: screens made of pictures (its
  menu, its skill screen, a race's score board and the intro) where the
  console keeps two pictures; four maps with up to 327 events, grids of
  identical info or coin events; three `.wav` songs —the title, the
  battle and the victory themes— that want the MSU-1 (42.8 MB of PCM);
  and the missing custom assets, which only taro may have.
* **Recommendation**: engine first —XYZ, Ditto's 2003 fields with the
  flag fix, the colour escape in messages—, then the 2000 battle with
  two compiler cases, and the 2003 battle not at all for this game. The
  real cost of Zounds is its picture screens and its data hygiene, and
  neither is 2003's.


## The game, in numbers

188 maps (the tree has 194 nodes: 188 maps, 5 areas and the root; the
largest is 200x200, the next 100x50), 10 actors (5 named: Unamë, Kazar,
Bandurion, Pointer, Buddy Bird), 50 skills (32 named), 100 items, 50
enemies (17 used), 50 troops (27 empty, 17 of one enemy, 5 of two, 1 of
three), 15 states, 20 terrains, 202 battle animations, 200 chipsets (101
referenced), 400 switches, 200 variables, 69 common events. 6,043 map
pages, 105 troop pages, 28,187 commands.

The folders: 213 MB, of which `Music/` is 211 (34 MIDIs, 699 KB; 19
`.wav`, 210.7 MB, 39.8 minutes at 22,050 Hz stereo 16-bit). 186 images
are `.xyz`; `Battle/` (98 PNG) and `BattleCharSet/` (64 PNG) are the
RM2k3 RTP's own files copied in. There is no `rm2k-snes.toml` or
`justfile`: the study used a throwaway project with Book of Three's,
renamed, in scratch.

The starting party in the System is **empty**; the intro adds the heroes
by events (`ChangePartyMembers`, 62 uses). The three `.wav` the game
plays are the System's title, battle and battle-end music; no map sets
its music from the tree, every song is a `PlayBGM`.


## 1. Reading: what Ditto does with 2003 today

Ditto's generator (`cargo xtask generate`, `rm2k/ditto/xtask/src/main.rs`)
reads liblcf's `fields.csv` and **skips every row with `Is2k3` set**
—"Ditto targets RPG Maker 2000"—, and in `flags.csv` skips the 2003 bits
the same way. Measured over liblcf `6854310`: **118 of 1,043 field rows**
are 2003-only, and 15 flag bits. The structs whose rows are *not* flagged
already exist in the generated schema —`Class`, `BattleCommand`,
`BattleCommands`—; what is not generated is:

* the six `Database` chunks that hold the 2003 sections: `battlecommands`
  (0x1d), `classes` (0x1e), `battleranimations` (0x20) and three empty
  blocks (0x1b, 0x1c, 0x1f);
* the four `BattlerAnimation*` structs, every row of which is flagged;
* per-record fields: `Actor` 5 (`class_id`, `battle_x`, `battle_y`,
  `battler_animation`, `battle_commands`), `Item` 6, `Skill` 5, `State`
  5, `System` 9 (`system2_name`, `menu_commands`, `invert_animations`,
  the frame…), `Terms` 7, `Terrain` 23 (the side-view grid),
  `TroopPageCondition` 8 (`turn_enemy_*`, `turn_actor_*`,
  `command_actor_id`, `command_id`), `EventPageCondition` 2 (`timer2`,
  `compare_operator`), `Troop` 2, `Map` 1, and the save-file ones.

**What lands in `unknown`** in Zounds' exact dump, every one a 2003 field:
the six `Database` chunks (`battlecommands` 161 bytes, `classes` 12,359,
`battleranimations` 19,098); `Actor.class_id` in 3 actors,
`battler_animation` in 3, `battle_commands` in all 10, `battle_x/y` in 1;
`Item.animation_data` in all 100 and `weapon_animation` in 6;
`Skill.battler_animation_data` in all 50, `battler_animation` in 5,
`sp_percent` in 1; `State.affect_type` in 11, `cursed` in 2,
`battler_animation_id` in 3; `System.system2_name`, `menu_commands`,
`invert_animations`; five `Terms`; `Terrain.footstep` in all 20 (three
with a sound), `grid_*` in 13, `on_damage_se` in 2;
`TroopPageCondition.command_id` in 58 pages and `command_actor_id` in 18.
Nothing else is unknown: the maps are clean. The resolved view, which the
converter reads, simply does not have those fields.

**The round trip is not exact on a 2003 game**: `just dump-round-trip`
gives 188 of 190 files equal; `RPG_RT.ldb` comes back **107 bytes short**
—105 of them in the troops chunk: all 105 troop pages have a 2-byte flag
chunk, and Ditto writes 1— and `Map0187.lmu` one byte off, the `timer2`
bit of event 2 "Time Over" (the fishing game's timer). It is the only
place where the 2000 reader does not just leave a 2003 thing aside: it
**misreads it**. Read from the binary, 36 troop pages are conditioned on
a battle command and 18 on a turn; the resolved view shows those 36 with
every flag false. The two consequences are in section 3.

**How much work**: dropping the generator's `continue` writes the lot
—structs, defaults, codec, description— from the same tables, and a 2000
game's dump does not change, because the new fields hold their defaults
and are left out. The one real piece is the **width of the two flag
fields**: a 2003 file packs its bits into the same chunk, so the codec
has to know the file is 2003's (`System.ldb_id`, which liblcf also uses)
to read and write `TroopPageCondition.flags` as 2 bytes. The consumers in
`rm2k-snes/` read the resolved view by field name and would not notice
new ones. Drafts:
[`ditto-does-not-read-the-2003-fields`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ditto-does-not-read-the-2003-fields.md),
[`ditto-drops-the-2003-flag-bits`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ditto-drops-the-2003-flag-bits.md).


## 2. Events: what the compiler does not compile

A census of every command, against the compiler's `codes.rs` and liblcf's
code table; then the converter's own `culprits` report over the built
cartridge, which chases every page that does not compile.

**2003-only commands** (liblcf's 1005–1009 and 5001–5005): Zounds uses
**two**, both in troop pages and nowhere else:

| code | command | uses | where |
|---:|---|---:|---|
| 1006 | `ForceFlee` | 36 | 36 troop pages, parameters `[0, 0, 1]`: the party flees, unconditionally |
| 1005 | `CallCommonEvent` | 19 | 19 troop pages: 18 call common event 2 "Robar - Battle Acion", 1 calls 65 |

`ChangeClass`, `ChangeBattleCommands`, `EnableCombo`, `OpenLoadMenu`,
`ExitGame`, `ToggleAtbMode`, `ToggleFullscreen`, `OpenVideoOptions`: 0.
The 2003 variants of `ControlVars` and `ConditionalBranch` operands: none
—every `ConditionalBranch` type is 2000's (switch 186, variable 787,
timer 1, gold 12, item 77, actor 33, event facing 198, started by the
action key 7), every `ControlVars` operand too (constant 1,529, variable
121, random 93, actor 16, event 117, other 8)—. `KeyInputProc` appears 7
times with 14 parameters, which is 2003's layout of the command; the
compiler lists all 7 as culprits. One event page is conditioned on 2003's
second timer (map 187).

**RM2k commands the compiler lacks** that Zounds uses: `ChangeParameters`
(6 uses, all in the debug common event), `EnterExitVehicle` (2 map
pages), `TeleportTargets` (1), `OpenMainMenu` (1, debug). That is the
whole list of codes unknown to `codes.rs`.

**Pages left out, by cause** (`culprits.json`, maps 4,495 pages with code,
commons 69, troops 105):

| section | compile | kept out by one command alone | with others |
|---|---:|---|---|
| maps | 3,514 (78%) | messages 907 (`ShowMessage`+`_2`: 900; `\c` only: 678), `TileSubstitution` 8, `MoveEvent` 2, `InputNumber` 1, `OpenShop` 1 | `ShowChoice` with those messages 43, `ConditionalBranch` 7, `Loop` 3, `PanScreen` 2, `EnterExitVehicle` 2, `ChangeSkills`+`ControlVars`+`TeleportTargets` 1 |
| commons | 41 | messages 13, `ControlVars` 3 (32-bit money: 500,000–999,999), `Loop` 3, `ConditionalBranch` 2, `KeyInputProc` 1 | `ShowChoice` 4, `ChangeParameters` 1, `OpenMainMenu` 1 |
| troops | 18 | `ForceFlee` 36, `CallCommonEvent` 19 | `ShowMessage`+`ChangeSP` 4 |

Plus 64 troop pages with a trigger the ROM cannot look at —the misread
flags—, one map page that stops as a whole (map 169, a block left open),
317 skipped calls, and 6 of the 17 parallel common events that do not
compile.

**The messages are the finding.** The compiler accepts `\|` and `\^` only
as a tail at the end of a box and refuses any other escape, on purpose
—ABL's 40 boxes with escapes are all tails—. Zounds opens most boxes with
`\c[5]Unamë:\c[0]`: `\c` 5,220 times in 2,604 of 7,102 lines; `\|` 669
(220 pages have it mid-line), `\v[k]` 97, `\n[k]` 41, `\s[k]` 24. Ignoring
`\c[n]` —drawing in the System's text colour— lets 678 map pages in at
once. Draft:
[`the-colour-escape-in-messages`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-colour-escape-in-messages.md).
The `ConditionalBranch` type 8 —"started by the action key", 7 uses— is
RM2k's and not compiled either; the 32-bit money is a limit of the
variables, 16-bit in the ROM.


## 3. Battles: the 2000 battle instead of 2003's

What Zounds configured in the 2003 database, read from the raw chunks:

* **Battle layout** (`battlecommands`): type `gauge` (the ATB bar
  visible), placement automatic, small command window, death handler off
  (its teleport fields point at map 160 but the flag is off).
* **Commands**: 11 slots, 9 named: Atacar (attack), Técnica (skill),
  Defender (defense), Objeto (item), Escapar (escape), Robar (subskill),
  Juglarismo (subskill), Tirar-Usar (item), Escapar (special). Per
  actor: Unamë [Atacar, Técnica, Objeto, Defender, Escapar-special, Row],
  Kazar [Atacar, Técnica, Tirar-Usar, Defender, Escapar-special, Row],
  Bandurion [Atacar, Técnica, Objeto, Defender, Row]; Pointer and Buddy
  Bird [Row]. **No actor and no class has Robar or Juglarismo**, and no
  skill is of a subskill type (skills: 27 normal, 4 switch, 1 teleport).
* **Classes**: 10, three named (Ladrón, Científico, Tester) with curves
  of their own; Unamë and Kazar are Ladrón, Bandurion is Científico. No
  class learns a skill. RPG_RT applies a class's curves **only after a
  `ChangeClass`** (EasyRPG's `Game_Actor::GetBaseMaxHp`, with the
  comment), and Zounds never runs one: the actors fight with their own
  curves (HP 48 → 476 over 50 levels for Unamë; attack, defense, spirit
  and agility 10 → 89, identical for the three).
* **Side view**: 33 battler animation sets, the 32 of the RTP plus one
  empty; the actors use Female Thief, Male Thief and Male Mage. Weapon
  animations on 6 items, skill animations on 5 skills, state poses on 3
  states, `invert_animations` on, `battle_x/y` on Unamë, the terrain
  grid on 13 terrains. `System2` is `system2c`, the RTP's, not in the
  repo.
* **Troop pages**: of 105, 36 are conditioned on actor 1 or 4 using
  "Escapar" (the `special` command) and do a `ForceFlee`; 23 on a switch
  —22 on switch 3 "Robar"— and call the steal common event; 18 on a turn.
  No `turn_enemy` or `turn_actor`.
* **Numbers that touch the formulas**: actors with critical hits (1 in
  30), enemies without; one two-handed weapon; no dual wield, no
  attack-all or pre-emptive weapons; `State.affect_type` on 11 states
  (10 "nothing", 1 "double"), `cursed` on 2; one skill costs 25% of MP
  (`sp_percent`), a 2003 field. Enemy agility 10–23 (the debug one 75),
  the party's 10 at level 1 for everyone.

**What the 2000 battle does with each, and what it needs from the data:**

| 2003 thing | Zounds uses it | in the 2000 battle | needs from the 2003 data |
|---|---|---|---|
| ATB (`gauge`), `ToggleAtbMode`, the menu's Wait | yes (layout only) | turns ordered by agility; the Wait entry and its terms vanish | nothing |
| side-view battlers, weapon/skill/state poses, grid, System2 | yes, RTP sets | front view: 16 monster images (XYZ) and the status window; nothing custom is lost | nothing |
| commands per actor | 2000's set, renamed, plus Escapar | Attack/Skill/Defend/Item per actor, Escape for the party | which actors have an Item/Skill command: all three |
| "Escapar" command events → `ForceFlee` | 36 pages | the built-in Escape, **with RM2k's chance of failing**; the pages never trigger | the condition flags, read right, so the pages are not taken as unconditioned |
| `CallCommonEvent` in a troop page | 19 pages: the steal | a call to the common body; the compiler already does it on maps | `TROOP_COMMANDS` to admit the call |
| classes | assigned, never changed | nothing changes | nothing |
| `sp_percent` | 1 skill | a fixed cost | the field |
| `command_actor`/`turn_enemy`/`turn_actor` conditions | 36 / 0 / 0 | covered above | the flags |
| death handler, row, `affect_type`, `cursed` | off / front / set | nothing / nothing / 2000's state fields stand | nothing |

**The two non-obvious impacts**, both from the flag bits Ditto drops:

1. The 36 "Escapar" pages read as pages **with no condition**. In RM2k a
   troop page with no condition runs at the start of the battle, and
   these pages flee. Today `ForceFlee` does not compile and the pages
   are out; the day it compiles —or the pages are taken as plain
   escapes— without the flags fix, every battle ends on its first frame.
2. Map 187's "Time Over" page (the fishing game) reads as conditioned on
   its switch alone, not on the second timer: it fires as soon as the
   switch is on.

What is lost for real: Zounds' escape **never failed** (`ForceFlee` with
its check off); RM2k's Escape has a chance to fail, and the game's
balance assumed otherwise. And the ATB's pacing: a 23-agility fish acted
about twice per 10-agility hero; in turns everyone acts once a round.
Neither touches the story, the switches or the variables.

**Outside battle**, the 2003 battle data reaches: the menu —`menu_commands`
is Item, Skill, Equipment, Status, **Wait**, Save, in that order, and
Wait toggles the ATB—; the five terms `Estado`, `Posicion`, `Orden`,
`Esperar`, `Activo`; the status screen's class name. Nothing in the
events reads a class or a command. Draft:
[`the-2003-battle-commands-callcommonevent-and-forceflee`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-2003-battle-commands-callcommonevent-and-forceflee.md).


## 4. Outside battle: what 2003 changes and what Zounds does

* **Images are XYZ.** RM2k3 writes every imported image as `.xyz`
  —`"XYZ1"`, width, height, a zlib stream of a 256-colour palette and
  the indices—. The finders accept the extension; nothing decodes it, so
  the build stops at the System. 186 files: 75 charsets, 20 chipsets, 50
  pictures, 16 monsters, 11 panoramas, 5 backdrops, the System, the
  Title, a faceset, 3 battle animations. The study converted them to PNG
  in a copy. Draft:
  [`the-tools-do-not-read-xyz-images`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-tools-do-not-read-xyz-images.md).
* **The RM2k3 RTP is not in `~/assets`**, and the game leans on it: 108
  of the 197 missing assets are its —`system2c`, the backdrops `barren`,
  `beach`, `ocean`, `plains`, charsets `char1`…`hero3`, facesets, the
  monster `bahamut`, 75 sounds the RTP battle animations play, 3 songs—.
  43 more are the RM2k RTP under other languages' file names (13
  chipsets like `chipset6` and `ff6_town`, which is how the RPG Advocate
  RTP was named), and **55 are nowhere**: custom chipsets ("Zoundz's
  Castle", "Cueva de lava"), charsets, 13 songs, 37 sounds, never
  committed. It costs a download of Enterbrain's RTP 2003 and a second
  RTP directory per game in `machine.just`. Draft:
  [`zounds-the-repository-lacks-197-assets`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-the-repository-lacks-197-assets.md).
* **Messages and faces**: every `ShowMessage` and `MessageOptions` is
  2000's; `ChangeFaceGraphic` 3,091 times. What 2003 adds here is only
  the colour escapes above, which are 2000's too.
* **Pictures**: 266 `ShowPicture`, all with RM2k's 16 parameters —no
  RM2k3 1.12 spritesheets or flags—; 56 files, numbers up to 50. Three
  maps keep more than the console's two: 75 "Super Race" (a score's
  digits), 136 "Menu" and 190 "Skill Screen" —**Zounds closes RM2k's menu
  (`ChangeMainMenuAccess`, 30 uses) and draws its own out of pictures**—,
  and the intro on map 106 "Imágenes" is pictures too. Draft:
  [`zounds-pictures-and-the-picture-made-screens`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-pictures-and-the-picture-made-screens.md);
  the roads are [The custom menu](2026-10-04-the-custom-menu.md) and
  [The picture system](2026-10-01-the-picture-system.md).
* **The `.wav` music**: 3 of the 19 are played, and they are the System's
  title (153.1 s), battle (64.5 s) and victory (24.8 s) themes. As MSU-1
  PCM at 44.1 kHz stereo, 176,400 B/s: **42.8 MB** for the three; the
  whole folder would be 421 MB. The MSU-1 path exists for ABL's
  replacement tracks —[The MSU file](../internals/the-msu-file.md)—; what
  is new is taking the game's own `.wav` as a song. Without MSU-1 the
  three slots fall silent or get a MIDI by a knob. Draft:
  [`zounds-wav-music-through-msu-1`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-wav-music-through-msu-1.md).
* **Maps**: 2003 changes nothing in the map format Zounds uses; what
  bites is the game's own habits: four maps over the console's 120
  events —47 with 284, 51 with 214, 57 with 131, 178 "Kuak-Man" with 327,
  grids of identical info, rock and coin events that the twin folding
  does not catch because each sets its own switch or draws a sprite;
  they lose 155, 88, 8 and 206 pages that run—; map 30, 200x200, whose
  cell stream (47,232 bytes) does not fit the 32,768 WRAM holds, and
  stops the build instead of being left out. Drafts:
  [`zounds-maps-over-120-events`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-maps-over-120-events.md),
  [`a-200x200-map-does-not-fit-the-cell-stream`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-200x200-map-does-not-fit-the-cell-stream.md).
* **Vehicles**: a boat starts on map 187 "Fishing Game", boarded with
  `EnterExitVehicle` on two pages; the engine has no vehicles. Draft:
  [`vehicles-enterexitvehicle-and-the-boat`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/vehicles-enterexitvehicle-and-the-boat.md).
* **Terrains**: 2003's footstep sounds on 3 terrains and damage sounds on
  2 are dropped with the fields; the rest of the terrain is 2000's.


## What the converter did with it

Run on a copy of the game in scratch, retouched only to get past each
stop: XYZ as PNG; a donor file under each of the 197 missing names;
`[windows.background]` for the System; Zounds' own backdrop as the
fallback and a placeholder for `ABLBackdropSJ02`, which an encounter asks
for; map 30 excluded; the debug troop's 99,999 HP, 9,999,999 experience
and 999,999 gold capped. The stops, in order, each one a draft:

1. `rm2k-snes-screens: System "Zounds_System" is not in …` — XYZ.
2. `wally: can't find CharSet "Posses"` — the missing assets.
3. `the actor choice's windows are 65 8bpp tiles … tilemap is at $4800`
   — the gradient under the System's frame, which no fusing covers and
   the message does not name: swapping the skin and shortening the terms
   drawn there changed nothing; the flat fill did. Draft:
   [`a-gradient-system-stops-the-converter-at-the-actor-choice`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-gradient-system-stops-the-converter-at-the-actor-choice.md).
4. `backdrop 'ABLBackdropSJ02' is neither in the game nor in the RTP` and
   the Book of Three fallback — the toml.
5. `map 30: a stream of map_cells is 47232 bytes and 32768 fit in WRAM`.
6. `troop 1 gives 9999999 experience and the ROM adds it in sixteen bits`,
   then `mapdata.inc:287259: Error: Range error (99999 not in
   [0..65535])` — the same limit, one refused with a message and one
   not. Draft:
   [`an-enemy-with-32-bit-numbers-breaks-the-assembler`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/an-enemy-with-32-bit-numbers-breaks-the-assembler.md).

Then it built: `zounds.sfc`, 8,388,608 bytes, 4,094 pieces in 54 of 127
data banks, 54 whole banks free (8 fast), bank 0 with 1,053 bytes free,
texts 1,834 of 262,144. Thirty-five warnings: pictures that do not fit a
map's VRAM or palettes (9), picture pages the ROM does not run (6), the
four maps over 120 events, two maps that send more walkers than there
are route slots, names cut in the battle (two actors, one skill, five
items) and in the slot screen, the title window's colours merged. Every
audio package fits —the fullest, package 2, 49,383 bytes of samples with
10,845 left—.

The ports' boot harness, in snes9x and bsnes alike: the title passes,
and at tick 397 the player has control on **map 106 "Imágenes"**, hero at
(176, 144), the intro's music playing, and the hero moves to no side: it
is the picture intro, and the ROM does not run its pages. Captures in
`/shared/captures/2026-10-15-zounds/`.


## 5. The plan

**Phase 0 — read the game as it is** (engine; every 2003 game needs it):
an XYZ decoder next to the PNG one; Ditto's 2003 fields, with the
version-aware width of the two flag fields; the RM2k3 RTP in `~/assets`
and a second RTP directory in `machine.just`. Unlocks a faithful dump, a
build without hand placeholders, and removes the one trap. Small: the
decoder is a page of code, the generator is a flag plus the flags'
width.

**Phase 1 — the compiler's gaps Zounds hits hardest** (engine, useful
to any game): the colour escape `\c[n]` ignored (678 map pages) and then
honoured; `\|` mid-line, `\n[k]`, `\v[k]`; the "started by the action key"
branch (7 pages); `TileSubstitution` (8). Medium: the escapes touch the
composer in `runtime/`.

**Phase 2 — the 2000 battle for a 2003 game** (engine, two cases):
`CallCommonEvent` compiled as the call it is, with `TROOP_COMMANDS`
admitting it; `ForceFlee` pages recognised as the Escape command's and
dropped, with the built-in Escape standing in; `sp_percent` as a fixed
cost; the menu's Wait entry dropped. Small, once Phase 0 reads the
flags. The 2003 battle itself —ATB, side view, per-actor command
windows— is not recommended for Zounds: its battlers are the RTP's, its
commands are 2000's plus an escape, and no event reads a class or a
command.

**Phase 3 — Zounds' own** (per game, and taro's game is editable): the 55
assets only taro may have; the picture screens —the menu, the skill
screen, the race, the intro— by the custom-menu road or by a picture
system past two; the four event grids and map 30, which are best
re-authored in the game (one event with `ControlVars` by position, a map
split in two); the three `.wav` through the MSU-1; the debug troop
patched out. Large, and none of it is 2003's.

**Engine against Zounds-specific**: XYZ, the 2003 fields, the flags, the
colour escape, the branch by action key, the two battle cases, vehicles
and the 32-bit refusal with a name are engine work, and the next 2003
game gets them for free; the RTP is an asset; everything in Phase 3 is
this game's.


## How the numbers were obtained

The scripts are in `~/scratch/aguara/zounds/`, each one with what it
counts at the top; the throwaway project in `project/`, the PNG copy in
`game-png/`, the boot run through a symlink into a ports worktree.

* `unknowns.py`: the `unknown` chunks of the exact dump by struct, named
  with liblcf's `fields.csv`. `decode2k3.py`: those chunks decoded
  —`battlecommands`, `classes`, `battleranimations`, the per-record
  fields— with the LCF grammar (BER ids and lengths, raw little-endian
  `Vector<Int32>`). `lcf_flags.py`: the flag bits read from the binaries,
  troop and event page conditions.
* `census.py`: every command in every page against `codes.rs` and
  liblcf's code table, with the operand variants of `ControlVars` and
  `ConditionalBranch`. `battle_events.py`, `stats.py`: the troop pages'
  2003 commands, the switch skills, the actors' and enemies' numbers, the
  pictures' parameters. `summarize_culprits.py`: the reading of
  `culprits.json` above.
* `facts.py`, `assets.py`, `rtp_classify.py`: the folders and the music
  (`wave`), every referenced asset against the game and `rtp.zip`, and
  the missing ones against EasyRPG's `rtp_table.cpp`. `xyz2png.py`,
  `placeholders.py`: the measuring copy.
* The build: `just cartridges release` and `just space` in the project,
  with the global tools at `91d55d39`; `just culprits release`; the boot
  through `just boot -k zounds` and `capture_zounds.py` in the ports
  worktree's `tests/`, with Zounds added to `FIRST_MAP` there.
* liblcf's semantics from `generator/csv/`; RPG_RT's from EasyRPG's
  `game_interpreter_battle.cpp`, `game_actor.cpp`, `scene_menu.cpp`.
