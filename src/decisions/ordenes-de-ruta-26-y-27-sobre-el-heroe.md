# Move route commands 26 and 27 on the hero

## What

**Move route commands 26 and 27 on the hero —lock and unlock facing— are
accepted and dropped at compile time.**

## Why

Decided with taro on 2026-09-06: they are an extra, and the game can be
played without them. They are dropped **at compile time**, so they never
reach the cartridge and nothing is left half done.

Commands **28 and 29** —speed— are done, and with them the hero's step
stopped being fixed: it counts RM2k half units and **stays at the speed the
route left it at**, as in RM2k, which restores the frequency when the route
ends but not the speed.
