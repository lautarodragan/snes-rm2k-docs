# The engine against RPG Maker 2000

**[Open the board](engine-vs-rm2k/index.html)**

The board lists everything RPG Maker 2000 has —the event commands of its
three tabs, the conditions of `ConditionalBranch` and the route commands,
the tabs of the database, the asset folders of a game, the map and its
events, and every screen— and says, for each one, what state it is in in
the port:

- **done**: as in RM2k;
- **partial**: it works, with differences —almost always a missing
  variant, like an actor chosen by a variable—;
- **patch**: it works only with a patch from the game;
- **degrades**: it is lost and the game goes on;
- **missing**: a page that uses it is left out of the cartridge;
- **n/a**: it makes no sense on the console.

It measures **what exists, not bugs**: a command marked done can still
have a bug, and the board won't show it. That is what the tests are for.
The page counts in its notes —how many pages each gap leaves out— come
from `rm2k-snes-events culprits`, run over the eight RM2k games the tools
are measured against.

It is **a snapshot**, taken on 2026-10-06 at commit `3d0c787c` of
snes-rm2k, and says so at the top. It isn't kept up to date by hand: when
it gets old, it is redone from a newer commit, not edited. Its notes point
to the divergences and decisions behind each
item, and to the code and the tasks of that day.

The board is a page of its own, outside the book's theme, so it keeps its
layout and its filters: the legend's chips hide and show each state, and
each row opens into its items.
