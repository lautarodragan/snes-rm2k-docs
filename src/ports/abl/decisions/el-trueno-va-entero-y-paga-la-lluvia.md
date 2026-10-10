# The thunder plays whole, and pays for the rain

## What

**The opening thunder plays whole, without a loop, at 8,800 Hz**, and what
that saves in map 1's package pays for **the whole rain**. And **sound
effects have two voices**, so the rain doesn't cut it off.

Whole and the two voices are taro's, from 2026-09-24, listening to the
experiment's ROMs in Mednafen and on video. The 8.8 kHz are taro's too,
from 2026-09-26.

## Why

With the 0.75 s cap and the 0.4 s loop, the thunder repeated its loudest
stretch until it filled its duration and cut off dead: taro heard it
stutter even though nothing stepped on it. That is what isn't negotiable:
**whole**.

The rate is. On 2026-09-24 he chose 22,050 Hz —that of its WAV— because it
had more treble than at 16 kHz. On 2026-09-26 the rain started playing
whole (its five seconds, without the loop), and in map 1's package, which
was already full, that lowered the rate of almost all of `escape_newyork`
—the polysynth from 21 to 8 kHz—. With the thunder at 8.8 kHz the two whole
effects take the same space that the thunder at 22 kHz and the trimmed rain
used to, and **no instrument goes down**. taro had already heard the
thunder at lower quality and found it quite acceptable.

With a single voice, the rain cut the thunder off, because it retriggers
every few seconds: see "the sound effects" in
`tools/runtime/sound_effects.s` in snes-rm2k.

## How it ended up

The whole thunder is an alias, `Thunder9@entero`, which `_compilar` puts
only on map 1 (`per_map` in `[sound_effects]` of the project file): maps 3,
20 and 32 also ask for the thunder, and those carry the usual one, whole at
6 kHz. Both, and the rain, are in `SE_ENTEROS_PAGADOS`: the music of their
package pays for them if needed. If the thunder or the rain change rate,
map 1's package becomes limiting again: the converter prints which samples
each package limits. See the task `efectos-de-sonido-sin-recortes.md` in
snes-rm2k-work.
