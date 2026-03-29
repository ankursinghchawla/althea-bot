---
name: Heady Five
slash_command: "/heady"
triggers:
  - "heady five"
  - "heady 5"
  - "top versions"
  - "top 5 versions"
  - "top five versions"
  - "best versions"
max_tokens: 2048
---

The user is asking for the top 5 versions of a Grateful Dead song, sourced from
HeadyVersion.com — the community's definitive ranking site for Dead performances.

## What to do

1. Search headyversion.com for the song to find the community's top-ranked versions.
2. Present the **top 5** (not 10) versions, ranked by community vote.
3. For each version, include:
   - **Date and venue** (verify date against jerrybase.com)
   - **Why it's ranked** — what makes this version special (musical qualities, historical significance, context)
   - **A curated piece of real user commentary** from HeadyVersion threads — something vivid that captures why heads love this version. If you can't find real commentary, say what the community consensus is instead. Never fabricate quotes.
4. After the top 5, add a brief "Honorable mention" — one more version that just missed the cut, with a one-line note on why it's worth hearing.

## Format

Keep it punchy. Each entry should be 2-4 sentences max (not counting the commentary).
Use this structure:

*1. [Date] — [Venue], [City]*
[Why this version is special — 2-3 sentences]
> "[Real user commentary or community consensus]"

## Rules

- Verify all dates and venues against jerrybase.com
- HeadyVersion rankings shift over time — note "as of current rankings" if appropriate
- If you cannot find HeadyVersion data for a song, say so honestly and offer your best knowledge of consensus top versions from the broader community instead
- Never fabricate user quotes. Paraphrase community sentiment if you can't find exact commentary.
- Keep the whole response under 400 words
