---
memory_layer: session
update_mode: append
role: "Session handoff notes — useful context that is not yet stable enough for base docs"
read_when: "resuming after a long session, handoff between agents"
not_for: "stable decisions (-> DECISIONS), stable rules (-> CONVENTIONS), completed explorations (-> archive/)"
---

# Short Memory

Use this directory for context that is useful to the next session but not stable
enough for base docs.

## Use When

- A long session needs a handoff note.
- Current understanding is useful but still tentative.
- The next Agent should inherit context that is not yet a decision.

## Do Not Store

- Stable project status. Use `STATUS.md` or `PROGRESS.md`.
- Stable decisions. Use `DECISIONS.md`.
- Long-term rules. Use `CONVENTIONS.md`.
- Completed retrospectives. Use `archive/`.

## Naming

- `YYYYMMDD_topic.md`
- `session_<id>_topic.md`
