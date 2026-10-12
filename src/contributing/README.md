# Contributing

The project lives in four repositories:

- **the-advocate**: the tools and the runtime. The converter and its stages,
  the 65816 engine in `runtime/`, their tests, and the libraries that
  know only one side —the console's formats, or RPG Maker's—. The tools are
  installed on the PATH and know nothing about any particular game.
- **the-advocate-ports**: the ported games, one directory per game. Each one
  is a whole project —its `rm2k-snes.toml`, its `justfile`, its `data/`—;
  see [Ports](../ports/README.md). A Blurred Line's directory also holds the
  test suite and its goldens, which for now are almost all the ROM tests of
  the engine; the root has the few that run the other games (see
  [How it is tested](../testing.md#the-other-games)).
- **the-advocate-docs**: this book.
- **the-advocate-work**: where the work stands —the tasks— for all the
  repositories, and the instructions for working on them. Every task is
  one file, `tasks/<name>.md`, with its state in its front matter, and
  **its name never changes**: this book cites a task with a link to it
  there, and the link does not go stale when the task moves on.

The commit messages are long on purpose: in all four, `git log` is the
record of why things are the way they are.

**The pages had Spanish file names until 2026-10-12**, and the commits,
the tasks and the comments written before that day cite them. The table
`[output.html.redirect]` in `book.toml`, at the root of this repository,
has one line per renamed page —its old path from the book's root, and its
new name—: an old URL lands on the new page through it, and it is where an
old citation is looked up. A page renamed again gets its line there, and
the lines that pointed at its old name are updated to the new one.

- [JetBrains](jetbrains.md): what to configure in the IDE so that annotate
  sees through the split of `main.s`.
