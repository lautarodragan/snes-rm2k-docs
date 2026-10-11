# A single sample bank

## What

**Music tracks share a single sample bank** —one sample per General MIDI
program and one per drum hit, across the whole cartridge—, which is
uploaded to the ARAM **in packages, one per map**. Each sample gets the
budget of its worst package, **unless that package doesn't have every track
that uses it**: then, as long as it fits in the directory, the tracks
inside play a copy and the ones outside stop paying for it.

## Why

**One bank and not one copy per track** is because of the numbering and
the directory. The SRCN the stream writes is the sample's number in the
cartridge, so two tracks that play piano point at the same one, and SRCN is
one byte. One copy per track (option B of step 6 of the task
`tasks/testing/la-calidad-de-la-musica.md` in the-advocate-work) would be
about 370 entries against 255. Until 2026-09-26 SRCN also numbered every
sound effect in the cartridge; since that day the effects share the slots
at the end of the directory, because the ARAM gets one package at a time:
see the task `el-directorio-de-los-efectos.md`.

**The budget is per package and not per bank** since 2026-09-26 (option A
of the same step, chosen by taro). What goes to the ARAM is never the bank
but a package, so what has to fit in the 64 KB is each package with its
sound effects, and the track that may come playing from the previous map
(see
[el-tema-que-suena-gana-y-los-efectos-esperan](el-tema-que-suena-gana-y-los-efectos-esperan.md)).
Until that day the **whole** bank had to fit, and nineteen of `release`'s
thirty-two tracks didn't bring any programs of their own.

**The copies**, since the same day and by taro: *"I don't find it
acceptable that instruments lose quality because of a single map, but I
don't want to lose quality in the sound effects either."* With one sample
per program, map 3's 43 KB of sound effects left the drums of every track
at 10 kHz and the oboe at 7. A copy is the same key as another sample, only
for the tracks of the group that limits it; the worst ones are made first
until the directory is filled as it was when each sound effect had its own
entry, and with the entries the effects freed, only those that don't lower
anyone's rate (see `copies` in
`rm2k-snes/rm2k-snes-audio/src/bank.rs` in the-advocate). And the tracks
a map turns on only to leave —`lufsorr` on map 3, which plays when there
are no sound effects left— don't count in the map's package: see
`Temas.de_salida` in `tools/port/eventos.py`.

**What it costs**: each package fills almost the whole ARAM, so uploading
it takes longer —the battle, 58 frames on entering instead of 36—; taro
accepted it ("1.3 s is a very low cost to pay for what we get in return").
The copies weigh on the cartridge, and what is freed from one package
competes in the others: the allocation gives everything the same fraction,
so what used to play at 22 kHz because the drums were at 10 now ends up
near 16. An exit track that doesn't fit next to its package freezes, when
turned on, for as long as it alone takes to upload.

How it is allocated, in `allocate`, `copies` and `Bank` of
`rm2k-snes/rm2k-snes-audio/src/bank.rs`; which group limits each
sample and which tracks use each copy, in the converter's report.
