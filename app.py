import os
import re
import glob
import logging

import yaml
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Slack app (Events API / HTTP mode) ---
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

ALTHEA_SYSTEM_PROMPT = """\
You are Althea, speaking in a Slack workspace with a small group of Grateful Dead fans.
You are chatting casually — not writing dossiers or processing tapes.
Keep responses conversational, warm, and concise (1-3 paragraphs unless someone asks
a deep question that deserves more). Use Slack-friendly formatting (*bold*, _italic_,
bullet points) when it helps.

---

You are **Althea** — named for the Garcia/Hunter song about a woman who tells it like
it is. You're the world's foremost authority on the Grateful Dead, combining the
academic rigor of a musicologist with the obsessive detail of a lifelong tape trader.
You've been in the community since the beginning — you *were* the community, or at
least the part of it that kept the records.

You speak the language fluently: "modal jamming," "polyphonic counterpoint," "Type II
improvisation," "the Godchaux years," "Betty Board," "shnid." You know the difference
between a Healy mix and a Miller transfer. You can date a show by the setlist alone.
You've heard every circulating source of every show worth hearing, and you have
opinions about all of them.

Your voice:
- Quietly brilliant — you know more than anyone in the room, and you never need to
  prove it. Your expertise shows in the precision of your words, not in volume.
- Genuinely warm — you're kind to everyone. This isn't naivety — it's a choice.
- Academic but passionate — precise vocabulary, but your enthusiasm for the music is
  always palpable.
- Expert vocabulary — Dead-specific terminology used fluently and naturally, never to
  impress, just because it's the right word.
- Accurate above all — never make claims you can't verify. If uncertain, acknowledge
  it. Your credibility is the only currency that matters.

Example phrases:
- "This is a March '73 show — right in the sweet spot of the Europe tour hangover,
  when they were playing with that loose, exploratory energy."
- "The Dark Star from this show is... well, I'd need to verify before I call it
  legendary. Let me think about what I know."
- "Per-track personnel for a '66 show? That's Garcia, Weir, Lesh, Kreutzmann, and
  Pigpen. No exceptions — they didn't have guests yet."

Anti-hallucination rules:
- Gaps are better than guesses. If you don't know, say so.
- Don't fabricate setlists, dates, or personnel.
- If you're uncertain about a specific performance detail, flag it rather than
  asserting it as fact.
- The Dead community is deeply knowledgeable and will catch errors.

You have access to web search and web fetch. Use search to find information and
fetch to read full page content when you need more detail than search snippets
provide. For example, search HeadyVersion to find a song's page URL, then fetch
that page to read the actual rankings and commentary. Use these tools freely to
look up setlists on jerrybase.com, find recordings on archive.org, check show
details, verify facts, and research anything you're not 100% certain about.
When you cite a source, include the URL so people can check it themselves.

IMPORTANT: Never narrate your research process. Do not say things like "Let me
search for..." or "Based on my research..." — just deliver the answer directly.

If a request is ambiguous or you need clarification, ask. For example, if someone
says "/show 3/15" without a year, ask which year. If "/heady Fire" could be
"Fire on the Mountain" or "Estimated Prophet > Fire," ask which song. Don't guess.
"""

# Server-side tools — Claude decides when to use these automatically
WEB_SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
}
WEB_FETCH_TOOL = {
    "type": "web_fetch_20250910",
    "name": "web_fetch",
    "max_uses": 3,
}
TOOLS = [WEB_SEARCH_TOOL, WEB_FETCH_TOOL]

# --- Skill loader ---
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "skills")


def load_skills():
    """Load skills from skills/[skill-name]/SKILL.md directories."""
    skills = []
    for skill_path in sorted(glob.glob(os.path.join(SKILLS_DIR, "*/SKILL.md"))):
        skill_dir = os.path.dirname(skill_path)
        with open(skill_path) as f:
            content = f.read()
        # Parse YAML frontmatter
        if not content.startswith("---"):
            continue
        _, fm, body = content.split("---", 2)
        meta = yaml.safe_load(fm)

        # Load FORMAT.md if it exists
        instructions = body.strip()
        format_path = os.path.join(skill_dir, "FORMAT.md")
        if os.path.exists(format_path):
            with open(format_path) as f:
                instructions += "\n\n---\n\n" + f.read().strip()

        skills.append({
            "name": meta.get("name", os.path.basename(skill_dir)),
            "triggers": [t.lower() for t in meta.get("triggers", [])],
            "slash_command": meta.get("slash_command", "").lower(),
            "max_tokens": meta.get("max_tokens", 1024),
            "instructions": instructions,
        })
    logger.info(f"Loaded {len(skills)} skill(s): {[s['name'] for s in skills]}")
    return skills


SKILLS = load_skills()


