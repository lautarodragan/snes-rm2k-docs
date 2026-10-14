# The timer has no palette of its own

## What

**The timer has no palette of its own**: it goes into the palette of any
character that uses thirteen colors or fewer.

## Why

Having it separate cost an undrawn event on map 2 —the middle cell of the
door Core breaks—, and an event that isn't drawn still takes up room in
`npcs_dibujables`.

What this costs today, and the idea of reserving it only while the timer
runs, is in [`timer-palette`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/timer-palette.md) in the-advocate-work.

## When it stops being enough

On a map that fills the eight palettes at fifteen colors. There room is
made for it by lowering a character to fourteen —the one that moves the
fewest pixels, and never a leader—: see the end of `drawable_npcs`, in
`rm2k-snes/wally/src/sprites/split.rs` in the-advocate. It only does that
to a palette with a single character in it.

And if not even that is enough —every palette full, and each shared or
lent to someone—, **the timer is lent a palette**, as a character is
since [every event is drawn](every-event-is-drawn.md): the one whose
nearest colors change the digits the least, each glyph color drawn with
its nearest. The converter says which one in a WARNING. It is from
2026-10-14, for ABL's Paradise with every leader of the game; until then
the converter stopped there. It only stops now if all eight palettes are
the leaders'. See `timer_digits` in `rm2k-snes/wally/src/sprites/extras.rs`.

## What it requires of the ROM

Since the palette belongs to a character, **the tint can't skip it
whole**: the digits aren't tinted and the character is. `upload_timer_pal`
uploads untinted only the digits' entries, and only while they are
visible. Until 2026-09-25 it uploaded the whole palette, which was right
when the digits had it to themselves, and the character was left untinted.
The colors the character shares with the digits are still untinted while
the timer is visible: see
[the-timer-and-its-neighbor-share-colors](../divergences/the-timer-and-its-neighbor-share-colors.md).
