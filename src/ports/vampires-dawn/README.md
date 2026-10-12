# Vampires Dawn

## Known issues

What playing the port shows today that the original does not. It is kept
current: whoever fixes one removes its line in the same change. The work
behind each one is a draft or a task in the tasks repository, named here
as text.

* **Healing skills cannot be used from the pause menu**: Skill opens
  each actor's list, but A on a heal does nothing, where the original
  asks on whom and heals. Task:
  [`the-skills-menu`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/the-skills-menu.md).
* **A skill that turns a switch on, used from the pause menu, is
  silent**: the original plays its sound effect. Draft:
  [`switch-skills-from-the-menu-play-no-sound`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/switch-skills-from-the-menu-play-no-sound.md).
* **Ten maps are not in the cartridge**, the world map (1) among them, and
  an event page that would take the hero to one of them is left out
  whole. Drafts: [`map-streams-that-dont-fit-in-wram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/map-streams-that-dont-fit-in-wram.md) (map 1)
  and [`vampires-dawn-maps-that-dont-fit-in-vram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/vampires-dawn-maps-that-dont-fit-in-vram.md) (15, 57, 99,
  150, 165, 225, 399, 402 and 403).
* **Only the message window follows the game's switches between its
  Systems**: the menu, the slot screen and the battle keep `VDBlutsys`, the
  one it starts with. The old man's three styles, the signs in `Wood` and
  the graves in `Stone` show, each over one colour of
  `[windows.background]` —the wood's grain and the stone's joints are
  lost—, and `Stone`'s frame loses most of its 57 colours to fit in the
  starting System's fifteen. See [What `ChangeSystemGraphics` does not model](../../divergences/what-changesystemgraphics-does-not-model.md).
* **An event page that uses any variable past the 256th does nothing**:
  the game names 600, and those pages are left out. Which scenes that
  touches was not looked at. Draft: [`variables-past-256`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/variables-past-256.md).
* **Summoning and turning into a wolf or a bat do nothing**: their
  parallel common events do not compile, nor do `Lebensstatus`, `Geschick`
  and `Staerke`. Drafts:
  [`vampires-dawn-summons-dont-compile`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/vampires-dawn-summons-dont-compile.md)
  and [`vampires-dawn-transformations-dont-compile`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/vampires-dawn-transformations-dont-compile.md).
* **Messages show no faces, and coloured words come out in the plain
  colour.** Tasks: [`draw-the-faces`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/draw-the-faces.md)
  and [`message-colours-and-speed`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/message-colours-and-speed.md).
* **An icon in a message shows as `$` and a letter**: a sign reads "$s
  Graveyard" where RM2k draws one of the ExFont's symbols. Draft:
  [`exfont-glyphs-in-messages`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/exfont-glyphs-in-messages.md).

## Its own System again (2026-10-12)

It builds with `VDBlutsys` and no longer with A Blurred Line's System:
what does not fit in the ROM goes to the `.msu`, which the game requires,
and with its gradient in `[windows.background]` —[The windows' background is the project's, by System](../../decisions/the-windows-background-is-the-projects-by-system.md)— none of its
screens is fused. Until the runtime draws gradients, its windows are the
gradient's average colour.

## Its own System (2026-10-11)

> Measured on 2026-10-11 with the tools of the-advocate's branch
> `tijereta-ventana-tiles` and the ports' of the same name.

- **Its screens fit with its own System, `VDBlutsys`**: the message
  window's frame took 28 tiles of 16, the actor choice's windows 158 of
  64, the shop's 166 of 96, and the item and equipment windows had to
  leave 160 pairs to their text; all of them are fused —[A window with a
  gradient is fused until it fits](../../decisions/a-window-with-a-gradient-is-fused-until-it-fits.md)—.
- **The ROM doesn't**: "a piece of 65536 bytes needs a new bank, and the
  127 banks the cartridge has for data are taken". It keeps A Blurred
  Line's System, which builds.
- **Maps 15 and 150 are not the window's**: "this map can't carry a
  message window" says that no VRAM layout leaves the window's 8 KB next
  to what the map spends —576 background tiles, 436 sprite tiles and 130
  upper ones in map 15—. The window's bank is 256 tiles whatever the
  System.

## As of 2026-10-11, later still: troops past a byte, 21 maps out

> Measured on 2026-10-11 with the tools of the-advocate's branch
> `huron-tropas-dos-bytes` (`5d7d5601`) and the ports' (`29d4c24`). The
> sections after this one are the earlier snapshots of the same day, kept
> as they were.

- **A troop's place in the ROM is a word now**, so a cartridge can carry
  up to 32,768 troops instead of 255. Of the four maps that were out only
  for the troops, **98 and 182 come back**; with 327 or 339 on top of
  them, the build stops on the ROM's 127 banks, the same limit as the
  poses, and they stay out with them. 419 of the 440 maps go in, and the
  cartridge carries 266 troops.
- A battle with a troop past place 255 —troop 332, at place 260— was run
  in snes9x and in bsnes: the right enemy, its HP and, on winning, its
  experience. **Playing it is still to be done.**

