# What turning toward the hero does not model

## What

Since 2026-09-11 the event the hero triggers **turns toward him**, like the
`SetFacing(GetDirectionToCharacter(GetPlayer()))` in
`Game_Event::ScheduleForegroundExecution`. The rules are in GIRO, in
`tools/port/eventos.py`, and in `turn_fire` in
`tools/runtime/turn_toward_hero.s`, both in snes-rm2k. What is left out:

* **Events that walk on their own do not turn.** Their own route is always
  running, and with a route running it decides where they face. In RM2k the
  running page **pauses** them —`SetPaused(true)`— and then they do turn;
  the pause is not modeled, so here they keep walking while they talk, which
  is the underlying debt. One that a scene already moved does turn: it keeps
  the route slot until the next map, but empty.
* **Another CharSet with the same pose.** If a refresh changes its page to
  one that draws another CharSet with the same direction and column, RM2k
  leaves it turned with the new drawing; here the turn is undone.
* **If the VRAM upload queue is full** on the frame of the trigger, the still
  event does not turn.

## Measured

The full queue does not happen in the game at that moment. `GangMember1` in
Lashe City was the one that showed the case of the already finished route:
until 2026-09-11 it never turned again.

Before turning, the event answered facing wherever it was facing, and before
that the page did not compile at all: on 2026-09-08 that cost **1572 action
pages in 1224 events on 220 maps**, half the game's NPCs mute.

## How it looks today

An NPC that walks on its own answers without turning around and without
stopping.
