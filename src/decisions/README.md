# Decisions

Decisions that were made and still hold.

One page per decision: **what was decided, why, and what was measured to
decide it**. They are the ones you need to know so as not to redo them or
contradict them, and that is why they live apart from the tasks: they
aren't half-done work, they are the floor the work stands on. What stays
here is the decision and its reason; **how it was reached is in the
record** —the `git log` of the repos, which is there for that—. When a
decision protects one specific line of code, its reason lives in that
line's comment and isn't repeated here.

What does **not** go here: what we would like to do and nobody is doing,
which is the wishlist of tasks in the-advocate-work; where the ROM doesn't do
what RM2k does, which is [the divergences](../divergences/README.md); and
what is half done today, which is the tasks in progress. If a decision
stops holding because a later one replaced it, **it isn't edited
silently**: it is changed saying which one replaced it, or it is deleted
and the commit message tells it.

The decisions of **A Blurred Line** —what its cartridge carries, what is
done with its content— are in
[their own section](../ports/abl/decisions/README.md), under the port.
From 2026-10-02 to 2026-10-10 they lived in the game's repo, with a copy of
the mixed ones in both; that day they came back together with the rest, and
in the book they are separated again. Mixed ones —an engine rule measured
on ABL— are here.

The file names are kept in Spanish, as they were written, so that the
references to `decisiones/<name>.md` in the code and in the tasks still
find them by name.

## The project

- [RPG Maker 2000 PLUS](rm2k-plus.md)
- [First the whole game, then the quality](primero-el-juego-entero-despues-la-calidad.md)
- [The game is playable without MSU-1](el-juego-se-juega-sin-msu-1.md)
- [The MSU-1 is required only when the ROM does not reach](el-msu-1-obligatorio-si-la-rom-no-alcanza.md)
- [The cartridge goes to 8 MB](el-cartucho-pasa-a-8-mb.md)
- [The tools split from ABL, into two repos](las-herramientas-se-separan-de-abl.md)
- [data/ is the resolved view](data-es-la-vista-resuelta.md)
- [The binary emitter ships with a sourcemap](el-emisor-binario-sale-con-sourcemap.md)
- [A long case at zero proves nothing](un-caso-largo-en-cero-no-prueba-nada.md)

## Events and the interpreter

- [Events trigger with two bits](los-eventos-disparan-con-dos-bits.md)
- [The active page is frozen until the refresh](la-pagina-activa-se-congela-hasta-el-refresco.md)
- [The refresh runs at three moments](el-refresco-corre-en-tres-momentos.md)
- [The action key looks at both cells](la-tecla-de-accion-mira-las-dos-celdas.md)
- [A door is a touch page](una-puerta-es-una-pagina-de-contacto.md)
- [A door to the same map doesn't reload the map](una-puerta-al-mismo-mapa-no-recarga-el-mapa.md)
- [Running out of the teleport budget is an error](agotar-el-presupuesto-de-teletransportes-es-un-error.md)
- [ConditionalBranch: five of the twelve kinds](conditional-branch-cinco-de-doce-clases.md)
- [CallEvent is compiled inline](call-event-se-compila-en-linea.md)
- [CallEvent into a shared body](call-event-a-un-cuerpo-compartido.md)
- [The test page switches itself off](la-pagina-de-prueba-se-apaga-sola.md)

## Move routes

- [Move route command 9, towards the hero](orden-9-de-ruta-hacia-el-heroe.md)
- [Move route commands 26 and 27 on the hero](ordenes-de-ruta-26-y-27-sobre-el-heroe.md)
- [Move route command 34 on the hero](la-orden-34-sobre-el-heroe.md)
- [Diagonals go on events](las-diagonales-van-sobre-eventos.md)
- [Walking through walls also applies to jumps](atravesar-paredes-vale-para-el-salto.md)

## Graphics and memory

- [Every event is drawn](se-dibujan-todos-los-eventos.md)
- [A graphic that doesn't fit isn't drawn](un-grafico-que-no-entra-no-se-dibuja.md)
- [The possible leaders are an approximation](los-lideres-posibles-son-una-aproximacion.md)
- [The possible leaders share one CGRAM slot](los-lideres-comparten-una-ranura-de-cgram.md)
- [The timer has no palette of its own](el-cronometro-no-tiene-paleta-propia.md)
- [Poses are uploaded on the fly](las-poses-se-suben-en-caliente.md)
- [Translucent events are baked](los-translucidos-van-horneados.md)
- [Translucent events don't use color math](el-color-math-no-se-usa.md)
- [Large pictures in mode 1](las-imagenes-grandes-en-modo-1.md)
- [The grid lives in WRAM](la-grilla-vive-en-la-wram.md)

## Audio

- [A single sample bank](un-solo-banco-de-muestras.md)
- [The playing track wins, and the sound effects wait](el-tema-que-suena-gana-y-los-efectos-esperan.md)
- [Boot is sized for the boot package](el-arranque-esta-dimensionado-para-el-paquete-de-arranque.md)
