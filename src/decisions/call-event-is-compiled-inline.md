# CallEvent is compiled inline

> **Partly superseded on 2026-10-02** by
> [call-event-into-a-shared-body](call-event-into-a-shared-body.md):
> a common event is called with `OP_CALL` into a shared body when the page
> runs in the foreground and the body doesn't depend on the map. What
> follows still holds for what gets inlined: parallel pages, bodies that
> depend on the map, and calls to pages of map events.

## What

**`CallEvent` is compiled inline** since 2026-09-12, with no interpreter
stack. With that, the Hover-Tram on map 9 can be taken.

## Why

In RM2k it is `Push<ExecutionType::Call>`, a stack of interpreters; here
none is needed, because the callee runs in full before the caller
continues, so pasting its bytecode in place gives the same result. **No
call in this game is recursive**, measured, and nesting is capped at
`LLAMADA_MAX`.

It is the only one of the four pieces of that round that **doesn't touch
the interpreter**: what changes is the bytecode that is emitted, not who
runs it.

## What was measured

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
