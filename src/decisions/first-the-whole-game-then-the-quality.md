# First the whole game, then the quality

## What

**Until the whole game can be played, unblocking a part is worth more than
its quality.** When something doesn't fit —a track, a sound effect, a
graphic—, it goes in with whatever quality it takes in the ROM, and with
the highest possible in the `.msu`. And **breaking saved-game
compatibility is never a problem**: nothing is kept between cartridges.

## Why

From taro, on 2026-09-30, about the radio music in the troop pages (its
three tracks in the battle package lower the sample rate of the battle
track) and common event 35 (`ResetAfterBattles`), whose variables had no
slot in the save: *"When we finish implementing everything and the whole
game is playable we can tighten screws as far as graphics and sound
quality go"*, and *"I'll always accept breaking saves"*.

## How it applies

- If the simple way to unblock something is to lower the quality of
  something else —the battle track, for example—, it is done that way, and
  the quality is noted as debt in the task.
- If separating the ROM's quality from the `.msu`'s is just as cheap, they
  are separated: the ROM goes down, the `.msu` doesn't.
- A change in the save format isn't avoided or versioned: it is made.

It doesn't contradict taro choosing by ear when quality is the question
—as with the `.msu` sound effects—: that still holds when it doesn't block
anything.
