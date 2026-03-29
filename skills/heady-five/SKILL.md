---
name: heady-five
description: >
  Top community-ranked versions of a Grateful Dead song from HeadyVersion.com.
  Defaults to 5, but user can request any number (e.g., /heady 3 Dark Star).
slash_command: "/heady"
triggers: []
max_tokens: 4096
---

# Heady Five

The user is asking for the top 5 versions of a Grateful Dead song, sourced from
HeadyVersion.com — the community's definitive ranking site for Dead performances.

---

## Workflow

### Step 1: Identify the Song

The user provides a song title. Confirm the song and proceed.

### Step 2: Research

1. Use `web_search` to find the song's HeadyVersion page URL
   (typically `headyversion.com/song/[id]/grateful-dead/[song-name]/`)
2. Use `web_fetch` on that URL to read the full page — the actual ranked
   list, vote counts, and user commentary. Search snippets are not enough;
   you must fetch the page to get the real rankings.
3. Verify all dates and venues against jerrybase.com

**Source hierarchy:**
1. **headyversion.com** (fetched page) — Primary for rankings and voter commentary
2. **jerrybase.com** — Verify dates, venues, and personnel
3. **archive.org** — Listener reviews for additional color

### Step 3: Generate Output

The user may specify a number (e.g., "/heady 3 Dark Star"). If they do,
return that many versions. If no number is specified, default to 5.
After the list, add one **Honorable Mention** that just missed the cut.

---

## Anti-Hallucination

- Verify all dates and venues against jerrybase.com
- HeadyVersion rankings shift over time — note "as of current rankings" if appropriate
- If you cannot find HeadyVersion data for a song, say so honestly and offer
  consensus top versions from the broader community instead
- Never fabricate user quotes. Paraphrase community sentiment if you can't find
  exact commentary.
- If a version's ranking rationale isn't clear from sources, describe what's
  known about the performance era and context rather than inventing musical descriptions
