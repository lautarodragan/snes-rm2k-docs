# Lossy: events

## Translucent events are baked

The blend of a page's "Trans" —RM2k draws the event at 160 out of 255— is
computed in the converter against the layer below its cell and stays in
the graphic: no colour math, no dithering, no separate palettes. It can be
done exactly because the translucent pages A Blurred Line has are all
static —`move_type` 0 and no route of their own—: if neither the object
nor what is behind it moves, the blend always gives the same result.

The other two ways are not enough there. Colour math applies to every
sprite in palettes 4 to 7 at once, and was tried and left out —see [Tried
and left out](../tried-and-left-out.md#colour-math-for-translucent-events)—.
Dithering, which is what games of the era did, does not simulate
transparency over a dark background: the fires on ABL's map 9 sit on
almost pure black, and dithering punches holes in the flame.

- **Loses**: nothing is seen through them; over an animated tile the
  blend is right for one frame; two over different backgrounds are two
  graphics. The CharSets in the project's `[graphics] opaque` —the save
  point— go opaque instead.
- **Where**: `decorate_translucent` in `rm2k-snes/convert/src/game.rs`,
  which names the graphic; `rm2k-snes/wally/src/sheets.rs`, which draws it
  with `translucent` from `rm2k-render`.
- **More**: [Translucent events end up opaque](../../divergences/translucent-events-end-up-opaque.md),
  the divergence, with what was measured and when it stops being enough.

## Decorative events become background

With `[graphics] decorative_events`, an event that is only a drawing is
painted into the background and stops being an event.

- **Loses**: its animation follows the ChipSet water's rhythm and phase;
  a translucency that does not fit gets dithered; blocking moves to the
  grid.
- **Saves**: sprite tiles, rows and slots.
- **Where**: `rm2k-snes/wally/src/decor.rs`.
- **More**: [Baked decorative events](../../divergences/baked-decorative-events.md).

## More than four still events that animate

A still event that animates needs all twelve of its poses, like a walker.
Past a cap per map, none of that map's still events animate.

- **Loses**: on those maps, still events stand still.
- **Where**: `animates_still` in Wally, `rm2k-snes/wally/src/sprites/npc.rs`.
- **More**: [More than four still events that animate](../../divergences/more-than-four-still-events-that-animate.md).
