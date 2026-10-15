# CallEvent: a shared body, or pasted in place

Two lossless optimizations —see [Lossless](lossless.md)— for RM2k's
`CallEvent`, which in RM2k pushes another interpreter. The port runs no
stack of interpreters: a common event is called into a shared body when
it can be, and pasted in place when it cannot.

## Into a shared body

**A common event has a shared body in the cartridge, and it is called with
`OP_CALL`** since 2026-10-02: autorun ones, the ones called by pages that
run in the foreground, and the ones those call. **It is still
[pasted in place](#pasted-in-place)** when the page is parallel, when the body
compiled with the map isn't the same as without it, and in troop pages and
equipment common events.

The interpreter has **a single call stack**, the foreground one: three
levels of five bytes in far RAM (`$6110` to `$611F`), and a call with the
stack full is skipped. The converter emits the deepest chain as
`COMMON_DEPTH` and the build refuses if it doesn't fit.

### Why

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

### What was measured

On 2026-10-02, in `release`: 25 bodies and 8,176 bytes in the cartridge;
autorun common events 7, 11, 39, 43 and 50 run, and 16, 42 and 44 don't
compile. The goldens didn't move. How much is left today is what
`just space` (in the ABL port) says, and which bodies there are, the
converter's report.

## Pasted in place

What does not go to a shared body —parallel pages, bodies that depend on
the map, calls to pages of map events— is pasted in place. It was the
first way, and for everything until 2026-10-02.

**`CallEvent` is compiled inline** since 2026-09-12, with no interpreter
stack. With that, the Hover-Tram on map 9 can be taken.

### Why it is enough

In RM2k it is `Push<ExecutionType::Call>`, a stack of interpreters; here
none is needed, because the callee runs in full before the caller
continues, so pasting its bytecode in place gives the same result. **No
call in this game is recursive**, measured, and nesting is capped at
`CALL_MAX`, in `rm2k-snes/events/src/compile.rs`.

It is the only one of the four pieces of that round that **doesn't touch
the interpreter**: what changes is the bytecode that is emitted, not who
runs it.

### What was measured when it was born

**Zero pages gained and zero lost** —2882 before and after—, because if the
callee doesn't compile the call is skipped, which is what the port had been
doing. Requiring it to compile would cost **183 pages** of the 221 that
compile and call.

**10 calls** are made for real, on four maps —9, 11, 114 and one more— and
216 are still skipped, almost all to common events that stop at
`ControlVars` and at the original's own menus: that has its own page in
[a-skipped-call](../divergences/a-skipped-call.md).

The price in cartridge is **+608 bytes of bytecode in the whole game,
+0.9%**, and three maps take it: 11 (+344), 9 (+195) and 114 (+69).
