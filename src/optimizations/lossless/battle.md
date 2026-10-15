# Lossless: battle

## The scene and the windows are one layer

In battle the scene and the windows share BG1 in mode 3, the windows in
the rows below the scene, so only BG1's horizontal scroll goes by HDMA and
no mode or base changes mid-frame.

- **Saves**: VRAM and HDMA channels.
- **Where**: `battle.rs` in `rm2k-snes/screens/`; `ba_win_tick` in
  `runtime/battle_scene.s`.
- **More**: [The VRAM split](../../internals/vram.md#battle-doesnt-use-the-layout).

## Each distinct troop page once

A game copies its battle systems' pages into every troop, so the troops'
pages are compiled and deduplicated by their bytecode: each distinct body
is stored once, and every troop that has it points to it.

- **Saves**: ROM in the troops' bytecode.
- **Where**: `rm2k-snes/events/src/troops.rs`.
- **More**: [What troop pages do not model](../../divergences/what-troop-pages-do-not-model.md).

## The battlers and the light backdrops in LZ2

The troop's battlers and the backdrops the ROM carries travel as LZ2 and
are decompressed when the battle starts.

- **Saves**: ROM.
- **Where**: `rm2k-snes/convert/src/scene.rs`; `runtime/battle_scene.s`.
- **More**: [The `.msu` file](../../internals/the-msu-file.md#what-does-not-fit-in-the-rom).

## Encounters and experience, precomputed

The encounter odds are integer arithmetic the converter prepares: the
reciprocal of each map's `encounter_steps`, in 1/65536, and the step at
which each row of the table is crossed; the ROM does not divide. And a
victory's experience comes summed per troop, since every enemy in a
victory is dead.

- **Saves**: CPU —no division on the console—.
- **Where**: `base` and `step_thresholds` in
  `rm2k-snes/battle/src/encounters.rs`, read by `runtime/encounters.s`;
  `troop_exp` in `rm2k-snes/battle/src/rules.rs`, read by `ba_exp_allocate`
  in `runtime/battle_loop.s`.
- **More**: the comments of those routines.

## The battlers in the grid's half of `$7E`

The troop's battlers are decompressed into the half of `$7E` the grid
uses, since `back_from_battle` decompresses the grid again anyway.

- **Saves**: far RAM.
- **Where**: `SCN_BATTLERS` in `runtime/battle_scene.s`.
- **More**: [The grid lives in WRAM](../the-grid-in-wram.md#what-is-lost).
