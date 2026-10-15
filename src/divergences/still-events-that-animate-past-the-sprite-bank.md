# Still events that animate past the sprite bank

## What

A still event with continuous animation changes pose on the fly, so it
cannot share the VRAM slot of the still events that show its (CharSet,
index, pose): it needs **a slot of its own**, a 32x32 block of sixteen
object tiles, and its character's twelve poses go to the cartridge.

Except with its twins. The column of a still event that animates comes from
the game clock and its speed —see
[The phase of still events that animate](the-phase-of-still-events-that-animate.md)—,
so all the ones with the same graphic, pose and speed show the same pose on
every frame: **one uploads it and the rest are drawn with its slot**. The
six torches of The Book of Three's opening hall cost four slots, one per
speed. One that turns toward the hero, changes graphic with its page or is
sent walking by a test page keeps a slot of its own, and in a map with a
cache of slots nobody shares.

A map whose slots don't fit **gives up whole looks** —a (CharSet, index,
pose), all its speeds at once— from the one with the fewest events, until
the map fits without losing anything else: before dropping its pictures,
its battle animations, fusing its ground, or making events wait for a slot
of the cache —where each one that animates wants a slot of its own while
in view—. In RM2k they all animate.

Why by look and not event by event: two equal fountains, one moving and
the other frozen, look worse than both still, even if one flickers faster.
The rule and its order are in `moves` in `rm2k-snes/wally/src/moves.rs` in
the-advocate, and the search in `fewer_still_animations` in
`rm2k-snes/wally/src/map.rs`.

Until 2026-10-15 the cap was a fixed four per map, all or none, and each
event had its own slot: the opening hall, with six, animated none.

## Measured

On 2026-10-15, with the-advocate `7aa66900` and the ports `66a83f3`:
`still-animation-dropped` in each `release`'s `degradations.json`, maps
and events, with the fixed cap and with this.

| Game | Before | After |
|---|---|---|
| A Blurred Line | 14 maps, 345 events | 1 map, 61 events |
| The Book of Three | 1, 6 | 0 |
| Desert Nightmare | 0 | 0 |
| Dooms 2 | 0 | 0 |
| El Dorado | 7, 57 | 0 |
| The Frozen World | 1, 8 | 0 |
| Sunset Over Imdahl | 16, 297 | 8, 153 |
| Vampires Dawn | 93, 1,525 | 5, 126 |

What is left are maps that are over even with none animating, or where
animating would make events wait for a slot of the cache: Sunset's and
Vampires Dawn's crowded towns, and A Blurred Line's 148, sixty-one
torches whose ground is fused to fit. Vampires Dawn's 102 animates one of
its three looks.

## How it looks today

On those maps, the still events of the looks given up stand still.

## What it costs

Frame time, where the frame was already full. The runtime walks the rows
only on the tick a column changes —`animate_still` in
`runtime/animated_stills.s`, with the why—, and each group uploads one pose
then. A Blurred Line's race, whose 29 parked cars now animate in four
groups, went from 45 extra frames in 976 driving ticks to 49 on map 49's
lap, and its test's limit from five per hundred to six.

## When it stops being enough

A map where what is left matters. One with fused ground could trade some
more fused tiles for its animation —today the animation goes first, and
A Blurred Line's 148 would need two slots—; one with a cache would need
fewer events wanting a slot at once.

## As an optimization

What it saves, and where it lives in the code: [Still events that animate past the sprite bank](../optimizations/lossy/events.md#still-events-that-animate-past-the-sprite-bank), in Optimizations.
