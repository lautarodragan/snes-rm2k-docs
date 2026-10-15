# CallEvent: a shared body, or pasted in place

Two lossless optimizations —see [Lossless](../../lossless.md)— for RM2k's
`CallEvent`, which in RM2k pushes another frame on the interpreter's
stack. The port has one such stack, the foreground interpreter's: a call
is a call when that interpreter runs it and the callee is a body the
cartridge has once —a common event's shared body, or a page of the same
map—, and the body is pasted in place when it cannot be.

## Into a shared body

**A common event has a shared body in the cartridge, and it is called with
`OP_CALL`** since 2026-10-02: autorun ones, the ones called by pages that
run in the foreground, and the ones those call. **A map event's page is
called with `OP_CALL_PAGE`** since 2026-10-15, from any page of the same
map that runs in the foreground: the operand is the page's index in the
map's page table, the console reads the page's code pointer there
—wherever the code is, behind the grid in WRAM or in the cartridge for a
map too big for it— and runs the same bytes the page runs as itself. **It
is still [pasted in place](#pasted-in-place)** when the caller is a parallel
page, a troop page or an equipment common event; when the common event's
body compiled with the map isn't the same as without it; and when the
page is called after a `Teleport` to another map.

**The return is `OP_DONE`.** A called page is the page's own bytes,
`OP_DONE` at the end included, so `OP_DONE` ends the *frame*: with
someone waiting on the stack it returns to the caller right after its
call, with nobody it ends the page. That is what RM2k's `END` and its
`EndEventProcessing` do —`Game_Interpreter::EndEventProcessing` ends the
frame it runs in, not the interpreter—. `OP_RETURN`, which ended a shared
body until then, is the same thing now.

The interpreter has **a single call stack**, the foreground one: eight
levels of five bytes —the caller's code pointer and cursor— in bank 0's
RAM (`call_depth` and `call_stack` in the runtime's `common_events.s`),
and a call with the stack full is skipped, as is a call to a page with
no code. The deepest chain in the eight games is six, Frozen World's
battle round; Vampires Dawn has two common events that call each other,
which no depth holds. The compiler reports in `degradations.json` each
chain it can see is deeper —`call-stack-exceeded`, on the chain's first
page—, and the build goes on: until 2026-10-15 the stack had three
levels in far RAM and the build refused a deeper chain of common events.
The parallel interpreters —a map's parallel pages, the parallel common
events, a troop's page in battle— run with the depth at zero and give it
back, so their `OP_DONE` ends their own page.

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

**Why a map event's page is called by its index in the table, and only
within its map.** The page's code is in the map already, compiled as
itself —"this event" resolved to its owner, as `Push` does—, and the
page table points at it with 24 bits wherever it ended up: a pointer in
the bytecode would have to be carried on a teleport like the stack's
frames are, an index needs nothing. The table the console indexes is the
loaded map's, so a page called after the page jumped to another map is
pasted, as it was. A page left out of the table —one whose condition the
console cannot evaluate— has no index and is pasted too; a page that does
not compile has a zero pointer, and the console skips the call, which is
what the port has always done with a call whose body does not compile.

**Why `OP_DONE` returns, instead of a called page ending in `OP_RETURN`.**
The callee is the page's own bytes, stored once: making them end in
`OP_RETURN` would have had every foreground page end that way, which is
every page's last byte in every map, and a parallel page called by a
foreground one would still have needed the other end. One opcode that
knows whether someone is waiting is the whole change, and it is what RM2k
does.

**Why the stack is the foreground's alone.** A parallel page that waited
inside a call —a message, a `Wait`— would hold its frames across frames
while the foreground pushes and pops its own; a stack per parallel is
eleven bytes per parallel at least, with far RAM full. Parallel pages
paste what they call, as they did, and the three places that run a
parallel interpreter zero the depth while it runs.

### What was measured

On 2026-10-02, in `release`: 25 bodies and 8,176 bytes in the cartridge;
autorun common events 7, 11, 39, 43 and 50 run, and 16, 42 and 44 don't
compile. The goldens didn't move. How much is left today is what
`just space` (in the ABL port) says, and which bodies there are, the
converter's report.

On 2026-10-15, the pages called instead of pasted, over the maps of each
game's `release` with the pages and routes of each map stored once:
Frozen World's map 1, the battle screen, from 386,706 bytes to 57,261
—the whole game, with that map, from 544,342 to 198,837—; Desert
Nightmare from 74,786 to 63,896; A Blurred Line from 145,888 to 143,817
(its map 11, from 10,052 to 8,316); Sunset over Imdahl from 23,105 to
22,192; Book of Three, Dooms 2, El Dorado and Vampires Dawn unchanged,
having no call to a map event's page from a foreground page. The task is
[`callevent-as-a-real-call`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/callevent-as-a-real-call.md).

## Pasted in place

What does not go to a shared body —parallel pages, bodies that depend on
the map, pages called after a jump to another map, troop pages— is pasted
in place. It was the first way, and for everything until 2026-10-02; for
map events' pages, until 2026-10-15.

**`CallEvent` is compiled inline** since 2026-09-12, with no interpreter
stack. With that, the Hover-Tram on map 9 can be taken.

### Why it is enough

In RM2k it is `Push<ExecutionType::Call>`, a stack of frames; pasting
gives the same result because the callee runs in full before the caller
continues. Nesting is capped at `CALL_MAX`, in
`rm2k-snes/events/src/compile.rs`: a common event can call itself, and
Vampires Dawn's 25 and 26 call each other, which pasted would never end.
What it costs is the callee's size at every call: on Frozen World's
battle screen, whose pages call the same pages dozens of times four levels
deep, that was four megabytes, which is why the pages became calls.

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
[a-skipped-call](../../../divergences/a-skipped-call.md).

The price in cartridge is **+608 bytes of bytecode in the whole game,
+0.9%**, and three maps take it: 11 (+344), 9 (+195) and 114 (+69).
