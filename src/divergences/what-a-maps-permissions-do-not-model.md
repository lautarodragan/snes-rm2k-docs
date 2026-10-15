# What a map's permissions do not model

## What

Each node of the map tree says whether its map allows saving, the Escape
skill and the Teleport skill, or that it takes its parent's. RM2k resolves
the parents each time a map is set up and writes the result over the same
permissions `ChangeSaveAccess`, `ChangeEscapeAccess` and
`ChangeTeleportAccess` set (easyrpg's `Game_Map::Setup`): a page's
`ChangeSaveAccess` lasts until the next map, and a map that allows saving
gives back what a page had forbidden. It is done on a change of map and on
a new game, not on a jump to the same map nor on loading a save, which
carries its own.

The port does the same: the converter climbs the tree, the cartridge carries
one byte per map with what it forbids, and the ROM writes it over its
permissions on those same occasions (`map_access_enter`, in
`runtime/enter_map.s` in the-advocate). What stays different:

* **The escape and teleport ones are stored and nothing reads them.** In
  RM2k they decide only whether the Escape and Teleport skills can be used
  from the menu, and the skills screen keeps both always grey (see
  [The skills screen](the-skills-screen.md)).
* **`ChangeTeleportAccess` does not compile**: only a map sets the
  teleport permission today.

The battle's Escape command is not one of these, in RM2k either: it
depends only on the battle —`EnemyEncounter`'s escape option, and always
allowed in a random encounter—. A map that forbids escaping, like ABL's
map 105, leaves the battle's Escape as it was.

## How it looks today

On A Blurred Line the map's save is not seen, and that is RM2k's behaviour,
not the port's: its parallel common events 2 (`DisableSaving`, with switch
236 off) and 8 (`EnableSaving`, with it on) write the save permission
whenever they run, and they run every frame in RM2k, so the 75 maps under
The Kingdom of Surl that forbid saving are overwritten one frame later. In
the port they are [pure](pure-parallel-common-events-run-only-when-what-they-read-changes.md)
and run only when owed, so entering a map owes them a run for this.

Where it does show is in the games without such common events: Dooms 2
forbids saving on 88 of its 92 maps, and Vampires Dawn on all of them.
