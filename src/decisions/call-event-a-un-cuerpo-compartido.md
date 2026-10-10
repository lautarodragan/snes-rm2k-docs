# CallEvent into a shared body

## What

**A common event has a shared body in the cartridge, and it is called with
`OP_CALL`** since 2026-10-02: autorun ones, the ones called by pages that
run in the foreground, and the ones those call. It partly replaces
[call-event-se-compila-en-linea](call-event-se-compila-en-linea.md): **it
is still pasted in place** when the page is parallel, when the body
compiled with the map isn't the same as without it, and in troop pages and
equipment common events.

The interpreter has **a single call stack**, the foreground one: three
levels of five bytes in far RAM (`$6110` to `$611F`), and a call with the
stack full is skipped. The converter emits the deepest chain as
`COMMON_DEPTH` and the build refuses if it doesn't fit.

## Why

**The portable console doesn't fit inlined.** Common event 39 calls 21,
which calls 25 eighteen times, which calls eight of 23 to 31: inlined it is
140,193 commands; shared, the game's 25 bodies are 8 KB.

**And inlining cost more than the old decision said.** That one measured
+608 bytes in the whole game, when ten calls compiled; with common event 35
compiling since 2026-09-30 —`ResetAfterBattles`, which the autorun
`AfterBattleMint` of every map with encounters calls— the bytecode of
`release`'s maps was 136.4 KB raw, and 81.5 without any call. Sharing, it
comes to 89.3 KB raw, 46.7 KB in LZ2 against 89.1 before.

**Why not every call.** A shared body is compiled without a map, and
whatever a map resolves isn't there: its events —a route, "this event"—,
its sprite bank, the pictures it carries, the sound effect that plays there
with a different sample, a `TileSubstitution`. That is why a page calls
only if the body compiled with its map is **byte for byte** the one without
a map; if not, it pastes as before, and stays just as exact. The only
difference that is forgiven is the refresh: without a map, every variable
write requests it, and with the map only the ones some page condition
looks at (`refresh` in `compile.rs`). In a foreground page it costs
nothing —the refresh is a flag, and it runs once when the interpreter lets
go—; in a parallel one, which runs every frame, it is what left half of
Lashe City at thirty frames per second, **and that is why parallel pages
paste**. Besides, they share the foreground's globals: a stack for them
would be another one per interpreter.

**Why in the cartridge and not with the map.** An autorun common event runs
on any map, and a shared one can keep running after a `Teleport`: read from
ROM, it doesn't move. What does move is the page that called, which is in
the map's bytecode in WRAM: `code_carry_before` moves the stack frames to
`CODE_CARRY` too, not just the cursor.

## What was measured

On 2026-10-02, in `release`: 25 bodies and 8,176 bytes in the cartridge;
autorun common events 7, 11, 39, 43 and 50 run, and 16, 42 and 44 don't
compile. The goldens didn't move. How much is left today is what
`just espacio` (in the ABL port) says, and which bodies there are, the
converter's report.
