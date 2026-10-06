# Introduction

This project takes a game made with **RPG Maker 2000** and turns it into a
**Super Nintendo** cartridge: a ROM that runs on the real console, not an
emulator of RPG Maker inside one.

It has two halves:

- **The tools**, which run on a computer. They read the RPG Maker project
  —its maps, its database, its event pages, its pictures and its music— and
  decide how each thing fits the console.
- **The runtime**, an engine written in 65816 assembly, which runs on the
  console and plays what the tools produced: it walks the hero around the
  map, runs the event pages, draws the windows and fights the battles.

## RPG Maker 2000 PLUS

The goal is to be compatible with RPG Maker 2000: a game should not need
changes to be ported. Whatever the engine adds on top —a custom menu, a
battle option the original never had— is available to *any* game, and
never breaks the ones that don't use it.

## Where it came from

The project was born porting one game, *A Blurred Line*, and grew into
general tools. Today it is being measured against other RPG Maker 2000
games as well, to find out what it takes for each of them to be playable.

## When something doesn't fit

The console is far smaller than a PC running RPG Maker: 64 KB of video
memory, 128 sprites, 15 colors per sprite palette. When a game asks for
more than the console has, the tools prefer to **degrade gracefully** —drop
a detail, warn about it, and keep going— over refusing to build. A game
that runs with a missing effect can be played and measured; one that does
not build can't.
