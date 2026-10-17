# More pictures at once

> **Measured on 2026-10-16** by Tijereta, over the dumps of the nine ports
> in the-advocate-ports `6d5c491` and their `Picture/` folders, with the
> tools of the-advocate `9407d385`. It is a snapshot: the numbers are from
> that day and this file is not updated. How to redo them is at the end, in
> "How it was measured". The task is
> [`zounds-pictures-and-the-picture-made-screens`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/zounds-pictures-and-the-picture-made-screens.md).

## Summary

* **Until that day the console kept two small pictures at a time**, one
  sprite palette each, every one cut in 32x32 objects, and a `MovePicture`
  changed only the tone and the transparency. Zounds builds its menu, its
  skill screen and a race's score board out of `ShowPicture`, and the
  converter left their third number on out.
* **One picture at a time is the usual; the screens made of pictures are
  four to fourteen**: Zounds' score board five, its menu four, its pick-axe
  screen fourteen; A Blurred Line's portable console eleven; Vampires
  Dawn's menus seven.
* **What held two was not the hardware's limit, but four of ours**: one
  palette per slot, sixteen tiles per object even for a 7x8 digit, the same
  file under two numbers converted twice, and one ramp for every picture.
  The hardware's limits —eight sprite palettes shared with the characters,
  512 object tiles, 128 objects, 32 per line— are what is left.
* **What was done** (taro: "if it comes out relatively cheap, let's try",
  2026-10-16): sixteen slots; pictures share a palette when their colours
  fit together —within two steps of 31 for the least used ones—, except a
  number the map tones; a sparse 32x32 block goes as 8x8 objects; the same
  pixels take their tiles once; a ramp per slot; and **moves that move**,
  as RM2k's do. Zounds' score board went from two numbers in 320 tiles to
  all five in 12.
* **What was not**: small pictures over a big one, and the pictures of
  the common events that are compiled once without a map. Both are dearer,
  and both are below with their cost.

## How many at once

A page or common event walked in order —following its `CallEvent`s,
ignoring branches—, a number added on `ShowPicture` and taken away on
`ErasePicture`. "Small" is what fits the plane of objects: 256x128 or less
on the console's screen.

    game              ShowPicture  most small ones up at once         maps with more than 2 small numbers
    abl                   348      3 on map 95; 11 in the console     1 (95)
                                   (common 39), never done
    book-of-three          11      1                                  0
    desert-nightmare     1249      1 (its many numbers are the        5, never more than 1 at once
                                   drawn-in masks, by number)
    dooms2                 27      1                                  0
    el-dorado             113      4 on maps 8 and 12                 2
    frozen-world           18      1                                  0
    sunset-over-imdahl   1143      4 in its menu (common 5)           0 (the rest are drawn into the map)
    vampires-dawn        4274      9 on maps 9, 94, 455; 7 in its     140 —112 of them show five faces
                                   menus (commons 25 to 28, 43, 44)   at transparency 100, never seen—
    zounds                266      5 on 75, 4 on 136 and 190;         3 (75, 136, 190)
                                   14 in PickAxe (common 21), 10 in
                                   Show Mining EXP (27), 9 in the
                                   notebook (29)

## Zounds' screens

* **Map 75**, the race's score: the digits `0` to `9` and `0Points`, 7x8
  and three colours in the file, placed by variables, under numbers 20 to
  24. Before: two numbers, 19 objects in 320 tiles. After: all five, 40
  objects in 12 tiles and one palette.
* **Map 136**, "Menu": a bar 320x15 that slides in from y=0 to y=8 while it
  appears, two faces 180x59 of 255 colours, an HP picture 28x20. Four at
  once. Before: the bar and one face, and the bar never seen, because it is
  shown at transparency 100 and its move was not done. After: the move is
  done, but the four take **512 tiles** —each face ten 32x32 objects, the
  bar eight— and the map's hero 64 more: the map fits no VRAM layout, and
  its pictures are left out as a whole.
* **Map 190**, the skill screen: `Zounds_SystemBox_Pic`, 320x240, under
  everything, the skill list 167x227 placed by variables, two selectors and
  a face. The box and the list are big pictures: the background layer holds
  one at a time and hides the small ones. After: the four small ones go in,
  but the screen does not show as RM2k's.
* **Common events 21, 27, 29 and 41** —the pick-axe, the mining
  experience, the notebook— are automatic or parallel: compiled once,
  without a map, and so without pictures.

## What limits it, one by one

* **Sprite palettes**: eight, shared with the map's characters, the timer,
  the raindrops and the battle animation's box. Three Zounds maps have none
  left for a picture. A picture that the map tones needs one of its own.
* **Object tiles**: the 512 the PPU names, shared with the characters; how
  many the map gets is its VRAM layout's. A 32x32 object takes sixteen
  whatever it draws.
* **Objects**: 128, and 32 on a line —34 slivers of eight pixels—. A
  picture as wide as the screen in 32x32 objects is eight; in 8x8 ones,
  thirty-two on each of its lines.
* **The background layer**: one big picture, and the map and the small
  ones go while it is up.
* **CPU and WRAM**: not what limits. A slot is some thirty bytes of far RAM
  with its ramp, and its frame is a few products and divisions when it
  moves.

## The options, with their cost

1. **More slots, palettes shared.** Cheap: the arrays grow, and the
   palette is the table's instead of the slot's. Done.
2. **Fewer tiles**: the same pixels once, and a sparse block as 8x8
   objects. Cheap: an object says its own tile and size. Done.
3. **Moves that move, and a ramp per slot.** Moderate: one more ramp per
   slot, the corner walked by Bresenham's steps. Done.
4. **Small pictures over a big one**: the background layer would have to
   leave the sprite VRAM and OAM alone, and two big ones at once —190's box
   and its list— need a second layer, or composing both into one when the
   cartridge is built, which only works if neither moves. Expensive.
5. **Pictures in the shared common events**: a cartridge-wide table whose
   tiles are uploaded when the picture is shown, with sprite VRAM reserved
   for them on every map that can run it. Expensive, and after 1 to 3 the
   biggest win: it is what Zounds' pick-axe and notebook, A Blurred Line's
   portable console and Vampires Dawn's menus ask for.
6. **Composing several pictures into one layer at run time**: per-pixel
   work on the CPU, and undoing it on erase. Not recommended, as in
   [The picture system and the portable console](2026-10-01-the-picture-system.md), option C.

## How it was measured

With throwaway Python scripts:

* **The commands**: each `data/maps/Map*.json` page and each common event
  of `data/db/commonevents.json`, walked in order, `CallEvent`s to common
  events followed six deep; codes 11110, 11120 and 11130, their parameters
  as in easyrpg-player's `CommandShowPicture`.
* **The sizes and colours**: each picture's file in the game's `Picture/`
  folder, with Pillow; the size on the console as RM2k's times 256/320 and
  224/240, unless it goes with the map.
* **Before and after**: Zounds' cartridge built with the tools of each
  side; the converter's log says, per map, how many pictures went in, in
  how many objects, tiles and palettes.
