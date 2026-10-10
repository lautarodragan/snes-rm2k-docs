# Graphics and sound, from RM2k to the SNES

> **Measured on 2026-09-07**, between commits `d3095de` and `de55cf7` of
> snes-rm2k, with `assets/medir.py`. The numbers are from that day and this
> file is not updated: the converter changed a lot since then. The script was
> deleted on 2026-09-19 in `17e8b79`; the last commit that has it is
> `5fadb64`.

Moving RM2k's graphics into a SNES cartridge is not mechanical, the way
dumping a `.lmu` to JSON is: you have to **choose** what goes in, with which
palette and shared with whom, and those decisions are made by measuring. This
is what came out of measuring.

`medir.py` measured by category —CharSets per frame, ChipSets by what is
used, whether one palette per chipset is enough, and the rest—. What the port
decided not to do based on these counts is in `workflow/divergencias/`.


## How to count without fooling yourself

Three ways to measure wrong, all three committed before arriving at the ones
here:

**The PNG's KB say nothing.** They are truecolor and compressed. `Panorama`
weighs 421 KB on disk and 759 in the cartridge, because the PNG compresses
what the ROM does not. The unit is the **8x8 tile at 4 bits**, 32 bytes,
which is what gets stored.

**The pixel is the wrong metric.** Counting how many pixels the 256 most used
colors cover gave 85%, and that sounds good; but a tile missing a single
color is not drawn worse, it is drawn **broken**. Counting *tiles that stay
whole*, those same 256 colors serve 40%.

**You have to count what the game uses, not what is in the folder.** RM2k
games drag along material nobody references —it was free— and measuring over
the files gives meaningless numbers: of the 456 characters in the CharSets,
the game uses 161; of the 12,096 object cells in the ChipSets, 3,232.

And the RTP has to be counted together with the game, not separately: eight
of the panoramas the maps ask for live there. Looking only at the game's
folder they came to 571 KB instead of 991.

And where you look for references also matters. Pictures are requested
mostly by **common events**: looking only at the maps gave 20 of 111 used,
and it is 97. Backdrops are not chosen by events but by **terrains**.


## What the console gives away

Two deduplications that cost nothing because the hardware already does them:

* **Mirroring.** The horizontal flip bit is in the tilemap and in OAM, so a
  tile and its reflection are the same tile. The walking animations to the
  left and to the right are the same one.
* **Palette.** The palette number is another field, so two identical drawings
  with different colors share their tiles. **A recolor does not cost a byte of
  graphics.**

And a third one that shows up on its own: an RM2k **autotile** is not a cell
of the image but a *combination of edges* that the engine builds from a small
block, and each block generates up to 50 combinations. On the SNES the
tilemap does that composition for free, pointing four cells at quarters that
already exist. Measured:

    autotiles    3460 ids -> 1936 8x8 tiles = 0.56 per id
    lower layer  1620 ids -> 3619           = 2.23
    upper layer  1612 ids -> 3801           = 2.36

Four per id would be sharing nothing.


## How much the game weighs

    map grids            818 KB    2 bytes per cell, 418,635 cells
    sprites              450 KB    1201 distinct frames
    collision            409 KB    1 byte per cell
    background tiles     287 KB    9199 8x8 tiles, shared between chipsets
    block tables        ~152 KB    scaled from map 1
    music               ~860 KB    estimated, 43 themes
    ------------------
    total              ~2.9 MB     and a LoROM cartridge goes up to 4

The art nobody draws yet, and that is needed for the game to be the game
—taro was explicit: without battles the project makes no sense—:

    Panorama   991 KB   the 19 the maps ask for, of 27
    Picture    604 KB   the 97 referenced, of 112
    Backdrop   494 KB   the 21 the terrains name, of 70
    Monster    301 KB   not filtered by use
    Battle     218 KB   not filtered
    FaceSet    168 KB   not filtered
    ------------------
    art       2.7 MB    (the last three are an upper bound)

Added up, ~5.6 MB against a ceiling of 4. **Compressing is not the condition
for the game to fit; it is what makes room for the art.**


## The palette, which is the real problem

