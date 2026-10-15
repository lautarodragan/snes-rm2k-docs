# More than four still events that animate

## What

A still event with continuous animation stops sharing the VRAM slot of its
(CharSet, index, pose) and needs **all twelve poses of its own**, like the
ones that walk. The cap is `ANIMATES_STILL_MAX` in `rm2k-snes/wally/src/moves.rs` in
the-advocate, and it is **per map and all or nothing**: with more of those, the
map animates none of them. In RM2k they all animate.

Why all or nothing is in the comment on the cap: animating some and not
others looks worse than not animating —two identical fountains, one moving
and the other frozen— and would need a rule to pick which ones.

## Measured

On 2026-09-09, with the cap at four: map 52 has thirty and asked for 572
sprite tiles against the 384 that fit. Of the game's 328 maps, 312 had four
or fewer, and among the ones the ROMs carried, the only one over was 52.

## How it looks today

On map 52 the still events that animate in RM2k are still.

## When it stops being enough

A map over the cap that does matter. There you have to look at that map's
sprite budget and raise the cap, not change the rule: the converter stops
with the number in the message if they do not fit.

## As an optimization

What it saves, and where it lives in the code: [More than four still events that animate](../optimizations/lossy.md#more-than-four-still-events-that-animate), in Optimizations.
