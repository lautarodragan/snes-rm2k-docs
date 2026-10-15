# Events

Every event page that can be compiled travels in the cartridge as
**bytecode**, and that bytecode has three owners that don't step on each
other:

```text
rm2k-snes/bytecode/       declares it: each opcode, its number and the bytes it
                                carries, in `src/events.rs`
rm2k-snes/events/         emits it: `rm2k-snes-events`, in Rust;
                                `compile_command`, one case per RM2k command
runtime/interpreter*.s    runs it: `run_code` and one `.proc op_*` per opcode
```

**The interpreter reads it from WRAM, not from the cartridge**, since
2026-10-01: it travels as LZ2 and is decompressed with the grid, behind it
(see [Maps](maps.md)). Since the next map takes that place, a page that
keeps running after a `Teleport` to another map —a cutscene that jumps and
keeps talking, and every case in the test suite— takes its bytecode along
to `CODE_CARRY`, and the hero's forced route is copied whole: see
`code_carry_before` in `runtime/decompress.s`. Jumps inside a page
are relative to where it starts, so moving it is moving a pointer.

**A map's block is laid out by the converter**: each page's bytecode and,
behind it, its own route's commands, and the page table points at each
with 24 bits. Since 2026-10-15 **two pages with the same bytes point at the
same code**, and two identical routes too (`lay_out_code` in
`rm2k-snes/convert/`). It holds because nothing in the runtime depends on
where a page is: besides the relative jumps, nothing writes the block, and
what tells two pages apart —a parallel's saved state, the refresh, the
action key— is the page's place in the table, `page_ofs`, never its code
pointer. **A routine that compared code pointers to know which page is
running would break it.**

The declaration is a `macro_rules!`, `bytecode!`: it gives one constant per
opcode, which the compiler takes with a `use`, and the table from which
`rm2k-snes-assemble` writes `event_opcodes.inc` into the cartridge's
directory, on every build. Until 2026-10-02 the declaration was a TOML file
in `snes/protocol/`, and from it came, generated and committed, the
Rust module, the `.inc` in `runtime/` and a Python module the ABL
tests read the bytecode with; since that day none of them reads it, and
`test_abl_side.py` makes sure of it. It is in English because nothing in
there knows about this game. The compiler is in English for the same
reason, and its README says what it receives and what it answers; the
converter, `rm2k-snes-convert`, calls it twice. Until 2026-09-29 it was
`tools/port/events.py`, whose constants and models stayed for the tests, in
`tests/harness/events.py` in the ABL port. **A new opcode is declared there
and nowhere else**: the number used to be chosen by the compiler and reach
the interpreter inside `mapdata.inc`, and that is how two branches chose
the same one without git seeing anything.

**On the ROM side, a new opcode is its `.proc` and nothing more.**
`run_code`'s dispatch is a `jmp (table, x)` and the table comes from the
same declaration —the `EVENT_HANDLERS` macro in `event_opcodes.inc`—, with
a rule for the name: the handler of `OP_X` is called `op_x`, and if it
doesn't exist the ROM doesn't assemble. That requires the numbers to stay
contiguous from 0, and the declaration doesn't compile if there are gaps.
Until 2026-09-25 the dispatch was a chain of `cmp`/`bne`/`jmp`, one link
per opcode, and it was the point where two branches that each added one
collided.

**A page is emitted only if all its commands can be run.** `compile_page`
stops —`Stop::Cannot`— and the event is left without code: running half a
script would leave the game in a state that doesn't exist, and the
comparison wouldn't see it: the golden is a capture of the ROM itself. For
the same reason, an event with a condition we don't know how to evaluate is
left out entirely: without knowing which page is active, running the wrong
one is worse than running none.

From that comes the only class of error that is fixed **from the outside**
and not by touching code: a page that teleports to a map the cartridge
doesn't carry is not emitted, and the event is drawn, stepped on, and does
nothing. That is why the converter names the missing maps of each page that
falls out for this reason: of all the reasons a page falls out, it is the
only one fixed by adding the map to the ROM.

The command codes the converter decides all this with come from liblcf and
from nowhere else: the compiler's `codes.rs` is held against the names in
Ditto's schema, which is generated from liblcf. When they were written from
memory —in the filter that recognized doors, which no longer exists— three
were wrong, and two of those were `PlayBGM` and `ChangeSpriteAssociation`:
the filter accepted as doors events that change the music and the hero's
sprite. **The comparison can't see that class of error**, because a wrong
list compiles a wrong ROM and the golden is the capture of that ROM. It is
checked by reading against liblcf, not by running.

## The mechanics that aren't an opcode

What the interpreter needs around it: who triggers a page, which one is
active, who blocks whose way, and what happens while the screen is black.
Again, the reason is in the comment of each routine.

**The ROM does the mechanics, and the table says where.** There was a time
when each of these lines was written twice, in assembly and in Python, and
the second column was the other program; that program no longer exists.
What is left outside the ROM is the converter, `rm2k-snes-convert`, and the
stages it asks —the compiler, `wally`, `rm2k-snes-mapdata`,
`rm2k-snes-screens`—, in Rust, which compile what the routine later reads:
the pages, the routes, the palettes, the glyphs. When there is something
like that, the third column names it; when the mechanic belongs entirely to the console, there is nothing to
name and a dash goes there.

