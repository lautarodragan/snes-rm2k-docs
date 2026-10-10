# Running out of the teleport budget is an error

## What

**Running out of the teleport budget is an error, not a case to handle.**
When it runs out, the ROM calls `enter_panic` instead of carrying on.

## Why

A jump silently dropped is the failure mode that `AGENTS.md` (in
snes-rm2k-work) names —a path nobody runs and nothing catches—, and this
one survived for weeks because the game kept going, only on the wrong map.
