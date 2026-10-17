# The chests' colours

> **Measured on 2026-10-16**, by Carpintero, with the tools at `63b46ae9`
> (the-advocate) and ABL at `059ddcd` (the-advocate-ports): the `release`
> cartridge, wally's own request and answer for every map, and captures of
> snes9x. It is a snapshot: this file is not updated. The task is
> [`abl-chests-change-colour-from-map-to-map`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-chests-change-colour-from-map-to-map.md).
> Nothing in the tools was changed: the alternatives below were made by hand,
> with a throwaway script over wally's output.

taro, playing: the chests change colour from map to map; open ones look
flatter than closed ones; and in the Neon Vipers' HQ, with Arden, they look
golden. The question is whether the same number of colours, distributed
differently, keeps them right **without treating chests as an exception and
without making anything else worse**.

## Where, and why golden

The HQ is the north-west corner of map 38, `Sector 34 With Car`, reached
through the pipe with Arden; its chests are events 45–47, `BLObjs`
character 2, closed in pose 9 and open in pose 10. They are thirteen greys
and the two orange pixels of the lock.

Map 38 has 22 characters with a palette and eight object palettes. The four
first are the leaders' —Talan's slot, the two vehicles the hero drives, and
Arden, who is also an event and gets her own— and nobody else may enter
them. The other seven event characters and the timer's colour share four.
The split (`drawable_npcs` in `rm2k-snes/wally/src/sprites/split.rs`) puts
each character, in order, into the first palette that holds its colours
**exactly**; when none does and none is free, it is **lent** the palette it
misses the fewest pixels of, and each missing colour is drawn with its
nearest **by luma**. The converter says so:

    map 38: 3 graphic(s) without a palette of their own, drawn with someone else's: BLObjs:2, Chara2:2, People4:0

The chest is lent palette 6, which is Chara4:1's —the blonde woman—: four
yellows, `(13,13,0)` to `(28,28,7)`. Luma weighs blue at 0.11, so a yellow
and a grey of the same brightness are near, and the greys land on yellows.
Two things make the choice worse than it has to be: the lending cost counts
the twelve poses of `BLObjs:2` —47 colours, other objects of the sheet—
when the map shows two, and it counts *how many* pixels miss, not *how far*
they go.

The same mechanism hits the other two lent characters, and they show more
than the chest: People4:0 is drawn with brown hair instead of olive, and
Chara2:2 —three kids with black hair— with brown hair and darker skin.

## Open chests

In every other map with chests (20, 21, 26, 32, 59, 60, 61, 62, 255, 261,
263, 289, 292, 293) both poses come out **exact**: the chest has room in a
palette and not one colour moves. The open chest is flatter **in the
drawing**: eleven colours, 77 of its pixels a near-black interior, and the
four light greys at four pixels each. On map 38 it does lose a grey: 16 and
19 both become `(18,18,1)`, and 23 becomes `(30,23,15)`.

Map 316 also moves the chest's greys, but it does not show the chest: its
`BLObjs:2` event shows pose 7, another object, and turns toward the hero, so
its fifteen colours are chosen over the twelve poses.

## Alternatives, by hand

Fixed: the leaders' four palettes, the count —four palettes of fifteen for
the seven characters—, the timer's colour in Chara2:4's palette, which
wally already lowered to fourteen for it. The seven were split into four
groups in every possible way (350); each group's palette is the union of
its characters' colours merged least visibly —adeleine's `merge_least_visible`,
reimplemented— down to fifteen, weighting each character by what one pose
of it covers on screen times its events. The script reproduces wally's
eight palettes for today's split but one colour, the timer's.

Error is the mean CIE76 ΔE per pixel over the poses the map shows, against
the CharSet's colours at 15 bits. The map's background has no merged colour,
so the original is the sheet.

| character | today | today, nearest by Lab | M, luma | M, Lab | N, Lab |
|---|---:|---:|---:|---:|---:|
| `Future1:0` (Talan) | 1.7 | 1.7 | 1.7 | 1.7 | 1.7 |
| `BLVehicles:2` | 6.9 | 6.9 | 6.9 | 6.9 | 6.9 |
| `BLVehicles:5` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 |
| `Chara2:0` (Arden) | 3.1 | 3.1 | 3.1 | 3.1 | 3.1 |
| `Crown3:1` | 3.6 | 3.6 | 7.4 | 6.3 | 3.6 |
| `Chara2:4` | 4.0 | 4.0 | 4.3 | 5.9 | 5.9 |
| `Chara4:1` | 6.3 | 6.3 | 6.3 | 6.3 | 6.3 |
| `People1:0` | 2.6 | 2.6 | 7.2 | 4.1 | 4.1 |
| `People4:0` | 17.1 | 14.9 | 7.1 | 5.8 | 11.1 |
| `Chara2:2` | 19.4 | 13.6 | 4.2 | 3.8 | 5.2 |
| `BLObjs:2` (the chest) | 25.9 | 17.9 | 1.2 | 1.4 | 1.6 |
| worst character | 25.9 | 17.9 | 7.4 | 6.9 | 11.1 |
| sum, times events on the map | 195 | 152 | 74 | 70 | 77 |

* **M**: Chara4:1 alone; Chara2:4 with People1:0 and the timer; Crown3:1
  with People4:0; Chara2:2 with the chest. **N**: Crown3:1 alone, Chara4:1
  alone, Chara2:4 with People1:0, and People4:0, Chara2:2 and the chest
  together.
* Only changing the nearest to a hue-aware distance (second column) helps
  little: the lent palettes do not have the colours.
* **No split leaves everyone as they are**: the smallest worsening of any
  character among the 350 is +1.8 ΔE, Chara2:4's in N. M makes three characters
  slightly worse —Crown3:1's jacket and People1:0's shirt lose a shade—
  and gives back three that today are drawn with the wrong colours.

The side by sides —original, today, M, N— of the captures and of every
character are in the task's captures. Seen there, the M column is the only
one with no character in the wrong colours; whether Crown3:1's paler jacket
is noticed is for taro to say.

## A hypothesis for the algorithm

Not tried in the tools. What M has that today's split does not:

**No character is drawn with a palette that was not made with its colours
in it.** When the event characters do not fit exactly, today some get exact
palettes and the rest get someone else's; M instead groups characters that
look alike and quantizes each group together, so the loss is spread as a
shade here and there instead of concentrated as wrong colours in three
characters. Joint quantization would only happen in maps that today lend
something —31 of ABL's maps—; where everything fits, nothing changes.

Two smaller changes go in the same direction and could come first, each on
its own: count the lending cost over the poses the map shows and by
*how far* the pixels move, not how many; and draw a missing colour with
its nearest by a distance that sees hue.

Costs to measure before trying it: a character quantized differently from
another map goes with its own pose bank in the cartridge (today four of the
seven already do on map 38; M would add Crown3:1), and the order the split
serves characters in —leaders, weights— would have to keep meaning
something. Map 38 also has no room for the rain's colours today ("the
raindrops don't fit"), which this experiment did not look at.
