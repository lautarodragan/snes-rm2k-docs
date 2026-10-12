# The action key looks at both cells

## What

**The action key looks at both cells, and each one asks for the opposite
layer.** `CheckEventTriggerHere` wants `GetLayer() != Layers_same` and
`CheckEventTriggerThere` wants `== Layers_same`.

## Why

It isn't symmetry for decoration: an event on the hero's layer blocks the
way, so the hero could never stand on top of it; one on another layer
doesn't stop them, and they walk over it.

The filter **lives in the ROM and not in the converter**, because the same
page counts or not depending on which cell is looking at it.
