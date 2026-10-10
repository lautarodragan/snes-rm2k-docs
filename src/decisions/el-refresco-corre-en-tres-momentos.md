# The refresh runs at three moments

## What

**The refresh runs at three moments and is split in two halves:**

    on leaving the interpreter   picks only the events with autorun pages
    at the start of the frame    picks every active page
    same, afterwards             reloads the NPCs' routes and graphics

## Why

It isn't an optimization of taste: it is what makes it fit in a frame.

The first is the `if (GetNeedRefresh()) Refresh();` at the end of
`Game_Interpreter::Update`, and RM2k's idiom depends on it: a page that
turns on the switch that deactivates it stops being the active one before
it is decided what runs next. Without it, map 2 lost eight frames
restarting itself.

EasyRPG also refreshes **before every command**. Here it isn't needed and
it is expensive —five frames in the opening cutscene, which turns on
switches by the bunch—: none of the existing opcodes reads which page of an
event is active. **The day one that does shows up, this goes back into the
loop.**

And the expensive half —reloading OAM rows and route slots— is deferred to
the next frame, because it isn't visible until it is drawn.
