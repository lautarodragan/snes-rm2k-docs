# Lossy: tables of a fixed size

## Graphics a move route switches to

A map holds a fixed number of the graphics move route command 34 switches
to; the rest are ignored.

- **Loses**: those changes of graphic.
- **Where**: `ROUTE_GFX_MAX` in `rm2k-snes/events/src/registry.rs` and, the
  same number, in `rm2k-snes/mapdata/src/record.rs`.
- **More**: [Move route command 34 on the hero](../../decisions/move-route-command-34-on-the-hero.md).

## Variables

The console keeps a fixed number of variables, each with a one-byte slot.
Event pages that need one that didn't get a slot are left out, and the
build lists them.

- **Loses**: those pages.
- **Where**: `variable_slot` in `rm2k-snes/events/src/compile.rs`.
- **More**: [Variables saturate at sixteen bits](../../divergences/variables-saturate-at-16-bits.md).

## A troop of more than eight enemies

A battle holds eight enemies: each takes a fixed place in the battle's far
RAM, and the hidden and scene masks are a byte per troop. A troop with
more is fitted to eight, leaving out first the members no page shows, then
those every page that shows them also kills; never one a page condition
or a branch asks about.

- **Loses**: those members, in the scenes the troop's pages play.
- **Where**: `fit.rs` of `rm2k-snes/battle/`.
- **More**: [A battle holds eight enemies](../../divergences/a-battle-holds-eight-enemies.md).
