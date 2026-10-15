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

The file names were in Spanish, as they were written, until 2026-10-12,
when they got English ones made from their titles. An old citation
—`decisiones/<name>.md`, in a commit or an old task— is looked up in the
redirect table of `book.toml` (see [Contributing](../contributing/README.md)).

## The project

- [RPG Maker 2000 PLUS](rm2k-plus.md)
- [First the whole game, then the quality](first-the-whole-game-then-the-quality.md)
- [The game is playable without MSU-1](the-game-is-playable-without-msu-1.md)
- [The MSU-1 is required only when the ROM does not reach](the-msu-1-is-required-only-when-the-rom-does-not-reach.md)
- [The cartridge goes to 8 MB](the-cartridge-goes-to-8-mb.md)
- [The tools split from ABL, into two repos](the-tools-split-from-abl.md)
- [data/ is the resolved view](data-is-the-resolved-view.md)
- [The binary emitter ships with a sourcemap](the-binary-emitter-ships-with-a-sourcemap.md)
- [A long case at zero proves nothing](a-long-case-at-zero-proves-nothing.md)
- [RAM is placed by the linker](ram-is-placed-by-the-linker.md)

## Events and the interpreter

- [Events trigger with two bits](events-trigger-with-two-bits.md)
- [The active page is frozen until the refresh](the-active-page-is-frozen-until-the-refresh.md)
- [The refresh runs at three moments](the-refresh-runs-at-three-moments.md)
- [The action key looks at both cells](the-action-key-looks-at-both-cells.md)
- [A door is a touch page](a-door-is-a-touch-page.md)
- [A door to the same map doesn't reload the map](a-door-to-the-same-map-doesnt-reload-the-map.md)
- [Running out of the teleport budget is an error](running-out-of-the-teleport-budget-is-an-error.md)
- [ConditionalBranch: five of the twelve kinds](conditional-branch-five-of-the-twelve-kinds.md)
- [CallEvent is compiled inline](call-event-is-compiled-inline.md)
- [CallEvent into a shared body](call-event-into-a-shared-body.md)
- [The test page switches itself off](the-test-page-switches-itself-off.md)

## Move routes

- [Move route command 9, towards the hero](move-route-command-9-towards-the-hero.md)
- [Move route commands 26 and 27 on the hero](move-route-commands-26-and-27-on-the-hero.md)
- [Move route command 34 on the hero](move-route-command-34-on-the-hero.md)
- [Diagonals went on events, until the other games](diagonals-go-on-events.md)
- [Walking through walls also applies to jumps](walking-through-walls-also-applies-to-jumps.md)

## Graphics and memory

- [Every event is drawn](every-event-is-drawn.md)
- [A graphic that doesn't fit isn't drawn](a-graphic-that-doesnt-fit-isnt-drawn.md)
- [The possible leaders are an approximation](the-possible-leaders-are-an-approximation.md)
- [The possible leaders share one CGRAM slot](the-possible-leaders-share-one-cgram-slot.md)
- [The timer has no palette of its own](the-timer-has-no-palette-of-its-own.md)
- [Poses are uploaded on the fly](poses-are-uploaded-on-the-fly.md)
- [Translucent events are baked](translucent-events-are-baked.md)
- [Translucent events don't use color math](translucent-events-dont-use-color-math.md)
- [Large pictures in mode 1](large-pictures-in-mode-1.md)
- [The grid lives in WRAM](the-grid-lives-in-wram.md)

## Audio

- [A single sample bank](a-single-sample-bank.md)
- [The playing track wins, and the sound effects wait](the-playing-track-wins-and-the-sound-effects-wait.md)
- [Boot is sized for the boot package](boot-is-sized-for-the-boot-package.md)
