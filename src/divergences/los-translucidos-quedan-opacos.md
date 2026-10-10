# Translucent events end up opaque

## What

RM2k's "Trans" draws the event at 160 out of 255 over whatever is behind it.
Here that blend is computed at conversion time and is **baked** into the
graphic, which is exact in a still picture and opaque in motion. Why it can
be done is in
[Translucent events are baked](../decisions/los-translucidos-van-horneados.md).

What is lost:

* **Nobody shows through from behind**, neither the hero nor another event.
* **If there is an animated tile behind it, the blend is right for one frame
  only.**
* **Two events with the same CharSet over different backgrounds are two
  graphics**, and therefore two palettes.

## Measured

On 2026-09-12, over the 39 bakeable pages of the 35 maps with translucent
events:

* four overlap another event's sprite —maps 74, 152 and 305—, and there the
  blend is against the floor and not against the neighbor;
* two are over water —the save points on maps 59 and 178—, which inside the
  sprite's 24x32 cell stays still;
* only three maps change palettes and **none fails**: 9 goes from seven to
  eight, 117 from six to seven, and 37 adds a graphic with someone else's
  palette.

## How it looks today

A fire over a barrel or a save point look the same as in RM2k. The
translucent Kersh on map 305, which overlaps a Guard, covers him.

## When it stops being enough

A translucent event that walks, or one standing over something that moves.
In this game there are none; in another, the way out is color math.
