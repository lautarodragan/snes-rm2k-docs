# The test game: ABL out, and a game of our own for the engine

> **Measured on 2026-10-02 at `3c83b5d8`** (snes-rm2k), by Leñatero. It is a
> snapshot: the numbers are from that day and this file is not updated. What
> says how many tests there are **today** is `just pruebas`; how to redo each
> count is at the end, in "How it was measured".

The request is taro's, on 2026-10-02: *"start the project of having an RPG
Maker 2000 game for tests"*. Today the tests of what RM2k does live with A
Blurred Line only because they need a game, and the runtime already lives in
`tools/runtime/`. The horizon is the one in
[`decisiones/rm2k-plus.md`](../decisions/rm2k-plus.md): an "RPG Maker 2000
PLUS" that ports other games.

That same day taro set the direction, and this study has it built in:

1. **First, everything of ABL in a single place and out of this repo**, in a
   repo of its own.
2. **Then, 100% original tests in this repo**, without a single reference to
   ABL or a copyrighted asset.
3. The assets: **EasyRPG's RTP replacement**, other free assets he has
   saved, **made-up assets** for now, **sound effects** he can make, and
   **music** from public-domain works with sequences under a declared
   license.


## Summary

* **The inventory.** There are 999 cases in 138 files. By what they test and
  not by folder: **80 files and 605 cases are about the engine** and can be
  written against a synthetic game —44 that only use ABL as a stage and 36
  that need content that has to be made: battles, music, pictures, menu—;
  **20 files and 208 cases check a property over all of a game's content**
  —every map, every animation, the built cartridge— and run on both; and
  **38 files and 186 cases are ABL's** and stay.
* **The game is written as text, and it already builds a cartridge.** A
  two-map game written as an exact Ditto dump —JSON with only what is not
  default, enums by name— built a cartridge that boots and walks, **in
  0.4 s**, with EasyRPG's RTP and the FluidR3 SoundFont. The editor is not
  needed, not even `.lmu`: the converter reads the dump. `ditto pack` turns
  it into binary to open it in the editor or run it in RPG_RT. Getting there
  meant dodging **seven ABL assumptions in the tools**, which are the first
  task of phase 2.
