# A door to the same map doesn't reload the map

## What

**A door to the same map doesn't reload the map.**

## Why

Reloading reads the event positions from the cartridge again, and that
loses whatever moved them even though the player never left. It is the
`map_changed` of `Game_Player::PerformTeleport`.

Guarded by `test_same_door.py` in the ABL port (the-advocate-ports/abl).
