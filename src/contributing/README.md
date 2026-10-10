# Contributing

The project lives in four repositories:

- **snes-rm2k**: the tools and the runtime. The converter and its stages,
  the 65816 engine in `tools/runtime/`, their tests, and the libraries that
  know only one side —the console's formats, or RPG Maker's—. The tools are
  installed on the PATH and know nothing about any particular game.
- **snes-rm2k-ports**: the ported games, one directory per game. Each one
  is a whole project —its `rm2k-snes.toml`, its `justfile`, its `data/`—;
  see [Ports](../ports/README.md). A Blurred Line's directory also holds the
  test suite and its goldens, which for now are the only ROM tests of the
  engine.
- **snes-rm2k-docs**: this book.
- **snes-rm2k-work**: where the work stands —the tasks, the decisions and
  the divergences from RM2k— for all the repositories, and the
  instructions for working on them.

The commit messages are long on purpose: in all four, `git log` is the
record of why things are the way they are.

- [JetBrains](jetbrains.md): what to configure in the IDE so that annotate
  sees through the split of `main.s`.
