---
name: show-dossier
description: >
  Concise dossier on a Grateful Dead show — verified setlist, era context,
  highlights from community reviews, and where to listen.
slash_command: "/show"
triggers: []
max_tokens: 4096
---

# Show Dossier

The user is asking for a concise dossier on a specific Grateful Dead show —
the context, setlist, and what made it notable.

---

## Workflow

### Step 1: Identify the Show

The user provides a date, venue, or both. Confirm the show and proceed.
If the date is ambiguous (e.g., multiple shows on that date), ask for clarification.

### Step 2: Research

Conduct web research across these sources:

**Source hierarchy:**
1. **jerrybase.com** — Definitive for setlists, dates, venues, personnel
2. **Dead Essays / Lost Live Dead / Light Into Ashes** — Historical context
3. **archive.org** — Transfer metadata, listener reviews, shnid identifiers
4. **Relisten.net** — Fan comments and show ratings
5. **dead.net** — Official history (may have legacy errors on early shows)

**Research targets:**
- Full verified setlist from jerrybase
- Era, tour, and lineup context
- What the community considers the highlights
- Best available source/recording

### Step 3: Generate Output

Present the dossier using the format in FORMAT.md.

---

## Anti-Hallucination

- Setlist must come from jerrybase.com — never reconstruct from memory
- Do not describe specific musical moments you "heard" — you can't hear the tape
- Performance descriptions must be attributed to documented reviews or community consensus
- If a date is disputed or ambiguous, flag it transparently
- Guest musicians must be verified, never guessed
- Keep the whole response under 400 words
