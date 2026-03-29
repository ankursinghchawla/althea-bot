---
name: upcoming-shows
description: >
  Find upcoming Grateful Dead-related live shows in a region — cover bands,
  tribute acts, Dead & Company, solo projects, associated acts, festivals.
slash_command: "/shows"
triggers: []
max_tokens: 4096
---

# Upcoming Shows

The user wants to find upcoming live shows related to the Grateful Dead
in their area or a specified region.

---

## Workflow

### Step 1: Identify the Region

The user provides a city, state, region, or general area (e.g., "Bay Area",
"NYC", "Pacific Northwest", "near Austin"). If they don't specify, ask.

### Step 2: Research

Use `web_search` to find upcoming shows. Search for combinations of:

- "Grateful Dead tribute" / "Dead cover band" + [region] + "upcoming shows"
- "Dead and Company" / "Bob Weir" / "Phil Lesh" / "Billy Strings" + [region] + "tour dates"
- Specific well-known tribute acts: Dark Star Orchestra, Joe Russo's Almost Dead (JRAD),
  Grateful Shred, Dead & Co, Golden Gate Wingmen, Melvin Seals & JGB
- "Grateful Dead festival" + [region] + current year
- Check jambase.com, songkick.com, bandsintown.com for aggregated listings

Search at least 2-3 sources to get a reasonable picture.

### Step 3: Present Results

Use the format in FORMAT.md. Group by date, closest first.

---

## What Counts as "Dead-Related"

- **Direct lineage**: Dead & Company, solo projects by living members (Bob Weir,
  Mickey Hart, Bill Kreutzmann)
- **Tribute/cover bands**: Dark Star Orchestra, JRAD, Grateful Shred, Cubensis,
  Stella Blue's Band, etc.
- **Extended family**: Billy Strings, Melvin Seals & JGB, Golden Gate Wingmen,
  Oteil Burbridge solo, etc.
- **Festivals with Dead-adjacent lineups**: Lockn', Peach Fest, etc.

Do NOT include acts with no Dead connection just because they're jam bands.

---

## Anti-Hallucination

- Only list shows you found in search results with real dates and venues
- Never invent show dates, venues, or lineups
- If you can't find shows in a region, say so honestly — suggest checking
  jambase.com or bandsintown.com directly
- Include ticket/info links when available
- Note if a show's status is unconfirmed or part of a rumored tour
