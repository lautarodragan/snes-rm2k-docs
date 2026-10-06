# The tools

The tools are a Cargo workspace, in three layers. Each layer only depends
on the ones below it:

| Layer | Knows about | Examples |
|---|---|---|
| `snes/` | the console's formats, nothing of RPG Maker | Adeleine (colors and palettes), Voodoo (images to tiles), Gunter (BRR samples), LZ2 compression, Goombario (a 65816 linter) |
| `rm2k/` | RPG Maker 2000's formats, nothing of the console | Ditto (reads and writes the formats), the rules of the format (passability, pages, experience), a renderer |
| `rm2k-snes/` | both | the event compiler, Wally (maps), battle, screens, images, audio, the cartridge builder, the converter |

Two of them make decisions that are easy to misplace:

- **Adeleine decides which colors are lost** and how the rest are grouped
  into palettes. Voodoo only converts an image that already fits, and
  refuses one that doesn't. The test for which side something belongs to:
  does it change a pixel of what is seen?
- **The event compiler** turns RPG Maker's event pages into a bytecode the
  runtime interprets. A page that uses something the console can't do is
  either compiled without that detail —declared as debt— or left out, and
  a report says which commands keep which pages out.

The tools are installed on the PATH, like any other program; a game's
build never calls `cargo`.
