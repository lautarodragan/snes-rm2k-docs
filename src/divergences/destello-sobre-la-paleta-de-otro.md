# A flash on someone else's palette

## What

On the console `FlashSprite` is **a CGRAM tint**: `paint_flash` uploads the
character's whole palette, so it tints everything that shares it —another
event with the same graphic, one that was lent the palette, or the hero when
the leader is also an NPC on the map—. **RM2k applies it to the sprite's
image**, that is, to just one. They are two different things.

## Measured

Before accepting it, on 2026-09-13, the compiler defended itself by not
compiling any page that flashed an event sharing a graphic: that cost **51
pages**, and one of them —`EV0027` on map 20— is the Bum's cutscene, without
which the player shows up invisible in Rat Tracks B2 and the game cannot go
on. There the one that flashes is `BumGuardingEntrance` and the one tinted
with it is `InnBum`: both are `Future3:1`.

It is covered by the `destello-compartido` case of the test run, on map 6,
where the target is the Kersh NPC and the one tinted with him is the hero.
Apart from that one, no case has a second visible sprite sharing the palette
of the one that flashes.

## How it looks today

It is guarded by `pruebas/herramientas/test_destello_paleta.py` in the ABL
port (the-advocate-ports/abl), which requires that nobody share the palette of
a possible leader, because there the one that leaks is the hero, who is on
screen all the time. **It protects the leader and not the one that
flashes**: the target is decided at run time and the hero is the only one
that can be known at conversion time, so a flash on another event would leak
just the same.

## When it stops being enough

When the one sharing the palette is next to the one that flashes and it
shows. The general way out would be to give the one that flashes a palette
of its own, on the fly, and today there is none free: the tight maps already
ask for more than eight.
