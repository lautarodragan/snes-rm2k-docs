# Screen ticks run after the interpreter

## What

**The flash, the shake, the panned camera, the sign and the rain advance
after the interpreter, and in RM2k they advance before it.** They are
`game_screen->Update()` and `game_pictures->Update()`, which in
`game_map.cpp:1305` come **before** `UpdateForegroundEvents`; here they come
after.

## Measured

It was left out when the frame was ordered like `Game_Map::Update`, on
2026-09-20 —see the comment on the loop in `tools/runtime/boot.s` in
the-advocate—. None of those ticks decides whether something moves or when, so
**the difference is one frame in what is shown** and nothing more.

## How it looks today

It is not red. Moving them is a separate change and **moves their goldens**,
so it ships with its own blessing.
