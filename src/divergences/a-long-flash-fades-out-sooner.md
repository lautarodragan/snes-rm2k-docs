# A long flash fades out sooner

## What

`FlashSprite` lasts as many tenths of a second as it asks for, and its
strength goes down linearly from the power it asks for to zero over that
time. On the console a flash's frames are counted in a byte, and the
strength of each frame is divided by them with the hardware's eight-bit
divisor —`one_flash` in `runtime/character_flash.s` in the-advocate—, so
**a flash longer than 255 frames, 42 tenths, fades out in 255**: the same
flash, going out sooner. A page that waits for it still waits the whole
time: the wait is a separate `OP_DELAY`, as the Wait command's. The
compiler notes each one as a `flash-shortened` loss, in the cartridge's
`degradations.json`.

## Measured

On 2026-10-16, over the ported games: only Sunset over Imdahl asks for
more, 60 tenths —360 frames— on thirteen pages, all on the hero, white and
at full power, the statue's portal among them. Until that day they did not
compile, and the game stuck on its first square.

## When it stops being enough

When a long flash at low power is what is seen: there the faster fade
shows. Doing it whole is counting the frames in a word and dividing by
sixteen bits, which the hardware does not do in one go.
