# Lossless: events

## A common event's shared body, called with `OP_CALL`

A common event called from the foreground has one body in the cartridge,
called with `OP_CALL` instead of pasted in place, when the body compiled
with the map is byte for byte the one without it.

- **Saves**: ROM and WRAM —a deep chain of calls pasted in place does not
  fit at all—.
- **Where**: `OP_CALL` in `rm2k-snes/bytecode/src/events.rs` and its
  `op_call` in the interpreter; `refresh` in `compile.rs` of
  `rm2k-snes/events/`.
- **More**: [CallEvent: a shared body, or pasted in place](events/common-event-calls.md).

## `CallEvent` pasted in place, with no interpreter stack

What does not go to a shared body —parallel pages, bodies that depend on
the map, calls to map events— is pasted in place: the callee runs whole
before the caller continues, so no stack of interpreters is needed.

- **Saves**: RAM —no interpreter per call— and the cost of a call in
  parallel pages.
- **Where**: the event compiler, `rm2k-snes/events/`.
- **More**: [CallEvent: a shared body, or pasted in place](events/common-event-calls.md#pasted-in-place).

## Identical pages are stored once

Two pages of a map whose compiled bytecode is the same point at the same
code in the map's block, and so do two identical own routes: the page
table already carries a 24-bit pointer per page. A battle screen made of
one page per monster, all with the same commands, is the case it was made
for.

- **Saves**: WRAM, where the map's bytecode is decompressed; ROM only a
  little, because LZ2 already finds most of the repetition. How much, per
  map: the `map_code` table of the cartridge's `mapdata.inc`.
- **Only within a map**: each map's block is its own stream, decompressed
  alone.
- **Where**: `lay_out_code` in `convert.rs` of `rm2k-snes/convert/`.
- **More**: [Events](../../internals/events.md); measured in
  [Frozen World's battle system](../../research/2026-10-15-frozen-worlds-battle-system.md).

## The pure parallel common events run only when what they read changes

A parallel common event that only reads switches and equipment, and only
writes skills and the three permissions, runs when its switch turns on and
on the frame after something it reads or writes changes, instead of every
frame. Between those moments it would give the same result.

- **Saves**: CPU —a body that took about an eighth of the frame—.
- **Where**: `pure` in `rm2k-snes/events/src/commons.rs`; `compar_tick` in
  `runtime/common_events.s`.
- **More**: [The pure parallel common events run only when what they read changes](../../divergences/pure-parallel-common-events-run-only-when-what-they-read-changes.md).

Since 2026-10-17 a map's parallel page follows the same rule when it is
pure the same way, or also sets the panorama —`ChangePBG`—: The Frozen
World's `BackdropSetter`, 113 `if switch → ChangePBG` on its battle screen,
cost ~110 of the frame's 262 lines.

- **Where**: `pure_page` in `rm2k-snes/events/src/commons.rs`, bit 7 of
  the page's trigger; `pure_due` in `runtime/event_pages.s`.

## The refresh runs at three moments

The active pages are recomputed when the interpreter lets go, at the
start of the frame, and the expensive half —OAM rows and route slots— on
the next frame; not before every command, as EasyRPG does, because no
opcode reads which page is active.

- **Saves**: CPU —it is what makes the frame fit in cutscenes that turn
  switches on by the bunch—.
- **Where**: `pick_pages` and `apply_pages` in `runtime/event_pages.s`.
- **More**: [The refresh runs at three moments](../../decisions/the-refresh-runs-at-three-moments.md).

## A refresh only when something changes, and only for what changed

A switch or a variable written with the value it already had asks for no
refresh: a variable is noted with the value it had, and the refresh is
asked only if, where it is looked at, it is not that value any more —a
parallel page that computes a percentage in place goes through two other
values every frame and comes back—. And a refresh sets up again only the
events whose active page changed, which is RM2k's `SetupFromPage`.

- **Saves**: CPU —The Frozen World's Plate Placement refreshed its 425
  pages every frame and ran at six frames per tick; its battle screen at
  four—.
- **Where**: `set_switch`, `var_note` and `var_settle` in
  `runtime/variables.s`; `page_applied` in `runtime/event_pages.s`.
- **More**: the task
  [`frozen-world-the-battle-maps-lag`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/frozen-world-the-battle-maps-lag.md).

## One dispatch table for the opcodes

`run_code` dispatches with one `jmp (table, x)`, built from the bytecode's
declaration, instead of a chain of comparisons.

- **Saves**: CPU on every opcode.
- **Where**: the `EVENT_HANDLERS` macro, from `rm2k-snes/bytecode/src/events.rs`.
- **More**: [Events](../../internals/events.md).
