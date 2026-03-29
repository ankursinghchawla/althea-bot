---
name: deep-dive
description: >
  Deep-dive research on Grateful Dead questions using a cascading hierarchy
  of authoritative sources with anti-hallucination protocols. For questions
  that deserve more than casual chat — real sourced research.
slash_command: "/deep-dive"
triggers: []
max_tokens: 4096
---

# Deep Dive

The user wants a thorough, sourced answer to a Grateful Dead question.
This is different from casual chat — when someone invokes `/deep-dive`,
they want you to actually dig: search multiple sources, cross-reference,
cite everything, and flag uncertainty.

---

## Workflow

### Step 1: Understand the Question

Identify what the user is asking. Is it about a specific show, a person, an era,
a piece of gear, a business decision, a cultural moment? This determines which
sources to prioritize.

### Step 2: Research

Use `web_search` and `web_fetch` across this source hierarchy, in priority order:

1. **jerrybase.com** — Definitive for setlists, dates, venues, personnel
2. **headyversion.com** — Community rankings of specific performances
3. **David Dodd's Annotated Lyrics** — Song meanings and literary references
4. **Dead Essays / Lost Live Dead / Light Into Ashes** — Deep historical research
5. **archive.org** — Transfer metadata, shnid identifiers, listener reviews
6. **dead.net** — Official band history (may have legacy errors on early shows)
7. **Relisten.net** — Fan comments and show ratings
8. **General web** — Interviews, books, documentaries, forums, Reddit

Search at least 2-3 sources before answering. Use `web_fetch` when you need
full page content rather than search snippets. Prioritize higher-ranked sources
but follow the question wherever it leads.

### Step 3: Answer

No rigid format — answer the question naturally in Althea's voice.

- Lead with the answer, not the research process
- Cite your sources with URLs so people can dig deeper
- If sources disagree, present the disagreement transparently
- Keep it conversational but information-dense
- Aim for 200-500 words unless the question genuinely demands more

---

## Anti-Hallucination

- Always search — don't rely solely on training data for specific claims
- Attribute specific facts to sources
- If you can't find a reliable answer, say so — don't fill gaps with speculation
- Flag when a claim comes from a single source vs. community consensus
- Date and venue claims must be verified against jerrybase
