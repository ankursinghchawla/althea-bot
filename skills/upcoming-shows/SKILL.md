---
name: upcoming-shows
description: >
  Find upcoming Grateful Dead-related live shows in a region — cover bands,
  tribute acts, solo projects, associated acts, jam rock, festivals.
  This is about FUTURE events, not historical Dead shows.
slash_command: "/upcoming-shows"
triggers: []
max_tokens: 4096
---

# Upcoming Shows

This skill is about UPCOMING LIVE EVENTS happening in the real world.
NOT historical Grateful Dead shows. The user wants to know what Dead-related
acts are playing near them soon.

Date filtering is handled automatically by the system. Focus on finding
shows and formatting output. The valid date range and search months are
injected below — use them in your search queries.

---

## Workflow

### Step 1: Identify the Region

The user provides a city, state, region, or general area. If they don't specify, ask.

### Step 2: Research

Use `web_search` to find upcoming shows. Use the search months provided in
the Date Boundaries section below — do NOT search for past months.

Search queries should include the specific month and year, e.g.:
- "Dead tribute band Los Angeles April 2026"
- "jambase grateful dead Los Angeles upcoming 2026"
- "Dark Star Orchestra tour dates 2026"
- "jam band concerts Los Angeles May 2026"

Also try:
- "site:jambase.com grateful dead [region] 2026"
- "site:bandsintown.com [artist] [region]"

Search at least 3-4 queries to get a reasonable picture.

### Step 3: Filter Results

- **Location must be in or near the requested region** (~1-2 hours driving).
  If a notable tour is coming but not to the region, mention it in one line
  at the end.
- **Verify dates are real.** If you're not confident a date is accurate,
  omit it.

### Step 4: Present Results

You MUST use the exact format in FORMAT.md. Do not use prose paragraphs,
bullet-point lists, or section headers like "Notable Tribute Bands" or
"Concert Venues to Watch." Only output structured show entries and the
optional weekly shows section. Skip straight to the output — no preamble,
no commentary, no recommendations beyond the listed shows.

---

## What Counts as "Dead-Related"

- **Direct lineage**: Dead & Company, solo projects by living members
- **Tribute/cover bands**: Dark Star Orchestra, JRAD, Grateful Shred, Cubensis,
  Stella Blue's Band, etc.
- **Extended family**: Billy Strings, Melvin Seals & JGB, Golden Gate Wingmen,
  Oteil Burbridge solo, etc.
- **Jam rock**: Phish, Goose, Pigeons Playing Ping Pong, Eggy, Trey Anastasio Band,
  and similar acts that share the Dead's audience
- **Festivals with Dead-adjacent lineups**: Lockn', Peach Fest, etc.

Do NOT include acts with no Dead or jam connection.

---

## Anti-Hallucination

- Only list shows you found in search results with real dates and venues
- Never invent show dates, venues, or lineups
- If you can't find shows in a region, say so honestly — suggest checking
  jambase.com or bandsintown.com directly
- Note if a show's status is unconfirmed or part of a rumored tour
