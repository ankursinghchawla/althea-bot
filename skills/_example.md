---
name: Example Skill
triggers:
  - "example"
  - "show me an example"
max_tokens: 1024
---

This is where format instructions go. Everything below the frontmatter gets
appended to Althea's system prompt when a message matches any trigger.

Triggers are case-insensitive substring matches against the user's message.
If any trigger phrase appears in the message, this skill activates.

max_tokens is optional (defaults to 1024). Set higher for skills that produce
longer output like dossiers.

To add a new skill: create a new .md file in this directory. No code changes needed.
