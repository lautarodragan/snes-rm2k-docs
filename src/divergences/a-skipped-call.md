# A skipped call

## What

When a `CallEvent` calls an event that does not compile, **the call is
skipped**. It is what the port has been doing all along, and in the Tram
Officer's scene what that costs was measured, when the skipped page does
something.

## Measured

On 2026-09-12, checking `tram` in red: with `CallEvent` not implemented **on
both sides** —which is how it was until that day— **frame 620** of that
scene gave **34.64%** of differing pixels between the ROM and the reference.
With the call implemented it gave zero.

The suspect is the timer, which that branch starts. It was not
investigated.

## How it looks today

The page that exposed it no longer goes through there —`CallEvent` is
compiled inline since 2026-09-12— but **the path still exists** for the
calls that are still skipped: `rm2k-snes-events culprits` lists them. On
2026-09-12 they were 216, almost all to common events that stopped at
`ControlVars` and at the original's own menus; in A Blurred Line the last
47, to common event 45, went away on 2026-10-11 with
[Variables saturate at sixteen bits](variables-saturate-at-16-bits.md).

## The autostart page that only calls

Since 2026-09-28 an autostart or parallel page that **compiles to nothing**
—everything in it was calls that got skipped— is not carried, the same as an
empty one: running it was an endless loop that left the hero unable to
move. See `paginas_del_mapa` in `tools/port/eventos.py` in the-advocate.

It is the `AfterBattleMint` of the maps with encounters —from 20 to 255—:
with switch 498 it calls common event 35, `ResetAfterBattles`, and the common
event is the one that turns 498 off. It is turned on by the turn-0 page each
troop carries, which runs since the battle learned to look at the turn (the
task [`release-troop-events`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/release-troop-events.md), in `tasks/` in the-advocate-work).

**Since 2026-09-30 common event 35 runs**: what blocked it were the
variables only it names —the 53 for the summons and for Talan's HP—, which
had no slot in the save because the variable sweep did not look at common
events. Now it does (`variables`, in the indices of `rm2k-snes-events`), and
the common event compiles in place of its `CallEvent`. It is guarded by
`test_despues_de_la_pelea_lerle_vuelve_al_grupo`, in
`pruebas/rpgmaker/test_sistemas_de_tropa.py` in the ABL port
(the-advocate-ports/abl).

Until 2026-10-02 that cost space: the whole common event was copied into
every map with encounters, because `CallEvent` compiled in place. Since that
day the autostart page calls it with `OP_CALL` to a shared body —see
[CallEvent to a shared body](../decisions/call-event-into-a-shared-body.md)—,
and it is in the cartridge only once.
