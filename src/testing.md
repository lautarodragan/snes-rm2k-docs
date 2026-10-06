# How it is tested

Nothing is considered right because it looks right. A test builds a
cartridge, runs it in an emulator, and **compares the screen pixel by
pixel at 15 bits**, which is the console's real color depth, against a
frozen capture (a *golden*).

Three rules come with that:

- **Changing a golden is deliberate.** It goes into version control, it is
  looked at, and the commit says why the picture changed.
- **A golden catches regressions, not birth defects.** A feature that is
  wrong from day one bakes its bug into its golden. What balances that is
  someone actually playing the game.
- **Two emulators, compared to each other.** One of them starts with
  garbage in work RAM and the other with zeros, so a difference between
  them means the ROM reads memory it never wrote.
