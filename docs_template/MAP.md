---
memory_layer: scaling
update_mode: patch
role: "Navigation map — where concepts, features, and artifacts live in the codebase"
read_when: "locating implementation, tracing artifact origin, feature-to-file mapping"
not_for: "term definitions (-> GLOSSARY), current status (-> STATUS/PROGRESS)"
---

# Map

Map concepts, features, artifacts, and user-facing outputs to implementation
files, entry points, inputs, and generated outputs.

In engineering projects, this typically maps features/modules to directories
and entry points. In research projects, this typically maps figures, tables,
and results to scripts, data inputs, and output paths.

| Concept / Artifact / Feature | File or Entry Point | Inputs / Outputs | Notes |
|---|---|---|---|
| `<name>` | `<path>` | `<path>` | `<note>` |

## Rules

- Keep this file as pointers and mappings, not prose.
- Prefer stable paths and canonical entry points.
- If a mapping changes, update this file with the code change.
