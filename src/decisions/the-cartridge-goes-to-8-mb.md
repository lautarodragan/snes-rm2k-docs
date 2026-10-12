# The cartridge goes to 8 MB

## What

**The cartridge goes to 8 MB, ExHiROM**, so that the whole game fits,
playable without MSU-1. It replaces "the cartridge stays at 4 MB", from
2026-09-13.

And **the battle without MSU-1 carries the sound effects of its
animations**, even though the animations themselves go only in the `.msu`:
92 KB.

## Why

From taro, on 2026-10-01, with the numbers of
[the study of the whole game without MSU-1](../ports/abl/research/2026-10-01-the-whole-game-without-msu-1.md)
in front of them: the whole game, with everything that was missing, is about
8,073 KB. It doesn't fit in 4 MB with any cut; in 8 MB it fits **without
lowering the quality of anything** once the lossless cuts are applied (LZ2
where data goes raw, DTE in the texts, skips in the sequences: 7,151 KB),
with about 850 KB to spare. And
[the-game-is-playable-without-msu-1](the-game-is-playable-without-msu-1.md) rules out the
other way out, reading the maps from the `.msu`.

The 2026-09-13 decision said "revisit on reaching 85-90% of the
cartridge"; `release` reached 124 of 124 banks with Tangle Forest.

## How it applies

- First an ExHiROM test ROM on the FX Pak, before moving the game.
- The quality cuts of the study (backgrounds per ChipSet, sound effects at
  a lower rate, the sample ceiling) are left for when 8 MB gets tight, and
  taro picks them by ear and by eye.
