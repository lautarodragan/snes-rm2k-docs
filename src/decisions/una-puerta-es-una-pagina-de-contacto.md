# A door is a touch page

## What

**A door is not a special case: it is a touch page with a `Teleport`
inside**, and it goes through the interpreter like any other event.

## Why

It had its own table while there was no interpreter —`collect_doors`,
`cruzar_puerta`—; it went away on 2026-09-20 because **the table froze the
active page when the game started**, and with that it lied about the two
doors on map 10 whose destination switch 231 changes.

The only survivor of that path is `FADE_DOOR`, which today only the test
harness writes, to drop the game onto a map: it is explained on its line in
`tools/runtime/low_ram.s` in the-advocate.
