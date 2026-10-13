# Reference

What the port stands on, without knowing anything about it: the format of
RPG Maker 2000 and the console. None of these pages talks about how the
port works —that is [Internals](../internals/README.md)—, but they are
needed to understand it.

- [Sources](sources.md): where the numbers and the semantics come from —
  liblcf, EasyRPG, fullsnes, the emulators, cc65—.
- **RPG Maker 2000**
  - [ChipSets](rpgmaker/chipsets.md): a ChipSet is not a tileset.
  - [The RTP](rpgmaker/rtp.md): the resources a game uses without bringing
    them, and which RTP each game needs.
- **The Super Nintendo**
  - [Emulators](snes/emulators.md): which ones to test the ROM with by
    hand, what each implements of the MSU-1 and of ExHiROM, debugging with
    Mesen2, and how to report a bug.