* **The assets almost all suffice.** EasyRPG's RTP replacement is CC0 or
  CC-BY 4.0 file by file and brings ChipSets, CharSets, faces, System, title,
  Game Over, 30 MIDIs and 96 sound effects. It lacks battle backgrounds and
  almost all enemies, which are made. The font is already free (ttyp0 and
  Shinonome, easyrpg-player's), and FluidR3 is MIT. Don Miguel's RTP is no
  good: Enterbrain's license ties it to the editor.
* **Separating ABL is feasible**, and the history is kept with `git
  filter-repo` over the paths ABL had in each era. What ABL takes today from
  `tools/` outside the PATH is two Python packages (`common` and `emulator`)
  and the runtime, which is already found through the installation.
* **ABL gains little in wall-clock time and a lot in maintenance.** Without
  the engine's tests, its test suite goes down from 999 to 394 cases, from
  643 to 351 CPU-s (**−45%**), but from 86.5 to 73 s of wall clock
  (**−16%**): the wall clock is ruled by the few long tests, and those stay.
  It stops maintaining some 206 cases, some 360 goldens and two test
  cartridges: it builds only `release`.
* **The recommendation is five phases**, the first one being the
  separation. The biggest risk is not technical: between phase 1 and 2 the
  engine has no ROM tests of its own, and a change in `tools/` is verified by
  running ABL's from the other repo.


## 1. The inventory

### By folder

    folder         files  cases  CPU-s   the longest
    rpgmaker          85    662    351   14 s
    abl               32    251    179   13 s
    herramientas      21     86    112   25 s
    total            138    999    643

The cases are the ones pytest collects —a parametrized file counts each
parameter—, and the CPU is the sum of what each one took in the run, with 16
processes: the test suite took **86.5 s of wall clock** with the cartridges
already built.

### By what they test

The folder is not enough to decide: `abl/` has engine tests (the MSU-1 ones,
the one about leaders without a graphic) and `rpgmaker/` has tests of ABL
systems (AG7, the portable console). Each file was classified by **what a
game would need to have for the test to keep saying the same thing**:

* **M1, engine with ABL as a stage**: a map to stand on and a test page. The
  test game suffices with maps and events.
* **M2, engine with content to be made**: the rule is the engine's, but it
  needs battles with their troops and battlers, songs with drums or chords,
  pictures, a menu with items, equipment and faces, a title.
* **M3, engine over all the content**: the property holds for any game, but
  the coverage comes from the game being big —every map of the cartridge,
  every animation, the deepest paths of the stack, the built cartridge—.
  **It runs on both games**, and on ABL it is the one that finds the most.
* **J, the game's own**: the playthrough, the scenes, ABL's systems, its
  patches, its forks, its index.

        class  files  cases  CPU-s  lines
        M1        44    327    113   5186
        M2        36    278    155   8755
        M3        20    208    184   3292
        J         38    186    191   5863

What moves is M1 and M2: **80 files, 605 cases, 268 CPU-s and some 13,900
lines**.

### What they use from ABL

**Almost everything is a map and a case.** Of the 289 cases in
`pruebas/casos/`, **206 are used only by engine tests**, 34 only by ABL or
M3 tests, 28 by both, and 21 do not appear written in any test because they
are requested by building the name (`grupo-11-en-<mapa>`, `en-<mapa>`). The
most repeated maps are 5 and 6, which were chosen for being big, open and
silent: that is easy to draw on purpose.

The goldens, counted by the case that names them: of the 649 in
`golden/tanda/`, **some 360 belong to engine tests** (287 from engine cases
and 74 from `test_caminar_golden`), 108 to ABL, 81 shared and 99 that the
name does not let us attribute. It is an approximate count: a golden's name
is not always its case's.

### By file

The maps column lists the ones the test names —through a `Teleport` in its
cases or through `ir_al_mapa`—; the last one says what the test game would
need to have, or why it stays.

| file | cases | CPU-s | class | ABL maps | what is needed, or why it stays |
|---|--:|--:|:-:|---|---|
| `rpgmaker/test_accion_con_ruta.py` | 3 | 1.1 | M1 | — | a map and a page |
| `rpgmaker/test_accion_propia.py` | 2 | 0.6 | M1 | — | a map and a page |
| `rpgmaker/test_autofire.py` | 6 | 3.8 | M1 | 5 | a PLUS feature |
| `rpgmaker/test_borrar_evento.py` | 1 | 0.5 | M1 | — | `EraseEvent` after a `Teleport`; today map 311 |
| `rpgmaker/test_camara.py` | 3 | 0.8 | M1 | 5 | a map and a page |
| `rpgmaker/test_caminar_golden.py` | 75 | 17.6 | M1 | 1, 4, 6, 19, 30, 74, 121 and `grupo-11-en-*` | twelve maps with different ChipSets, doors, priorities |
| `rpgmaker/test_comandos_golden.py` | 58 | 26.4 | M1 | 1, 2, 5, 6, 7, 73, 95, 133, 255, 269, 348 and `grupo-11-en-*` | 49 cases; a picture, a battle animation, a chest with a key |
| `rpgmaker/test_compositor.py` | 2 | 0.5 | M1 | — | a map and a page |
| `rpgmaker/test_condicional.py` | 4 | 0.7 | M1 | 5 and `en-*` | a map and a page |
| `rpgmaker/test_cronometro_condiciones.py` | 2 | 0.6 | M1 | — | a branch and a page condition on the timer |
| `rpgmaker/test_direccion_trabada.py` | 4 | 0.8 | M1 | 6, 9 | a map and a page |
| `rpgmaker/test_elegir.py` | 6 | 1.8 | M1 | 348 | a choice; today the Insta-Shave on map 7 |
| `rpgmaker/test_encuentro_cada_paso.py` | 1 | 0.3 | M1 | 21 | a map with encounters, in its own cartridge |
| `rpgmaker/test_etiquetas.py` | 1 | 0.9 | M1 | 5 | a map and a page |
| `rpgmaker/test_guardar.py` | 7 | 1.8 | M1 | 5, 6 | a save point |
| `rpgmaker/test_hablar_golden.py` | 15 | 9.3 | M1 | 7, 8, 9, 10, 13 | NPCs with page conditions |
| `rpgmaker/test_items.py` | 3 | 0.4 | M1 | 5 | a map and a page |
| `rpgmaker/test_llamada_compartida.py` | 2 | 0.5 | M1 | 5 | a map and a page |
| `rpgmaker/test_lugar_recordado.py` | 5 | 2.1 | M1 | 3, 6, 60, 61 | a map and a page |
| `rpgmaker/test_numero.py` | 3 | 1.6 | M1 | — | an `InputNumber`; today the Drust Camp door |
| `rpgmaker/test_oro.py` | 4 | 3.0 | M1 | 7, 8 | `ChangeGold` and its branch; today two scenes of the game |
| `rpgmaker/test_paralelos.py` | 2 | 0.5 | M1 | 11 | a map with many parallel events (today map 11) |
| `rpgmaker/test_pasos_de_encuentro.py` | 4 | 0.8 | M1 | 5, 66 | maps with encounters |
| `rpgmaker/test_posada.py` | 5 | 2.0 | M1 | 20 | a `ShowInn` |
| `rpgmaker/test_puerta_misma.py` | 2 | 1.2 | M1 | — | a map and a page |
| `rpgmaker/test_rama_grupo.py` | 2 | 0.3 | M1 | 6 | a map and a page |
| `rpgmaker/test_refresco_con_automatica.py` | 1 | 0.1 | M1 | 4 | a map and a page |
| `rpgmaker/test_repeticion.py` | 5 | 1.1 | M1 | 5 | a map and a page |
| `rpgmaker/test_rutas_golden.py` | 41 | 19.6 | M1 | 6, 10, 20, 70 | a big, open, silent map (today map 6) |
| `rpgmaker/test_salto_atraviesa.py` | 1 | 0.6 | M1 | — | a map and a page |
| `rpgmaker/test_salto_bloqueado.py` | 4 | 0.7 | M1 | 6 | a map and a page |
| `rpgmaker/test_salto_colgado.py` | 4 | 0.6 | M1 | 5, 6 | a map and a page |
| `rpgmaker/test_salto_velocidad.py` | 3 | 0.4 | M1 | 6 | a map and a page |
| `rpgmaker/test_saltos.py` | 3 | 1.1 | M1 | 4 | a map and a page |
| `rpgmaker/test_sonido_en_ruta.py` | 3 | 0.6 | M1 | 10 | sound effects |
| `rpgmaker/test_sprite_actor.py` | 4 | 0.7 | M1 | 5, 6 | a map and a page |
| `rpgmaker/test_sustitucion.py` | 2 | 0.9 | M1 | 1, 6 | a map and a page |
| `rpgmaker/test_tecla.py` | 7 | 1.7 | M1 | 5 | a map and a page |
| `rpgmaker/test_teletransporte_contra_rm2k.py` | 4 | 0.5 | M1 | 5 | measure again in RPG_RT: the game packed with `ditto pack` |
| `rpgmaker/test_terreno.py` | 7 | 0.5 | M1 | 5 | a map and a page |
| `rpgmaker/test_variable_en_texto.py` | 1 | 0.4 | M1 | 5 | a map and a page |
| `rpgmaker/test_variables.py` | 5 | 0.9 | M1 | 5 | a map and a page |
| `rpgmaker/test_velocidad.py` | 3 | 1.2 | M1 | 5 | a map and a page |
| `rpgmaker/test_velocidad_con_l_y_r.py` | 7 | 1.9 | M1 | 1, 5, 6 | a PLUS feature |
| `abl/test_msu.py` | 12 | 4.7 | M2 | 3, 5 | MSU-1 tracks for the songs |
| `abl/test_msu_datos.py` | 7 | 17.0 | M2 | 5 | a battle background in the `.msu` |
| `abl/test_msu_efectos.py` | 5 | 2.3 | M2 | 3, 6, 10 | quality sound effects in the `.msu` |
| `rpgmaker/test_batalla.py` | 27 | 15.2 | M2 | 2, 5 | troop, enemies, skills, items; the `rm2k-snes-battle` model |
| `rpgmaker/test_batalla_escena_dibujo.py` | 6 | 3.8 | M2 | 7, 60 | background and battlers |
| `rpgmaker/test_batalla_golden.py` | 13 | 2.8 | M2 | 6, 21 | background, battlers and battle animations |
| `rpgmaker/test_bateria_suena.py` | 1 | 0.2 | M2 | — | a MIDI with drums |
| `rpgmaker/test_curar.py` | 9 | 2.5 | M2 | 5, 20, 23 | a lost battle with a handler; `FullHeal` |
| `rpgmaker/test_equipo_y_habilidades.py` | 7 | 2.9 | M2 | 5, 6 | weapons, armor and skills |
| `rpgmaker/test_eventos_de_tropa.py` | 7 | 6.0 | M2 | 60 | troop pages by turn and HP, hidden enemies |
| `rpgmaker/test_experiencia_dibujo.py` | 12 | 5.7 | M2 | 5, 20 | experience curves and faces |
| `rpgmaker/test_fin_del_juego.py` | 4 | 1.0 | M2 | 21 | the menu and the title |
| `rpgmaker/test_fundido_de_pelea.py` | 3 | 6.0 | M2 | — | a battle with its audio package |
| `rpgmaker/test_fundido_del_tema.py` | 1 | 0.3 | M2 | 3 | a song and sound effects |
| `rpgmaker/test_game_over.py` | 13 | 3.9 | M2 | 5 | a battle without a handler and the Game Over image |
| `rpgmaker/test_guardar_golden.py` | 6 | 1.3 | M2 | 73 | a save point and faces |
| `rpgmaker/test_imagenes_golden.py` | 9 | 5.0 | M2 | 12, 81, 95, 311 | small pictures; today also scenes of the game |
| `rpgmaker/test_imagenes_grandes_golden.py` | 9 | 5.3 | M2 | 12, 49, 69 | full-screen pictures |
| `rpgmaker/test_menu_curar_dibujo.py` | 11 | 2.4 | M2 | 5 | medicines and faces |
| `rpgmaker/test_menu_dibujo.py` | 10 | 2.0 | M2 | 5 | a party with faces |
| `rpgmaker/test_menu_equipo_dibujo.py` | 6 | 1.9 | M2 | 5, 73 | starting and equippable equipment |
| `rpgmaker/test_menu_golden.py` | 20 | 4.1 | M2 | 73 and `grupo-11-en-*` | items, equipment and faces |
| `rpgmaker/test_menu_hp_de_la_pelea_dibujo.py` | 3 | 1.1 | M2 | 5 | a battle and the menu |
| `rpgmaker/test_menu_items_dibujo.py` | 7 | 3.1 | M2 | 5, 73 | sixteen items of several kinds |
| `rpgmaker/test_musica_escrituras.py` | 7 | 30.3 | M2 | — | any songs |
| `rpgmaker/test_musica_paquete.py` | 11 | 4.6 | M2 | 2, 3, 10, 38 | songs per map |
| `rpgmaker/test_musica_reparto.py` | 3 | 0.3 | M2 | — | a song with three-note chords; today `escape_newyork` |
| `rpgmaker/test_sistemas_de_tropa.py` | 12 | 4.8 | M2 | 60 | troop pages that change the party and the HP; today ABL's systems |
| `rpgmaker/test_tema_del_mapa.py` | 3 | 0.8 | M2 | 21 | maps with their own song, an inherited one and none |
| `rpgmaker/test_tema_que_ya_suena.py` | 1 | 0.3 | M2 | 3 | two `PlayBGM`s of the same song |
| `rpgmaker/test_tienda_dibujo.py` | 3 | 2.3 | M2 | 10 | three shops |
| `rpgmaker/test_titulo_dibujo.py` | 15 | 5.9 | M2 | — | a title image |
| `rpgmaker/test_titulo_golden.py` | 4 | 0.6 | M2 | — | a title image |
| `rpgmaker/test_tropa.py` | 2 | 1.4 | M2 | 6 | a switch skill and its troop page |
| `rpgmaker/test_victoria.py` | 6 | 2.1 | M2 | 60 | enemies that drop gold and items |
| `rpgmaker/test_volumen_y_tempo.py` | 3 | 0.8 | M2 | 3 | a song at another volume and tempo |
| `abl/test_lider_sin_grafico.py` | 104 | 14.1 | M3 | — | every map of the game |
| `herramientas/test_bancos.py` | 1 | 0.0 | M3 | — | on the built cartridge: runs with any game |
| `herramientas/test_cartuchos.py` | 6 | 0.3 | M3 | — | on the built cartridge: runs with any game |
| `herramientas/test_destello_paleta.py` | 3 | 3.2 | M3 | — | the leaders' palettes |
| `herramientas/test_encuentros.py` | 10 | 0.9 | M3 | — | the game's encounters |
| `herramientas/test_espacio.py` | 6 | 2.5 | M3 | — | on the built cartridge: runs with any game |
| `herramientas/test_horneados.py` | 3 | 73.7 | M3 | — | the baked events of each map |
| `herramientas/test_lideres.py` | 2 | 2.3 | M3 | — | the game's leaders |
| `herramientas/test_linter.py` | 3 | 1.5 | M3 | — | on the built cartridge: runs with any game |
| `herramientas/test_lz2.py` | 4 | 0.6 | M3 | — | on the built cartridge: runs with any game |
| `herramientas/test_paginas.py` | 10 | 12.2 | M3 | — | Cotorra moves it to `rm2k-snes-events` |
| `herramientas/test_protocolo_contra_el_juego.py` | 5 | 0.8 | M3 | — | all the pages; changes with the bytecodes in Rust |
| `herramientas/test_reservas_de_la_wram.py` | 4 | 0.0 | M3 | — | on the built cartridge: runs with any game |
| `herramientas/test_saltos_entre_bancos.py` | 4 | 6.0 | M3 | 6 | on the built cartridge: runs with any game |
| `herramientas/test_textos_del_juego.py` | 2 | 1.6 | M3 | — | the texts in `data/` |
| `herramientas/test_timer_paleta.py` | 2 | 2.0 | M3 | — | the timer and its palettes |
| `rpgmaker/test_animacion_cuadros.py` | 3 | 8.1 | M3 | 6 | every animation of the cartridge |
| `rpgmaker/test_carga_descomprimida.py` | 6 | 20.1 | M3 | 52 | every map of the cartridge |
| `rpgmaker/test_cores.py` | 21 | 31.5 | M3 | 2, 4, 5, 6, 7, 12, 28, 60, 61, 68, 69, 73, 108, 312 and `grupo-11-en-*` | seventeen cases on two cores |
| `rpgmaker/test_pila.py` | 9 | 2.2 | M3 | 6, 10, 11, 73 and `grupo-11-en-*` | the deepest known paths, which are ABL's |
| `abl/test_capitulo.py` | 5 | 1.4 | J | 5 | the game's own |
| `abl/test_escenas_golden.py` | 29 | 42.3 | J | 2, 3, 5, 7, 8, 9, 10, 17 | the game's own |
| `abl/test_guardar_save_point.py` | 3 | 4.0 | J | 4 | the game's own |
| `abl/test_hover_tram.py` | 2 | 0.5 | J | 32 | the game's own |
| `abl/test_luces.py` | 2 | 0.6 | J | 11 | the game's own |
| `abl/test_mapa_de_debug.py` | 21 | 9.6 | J | — | the game's own |
| `abl/test_mundo.py` | 2 | 0.7 | J | 5 | the game's own |
| `abl/test_paradise.py` | 6 | 2.0 | J | 5 | the game's own |
| `abl/test_piedras.py` | 6 | 2.7 | J | 11 | the game's own |
| `abl/test_puerta_del_10.py` | 2 | 0.5 | J | — | the game's own |
| `abl/test_recorrido_capitulo_golden.py` | 1 | 13.1 | J | — | the game's own |
| `abl/test_recorrido_carrera_golden.py` | 2 | 5.8 | J | — | the game's own |
| `abl/test_recorrido_golden.py` | 2 | 4.4 | J | 3 | the game's own |
| `abl/test_recorrido_lashe_cierre_golden.py` | 3 | 9.6 | J | — | the game's own |
| `abl/test_recorrido_lashe_golden.py` | 6 | 6.8 | J | 37, 38, 47 | the game's own |
| `abl/test_recorrido_lashe_planta_golden.py` | 3 | 4.6 | J | 48 | the game's own |
| `abl/test_recorrido_lashe_wick_golden.py` | 2 | 7.8 | J | 37 | the game's own |
| `abl/test_recorrido_paradise_golden.py` | 1 | 2.3 | J | — | the game's own |
| `abl/test_recorrido_sorbe_golden.py` | 1 | 5.0 | J | — | the game's own |
| `abl/test_recorrido_tangle_golden.py` | 1 | 4.3 | J | — | the game's own |
| `abl/test_recorrido_vipers_golden.py` | 1 | 1.4 | J | — | the game's own |
| `abl/test_recorrido_vipers_otras_ramas_golden.py` | 3 | 3.6 | J | 8 | the game's own |
| `abl/test_recuerdo.py` | 2 | 2.1 | J | — | the game's own |
| `abl/test_sorbe.py` | 4 | 1.0 | J | 5, 69 | the game's own |
| `abl/test_tangle.py` | 2 | 0.5 | J | 5 | the game's own |
| `abl/test_un_ano_antes.py` | 2 | 1.5 | J | — | the game's own |
| `abl/test_video.py` | 4 | 1.8 | J | — | the game's own |
| `abl/test_yun_y_drust.py` | 5 | 1.5 | J | 5 | the game's own |
| `herramientas/test_fork_mapas.py` | 9 | 2.6 | J | — | ABL's forks |
| `herramientas/test_goldens_del_recorrido.py` | 2 | 0.3 | J | — | the playthrough goldens |
| `herramientas/test_indice.py` | 3 | 0.0 | J | — | the index of ABL's tests |
| `herramientas/test_lado_de_abl.py` | 4 | 1.5 | J | — | ABL's boundary |
| `herramientas/test_parches.py` | 2 | 0.0 | J | 6 | ABL's patches |
| `herramientas/test_perillas_repetidas.py` | 1 | 0.0 | J | — | ABL's `rm2k-snes.toml` |
| `rpgmaker/test_ag7_y_la_planta.py` | 8 | 3.1 | J | 60 | AG7-17 and its pieces; the enemy AI, to M2 separately |
| `rpgmaker/test_consola_portatil.py` | 4 | 1.0 | J | 5 | the system of item 81; the generic part is already covered by others |
| `rpgmaker/test_musica_techos.py` | 26 | 40.5 | J | — | ABL's table of ceilings |
| `rpgmaker/test_rutas_auditorio.py` | 4 | 0.4 | J | 18 and `grupo-11-en-*` | a scene on map 18 |

### What changes with Cotorra

When `las-pruebas-sin-opcodes.md` is done, no Python test uses the bytecode:
`herramientas/test_paginas.py` moves to the tests of `rm2k-snes-events`,
`herramientas/test_protocolo_contra_el_juego.py` changes with the bytecodes
in Rust, and `arnes/events.py` (1,391 lines) and `arnes/event_opcodes.py`
(230) shrink or go away. **This plan counts on that**: no step here moves
harness code that speaks the bytecode, and whatever Cotorra leaves as a case
in `pruebas/casos/` is classified like any other.


## 2. Phase 1: ABL out

### What is ABL's today

**All of `rom/`**: 2,024 versioned files.

    rom/data/         31 MB    the game's dump
    rom/parches/      1.9 MB   what was decided about the game
    rom/pruebas/      16 MB    the tests, their cases and their goldens
    rom/justfile, rom/rm2k-snes.toml, rom/pytest.ini

**Outside `rom/`**:

* The root `justfile`: it only imports the one in `rom/`, and it says itself
  that it gets deleted when the repo is split.
* `tools/assembly/entregar.py` (`abl-entregar`): it is ABL's, as
  `tools/README.md` says. It uses `common`.
* `docs/` and `workflow/`: the classification already exists, in
  `workflow/tasks/testing/decisiones-y-divergencias-por-repo.md`. Of
  `decisiones/` and `divergencias/`, 59 go with the tools, 1 with ABL and 6
  are mixed; of `docs/`, ABL's are `inspeccion-integral-del-repo.md` and
  halves of `rtp.md` and `pipeline.md`. `workflow/tasks/` and `ESTADO.md` are
  almost all ABL's.
* `README.md` and `AGENTS.md`: mixed; each repo needs its own. `DITTO.md`
  talks about `data/` as the source of truth, which is ABL's.
* **The comments**: 65 files in `tools/` name ABL, almost all in the runtime
  and in the converter's stages. The tools decision says they stay for now,
  and they are not tests: taro's point 2 does not touch them.

### The history

This repo's history is 2,224 commits. By what they touch:

    only docs, workflow or the root     580
    both things                         529
    merges with no changes of their own 394
    only tools or runtime               530
    only ABL                            191

**`git subtree split --prefix=rom` does not work**: `rom/` has been ABL only
since the move of 2026-09-29 (`3b3f8db6`). Before that, ABL was in `data/`,
`parches/`, `pruebas/` and `pytest.ini` at the root; at the beginning, in
`Maps/`, `Chipset/` and `Charset/` —the game's `.lmu` files and PNGs,
committed on the first day—; and in `juego/`, `tiles/`, `poc/assets/` and
`poc/screenshots/`. And `rom/src/` was the runtime. A split by prefix would
lose everything from before the 29th.

**`git filter-repo` does**, on a clone and with the list of historical
paths: it keeps the 720 commits that touch ABL (191 + 529) and, in the ones
that touched both things, only ABL's half with the whole message. The
messages will name tool changes that are no longer in that repo: that is
acceptable, because the `git log` is the record. `filter-repo` rewrites the
hashes, and it also rewrites the abbreviated hashes that appear in the
messages; the ones that appear in files —`c64e4d9` in `AGENTS.md`, the ones
in the research documents— it does not.

**In this repo, `git rm` and no rewriting.** Rewriting this history would
break every worktree, every branch and every cited hash, and it is not
needed while the repo is private. If it is ever published, then it does
have to be purged: besides ABL's paths, `poc/build/rm2k.sfc` is a ROM built
with ABL, and it is the only art or audio binary outside those paths in the
whole history. The seven PNGs in `tools/` belong to the crates' tests, made
by formula.

`git filter-repo` is not installed; in Arch it is the `git-filter-repo`
package.

### How ABL finds the tools

**The executables are already on the PATH**, and `test_lado_de_abl.py`
enforces that ABL's side does not name `tools/`. What remains:

* **The runtime** is found by `rm2k-snes-cartridges` through the path of the
  checkout it was installed from (`suite.rs` in `rm2k-snes/project/`): it
  keeps working with ABL in another repo as long as the tools checkout
  exists. Embedding it in the binary, as the tools decision says, is what
  lets it be installed without the checkout, and it is not needed for
  phase 1.
* **Two Python packages**: ABL's tests import `common` (16 times) and
  `emulator` (4), with `../tools` in the `pythonpath` of `rom/pytest.ini`.
  It is the only thing ABL takes from `tools/` as source. The proposal is
  for `install` to leave them in a directory of the installation and for an
  executable to say where —for example `rm2k-snes-python-path`—, and for
  ABL's `justfile` to export it in `PYTHONPATH`. ABL still knows only the
  PATH.
* **`install-local`**: the recipe in `rom/justfile` that stops a worktree
  without its `bin/` builds the path of `tools/justfile` with `git
  rev-parse`. It becomes a variable that says where the tools checkout is.
* **The version**: the tools decision asks for the game to declare which
  version of the suite it is built with. With two repos it stops being a
  detail: it is what ties ABL's goldens to an engine.

**The harness leaves whole with ABL in phase 1.** Until the test game
exists, the 999 tests are still ABL's —it is option b) that taro chose in
the tools decision—, so there is no reason to split the harness yet. It is
split in phase 2, when there is another game that uses it.

### What stays in this repo

All of `tools/` —the suite, the runtime, their tests—, the tools' `docs/`
and `workflow/`, and, from phase 2 on, the test game.

### Risks

* **The engine without ROM tests.** Between phase 1 and 2, a change in
  `tools/` is only verified by running `just pruebas` in ABL's checkout with
  the tools of the change. Today the same recipe does that; tomorrow it is a
  step one has to remember to take, and the sub-agents work in worktrees of
  a single repo. **It is the argument for not delaying phase 2.**
* **Two repos in the same environment.** `install-local`, the worktrees and
  the delivery of builds assume one repo today. With two, an agent that
  touches the tools and wants to see ABL needs both copies and has to know
  which one it uses.
* **A forgotten historical path** leaves ABL material in the wrong repo or
  takes history away from ABL. It is checked afterwards: in ABL's repo, `git
  log --all --format= --name-only | sort -u` must have nothing from
  `tools/`; and if this repo is ever purged, the other way around.
* **Merging whatever is in flight.** The agents' branches that touch `rom/`
  have to go in before the cut: afterwards no merge is possible between the
  two repos.


## 3. The test game

### The assets

**Don Miguel's RTP cannot be used.** It is the 2000 English translation of
ASCII/Enterbrain's Japanese RTP. Its `Readme.txt` has no license: it has a
web address and "Do not change any of standard RTP files EVER!!!". What
governs it is Enterbrain's license, which —according to the quote that
circulates in the editor's forums— forbids to "distribute, assign, lease,
sublicense […] the RTP SOFTWARE and/or its data" without written
permission, and ties it to games made with the editor. The README of
EasyRPG's replacement says the same in other words: "original RPG Maker RTP
can't be distributed freely". I did not find the original text of the
license, only those two sources.

**EasyRPG's replacement** (`github.com/EasyRPG/RTP`, cloned at commit
`993d88c` from 2025-04-05) is what taro proposed, and it works:

* **The license** is per file, in its `AUTHORS.md`: each one is **CC0 or
  CC-BY 4.0** (a few also say OGA-BY), with its author. CC-BY requires
  attribution: the test game carries an `AUTHORS` with that of each file it
  uses.
* **What it brings**, in RM2k's format (indexed PNGs, 480x256 ChipSets): 8
  ChipSets (CC0, by Jason Perry), 17 CharSets, 5 FaceSets (CC0), 5 System
  (CC-BY), 4 titles (CC0), a Game Over, 13 panoramas, 3 battle animations,
  **30 MIDIs** and **96 sound effects**.
* **What it does not bring**: battle backgrounds (none) and enemies (one,
  `Hornet`). Those are made.
* **The names are not the RTP's** (`Actor1` instead of `Chara1`): that is
  why `docs/rpgmaker/rtp.md` says it is no good for ABL. For a game made for
  it, it is.
* **The System does not fit as it comes.** The console's message window has
  15 colors, and the text one has to fall before entry 9; the five System
  of the replacement have 32 colors in the window. One has to be drawn for
  the game, or reduced carefully: it is a limit of the console, not of ABL.

**The font is already free.** The port does not use RM2k's: it uses
easyrpg-player's two (`rm2k-snes/text/src/glyphs.rs`), ttyp0 —ttyp0 license,
which allows redistributing and modifying with a rename— and Shinonome's
`rmg2000`, in the public domain. The wishlist's blocker about the system
font does not apply.

**The SoundFont**: ABL uses the Microsoft GS Wavetable Synth, which is not
free. **FluidR3_GM is MIT**, according to the system package that installs
it (`soundfont-fluid`, "custom:MIT"). It is an input from the machine —a
flag—, not something that goes into the repo, but its samples end up in the
cartridge: for the test game's cartridge to be distributable, it has to come
from a free one.

**The music, besides the replacement's 30 MIDIs**: Mutopia publishes scores
of public-domain works with their MIDI, and each piece declares its license
on its page —"Public Domain", CC-BY or CC-BY-SA—. Piece 1's, as checked:
"Public Domain", with LilyPond, MIDI and PDF. The licenses page does not say
explicitly that the license covers the MIDI, so the cleanest thing is to
**choose public-domain pieces and generate the MIDI from their LilyPond**,
which is a mechanical derivative of a source with a declared license. That
covers what taro pointed out: the work being free does not make someone
else's sequence free.

**The sound effects**, the replacement's 96 (almost all CC0), plus the ones
taro makes.

**What is made up**, for now: battle backgrounds, enemies, `ShowPicture`
images, the System. There is precedent in the repo: the small game in
`rm2k-snes/screens/tests/game/` has a System and a FaceSet "made by
formula", and the one in `rm2k-snes/images/` PNGs with gradients and noise.

### How it is written

**As an exact Ditto dump, by hand or generated, and without the editor.** It
was tried by writing a game from scratch —a throwaway generator of about 120
lines—:

* **The converter reads the exact dump**, not only the resolved one: Ditto
  reads both views into the same types (`Dump::open`), and
  `rm2k-snes-convert` accepts as a game a directory that is a dump
  (`dump_dir` in `game.rs`). **No `.lmu` is needed.** `ditto pack` turns it
  into binary —in the experiment, 2,622 bytes in three files— to open it in
  the editor or run it in RPG_RT; `pack` only accepts the exact view.
* **What is written is little.** The exact view omits everything that equals
  its default and writes enums by name: an NPC with two lines of message and
  a `ControlSwitches` are 12 lines. The cases in `pruebas/casos/` already
  have that shape —a list of `event_commands`—, so what is already written is
  reused as is.
* **Tiles are not written by hand.** `.tiles` is one row of ids per line,
  and RM2k's ids (5000 + n for the fixed lower ones, 10000 + n for the upper
  ones, autotiles in 4000-4999) are not readable. The practical thing is to
  draw the map in ASCII with a legend and generate the `.tiles`; in the
  experiment, a 20x15 map is 15 lines of ASCII and 3 legend entries.
* **The cartridge built in 0.4 s**, and it boots: the hero appears, walks,
  and the NPC and the chest are drawn with the replacement's CharSets. A
  20x15 map gives 13 unique tiles and 3 sprite palettes.

**RM2k's editor, if wanted**, fits as a drawing tool and not as a source:
one opens what `ditto pack` gives, draws the map, and `ditto unpack` turns
it back into the exact dump that is versioned. The round trip is exact byte
for byte, which is what makes Ditto reliable for this. I did not try it with
the editor.

**The seven ABL assumptions that showed up** —each one a small task in
Rust—:

1. `rm2k-snes-cartridges` requires **exactly one new map**, the debug one,
   in `patches/manual/nuevos/`, even if `[debug] debug_map` is `false`
   (`cartridges.rs`, in `load`).
2. It requires **a cartridge called `release`** with `cases = "all"`: the
   name of ABL's cartridge is part of the interface.
3. **A single-map game does not build**: the starting map goes separately
   and `--maps` comes out empty.
4. The converter **reads the fifteen sections of the database** and stops
   if one is missing; Ditto does not require them.
5. **System and FaceSet are only looked up in the game**, not in the RTP: in
   the experiment they had to be copied into the game.
6. **`fallback_backdrop` has to be a background the game uses**, even in a
   game without battles.
7. **The window**: the 15-color limit above. To keep going, the experiment
   used an ABL System in the scratch directory, which was not versioned.

And one that is not an assumption: state 1, the death one, which the editor
always creates, is missing. A hand-written game has to start from a minimal
base like that of a new editor project.

What was **not** looked at: the converter's collision statistic gave 100%
open cells even though the map had walls. It may be the experiment's choice
of ids; I did not follow it up.

### How it coexists with what there is

* **The crates' small games** (`tests/game/` of `events`, `screens`,
  `battle`, `images` and `patches`) stay as they are: they test a single
  stage, without a ROM, in milliseconds, and half of them compare against
  the hashes of what the Python produced. The test game is the layer above:
  the whole cartridge in an emulator.
* **The cases** stay as a mechanism: the cartridge brings in the test pages
  and the harness picks one. The test game has its own cases directory;
  ABL's stay with ABL and shrink to the ones its tests use.
* **The goldens are born anew**, and that is the expensive part: a new
  golden defends what the ROM drew the day it was taken, right or wrong.
  Each test that moves has to be looked at once.


## 4. Where it lives

    tools/test-game/
      rm2k-snes.toml    its cartridges: a general one and those that need
                        their own flags, like `test-special` today
      data/             the exact dump
      maps/             the maps in ASCII and their legend, if generated
      ChipSet/, CharSet/, System/, Music/, Sound/, …
                        the assets, copied with their AUTHORS
      cases/            the cases
      tests/            the tests, in pytest
      golden/           its goldens
      build/            not versioned

In English, like everything in `tools/`, and without naming ABL, which is
what taro asked for the tests. **With its assets inside** and not behind a
flag: they are few —the ones used from the replacement plus the made-up
ones—, and that way the game is reproducible with nothing from the machine
except the SoundFont, which comes in through a flag as it does today for the
audio tests (`SOUNDFONT`).

**The harness**: in phase 2 it is split, and the generic part goes to
`tools/` as a Python package. Measured over the 9,411 lines of
`rom/pruebas/arnes/`:

* **ABL's, some 1,960**: `recorrido`, the `tramo_*`, `piedras`, `video`,
  `msu` and `lugares`;
* **the bytecode's, 1,621**: `events` and `event_opcodes`, which are
  Cotorra's;
* **generic, some 5,830**: `consola` —except the `ABLS` signature, which
  comes from the project file, and the title options—, `tanda`,
  `cartuchos`, `dibujo`, `menu`, `pantallas`, `batalla` —except the droid
  and the intro party—, the models (`modelo`, `experience`, `scene`,
  `animation`, `rm2k`, `lcf`, `render_map`), the stage clients and `lz2`. A
  good part is already in English.

It stays in Python: moving it is cheap and rewriting it in Rust is not, and
`tools/emulator/` —the libretro core from Python— is already in `tools/`.
ABL imports it from the installation, like `common` and `emulator` in
phase 1.

**In `tools/justfile`**: a recipe of its own —`test-game`, which builds its
cartridges and runs its tests—, and **not inside `test`**. `test` today is
the Python tests of `tools/tests/`, which run no ROM; the game's need a
libretro core and the SoundFont, like the audio ones, which also go
separately.


## 5. How much it costs, by phase

**Phase 1, ABL out.** It is mechanical and verifiable: in the new repo,
`just cartuchos` gives byte-for-byte identical ROMs and `just pruebas` the
999 in green.

* ABL's repo with `filter-repo` and the historical paths, and `git rm` of
  the same here;
* `common` and `emulator` installable, and ABL's `PYTHONPATH` from an
  executable;
* `abl-entregar` to ABL;
* `docs/` and `workflow/` according to the table that already exists;
* an `AGENTS.md` for each repo.

**Phase 2, the minimal game.** The seven assumptions of section 3 —each a
small change in `cartridge`, `convert` or `screens`, with its test—, a game
of three or four maps, the harness split, and **ten M1 files** moved to try
out the path: `test_variables`, `test_condicional`, `test_etiquetas`,
`test_saltos`, `test_puerta_misma`, `test_velocidad`, `test_tecla`,
`test_terreno`, `test_accion_propia` and `test_camara`, which use map 4, 5
or no map in particular. Meanwhile ABL's version keeps running: it is
deleted when taro has looked at the new goldens.

**Phase 3, the rest of M1.** 34 files, some 290 cases; almost all of it is
writing cases against the test game's maps. Whatever asks for more than a
map —a map with many parallel events, encounters, an `InputNumber`, an inn,
sound effects in a route— is added to the game as needed. The measurement
against RPG_RT (`test_teletransporte_contra_rm2k`) can be redone on the game
packed with `ditto pack`.

**Phase 4, M2.** 36 files, 278 cases, and it is the one that asks for
assets: battles —made-up enemies and backgrounds, the replacement's three
animations—, music —the replacement's MIDIs; one with drums and one with
chords—, small and full-screen pictures, a title, the menu with items and
equipment, and the MSU-1 tracks, which come out of the MIDI with the
SoundFont.

**Phase 5, M3 on both.** The 20 M3 files are written to also run against
the test game; on ABL they stay, because on a big game they are the ones
that find something.

**What ABL gains**, measured by removing the 80 M1 and M2 files from the
test suite:

    cases      999 → 394
    CPU-s      643 → 351   (−45%)
    wall      86.5 → 73 s  (−16%)

The wall clock barely goes down because it is ruled by the long tests,
which stay: `test_horneados` has a 25 s case, `test_carga_descomprimida` one
of 14 and `test_recorrido_capitulo_golden` one of 13. What does go down is
what has to be maintained: **some 206 cases, some 360 goldens**, and **two
of its three cartridges**: `test-special` and `test-encounter-every-step`
carry only cases of engine tests, so ABL builds only `release`. How much
faster `just cartuchos` is without them I did not measure.


## 6. The recommendation

**Feasible, in this order:**

1. **Phase 1, now**, as soon as Cotorra finishes: with the tests without
   opcodes, the harness ABL takes along has no bytecode inside.
2. **Phase 2 right after**, because the risk of phase 1 is the engine
   without tests of its own, and phase 2 cuts it short. Its first task is
   the seven assumptions: without them no game other than ABL builds, and
   that is the PLUS.
3. **Phases 3 to 5 by families**, moving and not duplicating, and with
   ABL's version alive until taro looks at the new goldens.

**The tasks that come out of this**, to `workflow/tasks/todo/`:

* *ABL to its own repo*: the whole of phase 1, with the list of historical
  paths and the check above.
* *What ABL takes from tools as Python*: `common` and `emulator`
  installable, and the `PYTHONPATH` from an executable.
* *The tools without ABL assumptions*: the seven of section 3.
* *The test game*: the directory, the map generator from ASCII, the minimal
  base, the replacement's assets with their `AUTHORS`, the drawn System and
  the `test-game` recipe.
* *The harness in tools*: splitting it, without the bytecode.
* *The engine tests to the test game*, one per phase (2 to 5).
* *Free music*: public-domain pieces from Mutopia, with the MIDI generated
  from their LilyPond; and asking taro for the asset sites he has saved and
  the sound effects he can make.


## How it was measured

All with throwaway scripts, which do not stay in the repo; what they do is
here so it can be redone.

* **The test suite and its times**: `just pruebas --junitxml=<file>`. Each
  `<testcase>` brings its `classname` —`pruebas.rpgmaker.test_x`— and its
  `time`; summed by file and by folder they give the tables. 999 in 86.5 s.
* **What stays in ABL**: the same recipe with an `--ignore=` for each M1 and
  M2 file. 394 in 73 s.
* **What each test uses**: the literals in each file that are case names
  from `pruebas/casos/`, the `Teleport`, `ChangePartyMembers`,
  `EnemyEncounter` and `PlayBGM` of those cases, and the `ir_al_mapa(N`. The
  class of each file is judgment, reading its docstring.
* **The goldens**: each PNG in `golden/tanda/` attributed to the longest
  case that is a prefix of its name.
* **The history**: `git log --format=@%H --name-only --no-renames`, and each
  commit classified by whether it touches paths that were ABL's —the ones in
  section 2—, paths of the tools, or only `docs/`, `workflow/` and the root.
* **The files in `tools/` that name ABL**: `grep -rlI -i -E
  "talan|lashe|a blurred line|\bABL\b" tools --exclude-dir=target`.
* **The synthetic game**: a generator that writes the exact dump —
  `ditto.json` with `"view": "exact"`, `maps.json`, the fifteen sections of
  `db/`, two maps and their `.tiles` from ASCII— and a minimal
  `rm2k-snes.toml`; `ditto pack` over the dump, and `rm2k-snes-cartridges
  --project <game> --game-dir <game>/data --rtp-dir <EasyRPG's replacement>
  --soundfont <FluidR3_GM.sf2> --without-tracks release`. The capture, with
  `tools/emulator/retro.py`.
* **The licenses**: `AUTHORS.md` and `COPYING` of EasyRPG's replacement;
  `Readme.txt` of Don Miguel's RTP; `pacman -Qi soundfont-fluid`;
  `resources/ttyp0/LICENSE` and easyrpg-player's README; Mutopia's licenses
  page and the one for its piece 1.
