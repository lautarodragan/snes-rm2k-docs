# The shop's party window, and the gold on the message's line

## What

When buying, RM2k's shop, `Scene_Shop`, has a right-hand column of three
windows: the party (`Window_ShopParty`, 136x48), "Owned Items" and
"Equipped Items" with their counts, and the gold. The party window shows
each member's CharSet facing down and walking —frames 0, 1, 2, 1, twelve
frames each—, still and in grey whoever cannot equip the item the cursor
marks, and next to each one one of the System's four arrows, 8x8 in four
frames: it raises their parameters, it leaves them as they are, it lowers
them, or they already have it on. Since 2026-10-15 the ROM draws that
window the same way, pixel for pixel —the CharSet frames, the grey, the
arrows and their place, measured against the original under Wine—, for
any game. Until that day it did not have it.

What is still different:

* **The column is laid out differently.** At 256x224 the buy list runs
  across the screen and the column goes below it, as it already did: the
  counts' window, now 120 wide, on the left, and the party's, RM2k's 136,
  on the right. **The gold moved to the right end of the message window**,
  whose line in every mode that shows the party is a short one ("What do
  you want to buy?", "How Many", "Done"). The list keeps its five rows.
* **A `ChangeSpriteAssociation` is not followed**: every member is drawn
  with the database's CharSet. The graphic that command gives an actor is
  kept as an index into the current map's table of graphics, not the
  cartridge's, and the shop carries each possible member's database
  CharSet only.
* **A two-weapon actor is not greyed out for a shield.** RM2k's
  `IsEquippable` refuses shields to actors with `two_weapon`; the cartridge
  carries no table that says which actors those are.
* **A member can step a frame or two late after a key.** The new frame of
  each member is uploaded to video memory only when the vblank has room
  for it after the text, and the frames right after a key are the ones
  where the text takes the whole vblank. A capture can catch two members
  on different frames for a moment; it does not show while playing.
* **A System whose windows fill the shop's tile bank leaves no room for
  the party**: then the shop shows no party, and the converter says so as
  the degradation `shop-party-no-room`. A Blurred Line's leaves room.

## Why

The list's five rows are what the 2026-09-28 layout fought for, and the
party window had no place in it without taking rows from the list. Three
ways of making room were drawn as mockups —the party where the gold was
and the gold to the message's line; the list down to four rows and a band
of its own for the party; the party squeezed into the gold's 104 pixels,
each arrow over the next member— and the first one kept the list whole,
kept RM2k's window as it is, and moved only the gold, to a window that had
room on its right. The task
[`party-in-the-shop`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/party-in-the-shop.md)
has the mockups and the captures.

## How it applies

The geometry is `TI_*` in `layout.rs` of `rm2k-snes-screens` in
the-advocate, and the party's conversion, its rule (`CmpEquip`) and its
reference drawing are `party.rs` there. The members and the arrows are
8x8 objects whose tiles go right after the shop's windows, in the BG1 bank
the map's load restores, and each member's slot holds the frame it shows:
see `runtime/shop_party.s`. The converter checks that the gold does not
run into a buy message and that the counts' terms fit their 120 pixels,
and says it as the degradation `shop-crowded` when they do not.
