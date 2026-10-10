# JetBrains

What has to be configured in the IDE to work on the-advocate, on the side of
the machine where the IDE runs.

## Making annotate see through the split of `main.s`

On 2026-09-25 `tools/runtime/main.s` was split into one file per subsystem.
`git blame` only follows each line to its real commit with
`-C --diff-algorithm=histogram` —the reason is in the `AGENTS.md` of
the-advocate-work, in the section "`git blame` y los cambios mecánicos"
(`git blame` and mechanical changes)—; without that,
every line of `tools/runtime/` says "it was the split". JetBrains' annotate
doesn't let you pass options to `blame`, so:

```sh
git config --global diff.algorithm histogram
```

and in the IDE, in the annotate options, turn on the detection of lines
moved between files, which is the `-C`. It is not measured whether those
two are enough: if annotate still says "it was the split", write it down
here.
