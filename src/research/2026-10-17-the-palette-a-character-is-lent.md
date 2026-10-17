# The palette a character is lent

*2026-10-17. Measured on the-advocate `b15c9408` (main, with the change
below on branch `carpintero-lending`) and the-advocate-ports `bd92975`,
every game of the ports. It is a snapshot: it is not updated.*

When a map has more characters than its eight object palettes hold, the
ones that fit in none are drawn with someone else's palette —see [Every
event is drawn](../decisions/every-event-is-drawn.md)—. [The chests'
colours](../ports/abl/research/2026-10-16-the-chests-colours.md) found, on
A Blurred Line's map 38, a chest of greys drawn golden that way, and two
ways the choice was worse than it had to be. This measures them over every
game, each on its own and together, and what a third would cost.

## The three steps

1. **The nearest colour sees hue.** A colour missing from the palette went
   to its nearest by the luma distance —the channels weighted 30/59/11, as
   the merges weigh them—, which barely sees blue: to it an olive of nearly
   a grey's light is nearer than a grey a little darker. Now the nearest is
   measured in CIE Lab (`lab_distance` in Adeleine, in integer tenths).
2. **The palette lent is the one the character is drawn nearest with.** It
   was the one that missed the fewest pixels, counted over the twelve poses
   of the character's block —other objects the map never shows, for the
   chest—, however near or far each went, and decided with the palettes as
   they were when the character's turn came. Now it is each pixel of the
   poses the map shows times how far its colour lands, decided at the end,
   with every palette whole.
3. **Group similar characters and quantise each group together**, so that
   nobody is drawn with a palette not made with its colours. Measured as a
   cost only, not implemented.

## How it was measured

Every game's cartridges were built once with a shim that kept each request
the converter makes to Wally; each variant of Wally then ran over the same
requests, with a throwaway patch that writes, for each character the map
draws with a palette of the map's (not the leaders' own colours), every
pixel of the poses the map shows against the sheet at 15 bits.

* **Per character**: the mean colour difference per pixel, in CIE76 (ΔE*ab,
  as on map 38) and in CIEDE2000. CIEDE2000 is the judge that matters: step
  1 measures in Lab, and CIE76 *is* Lab, so it would judge itself.
* **Per map**: the worst character, and the sum over its characters.
* **Better / worse**: a map whose sum moved by more than 0.05.
  **Noticeably worse**: a character that got worse by more than 2.3 in
  CIE76 or 1.0 in CIEDE2000, about one just-noticeable difference.

196 maps lend a palette, 197 instances (ABL's map 11 is converted twice,
lending differently): A Blurred Line 30, The Book of Three 3, Desert
Nightmare 42, Dooms 2 3, El Dorado 10, Frozen World 14, Sunset over Imdahl
11, Vampires Dawn 70, Zounds 13. **No map that does not lend changed**, in
any variant.

## Each step, and both

| | better / worse / same | sum of the totals | sum of the worst | characters noticeably worse |
|---|---|---|---|---|
| CIE76, step 2 | 143 / 14 / 40 | −21% | −24% | 28, on 24 maps |
| CIE76, step 1 | 187 / 1 / 9 | −11% | −13% | 0 |
| CIE76, both | 190 / 1 / 6 | −31% | −38% | 0 |
| CIEDE2000, step 2 | 135 / 22 / 40 | −18% | −23% | 56, on 38 maps |
| CIEDE2000, step 1 | 149 / 35 / 13 | −4% | −3% | 74, on 36 maps |
| **CIEDE2000, both** | **176 / 15 / 6** | **−23%** | **−30%** | **35, on 22 maps** |

Per game, both steps, in CIEDE2000 (better / worse / same): A Blurred Line
25/3/3, The Book of Three 3/0/0, Desert Nightmare 37/3/2, Dooms 2 2/1/0, El
Dorado 9/1/0, Frozen World 14/0/0, Sunset 11/0/0, Vampires Dawn 63/6/1,
Zounds 12/1/0.

