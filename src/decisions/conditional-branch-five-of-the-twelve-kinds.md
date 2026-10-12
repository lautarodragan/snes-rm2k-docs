# ConditionalBranch: five of the twelve kinds

## What

**`ConditionalBranch`: five of the twelve kinds.** Switch, variable, gold,
item and actor, and of the actor kind three of its seven questions —is in
the party, knows the skill, has the item equipped—.

## Why

The criterion with which they were added, from when only the switch kind
existed, and it still holds: **modelling a branch that nothing exercises is
inventing a difference**. With the switch kind alone, 21 of the 24 pages
the command unlocked got in, and the three missing ones asked whether the
hero was in the party, which without a variable party always gave the same
answer.

## How it compiles

To two opcodes: `OP_IF` —switch, polarity and target— and `OP_GOTO`, the
unconditional jump that goes where the `else` was. **The target is absolute
within the page**, so in the ROM jumping is assigning the cursor; which
target that is gets resolved by the converter, the only one that sees the
whole page, by emitting it blank and patching it when the branch closes.

Nesting comes from a stack and not from looking at the indentation the way
`SkipToNextConditional` does: it walks a flat list, while here the blocks
already come nested.
