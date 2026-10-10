# Walking through walls also applies to jumps

## What

**Walking through walls also applies to jumps**, not just to walking. But
**it is not leaving the map**.

## Why

`CheckOrMakeWayEx` cuts off with `if (self.GetThrough()) return true;`
before looking at passability, and `BeginMoveRouteJump` goes through it.

The bounds check comes first, so whoever walks through walls **gets stuck
on the last column**.
