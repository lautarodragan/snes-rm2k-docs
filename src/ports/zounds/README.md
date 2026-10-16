# Zounds

taro's own game, unfinished, made in **RPG Maker 2003**: the first 2003
game here, and the one the tools learned 2003 from. The study that
preceded the port is
[Zounds, an RPG Maker 2003 game](../../research/2026-10-15-zounds-an-rpg-maker-2003-game.md);
the port's project is `zounds/` in the-advocate-ports, built on 2026-10-15,
**without MSU-1**.

## What is 2003 about it, and what the port does with it

* **Ditto reads it whole.** The 2003 fields —classes, battle commands,
  battler animations, the second timer, the turn and command conditions of
  a troop page— and the 2003 bits of the flag fields, which until that day
  came back short: see point 5 of Ditto's README in the-advocate, and the
  tasks
  [`ditto-does-not-read-the-2003-fields`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ditto-does-not-read-the-2003-fields.md)
  and
  [`ditto-drops-the-2003-flag-bits`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/ditto-drops-the-2003-flag-bits.md).
* **Its battles are fought with the 2000 battle**: turns ordered by
  agility instead of the ATB, the front view instead of its RTP side-view
  battlers, Attack, Skill, Defend, Item and Escape for everyone. The two
  2003 commands its troop pages carry are compiled for it:
  `CallCommonEvent`, the steal mechanic, as the called body pasted into the
  page; and `ForceFlee`, the game's own Escape command, as an escape that
  cannot fail. The 36 pages that carry the second are conditioned on that
  command being chosen, which the 2000 battle has no event for, so they
  never run here and the built-in Escape stands in —with RPG Maker 2000's
  chance of failing, which the game's own never had—. Task:
  [`the-2003-battle-commands-callcommonevent-and-forceflee`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-2003-battle-commands-callcommonevent-and-forceflee.md).
* **Its images were XYZ**, RPG Maker 2003's own format, which the tools do
  not read on purpose: the port builds from a branch of the game's
  repository where they are PNG, converted once with EasyRPG's `xyz2png`.
  Task:
  [`the-tools-do-not-read-xyz-images`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-tools-do-not-read-xyz-images.md).

## What the game lacks, and the port fakes

The repository references 197 assets it never had —the RPG Maker 2003
RTP, the 2000 RTP under other RTPs' names, and 55 that are nowhere—. On
the port's branch each name has a stand-in: six songs that are A Blurred
Line's, with the same name, are the real ones; seven more were found again
by name in a public MIDI archive, for a private build only; twenty are the 2000 RTP's
own files, found through EasyRPG's RTP table; the other 171 are a copy of
some file of the game from the same folder, so a missing chipset is some
chipset and a missing sound some sound. The debug enemy's numbers were
brought within sixteen bits. Task:
[`zounds-the-repository-lacks-197-assets`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-the-repository-lacks-197-assets.md).

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change.

* **The intro does not play, and the hero does not move on map 106**: the
  intro is made of pictures, and the ROM does not run its pages. Draft:
  [`zounds-pictures-and-the-picture-made-screens`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-pictures-and-the-picture-made-screens.md).
* **Most dialogue is missing**: the boxes with accented letters and the
  hero's own name, `Unamë`, do not compile, because the font lacks those
  letters, and the pages that show them are left out. Draft:
  [`latin-1-letters-stop-a-box`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/latin-1-letters-stop-a-box.md).
* **The stand-in assets**: wrong chipsets on the maps that asked for the
  RTP's or the lost ones, one sound for 113 missing sounds, one song for
  the three songs still missing (`waltz`, `boat1`, `boat2`). See above.
* **Map 30 is left out**: 200x200, its cells do not fit WRAM. Draft:
  [`a-200x200-map-does-not-fit-the-cell-stream`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/a-200x200-map-does-not-fit-the-cell-stream.md).
* **Four maps lose their events past the 120th**: the grids of info, rock
  and coin events on maps 47, 51, 57 and 178. Draft:
  [`zounds-maps-over-120-events`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-maps-over-120-events.md).
* **The five `.wav` songs are silent**: the title, battle and victory
  themes, the mountains' (map 33) and the small caves' (maps 89, 91, 92
  and 177), which the map tree sets; they want the MSU-1. Draft:
  [`zounds-wav-music-through-msu-1`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-wav-music-through-msu-1.md).
* **No boat**: the fishing game's vehicle. Draft:
  [`vehicles-enterexitvehicle-and-the-boat`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/vehicles-enterexitvehicle-and-the-boat.md).
