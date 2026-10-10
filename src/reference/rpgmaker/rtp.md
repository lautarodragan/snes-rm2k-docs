# The RTP

An RM2k game uses resources that don't come with it: those of the **RTP**,
the package of ChipSets, CharSets, music and sound effects that the editor
installs next to it. The tools look for it wherever `--rtp-dir` says, after
the game, and bring none: the RTP is not ours to redistribute.

**Which RTP depends on the game, because the names change.** Games made
outside Japan with Don Miguel's translation (June 2000) use his, which
brings files he added that don't exist in the Japanese one —`Future1-3`,
for example—. **EasyRPG's free replacement** has different art and other
names (`Actor1-4` instead of `Chara1-4`): it is no good for a game made
with Don Miguel's, but it is for one made for it, and its license, file by
file, is CC0 or CC-BY 4.0 —see [the test
game](../../research/2026-10-02-el-juego-de-pruebas.md)—.

Don Miguel's is extracted from `RTPE.EXE`, which is a RAR self-extractor:

```sh
7z x -oRTP-tmp RTPE.EXE && mv RTP-tmp/Data/RTP <destination> && rm -rf RTP-tmp
```

What A Blurred Line uses from it: in [its RTP page](../../ports/abl/rtp.md).
