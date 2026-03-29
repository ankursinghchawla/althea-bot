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

This skill is about UPCOMING LIVE EVENTS happening in the real world in the
next 30 days. NOT historical Grateful Dead shows. The user wants to know what
Dead-related acts are playing near them soon.

---

## Workflow

### Step 1: Identify the Region

The user provides a city, state, region, or general area (e.g., "Bay Area",
"NYC", "Pacific Northwest", "near Austin", "LA"). If they don't specify, ask.

### Step 2: Research

Use `web_search` to find upcoming shows in the next 30 days. Search for:

- "Grateful Dead tribute" / "Dead cover band" + [region] + "upcoming shows" + current year
- "jam band" + [region] + "concert" + current month/year
- Specific well-known acts + [region] + "tour dates":
  Dark Star Orchestra, Joe Russo's Almost Dead (JRAD), Grateful Shred,
  Dead & Co, Melvin Seals & JGB, Billy Strings, Bob Weir, Mickey Hart,
  Oteil Burbridge, Golden Gate Wingmen, Cubensis, Stella Blue's Band
- Check jambase.com, songkick.com, bandsintown.com for aggregated listings

Search at least 2-3 sources to get a reasonable picture.

### Step 3: Filter Results

Before presenting results, apply these filters:

- **Dates must be in the future.** Today's date is provided in your context.
  Drop anything that has already happened.
- **Location must be in or near the requested region.** "Near" means within
  reasonable driving distance (~1-2 hours). A show in Dallas is NOT near LA.
  If a notable tour is coming but not to the region, you can mention it in
  one line at the end ("_JRAD is touring but no LA dates in the next 30 days_").
- **Verify dates are real.** If you're not confident a date is accurate,
  omit it rather than list a wrong date.

### Step 4: Present Results

Use the format in FORMAT.md. Skip straight to the output — no preamble.

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
