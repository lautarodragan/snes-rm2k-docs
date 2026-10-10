# How the port works

These pages describe how each part of the port works **today**: the maps
and their grid, the split of color and video memory, the event bytecode,
the audio and the data the MSU-1 serves. The broad picture —[from a game
to a ROM](../pipeline.md), [the tools](../tools.md), [what gives way when
a game doesn't fit](../fitting.md), [the cartridge](../cartridge/README.md)
and [how it is tested](../testing.md)— is in the chapters before; these
go one level down, close to the code.

- [The pipeline](pipeline.md): which binary turns what into what.
- [Maps](maps.md): the map is stored as 16×16 blocks, and lives in WRAM.
- [The CGRAM split](cgram.md): the converter decides it, map by map.
- [The VRAM split](vram.md): the layouts, where the ceiling is, and what
  happens when nothing fits.
- [Events](events.md): the bytecode, who declares, emits and runs it, and
  the mechanics around it.
- [Audio](audio.md): which piece does what, and where its reason is.
- [The `.msu` file](msu-datos.md): data the MSU-1 serves to the ROM.

## Internals and research

The difference that matters is between these pages and the dated
studies, the research:

- **An internals page has to be up to date, or it lies.** That is why it is
  best kept short and pointing at the code instead of repeating it: what
  the code already says goes stale without warning if it is copied here.
  Whoever changes what one of these pages describes changes the page in
  the same commit.
- **A study is a snapshot and is not touched.** At the top it says the date
  and the commit of what it measured, and its numbers are from that moment.
  If something changed, it is measured again and a new study is written;
  the old one stays as it was.

The paths these pages name —`tools/runtime/…`, `tools/rm2k-snes/…`— are in
the the-advocate repository; the ones in A Blurred Line —`pruebas/…`,
`parches/…`— are in its port, `abl/` in the-advocate-ports.
