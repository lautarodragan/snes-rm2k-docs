# data/ is the resolved view

## What

`data/` is the **resolved view** of the game —every field written out and
enums as numbers— and the exact dump **isn't versioned**.

## Why

From 2026-09-20. `ditto unpack` emits both in the same run: `data/` and
ABL's `build/ditto-exacto/`, shaped like the binary. With that,
`tools/rpgmaker/lcf.py` doesn't know any rule of the format, which was the
goal.

Losing the names in `data/` is accepted: they come back the day the
pipeline is Rust and Ditto is a library.

Not versioning the exact dump is what makes **the game the only source of
the binary**, which is what `ditto pack` already needed to have alongside
to compare against.

And the reason for reading the dump and not the binary, the decision this
one hangs from: the format **doesn't store a field when it holds its
default**, so whoever reads it has to know every default. Until 2026-09-14
there were two readers of the same format, each with its own defaults
written by hand, and both got them wrong the same way: an enemy's `max_hp`
arrived as 1 where the format says 10, the enemy died in one hit, and
there was nothing to compare against. Since then only Ditto reads the
format, with the defaults of liblcf's schema, and everything else reads
what it dumps.

Until 2026-10-10 this, with the story of how it was reached, was in
`DITTO.md` in snes-rm2k; it was deleted that day, and what holds for an
outside reader went into the book, in
[From a game to a ROM](../pipeline.md).
