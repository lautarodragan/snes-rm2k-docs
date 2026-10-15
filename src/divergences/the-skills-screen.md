# The skills screen: eight rows and two lines of description

## What

The pause menu's skills screen —Tech Skill in A Blurred Line, Skill or
Special in other games— shows **eight rows** of two columns and the
description of the skill under the cursor **in two lines**, where RM2k shows
ten rows and one line. The rest is RM2k's `Scene_Skill`: the help window on
top, the status line below it —name, level, condition, HP and SP with their
maximums, the terms in the System's colour 1—, and the list in the actor's
order, in grey what the map cannot use or the SP do not cover, scrolling one
row at a time when the cursor leaves it.

Smaller things that go with it:

* **Names are cut** at eleven cells, as in the battle's list; RM2k lets a
  long name run into its cost ("Field/Battery Repair- 0").
* **The cost has two places**, as in the battle: no cost the cartridge
  carries reaches 100 (see the draft
  [`skills-that-cost-100-or-more-are-left-out`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/skills-that-cost-100-or-more-are-left-out.md)).
* **The actor's name is cut at six cells** in the status line, which is
  what leaves room for the SP's maximum before the frame.
* **There are no scroll arrows**: RM2k draws a small arrow on the edge of
  the list when there is more above or below.
* **The condition always reads the normal one**: outside battle this port
  keeps no states, so an actor is either standing or at 0 HP, and one at 0
  HP cannot open its list.
* **Teleport and escape skills are always grey**: whether RM2k allows them
  depends on the map and on what the game permitted, which this port
  tracks since 2026-10-15 but does not consult here (see
  [What a map's permissions do not model](what-a-maps-permissions-do-not-model.md)).
  No game it was measured on teaches one.

## Why

RM2k draws at 320x240 with a six-pixel font; the console has 256x224 and
the port's text is about the same size in a smaller screen. A third of A
Blurred Line's skill descriptions are wider than a line, so one line would
cut them, as the battle's help window does today. Two lines and eight rows
fill the 224 lines exactly: a help window of 48, a status window of 32 and
a list of 144. Measured in the research
[The skills menu](../research/2026-10-12-the-skills-menu.md).

## How it applies

The geometry is `SK_*` in `layout.rs` of `rm2k-snes-screens` in
the-advocate, and the screen is `runtime/skills_screen.s`. The two lines are
slices of the one description the cartridge carries for the battle, cut at a
space where they fit (`description_spans` in `texts.rs`). The task is
[`the-skills-screen`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-skills-screen.md).
