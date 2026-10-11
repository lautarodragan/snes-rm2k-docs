# What the battle menu does not model

## What

Since 2026-10-04 the battle is RM2k's: the scene on top with nothing written
over it, and the System's windows —with their frame and their bar— in the
strip below, the party on the left and the commands on the right, the way
they end up in RM2k after sliding. See `ba_compose` in
`runtime/battle_skills.s` in the-advocate, `screen.rs` in
`rm2k-snes-battle` and `battle.rs` in `rm2k-snes-screens`. What is not the
same yet:

* **There is no sliding**: RM2k opens each turn with the party menu
  —Engage, Automatic, Escape— on the left, and on choosing Engage the
  windows move 76 pixels. Here there is no party menu (see
  [Escape is the fifth command](escape-es-la-quinta-orden.md)) and the
  windows are always where RM2k leaves them. It was optional and was not
  done.
* **The enemy list covers the whole party window**, and not only the names:
  the party line, in 256 pixels, leaves the HP in the middle of the window,
  and a half-window list has no room for the enemies' names.
* **The commands window starts at 178 and not at 76% of the screen**, which
  is what leaves "AgentTrain" its 59 pixels; the party one, for the same
  reason, goes to the edge: the SP ends two pixels from the frame. The
  converter warns if it does not fit with another font
  (`check_party_line`).
* **The bar uses the first of the System's two cursor drawings**, like the
  rest of the screens: see
  [The choice bar does not alternate its two drawings](la-barra-de-la-eleccion-no-alterna-sus-dos-dibujos.md).
* **The status** is always `normal_status`, or the name of the dead status
  for a fallen one: the battle has no other statuses.
* **The HP and SP** go in the text color, rather than the terms in the
  System color.
* **The description of a skill or an item** goes in the same font as the
  rest, on a line cut at the frame: RM2k writes it whole with a smaller one.
* **Item and skill names have eleven cells** in each column; the converter
  says which ones get cut.

## Measured

With the 2015 RPG_RT under Wine, on 2026-10-04 —the battle test, troops 82
and 87—, against the ROM with ABL's test run. The side-by-side captures,
with the ROM, are listed in the task [`el-menu-de-la-pelea-como-rm2k`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/el-menu-de-la-pelea-como-rm2k.md), in
`tasks/` in the-advocate-work.

## When it stops being enough

The party row is measured for *A Blurred Line*'s font: the HP and the SP are
runs the console does not cut, and with a wider font they overlap. The
converter warns about it —"the party's line does not fit"—. And a troop
with eight different battlers does not fit: the last palette belongs to the
windows, and the converter refuses.
