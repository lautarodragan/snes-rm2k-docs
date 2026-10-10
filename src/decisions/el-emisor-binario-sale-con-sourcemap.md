# The binary emitter ships with a sourcemap

## What

**The day the converter emits the data in binary** —`.incbin` instead of
`.byte` and `.word` in the `.inc`— **it ships with a sourcemap**: from the
offset in the `.bin` to which field of what it is, for example "the
`trigger` of page 2 of event 12 of map 8". Not later: with the emitter.

## Why

From taro, when the binary emitter was proposed, in September 2026; until
2026-10-10 it was written in `DITTO.md`, in snes-rm2k, which was deleted
that day.

Today the comments in the `.inc` are what lets you debug a piece of data,
and an `.incbin` has no comments. But that information also **already
evaporates on assembling**, so the map is worth having on its own and not
just as compensation:

* so that a red test says **which piece of data** fails, and not just how
  many pixels differ: the errors that showed up as "the screen turned to
  garbage" were pointers reading where they shouldn't;
* to translate a pointer read from RAM into what it points at, with the
  game running.

It has two hops —from the JSON to the `.bin`, and from the `.bin` to the
ROM offset—, and the second already exists: `rm2k-snes-assemble` writes a
`.sym` with the code's symbols, and this is its extension to the data.

**It is born with the emitter or not at all**: the serializer knows at
which offset it wrote each field while it writes it, and rebuilding that
afterwards means walking everything again.

What can't become binary stays as text: the constants the runtime uses as
symbols and the references only `ld65` resolves.