def match_skill(text):
    """Check if a message matches any skill slash command (anywhere in the text).
    Returns (skill, cleaned_text) or (None, text).

    Supports flexible placement:
      /heady Dark Star
      tell me the top 3 dark stars /heady
      /heady tell me the top 3 dark stars
    """
    text_lower = text.lower().strip()
    for skill in SKILLS:
        cmd = skill["slash_command"]
        if not cmd:
            continue
        if cmd in text_lower:
            # Remove the slash command from the text, wherever it appears
            # Use case-insensitive replacement
            import re as _re
            cleaned = _re.sub(_re.escape(cmd), "", text, count=1, flags=_re.IGNORECASE).strip()
            logger.info(f"Skill matched: {skill['name']} (command: {cmd})")
            return skill, cleaned or text
    return None, text


# Cache the bot's own user ID to identify its messages in threads
BOT_USER_ID = None


def get_bot_user_id(client):
    """Fetch and cache the bot's own Slack user ID."""
    global BOT_USER_ID
    if BOT_USER_ID is None:
        resp = client.auth_test()
        BOT_USER_ID = resp["user_id"]
    return BOT_USER_ID


def strip_mention(text):
    """Remove <@UXXXXX> mention tags from message text."""
    return re.sub(r"<@[A-Z0-9]+>\s*", "", text).strip()


def get_thread_messages(client, channel, thread_ts, bot_id):
    """Fetch thread history and convert to Claude message format."""
    result = client.conversations_replies(
        channel=channel, ts=thread_ts, limit=20
    )
    messages = []
    for msg in result["messages"]:
        if msg.get("subtype"):  # skip system messages
            continue
        role = "assistant" if msg.get("user") == bot_id else "user"
        text = strip_mention(msg.get("text", ""))
        if text:
            messages.append({"role": role, "content": text})

    # Claude requires messages to start with "user" role
    while messages and messages[0]["role"] != "user":
        messages.pop(0)

    # Claude requires alternating roles — merge consecutive same-role messages
    merged = []
    for msg in messages:
        if merged and merged[-1]["role"] == msg["role"]:
            merged[-1]["content"] += "\n" + msg["content"]
        else:
            merged.append(msg)

    return merged


def extract_response_text(response):
    """Extract text from Claude response, handling web search result blocks."""
    parts = []
    for block in response.content:
        if block.type == "text":
            parts.append(block.text)
    return "".join(parts)


def ask_althea(messages, skill=None):
    """Send messages to Claude with Althea's persona, web search, and optional skill."""
    system = ALTHEA_SYSTEM_PROMPT
    max_tokens = 4096
    if skill:
        system += f"\n\n---\n\n## Active Skill: {skill['name']}\n\n{skill['instructions']}"
        max_tokens = skill.get("max_tokens", 4096)

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=messages,
        tools=TOOLS,
    )
    return extract_response_text(response)


# --- Deduplication: skip Slack retries ---
_seen_events = set()
_seen_events_max = 1000


def is_duplicate(event):
    """Return True if we've already processed this event (Slack retry)."""
    event_id = event.get("client_msg_id") or event.get("ts")
    if not event_id:
        return False
    if event_id in _seen_events:
        logger.info(f"Skipping duplicate event: {event_id}")
        return True
    _seen_events.add(event_id)
    # Prevent unbounded growth
    if len(_seen_events) > _seen_events_max:
        _seen_events.clear()
    return False


@app.event("app_mention")
def handle_mention(event, client, say):
    """Respond when someone @mentions Althea in a channel."""
    if is_duplicate(event):
        return
    bot_id = get_bot_user_id(client)
    channel = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])

    try:
        text = strip_mention(event.get("text", ""))
        skill, cleaned_text = match_skill(text)

        if event.get("thread_ts"):
            messages = get_thread_messages(client, channel, thread_ts, bot_id)
        else:
            messages = [{"role": "user", "content": cleaned_text}]

        if not messages:
            return

        response_text = ask_althea(messages, skill=skill)
        say(text=response_text, thread_ts=thread_ts)

    except Exception as e:
        logger.exception("Error handling mention")
        say(
            text=f"I got a little lost in the jam there — something went wrong. Try again?\n\n_Debug: {type(e).__name__}: {e}_",
            thread_ts=thread_ts,
        )


@app.event("message")
def handle_dm(event, client, say):
    """Respond to direct messages."""
    # Only handle DMs, ignore bot messages and subtypes (edits, deletes, etc.)
    if event.get("channel_type") != "im":
        return
    if event.get("bot_id") or event.get("subtype"):
        return
    if is_duplicate(event):
        return

    try:
        text = strip_mention(event.get("text", ""))
        if not text:
            return

        skill, cleaned_text = match_skill(text)
        messages = [{"role": "user", "content": cleaned_text}]
        response_text = ask_althea(messages, skill=skill)
        say(text=response_text)

    except Exception as e:
        logger.exception("Error handling DM")
        say(text=f"Something went sideways — try again in a moment?\n\n_Debug: {type(e).__name__}: {e}_")


# --- Flask adapter for HTTP mode ---
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(port=port)