Deduplicating tiles between maps only helps if the palettes match. Today the
converter quantizes **per map**, so two maps that share a chipset get
different palettes and the same drawing ends up as different bytes.
Deduplication is not a packing problem: it is a palette problem in disguise.

**And this is no longer a claim, it is a measurement.** The converter shares
identical blocks since 2026-09-07 —see `Materiales`—, and over the maps of
`demo-apertura` that saves **0.1 KB, all of it empty blocks**. Taking instead
six maps that use the same chipset, number 23:

    maps 4 and 5   2 tiles equal byte for byte, of 150 -> 122 equal as drawings
    maps 2 and 4   2 of 139                            ->  91
    maps 2 and 5   2 of 139                            ->  95
    maps 3 and 4   1 of 150                            ->  83

That is, the drawing is shared up to 80% and the bytes are never shared. What
separates one column from the other is exactly the palette.

When measuring it there is a trap that bit along the way: the console's
tiles are **planar**, four pairs of bit planes interleaved per row.
Renumbering their bytes to compare drawings without a palette does not
compare drawings —it is the same mistake `canonico` documents— and gave 11
shared tiles where there are 122. You have to decode to pixels first.

But the **global** palette was the wrong question. CGRAM is reloaded when the
map changes, and tiles only need to be shared between maps of the same
chipset. Measured per chipset, over the ids each one actually uses:

    the smallest 17 colors, median 65, the largest 206
    fit in the background layer's 111:   33 of 42
    fit in 256:                          42 of 42
    taking the whole chipset:             9 of 42

The last row is the one that shows why filtering by use is not a detail of
the measurement but the condition for the idea to work.

**The price is not bytes.** One palette per chipset is more demanding than
one per map, because a map uses a subset of the chipset: a map that today fits
comfortably with 63 colors would go on to share one of 150, and it is going to
look **worse than today**. That is the real cost of deduplicating, and it is
artistic.


## The message window was charging the background half of CGRAM

The background's budget was not 111 colors: it was **47**, and not for lack
of room. BG1 runs at 8 bits per pixel and **addresses CGRAM directly**, so it
does not need 16-color palettes; it only needs nobody to step on its entries.
But it was given the block that lay *below* the message window's palette, and
that palette was one for the whole ROM: the lowest of the upper layers of all
its maps. In the opening ROM that put it at 3, and so:

    0        screen background color
    1..47    BG1  <- the only thing it was given
    48..63   the window
    64..111  palettes 4, 5 and 6: **nobody used them**
    112..127 the upper layer

In map 7 there were **57 entries thrown away** while the background merged 13
of its 60 colors. The nine PoC maps merged 97 colors among all of them.

The solution is to move the window to **palette 0**, at the very bottom. It
takes nine entries —the background color plus its eight colors— and the
background stays contiguous from 9 up to wherever its own upper layer starts,
without depending on what the other maps need. Measured on `demo-apertura`:

    budget per map         47 -> 55, 71, 87 or 103 depending on the map
    merged colors          97 -> 0

And a property that comes for free: the screen tint walks CGRAM from where
the background starts, so the window stays out of range **without anybody
having to remember it**. In RM2k the tone applies to the map and not to the
window.

Doing it there was a counting error the test suite caught: the window's
colors were counted with `sum(1 for w in cram if w)` and came to seven, but
they are **eight** —one is pure black and its CGRAM word is zero—. With seven
reserved, the text was drawn with a color nobody had uploaded: 79 pixels in
the text rows. Now `convert_ventana` looks at the highest index the window
actually uses and stops if it does not fit.


## Sprites have their own problem, and it is harder

Everything above is about backgrounds. The **sprite** palettes are another
eight —seven with the timer on— and there is no slack there: every RM2k
character this game uses takes **all 15 colors** after quantizing. Map 8,
which is the street Talan's pad opens onto, draws ten characters and there is
no lossless split; up to five palettes were tried and there is none.

And merging is expensive. The cheapest pair of those ten —`Chara2:0` with
`People1:0`— moves **920 of 5276 pixels, 17.4%**, with a jump of 18 out of
31 in one channel; the worst pair reaches 47%. It is not that the heuristic
is weak: `merge_least_used` already merges the least used color with its
nearest neighbor by luma, and the big jump comes from chaining merges.

