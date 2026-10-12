# The game is playable without MSU-1

## What

**The whole game has to be playable without MSU-1.** MSU-1 is an optional
improvement —music as audio tracks, better-quality sound effects and
backgrounds, the battle animations—, never a requirement to reach the end.

## Why

From taro, on 2026-10-01, on reading
[the study of maps over MSU-1](../ports/abl/research/2026-10-01-los-mapas-por-el-msu-1.md),
which recommended a `completo` cartridge that required MSU-1: "I want to
avoid depending on the msu completely. I'd like the game to be playable
without msu". It replaces that recommendation.

## How it applies

- **What fits in the ROM has to be enough to play**: maps, events, texts,
  music through the SPC700. If it doesn't fit, quality is lowered in the
  ROM ([primero-el-juego-entero-despues-la-calidad](primero-el-juego-entero-despues-la-calidad.md)),
  it isn't sent to the `.msu`.
- **The `.msu` carries the better version of the same thing.** taro's
  criterion, the same day: without MSU-1 the map backgrounds are quantized
  as needed so as not to duplicate graphics —sharing tiles between maps of
  the same ChipSet, with fewer colors—, and with MSU-1 they can be read
  from the `.msu` quantized per map, with all their colors.
- **The battle animations go only in the `.msu`**: without MSU-1 there are
  none. The ones events show in cutscenes stay in the ROM, unless they need
  to be taken out.
- **The exception is a game whose ROM does not reach**, decided by its
  project and not by the converter: since 2026-10-11, [the MSU-1 is
  required only when the ROM does not
  reach](el-msu-1-obligatorio-si-la-rom-no-alcanza.md). A Blurred Line is
  not one.
