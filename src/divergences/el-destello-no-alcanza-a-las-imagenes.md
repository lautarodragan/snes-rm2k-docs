# The flash does not reach pictures

## What

`FlashScreen` **does not reach a picture** from `ShowPicture`. On the console
the flash is a CGRAM transformation: `flash_tick`, in
`tools/runtime/screen_flash.s` in snes-rm2k, walks the map's palettes —the
background, the upper layer and the characters' colors, `M_SPRITE_CGRAM` from
128 on— and the picture lives in sprite palette `7 - s` of its slot
(`pic_palette`, in `picture.s`), which is outside that range. In RM2k it does
reach it, always: in easyrpg `Game_Pictures::ShowParams` starts with the
flags `1 | 32 | 64`, and 32 is `affected_by_flash`; only RM2k3's
`ShowPicture` has the parameter that changes them.

The message window and the timer do not get the flash either, but those are
not a divergence: in RM2k they also stay above it (`Priority_Screen` is 90,
against 130 for the window and 140 for the timer), and the header of
`screen_flash.s` says so.

## Measured

First written down in the `ESTADO.md` at the root of snes-rm2k, frozen on 2026-09-23, and
read again in the code on 2026-10-10: still the same. At the time no page of
A Blurred Line flashed with a picture shown, so there is no case in the test
run that sees it, and no golden that bakes it in.

## When it stops being enough

When a game flashes with a picture on screen. The way out is to add the
palettes of the occupied picture slots to what `flash_sprites` walks; it
costs frame time, and the flash is already split over two frames because it
does not fit in one.
