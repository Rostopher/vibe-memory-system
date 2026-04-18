---
memory_layer: base
update_mode: patch
role: "Prompt helper — ask the Agent to explain this memory system for you"
read_when: "user wants Agent to explain docs instead of reading them directly"
not_for: "project content (this is a meta-prompt, not a project doc)"
---

# Ask Your Agent

If you do not want to read the full docs tree yourself, ask the Agent:

```text
Read README.md and docs/MEMORY_MANIFEST.yml first, then explain in Chinese:
1. What this project's memory docs are for
2. Which docs matter most for the current task
3. What should be updated after the task
4. Which facts are stable and which are only session context
```

The Agent should explain the system in terms of the current project, not as a
generic file list.
