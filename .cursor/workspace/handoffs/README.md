# handoffs

The living session snapshot is `handoff.md` in this folder. `fly-onboard`
reads it at session start. `fly-handoff` updates it **in place**. Completed
plans move to `workspace/archive/`, not extra dated handoff files.
