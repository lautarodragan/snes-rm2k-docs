# Optimizations

What the port does to make an RPG Maker 2000 game fit a Super Nintendo:
in the cartridge's ROM, in the console's 128 KB of WRAM, in its 64 KB of
VRAM and 256 colours of CGRAM, in the sound chip's 64 KB of ARAM, and in
the CPU time of a frame. Each optimization is one entry: what it is, what
it saves, where it lives in the code and the page that explains it more.

- [Lossless](lossless.md): what saves space or time **without changing
  what is seen or heard**. The goldens and the tests come out the same
  with it and without it.
- [Lossy](lossy.md): what **trades fidelity for fit** —a colour merged, a
  tile fused, a sample at a lower rate, a picture scaled—. Each says what
  is lost, and the build warns when it applies.
- [Tried and left out](tried-and-left-out.md): what was built or measured
  and then removed or not adopted, and why, so it is not tried again
  blind.

How much each one saves **today** is not written here: it changes with
every game and every map, and the command that prints it is the source.
`just space`, in a game's project, says what each cartridge has left; the
converter's log says what each map lost. The numbers below are properties
of the hardware or of the formats, or come from a dated page that says
when they were measured.

The paths —`runtime/…`, `rm2k-snes/…`, `snes/…`— are in the-advocate.

Until 2026-10-15 several of these lived elsewhere: as decisions, as a
divergence, and the rule of the lossy ones as its own chapter, "When a
game doesn't fit". Their old addresses redirect here.
