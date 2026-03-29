---
name: song-dossier
description: >
  Concise dossier on a Grateful Dead song — origins, meaning, evolution,
  and a version worth hearing. Dense and curated, not padded.
slash_command: "/song"
triggers:
  - "song dossier"
  - "song brief"
  - "tell me about the song"
  - "song history"
max_tokens: 2048
---

# Song Dossier

The user is asking for a concise dossier on a Grateful Dead song — its origins,
meaning, and evolution across the band's career.

---

## Workflow

### Step 1: Identify the Song

The user provides a song title. Confirm the song and proceed.

### Step 2: Research

Conduct web research across these sources:

**Source hierarchy:**
1. **jerrybase.com** — Definitive for debut/final dates, performance counts
2. **David Dodd's Annotated Grateful Dead Lyrics (UCSC)** — Authoritative for
   lyrical analysis and literary/cultural references
3. **Dead Essays / Lost Live Dead / Light Into Ashes** — Historical research
4. **dead.net "Greatest Stories Ever Told"** — Band/insider commentary
5. **headyversion.com** — For the "Worth Hearing" recommendation
6. **Interviews, liner notes** — Band quotes on the song

**Research targets:**
- Writer credits
- Debut and final performance dates + total play count (from jerrybase)
- How the song was written (documented accounts only)
- Documented interpretations (Dodd, band interviews, community consensus)
- How the song changed across eras
- One or two standout versions

### Step 3: Generate Output

Present the dossier using the format in FORMAT.md.

---

## Anti-Hallucination

- Verify debut/final dates and play count against jerrybase.com
- Song meaning must come from documented sources (Dodd, interviews, liner notes)
  — not your own literary analysis
- If you can't verify a claim, omit it
- Dense and curated, not padded — every sentence earns its place
- Keep the whole response under 350 words
