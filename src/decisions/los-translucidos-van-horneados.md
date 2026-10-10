# Translucent events are baked

## What

**Translucent events are baked**: the blend of a page's "Trans"
—`translucent`, which in RM2k draws the event at opacity 160 out of 255—
is computed in the converter against the layer below its cell and stays in
the graphic. No color math, no dithering, no separate palettes. How, in
`decorar_translucido` (`tools/rpgmaker/rm2k.py` in snes-rm2k); the
exception, the save point, which goes opaque, in `SIN_TRAMA`, next to it.

## Why

The other two paths aren't enough in this game:

* **Color math** is real transparency, but the console applies it to every
  sprite in palettes 4 to 7 at once, so a map with translucent events would
  have to leave those four palettes to them alone. And once tried, it has
  two costs taro didn't accept: see
  [el-color-math-no-se-usa](el-color-math-no-se-usa.md).
* **Dithering** —dropping some of the pixels, which is what games of the
  era did— doesn't simulate transparency when the background is dark:
  **the fires on map 9 sit on almost pure black**, and dithering punches
  holes in the flame.

What makes baking possible is that **the game's translucent pages are all
static**: `move_type` 0 and no route of their own. If neither the object
nor the background moves, blending against the layer below always gives
the same result and can be computed once, exactly.

What is lost —nobody is seen through them, an animated tile underneath
counts for a single frame— and when it stops being enough, in
[los-translucidos-quedan-opacos](../divergences/los-translucidos-quedan-opacos.md).