## As of 2026-10-11, later: it builds from its project, with 23 maps out

> Measured on 2026-10-11 with the tools of the-advocate `0bb1120a` and the
> ports' branch `aguara-vd-toml`, the game read whole from its `.zip`
> —all 281 songs—. The section after this one is the earlier snapshot of
> the same day, kept as it was.

- **The project builds the release as committed**: `excluded` in
  `vampires-dawn/rm2k-snes.toml` lists 23 maps, each with what stops it,
  and `start_map` is 3, the game's own: its boot fits now. 417 of the 440
  maps go in; 2,227 pieces, 6.5 MB, travel in the `.msu`.
- It boots in snes9x with its `.msu` on map 3's "Skip Intro ?", and
  "Yes" takes it to the first house. **Playing it is still to be done.**
- **Each map alone**, next to map 8: 433 of 440. What stops the seven:
  the message window (15), VRAM (57, 99, 399), the mode 1 panorama (402,
  403) and map 1's grid, 147,232 bytes against 32 KB of WRAM. Since
  2026-10-10 maps 28, 95, 165, 195, 225, 236 and 351 stopped failing
  alone.
- **The whole cartridge asks for more than the maps alone**: with every
  map present, pages that teleport to them compile, more events come in
  and more of them are baked into the background. Map 150 then can't
  carry the window (609 background tiles; alone, 384), and 165 (Uruya)
  and 225 don't fit VRAM.
- **Two limits of the whole game decide the rest.** Its troops: 277,
  where a troop's place in the ROM is a byte (255); four maps whose
  troops nobody else uses are out for that. And what can't go to the
  `.msu`: the characters' poses, 4.3 MB of the ROM's 8, are uploaded on
  the fly and stay; nine maps with poses of their own are out so the
  rest fits the 127 banks. Each of those thirteen was tried back in: none
  returns without breaking the build.
- **Where the poses go**: the converter keeps one bank of twelve poses
  per character *and* per quantization, so a character whose colors come
  out differently in another map takes a bank of its own. 420 of the
  1,239 banks are such repeats. Sharing one quantization per character
  is what would bring back those nine maps, and make room for the others.

## As of 2026-10-11: it requires the MSU-1, and it builds

> Measured on 2026-10-11 with the tools of the-advocate's branch
> `tijereta-vd-msu` (e9a9488f) and the ports' (3a6ca29), with the 82 maps
> that don't convert excluded and starting on map 8, as the earlier
> measurements did. The older snapshots follow, as they were.

- **Its ROM does not reach.** Its data is 12.6 MB for the 7.94 the
  cartridge has —4.3 of them poses, 2.2 the maps' backgrounds—, and
  compressing what is reasonable leaves it about 1 MB short: the poses in
  LZ2 were the only thing that paid off, and they cost A Blurred Line
  frames. taro chose the MSU-1 rather than two cartridges: [the MSU-1 is
  required only when the ROM does not
  reach](../../decisions/the-msu-1-is-required-only-when-the-rom-does-not-reach.md).
- **So its project says `[rom] msu = "required"`, and it builds**: 1,533
  pieces, 5.3 MB, travel in the `.msu` —the maps' streams, the samples,
  the battlers, the panoramas' and big pictures' tiles—, and the rest fits
  in the 127 banks. How, in [the `.msu` file](../../internals/the-msu-file.md),
  "What does not fit in the ROM".
- It starts on map 8 in snes9x and in Mednafen with its `.msu`, and without
  it shows the screen that says the MSU-1 is missing. **Playing it is still
  to be done.**
- **The 82 excluded maps will ask for more ROM** when they convert, and
  what is left to send to the `.msu` is little: what stays in the ROM is
  mostly poses, which are uploaded on the fly.

## As of 2026-10-10

> Measured again on 2026-10-10 ([Other games, measured again](../../research/2026-10-10-other-games-measured-again.md),
> with the tools of the-advocate `1afe6457` and the ports at `951471f`),
> without fixing anything. What follows the next heading is the snapshot
> of 2026-10-06, kept as it was.

- **It still builds no cartridge**, and two limits of the whole game
  showed up: its `Music/` has 281 songs and the track number is a byte
  (unused files count too); and, with a copy of the game that only has the
  125 songs it names, its troops take 470 members where the table is one
  byte. Its start map, 3, doesn't fit the boot either: 46 of the 44 frames.
- With its own System, "the window needs 262 tiles of 256".
- **Each map**, next to map 8 and with the 125 songs: 359 of 440. What
  stops the rest: a song with more than 255 sounds (28), OAM (25), more
  than 120 events (15), VRAM (5), the tile animation in WRAM (4),
  panoramas (3).
- **The pages that compile**: 21,272 of 22,977 on the maps, 14 of 52 common
  events, 0 of 362 troop pages.

## As of 2026-10-06

> **A snapshot as of 2026-10-06.** What the survey of 2026-10-05 found
> ([Other games: the survey](../../research/2026-10-05-other-games.md),
> measured on `24e0223e` of the-advocate) and what the tasks that followed it
> changed up to 2026-10-06. It doesn't describe the port after that date.

