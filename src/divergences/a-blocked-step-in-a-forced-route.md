# A blocked step in a forced route

## What

**A blocked move in a forced route is skipped**, and RM2k would retry it
forever —`UpdateMoveRoute` with `skippable` off—.

It is an old, declared modeling decision, in `tools/port/eventos.py` in
the-advocate: a test that hangs says nothing.

## Measured

Until 2026-09-20 no golden exercised it. With the frame reordered, the hero's
route in `droid-covered` starts one frame later, the step up lands exactly
when the droid occupies the cell, and the step is lost: **the hero ends up one
cell lower than before**, and no tick makes the capture match —tried from -12
to +12—.

## How it looks today

The new golden freezes that. If the block is ever retried instead, **those
five goldens move**.