**What gets worse, with both**: no map gets worse by more than 1.7 in its
CIEDE2000 sum (Zounds' 130, El Dorado's 3, Vampires Dawn's 364, 298 and
401, ABL's 11). The worst characters: Vampires Dawn's 221 `sozai00:1`
(12.1 → 15.4), its 282 a tile (8.2 → 11.4), ABL's 318 `People5:5`
(14.9 → 18.0), and five tiles of Vampires Dawn's 167 (about +2.8 each).
They are where Lab and CIEDE2000 disagree on which colour is nearer, and
the numbers alone do not say it is worse to the eye: `sozai00:1`, the worst
of all by CIEDE2000, was drawn with a black dress and peach hair and is
drawn now with a blue dress and blond hair, as on its sheet, only a
brighter blue.

**What gets better**, the most: Vampires Dawn's 6, 166, 239, 95, 167 and
Desert Nightmare's 48, where whole patches of foliage drawn with the
greens of another palette turned blue, white or grey, and are green again
(side by sides below). On map 38 of A Blurred Line the chest goes from
25.9 to 9.1 (CIE76), the olive-haired woman (`People4:0`) from 17.1 to
14.6 and the three black-haired kids (`Chara2:2`) from 19.0 to 13.7, and
nobody else moves. The by-hand distribution M of the chests' research
reached 1.4 for the chest, at the cost of three characters that are not
lent: that is step 3's ground.

Step 1 alone barely moves the sum in CIEDE2000, and one map in six gets worse:
it pays only with step 2, which chooses the palette with the same
distance it is drawn with.

## The variants that lost

Measured the same way the same morning, on the main before Calandria's
change of still pages (`48362b6b`, 205 instances), all with step 2,
judged in CIEDE2000; the chosen pair gave 182 / 17 / 6 and −21% there:

* **The cost squared** (pixels × the squared distance, as a merge counts
  it), with the nearest in Oklab: 143 / 50 / 12, −16%, 134 characters
  noticeably worse on 71 maps. The square prefers a palette that draws
  every pixel a little off to one that draws a few far, and more
  characters came out worse.
* **The cost linear, the nearest in Oklab**: 157 / 33 / 15, −17%, 88
  characters on 50 maps. Oklab is newer and meant to be more even than
  Lab, but as the nearest of a lent colour it lost to Lab on every count.
* **Step 2 with the luma distance, squared**: 132 / 40 / 33.

## Step 3: what it would cost

Not implemented. The model: each palette that hosts a lent character is
quantised instead with all its characters together —their own colours,
weighted by the pixels the map shows— down to its fifteen entries, less
those the timer holds. A character that changes pose carries its twelve
poses in the cartridge with its palette's indices, so a member whose
colours move gets a bank of its own on that map; the cartridge stores
each pose once, so what it adds is the poses another map also uses. Lower
bound: only members whose colours move; upper: every member with a bank.

| game | maps | new pose banks | per map (mean, max) | ROM added |
|---|---|---|---|---|
| A Blurred Line | 30 | 31–37 | 1.0–1.2, 5 (map 3) | 156–174 KB |
| The Book of Three | 3 | 3 | 1.0, 2 | 6 KB |
| Desert Nightmare | 42 | 90–98 | 2.1–2.3, 5 | 336–378 KB |
| Dooms 2 | 3 | 5 | 1.7, 2 | 12 KB |
| El Dorado | 10 | 31–39 | 3.1–3.9, 9 | 110–121 KB |
| Frozen World | 14 | 27–51 | 1.9–3.6, 13 | 84–166 KB |
| Sunset over Imdahl | 11 | 33 | 3.0, 7 | 104 KB |
| Vampires Dawn | 70 | 191–214 | 2.7–3.1, 31 (map 95) | 508–598 KB |
| Zounds | 13 | 37–42 | 2.8–3.2, 12 | 88–112 KB |
| all | 196 | 448–522 | | 1.4–1.6 MB |

**Whether it fits**: A Blurred Line's `release`, with steps 1 and 2, has 7
halves of bank free and 5 KB of gaps, about 229 KB: step 3 fits, with
55–70 KB left. Vampires Dawn has no free bank: its half megabyte would go
to the `.msu`. Every other game has two dozen free banks or more. And it
is a model: a real grouping would also move characters that today share no
palette with a guest —as M did on map 38—, so its cost is above this.

What it buys is not measured here. On map 38 it was the chest at 1.4
against 9.1, and three characters a shade worse that today are exact.

## Where to look

The side by sides —the sheet at 15 bits, main, step 2, step 1, both, each
with its CIE76 mean—, for the maps that change the most and those that
get worse, and ABL's goldens that moved, before, after and difference, are
in the captures taro was given for this; the task is
[`abl-chests-change-colour-from-map-to-map`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/abl-chests-change-colour-from-map-to-map.md).