And what does **not** go here anymore: a Python function nobody calls, left
as "the written definition" of what the ROM does. It is documentation
shaped like code, it doesn't run, no test touches it, and it goes stale
without anyone noticing. The reason for each mechanic goes in the comment
of its routine.

| Mechanic | in `runtime/` | who compiles it, or who measures it |
| --- | --- | --- |
| Stepping on an event, and stepping on it at the end of a forced route —a door is that: a touch page with a `Teleport` inside— | `try_touch`, `action_in_cell` | — |
| Talking to an event with the action key | `try_action`, `queue_by_action` | — |
| An event's touch (trigger 2): touch from the hero's side, and an event on the hero's layer whose step the hero refuses | `queue_by_action`, `collide_with_hero` | `pages::triggerable`, in the compiler |
| A page waiting its turn is one bit per event, not a queue | `mark_waiting` | — |
| Which page is active, frozen until the refresh | `pick_pages`, `apply_pages` | — |
| The page's own routes, and the speed they bring | `page_routes`, `animate_ev_route` | `route::own`, in the compiler |
| The movement types —random, vertical, horizontal, toward the hero and away from him—: a route of one command that repeats, and the step it decides | `walk_choose`, `walk_blocked`, `walk_may_take`, in `walk_by_type.s`, from `ev_route_frame` | `route::own` and `ROUTE_BY_TYPE`, in the compiler |
| The route frequency, and facing the hero | `step_route`, `toward_hero`, `after_step`, `after_turn` | `wait_after_step`, `wait_after_turn`, in `rm2k-snes-mapdata` |
| Frequency goes up and down in the middle of a route (orders 30 and 31) | `step_route` | `route::min_frequency`, in the compiler |
| Diagonals, and which way they leave the character facing: an event's and, since 2026-10-14, the hero's | `cell_allowed_diag`, `face_diagonal`, `try_diagonal` | — |
| The relative turns (16 to 20) and moving forward (11), from where the character faces | `turn_relative`, `facing_now`, `forward` and `relative` in `step_route` | — |
| On the hero, what looks at the hero looks at himself: toward is down and away is up | — | `route::on_hero`, in the compiler |
| Changing the graphic in the middle of a route (order 34) | `load_route_graphics`, `refresh_npc` | `Graphics`, in the compiler |
| Collision with events | `cell_blocked`, `event_crossable` | — |
| The graphic follows the page, and the tile rules over the terrain | `page_graphic`, `pass_with_event`, `fit_npc` | `drawable_npcs`, in `wally` |
| Events drawn with a chipset tile | `load_npcs` | `drawable_npcs`, in `wally`; the sheet is drawn by `rm2k-render`, as a library of `wally` |
| The ones that are also opaque and fixed: baked into the map, with no row to draw | `build_oam` skips the hidden row | `baking::bakeable`, in `wally` |
| The teleport fade, with the map loading inside the black | `start_fade`, `fade_tick` | `fade_ramp`, and the `FADE_*` constants, in `rm2k-snes-mapdata` |
| The cap on chained teleports | `JUMPS_MAX` and its uses | enforced by `tests/rpgmaker/test_jumps.py` in the ABL port |
| The screen turns on in vblank and nowhere else | `flush_video` | — |
| The message window, placed by HDMA where `MessageOptions` asks —top, middle or bottom, with background or without— | `build_hdma`, `msg_place`, `msg_hdma_build`, `msg_start`, `msg_ptr_next`, `msg_letter` (the DTE pairs) | `rm2k-snes-screens`, which builds it with `rm2k-render` as a library, and `Messages` and `OP_MESSAGE_OPTIONS` in the compiler |
| Text composed on the fly, with the glyphs already pre-rendered | `message_tick`, `compose_char`, `prime_line` | `font_prerender` in `rm2k-snes-screens` |
| The waits in the middle of a box —`\.`, `\!` and the second-long one, backslash and bar—: the box is cut at the wait and shown, and composed again from the cut line when it is over | `msg_wait_mark`, `msg_hold_tick`, `msg_line_start`, in `message_waits.s` | `WAIT` and `Messages::add_waiting` in the compiler; `wait_mark` in `rm2k-snes-text` |
| A literal backslash, RM2k's `\\`: it is a mark in the lines, like a wait, and draws the font's backslash. `\V[n]` and `\N[n]` also go through the same escapes in a choice's options and in the box before an `InputNumber` | `units` draws the mark as an ordinary letter | `backslash_mark` in `rm2k-snes-text`; `with_variables`, `with_names` and `choice_boxes` in the compiler |
| Boot always lasts the same | `BOOT_FRAMES` | run by `Session` in `tests/harness/console.py` in the ABL port |
| Lost frames are counted | `count_lost` | read from WRAM by `Session.lost_frames` |
| Music doesn't wait for the loop: it goes in a vertical IRQ | `irq_music`, `IRQ_LINE` | — |

What makes the loop fit in one frame —FastROM, the precomposed glyphs, the
product table of the flash, the cheaper rain— doesn't change what is drawn
or when, and so it is checked without touching anything else: the goldens
and the tests come out the same.
