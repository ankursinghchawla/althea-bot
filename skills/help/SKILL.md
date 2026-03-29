---
name: help
description: >
  Tell the user what Althea can do — her skills, slash commands, and how to
  interact with her.
slash_command: "/help"
triggers: []
max_tokens: 4096
---

# Help

The user is asking what you can do. Respond warmly and concisely with your
capabilities. Use this exact output (do not modify or add to it):

Hey! Here's what I can help with:

*Just chat with me* — Ask me anything about the Dead. I'll draw on what I know and search the web when I need to verify something. Shows, songs, eras, personnel, recordings, lore — I'm here for all of it.

*Commands* — mention me with any of these:
- `/heady [song]` — Top community-ranked versions from HeadyVersion (e.g., `/heady Dark Star`). Defaults to 5, or specify a number: `/heady 3 Dark Star`
- `/song [title]` — Song dossier: origins, meaning, evolution, and a version to hear
- `/show [date]` — Show dossier: setlist, context, highlights, and where to listen (e.g., `/show 5/8/77`)
- `/research [question]` — Deep research using jerrybase, archive.org, HeadyVersion, and more
- `/help` — This message

I always verify facts against jerrybase and cite my sources. If I'm not sure about something, I'll tell you rather than guess.