The project is `vampires-dawn/` in the-advocate-ports, without MSU-1 and
without tests (see [Ports](../README.md)). **As of 2026-10-06 it doesn't
build a cartridge.**

## The game

440 maps, in English, with 274 MIDI themes and RM2k's own `Harmony.dll`.
It comes in a nested folder, with its installer. No DynRPG, no custom
fonts, an RM2k database.

## What the survey found (2026-10-05)

- **It builds no cartridge**: it uses more variables than the engine's
  256. The compilation of its pages stops there, so their count doesn't
  get measured.
- **Each map alone**: 0 of the 440: more than 256 variables (290 + 92), the
  window (19), OAM (19), battle animations (7), more than 120 events (7).
- **The window**: its System isn't in the game's copy; the survey used the
  RTP's, reduced.
- **The recommendation** put it last: it asks for redoing how the
  variables live —256 one-byte slots and 512 bytes of far RAM— for a
  single game.

## What changed after it (to 2026-10-06)

- **More than 256 variables degrade**: the ones without a slot leave the
  list with a warning, and the pages and events that use them stay out.
  Vampires Dawn gets past this (it names 600 variables). It still doesn't
  build, for other limits: maps with a panorama that doesn't fit, battle
  animations without room in the sprite bank (twenty-five excluded and
  more keep appearing) and the message window, which asks for 262 tiles
  against 256. (Task [`degrade-instead-of-failing`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/degrade-instead-of-failing.md).)
- **Map 1 without its animation box**: a map whose battle animation box
  doesn't fit in any VRAM layout is converted without it, with a warning.
  But that wasn't what stopped map 1: it is 300x300 and its background has
  597 unique 8x8 tiles, against the 544 of the biggest layout. (Task
  [`have-vampires-dawn-map-1-build-without-its-animation-box`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/have-vampires-dawn-map-1-build-without-its-animation-box.md).)
- **Fusing similar tiles**: 18 maps go over the ~544 background tiles (the
  biggest, Uruya, 817; the world, 597). With the fusion the background no
  longer blocks any of them, but what cuts is the sprite bank and the
  layer above —maps 15, 57, 95, 99, 150, 165 (Uruya), 225 and 399—, the
  mode 1 panels of maps 28, 402 and 403, and then the encounters. (Task
  [`merge-similar-tiles-when-the-background-doesnt-fit`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/merge-similar-tiles-when-the-background-doesnt-fit.md).)
- **Encounters with two-byte indices**: it has 779 troops and 136 zones,
  which didn't fit one-byte tables. With that the battle conversion passes
  (with maps excluded); next come the maps with more than 104 NPCs in OAM,
  and then map 1: "a stream of anim_tiles is 27264 bytes and 8192 fit in
  WRAM". (Task [`encounters-with-two-byte-indices`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/encounters-with-two-byte-indices.md).)
- **Uruya in 4bpp**, a throwaway experiment: map 165 alone, in mode 1 with
  both layers at 4bpp, fits in VRAM with room to spare (878 tiles); with
  Adeleine's palettes it keeps 19 distinct colors, with clustering by
  tile 73. (Task [`experiment-uruya-in-4bpp`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/experiment-uruya-in-4bpp.md).)
- **Decorative events as background**: in map 95 (Weg), 209 translucent
  `water1` events paint a river and took the whole sprite bank; baked into
  the background, with a knob. 5,483 candidates in the game, measured
  without looking at the drawing. (Task
  [`decorative-events-into-the-background`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/decorative-events-into-the-background.md).)
- **Four shortcuts**: the condition on direction (37 pages) and the random
  step and moving away from the hero (16 and 48). Map pages that compile,
  from a scan and not a cartridge, went from 21,214 to 21,272 of 22,977;
  what is left in `MoveEvent` is the hero's diagonal moves, about 45
  pages. (Task [`four-shortcuts-for-the-other-games`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/four-shortcuts-for-the-other-games.md).)
- **Parallel common events** don't run in the engine: Vampires Dawn has 35.
  (Task [`dashboard-against-the-whole-of-rm2k`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/dashboard-against-the-whole-of-rm2k.md).)
- **A ChipSet animation that doesn't fit in WRAM** (2026-10-10) keeps the
  tiles that cover the most cells moving and leaves the rest still: in
  maps 236 and 351, 9 of 51 and 5 of 37 water tiles stand still; in map
  1, the world, 100 of its 142, which cover only 4,275 of its 262,866
  water cells. Each in a cartridge with the starting map, map 1 then stops
  at its grid —180,000 bytes, against the 64 KB of WRAM it has—, and 236
  and 351 at the music: 281 songs, and the track goes in a byte. (Task [`tile-animations-that-dont-fit-in-wram`](https://github.com/lautarodragan/the-advocate-work/blob/main/tasks/tile-animations-that-dont-fit-in-wram.md).)

The tasks named here are in `tasks/testing/` in the-advocate-work.
