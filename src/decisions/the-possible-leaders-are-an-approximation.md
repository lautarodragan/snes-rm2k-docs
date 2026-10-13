# The possible leaders are an approximation

## What

**The possible leaders are an approximation.** The converter simulates the
`ChangePartyMembers` of the pages that compile to know which actors can be
first in the party.

## Why

There is no static way to know it exactly, and which actors get a palette
reserved depends on it. **If a character is ever drawn without graphics,
this is the first place to look**; `tests/tooling/test_leaders.py`
in the ABL port (the-advocate-ports/abl) guards the part that already failed
once.
