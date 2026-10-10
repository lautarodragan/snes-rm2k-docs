# The choice bar does not alternate its two drawings

## What

The System carries **two drawings of the cursor**, at (64,0) and at (96,0),
and RM2k alternates them every ten frames: easyrpg's `Window::Draw` draws
`cursor1` with `cursor_frame <= 10` and `cursor2` for the rest of a cycle of
21. The ROM draws **only the first one**, in the choice bar of the message
window (`msg_bar_source` in `tools/runtime/message_arrow.s` in the-advocate) and
in all the screens that already had the bar —items, equipment, shop,
battle—, which come from `Skin::cursor` in `rm2k-snes-screens`.

## Why

The bar is composed inside the window's tiles, the same as the text:
alternating it would mean recomposing the highlighted line every ten frames,
about 1920 bytes of VRAM each time, or keeping both versions of the line in
VRAM and switching the tilemap, which is sixty more tiles in a bank that with
*A Blurred Line* ended up at exactly 256.

## Measured

In *A Blurred Line* it is not seen: the two drawings of its System,
`ablskin`, are identical pixel by pixel —a dark red, (83,0,0), with a
transparent border—. Measured on 2026-10-04 with the 2015 RPG_RT under Wine:
forty consecutive captures of the title menu and of a choice give the same
color.

## How it looks today

The same as in RM2k with this System.

## When it stops being enough

With a System whose two drawings differ: there RM2k's bar blinks and the
ROM's stays still on the first one. The fix in the message window is a second
`window_bar` and recomposing the highlighted line every ten frames from
`msg_arrow`, which already runs on every vblank while the window is open.
