# A Blurred Line's RTP

ABL uses resources that don't come with the game: 5 chipsets (`ChipSet1/2/3`,
`Basis`, `Inner`) and 17 charsets (`Chara1-4`, `Crown*`, `Future1-3`,
`Men1`, `Women1`, `People7`, `Vehicle`). They are in **Don Miguel's RTP**
(June 2000), which is the one used outside Japan: his translation of RPG
Maker 2000 brought its own translated RTP, with files he added that don't
exist in the Japanese one —`Future1-3`, for example—. EasyRPG's free RTP
**is no good**: it is a replacement with different art and other names
(`Actor1-4` instead of `Chara1-4`). What an RTP is in general: [The
RTP](../../reference/rpgmaker/rtp.md).

It isn't in the repository, for the same reason as the original game —it
isn't ours to redistribute—: it is read from the folder `RTP_DIR` says. To
restore it, from `RTPE.EXE` (a RAR self-extractor):

```sh
7z x -oRTP-tmp RTPE.EXE && mv RTP-tmp/Data/RTP "$RTP_DIR" && rm -rf RTP-tmp
```