What is cheap is not drawing. Four of those ten appear in **a single page of
a single event** —`Future1:6`, `People1:0`, `People4:0` and `savept:0`— and
the last one is a save point, which this port does not have. Removing two
fits in the eight without touching anybody's pixel, and the converter already
knows not to draw an event whose graphic does not fit: today it stops with an
error instead of choosing.


## Sharing tiles between maps: VRAM is not enough

Measured on 2026-09-07, after moving the window to palette 0. With the new
budget, two maps of the same chipset sharing a background palette is **almost
free**:

    chipset 1  maps 4,5   union 67 colors in 103  -> merges 0
    chipset 9  maps 7,8   union 77 in 103         -> merges 0
    chipset 6  maps 1,2   union 64 in  55         -> merges 9, and that is
                                                     41 pixels of 5,120,000

But sharing **tiles** asks for more than the palette: it asks for a single
pool, because the ROM uploads a map's tile block with one contiguous DMA. And
that pool is uploaded whole on every map:

    shared pool of maps 1 and 2            437 background tiles
    map 2 also spends                      283 sprite tiles

    split with window          background 384, sprite 448   ->  437 > 384
    alternative split          background 480, sprite 256   ->  283 > 256

It fits in neither. So the 14 KB saving of the 1–2 pair is real in the
cartridge and **unrealizable on the console**: VRAM blocks it, not the
palettes. The message window already takes 8 KB of tiles plus 2 of tilemap,
and what is left has to be split between background and sprites.

What did stay from the palette work is the quality half, which was the
bigger one: the nine PoC maps went from merging 97 colors to merging 8, and
it shows —Core's blood on the floor of map 2 was brown and now it is red—.


## What came next

1. ~~**The palette strategy.**~~ Half done and with an unexpected ending: the
   quality half paid off a lot —97 merged colors down to 8— and the
   byte-saving one is **blocked by VRAM**, not by the palettes. See above.
   What is still alive in this item is only if more VRAM shows up: which
   palettes to build and how to assign them, looking statically at which
   combinations CharSets appear in with ChipSets and CharSets with each
   other. A sprite and the background it walks on share the screen, so they
   share CGRAM. A hypothesis of taro's worth measuring first: all of Lashe
   City shares a style and looks like the main sprites, so it should simplify
   a lot.

2. ~~**Separating the maps' material in the converter.**~~ Done on
   2026-09-07: blocks go through `Materiales`, have their own name, and the
   map stores which one it points to; identical ones are emitted once. What
   became clear doing it is that the separation saves nothing by itself
   —0.1 KB— and that item 1 is the one with all the savings inside. See
   above.

3. **A static-analysis spike to discard whole maps.** Not by interpreting
   every possible state, which is not practical, but the other way around:
   choosing candidate maps and tracing their references until reaching "to
   see this you need such an item or such a hero". taro's memory helps as a
   heuristic. His own intuition says it may change nothing: the discardable
   maps are probably test maps and use tilesets that are already in use.

4. **Compressing the grid**, which is the heaviest category. taro went
   through the whole game in the editor and knows there is a lot of waste:
   the largest maps —the car escape one, for example— use twenty or thirty
   tiles of the chipset, in large rectangular areas with repetitive patterns
   and a lot of unused space.

And a limit that applies to everything above: **this is static analysis**. It
says what is referenced, not what is seen while playing. A common event can
ask for a picture and never be reachable. The way out is not more analysis
but playing with a visible sentinel in place of the graphic, and noting where
it appears; that also finds the opposite, which no static filter sees: a
`ShowPicture` with the name built in a variable.


## The horizon

taro's idea is for this to end up general: a `migrar-rm2k-a-snes juego.zip
juego.sfc` that works without tweaking knobs for each game. Nothing measured
here is specific to *A Blurred Line* except the numbers: that CharSets carry
eight characters, that autotiles expand, that material is left over because
in 1999 leftovers were free, holds for any RM2k game.
